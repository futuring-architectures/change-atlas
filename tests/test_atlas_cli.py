import json
import re
import subprocess
import sys
import shutil
import tempfile
import unittest
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TOOLS = ROOT / "tools"
sys.path.insert(0, str(TOOLS))

import atlas_cli  # noqa: E402
import bootstrap_audit  # noqa: E402
import bootstrap_ingest  # noqa: E402
import steady_ingest  # noqa: E402


class SteadyIngestTests(unittest.TestCase):
    def test_html_capture_prefers_article_and_recovers_metadata(self):
        parser = steady_ingest.ArticleHTMLParser()
        parser.feed(
            """
            <html><head>
            <title>Fallback title</title>
            <meta property="og:title" content="A source title">
            <meta name="author" content="Ada Author">
            <meta property="og:site_name" content="Example Review">
            <meta property="article:published_time" content="2026-07-20T09:00:00Z">
            <link rel="canonical" href="https://example.com/canonical">
            </head><body><nav>Navigation noise</nav><article>
            <h1>A source title</h1><p>This is the first substantive paragraph with enough text.</p>
            <p>This is the second substantive paragraph.</p></article><footer>Footer noise</footer></body></html>
            """
        )
        self.assertEqual(parser.meta["author"], "Ada Author")
        self.assertEqual(parser.canonical_url, "https://example.com/canonical")
        self.assertIn("first substantive paragraph", parser.text())
        self.assertNotIn("Navigation noise", parser.text())
        self.assertNotIn("Footer noise", parser.text())

    def test_url_capture_draft_preserves_optional_pin_and_validates(self):
        article = steady_ingest.CapturedArticle(
            requested_url="https://example.com/story?ref=newsletter",
            final_url="https://example.com/story",
            canonical_url="https://example.com/story",
            title="A useful story",
            author="Ada Author",
            publisher="Example Review",
            published_at="2026-07-20",
            date_precision="day",
            body="First article paragraph.\n\nSecond article paragraph.",
        )
        pin = "The deliberately selected sentence."
        first = steady_ingest.build_capture_draft(article, "2026-07-21", pin)
        second = steady_ingest.build_capture_draft(article, "2026-07-21", pin)
        self.assertEqual(first, second)
        self.assertIn("## Curator pin\n\n" + pin, first.raw_content)
        self.assertIn("> " + pin, first.evidence_content)
        self.assertIn("claim_extraction_status: pending", first.evidence_content)

        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / first.raw_relative).parent.mkdir(parents=True)
            (root / first.evidence_relative).parent.mkdir(parents=True)
            (root / first.raw_relative).write_text(first.raw_content, encoding="utf-8")
            (root / first.evidence_relative).write_text(first.evidence_content, encoding="utf-8")
            pages, issues = atlas_cli.validate_content(root, atlas_cli.load_schema(ROOT))
            self.assertEqual(len(pages), 1)
            self.assertEqual(issues, [])

    def test_url_normalization_drops_fragments_but_keeps_query_identity(self):
        self.assertEqual(
            steady_ingest.normalize_url("HTTPS://Example.COM/story?q=1#section"),
            "https://example.com/story?q=1",
        )
        with self.assertRaises(ValueError):
            steady_ingest.normalize_url("file:///tmp/story.html")

    def test_finalize_registers_valid_active_evidence_and_is_idempotent(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory) / "atlas"
            shutil.copytree(ROOT / "tests/fixtures/valid", root)
            (root / "system/bootstrap").mkdir(parents=True)
            shutil.copy2(ROOT / "system/schema.yaml", root / "system/schema.yaml")
            shutil.copy2(ROOT / "system/collections.json", root / "system/collections.json")
            shutil.copy2(
                ROOT / "system/bootstrap/ingestion-plan.json",
                root / "system/bootstrap/ingestion-plan.json",
            )
            (root / "system/synthesis-backlog.json").write_text(
                '{"schema_version": 1, "propositions": []}\n', encoding="utf-8"
            )
            (root / "system/manifest.json").write_text(
                '{"schema_version": 1, "files": {}}\n', encoding="utf-8"
            )
            (root / "system/log.md").write_text("# Log\n", encoding="utf-8")
            pages, issues = atlas_cli.validate_content(root, atlas_cli.load_schema(root))
            self.assertEqual(issues, [])
            (root / "system/index.md").write_text(
                atlas_cli.render_system_index(pages, root), encoding="utf-8"
            )
            (root / "evidence/index.md").write_text(
                atlas_cli.render_evidence_index(pages, root), encoding="utf-8"
            )

            result = atlas_cli.command_ingest_finalize(
                root, "raw/example.md", "2026-07-21", write=True
            )
            self.assertEqual(result, 0)
            manifest = json.loads((root / "system/manifest.json").read_text(encoding="utf-8"))
            record = manifest["files"]["raw/example.md"]
            self.assertEqual(record["status"], "complete")
            self.assertEqual(record["evidence_id"], "evi-a1b2c3")
            self.assertEqual(record["claim_count"], 1)
            first_log = (root / "system/log.md").read_text(encoding="utf-8")
            self.assertEqual(
                atlas_cli.command_ingest_finalize(
                    root, "raw/example.md", "2026-07-21", write=True
                ),
                0,
            )
            self.assertEqual(first_log, (root / "system/log.md").read_text(encoding="utf-8"))


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

    def test_claim_heading_is_a_resolvable_link_target(self):
        source = ROOT / "tests/fixtures/valid/evidence/sources/source-example.md"
        page, issues = atlas_cli.parse_markdown(source)
        self.assertEqual(issues, [])
        self.assertIsNotNone(page)
        self.assertIn("Claim 1", page.anchors)
        self.assertEqual(
            atlas_cli.split_wikilink("[[source-example#Claim 1|Readable citation]]"),
            ("source-example", "Claim 1"),
        )

    def test_legacy_classification_suffix_in_claim_heading_is_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory) / "valid"
            shutil.copytree(ROOT / "tests/fixtures/valid", root)
            evidence = root / "evidence/sources/source-example.md"
            content = evidence.read_text(encoding="utf-8")
            evidence.write_text(
                content.replace("### Claim 1", "### Claim 1 — observation"),
                encoding="utf-8",
            )
            _, issues = atlas_cli.validate_content(root, self.schema)
            codes = {issue.code for issue in issues}
            self.assertIn("evidence.claim_missing", codes)
            self.assertIn("anchor.broken", codes)

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

    def test_unsupported_evidence_claim_class_is_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory) / "valid"
            shutil.copytree(ROOT / "tests/fixtures/valid", root)
            evidence = root / "evidence/sources/source-example.md"
            content = evidence.read_text(encoding="utf-8")
            evidence.write_text(
                content.replace("- Classification: `observation`", "- Classification: `unsupported`"),
                encoding="utf-8",
            )
            _, issues = atlas_cli.validate_content(root, self.schema)
            self.assertIn("evidence.claim_class_invalid", {issue.code for issue in issues})

    def test_source_metadata_value_and_status_must_agree(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory) / "valid"
            shutil.copytree(ROOT / "tests/fixtures/valid", root)
            evidence = root / "evidence/sources/source-example.md"
            content = evidence.read_text(encoding="utf-8")
            evidence.write_text(
                content.replace("author_status: verified", "author_status: unresolved"),
                encoding="utf-8",
            )
            _, issues = atlas_cli.validate_content(root, self.schema)
            self.assertIn("source_metadata.status_conflict", {issue.code for issue in issues})

    def test_inferred_month_precision_date_is_valid(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory) / "valid"
            shutil.copytree(ROOT / "tests/fixtures/valid", root)
            evidence = root / "evidence/sources/source-example.md"
            content = evidence.read_text(encoding="utf-8")
            content = content.replace("published_at: 2026-01-02", "published_at: 2026-01")
            content = content.replace("date_status: verified", "date_status: inferred")
            content = content.replace("date_precision: day", "date_precision: month")
            evidence.write_text(content, encoding="utf-8")
            _, issues = atlas_cli.validate_content(root, self.schema)
            self.assertEqual(issues, [])


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

    def test_status_counts_heading_anchored_claims(self):
        result = self.run_wiki("status", "--json")
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        expected = sum(
            len(re.findall(r"(?m)^### Claim [1-9][0-9]*$", path.read_text(encoding="utf-8")))
            for path in (ROOT / "evidence/sources").glob("*.md")
        )
        self.assertEqual(json.loads(result.stdout)["atomic_claims"], expected)

    def test_dashboard_is_current(self):
        result = self.run_wiki("dashboard", "--check")
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("CURRENT system/dashboard.md", result.stdout)


