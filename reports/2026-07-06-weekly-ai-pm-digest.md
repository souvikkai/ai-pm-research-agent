# Weekly AI PM Research Digest — 2026-07-06

## 1. Executive Summary

- 20 items met the hardware-native AI PM relevance threshold.
- Highest-scoring themes: ai infrastructure relevance, edge automotive industrial relevance, product strategy relevance, big tech accelerator relevance.
- Prioritize items that change SDK roadmap, compiler support, serving cost, edge deployment confidence, or AI accelerator adoption.
- Treat consumer AI news as signal only when it changes infrastructure, deployment, developer-platform, or enterprise product decisions.
- Use the top items to prepare interview stories around metrics, tradeoffs, roadmap sequencing, and customer constraints.
- Deep-dive candidate: Adaptive Inference Batching using Policy Gradients.

## 2. Must-Focus Items This Week

Read these first. They are the highest-value items for AI infrastructure PM interview prep, product judgment, or hardware-native roadmap thinking.

### Focus 1: Adaptive Inference Batching using Policy Gradients

- **Source:** arXiv cs.AI
- **Link:** https://arxiv.org/abs/2607.05272v1
- **Score:** 2.1/5
- **Why this is high value:** Directly relevant to serving efficiency, scheduling, latency, throughput, utilization, or inference cost.
- **What to extract:** Decide whether serving-stack work should target latency, throughput, cost per token, autoscaling, or reliability first.
- **Interview angle:** Use this to discuss how an AI PM evaluates datacenter, agents through customer impact, measurable infra metrics, and roadmap tradeoffs.

### Focus 2: When Words Predict Workload

- **Source:** arXiv cs.CL
- **Link:** https://arxiv.org/abs/2607.04951v1
- **Score:** 2.1/5
- **Why this is high value:** Directly relevant to serving efficiency, scheduling, latency, throughput, utilization, or inference cost.
- **What to extract:** Decide which edge demos, reference designs, and deployment constraints deserve roadmap priority.
- **Interview angle:** Use this to discuss how an AI PM evaluates edge, datacenter, agents through customer impact, measurable infra metrics, and roadmap tradeoffs.

### Focus 3: DSpark: Confidence-Scheduled Speculative Decoding with Semi-Autoregressive Generation

- **Source:** arXiv cs.CL
- **Link:** https://arxiv.org/abs/2607.05147v1
- **Score:** 2.0/5
- **Why this is high value:** Directly relevant to serving efficiency, scheduling, latency, throughput, utilization, or inference cost.
- **What to extract:** Decide whether serving-stack work should target latency, throughput, cost per token, autoscaling, or reliability first.
- **Interview angle:** Use this to discuss how an AI PM evaluates datacenter through customer impact, measurable infra metrics, and roadmap tradeoffs.

### Focus 4: What's new in Claude Sonnet 5

- **Source:** Simon Willison
- **Link:** https://simonwillison.net/2026/Jun/30/claude-sonnet-5/#atom-everything
- **Score:** 1.95/5
- **Why this is high value:** Useful for developer-platform strategy, SDK adoption, roadmap sequencing, or product positioning.
- **What to extract:** Decide whether this is a roadmap input, interview talking point, LinkedIn idea, or background reading.
- **Interview angle:** Use this to show disciplined judgment: what changed, why it matters, and what product metric would prove it mattered.

### Focus 5: LLM-as-a-Verifier: A General-Purpose Verification Framework

- **Source:** arXiv cs.AI
- **Link:** https://arxiv.org/abs/2607.05391v1
- **Score:** 1.85/5
- **Why this is high value:** High overall score for this week's hardware-native AI PM filter.
- **What to extract:** Decide which edge demos, reference designs, and deployment constraints deserve roadmap priority.
- **Interview angle:** Use this to discuss how an AI PM evaluates edge through customer impact, measurable infra metrics, and roadmap tradeoffs.


## 3. Top 10 Ranked Briefing

