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

Phase 1 is the empty foundation. The initial corpus remains unchanged at the repository root. It will be normalized and moved into the managed workflow during Phase 2, after the structural contract has been verified.

See [PROJECT_BRIEF.md](PROJECT_BRIEF.md), [AGENTS.md](AGENTS.md), and [system/schema.md](system/schema.md) for the complete design.

