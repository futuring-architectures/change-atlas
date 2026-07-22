# Change Atlas

**Futuring Architectures: The Change Atlas** is a living evidence map of technological, organizational, and cultural change.

This repository compiles immutable source material into source-grounded Evidence and a maintained Markdown Wiki. The initial 686-source, 16-collection bootstrap is complete. The Atlas now operates through individual-source ingestion and periodic reconciliation.

## Architecture

```text
raw/               Immutable source material
evidence/sources/  Verbatim excerpts, metadata, and atomic claims
wiki/              Maintained synthesis and typed relationships
system/            Schemas, templates, manifest, indexes, and logs
tools/wiki         Deterministic repository CLI
tests/             Reference and failure fixtures
```

Evidence records what was encountered. The Wiki compiles what the corpus currently supports. Private propositions preserve provisional cross-source hypotheses for continued testing; they are not reader-facing Wiki pages.

## Quick start

The CLI requires Python 3.9 or newer and has no third-party dependencies.

```bash
tools/wiki doctor
tools/wiki status
tools/wiki validate
tools/wiki index
tools/wiki dashboard
tools/wiki bootstrap-audit raw/anthology.md
python3 -m unittest discover -s tests -v
```

Validate the miniature reference Atlas:

```bash
tools/wiki validate tests/fixtures/valid
```

The deliberately invalid fixture should fail and report several issue codes:

```bash
tools/wiki validate tests/fixtures/broken
```

## Current phase

Phase 2 bootstrap is complete. New material now enters through Phase 3 URL-first ingestion. Give the Atlas an article URL and, optionally, the single quote you pinned for newsletter curation:

```bash
tools/wiki ingest https://example.com/article \
  --date 2026-07-21 \
  --quote "Optional verbatim curator pin" \
  --write
```

Preparation captures the accessible article beneath `raw/web/`, hashes it, and creates draft Evidence. The pin preserves why the source caught your attention; atomic claims are extracted separately from the complete article. Pages that require login or client-side rendering fail visibly instead of producing a misleading partial capture.

After metadata and claim review, incremental Wiki maintenance, and proposition assessment, activate the Evidence page and finalize the transaction:

```bash
tools/wiki ingest raw/web/2026-07-21-example-article.md \
  --date 2026-07-21 \
  --finalize \
  --write
```

Finalization requires a valid active Evidence record with completed claim extraction, then records the source, claims, affected Wiki pages, hash, and completion date in the manifest and operational log. Repeating capture or finalization does not duplicate content.

The original anthology was audited with:

```bash
tools/wiki bootstrap-audit \
  raw/thoughtforming-on-digital-transformation-2026-07-10.md \
  --write
```

This command identifies logical entries, inherited H1/H2 taxonomy, exact line ranges, missing quotes, malformed headings, and URL anomalies. It does not create Evidence or Wiki content.

After the audit passes, assign all Evidence identities and destinations deterministically:

```bash
tools/wiki bootstrap-plan \
  raw/thoughtforming-on-digital-transformation-2026-07-10.md \
  --write
```

Create a reviewable Evidence pilot one complete H1/H2 collection at a time:

```bash
tools/wiki bootstrap-evidence \
  raw/thoughtforming-on-digital-transformation-2026-07-10.md \
  --h1 "🔮 After the Internet" \
  --h2 "👩‍⚖️ Rules" \
  --date 2026-07-13 \
  --write
```

The generated pages are drafts: they contain stable IDs, exact raw provenance, editorial placement, unresolved source metadata, and the verbatim excerpt. Claim extraction and classification are a separate interpretive review. Drafts cannot be cited by the Wiki and are not added to the manifest as completed ingestion.

After every page in a collection has been reviewed and activated, register that partial progress:

```bash
tools/wiki bootstrap-register \
  raw/thoughtforming-on-digital-transformation-2026-07-10.md \
  --h1 "🔮 After the Internet" \
  --h2 "👩‍⚖️ Rules" \
  --date 2026-07-13 \
  --write
```

The anthology remains `partial` until all 686 entries are registered; `status` reports partial raw-file progress separately from completed files.

Track all 16 editorial collections in the generated Obsidian-readable dashboard:

```bash
tools/wiki dashboard
```

After synthesizing a collection, generate its Wiki-level editorial review package:

```bash
tools/wiki review-report --collection nature-of-the-firm-governance
```

Metadata checking and atomic-claim extraction are pipeline stages. The human editorial gate applies to the synthesized Wiki delta shown in the review report.

Propositions remain private synthesis memory in `system/synthesis-backlog.json` as `open`, `strengthened`, `qualified`, or `contested` records. Each retains a stable `prp-` identity, cumulative exact Evidence anchors, relevant collections, and an assessment history. `qualified` means that the statement itself expresses the material limitation; a qualifying assessment alone does not justify the status.

During each individual-source ingest, compare the new atomic claims with the private proposition backlog. Add exact claim anchors and record whether the source strengthens, qualifies, contests, resolves, or leaves each materially relevant proposition unchanged. Promote a proposition only when it resolves into an established public Wiki type, and record that page as its resolution target.

See [PROJECT_BRIEF.md](PROJECT_BRIEF.md), [AGENTS.md](AGENTS.md), and [system/schema.md](system/schema.md) for the complete design.
