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
import sys
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Sequence, Tuple


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
    "wiki/debates",
    "wiki/questions",
    "system/templates",
    "system/lint-reports",
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
    "system/index.md",
    "system/log.md",
    "evidence/index.md",
    "tools/wiki",
)
WIKILINK_RE = re.compile(r"\[\[([^\]]+)\]\]")
ANCHOR_RE = re.compile(r'<a\s+(?:id|name)=["\']([^"\']+)["\']\s*></a>', re.I)
ID_RE = re.compile(r"^[a-z]{3}-[a-z0-9]{6,}$")
SLUG_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
ISO_DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")


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


def parse_markdown(path: Path) -> Tuple[Optional[Page], List[Issue]]:
    issues: List[Issue] = []
    try:
        text = path.read_text(encoding="utf-8")
    except (OSError, UnicodeError) as exc:
        return None, [Issue("file.read", path, str(exc))]
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
    anchors = ANCHOR_RE.findall(body)
    links = WIKILINK_RE.findall(body)
    return Page(path, metadata, body, anchors, links), issues


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
    raw_cache: Dict[Path, Tuple[str, int]],
) -> List[Issue]:
    """Validate the immutable raw-file chain for one Evidence page."""
    issues: List[Issue] = []
    metadata = page.metadata
    raw_value = metadata.get("raw_file")
    raw_path: Optional[Path] = None
    raw_info: Optional[Tuple[str, int]] = None

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
                line_count = len(data.decode("utf-8").splitlines())
            except UnicodeDecodeError:
                issues.append(Issue("raw.encoding", page.path, "raw Markdown must be UTF-8"))
                line_count = 0
            raw_cache[raw_path] = (hashlib.sha256(data).hexdigest(), line_count)
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
    elif raw_info is not None and line_end > raw_info[1]:
        issues.append(
            Issue(
                "raw.range_invalid",
                page.path,
                f"raw_line_end {line_end} exceeds the raw file's {raw_info[1]} lines",
            )
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
    raw_cache: Dict[Path, Tuple[str, int]] = {}

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
    order = ["hub", "signal", "trend", "concept", "framework", "debate", "question", "evidence"]
    labels = {
        "hub": "Hubs",
        "signal": "Signals",
        "trend": "Trends",
        "concept": "Concepts",
        "framework": "Frameworks",
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
        for page in sorted(evidence, key=lambda item: (item.title.lower(), item.stem)):
            lines.append(f"- {_relative_wikilink(page, root)}")
        lines.append("")
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
    raw_files = _managed_raw_files(root)
    try:
        manifest = json.loads((root / "system/manifest.json").read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        manifest = {"files": {}}
    manifest_files = manifest.get("files", {}) if isinstance(manifest, dict) else {}
    raw_names = [path.relative_to(root).as_posix() for path in raw_files]
    processed = [name for name in raw_names if name in manifest_files]
    counts = Counter(page.page_type for page in pages)
    data = {
        "raw_files": len(raw_files),
        "processed_raw_files": len(processed),
        "unprocessed_raw_files": len(raw_files) - len(processed),
        "evidence_pages": counts.get("evidence", 0),
        "wiki_pages": sum(count for page_type, count in counts.items() if page_type != "evidence"),
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
    if schema is not None:
        _, issues = validate_content(root, schema)
        checks.append((not issues, f"repository content validates ({len(issues)} issue(s))"))
    for passed, label in checks:
        print(f"[{'ok' if passed else 'FAIL'}] {label}")
    failures = sum(1 for passed, _ in checks if not passed)
    print(f"Doctor {'passed' if not failures else 'failed'}: {failures} failure(s).")
    return 1 if failures else 0


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
    except (OSError, YamlSubsetError, json.JSONDecodeError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2
    parser.error(f"unknown command {args.command!r}")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
