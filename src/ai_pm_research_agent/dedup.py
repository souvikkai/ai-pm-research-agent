from __future__ import annotations

from ai_pm_research_agent.storage.models import CandidateItem
from ai_pm_research_agent.utils.text import normalize_url, similarity, stable_fingerprint


def deduplicate_items(items: list[CandidateItem], title_similarity_threshold: float = 0.92) -> list[CandidateItem]:
    seen_fingerprints: set[str] = set()
    seen_urls: set[str] = set()
    unique: list[CandidateItem] = []

    for item in items:
        fingerprint = stable_fingerprint(item.title, item.url)
        url = normalize_url(item.url)
        if fingerprint in seen_fingerprints or url in seen_urls:
            continue
        if any(similarity(item.title, existing.title) >= title_similarity_threshold for existing in unique):
            continue
        seen_fingerprints.add(fingerprint)
        seen_urls.add(url)
        unique.append(item)
    return unique