| Rank | Item | Category | Score | Why It Matters |
|---:|---|---|---:|---|
| 1 | [Adaptive Inference Batching using Policy Gradients](https://arxiv.org/abs/2607.05272v1) | research_paper | 2.1/5 | Inference serving systems must balance throughput and latency under bursty, heterogeneous workloads, yet the industry standard remains static batching policies that require manual tuning and cannot adapt to shifting tra... |
| 2 | [When Words Predict Workload](https://arxiv.org/abs/2607.04951v1) | research_paper | 2.1/5 | Standard distributed \ac{llm} schedulers rely on static token counts or rolling latency averages, making them susceptible to failures on statutorily constrained text. On \ac{epo} claims governed by Article 84 \ac{epc},... |
| 3 | [DSpark: Confidence-Scheduled Speculative Decoding with Semi-Autoregressive Generation](https://arxiv.org/abs/2607.05147v1) | research_paper | 2.0/5 | Speculative decoding accelerates Large Language Model (LLM) inference by decoupling draft generation from target verification. While recent parallel drafters efficiently propose long token sequences in a single forward... |
| 4 | [What's new in Claude Sonnet 5](https://simonwillison.net/2026/Jun/30/claude-sonnet-5/#atom-everything) | builder_blog | 1.95/5 | What's new in Claude Sonnet 5 Claude Sonnet 5 came out this morning . I always head straight for the "what's new" developer docs because they tend to have more actionable information than the official announcement post.... |
| 5 | [LLM-as-a-Verifier: A General-Purpose Verification Framework](https://arxiv.org/abs/2607.05391v1) | research_paper | 1.85/5 | Scaling pre-training, post-training, and test-time compute have become the central paradigms for improving the capabilities of LLMs. In this work, we identify verification, the ability to determine the correctness of a... |
| 6 | [Optimizing ML Workload Partitioning between CPUs and CIM Accelerators for Heterogeneous Computing](https://arxiv.org/abs/2607.05240v1) | research_paper | 1.85/5 | Computing-in-Memory (CIM) accelerators execute Matrix-Vector Multiplications (MVMs) in memory, making them a compelling solution for Machine Learning (ML) workloads. However, existing ML workload partitioning approaches... |
| 7 | [An event-driven framework for fly-inspired visual motion detection](https://arxiv.org/abs/2607.05205v1) | research_paper | 1.85/5 | Fast and reliable motion detection is essential for machine vision and autonomous systems operating in dynamic environments. This work integrates emerging event-based sensing with biologically structured neural computat... |
| 8 | [Multiplayer Interactive World Models with Representation Autoencoders](https://arxiv.org/abs/2607.05352v1) | research_paper | 1.7/5 | We introduce the first multiplayer world model for highly dynamic environments governed by complex physical interactions. Whereas single-player world models treat the other agents as part of the environment, ours condit... |
| 9 | [Unified Audio Intelligence Without Regressing on Text Intelligence](https://arxiv.org/abs/2607.05196v1) | research_paper | 1.7/5 | Audio intelligence involves understanding, reasoning about, and generating both audio and speech. In this work, we introduce Nemotron-Labs-Audex-30B-A3B (Audex), a unified audio-text LLM built on Nemotron-Cascade-2-30B-... |
| 10 | [UNIVERSE: Unified Video Action Models for Autonomous Driving with Flexible Mask-Modulated Modality Generation](https://arxiv.org/abs/2607.05133v1) | research_paper | 1.65/5 | World Action Models (WAMs) have shown strong potential for improving action generalization in autonomous driving by using future video prediction as dense supervision for scene dynamics and temporal causality. However,... |

## 4. Theme Map

### Graph Compilers, Runtime, and SDK Platform
- No high-signal item in this theme this week.

### Quantization, Numerics, and Model Compression
- **#9 Unified Audio Intelligence Without Regressing on Text Intelligence** — score 1.7/5; source: arXiv cs.CL; link: https://arxiv.org/abs/2607.05196v1

### Edge, Automotive, and Industrial AI
- **#2 When Words Predict Workload** — score 2.1/5; source: arXiv cs.CL; link: https://arxiv.org/abs/2607.04951v1
- **#5 LLM-as-a-Verifier: A General-Purpose Verification Framework** — score 1.85/5; source: arXiv cs.AI; link: https://arxiv.org/abs/2607.05391v1
- **#6 Optimizing ML Workload Partitioning between CPUs and CIM Accelerators for Heterogeneous Computing** — score 1.85/5; source: arXiv cs.AI; link: https://arxiv.org/abs/2607.05240v1
- **#7 An event-driven framework for fly-inspired visual motion detection** — score 1.85/5; source: arXiv cs.CV; link: https://arxiv.org/abs/2607.05205v1
- **#11 GaP: A Graph-as-Policy Multi-Agent Self-Learning Harness For Variational Automation Tasks** — score 1.6/5; source: arXiv cs.AI; link: https://arxiv.org/abs/2607.05369v1

### Datacenter AI Infrastructure and Serving
- **#1 Adaptive Inference Batching using Policy Gradients** — score 2.1/5; source: arXiv cs.AI; link: https://arxiv.org/abs/2607.05272v1
- **#2 When Words Predict Workload** — score 2.1/5; source: arXiv cs.CL; link: https://arxiv.org/abs/2607.04951v1
- **#3 DSpark: Confidence-Scheduled Speculative Decoding with Semi-Autoregressive Generation** — score 2.0/5; source: arXiv cs.CL; link: https://arxiv.org/abs/2607.05147v1
- **#6 Optimizing ML Workload Partitioning between CPUs and CIM Accelerators for Heterogeneous Computing** — score 1.85/5; source: arXiv cs.AI; link: https://arxiv.org/abs/2607.05240v1
- **#7 An event-driven framework for fly-inspired visual motion detection** — score 1.85/5; source: arXiv cs.CV; link: https://arxiv.org/abs/2607.05205v1

### Agents, RAG, Evals, and Safety
- **#1 Adaptive Inference Batching using Policy Gradients** — score 2.1/5; source: arXiv cs.AI; link: https://arxiv.org/abs/2607.05272v1
- **#2 When Words Predict Workload** — score 2.1/5; source: arXiv cs.CL; link: https://arxiv.org/abs/2607.04951v1
- **#5 LLM-as-a-Verifier: A General-Purpose Verification Framework** — score 1.85/5; source: arXiv cs.AI; link: https://arxiv.org/abs/2607.05391v1
- **#6 Optimizing ML Workload Partitioning between CPUs and CIM Accelerators for Heterogeneous Computing** — score 1.85/5; source: arXiv cs.AI; link: https://arxiv.org/abs/2607.05240v1
- **#8 Multiplayer Interactive World Models with Representation Autoencoders** — score 1.7/5; source: arXiv cs.AI; link: https://arxiv.org/abs/2607.05352v1


## 5. Research Papers Reading Queue

| Priority | Paper | Action | PM Reason |
|---:|---|---|---|
| 1 | [Adaptive Inference Batching using Policy Gradients](https://arxiv.org/abs/2607.05272v1) | Read full paper | A PM should translate the update into cost per token, TTFT, throughput, utilization, reliability, and operational simplicity. |
| 2 | [When Words Predict Workload](https://arxiv.org/abs/2607.04951v1) | Read full paper | A PM should frame the implication around deployment constraints: power, thermals, memory, latency, safety, and customer integration effort. |
| 3 | [DSpark: Confidence-Scheduled Speculative Decoding with Semi-Autoregressive Generation](https://arxiv.org/abs/2607.05147v1) | Read full paper | A PM should translate the update into cost per token, TTFT, throughput, utilization, reliability, and operational simplicity. |
| 5 | [LLM-as-a-Verifier: A General-Purpose Verification Framework](https://arxiv.org/abs/2607.05391v1) | Read full paper | A PM should frame the implication around deployment constraints: power, thermals, memory, latency, safety, and customer integration effort. |
| 6 | [Optimizing ML Workload Partitioning between CPUs and CIM Accelerators for Heterogeneous Computing](https://arxiv.org/abs/2607.05240v1) | Read full paper | A PM should frame the implication around deployment constraints: power, thermals, memory, latency, safety, and customer integration effort. |
| 7 | [An event-driven framework for fly-inspired visual motion detection](https://arxiv.org/abs/2607.05205v1) | Read full paper | A PM should frame the implication around deployment constraints: power, thermals, memory, latency, safety, and customer integration effort. |
| 8 | [Multiplayer Interactive World Models with Representation Autoencoders](https://arxiv.org/abs/2607.05352v1) | Skim | A PM should translate the update into cost per token, TTFT, throughput, utilization, reliability, and operational simplicity. |
| 9 | [Unified Audio Intelligence Without Regressing on Text Intelligence](https://arxiv.org/abs/2607.05196v1) | Skim | A PM should identify what customer workflow, roadmap bet, or competitive positioning this update could change. |
| 10 | [UNIVERSE: Unified Video Action Models for Autonomous Driving with Flexible Mask-Modulated Modality Generation](https://arxiv.org/abs/2607.05133v1) | Skim | A PM should identify what customer workflow, roadmap bet, or competitive positioning this update could change. |
| 11 | [GaP: A Graph-as-Policy Multi-Agent Self-Learning Harness For Variational Automation Tasks](https://arxiv.org/abs/2607.05369v1) | Skim | A PM should frame the implication around deployment constraints: power, thermals, memory, latency, safety, and customer integration effort. |

## 6. Big Tech, AI Lab, and Competitive Watch

### Google / DeepMind
- No high-signal tracked item this week.

### Meta
- No high-signal tracked item this week.

### Amazon / AWS
- No high-signal tracked item this week.

### Microsoft
- [Adaptive Inference Batching using Policy Gradients](https://arxiv.org/abs/2607.05272v1) — score 2.1/5

### Apple
- No high-signal tracked item this week.

### OpenAI
- [sqlite-utils 4.0rc2, mostly written by Claude Fable (for about $149.25)](https://simonwillison.net/2026/Jul/5/sqlite-utils-fable/#atom-everything) — score 1.6/5

### Anthropic
- [What's new in Claude Sonnet 5](https://simonwillison.net/2026/Jun/30/claude-sonnet-5/#atom-everything) — score 1.95/5
- [LLM-as-a-Verifier: A General-Purpose Verification Framework](https://arxiv.org/abs/2607.05391v1) — score 1.85/5
- [sqlite-utils 4.0rc2, mostly written by Claude Fable (for about $149.25)](https://simonwillison.net/2026/Jul/5/sqlite-utils-fable/#atom-everything) — score 1.6/5

### NVIDIA
- [When Words Predict Workload](https://arxiv.org/abs/2607.04951v1) — score 2.1/5
- [Multiplayer Interactive World Models with Representation Autoencoders](https://arxiv.org/abs/2607.05352v1) — score 1.7/5


### AI Accelerator and Developer Platform Competitive Intelligence

- **#2 When Words Predict Workload** (arXiv cs.CL) — https://arxiv.org/abs/2607.04951v1
  Target lens: what shipped, target developer, favored hardware, developer experience angle, and roadmap implication.
- **#8 Multiplayer Interactive World Models with Representation Autoencoders** (arXiv cs.AI) — https://arxiv.org/abs/2607.05352v1
  Target lens: what shipped, target developer, favored hardware, developer experience angle, and roadmap implication.
- **#11 GaP: A Graph-as-Policy Multi-Agent Self-Learning Harness For Variational Automation Tasks** (arXiv cs.AI) — https://arxiv.org/abs/2607.05369v1
  Target lens: what shipped, target developer, favored hardware, developer experience angle, and roadmap implication.

## 7. Model Zoo Watch

- **When Words Predict Workload** — ask what operators, graph patterns, quantization support, and demo value this model family stresses. https://arxiv.org/abs/2607.04951v1
- **DSpark: Confidence-Scheduled Speculative Decoding with Semi-Autoregressive Generation** — ask what operators, graph patterns, quantization support, and demo value this model family stresses. https://arxiv.org/abs/2607.05147v1
- **What's new in Claude Sonnet 5** — ask what operators, graph patterns, quantization support, and demo value this model family stresses. https://simonwillison.net/2026/Jun/30/claude-sonnet-5/#atom-everything
- **LLM-as-a-Verifier: A General-Purpose Verification Framework** — ask what operators, graph patterns, quantization support, and demo value this model family stresses. https://arxiv.org/abs/2607.05391v1
- **Multiplayer Interactive World Models with Representation Autoencoders** — ask what operators, graph patterns, quantization support, and demo value this model family stresses. https://arxiv.org/abs/2607.05352v1
- **Unified Audio Intelligence Without Regressing on Text Intelligence** — ask what operators, graph patterns, quantization support, and demo value this model family stresses. https://arxiv.org/abs/2607.05196v1
- **UNIVERSE: Unified Video Action Models for Autonomous Driving with Flexible Mask-Modulated Modality Generation** — ask what operators, graph patterns, quantization support, and demo value this model family stresses. https://arxiv.org/abs/2607.05133v1
- **SPEARBench: A Benchmark for Naturalness Evaluation in Streaming Speech-to-Speech Language Models** — ask what operators, graph patterns, quantization support, and demo value this model family stresses. https://arxiv.org/abs/2607.05365v1

## 8. Portfolio Project Ideas

- **Compiler support matrix for edge AI models** — Build a matrix mapping model families to operators, quantization needs, and runtime support. Hardness: medium. Stack: Python, ONNX, PyTorch, SQLite, Markdown. Resume bullet: Built an AI accelerator model-zoo readiness tool for compiler and SDK roadmap planning.
- **Inference cost and latency benchmark dashboard** — Compare vLLM/TensorRT-LLM-style serving metrics across model sizes and batching assumptions. Hardness: medium-high. Stack: Python, FastAPI, SQLite, Streamlit or React. Resume bullet: Created an inference PM dashboard linking TTFT, throughput, memory, and cost per token to roadmap decisions.
- **Deep-dive teardown: Adaptive Inference Batching using Policy Gradients** — Turn one weekly item into a product memo with customer, metric, roadmap, and competitive implications. Hardness: low-medium. Stack: Markdown, notebooks, source links. Resume bullet: Produced source-backed AI infrastructure product strategy briefs for executive-style decision making.

## 9. LinkedIn Post Ideas

### Option A: Broad weekly AI PM digest

This week's AI signal is less about novelty for its own sake and more about deployment judgment.

The items I would track as a hardware-native AI PM are the ones that connect model capability to serving cost, runtime maturity, developer adoption, and customer confidence.

My filter: what changes a roadmap decision, an SDK priority, or an infra metric?

Sources:
- Adaptive Inference Batching using Policy Gradients: https://arxiv.org/abs/2607.05272v1
- When Words Predict Workload: https://arxiv.org/abs/2607.04951v1
- DSpark: Confidence-Scheduled Speculative Decoding with Semi-Autoregressive Generation: https://arxiv.org/abs/2607.05147v1
- What's new in Claude Sonnet 5: https://simonwillison.net/2026/Jun/30/claude-sonnet-5/#atom-everything

### Option B: Deep dive on one research paper or technical blog

One item worth a deeper look this week: Adaptive Inference Batching using Policy Gradients.

The product question is not just whether the technique is technically impressive. It is whether it changes latency, memory, cost, reliability, or developer experience enough to affect a real deployment decision.

The PM move is to ask: what metric would prove this matters, and what customer workload would expose the tradeoff?

Source: https://arxiv.org/abs/2607.05272v1

### Option C: Hardware-native AI PM angle

AI product strategy is increasingly constrained by the physical stack: silicon, memory bandwidth, compiler support, runtime scheduling, and serving economics.

That is the opportunity for hardware-native PMs. The best roadmap decisions connect customer-facing capability to what the hardware and software stack can actually sustain in production.

Source-backed items:
- Adaptive Inference Batching using Policy Gradients: https://arxiv.org/abs/2607.05272v1
- When Words Predict Workload: https://arxiv.org/abs/2607.04951v1
- DSpark: Confidence-Scheduled Speculative Decoding with Semi-Autoregressive Generation: https://arxiv.org/abs/2607.05147v1
- What's new in Claude Sonnet 5: https://simonwillison.net/2026/Jun/30/claude-sonnet-5/#atom-everything

### Option D: Compiler / quantization / edge AI angle

Compiler and quantization work can look like implementation detail until you view it through SDK adoption.

Operator coverage, quantized graph lowering, model zoo completeness, and edge/datacenter benchmark quality all shape developer confidence. A missing graph pattern or unsupported datatype can become a product adoption blocker.

The PM question: which models should be forcing functions for compiler completeness and customer demos?

Sources:
- Adaptive Inference Batching using Policy Gradients: https://arxiv.org/abs/2607.05272v1
- When Words Predict Workload: https://arxiv.org/abs/2607.04951v1
- DSpark: Confidence-Scheduled Speculative Decoding with Semi-Autoregressive Generation: https://arxiv.org/abs/2607.05147v1
- What's new in Claude Sonnet 5: https://simonwillison.net/2026/Jun/30/claude-sonnet-5/#atom-everything


## 10. Interview Talking Points

- **Adaptive Inference Batching using Policy Gradients:** Use this to discuss how an AI PM evaluates datacenter, agents through customer impact, measurable infra metrics, and roadmap tradeoffs.
- **When Words Predict Workload:** Use this to discuss how an AI PM evaluates edge, datacenter, agents through customer impact, measurable infra metrics, and roadmap tradeoffs.
- **DSpark: Confidence-Scheduled Speculative Decoding with Semi-Autoregressive Generation:** Use this to discuss how an AI PM evaluates datacenter through customer impact, measurable infra metrics, and roadmap tradeoffs.
- **What's new in Claude Sonnet 5:** Use this to show disciplined judgment: what changed, why it matters, and what product metric would prove it mattered.
- **LLM-as-a-Verifier: A General-Purpose Verification Framework:** Use this to discuss how an AI PM evaluates edge through customer impact, measurable infra metrics, and roadmap tradeoffs.
- **Optimizing ML Workload Partitioning between CPUs and CIM Accelerators for Heterogeneous Computing:** Use this to discuss how an AI PM evaluates edge, datacenter, agents through customer impact, measurable infra metrics, and roadmap tradeoffs.
- **An event-driven framework for fly-inspired visual motion detection:** Use this to discuss how an AI PM evaluates edge, datacenter through customer impact, measurable infra metrics, and roadmap tradeoffs.
- **Multiplayer Interactive World Models with Representation Autoencoders:** Use this to discuss how an AI PM evaluates datacenter through customer impact, measurable infra metrics, and roadmap tradeoffs.

## 11. Recommended Deep Dive of the Week

**Pick:** [Adaptive Inference Batching using Policy Gradients](https://arxiv.org/abs/2607.05272v1)

Spend 30-60 minutes on this because It ranks highly on ai infrastructure relevance, which makes it useful for separating infrastructure signal from general AI noise. The goal is to extract one reusable PM story: what changed, what metric matters, what decision it affects, and what could break at 10x scale.

## 12. Source Index

- Adaptive Inference Batching using Policy Gradients — arXiv cs.AI — https://arxiv.org/abs/2607.05272v1
- When Words Predict Workload — arXiv cs.CL — https://arxiv.org/abs/2607.04951v1
- DSpark: Confidence-Scheduled Speculative Decoding with Semi-Autoregressive Generation — arXiv cs.CL — https://arxiv.org/abs/2607.05147v1
- What's new in Claude Sonnet 5 — Simon Willison — https://simonwillison.net/2026/Jun/30/claude-sonnet-5/#atom-everything
- LLM-as-a-Verifier: A General-Purpose Verification Framework — arXiv cs.AI — https://arxiv.org/abs/2607.05391v1
- Optimizing ML Workload Partitioning between CPUs and CIM Accelerators for Heterogeneous Computing — arXiv cs.AI — https://arxiv.org/abs/2607.05240v1
- An event-driven framework for fly-inspired visual motion detection — arXiv cs.CV — https://arxiv.org/abs/2607.05205v1
- Multiplayer Interactive World Models with Representation Autoencoders — arXiv cs.AI — https://arxiv.org/abs/2607.05352v1
- Unified Audio Intelligence Without Regressing on Text Intelligence — arXiv cs.CL — https://arxiv.org/abs/2607.05196v1
- UNIVERSE: Unified Video Action Models for Autonomous Driving with Flexible Mask-Modulated Modality Generation — arXiv cs.CV — https://arxiv.org/abs/2607.05133v1
- GaP: A Graph-as-Policy Multi-Agent Self-Learning Harness For Variational Automation Tasks — arXiv cs.AI — https://arxiv.org/abs/2607.05369v1
- SPEARBench: A Benchmark for Naturalness Evaluation in Streaming Speech-to-Speech Language Models — arXiv cs.AI — https://arxiv.org/abs/2607.05365v1
- EvoAgentBench: Benchmarking Agent Self-Evolution via Ability Transfer — arXiv cs.AI — https://arxiv.org/abs/2607.05202v1
- Telescope: Improving Zero Shot Detection of LLM Generated Content By Measuring Token Repetition Probability — arXiv stat.ML — https://arxiv.org/abs/2607.04061v1
- sqlite-utils 4.0rc2, mostly written by Claude Fable (for about $149.25) — Simon Willison — https://simonwillison.net/2026/Jul/5/sqlite-utils-fable/#atom-everything
- Vision Pretraining for Dense Spatial Perception — arXiv cs.CV — https://arxiv.org/abs/2607.05247v1
- Streaming Neural Speech Codecs through Time-Invariant Representations — arXiv cs.CL — https://arxiv.org/abs/2607.05250v1
- Beyond Independent Labels: Schwartz-Geometry Decoding for Human Value Detection — arXiv cs.CL — https://arxiv.org/abs/2607.05052v1
- Train Smarter, Not Longer: Memorization-Guided Data Reuse for Efficient LLM Training — arXiv cs.CL — https://arxiv.org/abs/2607.04969v1
- CompactionRL: Reinforcement Learning with Context Compaction for Long-Horizon Agents — arXiv cs.LG — https://arxiv.org/abs/2607.05378v1
