#!/usr/bin/env python3
"""Dependency-free control plane for the Change Atlas Markdown repository."""

from __future__ import annotations

import argparse
import dataclasses
import datetime as dt
import hashlib
import json
import os
import re
import subprocess
import sys
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Sequence, Tuple

from bootstrap_audit import parse_anthology, render_json as render_audit_json, render_markdown as render_audit_markdown
from bootstrap_ingest import (
    build_ingestion_plan,
    render_evidence_draft,
    render_plan_json,
    render_plan_markdown,
    select_collection,
    write_evidence_drafts,
)


MIN_PYTHON = (3, 9)
DEFAULT_ROOT = Path(__file__).resolve().parent.parent
REQUIRED_DIRECTORIES = (
    "raw",
    "evidence/sources",
    "wiki/hubs",
    "wiki/signals",
    "wiki/trends",
    "wiki/concepts",
    "wiki/frameworks",
    "wiki/propositions",
    "wiki/debates",
    "wiki/questions",
    "system/templates",
    "system/bootstrap",
    "system/lint-reports",
    "system/reviews",
    "tools",
    "tests/fixtures",
)
REQUIRED_FILES = (
    "AGENTS.md",
    "README.md",
    "PROJECT_BRIEF.md",
    "system/schema.yaml",
    "system/schema.md",
    "system/manifest.json",
    "system/collections.json",
    "system/synthesis-backlog.json",
    "system/dashboard.md",
    "system/index.md",
    "system/log.md",
    "evidence/index.md",
    "tools/wiki",
)
WIKILINK_RE = re.compile(r"\[\[([^\]]+)\]\]")
ANCHOR_RE = re.compile(r'<a\s+(?:id|name)=["\']([^"\']+)["\']\s*></a>', re.I)
HEADING_RE = re.compile(r"(?m)^#{1,6}\s+(.+?)\s*$")
CLAIM_HEADING_RE = re.compile(r"(?m)^### Claim ([1-9][0-9]*)\s*$")
ID_RE = re.compile(r"^[a-z]{3}-[a-z0-9]{6,}$")
SLUG_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
ISO_DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
COLLECTION_STAGES = (
    "planned",
    "evidence_ingested",
    "metadata_checked",
    "claims_extracted",
    "synthesis_ready",
    "awaiting_editorial_signoff",
    "signed_off",
    "committed",
)
SIGNOFF_MODES = ("required", "autonomous", "completed")
PROPOSITION_STATUSES = ("open", "strengthened", "qualified", "contested", "promoted", "retired")
PROPOSITION_OUTCOMES = (
    "opened",
    "no_change",
    "strengthened",
    "qualified",
    "contested",
    "promoted",
    "retired",
)
SYNTHESIS_COMPLETE_STAGES = (
    "synthesis_ready",
    "awaiting_editorial_signoff",
    "signed_off",
    "committed",
)
PROPOSITION_ID_RE = re.compile(r"^prp-[a-z0-9]{6,}$")


class YamlSubsetError(ValueError):
    """Raised when frontmatter uses unsupported or malformed YAML."""


@dataclasses.dataclass(frozen=True)
class YamlLine:
    indent: int
    content: str
    number: int


def _parse_scalar(value: str) -> Any:
    value = value.strip()
    if value == "":
        return None
    if value in ("null", "Null", "NULL", "~"):
        return None
    if value.lower() == "true":
        return True
    if value.lower() == "false":
        return False
    if value == "[]":
        return []
    if value == "{}":
        return {}
    if value.startswith('"'):
        try:
            return json.loads(value)
        except json.JSONDecodeError as exc:
            raise YamlSubsetError(f"invalid double-quoted string: {exc.msg}") from exc
    if value.startswith("'"):
        if len(value) < 2 or not value.endswith("'"):
            raise YamlSubsetError("unterminated single-quoted string")
        return value[1:-1].replace("''", "'")
    if value.startswith("[") or value.startswith("{"):
        try:
            return json.loads(value)
        except json.JSONDecodeError as exc:
            raise YamlSubsetError(
                "inline collections must use JSON-compatible quoting"
            ) from exc
    if re.fullmatch(r"-?\d+", value):
        return int(value)
    return value


def _split_mapping(content: str, line_number: int) -> Tuple[str, str]:
    if ":" not in content:
        raise YamlSubsetError(f"line {line_number}: expected 'key: value'")
    key, value = content.split(":", 1)
    key = key.strip()
    if not key or not re.fullmatch(r"[A-Za-z_][A-Za-z0-9_-]*", key):
        raise YamlSubsetError(f"line {line_number}: invalid mapping key {key!r}")
    return key, value.strip()


def _prepare_yaml(text: str) -> List[YamlLine]:
    prepared: List[YamlLine] = []
    for number, raw in enumerate(text.splitlines(), 1):
        if "\t" in raw[: len(raw) - len(raw.lstrip("\t "))]:
            raise YamlSubsetError(f"line {number}: tabs are not allowed for indentation")
        stripped = raw.strip()
        if not stripped or stripped.startswith("#"):
            continue
        indent = len(raw) - len(raw.lstrip(" "))
        if indent % 2:
            raise YamlSubsetError(f"line {number}: indentation must use multiples of two spaces")
        prepared.append(YamlLine(indent, raw[indent:].rstrip(), number))
    return prepared


def _parse_yaml_block(lines: Sequence[YamlLine], index: int, indent: int) -> Tuple[Any, int]:
    if index >= len(lines):
        return {}, index
    if lines[index].indent != indent:
        raise YamlSubsetError(
            f"line {lines[index].number}: unexpected indentation {lines[index].indent}"
        )

    is_list = lines[index].content.startswith("- ") or lines[index].content == "-"
    if is_list:
        output: List[Any] = []
        while index < len(lines):
            current = lines[index]
            if current.indent < indent:
                break
            if current.indent > indent:
                raise YamlSubsetError(f"line {current.number}: unexpected indentation")
            if not (current.content.startswith("- ") or current.content == "-"):
                break
            item_text = current.content[1:].strip()
            index += 1
            if not item_text:
                if index < len(lines) and lines[index].indent > indent:
                    item, index = _parse_yaml_block(lines, index, lines[index].indent)
                else:
                    item = None
                output.append(item)
                continue
            if ":" in item_text and re.match(r"^[A-Za-z_][A-Za-z0-9_-]*\s*:", item_text):
                key, value = _split_mapping(item_text, current.number)
                item_dict: Dict[str, Any] = {key: _parse_scalar(value)}
                if not value and index < len(lines) and lines[index].indent > indent:
                    nested, index = _parse_yaml_block(lines, index, lines[index].indent)
                    item_dict[key] = nested
                if index < len(lines) and lines[index].indent > indent:
                    continuation, index = _parse_yaml_block(lines, index, lines[index].indent)
                    if not isinstance(continuation, dict):
                        raise YamlSubsetError(
                            f"line {lines[index - 1].number}: list mapping continuation must be a mapping"
                        )
                    item_dict.update(continuation)
                output.append(item_dict)
            else:
                output.append(_parse_scalar(item_text))
                if index < len(lines) and lines[index].indent > indent:
                    raise YamlSubsetError(
                        f"line {lines[index].number}: scalar list item cannot have nested content"
                    )
        return output, index

    output_dict: Dict[str, Any] = {}
    while index < len(lines):
        current = lines[index]
        if current.indent < indent:
            break
        if current.indent > indent:
            raise YamlSubsetError(f"line {current.number}: unexpected indentation")
        if current.content.startswith("-"):
            break
        key, value = _split_mapping(current.content, current.number)
        if key in output_dict:
            raise YamlSubsetError(f"line {current.number}: duplicate key {key!r}")
        index += 1
        if value:
            output_dict[key] = _parse_scalar(value)
        elif index < len(lines) and lines[index].indent > indent:
            nested, index = _parse_yaml_block(lines, index, lines[index].indent)
            output_dict[key] = nested
        else:
            output_dict[key] = None
    return output_dict, index


def parse_yaml_subset(text: str) -> Dict[str, Any]:
    """Parse the documented YAML subset used by the Atlas."""
    lines = _prepare_yaml(text)
    if not lines:
        return {}
    if lines[0].indent != 0:
        raise YamlSubsetError(f"line {lines[0].number}: top-level content must not be indented")
    result, index = _parse_yaml_block(lines, 0, 0)
    if index != len(lines):
        raise YamlSubsetError(f"line {lines[index].number}: could not parse content")
    if not isinstance(result, dict):
        raise YamlSubsetError("top-level YAML value must be a mapping")
    return result


@dataclasses.dataclass
class Issue:
    code: str
    path: Path
    message: str
    severity: str = "error"

    def display(self, base: Optional[Path] = None) -> str:
        try:
            shown = self.path.relative_to(base) if base else self.path
        except ValueError:
            shown = self.path
        return f"{self.severity.upper()} [{self.code}] {shown}: {self.message}"


@dataclasses.dataclass
class Page:
    path: Path
    metadata: Dict[str, Any]
    body: str
    anchors: List[str]
    links: List[str]

    @property
    def stem(self) -> str:
        return self.path.stem

    @property
    def page_type(self) -> Optional[str]:
        value = self.metadata.get("type")
        return value if isinstance(value, str) else None

    @property
    def title(self) -> str:
        value = self.metadata.get("title")
        return value if isinstance(value, str) and value else self.stem


def parse_markdown_text(path: Path, text: str) -> Tuple[Optional[Page], List[Issue]]:
    issues: List[Issue] = []
    lines = text.splitlines(keepends=True)
    if not lines or lines[0].strip() != "---":
        return None, [Issue("frontmatter.missing", path, "file must begin with YAML frontmatter")]
    closing = None
    for index in range(1, len(lines)):
        if lines[index].strip() == "---":
            closing = index
            break
    if closing is None:
        return None, [Issue("frontmatter.malformed", path, "missing closing '---'")]
    yaml_text = "".join(lines[1:closing])
    body = "".join(lines[closing + 1 :])
    try:
        metadata = parse_yaml_subset(yaml_text)
    except YamlSubsetError as exc:
        return None, [Issue("frontmatter.malformed", path, str(exc))]
    anchors = ANCHOR_RE.findall(body) + HEADING_RE.findall(body)
    links = WIKILINK_RE.findall(body)
    return Page(path, metadata, body, anchors, links), issues


