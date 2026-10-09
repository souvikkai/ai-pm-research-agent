# Weekly AI PM Research Digest — 2026-10-09

Research publication window (inclusive, UTC): 2026-10-02T19:58:36.455706+00:00 to 2026-10-09T19:58:36.455706+00:00

## 1. Executive Summary

- 14 items met the hardware-native AI PM relevance threshold.
- Highest-scoring themes: ai infrastructure relevance, product strategy relevance, linkedin portfolio potential, compiler runtime quantization relevance.
- Prioritize items that change SDK roadmap, compiler support, serving cost, edge deployment confidence, or AI accelerator adoption.
- Add extra attention to GPU acceleration and AI-native engineering software when they connect to real workloads, metrics, trust, and customer adoption.
- Treat consumer AI news as signal only when it changes infrastructure, deployment, developer-platform, or enterprise product decisions.
- Use the top items to prepare interview stories around metrics, tradeoffs, roadmap sequencing, and customer constraints.
- Deep-dive candidate: TokenRouter: Efficient Serving System for Token-Level LLM Routing.

## 2. Strategic Synthesis

- DeepSeek synthesis was enabled but failed: `JSONDecodeError: Expecting value: line 1 column 1 (char 0)`
- The report below uses deterministic fallback content.

## 3. Must-Focus Items This Week

Read these first. They are the highest-value items for AI infrastructure PM interview prep, product judgment, or hardware-native roadmap thinking.

### Focus 1: TokenRouter: Efficient Serving System for Token-Level LLM Routing

- **Source:** arXiv cs.CL
- **Publication date:** 2026-10-08
- **Link:** https://arxiv.org/abs/2610.12242v1
- **Score:** 2.23/5
- **Why this is high value:** Directly relevant to serving efficiency, scheduling, latency, throughput, utilization, or inference cost.
- **Strategic relevance to Souvik's role:** Use this as broader AI infra signal: serving cost, latency, utilization, reliability, or platform adoption.
- **What to extract:** Decide whether serving-stack work should target latency, throughput, cost per token, autoscaling, or reliability first.
- **Interview angle:** Use this to discuss how an AI PM evaluates datacenter through customer impact, measurable infra metrics, and roadmap tradeoffs.

### Focus 2: Long Text to Predictive Features: LLM-Guided Blockwise Feature Engineering via Executable Program Search

- **Source:** arXiv cs.CL
- **Publication date:** 2026-10-08
- **Link:** https://arxiv.org/abs/2610.12390v1
- **Score:** 1.91/5
- **Why this is high value:** High overall score for this week's hardware-native AI PM filter.
- **Strategic relevance to Souvik's role:** Use this as broader AI infra signal: serving cost, latency, utilization, reliability, or platform adoption.
- **What to extract:** Decide which edge demos, reference designs, and deployment constraints deserve roadmap priority.
- **Interview angle:** Use this to discuss how an AI PM evaluates edge through customer impact, measurable infra metrics, and roadmap tradeoffs.

### Focus 3: SparseDecoding: Decoding-Aware Pruning for Accurate and Efficient LLM Inference

- **Source:** arXiv cs.CL
- **Publication date:** 2026-10-08
- **Link:** https://arxiv.org/abs/2610.12327v1
- **Score:** 1.87/5
- **Why this is high value:** Directly relevant to serving efficiency, scheduling, latency, throughput, utilization, or inference cost.
- **Strategic relevance to Souvik's role:** Use this as broader AI infra signal: serving cost, latency, utilization, reliability, or platform adoption.
- **What to extract:** Prioritize compiler/runtime coverage, framework integrations, and model zoo proof points for the affected workloads.
- **Interview angle:** Use this to discuss how an AI PM evaluates compiler, datacenter, agents through customer impact, measurable infra metrics, and roadmap tradeoffs.

### Focus 4: Claude Haiku 5.5

