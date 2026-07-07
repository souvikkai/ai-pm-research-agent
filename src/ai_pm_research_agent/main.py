from __future__ import annotations

import argparse
import logging
import os
from pathlib import Path

from ai_pm_research_agent.collectors.arxiv_collector import ArxivCollector
from ai_pm_research_agent.collectors.blog_collector import BlogCollector
from ai_pm_research_agent.collectors.huggingface_papers_collector import HuggingFacePapersCollector
from ai_pm_research_agent.collectors.papers_with_code_collector import PapersWithCodeCollector
from ai_pm_research_agent.collectors.podcast_collector import PodcastCollector
from ai_pm_research_agent.collectors.rss_collector import RSSCollector
from ai_pm_research_agent.config import PROJECT_ROOT, load_scoring_config, load_sources_config
from ai_pm_research_agent.dedup import deduplicate_items
from ai_pm_research_agent.rankers.relevance_ranker import RelevanceRanker
from ai_pm_research_agent.rankers.selection import select_ranked_items
from ai_pm_research_agent.reports.report_generator import ReportGenerator
from ai_pm_research_agent.storage.db import ItemStore
from ai_pm_research_agent.utils.env import load_env_file
from ai_pm_research_agent.utils.logging import configure_logging

LOGGER = logging.getLogger(__name__)


def build_collectors(sources_config: dict) -> list:
    collectors = []
    arxiv_config = sources_config.get("arxiv", {})
    if arxiv_config.get("enabled", True):
        collectors.append(
            ArxivCollector(
                categories=arxiv_config.get("categories", []),
                query_terms=arxiv_config.get("query_terms", []),
                max_results_per_category=arxiv_config.get("max_results_per_category", 25),
            )
        )

    hf_papers_config = sources_config.get("huggingface_papers", {})
    if hf_papers_config.get("enabled", True):
        collectors.append(
            HuggingFacePapersCollector(
                limit_per_day=hf_papers_config.get("limit_per_day", 20),
                sort=hf_papers_config.get("sort", "trending"),
            )
        )

    pwc_config = sources_config.get("papers_with_code", {})
    if pwc_config.get("enabled", True):
        collectors.append(
            PapersWithCodeCollector(
                max_results=pwc_config.get("max_results", 30),
                api_url=pwc_config.get("api_url", "https://paperswithcode.com/api/v1/papers/"),
                trending_url=pwc_config.get("trending_url", "https://paperswithcode.com/trending"),
            )
        )

    rss_groups = sources_config.get("rss_sources", {})
    newsletters = _enabled_sources(rss_groups.get("newsletters", []))
    company_blogs = _enabled_sources(rss_groups.get("company_blogs", []))
    engineering_blogs = _enabled_sources(rss_groups.get("engineering_blogs", []))
    podcasts = _enabled_sources(rss_groups.get("podcasts", []))
    if newsletters:
        collectors.append(RSSCollector(newsletters))
    if company_blogs:
        collectors.append(BlogCollector(company_blogs))
    if engineering_blogs:
        collectors.append(BlogCollector(engineering_blogs))
    if podcasts:
        collectors.append(PodcastCollector(podcasts))
    return collectors


def _enabled_sources(sources: list[dict]) -> list[dict]:
    return [source for source in sources if source.get("enabled", True)]


def run(lookback_days: int, project_root: Path = PROJECT_ROOT) -> Path:
    load_env_file(project_root)
    sources_config = load_sources_config(project_root)
    scoring_config = load_scoring_config(project_root)
    collectors = build_collectors(sources_config)

    candidates = []
    for collector in collectors:
        LOGGER.info("Collecting with %s", collector.__class__.__name__)
        candidates.extend(collector.collect(lookback_days=lookback_days))

    unique_items = deduplicate_items(candidates)
    LOGGER.info("Collected %s candidates, %s unique", len(candidates), len(unique_items))

    db_path = os.getenv("AI_PM_AGENT_DB_PATH", str(project_root / "data" / "ai_pm_research.db"))
    store = ItemStore(db_path)
    store.upsert_items(unique_items)
    store.close()

    ranker = RelevanceRanker(scoring_config)
    ranked = select_ranked_items(unique_items, ranker, scoring_config)

    report_dir = os.getenv("AI_PM_AGENT_REPORT_DIR", str(project_root / "reports"))
    report_path = ReportGenerator(report_dir).generate(ranked)
    LOGGER.info("Wrote report to %s", report_path)
    return report_path


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate the weekly AI PM research digest.")
    parser.add_argument("--lookback-days", type=int, default=7)
    args = parser.parse_args()
    configure_logging()
    report_path = run(lookback_days=args.lookback_days)
    print(report_path)


if __name__ == "__main__":
    main()
