#!/usr/bin/env python3
"""Deterministic structural parser and audit renderer for bootstrap anthologies."""

from __future__ import annotations

import dataclasses
import hashlib
import json
import re
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any, Dict, List, Optional, Sequence, Tuple
from urllib.parse import urlparse


H1_RE = re.compile(r"^# (.+)$")
H2_RE = re.compile(r"^## (.+)$")
H3_RE = re.compile(r"^### (.+)$")
LINK_RE = re.compile(r"\[(.+)\]\((https?://[^)]+)\)\s*$")
ZERO_WIDTH_RE = re.compile(r"[\u200b\u200c\u200d\u2060\ufeff]")


@dataclasses.dataclass(frozen=True)
class AuditIssue:
    code: str
    severity: str
    line: int
    entry_index: Optional[int]
    message: str

    def as_dict(self) -> Dict[str, Any]:
        return dataclasses.asdict(self)


@dataclasses.dataclass
class BootstrapEntry:
    index: int
    curated_h1: Optional[str]
    curated_h2: Optional[str]
    heading_raw: str
    source_title: str
    source_url: Optional[str]
    raw_line_start: int
    raw_line_end: int
    quote_line_start: Optional[int]
    quote_line_end: Optional[int]
    quote_text: Optional[str]
    issue_codes: List[str] = dataclasses.field(default_factory=list)

    @property
    def has_quote(self) -> bool:
        return self.quote_text is not None

    def audit_dict(self) -> Dict[str, Any]:
        """Return structural data only; the report does not duplicate quote bodies."""
        return {
            "index": self.index,
            "curated_path": [part for part in (self.curated_h1, self.curated_h2) if part],
            "heading_raw": self.heading_raw,
            "source_title": self.source_title,
            "source_url": self.source_url,
            "raw_line_start": self.raw_line_start,
            "raw_line_end": self.raw_line_end,
            "quote_line_start": self.quote_line_start,
            "quote_line_end": self.quote_line_end,
            "has_quote": self.has_quote,
            "issue_codes": sorted(self.issue_codes),
        }


@dataclasses.dataclass
class BootstrapAudit:
    raw_file: str
    raw_sha256: str
    line_count: int
    document_title: Optional[str]
    entries: List[BootstrapEntry]
    issues: List[AuditIssue]

    @property
    def quote_count(self) -> int:
        return sum(1 for entry in self.entries if entry.has_quote)

    @property
    def error_count(self) -> int:
        return sum(1 for issue in self.issues if issue.severity == "error")

    @property
    def warning_count(self) -> int:
        return sum(1 for issue in self.issues if issue.severity == "warning")

    @property
    def h1_values(self) -> List[str]:
        return list(dict.fromkeys(entry.curated_h1 for entry in self.entries if entry.curated_h1))

    @property
    def h2_paths(self) -> List[Tuple[str, str]]:
        return list(
            dict.fromkeys(
                (entry.curated_h1, entry.curated_h2)
                for entry in self.entries
                if entry.curated_h1 and entry.curated_h2
            )
        )

    def as_dict(self) -> Dict[str, Any]:
        url_stats = calculate_url_stats(self.entries)
        return {
            "schema_version": 1,
            "raw_file": self.raw_file,
            "raw_sha256": self.raw_sha256,
            "line_count": self.line_count,
            "document_title": self.document_title,
            "summary": {
                "h1_domains": len(self.h1_values),
                "h2_collections": len(self.h2_paths),
                "entries": len(self.entries),
                "quote_bodies": self.quote_count,
                "errors": self.error_count,
                "warnings": self.warning_count,
            },
            "url_diagnostics": url_stats,
            "issues": [issue.as_dict() for issue in self.issues],
            "entries": [entry.audit_dict() for entry in self.entries],
        }


def _clean_heading_text(value: str) -> str:
    return ZERO_WIDTH_RE.sub("", value).strip()


