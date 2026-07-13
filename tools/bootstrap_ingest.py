#!/usr/bin/env python3
"""Deterministic ingestion planning and Evidence-draft rendering for anthologies."""

from __future__ import annotations

import dataclasses
import hashlib
import json
import re
import unicodedata
from collections import Counter
from pathlib import Path
from typing import Any, Dict, List, Sequence, Tuple

from bootstrap_audit import BootstrapAudit, BootstrapEntry


@dataclasses.dataclass(frozen=True)
class IngestionPlanEntry:
    global_position: int
    collection_position: int
    evidence_id: str
    slug: str
    evidence_file: str
    curated_h1: str
    curated_h2: str
    source_title: str
    source_url: str
    raw_line_start: int
    raw_line_end: int
    quote_line_start: int
    quote_line_end: int
    issue_codes: Tuple[str, ...]

    @property
    def curated_path(self) -> List[str]:
        return [self.curated_h1, self.curated_h2]

    def as_dict(self) -> Dict[str, Any]:
        return {
            "collection_position": self.collection_position,
            "curated_path": self.curated_path,
            "evidence_file": self.evidence_file,
            "evidence_id": self.evidence_id,
            "global_position": self.global_position,
            "issue_codes": list(self.issue_codes),
            "quote_line_end": self.quote_line_end,
            "quote_line_start": self.quote_line_start,
            "raw_line_end": self.raw_line_end,
            "raw_line_start": self.raw_line_start,
            "slug": self.slug,
            "source_title": self.source_title,
            "source_url": self.source_url,
        }


@dataclasses.dataclass(frozen=True)
class IngestionPlan:
    raw_file: str
    raw_sha256: str
    entries: Tuple[IngestionPlanEntry, ...]

    def as_dict(self) -> Dict[str, Any]:
        collections = Counter((entry.curated_h1, entry.curated_h2) for entry in self.entries)
        return {
            "entries": [entry.as_dict() for entry in self.entries],
            "raw_file": self.raw_file,
            "raw_sha256": self.raw_sha256,
            "schema_version": 1,
            "summary": {
                "collections": len(collections),
                "entries": len(self.entries),
            },
        }


def slugify(value: str) -> str:
    normalized = unicodedata.normalize("NFKD", value).encode("ascii", "ignore").decode("ascii")
    normalized = normalized.lower().replace("&", " and ")
    normalized = re.sub(r"[^a-z0-9]+", "-", normalized).strip("-")
    return normalized or "untitled-source"


def stable_evidence_id(audit: BootstrapAudit, entry: BootstrapEntry) -> str:
    identity = f"{audit.raw_file}\0{audit.raw_sha256}\0{entry.index}".encode("utf-8")
    return f"evi-{hashlib.sha256(identity).hexdigest()[:12]}"


def build_ingestion_plan(audit: BootstrapAudit) -> IngestionPlan:
    if audit.error_count:
        raise ValueError("bootstrap audit contains structural errors")
    positions: Counter = Counter()
    planned: List[IngestionPlanEntry] = []
    for entry in audit.entries:
        if not entry.curated_h1 or not entry.curated_h2 or not entry.source_url:
            raise ValueError(f"entry {entry.index} lacks required structural metadata")
        if entry.quote_line_start is None or entry.quote_line_end is None or entry.quote_text is None:
            raise ValueError(f"entry {entry.index} lacks a curated quote")
        key = (entry.curated_h1, entry.curated_h2)
        positions[key] += 1
        evidence_id = stable_evidence_id(audit, entry)
        slug = f"{slugify(entry.source_title)}-{evidence_id}"
        planned.append(
            IngestionPlanEntry(
                global_position=entry.index,
                collection_position=positions[key],
                evidence_id=evidence_id,
                slug=slug,
                evidence_file=f"evidence/sources/{slug}.md",
                curated_h1=entry.curated_h1,
                curated_h2=entry.curated_h2,
                source_title=entry.source_title,
                source_url=entry.source_url,
                raw_line_start=entry.raw_line_start,
                raw_line_end=entry.raw_line_end,
                quote_line_start=entry.quote_line_start,
                quote_line_end=entry.quote_line_end,
                issue_codes=tuple(sorted(entry.issue_codes)),
            )
        )
    ids = [entry.evidence_id for entry in planned]
    slugs = [entry.slug for entry in planned]
    if len(ids) != len(set(ids)) or len(slugs) != len(set(slugs)):
        raise ValueError("planned Evidence identities are not unique")
    return IngestionPlan(audit.raw_file, audit.raw_sha256, tuple(planned))


