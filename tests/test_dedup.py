from ai_pm_research_agent.dedup import deduplicate_items
from ai_pm_research_agent.storage.models import CandidateItem


def test_deduplicate_items_removes_duplicate_urls_and_similar_titles():
    items = [
        CandidateItem(title="TensorRT-LLM improves LLM serving", source="A", url="https://x.com/a?utm_source=test", category="blog"),
        CandidateItem(title="TensorRT LLM improves LLM serving!", source="B", url="https://x.com/a", category="blog"),
        CandidateItem(title="New edge AI compiler support", source="C", url="https://x.com/b", category="blog"),
    ]

    unique = deduplicate_items(items)

    assert len(unique) == 2
    assert unique[0].title == "TensorRT-LLM improves LLM serving"
    assert unique[1].title == "New edge AI compiler support"
