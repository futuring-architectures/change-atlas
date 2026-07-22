# Change Atlas Schema

`schema.yaml` is the machine-readable contract. This document explains its semantics and the judgment rules that cannot be reduced to field validation.

## Frontmatter format

Pages use YAML frontmatter delimited by `---`. The Phase 1 CLI supports a constrained, dependency-free subset:

- nested mappings using spaces for indentation;
- block lists beginning with `-`;
- strings, integers, booleans, `null`, and empty `[]` or `{}`;
- double- or single-quoted strings;
- no anchors, aliases, tags, folded scalars, or advanced YAML types.

Use ISO dates (`YYYY-MM-DD`) as strings. Unknown values are `null`, never empty invented placeholders.

## Stable identity

Every Evidence or Wiki page has an immutable ID with a type prefix and at least six lowercase alphanumeric characters after it. Examples:

```yaml
id: evi-a19c2d
id: sig-83db20
id: trd-0a91ee
```

Filenames are readable lowercase slugs and may change when titles improve. Links should use filenames; manifests and long-lived references should retain immutable IDs.

## Common frontmatter

```yaml
id: sig-83db20
type: signal
title: Recommendation feeds displace social graphs
status: candidate
created_at: 2026-07-13
updated_at: 2026-07-13
tags:
  - networks
relationships:
  - type: evidenced_by
    target: "[[source-example#Claim 1]]"
```

Relationships are machine-checkable edges. Page bodies should also explain important relationships in readable language.

## Evidence

Evidence pages represent sources or curated source entries. They preserve the original quotation, metadata, editorial placement, and atomic claim anchors.

For steady-state URL ingestion, the URL is only the intake locator. Preparation stores the accessible article as an immutable Markdown capture beneath `raw/web/`; Evidence provenance points to that capture and its hash. This prevents a changed or vanished live page from silently changing what the Atlas claims to have reviewed.

The optional `curator_pin_status` field is `user_supplied` or `not_supplied`. A user-supplied pin has exact `raw_quote_line_start` and `raw_quote_line_end` coordinates and is rendered verbatim under `Curated excerpt`. It records editorial salience, not evidential classification: claims are extracted from the complete captured article, and a pin may yield zero, one, or several claims.

Evidence begins as `draft` with `claim_extraction_status: pending` when deterministic bookkeeping is complete but interpretive claim extraction has not been reviewed. Draft Evidence may preserve excerpts and provenance without claim anchors and must not be cited from the Wiki.

After review, set `claim_extraction_status` to `complete_with_claims` or `complete_no_claims`. The latter is a meaningful outcome: an excerpt may consist only of questions, context, or rhetoric that should not be normalized into a claim. Active Evidence cannot remain `pending`; `complete_with_claims` requires at least one stable `claim-N` anchor, while `complete_no_claims` requires none.

Every Evidence page must first establish repository-level provenance:

```yaml
raw_file: raw/thoughtforming.md
raw_sha256: 473b5c17a3d13a184a181dd55a47956c0a1b0dddb4fb8d5652e5077113cb2f6f
raw_entry_index: 1
raw_line_start: 13
raw_line_end: 16
raw_quote_line_start: 15
raw_quote_line_end: 15
ingested_at: 2026-07-13
```

- `raw_file` is a repository-relative path beneath `raw/`.
- `raw_sha256` is the lowercase SHA-256 of the complete immutable raw file.
- `raw_entry_index` is the one-based logical entry number within that raw file.
- `raw_line_start` and `raw_line_end` are inclusive, one-based coordinates in the raw file.
- `raw_quote_line_start` and `raw_quote_line_end`, when present, identify the exact verbatim excerpt within that entry. The validator reconstructs the blockquoted Evidence excerpt and compares it with those raw lines.
- `ingested_at` is the ISO date on which the Evidence record was first created.

The validator confirms that the raw file exists, its checksum matches, and the entry and line coordinates are positive and coherent. For a normal one-source-per-file ingest, the entry index is `1` and the line range covers the relevant source portion. For the initial anthology, all Evidence records share one `raw_file` and `raw_sha256` while carrying distinct entry and line coordinates.

Repository provenance and publication provenance are deliberately separate. `raw_*` fields identify the exact local input; `source_*` fields identify the original publication represented by that input.

Canonical URL, author, and publisher each carry a status of `verified`, `inferred`, or `unresolved`. Verified values are displayed by the original source page. Inferred values are supported indirectly by a URL, site identity, or corroborating source but are not explicitly confirmed on the accessible page. An unresolved field must remain `null`.

Publication dates use the same status vocabulary. `date_source` records how the date was recovered, and `date_precision` is `day`, `month`, `year`, or `unknown`. Partial dates use `YYYY-MM` or `YYYY`; never invent a day merely to satisfy a date format.

Each claim uses a stable, numbered Markdown heading as its anchor:

```markdown
### Claim 1
```

Classification is recorded in the claim's `Classification` field rather than repeated in the heading. Wiki references target the exact heading text, for example `[[source-example#Claim 1]]`. Simple `Claim N` headings navigate natively in Obsidian and receive conventional `claim-n` fragment identifiers in common HTML renderers.

Each claim records exactly one primary class:

- `observation`: a reported event, state, measurement, case, or example;
- `interpretation`: an explanation or meaning attributed to observations;
- `prediction`: an assertion about what may or will happen;
- `normative_position`: an assertion about what should happen or what is desirable;
- `conceptual_claim`: a definition, distinction, mechanism, or named idea.

