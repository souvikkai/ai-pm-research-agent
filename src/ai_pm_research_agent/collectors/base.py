from __future__ import annotations

from abc import ABC, abstractmethod

from ai_pm_research_agent.storage.models import CandidateItem


class Collector(ABC):
    @abstractmethod
    def collect(self, lookback_days: int = 7) -> list[CandidateItem]:
        """Return normalized candidate items."""
