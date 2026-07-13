import subprocess
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TOOLS = ROOT / "tools"
sys.path.insert(0, str(TOOLS))

import atlas_cli  # noqa: E402


class YamlSubsetTests(unittest.TestCase):
    def test_nested_relationships_parse(self):
        parsed = atlas_cli.parse_yaml_subset(
            """
id: sig-abcdef
tags:
  - networks
relationships:
  - type: supports
    target: "[[trend-example]]"
"""
        )
        self.assertEqual(parsed["tags"], ["networks"])
        self.assertEqual(
            parsed["relationships"],
            [{"type": "supports", "target": "[[trend-example]]"}],
        )

    def test_advanced_inline_yaml_is_rejected(self):
        with self.assertRaises(atlas_cli.YamlSubsetError):
            atlas_cli.parse_yaml_subset("tags: [unquoted, values]\n")


class ValidationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.schema = atlas_cli.load_schema(ROOT)

    def test_valid_reference_chain(self):
        pages, issues = atlas_cli.validate_content(ROOT / "tests/fixtures/valid", self.schema)
        self.assertEqual(len(pages), 5)
        self.assertEqual(issues, [])

    def test_broken_fixture_exercises_expected_checks(self):
        _, issues = atlas_cli.validate_content(ROOT / "tests/fixtures/broken", self.schema)
        codes = {issue.code for issue in issues}
        expected = {
            "frontmatter.malformed",
            "field.missing",
            "id.duplicate",
            "type.unknown",
            "link.broken",
            "relationship.unknown",
            "relationship.inverse_missing",
            "evidence.missing",
            "raw.entry_invalid",
            "raw.hash_mismatch",
            "raw.range_invalid",
            "date.invalid",
        }
        self.assertTrue(expected.issubset(codes), sorted(codes))

    def test_indexes_render_deterministically(self):
        pages, issues = atlas_cli.validate_content(ROOT / "tests/fixtures/valid", self.schema)
        self.assertEqual(issues, [])
        first = atlas_cli.render_system_index(pages, ROOT / "tests/fixtures/valid")
        second = atlas_cli.render_system_index(list(reversed(pages)), ROOT / "tests/fixtures/valid")
        self.assertEqual(first, second)
        self.assertIn("## Trends", first)
        self.assertIn("[[wiki/trends/trend-example|Example trend]]", first)


class CommandTests(unittest.TestCase):
    def run_wiki(self, *arguments):
        return subprocess.run(
            [sys.executable, str(TOOLS / "wiki"), "--root", str(ROOT), *arguments],
            check=False,
            text=True,
            capture_output=True,
        )

    def test_validate_command_accepts_reference_fixture(self):
        result = self.run_wiki("validate", "tests/fixtures/valid")
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("Validation passed", result.stdout)

    def test_validate_command_rejects_broken_fixture(self):
        result = self.run_wiki("validate", "tests/fixtures/broken")
        self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
        self.assertIn("relationship.inverse_missing", result.stdout)


if __name__ == "__main__":
    unittest.main()
