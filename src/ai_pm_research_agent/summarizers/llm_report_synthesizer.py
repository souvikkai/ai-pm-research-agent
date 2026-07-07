from __future__ import annotations

import json
import logging

from ai_pm_research_agent.llm.deepseek_client import DeepSeekClient
from ai_pm_research_agent.storage.models import ItemSummary, RankedItem
from ai_pm_research_agent.utils.text import excerpt

LOGGER = logging.getLogger(__name__)


SYSTEM_PROMPT = """You are a senior AI Infrastructure PM advisor.
You write concise weekly synthesis for Souvik Kundu, a semiconductor PM pivoting into AI Infrastructure / Developer Platform PM roles.
Optimize for judgment about serving, compilers, quantization, edge AI, AI accelerators, developer platforms, evals, agents, and Big Tech interview prep.
Use only the provided source summaries and links. Do not invent facts, metrics, citations, or claims.
Return only valid JSON."""


class LLMReportSynthesizer:
    def __init__(self, client: DeepSeekClient):
        self.client = client
        self.last_error: str | None = None

    def synthesize(
        self,
        ranked_items: list[RankedItem],
        summaries: dict[str, ItemSummary],
    ) -> dict:
        self.last_error = None
        if not ranked_items:
            return {}
        try:
            content = self.client.complete(
                SYSTEM_PROMPT,
                _build_prompt(ranked_items, summaries),
            )
            return _parse_json(content)
        except Exception as exc:
            self.last_error = f"{exc.__class__.__name__}: {exc}"
            LOGGER.warning("LLM report synthesis failed: %s", exc)
            return {}


def _build_prompt(ranked_items: list[RankedItem], summaries: dict[str, ItemSummary]) -> str:
    item_blocks: list[str] = []
    for index, entry in enumerate(ranked_items[:12], start=1):
        item = entry.item
        summary = summaries[item.url]
        item_blocks.append(
            "\n".join(
                [
                    f"Rank {index}",
                    f"Title: {item.title}",
                    f"Source: {item.source}",
                    f"Category: {item.category}",
                    f"URL: {item.url}",
                    f"Score: {entry.score.weighted_score}/5",
                    f"Score reasons: {'; '.join(entry.score.reasons) or 'None'}",
                    f"Summary: {excerpt(summary.one_sentence_summary, 500)}",
                    f"PM implication: {summary.pm_implication}",
                    f"Infra implication: {summary.infra_implication}",
                    f"Product decision: {summary.product_decision}",
                ]
            )
        )

    return f"""Ranked weekly items:

{"\n\n".join(item_blocks)}

Return JSON with exactly these keys:
{{
  "executive_summary": [
    "5 to 7 bullets, each grounded in the ranked items"
  ],
  "strategic_synthesis": {{
    "what_changed": "2 to 3 sentences",
    "what_ai_pm_should_watch": "2 to 3 sentences",
    "hype_vs_signal": "1 to 2 sentences",
    "big_tech_interview_angle": "1 to 2 sentences"
  }},
  "must_focus_rationale": {{
    "1": "why rank 1 matters most",
    "2": "why rank 2 matters most",
    "3": "why rank 3 matters most",
    "4": "why rank 4 matters most",
    "5": "why rank 5 matters most"
  }},
  "linkedin_posts": [
    {{
      "option": "A",
      "title": "Broad weekly AI PM digest",
      "draft": "source-grounded LinkedIn draft in Souvik's voice"
    }},
    {{
      "option": "B",
      "title": "Deep dive on one research paper or technical blog",
      "draft": "source-grounded LinkedIn draft"
    }},
    {{
      "option": "C",
      "title": "Hardware-native AI PM angle",
      "draft": "source-grounded LinkedIn draft"
    }},
    {{
      "option": "D",
      "title": "Compiler / quantization / edge AI angle",
      "draft": "source-grounded LinkedIn draft"
    }}
  ],
  "deep_dive": {{
    "title": "title from one ranked item",
    "url": "source URL",
    "why_30_60_minutes": "why this deserves a focused read",
    "questions_to_answer": [
      "3 practical PM questions"
    ]
  }}
}}"""


def _parse_json(content: str) -> dict:
    cleaned = content.strip()
    if cleaned.startswith("```"):
        cleaned = cleaned.strip("`").strip()
        if cleaned.lower().startswith("json"):
            cleaned = cleaned[4:].strip()
    if not cleaned.startswith("{"):
        start = cleaned.find("{")
        end = cleaned.rfind("}")
        if start >= 0 and end > start:
            cleaned = cleaned[start : end + 1]
    payload = json.loads(cleaned)
    if not isinstance(payload, dict):
        raise ValueError("LLM response was not a JSON object")
    return payload
