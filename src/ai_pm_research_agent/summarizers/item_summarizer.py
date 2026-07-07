from __future__ import annotations

from ai_pm_research_agent.storage.models import CandidateItem, ItemSummary, ScoreBreakdown
from ai_pm_research_agent.utils.text import excerpt, keyword_hits


DOMAIN_KEYWORDS = {
    "compiler": ["mlir", "tvm", "xla", "iree", "tensorrt", "triton", "openvino", "onnx", "executorch", "torch.compile", "kernel"],
    "quantization": ["quantization", "int8", "int4", "fp8", "mxfp", "awq", "gptq", "smoothquant", "kv cache"],
    "edge": ["edge", "automotive", "adas", "robotics", "industrial", "embedded", "npu", "dsp", "sensor", "real-time"],
    "datacenter": ["serving", "vllm", "triton inference", "ray serve", "kserve", "sglang", "gpu", "batching", "latency", "throughput"],
    "agents": ["agent", "rag", "eval", "safety", "tool use", "memory", "guardrail"],
}


class ItemSummarizer:
    def summarize(self, item: CandidateItem, score: ScoreBreakdown) -> ItemSummary:
        source_text = item.abstract or item.raw_text or item.title
        one_sentence = excerpt(source_text, 220) or item.title
        domain_notes = self._domain_notes(item)
        strongest_dimension = max(score.dimensions, key=lambda key: score.dimensions[key])

        return ItemSummary(
            title=item.title,
            one_sentence_summary=one_sentence,
            what_happened=_what_happened(item),
            why_it_matters=_why_it_matters(item, strongest_dimension),
            pm_implication=_pm_implication(item, domain_notes),
            infra_implication=_infra_implication(domain_notes),
            business_implication=_business_implication(item),
            product_decision=_product_decision(domain_notes),
            interview_talking_point=_interview_talking_point(item, domain_notes),
            follow_up_reading=[item.url],
            domain_notes=domain_notes,
        )

    def _domain_notes(self, item: CandidateItem) -> dict[str, str]:
        text = item.text_for_analysis.lower()
        notes: dict[str, str] = {}
        for domain, keywords in DOMAIN_KEYWORDS.items():
            hits = keyword_hits(text, keywords)
            if hits:
                notes[domain] = f"Signals: {', '.join(hits[:6])}."
        return notes


def _what_happened(item: CandidateItem) -> str:
    if item.category == "research_paper":
        return "A research paper introduced or evaluated a technical approach relevant to AI infrastructure, model deployment, or AI product judgment."
    if item.category == "podcast":
        return "A long-form discussion surfaced context worth tracking for AI infrastructure or AI product strategy."
    return "A source published an update relevant to AI infrastructure, developer platforms, model deployment, or AI product strategy."


def _why_it_matters(item: CandidateItem, strongest_dimension: str) -> str:
    readable = strongest_dimension.replace("_", " ")
    return f"It ranks highly on {readable}, which makes it useful for separating infrastructure signal from general AI noise."


def _pm_implication(item: CandidateItem, domain_notes: dict[str, str]) -> str:
    if "compiler" in domain_notes:
        return "A PM should ask whether the SDK, compiler support matrix, docs, and customer demos cover the model patterns developers now expect."
    if "quantization" in domain_notes:
        return "A PM should connect accuracy, latency, memory, and hardware support before treating the update as roadmap-ready."
    if "edge" in domain_notes:
        return "A PM should frame the implication around deployment constraints: power, thermals, memory, latency, safety, and customer integration effort."
    if "datacenter" in domain_notes:
        return "A PM should translate the update into cost per token, TTFT, throughput, utilization, reliability, and operational simplicity."
    return "A PM should identify what customer workflow, roadmap bet, or competitive positioning this update could change."


def _infra_implication(domain_notes: dict[str, str]) -> str:
    if "datacenter" in domain_notes:
        return "Likely touches serving efficiency, scaling behavior, GPU utilization, or inference cost."
    if "compiler" in domain_notes:
        return "Likely touches graph lowering, operator coverage, kernel generation, portability, or runtime scheduling."
    if "edge" in domain_notes:
        return "Likely touches constrained deployment across CPU, GPU, NPU, DSP, embedded Linux, or safety-critical systems."
    if "quantization" in domain_notes:
        return "Likely touches datatype support, memory footprint, throughput, accuracy, or hardware enablement."
    return "Infrastructure implication should be validated against latency, cost, reliability, and adoption metrics."


def _business_implication(item: CandidateItem) -> str:
    return "The business angle is whether this changes buyer confidence, developer adoption, competitive differentiation, or the cost curve for production AI."


def _product_decision(domain_notes: dict[str, str]) -> str:
    if "compiler" in domain_notes:
        return "Prioritize compiler/runtime coverage, framework integrations, and model zoo proof points for the affected workloads."
    if "quantization" in domain_notes:
        return "Decide whether to support a datatype or quantization path in the SDK, benchmarks, docs, and customer enablement."
    if "edge" in domain_notes:
        return "Decide which edge demos, reference designs, and deployment constraints deserve roadmap priority."
    if "datacenter" in domain_notes:
        return "Decide whether serving-stack work should target latency, throughput, cost per token, autoscaling, or reliability first."
    return "Decide whether this is a roadmap input, interview talking point, LinkedIn idea, or background reading."


def _interview_talking_point(item: CandidateItem, domain_notes: dict[str, str]) -> str:
    if domain_notes:
        domains = ", ".join(domain_notes)
        return f"Use this to discuss how an AI PM evaluates {domains} through customer impact, measurable infra metrics, and roadmap tradeoffs."
    return "Use this to show disciplined judgment: what changed, why it matters, and what product metric would prove it mattered."
