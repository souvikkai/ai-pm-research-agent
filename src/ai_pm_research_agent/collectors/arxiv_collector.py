from __future__ import annotations

import logging
import urllib.parse
import xml.etree.ElementTree as ET

from ai_pm_research_agent.collectors.base import Collector
from ai_pm_research_agent.storage.models import CandidateItem
from ai_pm_research_agent.utils.dates import days_ago, parse_date
from ai_pm_research_agent.utils.text import clean_html, normalize_space

LOGGER = logging.getLogger(__name__)
ATOM = "{http://www.w3.org/2005/Atom}"


class ArxivCollector(Collector):
    def __init__(self, categories: list[str], query_terms: list[str], max_results_per_category: int = 25):
        self.categories = categories
        self.query_terms = query_terms
        self.max_results_per_category = max_results_per_category

    def collect(self, lookback_days: int = 7) -> list[CandidateItem]:
        requests = _requests()
        cutoff = days_ago(lookback_days)
        items: list[CandidateItem] = []
        for category in self.categories:
            term_query = " OR ".join(f'all:"{term}"' for term in self.query_terms)
            query = f"cat:{category} AND ({term_query})"
            params = {
                "search_query": query,
                "start": 0,
                "max_results": self.max_results_per_category,
                "sortBy": "submittedDate",
                "sortOrder": "descending",
            }
            url = "https://export.arxiv.org/api/query?" + urllib.parse.urlencode(params)
            try:
                response = requests.get(url, timeout=30, headers={"User-Agent": "ai-pm-research-agent/0.1"})
                response.raise_for_status()
                root = ET.fromstring(response.content)
            except (requests.RequestException, ET.ParseError) as exc:
                LOGGER.warning("Failed to fetch arXiv category %s: %s", category, exc)
                continue
            for entry in root.findall(f"{ATOM}entry"):
                item = self._parse_entry(entry, category)
                if item.published_at and item.published_at < cutoff:
                    continue
                items.append(item)
        return items

    def _parse_entry(self, entry: ET.Element, category: str) -> CandidateItem:
        title = normalize_space(_text(entry, f"{ATOM}title") or "Untitled")
        abstract = clean_html(_text(entry, f"{ATOM}summary"))
        published = parse_date(_text(entry, f"{ATOM}published"))
        authors = [
            normalize_space(name.text or "")
            for name in entry.findall(f"{ATOM}author/{ATOM}name")
            if name.text
        ]
        link = ""
        for link_elem in entry.findall(f"{ATOM}link"):
            if link_elem.attrib.get("rel") == "alternate":
                link = link_elem.attrib.get("href", "")
                break
        arxiv_id = (_text(entry, f"{ATOM}id") or link).rsplit("/", 1)[-1]
        return CandidateItem(
            title=title,
            source=f"arXiv {category}",
            author=", ".join(authors) if authors else None,
            published_at=published,
            url=link or f"https://arxiv.org/abs/{arxiv_id}",
            category="research_paper",
            abstract=abstract,
            metadata={"arxiv_id": arxiv_id, "category": category, "authors": authors},
        )


def _text(entry: ET.Element, name: str) -> str | None:
    found = entry.find(name)
    return found.text if found is not None else None


def _requests():
    import requests

    return requests
