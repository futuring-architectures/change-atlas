#!/usr/bin/env python3
"""URL-first capture and Evidence drafting for steady-state ingestion."""

from __future__ import annotations

import dataclasses
import datetime as dt
import hashlib
import html
import json
import re
import urllib.error
import urllib.parse
import urllib.request
from html.parser import HTMLParser
from pathlib import Path
from typing import Dict, Iterable, List, Optional, Tuple


MAX_RESPONSE_BYTES = 8 * 1024 * 1024
BLOCK_TAGS = {
    "address", "article", "aside", "blockquote", "br", "dd", "div", "dl",
    "dt", "figcaption", "figure", "footer", "h1", "h2", "h3", "h4", "h5",
    "h6", "header", "hr", "li", "main", "nav", "ol", "p", "pre", "section",
    "table", "td", "th", "tr", "ul",
}
SKIP_TAGS = {"canvas", "noscript", "script", "style", "svg", "template"}
VOID_TAGS = {"area", "base", "br", "col", "embed", "hr", "img", "input", "link", "meta", "param", "source", "track", "wbr"}


@dataclasses.dataclass(frozen=True)
class CapturedArticle:
    requested_url: str
    final_url: str
    canonical_url: str
    title: str
    author: Optional[str]
    publisher: Optional[str]
    published_at: Optional[str]
    date_precision: str
    body: str


@dataclasses.dataclass(frozen=True)
class CaptureDraft:
    raw_relative: str
    raw_content: str
    evidence_relative: str
    evidence_content: str
    evidence_id: str
    raw_sha256: str


class ArticleHTMLParser(HTMLParser):
    """Conservative dependency-free extraction of source metadata and readable text."""

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.title_parts: List[str] = []
        self.in_title = False
        self.skip_depth = 0
        self.article_depth = 0
        self.saw_article = False
        self.all_parts: List[str] = []
        self.article_parts: List[str] = []
        self.meta: Dict[str, str] = {}
        self.canonical_url: Optional[str] = None

    def handle_starttag(self, tag: str, attrs: List[Tuple[str, Optional[str]]]) -> None:
        tag = tag.lower()
        values = {key.lower(): value for key, value in attrs if value is not None}
        if tag in SKIP_TAGS:
            self.skip_depth += 1
            return
        if self.skip_depth:
            return
        if tag == "title":
            self.in_title = True
        if tag == "article":
            self.saw_article = True
            self.article_depth += 1
        elif self.article_depth and tag not in VOID_TAGS:
            self.article_depth += 1
        if tag == "meta":
            key = (values.get("property") or values.get("name") or "").lower()
            content = values.get("content")
            if key and content and key not in self.meta:
                self.meta[key] = content.strip()
        if tag == "link" and "canonical" in values.get("rel", "").lower().split():
            self.canonical_url = values.get("href")
        if tag in BLOCK_TAGS:
            self._append_break()

    def handle_startendtag(self, tag: str, attrs: List[Tuple[str, Optional[str]]]) -> None:
        self.handle_starttag(tag, attrs)
        if tag.lower() not in VOID_TAGS:
            self.handle_endtag(tag)

    def handle_endtag(self, tag: str) -> None:
        tag = tag.lower()
        if tag in SKIP_TAGS:
            self.skip_depth = max(0, self.skip_depth - 1)
            return
        if self.skip_depth:
            return
        if tag == "title":
            self.in_title = False
        if tag in BLOCK_TAGS:
            self._append_break()
        if self.article_depth and tag not in VOID_TAGS:
            self.article_depth -= 1

    def handle_data(self, data: str) -> None:
        if self.skip_depth:
            return
        value = re.sub(r"\s+", " ", data)
        if not value.strip():
            return
        if self.in_title:
            self.title_parts.append(value.strip())
        self.all_parts.append(value)
        if self.article_depth:
            self.article_parts.append(value)

    def _append_break(self) -> None:
        self.all_parts.append("\n")
        if self.article_depth:
            self.article_parts.append("\n")

    def text(self) -> str:
        selected = self.article_parts if self.saw_article and self.article_parts else self.all_parts
        joined = "".join(selected)
        lines = [re.sub(r"[ \t]+", " ", line).strip() for line in joined.splitlines()]
        output: List[str] = []
        for line in lines:
            if line and (not output or line != output[-1]):
                output.append(line)
        return "\n\n".join(output).strip()


def normalize_url(value: str) -> str:
    parsed = urllib.parse.urlsplit(value.strip())
    if parsed.scheme not in {"http", "https"} or not parsed.netloc:
        raise ValueError("ingest URL must be an absolute HTTP(S) URL")
    return urllib.parse.urlunsplit((parsed.scheme.lower(), parsed.netloc.lower(), parsed.path or "/", parsed.query, ""))