- **Source:** Simon Willison
- **Publication date:** 2026-10-07
- **Link:** https://simonwillison.net/2026/Oct/7/claude-haiku-5-5/
- **Score:** 1.87/5
- **Why this is high value:** High overall score for this week's hardware-native AI PM filter.
- **Strategic relevance to Souvik's role:** Use this as broader AI infra signal: serving cost, latency, utilization, reliability, or platform adoption.
- **What to extract:** Decide whether this is a roadmap input, interview talking point, LinkedIn idea, or background reading.
- **Interview angle:** Use this to show disciplined judgment: what changed, why it matters, and what product metric would prove it mattered.

### Focus 5: VFold: Symmetry-Aware Cross-Layer Value Cache Compression

- **Source:** arXiv cs.CL
- **Publication date:** 2026-10-08
- **Link:** https://arxiv.org/abs/2610.12338v1
- **Score:** 1.83/5
- **Why this is high value:** High overall score for this week's hardware-native AI PM filter.
- **Strategic relevance to Souvik's role:** Use this as broader AI infra signal: serving cost, latency, utilization, reliability, or platform adoption.
- **What to extract:** Decide whether to support a datatype or quantization path in the SDK, benchmarks, docs, and customer enablement.
- **Interview angle:** Use this to discuss how an AI PM evaluates quantization, agents through customer impact, measurable infra metrics, and roadmap tradeoffs.


## 4. Top 10 Ranked Briefing

