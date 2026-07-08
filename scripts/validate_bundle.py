#!/usr/bin/env python3
"""Validate that every skill in the design-council bundle loads with valid
frontmatter and that each skill's `name` field matches its directory name.

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