def parse_markdown(path: Path) -> Tuple[Optional[Page], List[Issue]]:
    try:
        text = path.read_text(encoding="utf-8")
    except (OSError, UnicodeError) as exc:
        return None, [Issue("file.read", path, str(exc))]
    return parse_markdown_text(path, text)


def load_schema(root: Path) -> Dict[str, Any]:
    path = root / "system/schema.yaml"
    return parse_yaml_subset(path.read_text(encoding="utf-8"))


def content_markdown_files(content_root: Path) -> List[Path]:
    if content_root.is_file():
        return [content_root] if content_root.suffix.lower() == ".md" else []
    files: List[Path] = []
    for relative in ("evidence/sources", "wiki"):
        directory = content_root / relative
        if not directory.exists():
            continue
        for path in directory.rglob("*.md"):
            if path.name.startswith(".") or path.name == "index.md":
                continue
            files.append(path)
    return sorted(files, key=lambda item: str(item).lower())


def split_wikilink(value: Any) -> Tuple[Optional[str], Optional[str]]:
    if not isinstance(value, str):
        return None, None
    match = WIKILINK_RE.fullmatch(value.strip())
    if not match:
        return None, None
    inner = match.group(1).split("|", 1)[0].strip()
    target, separator, anchor = inner.partition("#")
    stem = Path(target).name
    if stem.endswith(".md"):
        stem = stem[:-3]
    return stem or None, anchor if separator else None


def _list_value(metadata: Dict[str, Any], key: str) -> List[Any]:
    value = metadata.get(key, [])
    return value if isinstance(value, list) else []


def _relationship_set(page: Page) -> set:
    output = set()
    for relation in _list_value(page.metadata, "relationships"):
        if not isinstance(relation, dict):
            continue
        target, _ = split_wikilink(relation.get("target"))
        if isinstance(relation.get("type"), str) and target:
            output.add((relation["type"], target))
    return output


def _validate_evidence_provenance(
    page: Page,
    content_root: Path,
    raw_cache: Dict[Path, Tuple[str, List[str]]],
) -> List[Issue]:
    """Validate the immutable raw-file chain for one Evidence page."""
    issues: List[Issue] = []
    metadata = page.metadata
    raw_value = metadata.get("raw_file")
    raw_path: Optional[Path] = None
    raw_info: Optional[Tuple[str, List[str]]] = None

    if not isinstance(raw_value, str) or not raw_value:
        issues.append(Issue("raw.path_invalid", page.path, "raw_file must be a repository-relative path"))
    else:
        supplied = Path(raw_value)
        if supplied.is_absolute() or ".." in supplied.parts or not supplied.parts or supplied.parts[0] != "raw":
            issues.append(
                Issue("raw.path_invalid", page.path, "raw_file must resolve beneath the repository raw/ directory")
            )
        elif content_root.is_dir():
            raw_root = (content_root / "raw").resolve()
            candidate = (content_root / supplied).resolve()
            try:
                candidate.relative_to(raw_root)
                raw_path = candidate
            except ValueError:
                issues.append(
                    Issue("raw.path_invalid", page.path, "raw_file escapes the repository raw/ directory")
                )
            if raw_path is not None and not raw_path.is_file():
                issues.append(Issue("raw.file_missing", page.path, f"raw file does not exist: {raw_value}"))
                raw_path = None

    supplied_hash = metadata.get("raw_sha256")
    if not isinstance(supplied_hash, str) or not re.fullmatch(r"[0-9a-f]{64}", supplied_hash):
        issues.append(Issue("raw.hash_invalid", page.path, "raw_sha256 must be 64 lowercase hexadecimal characters"))

    if raw_path is not None:
        if raw_path not in raw_cache:
            data = raw_path.read_bytes()
            try:
                raw_lines = data.decode("utf-8").splitlines()
            except UnicodeDecodeError:
                issues.append(Issue("raw.encoding", page.path, "raw Markdown must be UTF-8"))
                raw_lines = []
            raw_cache[raw_path] = (hashlib.sha256(data).hexdigest(), raw_lines)
        raw_info = raw_cache[raw_path]
        if isinstance(supplied_hash, str) and re.fullmatch(r"[0-9a-f]{64}", supplied_hash):
            if supplied_hash != raw_info[0]:
                issues.append(Issue("raw.hash_mismatch", page.path, "raw_sha256 does not match raw_file"))

    entry_index = metadata.get("raw_entry_index")
    if not isinstance(entry_index, int) or isinstance(entry_index, bool) or entry_index < 1:
        issues.append(Issue("raw.entry_invalid", page.path, "raw_entry_index must be a positive integer"))

    line_start = metadata.get("raw_line_start")
    line_end = metadata.get("raw_line_end")
    valid_start = isinstance(line_start, int) and not isinstance(line_start, bool) and line_start >= 1
    valid_end = isinstance(line_end, int) and not isinstance(line_end, bool) and line_end >= 1
    if not valid_start or not valid_end or (valid_start and valid_end and line_end < line_start):
        issues.append(
            Issue("raw.range_invalid", page.path, "raw line coordinates must be positive and end at or after start")
        )
    elif raw_info is not None and line_end > len(raw_info[1]):
        issues.append(
            Issue(
                "raw.range_invalid",
                page.path,
                f"raw_line_end {line_end} exceeds the raw file's {len(raw_info[1])} lines",
            )
        )

    quote_start = metadata.get("raw_quote_line_start")
    quote_end = metadata.get("raw_quote_line_end")
    if quote_start is not None or quote_end is not None:
        valid_quote_start = isinstance(quote_start, int) and not isinstance(quote_start, bool) and quote_start >= 1
        valid_quote_end = isinstance(quote_end, int) and not isinstance(quote_end, bool) and quote_end >= 1
        if (
            not valid_quote_start
            or not valid_quote_end
            or (valid_quote_start and valid_quote_end and quote_end < quote_start)
            or (valid_start and valid_end and valid_quote_start and valid_quote_end and not (line_start <= quote_start <= quote_end <= line_end))
        ):
            issues.append(
                Issue("raw.quote_range_invalid", page.path, "raw quote coordinates must be ordered within the entry range")
            )
        elif raw_info is not None and quote_end > len(raw_info[1]):
            issues.append(
                Issue("raw.quote_range_invalid", page.path, "raw quote coordinates exceed the raw file")
            )
        elif raw_info is not None:
            body_lines = page.body.splitlines()
            try:
                section_start = body_lines.index("## Curated excerpt") + 1
                section_end = next(
                    index
                    for index in range(section_start, len(body_lines))
                    if body_lines[index].startswith("## ")
                )
            except (ValueError, StopIteration):
                issues.append(Issue("evidence.excerpt_missing", page.path, "missing Curated excerpt section"))
            else:
                excerpt_lines = body_lines[section_start:section_end]
                while excerpt_lines and excerpt_lines[0] == "":
                    excerpt_lines.pop(0)
                while excerpt_lines and excerpt_lines[-1] == "":
                    excerpt_lines.pop()
                if not excerpt_lines or any(not line.startswith(">") for line in excerpt_lines):
                    issues.append(
                        Issue("evidence.excerpt_malformed", page.path, "Curated excerpt must contain only blockquote lines")
                    )
                else:
                    excerpt = "\n".join(line[2:] if line.startswith("> ") else line[1:] for line in excerpt_lines)
                    expected = "\n".join(raw_info[1][quote_start - 1 : quote_end])
                    if excerpt != expected:
                        issues.append(
                            Issue("evidence.excerpt_mismatch", page.path, "Curated excerpt differs from its raw quote lines")
                        )
    return issues


def _validate_evidence_source_metadata(page: Page, schema: Dict[str, Any]) -> List[Issue]:
    issues: List[Issue] = []
    metadata = page.metadata
    allowed_statuses = set(schema.get("evidence_source_metadata_statuses", []))
    recovered = False
    for value_field, status_field in (
        ("canonical_url", "canonical_url_status"),
        ("author", "author_status"),
        ("publisher", "publisher_status"),
    ):
        value = metadata.get(value_field)
        status = metadata.get(status_field)
        if status not in allowed_statuses:
            issues.append(
                Issue("source_metadata.status_invalid", page.path, f"{status_field} {status!r} is invalid")
            )
            continue
        if status == "unresolved" and value is not None:
            issues.append(
                Issue("source_metadata.status_conflict", page.path, f"{value_field} must be null when unresolved")
            )
        elif status in {"verified", "inferred"}:
            recovered = True
            if not isinstance(value, str) or not value.strip():
                issues.append(
                    Issue("source_metadata.value_missing", page.path, f"{value_field} requires a value when {status}")
                )
        if value_field == "canonical_url" and isinstance(value, str) and not re.match(r"^https?://", value):
            issues.append(
                Issue("source_metadata.url_invalid", page.path, "canonical_url must be an HTTP(S) URL")
            )

    date_status = metadata.get("date_status")
    date_precision = metadata.get("date_precision")
    published_at = metadata.get("published_at")
    date_source = metadata.get("date_source")
    if date_status not in set(schema.get("evidence_date_statuses", [])):
        issues.append(Issue("source_date.status_invalid", page.path, f"date_status {date_status!r} is invalid"))
    elif date_status == "unresolved":
        if published_at is not None or date_source is not None or date_precision != "unknown":
            issues.append(
                Issue(
                    "source_date.status_conflict",
                    page.path,
                    "unresolved publication dates require null value/source and unknown precision",
                )
            )
    else:
        recovered = True
        if date_precision not in set(schema.get("evidence_date_precisions", [])) - {"unknown"}:
            issues.append(
                Issue("source_date.precision_invalid", page.path, f"date_precision {date_precision!r} is invalid")
            )
        if not isinstance(date_source, str) or not date_source:
            issues.append(Issue("source_date.source_missing", page.path, "recovered date requires date_source"))
        valid_date = False
        if isinstance(published_at, str):
            try:
                if date_precision == "day" and ISO_DATE_RE.fullmatch(published_at):
                    dt.date.fromisoformat(published_at)
                    valid_date = True
                elif date_precision == "month" and re.fullmatch(r"\d{4}-\d{2}", published_at):
                    dt.date.fromisoformat(published_at + "-01")
                    valid_date = True
                elif date_precision == "year" and re.fullmatch(r"\d{4}", published_at):
                    valid_date = int(published_at) >= 1
            except ValueError:
                valid_date = False
        if not valid_date:
            issues.append(
                Issue("source_date.value_invalid", page.path, "published_at does not match date_precision")
            )

    checked_at = metadata.get("metadata_checked_at")
    valid_checked_at = False
    if isinstance(checked_at, str) and ISO_DATE_RE.fullmatch(checked_at):
        try:
            dt.date.fromisoformat(checked_at)
            valid_checked_at = True
        except ValueError:
            pass
    if checked_at is not None and not valid_checked_at:
        issues.append(
            Issue("source_metadata.checked_at_invalid", page.path, "metadata_checked_at must be null or ISO date")
        )
    if recovered and not valid_checked_at:
        issues.append(
            Issue("source_metadata.checked_at_missing", page.path, "recovered metadata requires metadata_checked_at")
        )
    return issues


