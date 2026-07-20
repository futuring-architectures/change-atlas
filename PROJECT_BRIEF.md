# Change Atlas — Project Brief

## Purpose

Change Atlas is a living evidence map of technological, organizational, and cultural change. It compiles a curated corpus into a durable, interlinked Markdown knowledge base maintained with an LLM.

The public working name is **Change Atlas**, under the **Futuring Architectures** brand:

> **Futuring Architectures: The Change Atlas**  
> A living evidence map of technological, organizational, and cultural change.

“Wiki” describes the maintenance mechanism, not the product identity. “Atlas” is preferred to “Map” because the system holds many maps at different scales and from different perspectives.

## Source Corpus

The initial raw input is stored at:

`raw/thoughtforming-on-digital-transformation-2026-07-10.md`

Although it has a `.txt` extension, it is structured as Markdown. The inspected corpus contains:

- four substantive H1 domains, plus the document title;
- 16 H2 thematic collections;
- 686 H3 source entries;
- 685 corresponding curated quote bodies;
- approximately 50,000 words;
- source entries nested in a meaningful H1 → H2 → H3 editorial hierarchy.

Each H3 normally contains a source title and URL, followed by a deliberately selected quotation. The quotation is often more important to this project than the source article as a whole. The hierarchy and ordering are also editorial data and must be preserved.

The bootstrap audit originally surfaced one missing quote and one malformed heading that were corrected before Evidence generation. Remaining input issues include a small number of recoverable malformed headings, tracking or tokenized URLs, fragile social-media links, and incomplete date metadata. These should be surfaced by deterministic validation rather than silently repaired during synthesis.

## Core Epistemic Architecture

The system has three conceptual levels:

1. **Evidence** records what was encountered.
2. **Wiki** compiles what the corpus currently supports.
3. **Frames** use that knowledge to explain particular situations.

In shorthand:

> Evidence constrains. Wiki generalizes. Frames hypothesize.

Frames are intentionally deferred until the Evidence and Wiki layers are operational.

### Evidence layer

Evidence remains close to the source and preserves provenance. It distinguishes:

- observations;
- interpretations;
- predictions;
- normative positions;
- conceptual claims.

An excerpt is never automatically treated as a Signal. One excerpt may yield zero, one, or several atomic claims.

Evidence records should preserve:

- the exact raw file path, SHA-256, entry number, and inclusive line range;
- the quotation verbatim;
- source title and original URL;
- canonical URL when recoverable;
- author and publisher when recoverable;
- publication date, date source, precision, and confidence;
- the original H1/H2 editorial path;
- global and within-section sequence;
- stable source and claim identifiers.

Unknown metadata must remain explicitly unknown rather than being guessed.

### Wiki layer

The agreed Wiki page types are:

- **Hubs** — navigational syntheses for topics and editorial domains;
- **Signals** — scoped and preferably dated observations, cases, or examples;
- **Trends** — directional patterns supported by multiple independent Signals over time;
- **Concepts** — named ideas with definitions and provenance;
- **Frameworks** — applicable Concepts with components, steps, axes, or other usable structure;
- **Propositions** — strengthened or genuinely qualified cross-source claims published for continued testing;
- **Tensions & Debates** — structured competing positions, contradictions, or unresolved differences;
- **Questions** — research gaps produced by ingestion, querying, or linting.

The existing H1/H2 hierarchy is a strong editorial prior, not the Wiki’s sole taxonomy. Cross-cutting links and multiple topic memberships are expected.

### Relationship layer

Relationships appear as typed links between Evidence and Wiki objects, not normally as a separate folder of pages.

Initial relationship vocabulary should include pairs such as:

- `supports` / `supported_by`;
- `contradicts` / `contradicted_by`;
- `qualifies` / `qualified_by`;
- `exemplifies` / `exemplified_by`;
- `refines` / `refined_by`;
- `operationalizes` / `operationalized_by`;
- `supersedes` / `superseded_by`;
- `raises_question` / `raised_by`;
- `evidenced_by` / `evidence_for`.

Relationships should be readable in page bodies and machine-checkable in YAML frontmatter. Reciprocal links must be validated.

## Steady-State Workflow

After the initial bulk bootstrap, new sources will be added manually, one Markdown file at a time:

```text
raw/ source
    ↓
normalized evidence and atomic claims
    ↓
create or update Wiki synthesis
    ↓
validate relationships and provenance
    ↓
update manifest, indexes, and log
```

A new source does not necessarily create a new Wiki page. It may strengthen, qualify, contradict, or leave unchanged an existing synthesis.

Ingestion must be idempotent: processing the same unchanged raw file twice must not duplicate evidence or Wiki content.

## Software Boundary

The minimum viable system is a versioned Markdown repository plus a small deterministic CLI used by Codex. It does not initially require a database, embeddings, RAG infrastructure, a web application, or autonomous background agents.

Deterministic software handles:

- file discovery and hashing;
- stable identifiers;
- structural parsing;
- manifests and operation logs;
- schema validation;
- internal-link checks;
- reciprocal-relationship checks;
- evidence-citation checks;
- index generation;
- duplicate-ingestion prevention.

The LLM handles:

- claim extraction and classification;
- synthesis across sources;
- deciding whether to create or update a page;
- interpreting support, qualification, and contradiction;
- proposing Trends, Concepts, Frameworks, Debates, and Questions.

