from __future__ import annotations

import logging
import os
from datetime import timedelta
from typing import Any

from ai_pm_research_agent.collectors.base import Collector
from ai_pm_research_agent.storage.models import CandidateItem
from ai_pm_research_agent.utils.dates import local_now, parse_date
from ai_pm_research_agent.utils.text import clean_html, normalize_space

LOGGER = logging.getLogger(__name__)


class HuggingFacePapersCollector(Collector):
    def __init__(
        self,
        limit_per_day: int = 20,
        sort: str = "trending",
        base_url: str = "https://huggingface.co",
        timeout_seconds: int = 30,
    ):
        self.limit_per_day = limit_per_day
        self.sort = sort
        self.base_url = base_url.rstrip("/")
        self.timeout_seconds = timeout_seconds

    def collect(self, lookback_days: int = 7) -> list[CandidateItem]:
        requests = _requests()
        items: list[CandidateItem] = []
        today = local_now().date()
        for offset in range(lookback_days):
            date = today - timedelta(days=offset)
            try:
                response = requests.get(
                    f"{self.base_url}/api/daily_papers",
                    params={
                        "p": 0,
                        "limit": self.limit_per_day,
                        "date": date.isoformat(),
                        "sort": self.sort,
                    },
                    headers=self._headers(),
                    timeout=self.timeout_seconds,
                )
                response.raise_for_status()
            except requests.RequestException as exc:
                LOGGER.warning("Failed to fetch Hugging Face daily papers for %s: %s", date, exc)
                continue
            payload = response.json()
            entries = payload if isinstance(payload, list) else payload.get("dailyPapers", [])
            for entry in entries:
                item = self._parse_entry(entry)
                if item:
                    items.append(item)
        return items

    def _parse_entry(self, entry: dict[str, Any]) -> CandidateItem | None:
        paper = entry.get("paper") if isinstance(entry.get("paper"), dict) else entry
        title = paper.get("title") or entry.get("title")
        if not title:
            return None
        arxiv_id = (
            paper.get("arxivId")
            or paper.get("paperId")
            or paper.get("id")
            or entry.get("paperId")
            or entry.get("arxivId")
        )
        url = paper.get("url") or entry.get("url")
        if not url:
            url = f"https://huggingface.co/papers/{arxiv_id}" if arxiv_id else self.base_url

        authors = _authors_to_string(paper.get("authors") or entry.get("authors") or [])
        summary = (
            paper.get("summary")
            or paper.get("abstract")
            or paper.get("ai_summary")
            or entry.get("summary")
            or entry.get("description")
            or ""
        )
        published = (
            paper.get("publishedAt")
            or paper.get("published_at")
            or entry.get("publishedAt")
            or entry.get("createdAt")
            or entry.get("date")
        )
        metadata = {
            "source_family": "huggingface_papers",
            "arxiv_id": arxiv_id,
            "upvotes": entry.get("upvotes") or paper.get("upvotes"),
            "github_repo": paper.get("githubRepo") or entry.get("githubRepo"),
            "project_page": paper.get("projectPage") or entry.get("projectPage"),
            "submitted_by": _submitter_name(entry.get("submittedBy") or entry.get("submitter")),
        }
        return CandidateItem(
            title=normalize_space(clean_html(title)),
            source="Hugging Face Daily Papers",
            author=authors or None,
            published_at=parse_date(published),
            url=url,
            category="research_paper",
            abstract=clean_html(summary),
            metadata={key: value for key, value in metadata.items() if value},
        )

    def _headers(self) -> dict[str, str]:
        headers = {"User-Agent": "ai-pm-research-agent/0.1"}
        token = os.getenv("HF_TOKEN") or os.getenv("HUGGINGFACE_TOKEN")
        if token:
            headers["Authorization"] = f"Bearer {token}"
        return headers


def _authors_to_string(authors: list[Any]) -> str:
    names = []
    for author in authors:
        if isinstance(author, str):
            names.append(author)
        elif isinstance(author, dict):
            names.append(author.get("name") or author.get("fullname") or author.get("user") or "")
    return ", ".join(name for name in names if name)


def _submitter_name(submitter: Any) -> str | None:
    if isinstance(submitter, str):
        return submitter
    if isinstance(submitter, dict):
        return submitter.get("name") or submitter.get("fullname") or submitter.get("username")
    return None


def _requests():
    import requests

    return requests
