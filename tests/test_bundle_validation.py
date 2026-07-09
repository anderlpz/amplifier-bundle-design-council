"""Acceptance gate for Track 1: validate the design-council bundle composes.

Verifies every skill loads with valid frontmatter, each skill's `name` field
matches its directory name, and the expected set of eight skills is complete.

Run directly: python3 tests/test_bundle_validation.py
Or via unittest: python3 -m unittest tests.test_bundle_validation
"""

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))

from validate_bundle import (  # noqa: E402  # pyright: ignore[reportMissingImports]
    EXPECTED_SKILLS,
    validate_skills,
    validate_skills_tool_wiring,
)

BUNDLE_ROOT = Path(__file__).resolve().parent.parent
SKILLS_DIR = BUNDLE_ROOT / "skills"


class TestBundleValidation(unittest.TestCase):
    def test_all_expected_skills_validate_with_no_errors(self):
        errors = validate_skills(SKILLS_DIR, EXPECTED_SKILLS)
        self.assertEqual(
            errors,
            [],
            "Expected no validation errors, got:\n" + "\n".join(errors),
        )

    def test_expected_skill_set_is_exactly_nine(self):
        self.assertEqual(len(EXPECTED_SKILLS), 9)

    def test_skills_are_wired_into_tool_skills_module(self):
        """Regression test for the /design-council discoverability bug.

        A bundle.md `skills: dirs: [...]` block validates fine (every SKILL.md
        has correct frontmatter) but is completely inert -- amplifier-foundation's
        Bundle.from_dict never reads a top-level 'skills' key. Skills on disk
        with perfect frontmatter were invisible to the skills system and
        `/design-council` was never registered as a command because nothing
        told the tool-skills module to discover this bundle's ./skills
        directory. This test fails if that wiring regresses.
        """
        errors = validate_skills_tool_wiring(BUNDLE_ROOT)
        self.assertEqual(
            errors,
            [],
            "Expected bundle.md to wire ./skills into tool-skills, got:\n"
            + "\n".join(errors),
        )


if __name__ == "__main__":
    unittest.main()