| Rank | Item | Publication Date | Category | Score | Why It Matters |
|---:|---|---|---|---:|---|
| 1 | [TokenRouter: Efficient Serving System for Token-Level LLM Routing](https://arxiv.org/abs/2610.12242v1) | 2026-10-08 | research_paper | 2.23/5 | Large language model (LLM) routing distributes inference work across different models, advancing the cost-quality Pareto frontier of LLM serving. While coarse-grained routing at the session or query level has been widel... |
| 2 | [Long Text to Predictive Features: LLM-Guided Blockwise Feature Engineering via Executable Program Search](https://arxiv.org/abs/2610.12390v1) | 2026-10-08 | research_paper | 1.91/5 | Industrial risk-control systems typically rely on structured-data models for efficient prediction, yet substantial valuable information remains embedded in unstructured long text. Extracting this information through man... |
| 3 | [SparseDecoding: Decoding-Aware Pruning for Accurate and Efficient LLM Inference](https://arxiv.org/abs/2610.12327v1) | 2026-10-08 | research_paper | 1.87/5 | The memory-bound nature of the decoding stage of large language model (LLM) inference incurs significant latency. Layer-wise training-free network pruning approaches guided by the Hessian have been a prominent solution... |
| 4 | [Claude Haiku 5.5](https://simonwillison.net/2026/Oct/7/claude-haiku-5-5/) | 2026-10-07 | builder_blog | 1.87/5 | As previously promised , here's Anthropic's new fast, low cost model: Introducing Claude Haiku 5.5 . The previous Haiku, 4.5, was very much showing its age. It came out almost a year ago , and was priced at $1/million i... |
| 5 | [VFold: Symmetry-Aware Cross-Layer Value Cache Compression](https://arxiv.org/abs/2610.12338v1) | 2026-10-08 | research_paper | 1.83/5 | While caching key-value (KV) states accelerates Large Language Model (LLM) decoding, this cache can dominate memory usage at long context lengths. One solution is to compress this memory by exploiting inter-layer cache... |
| 6 | [When Lower Reconstruction Loss Hurts: Distributionally Robust Refinement for Low-Bit LLM Quantization](https://arxiv.org/abs/2610.11226v1) | 2026-10-08 | research_paper | 1.74/5 | Weight-only post-training quantization (PTQ) relies heavily on reconstruction loss minimization to preserve model quality at low precision. We show that the weights favored by minimizing this loss need not yield better... |
| 7 | [Batch Before You Lift: Scalable Topological Deep Learning on Large Graphs](https://arxiv.org/abs/2610.12247v1) | 2026-10-08 | research_paper | 1.73/5 | Topological Deep Learning extends graph-based learning to higher-order domains, such as hypergraphs, cellular, and simplicial complexes. These domains are typically constructed from patterns in an input graph through a... |
| 8 | [Distilling Routed 3D Privilege for Spatial Reasoning in Vision-Language Models](https://arxiv.org/abs/2610.12355v1) | 2026-10-08 | research_paper | 1.63/5 | Spatial reasoning remains a persistent weakness of vision-language models (VLMs), because RGB inputs do not directly provide geometric evidence. Existing remedies either inject 3D into the model at inference, paying arc... |
| 9 | [Caught in the Act: Probes Effectively Detect Sabotage and Catch Unverbalized Deception](https://arxiv.org/abs/2610.12445v1) | 2026-10-08 | research_paper | 1.62/5 | Recent incidents have highlighted the challenge of monitoring LLM agents and the danger of models deceiving people. We show that white-box deception detection via probes can be scaled up to frontier monitoring settings... |
| 10 | [SPD-MetaFormer is what you need for small-data brain decoding](https://arxiv.org/abs/2610.10952v1) | 2026-10-07 | research_paper | 1.62/5 | Brain signal decoding is challenging because neural recordings are noisy and vary across individuals, while labeled data are often limited. Recent attention-based models on the symmetric positive definite (SPD) manifold... |

## 5. Theme Map

### Graph Compilers, Runtime, and SDK Platform
- **#1 TokenRouter: Efficient Serving System for Token-Level LLM Routing** — score 2.23/5; source: arXiv cs.CL; link: https://arxiv.org/abs/2610.12242v1
- **#7 Batch Before You Lift: Scalable Topological Deep Learning on Large Graphs** — score 1.73/5; source: arXiv cs.LG; link: https://arxiv.org/abs/2610.12247v1

### Quantization, Numerics, and Model Compression
- **#5 VFold: Symmetry-Aware Cross-Layer Value Cache Compression** — score 1.83/5; source: arXiv cs.CL; link: https://arxiv.org/abs/2610.12338v1
- **#6 When Lower Reconstruction Loss Hurts: Distributionally Robust Refinement for Low-Bit LLM Quantization** — score 1.74/5; source: arXiv stat.ML; link: https://arxiv.org/abs/2610.11226v1

### Edge, Automotive, and Industrial AI
- **#2 Long Text to Predictive Features: LLM-Guided Blockwise Feature Engineering via Executable Program Search** — score 1.91/5; source: arXiv cs.CL; link: https://arxiv.org/abs/2610.12390v1
- **#12 VersaCamVLA: Camera-Configurable VLA Policies for Robotic Manipulation** — score 1.5/5; source: arXiv cs.CV; link: https://arxiv.org/abs/2610.12451v1

### Datacenter AI Infrastructure and Serving
- **#1 TokenRouter: Efficient Serving System for Token-Level LLM Routing** — score 2.23/5; source: arXiv cs.CL; link: https://arxiv.org/abs/2610.12242v1
- **#3 SparseDecoding: Decoding-Aware Pruning for Accurate and Efficient LLM Inference** — score 1.87/5; source: arXiv cs.CL; link: https://arxiv.org/abs/2610.12327v1
- **#7 Batch Before You Lift: Scalable Topological Deep Learning on Large Graphs** — score 1.73/5; source: arXiv cs.LG; link: https://arxiv.org/abs/2610.12247v1
- **#8 Distilling Routed 3D Privilege for Spatial Reasoning in Vision-Language Models** — score 1.63/5; source: arXiv cs.AI; link: https://arxiv.org/abs/2610.12355v1
- **#11 OnTrack: Real-Time Monitoring and Intervention in LLM Agent Trajectories via Streaming Structure-Aware Optimal Transport** — score 1.56/5; source: arXiv cs.AI; link: https://arxiv.org/abs/2610.12375v1

### GPU Acceleration and Technical Computing
- No high-signal item in this theme this week.

### AI for Engineering Software Workflows
- No high-signal item in this theme this week.

### Agents, RAG, Evals, and Safety
- **#3 SparseDecoding: Decoding-Aware Pruning for Accurate and Efficient LLM Inference** — score 1.87/5; source: arXiv cs.CL; link: https://arxiv.org/abs/2610.12327v1
- **#5 VFold: Symmetry-Aware Cross-Layer Value Cache Compression** — score 1.83/5; source: arXiv cs.CL; link: https://arxiv.org/abs/2610.12338v1
- **#7 Batch Before You Lift: Scalable Topological Deep Learning on Large Graphs** — score 1.73/5; source: arXiv cs.LG; link: https://arxiv.org/abs/2610.12247v1
- **#9 Caught in the Act: Probes Effectively Detect Sabotage and Catch Unverbalized Deception** — score 1.62/5; source: arXiv cs.AI; link: https://arxiv.org/abs/2610.12445v1
- **#10 SPD-MetaFormer is what you need for small-data brain decoding** — score 1.62/5; source: arXiv stat.ML; link: https://arxiv.org/abs/2610.10952v1


## 6. Research Papers Reading Queue

| Priority | Paper | Action | PM Reason |
|---:|---|---|---|
| 1 | [TokenRouter: Efficient Serving System for Token-Level LLM Routing](https://arxiv.org/abs/2610.12242v1) | Read full paper | A PM should translate the update into cost per token, TTFT, throughput, utilization, reliability, and operational simplicity. |
| 2 | [Long Text to Predictive Features: LLM-Guided Blockwise Feature Engineering via Executable Program Search](https://arxiv.org/abs/2610.12390v1) | Read full paper | A PM should frame the implication around deployment constraints: power, thermals, memory, latency, safety, and customer integration effort. |
| 3 | [SparseDecoding: Decoding-Aware Pruning for Accurate and Efficient LLM Inference](https://arxiv.org/abs/2610.12327v1) | Read full paper | A PM should ask whether the SDK, compiler support matrix, docs, and customer demos cover the model patterns developers now expect. |
| 5 | [VFold: Symmetry-Aware Cross-Layer Value Cache Compression](https://arxiv.org/abs/2610.12338v1) | Read full paper | A PM should connect accuracy, latency, memory, and hardware support before treating the update as roadmap-ready. |
| 6 | [When Lower Reconstruction Loss Hurts: Distributionally Robust Refinement for Low-Bit LLM Quantization](https://arxiv.org/abs/2610.11226v1) | Skim | A PM should connect accuracy, latency, memory, and hardware support before treating the update as roadmap-ready. |
| 7 | [Batch Before You Lift: Scalable Topological Deep Learning on Large Graphs](https://arxiv.org/abs/2610.12247v1) | Skim | A PM should translate the update into cost per token, TTFT, throughput, utilization, reliability, and operational simplicity. |
| 8 | [Distilling Routed 3D Privilege for Spatial Reasoning in Vision-Language Models](https://arxiv.org/abs/2610.12355v1) | Skim | A PM should translate the update into cost per token, TTFT, throughput, utilization, reliability, and operational simplicity. |
| 9 | [Caught in the Act: Probes Effectively Detect Sabotage and Catch Unverbalized Deception](https://arxiv.org/abs/2610.12445v1) | Skim | A PM should identify what customer workflow, roadmap bet, or competitive positioning this update could change. |
| 10 | [SPD-MetaFormer is what you need for small-data brain decoding](https://arxiv.org/abs/2610.10952v1) | Skim | A PM should identify what customer workflow, roadmap bet, or competitive positioning this update could change. |
| 11 | [OnTrack: Real-Time Monitoring and Intervention in LLM Agent Trajectories via Streaming Structure-Aware Optimal Transport](https://arxiv.org/abs/2610.12375v1) | Skim | A PM should frame the implication around deployment constraints: power, thermals, memory, latency, safety, and customer integration effort. |

## 7. Big Tech, AI Lab, and Competitive Watch

### Google / DeepMind
- No high-signal tracked item this week.

### Meta
- No high-signal tracked item this week.

### Amazon / AWS
- No high-signal tracked item this week.

### Microsoft
- No high-signal tracked item this week.

### Apple
- No high-signal tracked item this week.

### OpenAI
- [Claude Haiku 5.5](https://simonwillison.net/2026/Oct/7/claude-haiku-5-5/) — score 1.87/5

### Anthropic
- [Claude Haiku 5.5](https://simonwillison.net/2026/Oct/7/claude-haiku-5-5/) — score 1.87/5

### NVIDIA
- No high-signal tracked item this week.


### AI Accelerator and Developer Platform Competitive Intelligence

No competitive-intelligence items crossed the threshold this week.

## 8. Model Zoo Watch

- **TokenRouter: Efficient Serving System for Token-Level LLM Routing** — ask what operators, graph patterns, quantization support, and demo value this model family stresses. https://arxiv.org/abs/2610.12242v1
- **Long Text to Predictive Features: LLM-Guided Blockwise Feature Engineering via Executable Program Search** — ask what operators, graph patterns, quantization support, and demo value this model family stresses. https://arxiv.org/abs/2610.12390v1
- **SparseDecoding: Decoding-Aware Pruning for Accurate and Efficient LLM Inference** — ask what operators, graph patterns, quantization support, and demo value this model family stresses. https://arxiv.org/abs/2610.12327v1
- **Claude Haiku 5.5** — ask what operators, graph patterns, quantization support, and demo value this model family stresses. https://simonwillison.net/2026/Oct/7/claude-haiku-5-5/
- **VFold: Symmetry-Aware Cross-Layer Value Cache Compression** — ask what operators, graph patterns, quantization support, and demo value this model family stresses. https://arxiv.org/abs/2610.12338v1
- **When Lower Reconstruction Loss Hurts: Distributionally Robust Refinement for Low-Bit LLM Quantization** — ask what operators, graph patterns, quantization support, and demo value this model family stresses. https://arxiv.org/abs/2610.11226v1
- **Distilling Routed 3D Privilege for Spatial Reasoning in Vision-Language Models** — ask what operators, graph patterns, quantization support, and demo value this model family stresses. https://arxiv.org/abs/2610.12355v1
- **Caught in the Act: Probes Effectively Detect Sabotage and Catch Unverbalized Deception** — ask what operators, graph patterns, quantization support, and demo value this model family stresses. https://arxiv.org/abs/2610.12445v1

## 9. Portfolio Project Ideas

- **Compiler support matrix for edge AI models** — Build a matrix mapping model families to operators, quantization needs, and runtime support. Hardness: medium. Stack: Python, ONNX, PyTorch, SQLite, Markdown. Resume bullet: Built an AI accelerator model-zoo readiness tool for compiler and SDK roadmap planning.
- **Inference cost and latency benchmark dashboard** — Compare vLLM/TensorRT-LLM-style serving metrics across model sizes and batching assumptions. Hardness: medium-high. Stack: Python, FastAPI, SQLite, Streamlit or React. Resume bullet: Created an inference PM dashboard linking TTFT, throughput, memory, and cost per token to roadmap decisions.
- **Deep-dive teardown: TokenRouter: Efficient Serving System for Token-Level LLM Routing** — Turn one weekly item into a product memo with customer, metric, roadmap, and competitive implications. Hardness: low-medium. Stack: Markdown, notebooks, source links. Resume bullet: Produced source-backed AI infrastructure product strategy briefs for executive-style decision making.

## 10. LinkedIn Post Ideas

### Option A: Broad weekly AI PM digest

This week's AI signal is less about novelty for its own sake and more about deployment judgment.

The items I would track as a hardware-native AI PM are the ones that connect model capability to serving cost, runtime maturity, developer adoption, and customer confidence.

My filter: what changes a roadmap decision, an SDK priority, or an infra metric?

Note: Use the completed deep-dive extraction sentence as the seed for the final post.

Sources:
- TokenRouter: Efficient Serving System for Token-Level LLM Routing: https://arxiv.org/abs/2610.12242v1
- Long Text to Predictive Features: LLM-Guided Blockwise Feature Engineering via Executable Program Search: https://arxiv.org/abs/2610.12390v1
- SparseDecoding: Decoding-Aware Pruning for Accurate and Efficient LLM Inference: https://arxiv.org/abs/2610.12327v1
- Claude Haiku 5.5: https://simonwillison.net/2026/Oct/7/claude-haiku-5-5/

### Option B: Deep dive on one research paper or technical blog

One item worth a deeper look this week: TokenRouter: Efficient Serving System for Token-Level LLM Routing.

The product question is not just whether the technique is technically impressive. It is whether it changes latency, memory, cost, reliability, or developer experience enough to affect a real deployment decision.

The PM move is to ask: what metric would prove this matters, and what customer workload would expose the tradeoff?

Note: Use the completed deep-dive extraction sentence as the seed for the final post.

Source: https://arxiv.org/abs/2610.12242v1

### Option C: Hardware-native AI PM angle

AI product strategy is increasingly constrained by the physical stack: silicon, memory bandwidth, compiler support, runtime scheduling, and serving economics.

That is the opportunity for hardware-native PMs. The best roadmap decisions connect customer-facing capability to what the hardware and software stack can actually sustain in production.

Source-backed items:
- TokenRouter: Efficient Serving System for Token-Level LLM Routing: https://arxiv.org/abs/2610.12242v1
- Long Text to Predictive Features: LLM-Guided Blockwise Feature Engineering via Executable Program Search: https://arxiv.org/abs/2610.12390v1
- SparseDecoding: Decoding-Aware Pruning for Accurate and Efficient LLM Inference: https://arxiv.org/abs/2610.12327v1
- Claude Haiku 5.5: https://simonwillison.net/2026/Oct/7/claude-haiku-5-5/

Note: Use the completed deep-dive extraction sentence as the seed for the final post.

### Option D: Compiler / GPU / engineering AI angle

Compiler, GPU, and engineering-AI work can look like implementation detail until you view it through customer workflow adoption.

Operator coverage, acceleration portability, model zoo completeness, traceability, and benchmark quality all shape developer confidence. A missing graph pattern, weak GPU path, or untrusted AI assistant can become a product adoption blocker.

The PM question: which workloads should become forcing functions for platform completeness, customer demos, and roadmap proof?

Note: Use the completed deep-dive extraction sentence as the seed for the final post.

Sources:
- TokenRouter: Efficient Serving System for Token-Level LLM Routing: https://arxiv.org/abs/2610.12242v1
- Long Text to Predictive Features: LLM-Guided Blockwise Feature Engineering via Executable Program Search: https://arxiv.org/abs/2610.12390v1
- SparseDecoding: Decoding-Aware Pruning for Accurate and Efficient LLM Inference: https://arxiv.org/abs/2610.12327v1
- Claude Haiku 5.5: https://simonwillison.net/2026/Oct/7/claude-haiku-5-5/


## 11. Interview Talking Points

- **TokenRouter: Efficient Serving System for Token-Level LLM Routing:** Use this to discuss how an AI PM evaluates datacenter through customer impact, measurable infra metrics, and roadmap tradeoffs.
- **Long Text to Predictive Features: LLM-Guided Blockwise Feature Engineering via Executable Program Search:** Use this to discuss how an AI PM evaluates edge through customer impact, measurable infra metrics, and roadmap tradeoffs.
- **SparseDecoding: Decoding-Aware Pruning for Accurate and Efficient LLM Inference:** Use this to discuss how an AI PM evaluates compiler, datacenter, agents through customer impact, measurable infra metrics, and roadmap tradeoffs.
- **Claude Haiku 5.5:** Use this to show disciplined judgment: what changed, why it matters, and what product metric would prove it mattered.
- **VFold: Symmetry-Aware Cross-Layer Value Cache Compression:** Use this to discuss how an AI PM evaluates quantization, agents through customer impact, measurable infra metrics, and roadmap tradeoffs.
- **When Lower Reconstruction Loss Hurts: Distributionally Robust Refinement for Low-Bit LLM Quantization:** Use this to discuss how an AI PM evaluates quantization through customer impact, measurable infra metrics, and roadmap tradeoffs.
- **Batch Before You Lift: Scalable Topological Deep Learning on Large Graphs:** Use this to discuss how an AI PM evaluates datacenter, agents through customer impact, measurable infra metrics, and roadmap tradeoffs.
- **Distilling Routed 3D Privilege for Spatial Reasoning in Vision-Language Models:** Use this to discuss how an AI PM evaluates datacenter through customer impact, measurable infra metrics, and roadmap tradeoffs.

## Recommended Deep Dive of the Week

**Paper:** [TokenRouter: Efficient Serving System for Token-Level LLM Routing — Tianyu Fu, Tengxuan Liu, Ruoxi Wang, Yixin Dong, Yi Ge, Yichen You, Yu Wang](https://arxiv.org/abs/2610.12242v1)
**Why this one:** It ranked highly this week. It ranks highly on ai infrastructure relevance, which makes it useful for separating infrastructure signal from general AI noise. Use it to practice converting a technical claim into a product decision.

### Reading protocol (20-30 min)
- [ ] Pass 1 (3 min): Abstract + conclusion only. Kill question: does this touch inference cost, latency, quantization, serving, or dev workflow? If no, stop.
- [ ] Pass 2 (10 min): Figures and tables only. Note the baseline, hardware, batch size, and sequence length behind the headline claim.
- [ ] Pass 3 (10 min): Method section at mechanism level. Name the tradeoff (memory vs compute, accuracy vs latency, generality vs speed). Skip all derivations.

### The extraction (fill this in — the deep dive is not done until this sentence is written)
> This paper showed ______ under conditions ______.
> This changes the ______ decision for ______ because ______.

### Benchmark skepticism check
- Baseline compared against: ______
- Hardware / batch size / seq length: ______
- Would the claim survive production conditions (vLLM-class baseline, realistic batch sizes)? ______

## 13. Source Index

- TokenRouter: Efficient Serving System for Token-Level LLM Routing — arXiv cs.CL — https://arxiv.org/abs/2610.12242v1
- Long Text to Predictive Features: LLM-Guided Blockwise Feature Engineering via Executable Program Search — arXiv cs.CL — https://arxiv.org/abs/2610.12390v1
- SparseDecoding: Decoding-Aware Pruning for Accurate and Efficient LLM Inference — arXiv cs.CL — https://arxiv.org/abs/2610.12327v1
- Claude Haiku 5.5 — Simon Willison — https://simonwillison.net/2026/Oct/7/claude-haiku-5-5/
- VFold: Symmetry-Aware Cross-Layer Value Cache Compression — arXiv cs.CL — https://arxiv.org/abs/2610.12338v1
- When Lower Reconstruction Loss Hurts: Distributionally Robust Refinement for Low-Bit LLM Quantization — arXiv stat.ML — https://arxiv.org/abs/2610.11226v1
- Batch Before You Lift: Scalable Topological Deep Learning on Large Graphs — arXiv cs.LG — https://arxiv.org/abs/2610.12247v1
- Distilling Routed 3D Privilege for Spatial Reasoning in Vision-Language Models — arXiv cs.AI — https://arxiv.org/abs/2610.12355v1
- Caught in the Act: Probes Effectively Detect Sabotage and Catch Unverbalized Deception — arXiv cs.AI — https://arxiv.org/abs/2610.12445v1
- SPD-MetaFormer is what you need for small-data brain decoding — arXiv stat.ML — https://arxiv.org/abs/2610.10952v1
- OnTrack: Real-Time Monitoring and Intervention in LLM Agent Trajectories via Streaming Structure-Aware Optimal Transport — arXiv cs.AI — https://arxiv.org/abs/2610.12375v1
- VersaCamVLA: Camera-Configurable VLA Policies for Robotic Manipulation — arXiv cs.CV — https://arxiv.org/abs/2610.12451v1
- Training Parallel Speculative Draft Models by Directly Minimizing Expected Decoding Rounds — arXiv stat.ML — https://arxiv.org/abs/2610.10411v1
- Language Models as AI Research World Models — arXiv cs.CL — https://arxiv.org/abs/2610.12235v1
