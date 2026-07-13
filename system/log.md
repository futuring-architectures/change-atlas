# Change Atlas Log

Append-only record of ingestion, reconciliation, linting, and system operations. Git records exact diffs; this log records their purpose.

## [2026-07-13] system | Phase 1 foundation

- Established repository structure, schemas, templates, deterministic CLI, and validation tests.
- Performed no corpus ingestion or synthesis.

## [2026-07-13] system | Complete Evidence provenance metadata

- Required raw file, SHA-256, logical entry index, inclusive line range, and ingest date on every Evidence record.
- Added deterministic raw existence, checksum, coordinate, and ingest-date validation.
- Performed no corpus ingestion or synthesis.

## [2026-07-13] bootstrap | Install raw anthology and structural auditor

- Moved the unchanged anthology into `raw/` with SHA-256 `473b5c17a3d13a184a181dd55a47956c0a1b0dddb4fb8d5652e5077113cb2f6f`.
- Added a deterministic, report-only structural audit command.
- Audited 686 entries across four H1 domains and 16 H2 collections: 685 quote bodies, one blocking missing-quote error, and seven recoverable warnings.
- Performed no Evidence generation or Wiki synthesis.

## [2026-07-13] bootstrap | Finalize corrected raw anthology

- Corrected the malformed heading for entry 562 and supplied the curated quotation for entry 563 before Evidence generation.
- Established the revised raw anthology baseline with SHA-256 `42794efb22e69cef120d7cf5812b79e06dfbeca9904fde60916de94fe2bd036a`.
- Re-audited 686 entries: 686 quote bodies, zero blocking errors, and six recoverable warnings.
- Performed no Evidence generation or Wiki synthesis.

## [2026-07-13] bootstrap | Plan corpus and generate Rules Evidence pilot

- Assigned deterministic Evidence IDs and destinations to all 686 audited entries without duplicating quote bodies in the ingestion plan.
- Generated 13 provenance-complete draft Evidence records for `🔮 After the Internet → 👩‍⚖️ Rules` (global entries 228–240).
- Added exact quote coordinates and validation against the immutable raw excerpt, plus overwrite protection and an active-Evidence claim-anchor gate.
- Preserved the original editorial hierarchy and ordering in the Evidence index.
- Left all pilot records in `draft`; performed no claim extraction, manifest completion, or Wiki synthesis.