class CollectionWorkflowTests(unittest.TestCase):
    def test_tracker_matches_bootstrap_plan(self):
        tracker = atlas_cli.load_collection_tracker(ROOT)
        self.assertEqual(len(tracker["collections"]), 16)
        self.assertEqual(sum(record["entries"] for record in tracker["collections"]), 686)
        governance = next(
            record for record in tracker["collections"]
            if record["id"] == "nature-of-the-firm-governance"
        )
        self.assertEqual(governance["signoff_mode"], "completed")
        self.assertEqual(governance["stage"], "committed")
        self.assertEqual(governance["signed_off_at"], "2026-07-14")
        self.assertEqual(governance["baseline"], "07b8701")
        self.assertEqual(governance["checkpoint"], "daa1adb")

    def test_dashboard_separates_pipeline_from_editorial_signoff(self):
        tracker = atlas_cli.load_collection_tracker(ROOT)
        governance = next(
            record for record in tracker["collections"]
            if record["id"] == "nature-of-the-firm-governance"
        )
        governance["stage"] = "awaiting_editorial_signoff"
        governance["signoff_mode"] = "required"
        pages, issues = atlas_cli.validate_content(ROOT, atlas_cli.load_schema(ROOT))
        self.assertEqual(issues, [])
        rendered = atlas_cli.render_collection_dashboard(ROOT, pages, tracker)
        self.assertIn("Nature of the Firm / 👩‍⚖️ Governance", rendered)
        self.assertIn("Only **awaiting editorial sign-off** requires the editor", rendered)
        governance_line = next(
            line for line in rendered.splitlines()
            if "Nature of the Firm / 👩‍⚖️ Governance" in line
        )
        self.assertIn("| Awaiting Editorial Signoff | Required |", governance_line)
        backlog = atlas_cli.load_synthesis_backlog(ROOT)
        tracked = len(backlog["propositions"])
        unresolved = sum(
            proposition["status"] not in {"promoted", "retired"}
            for proposition in backlog["propositions"]
        )
        self.assertIn(f"- Tracked propositions: {tracked}", rendered)
        self.assertIn(f"- Unresolved propositions: {unresolved}", rendered)

    def test_synthesis_backlog_tracks_governance_propositions(self):
        tracker = atlas_cli.load_collection_tracker(ROOT)
        backlog = atlas_cli.load_synthesis_backlog(ROOT)
        pages, content_issues = atlas_cli.validate_content(ROOT, atlas_cli.load_schema(ROOT))
        self.assertEqual(content_issues, [])
        governance = [
            proposition for proposition in backlog["propositions"]
            if proposition["origin_collection"] == "nature-of-the-firm-governance"
        ]
        networks = [
            proposition for proposition in backlog["propositions"]
            if proposition["origin_collection"] == "after-the-internet-networks"
        ]
        self.assertEqual(len(governance), 4)
        self.assertEqual(len(networks), 6)
        self.assertEqual(
            len({proposition["id"] for proposition in backlog["propositions"]}),
            len(backlog["propositions"]),
        )
        self.assertEqual(
            atlas_cli.validate_synthesis_backlog(ROOT, pages, tracker, backlog),
            [],
        )

    def test_autonomous_committed_report_is_not_editorial_signoff(self):
        tracker = json.loads(json.dumps(atlas_cli.load_collection_tracker(ROOT)))
        networks = next(
            record for record in tracker["collections"]
            if record["id"] == "after-the-internet-networks"
        )
        networks["stage"] = "committed"
        networks["signoff_mode"] = "autonomous"
        networks["checkpoint"] = "abcdef0"
        rendered = atlas_cli.render_collection_review(ROOT, networks, networks["baseline"])
        self.assertIn("editorial_signoff: autonomous", rendered)
        self.assertIn("- Decision: autonomous checkpoint", rendered)
        self.assertIn("- Checkpoint: `abcdef0`", rendered)
        self.assertNotIn("The editor signed off", rendered)

    def test_relevant_collection_requires_backlog_assessment_before_synthesis(self):
        tracker = json.loads(json.dumps(atlas_cli.load_collection_tracker(ROOT)))
        backlog = atlas_cli.load_synthesis_backlog(ROOT)
        pages, content_issues = atlas_cli.validate_content(ROOT, atlas_cli.load_schema(ROOT))
        self.assertEqual(content_issues, [])
        ecosystems = next(
            record for record in tracker["collections"]
            if record["id"] == "nature-of-the-firm-ecosystems"
        )
        ecosystems["stage"] = "synthesis_ready"
        for proposition in backlog["propositions"]:
            if "nature-of-the-firm-ecosystems" in proposition["relevant_collections"]:
                proposition["assessments"] = [
                    assessment for assessment in proposition["assessments"]
                    if assessment["collection"] != "nature-of-the-firm-ecosystems"
                ]
        issues = atlas_cli.validate_synthesis_backlog(ROOT, pages, tracker, backlog)
        self.assertIn("backlog.relevant_unassessed", {issue.code for issue in issues})


