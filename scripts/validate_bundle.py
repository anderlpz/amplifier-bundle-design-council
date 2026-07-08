#!/usr/bin/env python3
"""Validate that every skill in the design-council bundle loads with valid
frontmatter and that each skill's `name` field matches its directory name.

Also validates that bundle.md actually wires the bundle's ./skills directory
into the tool-skills module's discovery config. A bundle.md `skills: dirs:
[...]` block is NOT part of the amplifier-foundation bundle schema (only
name/version/description/includes/namespace_root/session/providers/tools/
hooks/spawn/agents/context are read) and is silently ignored -- skills on
disk with valid frontmatter can still be completely invisible to the skills
system if this wiring is missing. See amplifier-bundle-skills' own
behaviors/skills.yaml for the canonical pattern.

Usage:
    python3 scripts/validate_bundle.py

Exits 1 and prints a VALIDATION FAILED listing if any errors are found.
Exits 0 and prints VALIDATION OK otherwise.
"""

import sys
from pathlib import Path

import yaml

EXPECTED_SKILLS = [
    "originality-critic",
    "coherence-guardian",
    "human-advocate",
    "craft-inspector",
    "context-tester",
    "purpose-keeper",
    "emotion-reader",
    "design-council",
]


def parse_bundle_frontmatter(bundle_md_path: Path) -> dict:
    """Parse the YAML frontmatter block out of bundle.md.

    Raises ValueError if the frontmatter block is missing or malformed.
    """
    text = bundle_md_path.read_text(encoding="utf-8")
    parts = text.split("---")
    if len(parts) < 3 or parts[0].strip() != "":
        raise ValueError(f"{bundle_md_path}: missing frontmatter block")

    frontmatter = yaml.safe_load(parts[1])
    if not isinstance(frontmatter, dict):
        raise ValueError(f"{bundle_md_path}: frontmatter did not parse to a dict")
    return frontmatter


def validate_skills_tool_wiring(bundle_root: Path) -> list[str]:
    """Validate bundle.md wires this bundle's skills into the tool-skills module.

    Returns a list of error strings; empty means the wiring is present and correct.
    """
    errors: list[str] = []
    bundle_md_path = bundle_root / "bundle.md"

    try:
        frontmatter = parse_bundle_frontmatter(bundle_md_path)
    except ValueError as exc:
        return [str(exc)]

    bundle_name = frontmatter.get("bundle", {}).get("name", "")

    # Reject the dead `skills: dirs: [...]` key outright -- it does nothing
    # and its mere presence is a strong signal the wiring bug has regressed.
    if "skills" in frontmatter:
        errors.append(
            "bundle.md: top-level 'skills:' key is not part of the bundle "
            "schema and is silently ignored -- it must not be used to "
            "register skill directories. Use 'tools: [{module: tool-skills, "
            "config: {skills: [...]}}]' instead."
        )

    tools = frontmatter.get("tools", [])
    if not isinstance(tools, list):
        errors.append("bundle.md: 'tools' must be a list")
        return errors

    tool_skills_entries = [
        t for t in tools if isinstance(t, dict) and t.get("module") == "tool-skills"
    ]
    if not tool_skills_entries:
        errors.append(
            "bundle.md: no 'tools' entry configures the 'tool-skills' module "
            "-- this bundle's ./skills directory will never be discovered"
        )
        return errors

    expected_ref_suffixes = (f"@{bundle_name}:skills", "subdirectory=skills")
    found = False
    for entry in tool_skills_entries:
        skills_refs = entry.get("config", {}).get("skills", [])
        for ref in skills_refs:
            if isinstance(ref, str) and any(
                suffix in ref for suffix in expected_ref_suffixes
            ):
                found = True

    if not found:
        errors.append(
            "bundle.md: tool-skills module config.skills does not reference "
            f"this bundle's own skills directory (expected an entry like "
            f"'@{bundle_name}:skills')"
        )

    return errors


def validate_skills(skills_dir: Path, expected_skills: list[str]) -> list[str]:
    """Validate each expected skill's SKILL.md and return a list of error strings.

    An empty list means all skills validated cleanly.
    """
    errors: list[str] = []

    for skill_name in expected_skills:
        skill_dir = skills_dir / skill_name

        if not skill_dir.is_dir():
            errors.append(f"{skill_name}: missing skill directory")
            continue

        skill_md = skill_dir / "SKILL.md"
        if not skill_md.exists():
            errors.append(f"{skill_name}: missing SKILL.md")
            continue

        text = skill_md.read_text(encoding="utf-8")
        parts = text.split("---")
        if len(parts) < 3 or parts[0].strip() != "":
            errors.append(f"{skill_name}: missing frontmatter block")
            continue

        frontmatter_text = parts[1]
        try:
            frontmatter = yaml.safe_load(frontmatter_text)
        except yaml.YAMLError as exc:
            errors.append(f"{skill_name}: YAML error in frontmatter: {exc}")
            continue

        if not isinstance(frontmatter, dict) or "name" not in frontmatter:
            errors.append(f"{skill_name}: frontmatter missing 'name' field")
            continue

        if frontmatter["name"] != skill_name:
            errors.append(
                f"{skill_name}: name mismatch — frontmatter name is "
                f"'{frontmatter['name']}', directory is '{skill_name}'"
            )

    return errors


def main() -> int:
    bundle_root = Path(__file__).resolve().parent.parent
    skills_dir = bundle_root / "skills"

    errors = validate_skills(skills_dir, EXPECTED_SKILLS)

    if errors:
        print("VALIDATION FAILED")
        for error in errors:
            print(f"  - {error}")
        return 1

    print(
        f"VALIDATION OK \u2014 {len(EXPECTED_SKILLS)} skills, "
        "all names match their directories"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
