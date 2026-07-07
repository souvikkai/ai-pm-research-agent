from __future__ import annotations

from ai_pm_research_agent.storage.models import CandidateItem, RankedItem, ScoreBreakdown
from ai_pm_research_agent.utils.text import keyword_hits


class RelevanceRanker:
    def __init__(self, scoring_config: dict):
        self.weights: dict[str, float] = scoring_config["weights"]
        self.keyword_groups: dict[str, list[str]] = scoring_config["keyword_groups"]

    def score_item(self, item: CandidateItem) -> ScoreBreakdown:
        text = item.text_for_analysis
        dimensions: dict[str, int] = {}
        reasons: list[str] = []

        for dimension, keywords in self.keyword_groups.items():
            hits = keyword_hits(text, keywords)
            dimensions[dimension] = _hits_to_score(hits, item.category)
            if hits:
                reasons.append(f"{dimension}: {', '.join(hits[:5])}")

        weighted = sum(dimensions.get(name, 1) * weight for name, weight in self.weights.items())
        weighted = _apply_strategic_core_adjustment(weighted, dimensions)
        return ScoreBreakdown(dimensions=dimensions, weighted_score=round(weighted, 2), reasons=reasons)

    def rank(self, items: list[CandidateItem], min_score: float = 0.0) -> list[RankedItem]:
        ranked = [RankedItem(item=item, score=self.score_item(item)) for item in items]
        ranked = [entry for entry in ranked if entry.score.weighted_score >= min_score]
        return sorted(ranked, key=lambda entry: entry.score.weighted_score, reverse=True)


def _hits_to_score(hits: list[str], category: str) -> int:
    count = len(set(hit.lower() for hit in hits))
    if category == "research_paper" and count:
        count += 1
    if count >= 8:
        return 5
    if count >= 5:
        return 4
    if count >= 3:
        return 3
    if count >= 1:
        return 2
    return 1


def _apply_strategic_core_adjustment(weighted: float, dimensions: dict[str, int]) -> float:
    core_dimensions = [
        "ai_infrastructure_relevance",
        "compiler_runtime_quantization_relevance",
        "edge_automotive_industrial_relevance",
    ]
    core_max = max(dimensions.get(name, 1) for name in core_dimensions)
    if core_max < 3:
        return max(1.0, weighted - 0.4)
    if core_max >= 4:
        return min(5.0, weighted + 0.1)
    return weighted
