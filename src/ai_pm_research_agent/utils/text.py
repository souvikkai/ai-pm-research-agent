from __future__ import annotations

import hashlib
import html
import re
from difflib import SequenceMatcher
from urllib.parse import parse_qsl, urlencode, urlsplit, urlunsplit


TAG_RE = re.compile(r"<[^>]+>")
SPACE_RE = re.compile(r"\s+")
PUNCT_RE = re.compile(r"[^a-z0-9\s]")


def clean_html(value: str | None) -> str:
    if not value:
        return ""
    text = TAG_RE.sub(" ", value)
    return normalize_space(html.unescape(text))


def normalize_space(value: str) -> str:
    return SPACE_RE.sub(" ", value).strip()


def normalize_title(value: str) -> str:
    text = PUNCT_RE.sub(" ", value.lower())
    return normalize_space(text)


def normalize_url(url: str) -> str:
    parts = urlsplit(url.strip())
    query = [(k, v) for k, v in parse_qsl(parts.query) if not k.lower().startswith("utm_")]
    return urlunsplit((parts.scheme, parts.netloc.lower(), parts.path.rstrip("/"), urlencode(query), ""))


def stable_fingerprint(title: str, url: str) -> str:
    normalized = f"{normalize_title(title)}|{normalize_url(url)}"
    return hashlib.sha256(normalized.encode("utf-8")).hexdigest()


def similarity(left: str, right: str) -> float:
    return SequenceMatcher(None, normalize_title(left), normalize_title(right)).ratio()


def excerpt(text: str | None, max_chars: int = 280) -> str:
    clean = normalize_space(clean_html(text))
    if len(clean) <= max_chars:
        return clean
    return clean[: max_chars - 1].rstrip() + "..."


def keyword_hits(text: str, keywords: list[str]) -> list[str]:
    lower = text.lower()
    hits: list[str] = []
    for keyword in keywords:
        normalized = keyword.lower()
        if _keyword_matches(lower, normalized):
            hits.append(keyword)
    return hits


def _keyword_matches(text: str, keyword: str) -> bool:
    if not keyword:
        return False
    if re.search(r"\w", keyword):
        pattern = rf"(?<![a-z0-9]){re.escape(keyword)}(?![a-z0-9])"
        return re.search(pattern, text) is not None
    return keyword in text
