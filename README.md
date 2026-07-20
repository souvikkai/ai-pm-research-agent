# AI PM Research Agent

This repo builds a weekly research digest for Souvik Kundu's pivot from semiconductor / hardware PM into AI Infrastructure and AI PM roles. It is optimized for judgment, not volume: the core question is:

> What did I need to know this week to become a stronger AI Infrastructure / Developer Platform PM for AI accelerators, edge inference, and datacenter AI serving?

## What It Does

The agent collects AI research and industry updates, normalizes them into one schema, removes duplicates, scores relevance, summarizes high-signal items, and writes a weekly Markdown report.

The report focuses on:

- AI infrastructure, serving, evals, agents, and RAG
- Graph compilers, runtimes, SDKs, and developer platforms
- Quantization, numerics, and model compression
- Edge AI, automotive AI, industrial AI, robotics, and constrained deployment
- Datacenter inference, GPU utilization, serving cost, and reliability
- AI accelerator and developer-platform competitive intelligence
- Portfolio project ideas and source-backed LinkedIn drafts

## Repo Structure

```text
ai-pm-research-agent/
  config/
    scoring.yaml
    sources.yaml
  reports/
  src/ai_pm_research_agent/
    collectors/
    rankers/
    reports/
    storage/
    summarizers/
    utils/
  tests/
  .github/workflows/weekly-digest.yml
  .env
  main.py
  pyproject.toml
```

## How It Works

1. **Collect** from arXiv and RSS sources.
2. **Normalize** each item into title, source, author, date, URL, category, text, and metadata.
3. **Deduplicate** by normalized URL, fingerprint, and near-duplicate title matching.
4. **Score** every item using the weighted AI infrastructure PM rubric in `config/scoring.yaml`.
5. **Summarize** high-value items with deterministic source-grounded summaries.
6. **Synthesize** themes across product, infra, compiler, edge, datacenter, and competitive lenses, optionally using DeepSeek after filtering.
7. **Generate** `reports/YYYY-MM-DD-weekly-ai-pm-digest.md`.
8. **Draft LinkedIn posts** with source links from the report.

## Scoring

The current weighted scoring model is:

- AI PM relevance: 15%
- AI infrastructure relevance: 20%
- Compiler / runtime / quantization relevance: 20%
- Edge / automotive / industrial relevance: 15%
- Big Tech / AI accelerator relevance: 10%
- Product strategy relevance: 10%
- LinkedIn / portfolio potential: 10%

Each dimension is scored 1-5 using keywords and source metadata. This MVP is intentionally transparent and easy to tune. Edit `config/scoring.yaml` to adjust weights, thresholds, or keyword groups.

The default inclusion threshold is intentionally calibrated for the current non-LLM MVP collector, which mostly sees titles, abstracts, and RSS summaries rather than full article bodies. If fewer than `fallback_min_items` clear the threshold, the agent uses the highest-scored candidates so the weekly report is never blank.

## Configure Sources

Edit `config/sources.yaml`.

Current MVP source types:

- arXiv categories: `cs.AI`, `cs.CL`, `cs.LG`, `cs.CV`, `stat.ML`
- Hugging Face Daily Papers
- Papers with Code / trending implementation-adjacent papers
- RSS newsletters
- AI lab and company blogs
- Engineering blogs
- Podcast RSS feeds

Add a new RSS source like this:

```yaml
rss_sources:
  engineering_blogs:
    - name: Example Infra Blog
      url: https://example.com/feed.xml
      category: engineering_blog
```

If a source is strategically important but has no working RSS feed, keep it in `sources.yaml` with `enabled: false` and add a note. That keeps the roadmap visible without creating noisy weekly fetch warnings.

Hugging Face Daily Papers and Papers with Code are configured at the top level of `sources.yaml`. Papers with Code is treated as a best-effort source because the old API/docs may redirect into Hugging Face's paper experience; the collector tries the legacy API first and then falls back to the trending page.

## Run Locally

