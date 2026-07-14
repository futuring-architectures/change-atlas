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

## [2026-07-13] evidence | Review and activate Rules pilot

- Reviewed all 13 Evidence records in `🔮 After the Internet → 👩‍⚖️ Rules` and activated the completed batch.
- Extracted 30 atomic claims: four observations, 13 interpretations, nine conceptual claims, and four normative positions; extracted no predictions.
- Recorded one deliberate `complete_no_claims` result for a question-only excerpt rather than converting open questions into assertions.
- Added validation for claim-review state, classification vocabulary, sequential anchors, matching headings, and required scope, date-relevance, and qualification fields.
- Registered entries 228–240 in the manifest; the anthology remains `partial` at 13 of 686 entries.
- Performed no source-metadata recovery or Wiki synthesis.

## [2026-07-13] evidence | Recover Rules source metadata

- Checked the 13 original source pages for canonical URL, author, publisher, and publication date.
- Verified publication dates for 12 records; recorded the Locus Magazine date as inferred because the original page blocked access.
- Marked Kevin Kelly's authorship as inferred from site identity; verified the remaining accessible author and publisher values from their source pages.
- Propagated recovered dates into all 30 claim date-relevance fields without changing excerpts or normalized claim meaning.
- Added validation for verified, inferred, and unresolved source metadata, including date source and precision.
- Performed no Wiki synthesis.

## [2026-07-14] synthesis | Create first Rules Wiki map

- Synthesized the 30 reviewed claims in `🔮 After the Internet → 👩‍⚖️ Rules` into one Hub, two candidate Signals, three candidate Concepts, one candidate Framework, one open Debate, and three open Questions.
- Preserved the distinction between observations, interpretations, conceptual claims, and normative positions in the Wiki prose and citations.
- Added reciprocal typed relationships only where the pilot supported a specific semantic edge.
- Promoted no Trend because the batch lacks multiple independent, defensibly dated Signals for a directional claim.
- Marked uncertainties in event timing, source independence, category boundaries, and one-sided normative coverage for later reconciliation and linting.

## [2026-07-14] system | Adopt portable claim-heading links

- Replaced HTML claim anchors and classification-bearing claim headings with stable `Claim N` Markdown headings.
- Updated canonical Evidence citations to target the exact heading text while preserving claim numbers and reader-facing aliases.
- Extended validation to resolve Markdown headings as internal link targets and require sequential `Claim N` headings on reviewed Evidence.
- Updated Wiki templates, fixtures, tests, and operating guidance so future synthesis uses the portable heading convention.