def _parse_source_heading(raw: str, line: int, entry_index: int) -> Tuple[str, Optional[str], List[AuditIssue]]:
    issues: List[AuditIssue] = []
    match = LINK_RE.search(raw)
    if not match:
        issues.append(
            AuditIssue(
                "heading.unparseable",
                "error",
                line,
                entry_index,
                "H3 heading does not contain a terminal HTTP(S) Markdown link",
            )
        )
        return _clean_heading_text(raw), None, issues

    prefix_raw = raw[: match.start()]
    prefix_clean = _clean_heading_text(prefix_raw)
    hidden_prefix = bool(prefix_raw) and not prefix_clean
    if prefix_clean or hidden_prefix:
        reason = "hidden Unicode before the link" if hidden_prefix else f"text before the link: {prefix_clean!r}"
        issues.append(
            AuditIssue(
                "heading.noncanonical",
                "warning",
                line,
                entry_index,
                f"H3 is recoverable but noncanonical ({reason})",
            )
        )
    label = _clean_heading_text(match.group(1))
    title = f"{prefix_clean}{label}" if prefix_clean else label
    url = match.group(2).strip()
    return title, url, issues


def calculate_url_stats(entries: Sequence[BootstrapEntry]) -> Dict[str, int]:
    stats = Counter()
    for entry in entries:
        if not entry.source_url:
            stats["missing_urls"] += 1
            continue
        parsed = urlparse(entry.source_url)
        host = (parsed.hostname or "").lower()
        if parsed.query:
            stats["query_urls"] += 1
        if "token=" in parsed.query.lower():
            stats["token_urls"] += 1
        if host in {"x.com", "www.x.com", "twitter.com", "www.twitter.com"}:
            stats["social_post_urls"] += 1
        if parsed.scheme == "http":
            stats["plain_http_urls"] += 1
        if not host or "." not in host:
            stats["suspicious_hosts"] += 1
    return dict(sorted(stats.items()))


def parse_anthology(path: Path, raw_file_label: Optional[str] = None) -> BootstrapAudit:
    data = path.read_bytes()
    text = data.decode("utf-8")
    lines = text.splitlines()
    issues: List[AuditIssue] = []
    entries: List[BootstrapEntry] = []
    document_title: Optional[str] = None
    current_h1: Optional[str] = None
    current_h2: Optional[str] = None
    current: Optional[Dict[str, Any]] = None

    def finish_entry(end_line: int) -> None:
        nonlocal current
        if current is None:
            return
        index = len(entries) + 1
        body_lines = [(number, value) for number, value in current["body"] if value.strip()]
        entry_issues: List[AuditIssue] = list(current["heading_issues"])
        quote_text: Optional[str] = None
        quote_start: Optional[int] = None
        quote_end: Optional[int] = None
        if not body_lines:
            entry_issues.append(
                AuditIssue(
                    "quote.missing",
                    "error",
                    current["line"],
                    index,
                    "entry has no curated quote body",
                )
            )
        else:
            quote_start = body_lines[0][0]
            quote_end = body_lines[-1][0]
            quote_text = "\n".join(
                value
                for number, value in current["body"]
                if quote_start <= number <= quote_end
            )
            if len(body_lines) > 1:
                entry_issues.append(
                    AuditIssue(
                        "quote.multiline",
                        "warning",
                        quote_start,
                        index,
                        f"quote body spans {len(body_lines)} nonblank lines",
                    )
                )
            stripped = quote_text.strip()
            if not (stripped.startswith("*") and stripped.endswith("*")):
                entry_issues.append(
                    AuditIssue(
                        "quote.noncanonical",
                        "warning",
                        quote_start,
                        index,
                        "quote body is not enclosed in Markdown emphasis",
                    )
                )
        if not current_h1 or not current_h2:
            entry_issues.append(
                AuditIssue(
                    "taxonomy.missing",
                    "error",
                    current["line"],
                    index,
                    "entry is missing an H1 or H2 editorial parent",
                )
            )
        url = current["url"]
        if url:
            parsed = urlparse(url)
            host = parsed.hostname or ""
            if not host or "." not in host:
                entry_issues.append(
                    AuditIssue(
                        "url.suspicious_host",
                        "warning",
                        current["line"],
                        index,
                        f"URL host appears incomplete: {host!r}",
                    )
                )
        entry = BootstrapEntry(
            index=index,
            curated_h1=current_h1,
            curated_h2=current_h2,
            heading_raw=current["heading_raw"],
            source_title=current["title"],
            source_url=url,
            raw_line_start=current["line"],
            raw_line_end=max(current["line"], end_line),
            quote_line_start=quote_start,
            quote_line_end=quote_end,
            quote_text=quote_text,
            issue_codes=[issue.code for issue in entry_issues],
        )
        entries.append(entry)
        issues.extend(entry_issues)
        current = None

    for line_number, line in enumerate(lines, 1):
        h1 = H1_RE.match(line)
        h2 = H2_RE.match(line)
        h3 = H3_RE.match(line)
        if h1 or h2 or h3:
            finish_entry(line_number - 1)
        if h1:
            heading = h1.group(1).strip()
            if document_title is None:
                document_title = heading
                current_h1 = None
            else:
                current_h1 = heading
            current_h2 = None
        elif h2:
            current_h2 = h2.group(1).strip()
        elif h3:
            index = len(entries) + 1
            raw_heading = h3.group(1).strip()
            title, url, heading_issues = _parse_source_heading(raw_heading, line_number, index)
            current = {
                "line": line_number,
                "heading_raw": raw_heading,
                "title": title,
                "url": url,
                "heading_issues": heading_issues,
                "body": [],
            }
        elif current is not None:
            current["body"].append((line_number, line))
    finish_entry(len(lines))

    # Confirm logical entry ranges are ordered and non-overlapping.
    previous_end = 0
    for entry in entries:
        if entry.raw_line_start <= previous_end:
            issue = AuditIssue(
                "range.overlap",
                "error",
                entry.raw_line_start,
                entry.index,
                "logical entry range overlaps its predecessor",
            )
            issues.append(issue)
            entry.issue_codes.append(issue.code)
        previous_end = entry.raw_line_end

    return BootstrapAudit(
        raw_file=raw_file_label or path.as_posix(),
        raw_sha256=hashlib.sha256(data).hexdigest(),
        line_count=len(lines),
        document_title=document_title,
        entries=entries,
        issues=sorted(issues, key=lambda issue: (issue.line, issue.code)),
    )


