from ai_pm_research_agent.rankers.relevance_ranker import RelevanceRanker
from ai_pm_research_agent.storage.models import CandidateItem


def test_ranker_prioritizes_hardware_native_ai_pm_topics():
    config = {
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
            "ai_pm_relevance": ["roadmap", "developer experience"],
            "ai_infrastructure_relevance": ["inference", "latency", "gpu"],
            "compiler_runtime_quantization_relevance": ["tensorrt", "int4", "compiler"],
            "edge_automotive_industrial_relevance": ["edge", "automotive"],
            "big_tech_accelerator_relevance": ["nvidia"],
            "product_strategy_relevance": ["sdk", "customer"],
            "linkedin_portfolio_potential": ["benchmark"],
        },
    }
    item = CandidateItem(
        title="NVIDIA TensorRT compiler adds INT4 edge inference benchmark",
        source="NVIDIA",
        url="https://example.com",
        category="company_blog",
        raw_text="SDK roadmap improves developer experience for automotive customer GPU latency.",
    )

    score = RelevanceRanker(config).score_item(item)

    assert score.weighted_score >= 2.0
    assert score.dimensions["compiler_runtime_quantization_relevance"] >= 3
    assert score.dimensions["edge_automotive_industrial_relevance"] >= 2


def test_ranker_does_not_match_keywords_inside_unrelated_words():
    config = {
        "weights": {"big_tech_accelerator_relevance": 1.0},
        "keyword_groups": {"big_tech_accelerator_relevance": ["meta", "intel"]},
    }
    item = CandidateItem(
        title="Substantially better clinical treatment planning",
        source="Example",
        url="https://example.com",
        category="research_paper",
        abstract="This mentions multimodal clinical treatment, not the target companies.",
    )

    score = RelevanceRanker(config).score_item(item)

    assert score.dimensions["big_tech_accelerator_relevance"] == 1


def test_ranker_penalizes_items_without_strategic_core_signal():
    config = {
        "weights": {
            "ai_infrastructure_relevance": 0.25,
            "compiler_runtime_quantization_relevance": 0.25,
            "edge_automotive_industrial_relevance": 0.25,
            "product_strategy_relevance": 0.25,
        },
        "keyword_groups": {
            "ai_infrastructure_relevance": ["inference"],
            "compiler_runtime_quantization_relevance": ["compiler"],
            "edge_automotive_industrial_relevance": ["edge"],
            "product_strategy_relevance": ["api", "docs", "release"],
        },
    }
    item = CandidateItem(
        title="API docs release",
        source="Example",
        url="https://example.com",
        category="builder_blog",
    )

    score = RelevanceRanker(config).score_item(item)

    assert score.weighted_score < 1.5