The quote remains verbatim even when its normalized claim is terse.

## Signal

A Signal is an evidence-grounded occurrence, case, example, or observable condition. It is not merely an interesting sentence.

Signals should state:

- what was observed;
- where and to whom it applies;
- the relevant date or explicit date uncertainty;
- the supporting Evidence;
- limitations and alternative readings.

## Trend

A Trend is a scoped directional synthesis, not a popular phrase. Promotion normally requires:

- multiple independent Signals;
- at least two defensible observation dates;
- a stated scope and period;
- a counter-signal search;
- separation of observation from interpretation and prediction.

Use `candidate` when these conditions are not yet satisfied. Do not convert repeated forecasts into evidence that the forecasted development occurred.

## Concept

A Concept page records a named idea, definition, provenance, aliases, distinctions, contested meanings, and Evidence. Prefer one page with scoped variants over near-duplicate pages.

## Framework

A Framework is a reusable structure: steps, axes, components, causal relationships, decision rules, or a matrix. It must explain where it applies, how to use it, and its limitations. A memorable idea without applicable structure remains a Concept.

Framework statuses have these semantics:

- `candidate`: a provisional Framework that is sufficiently structured and evidence-linked to publish, use, and test, but has not been accepted by the editor as active;
- `active`: a Framework the editor accepts as part of the Atlas's current working set;
- `contested`: a Framework whose support, structure, assumptions, or applicability is materially challenged and requires editorial disposition;
- `deprecated`: a Framework the editor retains for provenance and existing links but no longer recommends for current use;
- `archived`: an inactive Framework retained primarily as a historical record.

New Frameworks begin as `candidate`. An agent may independently change a `candidate` or `active` Framework to `contested` when warranted by later evidence or review. Only the editor may decide that a Framework is `active`, `deprecated`, or `archived`; an agent may apply one of those states only under explicit editor instruction. Agents must not alter `deprecated` or `archived` Frameworks without explicit editor instruction, and must not return `contested` Frameworks to `candidate`.

## Debate

A Debate organizes competing positions without forcing premature resolution. Distinguish genuine contradiction from differences in timeframe, scope, definitions, assumptions, values, and evidential standards.

## Question

A Question records a research gap. Its `origin` identifies whether it arose from ingestion, linting, querying, human input, or another page. Questions should state why the answer matters and what evidence would reduce uncertainty.

## Hubs

Hubs are navigational syntheses rather than folders disguised as prose. The original H1/H2 hierarchy can seed Hubs, but the Wiki may develop cross-cutting Hubs that span editorial sections.

## Typed relationships

Use only relationship types declared in `schema.yaml`. Each relationship has a required inverse. For example:

```yaml
# signal page
- type: supports
  target: "[[recommendation-media]]"

# trend page
- type: supported_by
  target: "[[recommendation-feed-displacement]]"
```

Evidence citations and relationship edges serve different purposes. The `evidence` field proves provenance; typed links describe the graph. A page may require both.

### Reader-facing link text

Frontmatter references remain canonical and unaliased so their targets are easy to inspect and compare mechanically:

```yaml
evidence:
  - "[[source-example#Claim 1]]"
```

Page bodies use Obsidian display aliases so generated slugs do not become reader-facing prose. In an Evidence list, identify the source and claim:

```markdown
- [[source-example#Claim 1|Source title — claim 1]]
```

In explanatory prose, the alias may instead name the claim's role in the sentence:

```markdown
The case shows [[source-example#Claim 1|a reversal in interoperability policy]].
```

Aliases change only presentation. The target before `|` remains the stable Evidence page and claim anchor.
Use the same principle for Wiki-to-Wiki links whenever a raw filename slug would otherwise appear in the rendered sentence.

## Page creation rule

Create a new page when the object is sufficiently distinct that other pages would meaningfully link to it. Update an existing page when new evidence adds an attribute, example, qualification, counterpoint, or status change to the same object.

## Synthesis backlog

An emerging proposition is a hypothesis that is too meaningful to discard but not established enough to become a reader-facing Wiki object. It remains private workflow memory while Evidence strengthens, qualifies, contests, or resolves it.

`system/synthesis-backlog.json` gives each proposition a stable `prp-` identity, current status, originating Hub and collection, cumulative Evidence claims, relevant future collections, assessment history, and optional resolution target. Later wording changes must retain the identity. After the bootstrap collection sequence, individual source ingests compare new claims with these private records.

Backlog statuses are `open`, `strengthened`, `qualified`, `contested`, `promoted`, or `retired`. `qualified` requires the statement itself to express its material limitation; a qualifying assessment alone does not justify the status. `promoted` means the proposition has resolved into an established public Wiki type and `resolution_target` identifies that page. Every relevant bootstrap collection records one of `opened`, `no_change`, `strengthened`, `qualified`, `contested`, `promoted`, or `retired`. A relevant collection may not reach `synthesis_ready` without an assessment unless the proposition was already promoted or retired. In steady-state ingestion, the source transaction records what the new Evidence did or did not change; collection relevance no longer acts as the trigger.

## Human review boundaries

Require human review before:

- merging or deleting ambiguous pages;
- promoting a contested candidate to an active Trend;
- resolving a Debate editorially;
- replacing a source date inferred with low confidence;
- making a large ontology or relationship-vocabulary change.