def _first(mapping: Dict[str, str], keys: Iterable[str]) -> Optional[str]:
    for key in keys:
        value = mapping.get(key)
        if value:
            return html.unescape(value).strip()
    return None


def _publication_date(value: Optional[str]) -> Tuple[Optional[str], str]:
    if not value:
        return None, "unknown"
    candidate = value.strip()
    match = re.match(r"^(\d{4})-(\d{2})-(\d{2})", candidate)
    if match:
        normalized = "-".join(match.groups())
        try:
            dt.date.fromisoformat(normalized)
            return normalized, "day"
        except ValueError:
            pass
    match = re.match(r"^(\d{4})-(\d{2})(?:\D|$)", candidate)
    if match:
        normalized = "-".join(match.groups())
        try:
            dt.date.fromisoformat(normalized + "-01")
            return normalized, "month"
        except ValueError:
            pass
    match = re.match(r"^(\d{4})(?:\D|$)", candidate)
    if match:
        return match.group(1), "year"
    return None, "unknown"


def fetch_article(url: str, timeout: int = 30) -> CapturedArticle:
    requested = normalize_url(url)
    request = urllib.request.Request(
        requested,
        headers={
            "User-Agent": "Change-Atlas/1.0 (+personal research capture)",
            "Accept": "text/html,application/xhtml+xml;q=0.9,text/plain;q=0.8",
        },
    )
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            content_type = response.headers.get_content_type()
            if content_type not in {"text/html", "application/xhtml+xml", "text/plain"}:
                raise ValueError(f"unsupported URL content type: {content_type}")
            payload = response.read(MAX_RESPONSE_BYTES + 1)
            if len(payload) > MAX_RESPONSE_BYTES:
                raise ValueError("source response exceeds the 8 MiB capture limit")
            charset = response.headers.get_content_charset() or "utf-8"
            try:
                source = payload.decode(charset)
            except (LookupError, UnicodeDecodeError):
                source = payload.decode("utf-8", errors="replace")
            final_url = normalize_url(response.geturl())
    except urllib.error.HTTPError as exc:
        raise ValueError(f"source returned HTTP {exc.code}") from exc
    except urllib.error.URLError as exc:
        raise ValueError(f"source could not be fetched: {exc.reason}") from exc

    if content_type == "text/plain":
        title = urllib.parse.unquote(Path(urllib.parse.urlsplit(final_url).path).name) or final_url
        return CapturedArticle(requested, final_url, final_url, title, None, None, None, "unknown", source.strip())

    parser = ArticleHTMLParser()
    parser.feed(source)
    canonical = normalize_url(urllib.parse.urljoin(final_url, parser.canonical_url)) if parser.canonical_url else final_url
    title = _first(parser.meta, ("og:title", "twitter:title")) or " ".join(parser.title_parts).strip()
    if not title:
        raise ValueError("source page has no recoverable title")
    body = parser.text()
    if len(body.split()) < 20:
        raise ValueError("source page yielded too little readable text; it may require login or client-side rendering")
    author = _first(parser.meta, ("author", "article:author", "parsely-author", "byl"))
    publisher = _first(parser.meta, ("og:site_name", "application-name"))
    published_raw = _first(
        parser.meta,
        ("article:published_time", "date", "datepublished", "parsely-pub-date", "sailthru.date"),
    )
    published_at, precision = _publication_date(published_raw)
    return CapturedArticle(
        requested, final_url, canonical, html.unescape(title), author, publisher,
        published_at, precision, body,
    )


def slugify(value: str) -> str:
    normalized = value.lower().replace("’", "").replace("'", "")
    slug = re.sub(r"[^a-z0-9]+", "-", normalized).strip("-")
    return slug[:80].rstrip("-") or "source"


def _quoted(value: Optional[str]) -> str:
    return "null" if value is None else json.dumps(value, ensure_ascii=False)


def _blockquote(value: str) -> str:
    return "\n".join(">" if not line else f"> {line}" for line in value.splitlines())