class BootstrapAuditTests(unittest.TestCase):
    def test_small_anthology_preserves_taxonomy_and_exceptions(self):
        audit = bootstrap_audit.parse_anthology(
            ROOT / "tests/fixtures/bootstrap/anthology.md",
            "tests/fixtures/bootstrap/anthology.md",
        )
        self.assertEqual(len(audit.entries), 3)
        self.assertEqual(audit.quote_count, 2)
        self.assertEqual(audit.h1_values, ["Domain"])
        self.assertEqual(audit.h2_paths, [("Domain", "Theme"), ("Domain", "Other theme")])
        self.assertEqual(audit.entries[1].source_title, "Two-part title")
        self.assertIn("heading.noncanonical", audit.entries[1].issue_codes)
        self.assertIn("quote.missing", audit.entries[2].issue_codes)

    def test_full_corpus_regression_counts(self):
        audit = bootstrap_audit.parse_anthology(
            ROOT / "raw/thoughtforming-on-digital-transformation-2026-07-10.md",
            "raw/thoughtforming-on-digital-transformation-2026-07-10.md",
        )
        self.assertEqual(audit.raw_sha256, "42794efb22e69cef120d7cf5812b79e06dfbeca9904fde60916de94fe2bd036a")
        self.assertEqual(len(audit.h1_values), 4)
        self.assertEqual(len(audit.h2_paths), 16)
        self.assertEqual(len(audit.entries), 686)
        self.assertEqual(audit.quote_count, 686)
        self.assertEqual(audit.error_count, 0)
        self.assertEqual(Counter(issue.code for issue in audit.issues)["heading.noncanonical"], 2)
        self.assertEqual(Counter(issue.code for issue in audit.issues)["quote.multiline"], 2)

    def test_audit_rendering_is_deterministic_and_omits_quote_bodies(self):
        audit = bootstrap_audit.parse_anthology(
            ROOT / "tests/fixtures/bootstrap/anthology.md",
            "tests/fixtures/bootstrap/anthology.md",
        )
        first = bootstrap_audit.render_json(audit)
        second = bootstrap_audit.render_json(audit)
        self.assertEqual(first, second)
        self.assertNotIn("A normal curated quote", first)
        self.assertIn('"has_quote": true', first)


class BootstrapIngestionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.raw_path = ROOT / "raw/thoughtforming-on-digital-transformation-2026-07-10.md"
        cls.raw_label = "raw/thoughtforming-on-digital-transformation-2026-07-10.md"
        cls.audit = bootstrap_audit.parse_anthology(cls.raw_path, cls.raw_label)
        cls.plan = bootstrap_ingest.build_ingestion_plan(cls.audit)

    def test_full_plan_has_stable_unique_identity_and_collection_positions(self):
        self.assertEqual(len(self.plan.entries), 686)
        self.assertEqual(len({entry.evidence_id for entry in self.plan.entries}), 686)
        self.assertEqual(len({entry.evidence_file for entry in self.plan.entries}), 686)
        rules = [entry for entry in self.plan.entries if entry.curated_h2 == "👩‍⚖️ Rules"]
        self.assertEqual([entry.global_position for entry in rules], list(range(228, 241)))
        self.assertEqual([entry.collection_position for entry in rules], list(range(1, 14)))

    def test_plan_is_deterministic_and_does_not_duplicate_quotes(self):
        first = bootstrap_ingest.render_plan_json(self.plan)
        second = bootstrap_ingest.render_plan_json(bootstrap_ingest.build_ingestion_plan(self.audit))
        self.assertEqual(first, second)
        self.assertNotIn("So much modern antitrust action", first)

    def test_draft_preserves_provenance_taxonomy_and_quote(self):
        source_entry = self.audit.entries[227]
        plan_entry = self.plan.entries[227]
        rendered = bootstrap_ingest.render_evidence_draft(
            self.audit, source_entry, plan_entry, "2026-07-13"
        )
        self.assertIn("status: draft", rendered)
        self.assertIn("claim_extraction_status: pending", rendered)
        self.assertIn(f"raw_entry_index: {source_entry.index}", rendered)
        self.assertIn('  - "🔮 After the Internet"', rendered)
        self.assertIn('  - "👩‍⚖️ Rules"', rendered)
        self.assertIn("> " + source_entry.quote_text, rendered)
        self.assertNotIn('<a id="claim-', rendered)

    def test_draft_writer_is_idempotent_and_refuses_changed_output(self):
        source_entry = self.audit.entries[227]
        plan_entry = self.plan.entries[227]
        content = bootstrap_ingest.render_evidence_draft(
            self.audit, source_entry, plan_entry, "2026-07-13"
        )
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            written, unchanged = bootstrap_ingest.write_evidence_drafts(root, [(plan_entry, content)])
            self.assertEqual((written, unchanged), (1, 0))
            written, unchanged = bootstrap_ingest.write_evidence_drafts(root, [(plan_entry, content)])
            self.assertEqual((written, unchanged), (0, 1))
            target = root / plan_entry.evidence_file
            target.write_text(content + "user edit\n", encoding="utf-8")
            with self.assertRaises(ValueError):
                bootstrap_ingest.write_evidence_drafts(root, [(plan_entry, content)])

    def test_draft_validates_but_activation_requires_completed_claim_review(self):
        source_entry = self.audit.entries[227]
        plan_entry = self.plan.entries[227]
        content = bootstrap_ingest.render_evidence_draft(
            self.audit, source_entry, plan_entry, "2026-07-13"
        )
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            raw_target = root / self.raw_label
            raw_target.parent.mkdir(parents=True)
            shutil.copyfile(self.raw_path, raw_target)
            bootstrap_ingest.write_evidence_drafts(root, [(plan_entry, content)])
            schema = atlas_cli.load_schema(ROOT)
            _, issues = atlas_cli.validate_content(root, schema)
            self.assertEqual(issues, [])
            target = root / plan_entry.evidence_file
            target.write_text(content.replace("status: draft", "status: active"), encoding="utf-8")
            _, issues = atlas_cli.validate_content(root, schema)
            self.assertIn("evidence.claim_pending", {issue.code for issue in issues})
            no_claims = content.replace("status: draft", "status: active").replace(
                "claim_extraction_status: pending", "claim_extraction_status: complete_no_claims"
            )
            target.write_text(no_claims, encoding="utf-8")
            _, issues = atlas_cli.validate_content(root, schema)
            self.assertEqual(issues, [])

    def test_evidence_index_preserves_editorial_collection_order(self):
        schema = atlas_cli.load_schema(ROOT)
        pages, issues = atlas_cli.validate_content(ROOT, schema)
        self.assertEqual(issues, [])
        rendered = atlas_cli.render_evidence_index(pages, ROOT)
        self.assertIn("## 🔮 After the Internet", rendered)
        self.assertIn("### 👩‍⚖️ Rules", rendered)
        self.assertLess(rendered.index("- 1. [["), rendered.index("- 13. [["))


if __name__ == "__main__":
    unittest.main()
