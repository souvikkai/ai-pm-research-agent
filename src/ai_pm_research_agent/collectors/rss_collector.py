from __future__ import annotations

import logging
import xml.etree.ElementTree as ET
from datetime import datetime

from ai_pm_research_agent.collectors.base import Collector
from ai_pm_research_agent.storage.models import CandidateItem
from ai_pm_research_agent.utils.dates import days_ago, parse_date
from ai_pm_research_agent.utils.text import clean_html

LOGGER = logging.getLogger(__name__)


class RSSCollector(Collector):
    def __init__(self, feeds: list[dict], timeout_seconds: int = 20):
        self.feeds = feeds
        self.timeout_seconds = timeout_seconds

    def collect(self, lookback_days: int = 7) -> list[CandidateItem]:
        requests = _requests()
        cutoff = days_ago(lookback_days)
        items: list[CandidateItem] = []
        for feed in self.feeds:
            try:
                items.extend(self._collect_feed(feed, cutoff))
            except requests.RequestException as exc:
                LOGGER.warning("Failed to fetch RSS feed %s: %s", feed.get("name"), exc)
            except ET.ParseError as exc:
                LOGGER.warning("Failed to parse RSS feed %s: %s", feed.get("name"), exc)
        return items

    def _collect_feed(self, feed: dict, cutoff: datetime) -> list[CandidateItem]:
        requests = _requests()
        response = requests.get(feed["url"], timeout=self.timeout_seconds, headers={"User-Agent": "ai-pm-research-agent/0.1"})
        response.raise_for_status()
        root = ET.fromstring(response.content)
        entries = root.findall(".//item") or root.findall("{http://www.w3.org/2005/Atom}entry")
        normalized: list[CandidateItem] = []
        for entry in entries:
            item = self._parse_entry(entry, feed)
            if item.published_at and item.published_at < cutoff:
                continue
            normalized.append(item)
        return normalized

    def _parse_entry(self, entry: ET.Element, feed: dict) -> CandidateItem:
        atom = "{http://www.w3.org/2005/Atom}"
        title = _first_text(entry, ["title", f"{atom}title"]) or "Untitled"
        link = _first_text(entry, ["link", "guid"])
        atom_link = entry.find(f"{atom}link")
        if atom_link is not None:
            link = atom_link.attrib.get("href", link)
        published = _first_text(entry, ["pubDate", "published", "updated", f"{atom}published", f"{atom}updated"])
        author = _first_text(entry, ["author", "creator", f"{atom}author/{atom}name"])
        summary = _first_text(entry, ["description", "summary", "content", f"{atom}summary", f"{atom}content"])
        return CandidateItem(
            title=clean_html(title),
            source=feed["name"],
            author=clean_html(author),
            published_at=parse_date(published),
            url=link or feed["url"],
            category=feed.get("category", "rss"),
            raw_text=clean_html(summary),
            metadata={"feed_url": feed["url"]},
        )


def _first_text(entry: ET.Element, names: list[str]) -> str | None:
    for name in names:
        found = entry.find(name)
        if found is not None and found.text:
            return found.text
    return None


def _requests():
    import requests

    return requests
