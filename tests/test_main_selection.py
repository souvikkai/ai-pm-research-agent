from ai_pm_research_agent.rankers.relevance_ranker import RelevanceRanker
from ai_pm_research_agent.rankers.selection import select_ranked_items
from ai_pm_research_agent.storage.models import CandidateItem


def test_select_ranked_items_falls_back_when_threshold_is_too_strict():
    config = {
        "weights": {
            "ai_pm_relevance": 0.5,
            "ai_infrastructure_relevance": 0.5,
        },
        "keyword_groups": {
            "ai_pm_relevance": ["roadmap"],
            "ai_infrastructure_relevance": ["inference"],
        },
        "thresholds": {
            "include_min_score": 4.9,
            "fallback_min_items": 2,
            "summarize_limit": 3,
        },
    }
    items = [
        CandidateItem(title="Inference roadmap", source="A", url="https://a.example", category="blog"),
        CandidateItem(title="General AI update", source="B", url="https://b.example", category="blog"),
    ]

    ranked = select_ranked_items(items, RelevanceRanker(config), config)

    assert len(ranked) == 2
    assert ranked[0].item.title == "Inference roadmap"
