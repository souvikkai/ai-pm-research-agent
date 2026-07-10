from __future__ import annotations

from collections import defaultdict
from datetime import datetime
from pathlib import Path

from ai_pm_research_agent.llm.deepseek_client import (
    DeepSeekClient,
    llm_item_summaries_enabled,
    llm_summaries_enabled,
)
from ai_pm_research_agent.storage.models import ItemSummary, RankedItem
from ai_pm_research_agent.summarizers.item_summarizer import ItemSummarizer
from ai_pm_research_agent.summarizers.linkedin_generator import LinkedInGenerator
from ai_pm_research_agent.summarizers.llm_item_summarizer import LLMItemSummarizer
from ai_pm_research_agent.summarizers.llm_report_synthesizer import LLMReportSynthesizer
from ai_pm_research_agent.summarizers.paper_summarizer import PaperSummarizer
from ai_pm_research_agent.utils.dates import report_date_slug
from ai_pm_research_agent.utils.text import keyword_hits


class ReportGenerator:
    def __init__(self, report_dir: str | Path):
        self.report_dir = Path(report_dir)
        self.report_dir.mkdir(parents=True, exist_ok=True)
        self.item_summarizer = ItemSummarizer()
        self.paper_summarizer = PaperSummarizer()
        self.linkedin_generator = LinkedInGenerator()
        self.llm_client = self._build_llm_client()
        self.llm_summarizer = self._build_llm_summarizer()
        self.llm_report_synthesizer = self._build_llm_report_synthesizer()

    def generate(self, ranked_items: list[RankedItem], report_date: datetime | None = None) -> Path:
        date_slug = report_date_slug(report_date)
        output_path = self.report_dir / f"{date_slug}-weekly-ai-pm-digest.md"
        summaries = self._summaries(ranked_items)
        sections = self._section_items(ranked_items)
        ranks = {entry.item.url: index for index, entry in enumerate(ranked_items, start=1)}
        synthesis = self._synthesis(ranked_items, summaries)

        lines: list[str] = [
            f"# Weekly AI PM Research Digest — {date_slug}",
            "",
            "## 1. Executive Summary",
            "",
            *self._executive_summary(ranked_items, synthesis),
            "",
            "## 2. Strategic Synthesis",
            "",
            *self._strategic_synthesis(synthesis),
            "",
            "## 3. Must-Focus Items This Week",
            "",
            *self._must_focus_items(ranked_items, summaries, synthesis),
            "",
            "## 4. Top 10 Ranked Briefing",
            "",
            *self._ranked_briefing_table(ranked_items[:10], summaries),
            "",
            "## 5. Theme Map",
            "",
            *self._theme_map(sections, ranks),
            "",
            "## 6. Research Papers Reading Queue",
            "",
            *self._paper_queue(sections["research_paper"], summaries, ranks),
            "",
            "## 7. Big Tech, AI Lab, and Competitive Watch",
            "",
            *self._big_tech_watch(ranked_items),
            "",
            *self._competitive_intel(ranked_items, ranks),
            "",
            "## 8. Model Zoo Watch",
            "",
            *self._model_zoo_watch(ranked_items),
            "",
            "## 9. Portfolio Project Ideas",
            "",
            *self._portfolio_ideas(ranked_items),
            "",
            "## 10. LinkedIn Post Ideas",
            "",
            *self._linkedin_posts(ranked_items, synthesis),
            "",
            "## 11. Interview Talking Points",
            "",
            *self._interview_talking_points(ranked_items, summaries),
            "",
            "## Recommended Deep Dive of the Week",
            "",
            *self._deep_dive(ranked_items, summaries, synthesis),
            "",
            "## 13. Source Index",
            "",
            *self._source_index(ranked_items),
            "",
        ]
        output_path.write_text("\n".join(lines), encoding="utf-8")
        return output_path

    def _summaries(self, ranked_items: list[RankedItem]) -> dict[str, ItemSummary]:
        summaries = {}
        for entry in ranked_items:
            summarizer = self.paper_summarizer if entry.item.category == "research_paper" else self.item_summarizer
            summary = summarizer.summarize(entry.item, entry.score)
            if self.llm_summarizer:
                summary = self.llm_summarizer.enhance(entry.item, entry.score, summary)
            summaries[entry.item.url] = summary
        return summaries

    def _build_llm_client(self) -> DeepSeekClient | None:
        if not llm_summaries_enabled():
            return None
        return DeepSeekClient.from_env()

    def _build_llm_summarizer(self) -> LLMItemSummarizer | None:
        if not llm_item_summaries_enabled() or self.llm_client is None:
            return None
        return LLMItemSummarizer(self.llm_client)

    def _build_llm_report_synthesizer(self) -> LLMReportSynthesizer | None:
        if self.llm_client is None:
            return None
        return LLMReportSynthesizer(self.llm_client)

    def _synthesis(
        self, ranked_items: list[RankedItem], summaries: dict[str, ItemSummary]
    ) -> dict:
        if self.llm_report_synthesizer is None:
            return {}
        synthesis = self.llm_report_synthesizer.synthesize(ranked_items, summaries)
        if not synthesis and self.llm_report_synthesizer.last_error:
            return {"_llm_error": self.llm_report_synthesizer.last_error}
        return synthesis

    def _section_items(self, ranked_items: list[RankedItem]) -> dict[str, list[RankedItem]]:
        sections: dict[str, list[RankedItem]] = defaultdict(list)
        for entry in ranked_items:
            if entry.item.category == "research_paper":
                sections["research_paper"].append(entry)
            text = entry.item.text_for_analysis.lower()
            if keyword_hits(text, ["mlir", "tvm", "xla", "iree", "tensorrt", "triton", "onnx", "openvino", "executorch", "torch.compile", "compiler", "runtime", "sdk"]):
                sections["compiler"].append(entry)
            if keyword_hits(text, ["quantization", "quantized", "int8", "int4", "fp8", "mxfp", "awq", "gptq", "smoothquant", "compression"]):
                sections["quantization"].append(entry)
            if keyword_hits(text, ["edge", "automotive", "adas", "robotics", "robot", "industrial", "embedded", "sensor", "npu", "dsp", "low-power"]):
                sections["edge"].append(entry)
            if keyword_hits(text, ["serving", "datacenter", "vllm", "kserve", "ray serve", "sglang", "gpu", "batching", "throughput", "latency"]):
                sections["datacenter"].append(entry)
            if keyword_hits(text, ["agent", "agents", "rag", "eval", "evaluation", "safety", "guardrail", "tool use", "memory"]):
                sections["agents"].append(entry)
        return sections

    def _executive_summary(self, ranked_items: list[RankedItem], synthesis: dict) -> list[str]:
        llm_bullets = synthesis.get("executive_summary")
        if isinstance(llm_bullets, list) and llm_bullets:
            return [f"- {bullet}" for bullet in llm_bullets[:7]]
        if not ranked_items:
            return ["- No items met the configured relevance threshold this week."]
        top_domains = self._dominant_dimensions(ranked_items[:10])
        lines = [
            f"- {len(ranked_items)} items met the hardware-native AI PM relevance threshold.",
            f"- Highest-scoring themes: {', '.join(top_domains[:4])}.",
            "- Prioritize items that change SDK roadmap, compiler support, serving cost, edge deployment confidence, or AI accelerator adoption.",
            "- Treat consumer AI news as signal only when it changes infrastructure, deployment, developer-platform, or enterprise product decisions.",
            "- Use the top items to prepare interview stories around metrics, tradeoffs, roadmap sequencing, and customer constraints.",
        ]
        if ranked_items:
            lines.append(f"- Deep-dive candidate: {ranked_items[0].item.title}.")
        return lines[:8]

    def _strategic_synthesis(self, synthesis: dict) -> list[str]:
        strategic = synthesis.get("strategic_synthesis")
        if not isinstance(strategic, dict):
            if synthesis.get("_llm_error"):
                return [
                    f"- DeepSeek synthesis was enabled but failed: `{synthesis['_llm_error']}`",
                    "- The report below uses deterministic fallback content.",
                ]
            return [
                "- LLM synthesis was not enabled or did not complete; use the ranked briefing and theme map below.",
            ]
        fields = [
            ("What changed", strategic.get("what_changed")),
            ("What an AI PM should watch", strategic.get("what_ai_pm_should_watch")),
            ("Hype vs signal", strategic.get("hype_vs_signal")),
            ("Big Tech interview angle", strategic.get("big_tech_interview_angle")),
        ]
        return [f"- **{label}:** {value}" for label, value in fields if value]

    def _top_items(self, entries: list[RankedItem], summaries: dict[str, ItemSummary]) -> list[str]:
        if not entries:
            return ["No top items available."]
        lines: list[str] = []
        for index, entry in enumerate(entries, start=1):
            item = entry.item
            summary = summaries[item.url]
            lines.extend(
                [
                    f"### {index}. {item.title}",
                    "",
                    f"- **Source:** {item.source}",
                    f"- **Link:** {item.url}",
                    f"- **Date:** {item.published_at.date().isoformat() if item.published_at else 'Unknown'}",
                    f"- **Category:** {item.category}",
                    f"- **Score:** {entry.score.weighted_score}/5",
                    f"- **Summary:** {summary.one_sentence_summary}",
                    f"- **Why it matters for AI PM:** {summary.why_it_matters}",
                    f"- **Product decision it could change:** {summary.product_decision}",
                    f"- **Interview talking point:** {summary.interview_talking_point}",
                    "",
                ]
            )
        return lines

    def _must_focus_items(
        self, ranked_items: list[RankedItem], summaries: dict[str, ItemSummary], synthesis: dict
    ) -> list[str]:
        focus_items = self._focus_items(ranked_items)
        focus_rationale = synthesis.get("must_focus_rationale", {})
        if not isinstance(focus_rationale, dict):
            focus_rationale = {}
        if not focus_items:
            return ["No must-focus items available this week."]
        lines = [
            "Read these first. They are the highest-value items for AI infrastructure PM interview prep, product judgment, or hardware-native roadmap thinking.",
            "",
        ]
        for index, entry in enumerate(focus_items, start=1):
            item = entry.item
            summary = summaries[item.url]
            lines.extend(
                [
                    f"### Focus {index}: {item.title}",
                    "",
                    f"- **Source:** {item.source}",
                    f"- **Link:** {item.url}",
                    f"- **Score:** {entry.score.weighted_score}/5",
                    f"- **Why this is high value:** {focus_rationale.get(str(index), self._focus_reason(entry))}",
                    f"- **What to extract:** {summary.product_decision}",
                    f"- **Interview angle:** {summary.interview_talking_point}",
                    "",
                ]
            )
        return lines

    def _ranked_briefing_table(
        self, entries: list[RankedItem], summaries: dict[str, ItemSummary]
    ) -> list[str]:
        if not entries:
            return ["No ranked items available."]
        lines = [
            "| Rank | Item | Category | Score | Why It Matters |",
            "|---:|---|---|---:|---|",
        ]
        for index, entry in enumerate(entries, start=1):
            item = entry.item
            summary = summaries[item.url]
            lines.append(
                f"| {index} | [{_escape_table(item.title)}]({item.url}) | {item.category} | {entry.score.weighted_score}/5 | {_escape_table(summary.one_sentence_summary)} |"
            )
        return lines

    def _theme_map(
        self, sections: dict[str, list[RankedItem]], ranks: dict[str, int]
    ) -> list[str]:
        groups = [
            ("Graph Compilers, Runtime, and SDK Platform", "compiler"),
            ("Quantization, Numerics, and Model Compression", "quantization"),
            ("Edge, Automotive, and Industrial AI", "edge"),
            ("Datacenter AI Infrastructure and Serving", "datacenter"),
            ("Agents, RAG, Evals, and Safety", "agents"),
        ]
        lines: list[str] = []
        for title, key in groups:
            lines.append(f"### {title}")
            entries = sections.get(key, [])
            if not entries:
                lines.extend(["- No high-signal item in this theme this week.", ""])
                continue
            for entry in entries[:5]:
                rank = ranks.get(entry.item.url)
                prefix = f"#{rank} " if rank else ""
                lines.append(
                    f"- **{prefix}{entry.item.title}** — score {entry.score.weighted_score}/5; source: {entry.item.source}; link: {entry.item.url}"
                )
            lines.append("")
        return lines

    def _paper_queue(
        self, entries: list[RankedItem], summaries: dict[str, ItemSummary], ranks: dict[str, int]
    ) -> list[str]:
        if not entries:
            return ["No research papers crossed the threshold this week."]
        lines = [
            "| Priority | Paper | Action | PM Reason |",
            "|---:|---|---|---|",
        ]
        for entry in entries[:10]:
            item = entry.item
            summary = summaries[item.url]
            rank = ranks.get(item.url, "-")
            action = summary.domain_notes.get("recommended_action", "Skim")
            lines.append(
                f"| {rank} | [{_escape_table(item.title)}]({item.url}) | {action} | {_escape_table(summary.pm_implication)} |"
            )
        return lines

    def _items_for_section(self, entries: list[RankedItem], summaries: dict[str, ItemSummary], paper: bool = False) -> list[str]:
        if not entries:
            return ["No high-signal items in this section this week."]
        lines: list[str] = []
        for entry in entries[:8]:
            item = entry.item
            summary = summaries[item.url]
            lines.extend(
                [
                    f"### {item.title}",
                    "",
                    f"- **Source:** {item.source}",
                    f"- **Link:** {item.url}",
                    f"- **Score:** {entry.score.weighted_score}/5",
                    f"- **What happened:** {summary.what_happened}",
                    f"- **PM implication:** {summary.pm_implication}",
                    f"- **AI infra implication:** {summary.infra_implication}",
                    f"- **Business / competitive implication:** {summary.business_implication}",
                ]
            )
            if paper:
                lines.extend(
                    [
                        f"- **Authors:** {item.author or 'Unknown'}",
                        f"- **Problem being solved:** {summary.one_sentence_summary}",
                        "- **Core idea:** See abstract and source; MVP avoids fabricating method details beyond available metadata.",
                        f"- **Recommended action:** {summary.domain_notes.get('recommended_action', 'Skim')}",
                    ]
                )
            for key, note in summary.domain_notes.items():
                lines.append(f"- **{key.replace('_', ' ').title()}:** {note}")
            lines.append("")
        return lines

    def _big_tech_watch(self, ranked_items: list[RankedItem]) -> list[str]:
        companies = ["Google / DeepMind", "Meta", "Amazon / AWS", "Microsoft", "Apple", "OpenAI", "Anthropic", "NVIDIA"]
        aliases = {
            "Google / DeepMind": ["google", "deepmind", "tpu"],
            "Meta": ["meta", "pytorch", "executorch"],
            "Amazon / AWS": ["amazon", "aws", "trainium", "inferentia"],
            "Microsoft": ["microsoft", "azure", "onnx"],
            "Apple": ["apple", "core ml"],
            "OpenAI": ["openai"],
            "Anthropic": ["anthropic", "claude"],
            "NVIDIA": ["nvidia", "cuda", "tensorrt", "triton"],
        }
        lines: list[str] = []
        for company in companies:
            matches = [
                entry
                for entry in ranked_items
                if keyword_hits(entry.item.text_for_analysis, aliases[company])
            ]
            lines.append(f"### {company}")
            if matches:
                lines.extend(f"- [{entry.item.title}]({entry.item.url}) — score {entry.score.weighted_score}/5" for entry in matches[:4])
            else:
                lines.append("- No high-signal tracked item this week.")
            lines.append("")
        return lines

    def _competitive_intel(self, ranked_items: list[RankedItem], ranks: dict[str, int]) -> list[str]:
        keywords = ["nvidia", "arm", "hailo", "tenstorrent", "groq", "cerebras", "amd", "intel", "qualcomm", "core ml", "openvino", "onnx", "modular", "optimum", "tensorrt"]
        matches = [entry for entry in ranked_items if keyword_hits(entry.item.text_for_analysis, keywords)]
        if not matches:
            return ["### AI Accelerator and Developer Platform Competitive Intelligence", "", "No competitive-intelligence items crossed the threshold this week."]
        lines: list[str] = []
        lines.extend(["### AI Accelerator and Developer Platform Competitive Intelligence", ""])
        for entry in matches[:8]:
            rank = ranks.get(entry.item.url)
            prefix = f"#{rank} " if rank else ""
            lines.extend(
                [
                    f"- **{prefix}{entry.item.title}** ({entry.item.source}) — {entry.item.url}",
                    "  Target lens: what shipped, target developer, favored hardware, developer experience angle, and roadmap implication.",
                ]
            )
        return lines

    def _model_zoo_watch(self, ranked_items: list[RankedItem]) -> list[str]:
        keywords = ["llm", "small language model", "vision transformer", "vlm", "bev", "yolo", "sam", "speech", "diffusion", "time-series", "robotics"]
        matches = [entry for entry in ranked_items if keyword_hits(entry.item.text_for_analysis, keywords)]
        if not matches:
            return ["No model-zoo forcing-function items crossed the threshold this week."]
        return [
            f"- **{entry.item.title}** — ask what operators, graph patterns, quantization support, and demo value this model family stresses. {entry.item.url}"
            for entry in matches[:8]
        ]

    def _portfolio_ideas(self, ranked_items: list[RankedItem]) -> list[str]:
        anchor = ranked_items[0].item.title if ranked_items else "weekly AI infrastructure signal"
        return [
            "- **Compiler support matrix for edge AI models** — Build a matrix mapping model families to operators, quantization needs, and runtime support. Hardness: medium. Stack: Python, ONNX, PyTorch, SQLite, Markdown. Resume bullet: Built an AI accelerator model-zoo readiness tool for compiler and SDK roadmap planning.",
            "- **Inference cost and latency benchmark dashboard** — Compare vLLM/TensorRT-LLM-style serving metrics across model sizes and batching assumptions. Hardness: medium-high. Stack: Python, FastAPI, SQLite, Streamlit or React. Resume bullet: Created an inference PM dashboard linking TTFT, throughput, memory, and cost per token to roadmap decisions.",
            f"- **Deep-dive teardown: {anchor}** — Turn one weekly item into a product memo with customer, metric, roadmap, and competitive implications. Hardness: low-medium. Stack: Markdown, notebooks, source links. Resume bullet: Produced source-backed AI infrastructure product strategy briefs for executive-style decision making.",
        ]

    def _linkedin_posts(self, ranked_items: list[RankedItem], synthesis: dict) -> list[str]:
        lines: list[str] = []
        posts = synthesis.get("linkedin_posts")
        if not isinstance(posts, list) or not posts:
            posts = self.linkedin_generator.generate(ranked_items)
        for post in posts:
            lines.extend([f"### Option {post['option']}: {post['title']}", "", post["draft"], ""])
        return lines

    def _interview_talking_points(self, ranked_items: list[RankedItem], summaries: dict[str, ItemSummary]) -> list[str]:
        if not ranked_items:
            return ["No interview talking points generated."]
        return [f"- **{entry.item.title}:** {summaries[entry.item.url].interview_talking_point}" for entry in ranked_items[:8]]

    def _deep_dive(
        self, ranked_items: list[RankedItem], summaries: dict[str, ItemSummary], synthesis: dict
    ) -> list[str]:
        entry = self._deep_dive_entry(ranked_items, synthesis)
        if entry is None:
            return ["No deep dive selected."]
        item = entry.item
        summary = summaries[item.url]
        llm_deep_dive = synthesis.get("deep_dive")
        if not isinstance(llm_deep_dive, dict):
            llm_deep_dive = {}
        why_this_one = llm_deep_dive.get("why_this_one") or llm_deep_dive.get("why_30_60_minutes")
        if not why_this_one:
            why_this_one = (
                f"It ranked highly this week. {summary.why_it_matters} "
                "Use it to practice converting a technical claim into a product decision."
            )
        benchmark = llm_deep_dive.get("benchmark_skepticism")
        if not isinstance(benchmark, dict):
            benchmark = {}
        baseline = benchmark.get("baseline_compared_against") or "______"
        hardware = benchmark.get("hardware_batch_size_seq_length") or "______"
        production = benchmark.get("production_survival_check") or "______"

        return [
            f"**Paper:** [{item.title} — {item.author or 'Unknown authors'}]({item.url})",
            f"**Why this one:** {why_this_one}",
            "",
            "### Reading protocol (20-30 min)",
            "- [ ] Pass 1 (3 min): Abstract + conclusion only. Kill question: does this touch inference cost, latency, quantization, serving, or dev workflow? If no, stop.",
            "- [ ] Pass 2 (10 min): Figures and tables only. Note the baseline, hardware, batch size, and sequence length behind the headline claim.",
            "- [ ] Pass 3 (10 min): Method section at mechanism level. Name the tradeoff (memory vs compute, accuracy vs latency, generality vs speed). Skip all derivations.",
            "",
            "### The extraction (fill this in — the deep dive is not done until this sentence is written)",
            "> This paper showed ______ under conditions ______.",
            "> This changes the ______ decision for ______ because ______.",
            "",
            "### Benchmark skepticism check",
            f"- Baseline compared against: {baseline}",
            f"- Hardware / batch size / seq length: {hardware}",
            f"- Would the claim survive production conditions (vLLM-class baseline, realistic batch sizes)? {production}",
        ]

    def _source_index(self, ranked_items: list[RankedItem]) -> list[str]:
        if not ranked_items:
            return ["No sources captured."]
        return [
            f"- {entry.item.title} — {entry.item.source} — {entry.item.url}"
            for entry in ranked_items
        ]

    def _dominant_dimensions(self, ranked_items: list[RankedItem]) -> list[str]:
        totals: dict[str, int] = defaultdict(int)
        for entry in ranked_items:
            for dimension, score in entry.score.dimensions.items():
                totals[dimension.replace("_", " ")] += score
        return [dimension for dimension, _ in sorted(totals.items(), key=lambda pair: pair[1], reverse=True)]

    def _focus_items(self, ranked_items: list[RankedItem]) -> list[RankedItem]:
        focus: list[RankedItem] = []
        desired_dimensions = [
            "ai_infrastructure_relevance",
            "compiler_runtime_quantization_relevance",
            "edge_automotive_industrial_relevance",
            "product_strategy_relevance",
        ]
        for entry in ranked_items:
            if len(focus) >= 5:
                break
            if entry.score.weighted_score >= 1.8 or any(
                entry.score.dimensions.get(dimension, 1) >= 4
                for dimension in desired_dimensions
            ):
                focus.append(entry)
        if len(focus) < 5:
            for entry in ranked_items:
                if entry not in focus:
                    focus.append(entry)
                if len(focus) >= 5:
                    break
        return focus

    def _focus_reason(self, entry: RankedItem) -> str:
        dimensions = entry.score.dimensions
        if dimensions.get("ai_infrastructure_relevance", 1) >= 4:
            return "Directly relevant to serving efficiency, scheduling, latency, throughput, utilization, or inference cost."
        if dimensions.get("compiler_runtime_quantization_relevance", 1) >= 4:
            return "Relevant to compiler/runtime/quantization roadmap and AI accelerator software completeness."
        if dimensions.get("edge_automotive_industrial_relevance", 1) >= 4:
            return "Strong fit for edge, automotive, industrial, or safety-constrained deployment thinking."
        if dimensions.get("product_strategy_relevance", 1) >= 4:
            return "Useful for developer-platform strategy, SDK adoption, roadmap sequencing, or product positioning."
        return "High overall score for this week's hardware-native AI PM filter."

    def _deep_dive_entry(self, ranked_items: list[RankedItem], synthesis: dict) -> RankedItem | None:
        llm_deep_dive = synthesis.get("deep_dive")
        if isinstance(llm_deep_dive, dict):
            url = llm_deep_dive.get("url")
            title = llm_deep_dive.get("title")
            for entry in ranked_items:
                if url and entry.item.url == url:
                    return entry
                if title and entry.item.title == title:
                    return entry
        for entry in ranked_items:
            if entry.item.category == "research_paper":
                return entry
        return ranked_items[0] if ranked_items else None


def _escape_table(value: str) -> str:
    return value.replace("|", "\\|").replace("\n", " ")