def validate_content(content_root: Path, schema: Dict[str, Any]) -> Tuple[List[Page], List[Issue]]:
    paths = content_markdown_files(content_root)
    pages: List[Page] = []
    issues: List[Issue] = []
    for path in paths:
        page, page_issues = parse_markdown(path)
        issues.extend(page_issues)
        if page:
            pages.append(page)

    by_stem: Dict[str, List[Page]] = defaultdict(list)
    by_id: Dict[str, List[Page]] = defaultdict(list)
    for page in pages:
        by_stem[page.stem].append(page)
        page_id = page.metadata.get("id")
        if isinstance(page_id, str):
            by_id[page_id].append(page)

    for stem, matches in by_stem.items():
        if len(matches) > 1:
            for page in matches:
                issues.append(Issue("slug.duplicate", page.path, f"slug {stem!r} is not unique"))
    for page_id, matches in by_id.items():
        if len(matches) > 1:
            for page in matches:
                issues.append(Issue("id.duplicate", page.path, f"ID {page_id!r} is not unique"))

    types = schema.get("types", {})
    common_required = schema.get("common_required", [])
    date_fields = schema.get("date_fields", [])
    evidence_required = set(schema.get("evidence_required_for", []))
    relationship_inverses = schema.get("relationships", {})
    unique_pages = {stem: matches[0] for stem, matches in by_stem.items() if len(matches) == 1}
    raw_cache: Dict[Path, Tuple[str, List[str]]] = {}

    for page in pages:
        metadata = page.metadata
        for field in common_required:
            if field not in metadata:
                issues.append(Issue("field.missing", page.path, f"missing required field {field!r}"))

        page_type = page.page_type
        type_schema = types.get(page_type) if page_type else None
        if not isinstance(type_schema, dict):
            issues.append(Issue("type.unknown", page.path, f"unknown page type {page_type!r}"))
            type_schema = None
        else:
            for field in type_schema.get("required", []):
                if field not in metadata:
                    issues.append(Issue("field.missing", page.path, f"missing required field {field!r}"))
            status = metadata.get("status")
            if status not in type_schema.get("statuses", []):
                issues.append(
                    Issue("status.invalid", page.path, f"status {status!r} is invalid for {page_type}")
                )
            page_id = metadata.get("id")
            prefix = type_schema.get("id_prefix", "")
            if isinstance(page_id, str):
                if not ID_RE.fullmatch(page_id):
                    issues.append(Issue("id.invalid", page.path, f"ID {page_id!r} has invalid form"))
                elif prefix and not page_id.startswith(prefix):
                    issues.append(
                        Issue("id.prefix", page.path, f"ID {page_id!r} must start with {prefix!r}")
                    )
            expected_directory = type_schema.get("directory")
            if content_root.is_dir() and isinstance(expected_directory, str):
                try:
                    relative = page.path.relative_to(content_root)
                    actual_directory = relative.parent.as_posix()
                    if actual_directory != expected_directory:
                        issues.append(
                            Issue(
                                "path.type_mismatch",
                                page.path,
                                f"type {page_type!r} belongs in {expected_directory!r}, not {actual_directory!r}",
                            )
                        )
                except ValueError:
                    pass

        if not SLUG_RE.fullmatch(page.stem):
            issues.append(Issue("slug.invalid", page.path, "filename must be a lowercase kebab-case slug"))

        page_date_fields = list(date_fields)
        if isinstance(type_schema, dict):
            page_date_fields.extend(type_schema.get("date_fields", []))
        for field in page_date_fields:
            value = metadata.get(field)
            if not isinstance(value, str) or not ISO_DATE_RE.fullmatch(value):
                issues.append(Issue("date.invalid", page.path, f"{field} must be an ISO YYYY-MM-DD string"))
            else:
                try:
                    dt.date.fromisoformat(value)
                except ValueError:
                    issues.append(Issue("date.invalid", page.path, f"{field} is not a real calendar date"))

        tags = metadata.get("tags")
        if "tags" in metadata and not isinstance(tags, list):
            issues.append(Issue("field.type", page.path, "tags must be a list"))
        relationships = metadata.get("relationships")
        if "relationships" in metadata and not isinstance(relationships, list):
            issues.append(Issue("field.type", page.path, "relationships must be a list"))

        if page_type in evidence_required:
            refs = metadata.get("evidence")
            if not isinstance(refs, list) or not refs:
                issues.append(
                    Issue("evidence.missing", page.path, f"{page_type} pages require at least one Evidence claim")
                )

        for anchor, count in Counter(page.anchors).items():
            if count > 1:
                issues.append(Issue("anchor.duplicate", page.path, f"anchor {anchor!r} occurs more than once"))

        if page_type == "evidence":
            issues.extend(_validate_evidence_provenance(page, content_root, raw_cache))
            issues.extend(_validate_evidence_source_metadata(page, schema))
            claim_heading_numbers = CLAIM_HEADING_RE.findall(page.body)
            claim_heading_lines = re.findall(r"(?m)^### (Claim(?:\s+.*)?)\s*$", page.body)
            claim_anchors = [f"Claim {number}" for number in claim_heading_numbers]
            claim_status = metadata.get("claim_extraction_status")
            allowed_claim_statuses = schema.get("evidence_claim_extraction_statuses", [])
            if claim_status not in allowed_claim_statuses:
                issues.append(
                    Issue(
                        "evidence.claim_status_invalid",
                        page.path,
                        f"claim_extraction_status {claim_status!r} is invalid",
                    )
                )
            elif claim_status == "complete_with_claims" and not claim_anchors:
                issues.append(
                    Issue("evidence.claim_missing", page.path, "completed claim extraction requires a claim anchor")
                )
            elif claim_status == "complete_no_claims" and claim_anchors:
                issues.append(
                    Issue("evidence.claim_status_conflict", page.path, "complete_no_claims cannot contain claim anchors")
                )
            if metadata.get("status") == "active" and claim_status == "pending":
                issues.append(
                    Issue("evidence.claim_pending", page.path, "active Evidence cannot have pending claim extraction")
                )
            classifications = re.findall(r"(?m)^- Classification: `([^`]+)`\s*$", page.body)
            if len(classifications) != len(claim_anchors):
                issues.append(
                    Issue(
                        "evidence.claim_classification_count",
                        page.path,
                        "each claim anchor requires exactly one Classification field",
                    )
                )
            if len(claim_heading_lines) != len(claim_anchors):
                issues.append(
                    Issue(
                        "evidence.claim_heading_count",
                        page.path,
                        "claim headings must use the exact form '### Claim N'",
                    )
                )
            else:
                for index, heading_number in enumerate(claim_heading_numbers, 1):
                    if int(heading_number) != index:
                        issues.append(
                            Issue(
                                "evidence.claim_heading_mismatch",
                                page.path,
                                f"claim heading {heading_number} must appear in sequence as Claim {index}",
                            )
                        )
            for field in ("Scope", "Date relevance", "Qualification"):
                field_count = len(re.findall(rf"(?m)^- {re.escape(field)}: .+$", page.body))
                if field_count != len(claim_anchors):
                    issues.append(
                        Issue(
                            "evidence.claim_field_count",
                            page.path,
                            f"each claim requires exactly one {field} field",
                        )
                    )
            allowed_classes = set(schema.get("claim_classes", []))
            for classification in classifications:
                if classification not in allowed_classes:
                    issues.append(
                        Issue(
                            "evidence.claim_class_invalid",
                            page.path,
                            f"unsupported claim classification {classification!r}",
                        )
                    )
            expected_anchors = [f"Claim {index}" for index in range(1, len(claim_anchors) + 1)]
            if claim_anchors != expected_anchors:
                issues.append(
                    Issue(
                        "evidence.claim_anchor_sequence",
                        page.path,
                        "claim headings must be unique and sequential from Claim 1",
                    )
                )

    # Resolve body links, evidence citations, relationships, and inverses after all pages exist.
    for page in pages:
        for raw_link in page.links:
            target, anchor = split_wikilink(f"[[{raw_link}]]")
            if not target or target not in unique_pages:
                issues.append(Issue("link.broken", page.path, f"unresolved link [[{raw_link}]]"))
            elif anchor and anchor not in unique_pages[target].anchors:
                issues.append(
                    Issue("anchor.broken", page.path, f"link [[{raw_link}]] targets a missing anchor")
                )

        refs = page.metadata.get("evidence", [])
        if isinstance(refs, list):
            for ref in refs:
                target, anchor = split_wikilink(ref)
                if not target or target not in unique_pages:
                    issues.append(Issue("evidence.broken", page.path, f"unresolved Evidence reference {ref!r}"))
                    continue
                evidence_page = unique_pages[target]
                if evidence_page.page_type != "evidence":
                    issues.append(
                        Issue("evidence.wrong_type", page.path, f"reference {ref!r} does not target Evidence")
                    )
                if not anchor:
                    issues.append(
                        Issue("evidence.anchor_required", page.path, f"reference {ref!r} must target a claim anchor")
                    )
                elif anchor not in evidence_page.anchors:
                    issues.append(
                        Issue("evidence.broken", page.path, f"claim anchor in {ref!r} does not exist")
                    )

        relationships = page.metadata.get("relationships", [])
        if not isinstance(relationships, list):
            continue
        for index, relation in enumerate(relationships, 1):
            if not isinstance(relation, dict):
                issues.append(
                    Issue("relationship.malformed", page.path, f"relationship {index} must be a mapping")
                )
                continue
            relation_type = relation.get("type")
            target_value = relation.get("target")
            if relation_type not in relationship_inverses:
                issues.append(
                    Issue("relationship.unknown", page.path, f"unknown relationship type {relation_type!r}")
                )
                continue
            target, _ = split_wikilink(target_value)
            if not target or target not in unique_pages:
                issues.append(
                    Issue("relationship.broken", page.path, f"unresolved relationship target {target_value!r}")
                )
                continue
            inverse = relationship_inverses[relation_type]
            if (inverse, page.stem) not in _relationship_set(unique_pages[target]):
                issues.append(
                    Issue(
                        "relationship.inverse_missing",
                        page.path,
                        f"{relation_type} → {target} requires {inverse} → {page.stem}",
                    )
                )

    return pages, sorted(issues, key=lambda issue: (str(issue.path), issue.code, issue.message))


