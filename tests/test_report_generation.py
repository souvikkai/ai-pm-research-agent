from datetime import UTC, datetime

from ai_pm_research_agent.rankers.relevance_ranker import RelevanceRanker
from ai_pm_research_agent.reports.report_generator import ReportGenerator
from ai_pm_research_agent.storage.models import CandidateItem


def test_report_generator_writes_updated_section_structure(tmp_path):
    scoring_config = {
        "weights": {
            "ai_pm_relevance": 0.15,
            "ai_infrastructure_relevance": 0.20,
            "compiler_runtime_quantization_relevance": 0.20,
            "edge_automotive_industrial_relevance": 0.15,
            "big_tech_accelerator_relevance": 0.10,
            "product_strategy_relevance": 0.10,
            "linkedin_portfolio_potential": 0.10,
        },
        "keyword_groups": {
            "ai_pm_relevance": ["roadmap", "platform"],
            "ai_infrastructure_relevance": ["serving", "gpu"],
            "compiler_runtime_quantization_relevance": ["mlir", "quantization"],
            "edge_automotive_industrial_relevance": ["edge", "industrial"],
            "big_tech_accelerator_relevance": ["nvidia"],
            "product_strategy_relevance": ["sdk", "model zoo"],
            "linkedin_portfolio_potential": ["demo", "benchmark"],
        },
    }
    item = CandidateItem(
        title="MLIR quantization path improves edge serving demo",
        source="Example Lab",
        url="https://example.com/mlir",
        category="research_paper",
        published_at=datetime(2026, 6, 30, tzinfo=UTC),
        author="A. Researcher",
        abstract="MLIR quantization for edge GPU serving improves SDK model zoo confidence.",
    )
    ranked = RelevanceRanker(scoring_config).rank([item])

    path = ReportGenerator(tmp_path).generate(ranked, report_date=datetime(2026, 6, 30, tzinfo=UTC))
    report = path.read_text(encoding="utf-8")

    assert "## 2. Strategic Synthesis" in report
    assert "## 3. Must-Focus Items This Week" in report
    assert "## 4. Top 10 Ranked Briefing" in report
    assert "## 5. Theme Map" in report
    assert "### Graph Compilers, Runtime, and SDK Platform" in report
    assert "### Edge, Automotive, and Industrial AI" in report
    assert "## 7. Big Tech, AI Lab, and Competitive Watch" in report
    assert "### AI Accelerator and Developer Platform Competitive Intelligence" in report
    assert "### Option D: Compiler / quantization / edge AI angle" in report
    assert "## Recommended Deep Dive of the Week" in report
    assert "### Reading protocol (20-30 min)" in report
    assert "- [ ] Pass 1 (3 min): Abstract + conclusion only." in report
    assert "> This paper showed ______ under conditions ______." in report
    assert "> This changes the ______ decision for ______ because ______." in report
    assert "### Benchmark skepticism check" in report
    assert "- Baseline compared against: ______" in report
    assert "- Hardware / batch size / seq length: ______" in report
    assert "Use the completed deep-dive extraction sentence as the seed" in report
