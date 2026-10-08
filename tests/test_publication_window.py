from datetime import UTC, datetime, timedelta
from types import SimpleNamespace

import pytest

from ai_pm_research_agent import main
from ai_pm_research_agent.collectors.arxiv_collector import ArxivCollector
from ai_pm_research_agent.collectors.huggingface_papers_collector import HuggingFacePapersCollector
from ai_pm_research_agent.collectors.papers_with_code_collector import PapersWithCodeCollector
from ai_pm_research_agent.storage.db import ItemStore
from ai_pm_research_agent.storage.models import CandidateItem
from ai_pm_research_agent.summarizers.llm_report_synthesizer import LLMReportSynthesizer
from ai_pm_research_agent.utils.dates import publication_in_window

NOW = datetime(2026, 10, 2, 15, tzinfo=UTC)
CUTOFF = NOW - timedelta(days=7)


def hf_entry(title, published=None, **community):
    return {"paper": {"title": title, "id": "2504.19413", "publishedAt": published}, **community}


@pytest.mark.parametrize("value,eligible", [
    (CUTOFF, True), (NOW, True),
    (CUTOFF - timedelta(microseconds=1), False),
    (NOW + timedelta(microseconds=1), False),
    ("2026-09-25T08:00:00-07:00", True),
    ("2026-10-02T17:00:00+02:00", True),
    ("2026-09-25T07:59:59.999999-07:00", False),
    (None, False), ("garbage", False), ("2026-10", False),
    ("2026-02-30T12:00:00Z", False), ("2025-04-28T00:00:00Z", False),
])
def test_inclusive_publication_window(value, eligible):
    assert publication_in_window(value, CUTOFF, NOW) is eligible


@pytest.mark.parametrize("community", [
    {"publishedAt": NOW.isoformat()}, {"createdAt": NOW.isoformat()},
    {"updatedAt": NOW.isoformat()}, {"date": NOW.isoformat()},
])
def test_hf_community_only_dates_are_not_publication_dates(community):
    item = HuggingFacePapersCollector()._parse_entry(hf_entry("Undated", **community))
    assert item.published_at is None
    assert item.metadata["community_dates"] == community


def test_hf_flat_entry_timestamp_is_not_assumed_to_be_publication():
    item = HuggingFacePapersCollector()._parse_entry({
        "title": "Community-only flat entry", "id": "2504.19413",
        "publishedAt": NOW.isoformat(),
    })
    assert item.published_at is None


def test_arxiv_original_publication_not_update_controls_window(monkeypatch):
    content = '''<feed xmlns="http://www.w3.org/2005/Atom">
        <entry><title>Mem0</title><id>https://arxiv.org/abs/2504.19413</id>
        <published>2025-04-28T00:00:00Z</published><updated>2026-10-02T15:00:00Z</updated></entry>
        <entry><title>Cutoff</title><published>2026-09-25T15:00:00Z</published></entry>
        <entry><title>Now</title><published>2026-10-02T15:00:00Z</published></entry>
        <entry><title>Undated</title><id>https://arxiv.org/abs/2610.00001</id></entry>
        </feed>'''
    response = SimpleNamespace(raise_for_status=lambda: None, content=content.encode())
    monkeypatch.setattr("requests.get", lambda *args, **kwargs: response)
    items = ArxivCollector(["cs.AI"], ["serving"]).collect(7, now=NOW)
    assert [item.title for item in items] == ["Cutoff", "Now"]


def test_hf_recent_daily_lists_exclude_old_originals(monkeypatch):
    payload = [
        hf_entry("Mem0", "2025-04-28T00:00:00Z", publishedAt=NOW.isoformat()),
        hf_entry("Old updated paper", "2025-04-28T00:00:00Z",
                 createdAt=NOW.isoformat(), updatedAt=NOW.isoformat()),
        hf_entry("Community only", createdAt=NOW.isoformat()),
        hf_entry("Malformed", "invalid"),
        hf_entry("Future", (NOW + timedelta(seconds=1)).isoformat()),
        hf_entry("Fresh", NOW.isoformat()),
    ]
    response = SimpleNamespace(raise_for_status=lambda: None, json=lambda: payload)
    calls = []

    def get(url, **kwargs):
        calls.append(kwargs["params"]["date"])
        return response

    monkeypatch.setattr("requests.get", get)
    items = HuggingFacePapersCollector().collect(7, now=NOW)
    assert len(calls) == 7
    assert {item.title for item in items} == {"Fresh"}


