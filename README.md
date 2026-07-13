# Change Atlas

**Futuring Architectures: The Change Atlas** is a living evidence map of technological, organizational, and cultural change.

This repository compiles immutable source material into source-grounded Evidence and a maintained Markdown Wiki. Phase 1 establishes the repository contract, schemas, templates, validation tools, and tests. It deliberately performs no corpus synthesis.

## Architecture

```text
raw/               Immutable source material
evidence/sources/  Verbatim excerpts, metadata, and atomic claims
wiki/              Maintained synthesis and typed relationships
system/            Schemas, templates, manifest, indexes, and logs
tools/wiki         Deterministic repository CLI
tests/             Reference and failure fixtures
```

Evidence records what was encountered. The Wiki compiles what the corpus currently supports. Frames are deferred until the first two layers are operational.

## Quick start

The CLI requires Python 3.9 or newer and has no third-party dependencies.

```bash
tools/wiki doctor
tools/wiki status
tools/wiki validate
tools/wiki index
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

Phase 1 established the validated foundation. Phase 2 begins with a report-only structural audit of the immutable anthology now stored beneath `raw/`:

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

See [PROJECT_BRIEF.md](PROJECT_BRIEF.md), [AGENTS.md](AGENTS.md), and [system/schema.md](system/schema.md) for the complete design.