Human judgment remains important for meaningful Trend promotion, ambiguous concept merging, and other editorial decisions the corpus cannot settle.

## Intended Repository Structure

```text
raw/
evidence/
  sources/
wiki/
  hubs/
  signals/
  trends/
  concepts/
  frameworks/
  propositions/
  debates/
  questions/
system/
  templates/
  lint-reports/
  schema.yaml
  schema.md
  manifest.json
  index.md
  log.md
tools/
tests/
  fixtures/
AGENTS.md
README.md
PROJECT_BRIEF.md
```

## Git Policy

The complete Atlas should be versioned in Git, including `raw/`, `evidence/`, `wiki/`, `system/`, `tools/`, tests, and operating instructions.

Generated disposable caches, virtual environments, secrets, search indexes, and transient Obsidian workspace state should be ignored.

Recommended commit boundaries are semantic:

- system setup;
- one bootstrap theme or controlled batch;
- one steady-state source ingest;
- one lint repair pass;
- one reconciliation operation.

Git records exactly what changed. `system/log.md` records why an ingest or reconciliation occurred.

Collection progress is recorded in `system/collections.json` and rendered into `system/dashboard.md`. Collection review reports under `system/reviews/` present Wiki-level synthesis deltas for editorial judgment. Source-metadata checking and claim extraction remain pipeline responsibilities rather than human approval gates.

`system/synthesis-backlog.json` provides synthesis memory for propositions that are meaningful but not yet ready to become reader-facing Wiki objects. Stable proposition identities prevent wording drift and duplication. During bootstrap, collection assessments record whether later collections strengthen, qualify, contest, promote, retire, or leave each proposition unchanged. In steady state, each individual source is the assessment trigger. Published Proposition pages preserve the same `prp-` identity; their backlog records become `promoted` and point to that authoritative page.

**Current handoff note:** at the time this brief was created, `/Users/ronkersic/Projects/change-atlas` contained the source corpus but was not yet initialized as a Git repository.

## Phase 1 — Foundation

Phase 1 establishes an empty but trustworthy Atlas system. It must not synthesize the initial corpus yet.

### 1. Scaffold the repository

Create the intended directory structure without modifying the source corpus.

### 2. Create `AGENTS.md`

Define durable operating rules for Codex, including:

- raw sources are immutable;
- Evidence remains source-grounded;
- Wiki claims require resolvable Evidence links;
- page creation versus update rules;
- relationship maintenance;
- ingest, query, reconcile, and lint workflows;
- operations requiring human review.

### 3. Define schemas

Use:

- `system/schema.yaml` for machine-readable requirements;
- `system/schema.md` for semantic definitions, examples, and judgment rules.

Default conventions:

- Python CLI;
- YAML frontmatter;
- Obsidian-style `[[wikilinks]]`;
- readable filenames plus immutable identifiers;
- Markdown as the knowledge store.

### 4. Create templates

Create templates for Evidence, Hub, Signal, Trend, Concept, Framework, Debate, Question, and lint-report pages.

### 5. Build the deterministic CLI foundation

The first CLI should expose:

```bash
tools/wiki doctor
tools/wiki status
tools/wiki validate
tools/wiki index
```

- `doctor` checks the environment, repository structure, and schema installation.
- `status` reports raw, processed, Evidence, and Wiki counts.
- `validate` checks frontmatter, IDs, page types, links, Evidence anchors, relationship types, and inverse relationships.
- `index` regenerates navigational indexes deterministically.

Bootstrap and ingest commands belong to later phases, after the contract is verified.

### 6. Establish state tracking

Create an empty versioned manifest and append-only operational log. The manifest will later associate raw file hashes with derived Evidence and affected Wiki pages.

### 7. Add tests and fixtures

Tests must cover missing and duplicate IDs, unknown page types, broken links, unsupported relationships, missing inverse relationships, malformed frontmatter, and Wiki claims lacking Evidence.

Include one fully valid miniature chain:

```text
Evidence → Signal → Trend → Debate → Question
```

## Phase 1 Acceptance Criteria

Phase 1 is complete when:

- `tools/wiki doctor` succeeds;
- `tools/wiki validate` accepts the valid reference fixture;
- intentionally broken fixtures fail for the expected reasons;
- indexes regenerate deterministically;
- manifest and log formats are established;
- `AGENTS.md` fully defines future operation;
- no initial-corpus synthesis has occurred;
- the existing source file remains unchanged.

## Later Phases

### Phase 2 — Bootstrap

- Parse and validate all initial source entries.
- Create normalized Evidence records.
- Recover source metadata and dates where possible.
- Build the initial Wiki in controlled thematic batches.
- Reconcile pages and relationships across H2 boundaries.

### Phase 3 — Steady-state ingestion

- Add `tools/wiki ingest <raw-file>`.
- Enforce hash-based idempotence.
- Extract Evidence and maintain the Wiki incrementally.
- Validate and log each ingest transaction.

### Phase 4 — Health and querying

- Add structural and semantic linting.
- Detect contradictions, staleness, weakly supported Trends, and coverage gaps.
- Improve query and navigation workflows.
- Add enhanced local search only if ordinary indexes and text search become insufficient.

### Deferred — Frames

Frames will later be implemented as a separate sensemaking workflow that reads both Evidence and Wiki content. Active Frames are provisional, question-bound explanatory hypotheses rather than canonical Wiki page types. Durable outcomes may be promoted into Concepts, Frameworks, Trends, Debates, or Questions.
