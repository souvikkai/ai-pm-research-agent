from __future__ import annotations

from ai_pm_research_agent.storage.models import CandidateItem, ItemSummary, ScoreBreakdown
from ai_pm_research_agent.summarizers.item_summarizer import ItemSummarizer


class PaperSummarizer(ItemSummarizer):
    def summarize(self, item: CandidateItem, score: ScoreBreakdown) -> ItemSummary:
        summary = super().summarize(item, score)
        summary.domain_notes["paper_framework"] = (
            "PM read path: abstract first, conclusion second, figures and experiments third, method details only if needed."
        )
        summary.domain_notes["recommended_action"] = (
            "Read full paper"
            if score.weighted_score >= 1.8
            else "Skim"
            if score.weighted_score >= 1.45
            else "Skip"
        )
        return summary
