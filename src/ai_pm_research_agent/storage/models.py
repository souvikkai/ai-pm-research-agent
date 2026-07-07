from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any


@dataclass(slots=True)
class CandidateItem:
    title: str
    source: str
    url: str
    category: str
    published_at: datetime | None = None
    author: str | None = None
    raw_text: str | None = None
    abstract: str | None = None
    metadata: dict[str, Any] = field(default_factory=dict)

    @property
    def text_for_analysis(self) -> str:
        parts = [self.title, self.source, self.category, self.author or ""]
        parts.append(self.raw_text or "")
        parts.append(self.abstract or "")
        parts.extend(str(value) for value in self.metadata.values() if value)
        return "\n".join(parts)


@dataclass(slots=True)
class ScoreBreakdown:
    dimensions: dict[str, int]
    weighted_score: float
    reasons: list[str] = field(default_factory=list)


@dataclass(slots=True)
class RankedItem:
    item: CandidateItem
    score: ScoreBreakdown


@dataclass(slots=True)
class ItemSummary:
    title: str
    one_sentence_summary: str
    what_happened: str
    why_it_matters: str
    pm_implication: str
    infra_implication: str
    business_implication: str
    product_decision: str
    interview_talking_point: str
    follow_up_reading: list[str] = field(default_factory=list)
    domain_notes: dict[str, str] = field(default_factory=dict)