def _relative_wikilink(page: Page, root: Path) -> str:
    relative = page.path.relative_to(root).with_suffix("").as_posix()
    return f"[[{relative}|{page.title}]]"


def render_system_index(pages: Sequence[Page], root: Path) -> str:
    lines = [
        "# Change Atlas Index",
        "",
        "Generated by `tools/wiki index`. Do not edit manually.",
        "",
    ]
    if not pages:
        lines.extend(["_No Evidence or Wiki pages yet._", ""])
        return "\n".join(lines)
    grouped: Dict[str, List[Page]] = defaultdict(list)
    for page in pages:
        grouped[page.page_type or "unknown"].append(page)
    order = ["hub", "signal", "concept", "framework", "proposition", "trend", "debate", "question", "evidence"]
    labels = {
        "hub": "Hubs",
        "signal": "Signals",
        "trend": "Trends",
        "concept": "Concepts",
        "framework": "Frameworks",
        "proposition": "Propositions",
        "debate": "Debates",
        "question": "Questions",
        "evidence": "Evidence",
        "unknown": "Unknown",
    }
    for page_type in order + sorted(set(grouped) - set(order)):
        entries = grouped.get(page_type)
        if not entries:
            continue
        lines.extend([f"## {labels.get(page_type, page_type.title())}", ""])
        for page in sorted(entries, key=lambda item: (item.title.lower(), item.stem)):
            description = page.metadata.get("description")
            suffix = f" — {description}" if isinstance(description, str) and description else ""
            lines.append(f"- {_relative_wikilink(page, root)}{suffix}")
        lines.append("")
    return "\n".join(lines)


def render_evidence_index(pages: Sequence[Page], root: Path) -> str:
    evidence = [page for page in pages if page.page_type == "evidence"]
    lines = [
        "# Evidence Index",
        "",
        "Generated by `tools/wiki index`. Do not edit manually.",
        "",
    ]
    if not evidence:
        lines.extend(["_No Evidence pages yet._", ""])
    else:
        grouped: Dict[Tuple[str, str], List[Page]] = defaultdict(list)
        for page in evidence:
            curated_path = page.metadata.get("curated_path")
            if isinstance(curated_path, list) and len(curated_path) >= 2:
                key = (str(curated_path[0]), str(curated_path[1]))
            else:
                key = ("Unplaced", "Unplaced")
            grouped[key].append(page)
        ordered_groups = sorted(
            grouped.items(),
            key=lambda item: min(
                page.metadata.get("global_position", 10**9)
                if isinstance(page.metadata.get("global_position"), int)
                else 10**9
                for page in item[1]
            ),
        )
        current_h1: Optional[str] = None
        for (h1, h2), group_pages in ordered_groups:
            if h1 != current_h1:
                lines.extend([f"## {h1}", ""])
                current_h1 = h1
            lines.extend([f"### {h2}", ""])
            for page in sorted(
                group_pages,
                key=lambda item: (
                    item.metadata.get("collection_position", 10**9)
                    if isinstance(item.metadata.get("collection_position"), int)
                    else 10**9,
                    item.title.lower(),
                    item.stem,
                ),
            ):
                position = page.metadata.get("collection_position")
                prefix = f"{position}. " if isinstance(position, int) else ""
                lines.append(f"- {prefix}{_relative_wikilink(page, root)}")
            lines.append("")
    return "\n".join(lines)


def load_collection_tracker(root: Path) -> Dict[str, Any]:
    path = root / "system/collections.json"
    tracker = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(tracker, dict) or tracker.get("schema_version") != 1:
        raise ValueError("collection tracker must use schema_version 1")
    raw_file = tracker.get("raw_file")
    chunk_size = tracker.get("processing_chunk_size")
    collections = tracker.get("collections")
    if not isinstance(raw_file, str) or not raw_file.startswith("raw/"):
        raise ValueError("collection tracker raw_file must point beneath raw/")
    if not isinstance(chunk_size, int) or isinstance(chunk_size, bool) or chunk_size < 1:
        raise ValueError("processing_chunk_size must be a positive integer")
    if not isinstance(collections, list) or not collections:
        raise ValueError("collection tracker must contain collections")

    plan = json.loads((root / "system/bootstrap/ingestion-plan.json").read_text(encoding="utf-8"))
    plan_entries = plan.get("entries") if isinstance(plan, dict) else None
    if not isinstance(plan_entries, list):
        raise ValueError("bootstrap ingestion plan has no entries")
    expected: Dict[Tuple[str, str], List[int]] = {}
    expected_order: List[Tuple[str, str]] = []
    for entry in plan_entries:
        if not isinstance(entry, dict):
            raise ValueError("bootstrap ingestion plan contains a malformed entry")
        curated_path = entry.get("curated_path")
        position = entry.get("global_position")
        if (
            not isinstance(curated_path, list)
            or len(curated_path) != 2
            or not all(isinstance(value, str) for value in curated_path)
            or not isinstance(position, int)
        ):
            raise ValueError("bootstrap ingestion plan contains invalid collection data")
        key = (curated_path[0], curated_path[1])
        if key not in expected:
            expected[key] = []
            expected_order.append(key)
        expected[key].append(position)

    seen_ids = set()
    actual_order: List[Tuple[str, str]] = []
    for record in collections:
        if not isinstance(record, dict):
            raise ValueError("collection tracker records must be mappings")
        collection_id = record.get("id")
        h1 = record.get("h1")
        h2 = record.get("h2")
        key = (h1, h2)
        if not isinstance(collection_id, str) or not SLUG_RE.fullmatch(collection_id):
            raise ValueError(f"invalid collection id {collection_id!r}")
        if collection_id in seen_ids:
            raise ValueError(f"duplicate collection id {collection_id!r}")
        seen_ids.add(collection_id)
        if key not in expected:
            raise ValueError(f"unknown tracked collection {h1!r} → {h2!r}")
        positions = expected[key]
        if (
            record.get("entries") != len(positions)
            or record.get("entry_start") != positions[0]
            or record.get("entry_end") != positions[-1]
        ):
            raise ValueError(f"tracked range differs from ingestion plan for {collection_id}")
        if record.get("stage") not in COLLECTION_STAGES:
            raise ValueError(f"invalid stage for {collection_id}: {record.get('stage')!r}")
        if record.get("signoff_mode") not in SIGNOFF_MODES:
            raise ValueError(f"invalid signoff_mode for {collection_id}: {record.get('signoff_mode')!r}")
        if record.get("stage") == "committed" and not isinstance(record.get("checkpoint"), str):
            raise ValueError(f"committed collection {collection_id} requires a checkpoint")
        actual_order.append(key)
    if actual_order != expected_order:
        raise ValueError("collection tracker order differs from the ingestion plan")
    return tracker


def load_synthesis_backlog(root: Path) -> Dict[str, Any]:
    path = root / "system/synthesis-backlog.json"
    backlog = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(backlog, dict) or backlog.get("schema_version") != 1:
        raise ValueError("synthesis backlog must use schema_version 1")
    propositions = backlog.get("propositions")
    if not isinstance(propositions, list):
        raise ValueError("synthesis backlog propositions must be a list")
    return backlog


