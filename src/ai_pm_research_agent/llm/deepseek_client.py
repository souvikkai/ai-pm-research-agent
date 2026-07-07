from __future__ import annotations

import logging
import os
from dataclasses import dataclass
from typing import Any

LOGGER = logging.getLogger(__name__)


@dataclass(slots=True)
class DeepSeekClient:
    api_key: str
    model: str = "deepseek-v4-flash"
    base_url: str = "https://api.deepseek.com"
    timeout_seconds: int = 45
    max_tokens: int = 2500
    temperature: float = 0.2

    @classmethod
    def from_env(cls) -> DeepSeekClient | None:
        api_key = os.getenv("DEEPSEEK_API_KEY")
        if not api_key:
            return None
        return cls(
            api_key=api_key,
            model=os.getenv("DEEPSEEK_MODEL", "deepseek-v4-flash"),
            base_url=os.getenv("DEEPSEEK_BASE_URL", "https://api.deepseek.com"),
            timeout_seconds=int(os.getenv("DEEPSEEK_TIMEOUT_SECONDS", "45")),
            max_tokens=int(os.getenv("DEEPSEEK_MAX_TOKENS", "2500")),
            temperature=float(os.getenv("DEEPSEEK_TEMPERATURE", "0.2")),
        )

    def complete(self, system_prompt: str, user_prompt: str) -> str:
        url = f"{self.base_url.rstrip('/')}/chat/completions"
        payload: dict[str, Any] = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            "temperature": self.temperature,
            "max_tokens": self.max_tokens,
            "stream": False,
            "response_format": {"type": "json_object"},
        }
        response = _post_chat(
            url,
            headers={
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
            },
            payload=payload,
            timeout_seconds=self.timeout_seconds,
        )
        response.raise_for_status()
        data = response.json()
        try:
            return data["choices"][0]["message"]["content"].strip()
        except (KeyError, IndexError, TypeError) as exc:
            LOGGER.warning("Unexpected DeepSeek response shape: %s", data)
            raise ValueError("Unexpected DeepSeek response shape") from exc


def llm_summaries_enabled() -> bool:
    value = os.getenv("AI_PM_AGENT_USE_LLM_SUMMARIES", "false")
    return value.strip().lower() in {"1", "true", "yes", "on"}


def llm_item_summaries_enabled() -> bool:
    value = os.getenv("AI_PM_AGENT_USE_LLM_ITEM_SUMMARIES", "false")
    return value.strip().lower() in {"1", "true", "yes", "on"}


def _post_chat(url: str, headers: dict[str, str], payload: dict[str, Any], timeout_seconds: int):
    import requests

    return requests.post(url, headers=headers, json=payload, timeout=timeout_seconds)
