from __future__ import annotations

import json
import logging

from ai_pm_research_agent.llm.deepseek_client import DeepSeekClient
from ai_pm_research_agent.storage.models import CandidateItem, ItemSummary, ScoreBreakdown
from ai_pm_research_agent.utils.text import excerpt

LOGGER = logging.getLogger(__name__)


SYSTEM_PROMPT = """You summarize AI research and industry updates for a hardware-native AI Infrastructure PM.
Be source-grounded, concise, non-hypey, and product-minded.
Do not invent facts, numbers, companies, benchmarks, or claims that are not in the provided text.
Return only valid JSON."""


class LLMItemSummarizer:
    def __init__(self, client: DeepSeekClient):
        self.client = client

    def enhance(self, item: CandidateItem, score: ScoreBreakdown, base: ItemSummary) -> ItemSummary:
        source_text = excerpt(item.abstract or item.raw_text or item.title, max_chars=2800)
        prompt = _build_prompt(item, score, base, source_text)
        try:
            content = self.client.complete(SYSTEM_PROMPT, prompt)
            payload = _parse_json(content)
        except Exception as exc:
            LOGGER.warning("LLM summary failed for %s: %s", item.title, exc)
            return base

        base.one_sentence_summary = payload.get("one_sentence_summary", base.one_sentence_summary)
        base.why_it_matters = payload.get("why_it_matters", base.why_it_matters)
        base.pm_implication = payload.get("pm_implication", base.pm_implication)
        base.infra_implication = payload.get("infra_implication", base.infra_implication)
        base.business_implication = payload.get("business_implication", base.business_implication)
        base.product_decision = payload.get("product_decision", base.product_decision)
        base.interview_talking_point = payload.get(
            "interview_talking_point", base.interview_talking_point
        )
        base.domain_notes["llm_enhanced"] = (
            f"Enhanced with {self.client.model}; claims are constrained to the collected source text."
        )
        return base


def _build_prompt(
    item: CandidateItem, score: ScoreBreakdown, base: ItemSummary, source_text: str
) -> str:
    return f"""Source metadata:
- Title: {item.title}
- Source: {item.source}
- Category: {item.category}
- URL: {item.url}
- Author: {item.author or "Unknown"}
- Score: {score.weighted_score}/5
- Score reasons: {"; ".join(score.reasons) or "None"}

Collected source text:
{source_text}

Existing deterministic summary:
- Summary: {base.one_sentence_summary}
- PM implication: {base.pm_implication}
- Infra implication: {base.infra_implication}

Return JSON with exactly these string keys:
{{
  "one_sentence_summary": "one factual sentence",
  "why_it_matters": "why this matters for a hardware-native AI Infrastructure PM",
  "pm_implication": "PM implication in one sentence",
  "infra_implication": "infra/compiler/edge/datacenter implication in one sentence",
  "business_implication": "business or competitive implication in one sentence",
  "product_decision": "what product decision this could change",
  "interview_talking_point": "one practical interview talking point"
}}"""


def _parse_json(content: str) -> dict[str, str]:
    cleaned = content.strip()
    if cleaned.startswith("```"):
        cleaned = cleaned.strip("`")
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
    return {str(key): str(value) for key, value in payload.items() if value is not None}
