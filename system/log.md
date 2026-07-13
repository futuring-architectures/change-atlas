# Change Atlas Log

Append-only record of ingestion, reconciliation, linting, and system operations. Git records exact diffs; this log records their purpose.

## [2026-07-13] system | Phase 1 foundation

- Established repository structure, schemas, templates, deterministic CLI, and validation tests.
- Performed no corpus ingestion or synthesis.

## [2026-07-13] system | Complete Evidence provenance metadata

- Required raw file, SHA-256, logical entry index, inclusive line range, and ingest date on every Evidence record.
- Added deterministic raw existence, checksum, coordinate, and ingest-date validation.
- Performed no corpus ingestion or synthesis.