def render_json(audit: BootstrapAudit) -> str:
    return json.dumps(audit.as_dict(), indent=2, ensure_ascii=False, sort_keys=True) + "\n"


def render_markdown(audit: BootstrapAudit) -> str:
    summary = audit.as_dict()["summary"]
    url_stats = calculate_url_stats(audit.entries)
    section_counts: Dict[Tuple[str, str], int] = defaultdict(int)
    for entry in audit.entries:
        if entry.curated_h1 and entry.curated_h2:
            section_counts[(entry.curated_h1, entry.curated_h2)] += 1
    issue_counts = Counter(issue.code for issue in audit.issues)
    gate = "FAIL — review errors before Evidence generation" if audit.error_count else "PASS"
    lines = [
        "# Bootstrap Structural Audit",
        "",
        f"- Raw file: `{audit.raw_file}`",
        f"- SHA-256: `{audit.raw_sha256}`",
        f"- Source lines: {audit.line_count}",
        f"- Gate: **{gate}**",
        "",
        "## Summary",
        "",
        "| Measure | Count |",
        "|---|---:|",
        f"| H1 domains | {summary['h1_domains']} |",
        f"| H2 collections | {summary['h2_collections']} |",
        f"| H3 entries | {summary['entries']} |",
        f"| Quote bodies | {summary['quote_bodies']} |",
        f"| Errors | {summary['errors']} |",
        f"| Warnings | {summary['warnings']} |",
        "",
        "## Editorial collections",
        "",
        "| H1 | H2 | Entries |",
        "|---|---|---:|",
    ]
    for (h1, h2), count in section_counts.items():
        lines.append(f"| {h1} | {h2} | {count} |")
    lines.extend(["", "## Issue summary", ""])
    if issue_counts:
        lines.extend(["| Code | Count |", "|---|---:|"])
        for code, count in sorted(issue_counts.items()):
            lines.append(f"| `{code}` | {count} |")
    else:
        lines.append("_No structural issues._")
    lines.extend(["", "## Issue details", ""])
    if audit.issues:
        for issue in audit.issues:
            entry = f", entry {issue.entry_index}" if issue.entry_index else ""
            lines.append(
                f"- **{issue.severity.upper()} `{issue.code}`** — line {issue.line}{entry}: {issue.message}"
            )
    else:
        lines.append("_No structural issues._")
    lines.extend(["", "## URL diagnostics", ""])
    if url_stats:
        lines.extend(["| Diagnostic | Count |", "|---|---:|"])
        for key, count in url_stats.items():
            lines.append(f"| {key.replace('_', ' ').title()} | {count} |")
    else:
        lines.append("_No URL diagnostics._")
    lines.extend(
        [
            "",
            "## Next gate",
            "",
            "Review every error and decide whether to repair the raw source or register an explicit exception. Do not generate Evidence shells until the structural gate is accepted.",
            "",
        ]
    )
    return "\n".join(lines)