def validate_synthesis_backlog(
    root: Path,
    pages: Iterable[Page],
    tracker: Dict[str, Any],
    backlog: Optional[Dict[str, Any]] = None,
) -> List[Issue]:
    path = root / "system/synthesis-backlog.json"
    issues: List[Issue] = []
    if backlog is None:
        try:
            backlog = load_synthesis_backlog(root)
        except (OSError, ValueError, json.JSONDecodeError) as exc:
            return [Issue("backlog.invalid", path, str(exc))]

    collection_by_id = {record["id"]: record for record in tracker["collections"]}
    page_by_stem = {page.stem: page for page in pages}
    seen_ids = set()
    for index, proposition in enumerate(backlog["propositions"], 1):
        label = f"proposition {index}"
        if not isinstance(proposition, dict):
            issues.append(Issue("backlog.record_invalid", path, f"{label} must be a mapping"))
            continue
        proposition_id = proposition.get("id")
        if not isinstance(proposition_id, str) or not PROPOSITION_ID_RE.fullmatch(proposition_id):
            issues.append(Issue("backlog.id_invalid", path, f"{label} has invalid id {proposition_id!r}"))
        elif proposition_id in seen_ids:
            issues.append(Issue("backlog.id_duplicate", path, f"duplicate proposition id {proposition_id!r}"))
        else:
            seen_ids.add(proposition_id)
            label = proposition_id

        statement = proposition.get("statement")
        if not isinstance(statement, str) or not statement.strip():
            issues.append(Issue("backlog.statement_missing", path, f"{label} requires a statement"))
        status = proposition.get("status")
        if status not in PROPOSITION_STATUSES:
            issues.append(Issue("backlog.status_invalid", path, f"{label} has invalid status {status!r}"))

        origin = proposition.get("origin_collection")
        if origin not in collection_by_id:
            issues.append(Issue("backlog.collection_unknown", path, f"{label} has unknown origin {origin!r}"))
        surfaced_in = proposition.get("surfaced_in")
        if not isinstance(surfaced_in, str) or not surfaced_in.startswith("wiki/"):
            issues.append(Issue("backlog.surface_invalid", path, f"{label} must point surfaced_in beneath wiki/"))
        elif not (root / f"{surfaced_in}.md").is_file():
            issues.append(Issue("backlog.surface_missing", path, f"{label} surfaced_in page does not exist"))

        evidence = proposition.get("evidence")
        if not isinstance(evidence, list) or not evidence:
            issues.append(Issue("backlog.evidence_missing", path, f"{label} requires Evidence claims"))
        else:
            for reference in evidence:
                target, anchor = split_wikilink(reference)
                target_page = page_by_stem.get(target) if target else None
                if target_page is None or target_page.page_type != "evidence":
                    issues.append(Issue("backlog.evidence_broken", path, f"{label} has invalid Evidence link {reference!r}"))
                elif not anchor or anchor not in target_page.anchors:
                    issues.append(Issue("backlog.evidence_anchor", path, f"{label} link {reference!r} must target a claim"))
                elif target_page.metadata.get("status") != "active":
                    issues.append(Issue("backlog.evidence_inactive", path, f"{label} cites inactive Evidence {reference!r}"))

        relevant = proposition.get("relevant_collections")
        if not isinstance(relevant, list) or not relevant:
            issues.append(Issue("backlog.relevance_missing", path, f"{label} requires relevant_collections"))
            relevant = []
        elif len(relevant) != len(set(value for value in relevant if isinstance(value, str))):
            issues.append(Issue("backlog.relevance_duplicate", path, f"{label} repeats a relevant collection"))
        for collection_id in relevant:
            if collection_id not in collection_by_id:
                issues.append(Issue("backlog.collection_unknown", path, f"{label} has unknown relevant collection {collection_id!r}"))

        assessments = proposition.get("assessments")
        if not isinstance(assessments, list) or not assessments:
            issues.append(Issue("backlog.assessment_missing", path, f"{label} requires an assessment history"))
            assessments = []
        assessed_collections = set()
        for assessment in assessments:
            if not isinstance(assessment, dict):
                issues.append(Issue("backlog.assessment_invalid", path, f"{label} has a malformed assessment"))
                continue
            collection_id = assessment.get("collection")
            if collection_id not in collection_by_id:
                issues.append(Issue("backlog.collection_unknown", path, f"{label} assessment has unknown collection {collection_id!r}"))
            elif collection_id in assessed_collections:
                issues.append(Issue("backlog.assessment_duplicate", path, f"{label} has multiple assessments for {collection_id}"))
            else:
                assessed_collections.add(collection_id)
            date = assessment.get("date")
            try:
                valid_date = isinstance(date, str) and bool(ISO_DATE_RE.fullmatch(date))
                if valid_date:
                    dt.date.fromisoformat(date)
            except ValueError:
                valid_date = False
            if not valid_date:
                issues.append(Issue("backlog.assessment_date", path, f"{label} assessment requires a valid ISO date"))
            if assessment.get("outcome") not in PROPOSITION_OUTCOMES:
                issues.append(Issue("backlog.assessment_outcome", path, f"{label} assessment has invalid outcome"))
            if not isinstance(assessment.get("note"), str) or not assessment["note"].strip():
                issues.append(Issue("backlog.assessment_note", path, f"{label} assessment requires a note"))
        if origin in collection_by_id and origin not in assessed_collections:
            issues.append(Issue("backlog.origin_unassessed", path, f"{label} requires an assessment from its origin collection"))

        resolution_target = proposition.get("resolution_target")
        if status == "promoted":
            target, anchor = split_wikilink(resolution_target)
            target_page = page_by_stem.get(target) if target else None
            if target_page is None or target_page.page_type == "evidence" or anchor:
                issues.append(Issue("backlog.resolution_missing", path, f"promoted {label} requires a Wiki resolution_target"))
            elif target_page.page_type == "proposition" and target_page.metadata.get("id") != proposition_id:
                issues.append(
                    Issue(
                        "backlog.resolution_identity",
                        path,
                        f"promoted {label} must retain its identity on Proposition page {target!r}",
                    )
                )
        elif resolution_target is not None:
            issues.append(Issue("backlog.resolution_conflict", path, f"unpromoted {label} must have null resolution_target"))

        if status not in {"promoted", "retired"}:
            for collection_id in relevant:
                record = collection_by_id.get(collection_id)
                if record and record.get("stage") in SYNTHESIS_COMPLETE_STAGES and collection_id not in assessed_collections:
                    issues.append(
                        Issue(
                            "backlog.relevant_unassessed",
                            path,
                            f"{label} requires an assessment before {collection_id} reaches {record['stage']}",
                        )
                    )
    return issues


def _collection_evidence_pages(pages: Iterable[Page], record: Dict[str, Any]) -> List[Page]:
    expected_path = [record["h1"], record["h2"]]
    return [
        page
        for page in pages
        if page.page_type == "evidence" and page.metadata.get("curated_path") == expected_path
    ]


def render_collection_dashboard(root: Path, pages: Iterable[Page], tracker: Dict[str, Any]) -> str:
    pages = list(pages)
    backlog = load_synthesis_backlog(root)
    lines = [
        "# Collection workflow",
        "",
        "This dashboard is generated from `system/collections.json` and repository content. Pipeline stages are handled by the Atlas workflow. Only **awaiting editorial sign-off** requires the editor.",
        "",
        "| Collection | Entries | Evidence | Claims | Pipeline stage | Sign-off | Review | Checkpoint |",
        "|---|---:|---:|---:|---|---|---|---|",
    ]
    for record in tracker["collections"]:
        evidence = _collection_evidence_pages(pages, record)
        claims = sum(len(CLAIM_HEADING_RE.findall(page.body)) for page in evidence)
        review_path = root / "system/reviews" / f"{record['id']}.md"
        review = f"[[system/reviews/{record['id']}|Open report]]" if review_path.exists() else "—"
        checkpoint = f"`{record['checkpoint']}`" if record.get("checkpoint") else "—"
        signoff_labels = {"required": "Required", "autonomous": "Autonomous", "completed": "Completed"}
        stage = str(record["stage"]).replace("_", " ").title()
        collection = f"{record['h1']} / {record['h2']}"
        lines.append(
            f"| {collection} | {record['entries']} | {len(evidence)} | {claims} | {stage} | "
            f"{signoff_labels[record['signoff_mode']]} | {review} | {checkpoint} |"
        )
    completed = sum(record["stage"] == "committed" for record in tracker["collections"])
    total_entries = sum(record["entries"] for record in tracker["collections"])
    proposition_counts = Counter(record["status"] for record in backlog["propositions"])
    unresolved_propositions = sum(
        proposition_counts[status]
        for status in ("open", "strengthened", "qualified", "contested")
    )
    lines.extend([
        "",
        "## Progress",
        "",
        f"- Collection checkpoints committed: {completed}/{len(tracker['collections'])}",
        f"- Planned source entries: {total_entries}",
        f"- Preferred processing chunk: up to {tracker['processing_chunk_size']} entries",
        "",
        "## Synthesis backlog",
        "",
        f"- Tracked propositions: {len(backlog['propositions'])}",
        f"- Unresolved propositions: {unresolved_propositions}",
        f"- Promoted propositions: {proposition_counts['promoted']}",
        f"- Retired propositions: {proposition_counts['retired']}",
        "- Pipeline source of truth: `system/synthesis-backlog.json`",
        "",
        "## Stage meanings",
        "",
        "`planned → evidence ingested → metadata checked → claims extracted → synthesis ready` are pipeline stages.",
        "",
        "`awaiting editorial sign-off` is the sole human gate. After the designated sign-off collection, later collections use autonomous validated checkpoints.",
        "",
    ])
    return "\n".join(lines)


def _write_or_check(path: Path, content: str, check: bool) -> bool:
    existing = path.read_text(encoding="utf-8") if path.exists() else None
    if existing == content:
        return False
    if not check:
        path.parent.mkdir(parents=True, exist_ok=True)
        temporary = path.with_name(path.name + ".tmp")
        temporary.write_text(content, encoding="utf-8")
        os.replace(temporary, path)
    return True


def command_dashboard(root: Path, check: bool = False) -> int:
    tracker = load_collection_tracker(root)
    schema = load_schema(root)
    pages, issues = validate_content(root, schema)
    issues.extend(validate_synthesis_backlog(root, pages, tracker))
    if issues:
        print("Cannot generate the dashboard until validation succeeds.", file=sys.stderr)
        return 1
    path = root / "system/dashboard.md"
    changed = _write_or_check(path, render_collection_dashboard(root, pages, tracker), check)
    if check and changed:
        print(f"STALE {path.relative_to(root)}")
        return 1
    print(f"{'UPDATED' if changed else 'CURRENT'} {path.relative_to(root)}")
    return 0


def _git_output(root: Path, arguments: Sequence[str], allow_failure: bool = False) -> str:
    result = subprocess.run(
        ["git", *arguments],
        cwd=root,
        check=False,
        text=True,
        capture_output=True,
    )
    if result.returncode and not allow_failure:
        raise ValueError(result.stderr.strip() or f"git {' '.join(arguments)} failed")
    return result.stdout


def _git_page_at(root: Path, revision: str, relative: str) -> Optional[Page]:
    text = _git_output(root, ["show", f"{revision}:{relative}"], allow_failure=True)
    if not text:
        return None
    page, issues = parse_markdown_text(root / relative, text)
    return page if page is not None and not issues else None