def build_capture_draft(article: CapturedArticle, ingest_date: str, quote: Optional[str] = None) -> CaptureDraft:
    dt.date.fromisoformat(ingest_date)
    pin = quote.strip() if quote and quote.strip() else None
    raw_lines = [
        f"# {article.title}",
        "",
        "## Capture metadata",
        "",
        f"- Requested URL: <{article.requested_url}>",
        f"- Final URL: <{article.final_url}>",
        f"- Canonical URL: <{article.canonical_url}>",
        f"- Captured on: {ingest_date}",
        "",
        "## Captured article",
        "",
    ]
    raw_lines.extend(article.body.splitlines())
    quote_start: Optional[int] = None
    quote_end: Optional[int] = None
    if pin:
        raw_lines.extend(["", "## Curator pin", ""])
        quote_start = len(raw_lines) + 1
        raw_lines.extend(pin.splitlines())
        quote_end = len(raw_lines)
    raw_content = "\n".join(raw_lines).rstrip() + "\n"
    raw_hash = hashlib.sha256(raw_content.encode("utf-8")).hexdigest()
    identity = article.canonical_url.encode("utf-8")
    evidence_id = f"evi-{hashlib.sha256(identity).hexdigest()[:12]}"
    stem = slugify(article.title)
    raw_relative = f"raw/web/{ingest_date}-{stem}.md"
    evidence_relative = f"evidence/sources/{stem}-{evidence_id}.md"
    raw_line_end = len(raw_content.splitlines())

    metadata_recovered = any((article.author, article.publisher, article.published_at))
    date_status = "verified" if article.published_at else "unresolved"
    evidence_lines = [
        "---",
        f"id: {evidence_id}",
        "type: evidence",
        f"title: {_quoted(article.title)}",
        "status: draft",
        f"created_at: {ingest_date}",
        f"updated_at: {ingest_date}",
        "tags: []",
        "relationships: []",
        f"raw_file: {_quoted(raw_relative)}",
        f"raw_sha256: {_quoted(raw_hash)}",
        "raw_entry_index: 1",
        "raw_line_start: 1",
        f"raw_line_end: {raw_line_end}",
    ]
    if quote_start is not None and quote_end is not None:
        evidence_lines.extend((f"raw_quote_line_start: {quote_start}", f"raw_quote_line_end: {quote_end}"))
    evidence_lines.extend([
        f"ingested_at: {ingest_date}",
        f"source_title: {_quoted(article.title)}",
        f"source_url: {_quoted(article.requested_url)}",
        f"canonical_url: {_quoted(article.canonical_url)}",
        "canonical_url_status: verified",
        f"author: {_quoted(article.author)}",
        f"author_status: {'verified' if article.author else 'unresolved'}",
        f"publisher: {_quoted(article.publisher)}",
        f"publisher_status: {'verified' if article.publisher else 'unresolved'}",
        f"published_at: {_quoted(article.published_at)}",
        f"date_status: {date_status}",
        f"date_source: {'source_page_metadata' if article.published_at else 'null'}",
        f"date_precision: {article.date_precision}",
        f"metadata_checked_at: {ingest_date if metadata_recovered or article.canonical_url else 'null'}",
        "curated_path: []",
        "collection_position: null",
        "global_position: null",
        "claim_extraction_status: pending",
        f"curator_pin_status: {'user_supplied' if pin else 'not_supplied'}",
        "---",
        "",
        f"# {article.title}",
        "",
        "## Source metadata",
        "",
        f"- Raw file: `{raw_relative}`",
        f"- Raw SHA-256: `{raw_hash}`",
        f"- Raw entry and lines: entry 1, lines 1–{raw_line_end}",
        f"- Original URL: <{article.requested_url}>",
        f"- Canonical URL: <{article.canonical_url}>",
        f"- Author: {article.author or 'Unresolved'}",
        f"- Publisher: {article.publisher or 'Unresolved'}",
        f"- Publication date: {article.published_at or 'Unresolved'}",
        f"- Captured: {ingest_date}",
        "",
        "## Curated excerpt",
        "",
    ])
    evidence_lines.extend(_blockquote(pin).splitlines() if pin else ["_No curator pin supplied._"])
    evidence_lines.extend([
        "",
        "## Atomic claims",
        "",
        "_Pending interpretive extraction from the complete captured article. Draft Evidence must not be cited by Wiki pages._",
        "",
        "## Relationships",
        "",
        "_No relationships recorded._",
        "",
    ])
    return CaptureDraft(
        raw_relative, raw_content, evidence_relative, "\n".join(evidence_lines),
        evidence_id, raw_hash,
    )


def write_capture_draft(root: Path, draft: CaptureDraft) -> Tuple[Path, Path]:
    raw_path = root / draft.raw_relative
    evidence_path = root / draft.evidence_relative
    for path in (raw_path, evidence_path):
        if path.exists():
            raise ValueError(f"refusing to overwrite existing ingest artifact: {path.relative_to(root)}")
    raw_path.parent.mkdir(parents=True, exist_ok=True)
    evidence_path.parent.mkdir(parents=True, exist_ok=True)
    raw_path.write_text(draft.raw_content, encoding="utf-8")
    try:
        evidence_path.write_text(draft.evidence_content, encoding="utf-8")
    except Exception:
        raw_path.unlink()
        raise
    return raw_path, evidence_path
