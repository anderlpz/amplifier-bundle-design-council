#!/usr/bin/env python3
"""Render this bundle's `hooks-skills-visibility` block exactly as a session would.

This is lane evidence, not repo tooling. It imports the SHIPPED renderer
(`amplifier_module_tool_skills.hooks.SkillsVisibilityHook._format_skills_list`)
and the SHIPPED discovery (`discover_skills`) from the installed
amplifier-bundle-skills cache, points them at this repo's ./skills directory,
and prints the resulting block plus its byte size.

No LLM call, no network, no API spend -- the renderer is pure string assembly
over the SKILL.md frontmatter on disk, so a scratch-session render is exactly
reproducible offline.

Usage:
    python3 docs/lanes/kv98-catalog-design-council/render_catalog.py \
        [--skills-dir PATH] [--tool-skills PATH] [--out FILE]
"""

from __future__ import annotations

import argparse
import glob
import sys
from pathlib import Path

DEFAULT_TOOL_SKILLS_GLOB = (
    "~/.amplifier/cache/amplifier-bundle-skills-*/modules/tool-skills"
)


def _resolve_tool_skills(explicit: str | None) -> Path:
    if explicit:
        return Path(explicit).expanduser().resolve()
    matches = sorted(glob.glob(str(Path(DEFAULT_TOOL_SKILLS_GLOB).expanduser())))
    if not matches:
        sys.exit(
            "could not locate an installed tool-skills module; pass --tool-skills PATH"
        )
    return Path(matches[-1]).resolve()


def main() -> int:
    repo_root = Path(__file__).resolve().parents[3]
    ap = argparse.ArgumentParser()
    ap.add_argument("--skills-dir", default=str(repo_root / "skills"))
    ap.add_argument("--tool-skills", default=None)
    ap.add_argument("--out", default=None)
    args = ap.parse_args()

    sys.path.insert(0, str(_resolve_tool_skills(args.tool_skills)))
    from amplifier_module_tool_skills.discovery import discover_skills
    from amplifier_module_tool_skills.hooks import SkillsVisibilityHook

    skills = discover_skills(Path(args.skills_dir).resolve())
    # Default config: budget mode at DEFAULT_VISIBILITY_TOKEN_BUDGET, which is
    # what a session gets when nothing overrides `visibility:` settings.
    hook = SkillsVisibilityHook(skills=skills, config={})
    block = hook._format_skills_list(skills)  # noqa: SLF001 - the shipped renderer

    print(block)
    print()
    print(f"# skills rendered : {len(skills)}")
    print(f"# block bytes     : {len(block.encode('utf-8'))}")
    print(f"# block chars     : {len(block)}")
    print(f"# est. tokens (len//4): {len(block) // 4}")

    if args.out:
        Path(args.out).write_text(block + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