def render_plan_json(plan: IngestionPlan) -> str:
    return json.dumps(plan.as_dict(), indent=2, ensure_ascii=False, sort_keys=True) + "\n"


def render_plan_markdown(plan: IngestionPlan) -> str:
    collections = Counter((entry.curated_h1, entry.curated_h2) for entry in plan.entries)
    lines = [
        "# Bootstrap Ingestion Plan",
        "",
        f"- Raw file: `{plan.raw_file}`",
        f"- SHA-256: `{plan.raw_sha256}`",
        f"- Planned Evidence records: {len(plan.entries)}",
        f"- Editorial collections: {len(collections)}",
        "- Quote bodies are intentionally omitted from this plan.",
        "",
        "## Collections",
        "",
        "| H1 | H2 | Entries | Global range |",
        "|---|---|---:|---:|",
    ]
    for h1, h2 in dict.fromkeys((entry.curated_h1, entry.curated_h2) for entry in plan.entries):
        matches = [entry for entry in plan.entries if (entry.curated_h1, entry.curated_h2) == (h1, h2)]
        lines.append(f"| {h1} | {h2} | {len(matches)} | {matches[0].global_position}–{matches[-1].global_position} |")
    lines.extend(
        [
            "",
            "## Review boundary",
            "",
            "The plan assigns identities and destinations only. Evidence drafts preserve source metadata and excerpts; atomic claims require a separate interpretive review before activation.",
            "",
        ]
    )
    return "\n".join(lines)


def _yaml_string(value: str) -> str:
    return json.dumps(value, ensure_ascii=False)


def _tag(value: str) -> str:
    return slugify(value)


