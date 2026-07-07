from __future__ import annotations

import logging

from ai_pm_research_agent.rankers.relevance_ranker import RelevanceRanker
from ai_pm_research_agent.storage.models import CandidateItem, RankedItem

LOGGER = logging.getLogger(__name__)


def select_ranked_items(
    items: list[CandidateItem], ranker: RelevanceRanker, scoring_config: dict
) -> list[RankedItem]:
    thresholds = scoring_config.get("thresholds", {})
    min_score = thresholds.get("include_min_score", 1.45)
    fallback_min_items = thresholds.get("fallback_min_items", 10)
    summarize_limit = thresholds.get("summarize_limit", 24)
    ranked = ranker.rank(items, min_score=min_score)
    if len(ranked) < fallback_min_items:
        LOGGER.warning(
            "Only %s items met the threshold %.2f; falling back to top %s scored items",
            len(ranked),
            min_score,
            fallback_min_items,
        )
        ranked = ranker.rank(items, min_score=0.0)[:fallback_min_items]
    return ranked[:summarize_limit]
