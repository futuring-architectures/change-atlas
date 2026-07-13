# Change Atlas Operating Contract

These instructions govern all work in this repository. The Atlas is a source-grounded knowledge system, not a generic note collection.

## Purpose and layers

Change Atlas compiles curated source material into two maintained layers:

1. `evidence/` records what was encountered and preserves provenance.
2. `wiki/` compiles what the corpus currently supports.

Frames are deferred. Do not introduce a `frames/` layer or active Frame workflow until explicitly requested.

## Non-negotiable rules

1. Treat files in `raw/` as immutable. Never rewrite, reformat, rename, or delete a raw source during ingest.
2. Preserve quotations verbatim. Normalized claims must never replace their source excerpts.
3. Every Evidence record must identify its raw file, exact SHA-256, logical entry number, and inclusive line range.
4. Do not invent missing metadata. Represent unknown author, date, publisher, or canonical URL explicitly as `null` with a corresponding status.
5. Preserve the initial corpus hierarchy and ordering as editorial data. Do not treat it as the only taxonomy.
6. An excerpt is not automatically a Signal. Classify claims before considering promotion.
7. Every substantive Wiki page must cite resolvable Evidence claim anchors unless its type is explicitly exempted by the schema.
8. Maintain typed relationships in frontmatter and readable links in the body. Update reciprocal relationships together.
9. Never promote repeated rhetoric into a real-world Trend without dated observations, independent support, scope, and counter-evidence review.
10. Prefer updating an existing page when new material refines the same object. Create a new page only for a distinct object that other pages would meaningfully link to.
11. Preserve unrelated user changes. Do not delete or bulk-rewrite pages without explicit approval.

## Deterministic versus interpretive work

Use deterministic tooling for:

- discovering files and computing hashes;
- parsing structural Markdown;
- assigning and checking stable identifiers;
- validating frontmatter, links, anchors, and reciprocal relationships;
- generating indexes;
- checking the manifest and preventing duplicate ingestion;
- appending operational records.

Use LLM judgment for:

- extracting and classifying atomic claims;
- deciding whether evidence supports, qualifies, or contradicts existing synthesis;
- proposing Signals, Trends, Concepts, Frameworks, Debates, and Questions;
- choosing between creating a page and updating an existing one;
- explaining uncertainty and scope.

Do not use LLM judgment for bookkeeping that the CLI can perform.

## Page types

- `evidence`: source metadata, verbatim excerpts, and anchored atomic claims.
- `hub`: navigation and synthesis for a topic or editorial domain.
- `signal`: a scoped observation, event, case, or example.
- `trend`: a directional pattern supported by multiple Signals over time.
- `concept`: a named idea with definition, provenance, and distinctions.
- `framework`: a reusable structure with components, steps, axes, or relationships.
- `debate`: a structured comparison of competing positions or interpretations.
- `question`: a tracked research gap or unresolved issue.

Follow `system/schema.yaml` for machine requirements and `system/schema.md` for semantic rules.

## Evidence classification

Atomic claims use one of these classes:

- `observation`
- `interpretation`
- `prediction`
- `normative_position`
- `conceptual_claim`

A claim may be evidence for more than one page, but every use must preserve its original classification and source anchor.

## Relationship maintenance

Use only relationship types declared in `system/schema.yaml`. Targets use Obsidian-style links such as `[[recommendation-media]]` or `[[source-example#claim-1]]`.

When adding a relationship:

1. confirm the target exists;
2. add the declared inverse relationship to the target page;
3. add a readable relationship or evidence link in the page body;
4. run `tools/wiki validate`.

An apparent contradiction may instead be a difference in timeframe, scope, definition, values, or evidential standard. Record those distinctions before applying `contradicts`.

## Ingest workflow — later phases

Phase 1 contains no ingest command. When ingestion is implemented, each transaction must:

1. hash the raw file and check `system/manifest.json`;
2. parse without modifying the raw source;
3. create or update normalized Evidence;
4. extract atomic claims with stable anchors;
5. compare claims against existing Wiki pages;
6. update or create the minimum necessary Wiki surface;
7. validate schema, links, citations, and inverse relationships;
8. update the manifest and append to `system/log.md` only after successful validation.

Re-running an unchanged source must not duplicate content.

## Query workflow

1. Read `system/index.md` first.
2. Search titles, summaries, frontmatter, and relationship neighborhoods before reading many full pages.
3. Follow Evidence links for any material claim.
4. State uncertainty and distinguish corpus-supported conclusions from new inference.
5. File durable new synthesis only when explicitly requested or when the active workflow calls for it.

## Reconciliation workflow

Reconciliation is separate from ingestion. It should identify:

- duplicate or overlapping pages;
- cross-theme connections missed during batch processing;
- relationships missing their inverse;
- claims whose scope has expanded beyond their evidence;
- superseded synthesis and stale Hubs.

Propose ambiguous merges or deletions for human review. Do not perform them unilaterally.

## Lint workflow

Run deterministic validation first:

```bash
tools/wiki validate
tools/wiki index --check
```

Semantic lint may then inspect:

- contradictions and scope mismatches;
- Trends supported only by predictions or interpretations;
- insufficient source independence;
- missing counter-evidence;
- stale pages, orphans, and coverage gaps;
- unresolved dates and broken external provenance.

Store reports in `system/lint-reports/`. Lint reports propose substantive changes; they do not silently rewrite the Wiki.

## Required checks after changes

For schema, template, CLI, Evidence, or Wiki changes, run:

```bash
tools/wiki doctor
tools/wiki validate
tools/wiki index --check
python3 -m unittest discover -s tests -v
```

If an index is stale, run `tools/wiki index` and repeat validation.

## Git discipline

- Keep raw material, Evidence, Wiki pages, schemas, tools, tests, manifest, indexes, and log in Git.
- Keep secrets, caches, environments, disposable search indexes, and transient Obsidian workspace state out of Git.
- Prefer one semantic operation per commit: system setup, one controlled bootstrap batch, one source ingest, one lint repair, or one reconciliation.
- Do not commit unless the user asks for a commit.
