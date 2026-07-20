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
- `proposition`: a strengthened or genuinely qualified claim published for continued testing across individual source ingests.
- `debate`: a structured comparison of competing positions or interpretations.
- `question`: a tracked research gap or unresolved issue.

Follow `system/schema.yaml` for machine requirements and `system/schema.md` for semantic rules.

## Framework status governance

Framework status combines evidence assessment with editorial authority:

- Create every new Framework as `candidate`. An agent may assign this status without separate editor approval.
- An agent may change a `candidate` or `active` Framework to `contested` when later evidence or review materially challenges its support, structure, assumptions, or applicability. Record the reason in the page and the applicable collection review or operational record.
- `active`, `deprecated`, and `archived` are editor-controlled states. An agent may recommend one of these states, but may assign it only when carrying out an explicit editor instruction.
- Do not change a `deprecated` or `archived` Framework, including changing it to `contested`, without explicit editor instruction.
- Do not return a `contested` Framework to `candidate`. The editor decides whether it becomes `active`, `deprecated`, or `archived`.

## Proposition publication and maintenance

Keep new and unresolved hypotheses in `system/synthesis-backlog.json` as `open`. Publish a first-class page under `wiki/propositions/` only when later Evidence has strengthened the claim or the statement has been rewritten to incorporate a material qualification. A qualifying assessment alone does not make a Proposition publishable.

When publishing a Proposition:

1. preserve its `prp-` identity;
2. reconstruct the cumulative stable Evidence claim anchors behind every material assessment;
3. state scope, confidence, counter-evidence, and what would change the status;
4. link related Signals, Concepts, Frameworks, Debates, Questions, and Trends without collapsing their distinct roles;
5. mark the backlog record `promoted` and set `resolution_target` to the Proposition page.

An agent may strengthen, qualify, or contest a published Proposition when new Evidence warrants the change. `qualified` requires revising the statement so the limitation or condition is part of the claim. Keep a published `contested` Proposition accessible with a warning and link it to the relevant Debate. Do not promote a Proposition to a Trend merely because arguments repeat; apply the Trend evidence rule. Archiving a published Proposition remains an editor decision.

## Evidence classification

Atomic claims use one of these classes:

- `observation`
- `interpretation`
- `prediction`
- `normative_position`
- `conceptual_claim`

A claim may be evidence for more than one page, but every use must preserve its original classification and source anchor.

## Relationship maintenance

Use only relationship types declared in `system/schema.yaml`. Targets use Obsidian-style links such as `[[recommendation-media]]` or `[[source-example#Claim 1]]`.

Keep frontmatter Evidence and relationship targets canonical and unaliased for stable machine inspection. In page bodies, add readable display aliases to Evidence claim links: use `[[source-slug#Claim 1|Source title — claim 1]]` in Evidence lists and a concise semantic label in explanatory prose. Give Wiki-to-Wiki links readable title or sentence-level aliases as well. Do not expose generated slugs as reader-facing text when an alias can state the source, page, or claim clearly.

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

## Bootstrap anthology audit

The initial anthology is a special raw container holding many logical sources. Before creating Evidence, run:

```bash
tools/wiki bootstrap-audit raw/thoughtforming-on-digital-transformation-2026-07-10.md --write
```

The audit is deterministic and report-only. It must preserve H1/H2 context, H3 source headings, entry order, exact stanza ranges, and quote ranges. Review every structural error before generating Evidence shells. Warnings may be accepted only when the parser's recovery is explicit and lossless.

The audit reports in `system/bootstrap/` are generated records of this checkpoint. They must not contain duplicate quote bodies; the raw anthology remains the only source text at this stage.

## Bootstrap Evidence planning

After the structural audit passes, generate the deterministic ingestion plan before creating Evidence:

```bash
tools/wiki bootstrap-plan raw/thoughtforming-on-digital-transformation-2026-07-10.md --write
```

Generate one exact H1/H2 collection at a time with `bootstrap-evidence`. This creates provenance-complete `draft` Evidence only. It must preserve the excerpt verbatim and must not overwrite a changed draft. Deterministic generation does not extract claims, activate Evidence, update the manifest, or synthesize Wiki pages.

Review each draft interpretively and record `claim_extraction_status`. Use `complete_with_claims` with stable classified claim anchors, or `complete_no_claims` when forcing an assertion would misrepresent the excerpt. Change the Evidence status to `active` only when that review is complete. Draft Evidence cannot be cited by the Wiki, and no-claim Evidence cannot serve as a claim citation. Update the manifest and operational log only after the reviewed batch validates successfully.

Register each completed bootstrap collection with `tools/wiki bootstrap-register`. A partially processed anthology remains `partial` in the manifest and must not be counted as a fully processed raw file.

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
- internal propositions mature enough for Wiki publication and published Propositions whose citations or statuses no longer reflect their Evidence.

Propose ambiguous merges or deletions for human review. Do not perform them unilaterally.

## Collection workflow and editorial sign-off

Use `system/collections.json` as the machine-readable source of truth for bootstrap collection progress. Regenerate `system/dashboard.md` with `tools/wiki dashboard` whenever collection state or derived content counts change.

Pipeline stages such as metadata checking and claim extraction are agent responsibilities. They must not be presented as human review tasks. The editor signs off on the synthesized Wiki state through the collection review report, not on every Evidence record.

Before starting a collection, record its comparison baseline. After synthesis, generate `system/reviews/<collection-id>.md` with `tools/wiki review-report --collection <collection-id>`. The report must summarize created, updated, merged, renamed, or deleted Wiki pages; material relationship changes; candidate Trends; changed Debates and Questions; and validation exceptions.

Before synthesizing each bootstrap collection, load `system/synthesis-backlog.json`. Assess every open, strengthened, qualified, or contested proposition that lists the collection in `relevant_collections`. Record an assessment even when the new batch produces no change. A relevant collection cannot reach `synthesis_ready` until those assessments exist.

Give each new proposition one stable `prp-` identity. Update its evidence and status across batches rather than creating a differently worded duplicate. Allowed outcomes are `opened`, `no_change`, `strengthened`, `qualified`, `contested`, `promoted`, and `retired`. Promotion records the target Wiki page; retirement records why the proposition is no longer useful. Reader-facing Hub prose may summarize the backlog, but the JSON record is the pipeline source of truth.

After bootstrap, each individual source ingest replaces the collection trigger: compare its atomic claims with published Propositions and unresolved backlog records, add exact claim anchors, and record whether the source strengthens, qualifies, contests, resolves, or leaves each materially relevant claim unchanged.

`🧰 Nature of the Firm → 👩‍⚖️ Governance` is the designated editorial sign-off collection. After its sign-off, remaining bootstrap collections may proceed autonomously in validated collection-level checkpoints. Stop the loop for validation failures, unresolved provenance that materially affects synthesis, or ambiguous destructive changes. Routine metadata and claim processing are not blockers.

## Lint workflow

Run deterministic validation first:

```bash
tools/wiki validate
tools/wiki index --check
tools/wiki dashboard --check
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
