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

from validate_bundle import EXPECTED_SKILLS, validate_skills  # noqa: E402  # pyright: ignore[reportMissingImports]

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

    def test_expected_skill_set_is_exactly_eight(self):
        self.assertEqual(len(EXPECTED_SKILLS), 8)


if __name__ == "__main__":
    unittest.main()