def render_evidence_draft(
    audit: BootstrapAudit,
    source_entry: BootstrapEntry,
    plan_entry: IngestionPlanEntry,
    ingest_date: str,
) -> str:
    if source_entry.quote_text is None:
        raise ValueError(f"entry {source_entry.index} has no quote body")
    quote_lines = source_entry.quote_text.split("\n")
    blockquote = "\n".join(">" if line == "" else f"> {line}" for line in quote_lines)
    issue_text = ", ".join(f"`{code}`" for code in plan_entry.issue_codes) or "None"
    return "\n".join(
        [
            "---",
            f"id: {plan_entry.evidence_id}",
            "type: evidence",
            f"title: {_yaml_string(plan_entry.source_title)}",
            "status: draft",
            f"created_at: {ingest_date}",
            f"updated_at: {ingest_date}",
            "tags:",
            f"  - {_tag(plan_entry.curated_h1)}",
            f"  - {_tag(plan_entry.curated_h2)}",
            "relationships: []",
            f"raw_file: {_yaml_string(audit.raw_file)}",
            f"raw_sha256: {_yaml_string(audit.raw_sha256)}",
            f"raw_entry_index: {plan_entry.global_position}",
            f"raw_line_start: {plan_entry.raw_line_start}",
            f"raw_line_end: {plan_entry.raw_line_end}",
            f"raw_quote_line_start: {plan_entry.quote_line_start}",
            f"raw_quote_line_end: {plan_entry.quote_line_end}",
            f"ingested_at: {ingest_date}",
            f"source_title: {_yaml_string(plan_entry.source_title)}",
            f"source_url: {_yaml_string(plan_entry.source_url)}",
            "canonical_url: null",
            "author: null",
            "publisher: null",
            "published_at: null",
            "date_status: unresolved",
            "date_source: null",
            "date_precision: unknown",
            "curated_path:",
            f"  - {_yaml_string(plan_entry.curated_h1)}",
            f"  - {_yaml_string(plan_entry.curated_h2)}",
            f"collection_position: {plan_entry.collection_position}",
            f"global_position: {plan_entry.global_position}",
            "---",
            "",
            f"# {plan_entry.source_title}",
            "",
            "## Source metadata",
            "",
            f"- Raw file: `{audit.raw_file}`",
            f"- Raw SHA-256: `{audit.raw_sha256}`",
            f"- Raw entry and lines: entry {plan_entry.global_position}, lines {plan_entry.raw_line_start}–{plan_entry.raw_line_end}",
            f"- Quote lines: {plan_entry.quote_line_start}–{plan_entry.quote_line_end}",
            f"- Original URL: <{plan_entry.source_url}>",
            "- Canonical URL: unresolved",
            "- Author: unresolved",
            "- Publisher: unresolved",
            "- Publication date: unresolved",
            f"- Curated path: {plan_entry.curated_h1} → {plan_entry.curated_h2}",
            f"- Collection/global position: {plan_entry.collection_position}/{plan_entry.global_position}",
            f"- Structural audit warnings: {issue_text}",
            "",
            "## Curated excerpt",
            "",
            blockquote,
            "",
            "## Atomic claims",
            "",
            "_Pending interpretive extraction and classification. Draft Evidence must not be cited by Wiki pages._",
            "",
            "## Relationships",
            "",
            "_No relationships recorded._",
            "",
        ]
    )


def select_collection(
    audit: BootstrapAudit,
    plan: IngestionPlan,
    curated_h1: str,
    curated_h2: str,
) -> List[Tuple[BootstrapEntry, IngestionPlanEntry]]:
    source_by_index = {entry.index: entry for entry in audit.entries}
    selected = [
        (source_by_index[entry.global_position], entry)
        for entry in plan.entries
        if entry.curated_h1 == curated_h1 and entry.curated_h2 == curated_h2
    ]
    if not selected:
        raise ValueError(f"collection not found: {curated_h1} → {curated_h2}")
    return selected


def write_evidence_drafts(
    root: Path,
    rendered: Sequence[Tuple[IngestionPlanEntry, str]],
) -> Tuple[int, int]:
    evidence_directory = root / "evidence/sources"
    existing_ids: Dict[str, Path] = {}
    for path in evidence_directory.glob("*.md"):
        match = re.search(r"(?m)^id: (evi-[a-z0-9]+)$", path.read_text(encoding="utf-8"))
        if match:
            existing_ids[match.group(1)] = path

    outcomes: List[Tuple[Path, str, bool]] = []
    for entry, content in rendered:
        path = root / entry.evidence_file
        other = existing_ids.get(entry.evidence_id)
        if other is not None and other.resolve() != path.resolve():
            raise ValueError(f"Evidence ID {entry.evidence_id} already exists at {other.relative_to(root)}")
        existing = path.read_text(encoding="utf-8") if path.exists() else None
        if existing is not None and existing != content:
            raise ValueError(f"refusing to overwrite changed Evidence draft: {entry.evidence_file}")
        outcomes.append((path, content, existing == content))

    written = 0
    unchanged = 0
    for path, content, is_unchanged in outcomes:
        if is_unchanged:
            unchanged += 1
            continue
        path.parent.mkdir(parents=True, exist_ok=True)
        temporary = path.with_name(path.name + ".tmp")
        temporary.write_text(content, encoding="utf-8")
        temporary.replace(path)
        written += 1
    return written, unchanged