def test_pwc_undated_trending_fallback_is_excluded(monkeypatch):
    response = SimpleNamespace(
        raise_for_status=lambda: None, headers={"Content-Type": "text/html"},
        text='<h3><a href="/papers/2504.19413">Mem0</a></h3><p>Memory</p>',
    )
    monkeypatch.setattr("requests.get", lambda *args, **kwargs: response)
    assert PapersWithCodeCollector().collect(7, now=NOW) == []


def test_pwc_api_requires_original_publication(monkeypatch):
    response = SimpleNamespace(
        raise_for_status=lambda: None, headers={"Content-Type": "application/json"},
        json=lambda: {"results": [
            {"title": "Fresh", "published": NOW.isoformat()},
            {"title": "Old", "published": "2025-04-28", "date": NOW.isoformat()},
            {"title": "Community only", "date": NOW.isoformat()},
            {"title": "Malformed", "published": "bad"},
            {"title": "Future", "published": (NOW + timedelta(seconds=1)).isoformat()},
        ]},
    )
    monkeypatch.setattr("requests.get", lambda *args, **kwargs: response)
    assert [item.title for item in PapersWithCodeCollector().collect(7, now=NOW)] == ["Fresh"]


def test_mocked_run_filters_before_storage_and_fallback_with_existing_mem0(tmp_path, monkeypatch):
    def paper(title, date):
        return CandidateItem(title=title, source="Mock", url=f"https://example.com/{title}",
                             category="research_paper", published_at=date, abstract="Inference")

    old = paper("Mem0", datetime(2025, 4, 28, tzinfo=UTC))
    fresh = paper("Fresh serving", NOW)
    boundary = paper("Cutoff paper", CUTOFF)
    invalid = [old, paper("Unknown", None), paper("Malformed", "bad"),
               paper("Future", NOW + timedelta(microseconds=1)),
               paper("Too old", CUTOFF - timedelta(microseconds=1))]
    blog = CandidateItem(title="Undated blog", source="Mock", url="https://example.com/blog", category="blog")
    db_path = tmp_path / "items.db"
    store = ItemStore(db_path)
    store.upsert_items([old])
    store.close()

    class MockCollector(HuggingFacePapersCollector):
        def collect(self, lookback_days, now=None):
            assert lookback_days == 7
            assert now is NOW
            return invalid + [fresh, boundary, blog]

    clock_calls = []

    def clock():
        clock_calls.append(True)
        return NOW

    monkeypatch.setattr(main, "utc_now", clock)
    monkeypatch.setattr(main, "load_env_file", lambda root: None)
    monkeypatch.setattr(main, "load_sources_config", lambda root: {})
    monkeypatch.setattr(main, "build_collectors", lambda config: [MockCollector()])
    monkeypatch.setattr(main, "load_scoring_config", lambda root: {
        "weights": {"ai_infrastructure_relevance": 1},
        "keyword_groups": {"ai_infrastructure_relevance": ["serving"]},
        "thresholds": {"include_min_score": 6, "fallback_min_items": 10},
    })
    monkeypatch.setenv("AI_PM_AGENT_DB_PATH", str(db_path))
    monkeypatch.setenv("AI_PM_AGENT_REPORT_DIR", str(tmp_path / "reports"))
    monkeypatch.setenv("AI_PM_AGENT_USE_LLM_SUMMARIES", "false")
    prompts = []
    client = SimpleNamespace(complete=lambda system, prompt: prompts.append(prompt) or "{}")
    monkeypatch.setattr(main.ReportGenerator, "_build_llm_report_synthesizer",
                        lambda self: LLMReportSynthesizer(client))

    report = main.run(7, tmp_path).read_text(encoding="utf-8")
    assert len(clock_calls) == 1
    for item in invalid:
        assert item.url not in report
    assert "Fresh serving" in report and "Cutoff paper" in report and "Undated blog" in report
    assert "**Publication date:** 2026-10-02" in report
    assert "| Publication Date |" in report
    assert CUTOFF.isoformat() in report and NOW.isoformat() in report
    assert "Publication timestamp: " + NOW.isoformat() in prompts[0]
    assert CUTOFF.isoformat() in prompts[0] and NOW.isoformat() in prompts[0]
    assert "Mem0" not in prompts[0]
    store = ItemStore(db_path)
    stored = dict(store.connection.execute("SELECT title, published_at FROM items"))
    store.close()
    assert set(stored) == {"Mem0", "Fresh serving", "Cutoff paper", "Undated blog"}
    assert stored["Mem0"] == old.published_at.isoformat()
