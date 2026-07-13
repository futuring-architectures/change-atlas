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
    target: "[[source-example#claim-1]]"
```

Relationships are machine-checkable edges. Page bodies should also explain important relationships in readable language.

## Evidence

Evidence pages represent sources or curated source entries. They preserve the original quotation, metadata, editorial placement, and atomic claim anchors.

Every Evidence page must first establish repository-level provenance:

```yaml
raw_file: raw/thoughtforming.md
raw_sha256: 473b5c17a3d13a184a181dd55a47956c0a1b0dddb4fb8d5652e5077113cb2f6f
raw_entry_index: 1
raw_line_start: 13
raw_line_end: 16
ingested_at: 2026-07-13
```

- `raw_file` is a repository-relative path beneath `raw/`.
- `raw_sha256` is the lowercase SHA-256 of the complete immutable raw file.
- `raw_entry_index` is the one-based logical entry number within that raw file.
- `raw_line_start` and `raw_line_end` are inclusive, one-based coordinates in the raw file.
- `ingested_at` is the ISO date on which the Evidence record was first created.

The validator confirms that the raw file exists, its checksum matches, and the entry and line coordinates are positive and coherent. For a normal one-source-per-file ingest, the entry index is `1` and the line range covers the relevant source portion. For the initial anthology, all Evidence records share one `raw_file` and `raw_sha256` while carrying distinct entry and line coordinates.

Repository provenance and publication provenance are deliberately separate. `raw_*` fields identify the exact local input; `source_*` fields identify the original publication represented by that input.

Each claim must have a stable explicit anchor:

```html
<a id="claim-1"></a>
```

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

## Page creation rule

Create a new page when the object is sufficiently distinct that other pages would meaningfully link to it. Update an existing page when new evidence adds an attribute, example, qualification, counterpoint, or status change to the same object.

## Human review boundaries

Require human review before:

- merging or deleting ambiguous pages;
- promoting a contested candidate to an active Trend;
- resolving a Debate editorially;
- replacing a source date inferred with low confidence;
- making a large ontology or relationship-vocabulary change.
