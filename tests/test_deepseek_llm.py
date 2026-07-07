import json

from ai_pm_research_agent.llm.deepseek_client import DeepSeekClient
from ai_pm_research_agent.summarizers.llm_item_summarizer import _parse_json


def test_deepseek_client_uses_openai_compatible_chat_endpoint(monkeypatch):
    captured = {}

    class FakeResponse:
        def raise_for_status(self):
            return None

        def json(self):
            return {"choices": [{"message": {"content": "ok"}}]}

    def fake_post_chat(url, headers, payload, timeout_seconds):
        captured["url"] = url
        captured["headers"] = headers
        captured["json"] = payload
        captured["timeout"] = timeout_seconds
        return FakeResponse()

    monkeypatch.setattr("ai_pm_research_agent.llm.deepseek_client._post_chat", fake_post_chat)
    client = DeepSeekClient(api_key="test-key", model="deepseek-v4-flash")

    result = client.complete("system", "user")

    assert result == "ok"
    assert captured["url"] == "https://api.deepseek.com/chat/completions"
    assert captured["headers"]["Authorization"] == "Bearer test-key"
    assert captured["json"]["model"] == "deepseek-v4-flash"
    assert captured["json"]["response_format"] == {"type": "json_object"}
    assert captured["json"]["messages"][0]["role"] == "system"


def test_parse_json_accepts_plain_json():
    payload = {"one_sentence_summary": "Short summary"}

    parsed = _parse_json(json.dumps(payload))

    assert parsed["one_sentence_summary"] == "Short summary"
