from __future__ import annotations

from ai_pm_research_agent.storage.models import RankedItem


class LinkedInGenerator:
    def generate(self, ranked_items: list[RankedItem]) -> list[dict[str, str]]:
        top = ranked_items[:4]
        source_lines = "\n".join(f"- {entry.item.title}: {entry.item.url}" for entry in top)
        anchor = top[0].item if top else None
        anchor_title = anchor.title if anchor else "this week's AI infrastructure updates"

        return [
            {
                "option": "A",
                "title": "Broad weekly AI PM digest",
                "draft": (
                    "This week's AI signal is less about novelty for its own sake and more about deployment judgment.\n\n"
                    "The items I would track as a hardware-native AI PM are the ones that connect model capability to serving cost, "
                    "runtime maturity, developer adoption, and customer confidence.\n\n"
                    "My filter: what changes a roadmap decision, an SDK priority, or an infra metric?"
                    f"\n\nSources:\n{source_lines}"
                ),
            },
            {
                "option": "B",
                "title": "Deep dive on one research paper or technical blog",
                "draft": (
                    f"One item worth a deeper look this week: {anchor_title}.\n\n"
                    "The product question is not just whether the technique is technically impressive. It is whether it changes "
                    "latency, memory, cost, reliability, or developer experience enough to affect a real deployment decision.\n\n"
                    "The PM move is to ask: what metric would prove this matters, and what customer workload would expose the tradeoff?"
                    f"\n\nSource: {anchor.url if anchor else 'See report source index.'}"
                ),
            },
            {
                "option": "C",
                "title": "Hardware-native AI PM angle",
                "draft": (
                    "AI product strategy is increasingly constrained by the physical stack: silicon, memory bandwidth, compiler support, "
                    "runtime scheduling, and serving economics.\n\n"
                    "That is the opportunity for hardware-native PMs. The best roadmap decisions connect customer-facing capability to "
                    "what the hardware and software stack can actually sustain in production.\n\n"
                    f"Source-backed items:\n{source_lines}"
                ),
            },
            {
                "option": "D",
                "title": "Compiler / quantization / edge AI angle",
                "draft": (
                    "Compiler and quantization work can look like implementation detail until you view it through SDK adoption.\n\n"
                    "Operator coverage, quantized graph lowering, model zoo completeness, and edge/datacenter benchmark quality all shape "
                    "developer confidence. A missing graph pattern or unsupported datatype can become a product adoption blocker.\n\n"
                    "The PM question: which models should be forcing functions for compiler completeness and customer demos?"
                    f"\n\nSources:\n{source_lines}"
                ),
            },
        ]