```bash
cd ai-pm-research-agent
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
python -m pip install -e ".[dev]"
pytest
ai-pm-research-agent --lookback-days 7
```

The report will be written to `reports/YYYY-MM-DD-weekly-ai-pm-digest.md`.

Report dates use `AI_PM_AGENT_TIMEZONE` from `.env` / environment variables. The default is `America/Phoenix`, so an evening run in Arizona will not roll the filename to the next UTC day.

## Environment Variables

Edit `.env` if you want to customize runtime paths or add API keys.

The agent does not require an LLM API key. By default, it uses extractive, source-grounded summaries to avoid fabricated claims.

To enable optional DeepSeek summaries for the already-filtered items:

```bash
AI_PM_AGENT_USE_LLM_SUMMARIES=true
AI_PM_AGENT_USE_LLM_ITEM_SUMMARIES=false
DEEPSEEK_API_KEY=your_key_here
DEEPSEEK_MODEL=deepseek-v4-flash
DEEPSEEK_MAX_TOKENS=2500
```

DeepSeek is called only after collection, deduplication, and scoring. By default, the agent makes one report-level synthesis call for the filtered ranked items: executive summary, strategic synthesis, must-focus rationale, deep dive, and LinkedIn drafts. That keeps cost low because the LLM never sees the entire feed.

Keep `AI_PM_AGENT_USE_LLM_ITEM_SUMMARIES=false` unless you explicitly want DeepSeek to enhance each selected item one by one. If any API call fails, the report falls back to deterministic summaries.

## Weekly Scheduling

The repo includes `.github/workflows/weekly-digest.yml`.

It runs every Friday at 15:00 UTC, installs the package, runs tests, generates the digest, and commits the report back to the repo.

You can also run it manually from GitHub Actions with `workflow_dispatch`.

## Report Sections

The generated report uses this structure:

1. Executive Summary
2. Strategic Synthesis
3. Must-Focus Items This Week
4. Top 10 Ranked Briefing
5. Theme Map
6. Research Papers Reading Queue
7. Big Tech, AI Lab, and Competitive Watch
8. Model Zoo Watch
9. Portfolio Project Ideas
10. LinkedIn Post Ideas
11. Interview Talking Points
12. Recommended Deep Dive of the Week
13. Source Index

The recommended deep dive is an active-reading artifact, not a passive summary. It includes a 20-30 minute reading protocol, blank extraction sentences the reader must complete, and a benchmark skepticism check for baseline, hardware, batch size, sequence length, and production realism. The completed extraction sentence is intended to become the seed for LinkedIn posts and PM interview stories.

## Example Output

```markdown
# Weekly AI PM Research Digest — 2026-06-30

## 1. Executive Summary

- 18 items met the hardware-native AI PM relevance threshold.
- Highest-scoring themes: compiler runtime quantization relevance, AI infrastructure relevance, edge automotive industrial relevance.
- Prioritize items that change SDK roadmap, compiler support, serving cost, edge deployment confidence, or AI accelerator adoption.

## 15. Recommended Deep Dive of the Week

**Pick:** [Example source title](https://example.com/source)

Spend 30-60 minutes on this because it changes a deployment or roadmap decision.
```

## Current MVP and Next Steps

Implemented:

- arXiv collector
- Hugging Face Daily Papers collector
- Papers with Code collector with trending-page fallback
- RSS collector for newsletters, blogs, and podcasts
- Deduplication
- Hardware-native weighted scoring
- SQLite persistence
- Markdown report generation
- Source index
- Four LinkedIn draft angles
- Optional DeepSeek report-level synthesis and LinkedIn refinement
- Tests for scoring, deduplication, and report generation
- GitHub Actions weekly cron

Recommended next additions:

- Semantic Scholar enrichment
- Source health dashboard for paper collectors
- LLM-backed theme synthesis and LinkedIn draft refinement
- Local dashboard or FastAPI endpoint
- Richer company taxonomy and source health monitoring