def _wiki_delta(root: Path, baseline: str) -> List[Tuple[str, str]]:
    changed: Dict[str, str] = {}
    output = _git_output(root, ["diff", "--name-status", "--find-renames", baseline, "--", "wiki"])
    for line in output.splitlines():
        fields = line.split("\t")
        if len(fields) < 2:
            continue
        status = fields[0]
        path = fields[-1]
        if path.endswith(".md") and not path.endswith("/index.md"):
            changed[path] = status
    untracked = _git_output(root, ["ls-files", "--others", "--exclude-standard", "--", "wiki"])
    for path in untracked.splitlines():
        if path.endswith(".md") and not path.endswith("/index.md"):
            changed[path] = "A"
    return sorted(changed.items())


def _metadata_links(page: Optional[Page], field: str) -> set:
    if page is None:
        return set()
    if field == "relationships":
        return {
            (item.get("type"), item.get("target"))
            for item in _list_value(page.metadata, field)
            if isinstance(item, dict)
        }
    return {item for item in _list_value(page.metadata, field) if isinstance(item, str)}


def render_collection_review(root: Path, record: Dict[str, Any], baseline: str) -> str:
    schema = load_schema(root)
    pages, validation_issues = validate_content(root, schema)
    tracker = load_collection_tracker(root)
    backlog = load_synthesis_backlog(root)
    validation_issues.extend(validate_synthesis_backlog(root, pages, tracker, backlog))
    evidence = _collection_evidence_pages(pages, record)
    unresolved = sum(
        any(
            page.metadata.get(field) == "unresolved"
            for field in ("canonical_url_status", "author_status", "publisher_status", "date_status")
        )
        for page in evidence
    )
    claims = sum(len(CLAIM_HEADING_RE.findall(page.body)) for page in evidence)
    rows: List[str] = []
    candidate_trends: List[str] = []
    judgment_pages: List[str] = []
    destructive_changes: List[str] = []
    for relative, status in _wiki_delta(root, baseline):
        current_path = root / relative
        current, current_issues = parse_markdown(current_path) if current_path.exists() else (None, [])
        before = _git_page_at(root, baseline, relative)
        page = current or before
        if page is None:
            continue
        current_evidence = _metadata_links(current, "evidence")
        before_evidence = _metadata_links(before, "evidence")
        current_relationships = _metadata_links(current, "relationships")
        before_relationships = _metadata_links(before, "relationships")
        change = "Added" if status.startswith("A") else "Deleted" if status.startswith("D") else "Updated"
        rows.append(
            f"| {change} | {page.page_type or 'unknown'} | [[{relative[:-3]}|{page.title}]] | "
            f"+{len(current_evidence - before_evidence)}/−{len(before_evidence - current_evidence)} | "
            f"+{len(current_relationships - before_relationships)}/−{len(before_relationships - current_relationships)} |"
        )
        if page.page_type == "trend" and current is not None:
            candidate_trends.append(f"[[{relative[:-3]}|{page.title}]]")
        if page.page_type in {"debate", "question"} and current is not None:
            judgment_pages.append(f"[[{relative[:-3]}|{page.title}]]")
        if status.startswith(("D", "R")):
            destructive_changes.append(f"{change}: `{relative}`")
        validation_issues.extend(current_issues)

    signoff_required = record.get("signoff_mode") == "required"
    signoff_completed = record.get("signoff_mode") == "completed" or record.get("stage") == "signed_off"
    autonomous_completed = record.get("signoff_mode") == "autonomous" and record.get("stage") == "committed"
    signoff_state = "completed" if signoff_completed else "required" if signoff_required else "autonomous"
    lines = [
        "---",
        f"collection_id: {record['id']}",
        f"baseline: {baseline}",
        f"generated_at: {dt.date.today().isoformat()}",
        f"editorial_signoff: {signoff_state}",
        "---",
        "",
        f"# Review — {record['h1']} / {record['h2']}",
        "",
        "## Editorial decision",
        "",
        (
            "The editor signed off on this synthesized Wiki delta. Evidence metadata and claim extraction remain pipeline responsibilities."
            if signoff_completed
            else
            "Review and sign off on the synthesized Wiki delta below. Evidence metadata and claim extraction are pipeline responsibilities; drill into them only when an exception materially affects synthesis."
            if signoff_required
            else "This collection was checkpointed autonomously after validation. Material exceptions remain listed for audit."
            if autonomous_completed
            else "This collection is eligible for an autonomous checkpoint after validation. Material exceptions remain listed for audit."
        ),
        "",
        "## Pipeline state",
        "",
        f"- Source entries planned: {record['entries']}",
        f"- Evidence records present: {len(evidence)}",
        f"- Atomic claims extracted: {claims}",
        f"- Evidence records with unresolved source metadata: {unresolved}",
        f"- Deterministic validation issues: {len(validation_issues)}",
        f"- Comparison baseline: `{baseline}`",
        "",
        "## Wiki delta",
        "",
        "| Change | Type | Page | Evidence links +/− | Relationships +/− |",
        "|---|---|---|---:|---:|",
    ]
    lines.extend(rows or ["| — | — | No Wiki changes detected | — | — |"])
    opened_propositions = [
        proposition
        for proposition in backlog["propositions"]
        if proposition.get("origin_collection") == record["id"]
    ]
    assessed_propositions = [
        proposition
        for proposition in backlog["propositions"]
        if proposition.get("origin_collection") != record["id"]
        and any(
            assessment.get("collection") == record["id"]
            for assessment in proposition.get("assessments", [])
            if isinstance(assessment, dict)
        )
    ]
    unresolved_propositions = sum(
        proposition.get("status") in {"open", "strengthened", "qualified", "contested"}
        for proposition in backlog["propositions"]
    )
    lines.extend(["", "## Synthesis backlog", ""])
    lines.append(f"- Unresolved propositions carried across batches: {unresolved_propositions}")
    if opened_propositions:
        lines.append("- Opened by this collection:")
        for proposition in opened_propositions:
            lines.append(f"  - `{proposition['id']}` — {proposition['statement']} (`{proposition['status']}`)")
    else:
        lines.append("- Opened by this collection: none.")
    if assessed_propositions:
        lines.append("- Existing propositions assessed by this collection:")
        for proposition in assessed_propositions:
            assessment = next(
                item
                for item in proposition["assessments"]
                if item.get("collection") == record["id"]
            )
            lines.append(f"  - `{proposition['id']}` — `{assessment['outcome']}`: {assessment['note']}")
    else:
        lines.append("- Existing propositions assessed by this collection: none.")
    lines.append("- Full pipeline record: `system/synthesis-backlog.json`")
    lines.extend(["", "## Material review queue", ""])
    lines.append(
        "- Candidate Trends: " + ", ".join(candidate_trends)
        if candidate_trends else "- Candidate Trends: none."
    )
    lines.append(
        "- Changed Debates or Questions: " + ", ".join(judgment_pages)
        if judgment_pages else "- Changed Debates or Questions: none."
    )
    lines.append(
        "- Deletions or renames: " + "; ".join(destructive_changes)
        if destructive_changes else "- Deletions or renames: none."
    )
    lines.append(
        f"- Validation exceptions: {len(validation_issues)}; resolve before sign-off."
        if validation_issues else "- Validation exceptions: none."
    )
    if signoff_completed:
        lines.extend([
            "",
            "## Sign-off",
            "",
            "- Decision: signed off",
            f"- Date: {record.get('signed_off_at', dt.date.today().isoformat())}",
            "- Notes: Governance calibration approved as the standard for the autonomous collection loop.",
            "",
        ])
    elif autonomous_completed:
        lines.extend([
            "",
            "## Sign-off",
            "",
            "- Decision: autonomous checkpoint",
            f"- Date: {dt.date.today().isoformat()}",
            f"- Checkpoint: `{record.get('checkpoint', 'unrecorded')}`",
            "- Notes: Completed under the Governance-calibrated autonomous workflow; no editor sign-off was requested.",
            "",
        ])
    else:
        lines.extend(["", "## Sign-off", "", "- Decision: pending", "- Notes: —", ""])
    return "\n".join(lines)


def command_review_report(root: Path, collection_id: str, check: bool = False) -> int:
    tracker = load_collection_tracker(root)
    matches = [record for record in tracker["collections"] if record.get("id") == collection_id]
    if not matches:
        raise ValueError(f"unknown collection id {collection_id!r}")
    record = matches[0]
    baseline = record.get("baseline")
    if not isinstance(baseline, str) or not baseline:
        raise ValueError(f"collection {collection_id} has no comparison baseline")
    path = root / "system/reviews" / f"{collection_id}.md"
    changed = _write_or_check(path, render_collection_review(root, record, baseline), check)
    if check and changed:
        print(f"STALE {path.relative_to(root)}")
        return 1
    print(f"{'UPDATED' if changed else 'CURRENT'} {path.relative_to(root)}")
    return 0


def command_index(root: Path, check: bool = False) -> int:
    schema = load_schema(root)
    pages, issues = validate_content(root, schema)
    if issues:
        print("Cannot generate indexes until validation succeeds.", file=sys.stderr)
        for issue in issues:
            print(issue.display(root), file=sys.stderr)
        return 1
    desired = {
        root / "system/index.md": render_system_index(pages, root),
        root / "evidence/index.md": render_evidence_index(pages, root),
    }
    changed = [path for path, content in desired.items() if _write_or_check(path, content, check)]
    if check and changed:
        for path in changed:
            print(f"STALE {path.relative_to(root)}")
        return 1
    if changed:
        for path in changed:
            print(f"UPDATED {path.relative_to(root)}")
    else:
        print("Indexes are current.")
    return 0


