from __future__ import annotations

import logging
import re
from typing import Any

from ai_pm_research_agent.collectors.base import Collector
from ai_pm_research_agent.storage.models import CandidateItem
from ai_pm_research_agent.utils.dates import days_ago, parse_date
from ai_pm_research_agent.utils.text import clean_html, normalize_space

LOGGER = logging.getLogger(__name__)


class PapersWithCodeCollector(Collector):
    def __init__(
        self,
        max_results: int = 30,
        api_url: str = "https://paperswithcode.com/api/v1/papers/",
        trending_url: str = "https://paperswithcode.com/trending",
        timeout_seconds: int = 30,
    ):
        self.max_results = max_results
        self.api_url = api_url
        self.trending_url = trending_url
        self.timeout_seconds = timeout_seconds

    def collect(self, lookback_days: int = 7) -> list[CandidateItem]:
        api_items = self._collect_api(lookback_days)
        if api_items:
            return api_items[: self.max_results]
        return self._collect_trending_page()[: self.max_results]

    def _collect_api(self, lookback_days: int) -> list[CandidateItem]:
        requests = _requests()
        try:
            response = requests.get(
                self.api_url,
                params={"page_size": self.max_results, "ordering": "-published"},
                headers={"User-Agent": "ai-pm-research-agent/0.1", "Accept": "application/json"},
                timeout=self.timeout_seconds,
            )
            response.raise_for_status()
            if "application/json" not in response.headers.get("Content-Type", ""):
                return []
            payload = response.json()
        except requests.RequestException as exc:
            LOGGER.warning("Failed to fetch Papers with Code API: %s", exc)
            return []
        entries = payload.get("results", payload if isinstance(payload, list) else [])
        cutoff = days_ago(lookback_days)
        items = [self._parse_api_entry(entry) for entry in entries]
        return [
            item
            for item in items
            if item and (not item.published_at or item.published_at >= cutoff)
        ]

    def _parse_api_entry(self, entry: dict[str, Any]) -> CandidateItem | None:
        title = entry.get("title")
        if not title:
            return None
        paper_url = entry.get("paper_url") or entry.get("url") or entry.get("arxiv_url")
        arxiv_id = entry.get("arxiv_id")
        url = paper_url or (f"https://arxiv.org/abs/{arxiv_id}" if arxiv_id else self.trending_url)
        metadata = {
            "source_family": "papers_with_code",
            "arxiv_id": arxiv_id,
            "repository_url": entry.get("repository_url"),
            "proceeding": entry.get("proceeding"),
            "tasks": entry.get("tasks"),
        }
        return CandidateItem(
            title=normalize_space(clean_html(title)),
            source="Papers with Code",
            author=_authors_to_string(entry.get("authors") or []),
            published_at=parse_date(entry.get("published") or entry.get("date")),
            url=url,
            category="research_paper",
            abstract=clean_html(entry.get("abstract") or ""),
            metadata={key: value for key, value in metadata.items() if value},
        )

    def _collect_trending_page(self) -> list[CandidateItem]:
        requests = _requests()
        try:
            response = requests.get(
                self.trending_url,
                headers={"User-Agent": "ai-pm-research-agent/0.1"},
                timeout=self.timeout_seconds,
            )
            response.raise_for_status()
        except requests.RequestException as exc:
            LOGGER.warning("Failed to fetch Papers with Code trending page: %s", exc)
            return []
        return _parse_hf_trending_html(response.text)


def _parse_hf_trending_html(html: str) -> list[CandidateItem]:
    items: list[CandidateItem] = []
    pattern = re.compile(
        r'<h3[^>]*>\s*<a[^>]+href="(?P<href>/papers/[^"]+)"[^>]*>(?P<title>.*?)</a>.*?'
        r'<p[^>]*>(?P<summary>.*?)</p>',
        re.IGNORECASE | re.DOTALL,
    )
    for match in pattern.finditer(html):
        href = match.group("href")
        title = clean_html(match.group("title"))
        summary = clean_html(match.group("summary"))
        if not title:
            continue
        items.append(
            CandidateItem(
                title=normalize_space(title),
                source="Papers with Code / HF Trending",
                url=f"https://huggingface.co{href}",
                category="research_paper",
                abstract=summary,
                metadata={"source_family": "papers_with_code", "fallback": "hf_trending_page"},
            )
        )
    return items


def _authors_to_string(authors: list[Any]) -> str | None:
    names = []
    for author in authors:
        if isinstance(author, str):
            names.append(author)
        elif isinstance(author, dict):
            names.append(author.get("name") or author.get("full_name") or "")
    return ", ".join(name for name in names if name) or None


def _requests():
    import requests

    return requests
