from ai_pm_research_agent.collectors.huggingface_papers_collector import HuggingFacePapersCollector
from ai_pm_research_agent.collectors.papers_with_code_collector import (
    PapersWithCodeCollector,
    _parse_hf_trending_html,
)
from ai_pm_research_agent.main import build_collectors


def test_huggingface_papers_collector_parses_daily_paper_entry():
    collector = HuggingFacePapersCollector()
    item = collector._parse_entry(
        {
            "paper": {
                "title": "Fast KV Cache Compression for LLM Serving",
                "arxivId": "2607.00001",
                "summary": "A method for reducing KV cache memory during inference.",
                "publishedAt": "2026-07-07T00:00:00Z",
                "authors": [{"name": "A. Researcher"}],
                "githubRepo": "https://github.com/example/repo",
            },
            "upvotes": 42,
        }
    )

    assert item is not None
    assert item.title == "Fast KV Cache Compression for LLM Serving"
    assert item.source == "Hugging Face Daily Papers"
    assert item.url == "https://huggingface.co/papers/2607.00001"
    assert item.metadata["github_repo"] == "https://github.com/example/repo"


def test_papers_with_code_collector_parses_api_entry():
    collector = PapersWithCodeCollector()
    item = collector._parse_api_entry(
        {
            "title": "TensorRT LLM Benchmark",
            "arxiv_id": "2607.00002",
            "abstract": "A benchmark for inference throughput.",
            "published": "2026-07-07",
            "authors": [{"name": "B. Builder"}],
            "repository_url": "https://github.com/example/benchmark",
        }
    )

    assert item is not None
    assert item.source == "Papers with Code"
    assert item.url == "https://arxiv.org/abs/2607.00002"
    assert item.metadata["repository_url"] == "https://github.com/example/benchmark"


def test_papers_with_code_trending_fallback_parser():
    html = """
    <h3><a href="/papers/2607.00003">Edge VLM Runtime</a></h3>
    <p>Optimizes vision-language model inference for embedded GPUs.</p>
    """

    items = _parse_hf_trending_html(html)

    assert len(items) == 1
    assert items[0].title == "Edge VLM Runtime"
    assert items[0].url == "https://huggingface.co/papers/2607.00003"


def test_build_collectors_includes_hf_and_pwc_collectors():
    collectors = build_collectors(
        {
            "arxiv": {"enabled": False},
            "huggingface_papers": {"enabled": True, "limit_per_day": 5},
            "papers_with_code": {"enabled": True, "max_results": 5},
            "rss_sources": {},
        }
    )

    names = [collector.__class__.__name__ for collector in collectors]
    assert "HuggingFacePapersCollector" in names
    assert "PapersWithCodeCollector" in names