def command_validate(root: Path, target: Optional[str]) -> int:
    schema = load_schema(root)
    content_root = (root / target).resolve() if target else root
    if not content_root.exists():
        print(f"ERROR: validation target does not exist: {content_root}", file=sys.stderr)
        return 2
    pages, issues = validate_content(content_root, schema)
    if target is None:
        try:
            tracker = load_collection_tracker(root)
            issues.extend(validate_synthesis_backlog(root, pages, tracker))
        except (OSError, ValueError, json.JSONDecodeError) as exc:
            issues.append(Issue("backlog.invalid", root / "system/synthesis-backlog.json", str(exc)))
    if issues:
        for issue in issues:
            print(issue.display(content_root))
        print(f"Validation failed: {len(issues)} issue(s) across {len(pages)} parsed page(s).")
        return 1
    print(f"Validation passed: {len(pages)} page(s), 0 issues.")
    return 0


def _managed_raw_files(root: Path) -> List[Path]:
    raw = root / "raw"
    if not raw.exists():
        return []
    return sorted(
        path
        for path in raw.rglob("*")
        if path.is_file() and not path.name.startswith(".")
    )


def command_status(root: Path, as_json: bool = False) -> int:
    schema = load_schema(root)
    pages, issues = validate_content(root, schema)
    try:
        tracker = load_collection_tracker(root)
        backlog = load_synthesis_backlog(root)
        issues.extend(validate_synthesis_backlog(root, pages, tracker, backlog))
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        backlog = {"propositions": []}
        issues.append(Issue("backlog.invalid", root / "system/synthesis-backlog.json", str(exc)))
    raw_files = _managed_raw_files(root)
    try:
        manifest = json.loads((root / "system/manifest.json").read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        manifest = {"files": {}}
    manifest_files = manifest.get("files", {}) if isinstance(manifest, dict) else {}
    raw_names = [path.relative_to(root).as_posix() for path in raw_files]
    processed = [
        name
        for name in raw_names
        if name in manifest_files
        and (
            not isinstance(manifest_files[name], dict)
            or manifest_files[name].get("status", "complete") == "complete"
        )
    ]
    partial = [
        name
        for name in raw_names
        if isinstance(manifest_files.get(name), dict)
        and manifest_files[name].get("status") == "partial"
    ]
    counts = Counter(page.page_type for page in pages)
    evidence = [page for page in pages if page.page_type == "evidence"]
    data = {
        "raw_files": len(raw_files),
        "processed_raw_files": len(processed),
        "partially_processed_raw_files": len(partial),
        "unprocessed_raw_files": len(raw_files) - len(processed) - len(partial),
        "evidence_pages": counts.get("evidence", 0),
        "draft_evidence_pages": sum(page.metadata.get("status") == "draft" for page in evidence),
        "active_evidence_pages": sum(page.metadata.get("status") == "active" for page in evidence),
        "atomic_claims": sum(len(CLAIM_HEADING_RE.findall(page.body)) for page in evidence),
        "claim_review_pending": sum(
            page.metadata.get("claim_extraction_status") == "pending" for page in evidence
        ),
        "reviewed_without_claims": sum(
            page.metadata.get("claim_extraction_status") == "complete_no_claims" for page in evidence
        ),
        "metadata_reviewed": sum(page.metadata.get("metadata_checked_at") is not None for page in evidence),
        "verified_publication_dates": sum(page.metadata.get("date_status") == "verified" for page in evidence),
        "inferred_publication_dates": sum(page.metadata.get("date_status") == "inferred" for page in evidence),
        "unresolved_publication_dates": sum(page.metadata.get("date_status") == "unresolved" for page in evidence),
        "wiki_pages": sum(count for page_type, count in counts.items() if page_type != "evidence"),
        "synthesis_propositions": len(backlog["propositions"]),
        "unresolved_synthesis_propositions": sum(
            proposition.get("status") in {"open", "strengthened", "qualified", "contested"}
            for proposition in backlog["propositions"]
        ),
        "validation_issues": len(issues),
    }
    if as_json:
        print(json.dumps(data, indent=2, sort_keys=True))
    else:
        width = max(len(key) for key in data)
        for key, value in data.items():
            print(f"{key.replace('_', ' ').title():<{width + 2}} {value}")
    return 1 if issues else 0


def command_doctor(root: Path) -> int:
    checks: List[Tuple[bool, str]] = []
    checks.append((sys.version_info >= MIN_PYTHON, f"Python {sys.version.split()[0]} (requires 3.9+)"))
    checks.append((root.is_dir(), f"repository root exists: {root}"))
    checks.append(((root / ".git").is_dir(), "local Git repository is initialized"))
    for relative in REQUIRED_DIRECTORIES:
        checks.append(((root / relative).is_dir(), f"directory {relative}"))
    for relative in REQUIRED_FILES:
        checks.append(((root / relative).is_file(), f"file {relative}"))
    checks.append((os.access(root / "tools/wiki", os.X_OK), "tools/wiki is executable"))
    try:
        schema = load_schema(root)
        checks.append((schema.get("schema_version") == 1, "schema version 1 loads"))
    except (OSError, YamlSubsetError) as exc:
        schema = None
        checks.append((False, f"schema loads: {exc}"))
    try:
        manifest = json.loads((root / "system/manifest.json").read_text(encoding="utf-8"))
        manifest_ok = (
            isinstance(manifest, dict)
            and manifest.get("schema_version") == 1
            and isinstance(manifest.get("files"), dict)
        )
        checks.append((manifest_ok, "manifest version 1 loads"))
    except (OSError, json.JSONDecodeError) as exc:
        checks.append((False, f"manifest loads: {exc}"))
    tracker = None
    try:
        tracker = load_collection_tracker(root)
        checks.append((len(tracker["collections"]) == 16, "collection tracker matches 16 editorial collections"))
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        checks.append((False, f"collection tracker loads: {exc}"))
    if schema is not None:
        pages, issues = validate_content(root, schema)
        if tracker is not None:
            try:
                backlog = load_synthesis_backlog(root)
                backlog_issues = validate_synthesis_backlog(root, pages, tracker, backlog)
                checks.append((not backlog_issues, f"synthesis backlog validates ({len(backlog_issues)} issue(s))"))
            except (OSError, ValueError, json.JSONDecodeError) as exc:
                checks.append((False, f"synthesis backlog loads: {exc}"))
        checks.append((not issues, f"repository content validates ({len(issues)} issue(s))"))
    for passed, label in checks:
        print(f"[{'ok' if passed else 'FAIL'}] {label}")
    failures = sum(1 for passed, _ in checks if not passed)
    print(f"Doctor {'passed' if not failures else 'failed'}: {failures} failure(s).")
    return 1 if failures else 0


def command_bootstrap_audit(root: Path, raw_file: str, write: bool = False) -> int:
    supplied = Path(raw_file)
    candidate = (root / supplied).resolve() if not supplied.is_absolute() else supplied.resolve()
    raw_root = (root / "raw").resolve()
    try:
        candidate.relative_to(raw_root)
    except ValueError:
        print("ERROR: bootstrap input must be located beneath raw/", file=sys.stderr)
        return 2
    if not candidate.is_file():
        print(f"ERROR: raw anthology does not exist: {candidate}", file=sys.stderr)
        return 2
    label = candidate.relative_to(root).as_posix()
    audit = parse_anthology(candidate, label)
    print(f"Raw file: {label}")
    print(f"SHA-256: {audit.raw_sha256}")
    print(f"H1 domains: {len(audit.h1_values)}")
    print(f"H2 collections: {len(audit.h2_paths)}")
    print(f"H3 entries: {len(audit.entries)}")
    print(f"Quote bodies: {audit.quote_count}")
    print(f"Errors: {audit.error_count}")
    print(f"Warnings: {audit.warning_count}")
    if write:
        output_directory = root / "system/bootstrap"
        output_directory.mkdir(parents=True, exist_ok=True)
        outputs = {
            output_directory / "anthology-audit.md": render_audit_markdown(audit),
            output_directory / "anthology-audit.json": render_audit_json(audit),
        }
        for path, content in outputs.items():
            temporary = path.with_name(path.name + ".tmp")
            temporary.write_text(content, encoding="utf-8")
            os.replace(temporary, path)
            print(f"WROTE {path.relative_to(root)}")
    return 1 if audit.error_count else 0


def _load_bootstrap(root: Path, raw_file: str):
    supplied = Path(raw_file)
    candidate = (root / supplied).resolve() if not supplied.is_absolute() else supplied.resolve()
    raw_root = (root / "raw").resolve()
    try:
        candidate.relative_to(raw_root)
    except ValueError as exc:
        raise ValueError("bootstrap input must be located beneath raw/") from exc
    if not candidate.is_file():
        raise ValueError(f"raw anthology does not exist: {candidate}")
    label = candidate.relative_to(root).as_posix()
    audit = parse_anthology(candidate, label)
    if audit.error_count:
        raise ValueError(f"bootstrap audit contains {audit.error_count} structural error(s)")
    return audit, build_ingestion_plan(audit)


def command_bootstrap_plan(root: Path, raw_file: str, write: bool = False) -> int:
    audit, plan = _load_bootstrap(root, raw_file)
    print(f"Raw file: {plan.raw_file}")
    print(f"SHA-256: {plan.raw_sha256}")
    print(f"Planned Evidence records: {len(plan.entries)}")
    print(f"Editorial collections: {len(audit.h2_paths)}")
    if write:
        output_directory = root / "system/bootstrap"
        output_directory.mkdir(parents=True, exist_ok=True)
        outputs = {
            output_directory / "ingestion-plan.md": render_plan_markdown(plan),
            output_directory / "ingestion-plan.json": render_plan_json(plan),
        }
        for path, content in outputs.items():
            temporary = path.with_name(path.name + ".tmp")
            temporary.write_text(content, encoding="utf-8")
            os.replace(temporary, path)
            print(f"WROTE {path.relative_to(root)}")
    return 0


def command_bootstrap_evidence(
    root: Path,
    raw_file: str,
    curated_h1: str,
    curated_h2: str,
    ingest_date: str,
    write: bool = False,
) -> int:
    try:
        dt.date.fromisoformat(ingest_date)
    except ValueError as exc:
        raise ValueError("--date must be a real ISO YYYY-MM-DD date") from exc
    audit, plan = _load_bootstrap(root, raw_file)
    selected = select_collection(audit, plan, curated_h1, curated_h2)
    rendered = [
        (plan_entry, render_evidence_draft(audit, source_entry, plan_entry, ingest_date))
        for source_entry, plan_entry in selected
    ]
    print(f"Collection: {curated_h1} → {curated_h2}")
    print(f"Evidence drafts: {len(rendered)}")
    print(f"Raw SHA-256: {audit.raw_sha256}")
    for plan_entry, _ in rendered:
        print(f"PLAN {plan_entry.evidence_file}")
    if not write:
        print("Dry run only; pass --write to create drafts.")
        return 0
    written, unchanged = write_evidence_drafts(root, rendered)
    print(f"WROTE {written} Evidence draft(s); {unchanged} unchanged.")
    print("Manifest and operation log remain unchanged until interpretive review and activation.")
    return 0


def command_bootstrap_register(
    root: Path,
    raw_file: str,
    curated_h1: str,
    curated_h2: str,
    completed_at: str,
    write: bool = False,
) -> int:
    try:
        dt.date.fromisoformat(completed_at)
    except ValueError as exc:
        raise ValueError("--date must be a real ISO YYYY-MM-DD date") from exc
    audit, plan = _load_bootstrap(root, raw_file)
    selected = select_collection(audit, plan, curated_h1, curated_h2)
    schema = load_schema(root)
    _, validation_issues = validate_content(root, schema)
    if validation_issues:
        raise ValueError(f"repository validation has {len(validation_issues)} issue(s)")

    evidence_records: Dict[str, Dict[str, str]] = {}
    for _, plan_entry in selected:
        page, page_issues = parse_markdown(root / plan_entry.evidence_file)
        if page_issues or page is None:
            raise ValueError(f"cannot parse reviewed Evidence: {plan_entry.evidence_file}")
        metadata = page.metadata
        expected = {
            "id": plan_entry.evidence_id,
            "raw_file": audit.raw_file,
            "raw_sha256": audit.raw_sha256,
            "raw_entry_index": plan_entry.global_position,
        }
        for field, value in expected.items():
            if metadata.get(field) != value:
                raise ValueError(f"{plan_entry.evidence_file} has unexpected {field}")
        if metadata.get("status") != "active":
            raise ValueError(f"{plan_entry.evidence_file} is not active")
        if metadata.get("claim_extraction_status") not in {"complete_with_claims", "complete_no_claims"}:
            raise ValueError(f"{plan_entry.evidence_file} has incomplete claim review")
        evidence_records[str(plan_entry.global_position)] = {
            "file": plan_entry.evidence_file,
            "id": plan_entry.evidence_id,
        }

    manifest_path = root / "system/manifest.json"
    original_manifest_content = manifest_path.read_text(encoding="utf-8")
    manifest = json.loads(original_manifest_content)
    files = manifest.setdefault("files", {})
    if not isinstance(files, dict):
        raise ValueError("manifest files must be a mapping")
    record = files.get(audit.raw_file)
    if record is None:
        record = {
            "collections": {},
            "evidence": {},
            "mode": "bootstrap_anthology",
            "raw_sha256": audit.raw_sha256,
            "status": "partial",
            "total_entries": len(plan.entries),
        }
    if not isinstance(record, dict):
        raise ValueError("bootstrap manifest record must be a mapping")
    if record.get("raw_sha256") != audit.raw_sha256:
        raise ValueError("manifest raw hash differs from the audited anthology")
    if record.get("mode") != "bootstrap_anthology" or record.get("total_entries") != len(plan.entries):
        raise ValueError("manifest bootstrap identity differs from the ingestion plan")
    existing_evidence = record.setdefault("evidence", {})
    collections = record.setdefault("collections", {})
    if not isinstance(existing_evidence, dict) or not isinstance(collections, dict):
        raise ValueError("manifest bootstrap evidence and collections must be mappings")
    for index, evidence_record in evidence_records.items():
        existing = existing_evidence.get(index)
        if existing is not None and existing != evidence_record:
            raise ValueError(f"manifest entry {index} conflicts with reviewed Evidence")
        existing_evidence[index] = evidence_record
    collection_key = f"{curated_h1} → {curated_h2}"
    collection_record = {
        "completed_at": completed_at,
        "entry_end": selected[-1][1].global_position,
        "entry_start": selected[0][1].global_position,
        "evidence_ids": [plan_entry.evidence_id for _, plan_entry in selected],
    }
    existing_collection = collections.get(collection_key)
    if existing_collection is not None and existing_collection != collection_record:
        raise ValueError(f"manifest collection conflicts with {collection_key}")
    collections[collection_key] = collection_record
    record["completed_entries"] = len(existing_evidence)
    record["status"] = "complete" if len(existing_evidence) == len(plan.entries) else "partial"
    files[audit.raw_file] = record

    print(f"Collection: {collection_key}")
    print(f"Reviewed Evidence: {len(selected)}")
    print(f"Anthology progress: {len(existing_evidence)}/{len(plan.entries)}")
    print(f"Manifest status: {record['status']}")
    if not write:
        print("Dry run only; pass --write to update the manifest.")
        return 0
    content = json.dumps(manifest, indent=2, ensure_ascii=False, sort_keys=True) + "\n"
    if content == original_manifest_content:
        print("Manifest is unchanged.")
        return 0
    temporary = manifest_path.with_name(manifest_path.name + ".tmp")
    temporary.write_text(content, encoding="utf-8")
    os.replace(temporary, manifest_path)
    print(f"WROTE {manifest_path.relative_to(root)}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="wiki", description="Change Atlas repository control plane")
    parser.add_argument(
        "--root",
        type=Path,
        default=DEFAULT_ROOT,
        help="repository root (defaults to the parent of tools/)",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)
    subparsers.add_parser("doctor", help="check repository installation and integrity")
    status = subparsers.add_parser("status", help="show corpus and Wiki state")
    status.add_argument("--json", action="store_true", help="emit machine-readable JSON")
    validate = subparsers.add_parser("validate", help="validate Evidence and Wiki Markdown")
    validate.add_argument(
        "target",
        nargs="?",
        help="optional repository-relative fixture or content directory",
    )
    index = subparsers.add_parser("index", help="regenerate deterministic indexes")
    index.add_argument("--check", action="store_true", help="fail instead of writing when indexes are stale")
    dashboard = subparsers.add_parser("dashboard", help="regenerate the collection workflow dashboard")
    dashboard.add_argument("--check", action="store_true", help="fail instead of writing when the dashboard is stale")
    review_report = subparsers.add_parser(
        "review-report",
        help="summarize the Wiki delta for one tracked collection",
    )
    review_report.add_argument("--collection", required=True, help="tracked collection id")
    review_report.add_argument("--check", action="store_true", help="fail instead of writing when the report is stale")
    bootstrap_audit = subparsers.add_parser(
        "bootstrap-audit",
        help="parse a raw anthology and report structural entries without creating Evidence",
    )
    bootstrap_audit.add_argument("raw_file", help="repository-relative Markdown file beneath raw/")
    bootstrap_audit.add_argument(
        "--write",
        action="store_true",
        help="write deterministic Markdown and JSON reports to system/bootstrap/",
    )
    bootstrap_plan = subparsers.add_parser(
        "bootstrap-plan",
        help="assign deterministic Evidence identities and destinations for an audited anthology",
    )
    bootstrap_plan.add_argument("raw_file", help="repository-relative Markdown file beneath raw/")
    bootstrap_plan.add_argument(
        "--write",
        action="store_true",
        help="write deterministic Markdown and JSON plans to system/bootstrap/",
    )
    bootstrap_evidence = subparsers.add_parser(
        "bootstrap-evidence",
        help="render a complete H1/H2 collection as provenance-complete draft Evidence",
    )
    bootstrap_evidence.add_argument("raw_file", help="repository-relative Markdown file beneath raw/")
    bootstrap_evidence.add_argument("--h1", required=True, help="exact inherited H1 heading")
    bootstrap_evidence.add_argument("--h2", required=True, help="exact inherited H2 heading")
    bootstrap_evidence.add_argument("--date", required=True, help="ingestion date in ISO YYYY-MM-DD form")
    bootstrap_evidence.add_argument("--write", action="store_true", help="create Evidence drafts")
    bootstrap_register = subparsers.add_parser(
        "bootstrap-register",
        help="register a validated, reviewed H1/H2 Evidence collection in the manifest",
    )
    bootstrap_register.add_argument("raw_file", help="repository-relative Markdown file beneath raw/")
    bootstrap_register.add_argument("--h1", required=True, help="exact inherited H1 heading")
    bootstrap_register.add_argument("--h2", required=True, help="exact inherited H2 heading")
    bootstrap_register.add_argument("--date", required=True, help="review completion date in ISO YYYY-MM-DD form")
    bootstrap_register.add_argument("--write", action="store_true", help="update the manifest")
    return parser


def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    root = args.root.expanduser().resolve()
    try:
        if args.command == "doctor":
            return command_doctor(root)
        if args.command == "status":
            return command_status(root, args.json)
        if args.command == "validate":
            return command_validate(root, args.target)
        if args.command == "index":
            return command_index(root, args.check)
        if args.command == "dashboard":
            return command_dashboard(root, args.check)
        if args.command == "review-report":
            return command_review_report(root, args.collection, args.check)
        if args.command == "bootstrap-audit":
            return command_bootstrap_audit(root, args.raw_file, args.write)
        if args.command == "bootstrap-plan":
            return command_bootstrap_plan(root, args.raw_file, args.write)
        if args.command == "bootstrap-evidence":
            return command_bootstrap_evidence(
                root,
                args.raw_file,
                args.h1,
                args.h2,
                args.date,
                args.write,
            )
        if args.command == "bootstrap-register":
            return command_bootstrap_register(
                root,
                args.raw_file,
                args.h1,
                args.h2,
                args.date,
                args.write,
            )
    except (OSError, ValueError, YamlSubsetError, json.JSONDecodeError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2
    parser.error(f"unknown command {args.command!r}")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
