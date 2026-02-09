# Anthropic's Training Infrastructure

The evolution of Anthropic's compute infrastructure — from a small startup on Google Cloud to a triple-cloud operation with $95B+ in infrastructure commitments across AWS, Google, and Microsoft Azure.

Anthropic is the only frontier AI lab running production workloads across three major chip architectures (Trainium, TPUs, NVIDIA GPUs) and three cloud providers simultaneously. This multi-cloud strategy is central to how Anthropic operates.

## The Stack

### Frameworks

The Claude 3 model card confirmed the core frameworks: **JAX, PyTorch, and Triton**.

- **JAX** is the primary ML framework, particularly for TPU and Trainium workloads. Anthropic is listed alongside Google DeepMind and xAI as a major JAX user. JAX's functional purity and XLA compilation make it natural for TPU-based training.
- **PyTorch** is also used. The AWS Neuron SDK supports both PyTorch and JAX on Trainium.
- **Triton** (OpenAI's GPU programming language) is used for custom GPU kernels.
- Anthropic engineers write **custom low-level kernels** for Trainium hardware via the AWS Neuron Kernel Interface (NKI), which exposes the full Trainium ISA.

No specific JAX libraries (Haiku, Flax, Optax) have been publicly confirmed. Anthropic has not open-sourced any core training infrastructure tools.

### What Job Postings Reveal

- **Pre-training team**: "core ML framework primitives in JAX, PyTorch"; high-performance ML training infrastructure
- **RL team**: profiling, benchmarking, distributed systems debugging
- **AI Reliability Engineering (AIRE) team**: reliability metrics, model serving, batch inference, and training pipelines
- **Discovery team**: infrastructure engineers working end-to-end on scientific AGI blockers
- Required skills across postings: JAX, PyTorch, Triton, Beam/Spark/Dask for data pipelines, GPU/TPU architecture expertise, Kubernetes, AWS/GCP

### What's Not Publicly Known

- The name or architecture of their internal distributed training framework
- Which parallelism strategies they use (at their scale, certainly all of them)
- Whether they fork or modify JAX/NCCL
- Checkpointing frequency or fault tolerance implementation
- Specific MFU numbers (one source claims ~40% on TPUs vs typical ~30% on GPUs, attributed to ex-Google compiler expertise)

## The Triple-Cloud Strategy

### AWS — Primary Training Partner

Amazon has invested **$8 billion** in Anthropic across three tranches:

| Date | Amount |
|------|--------|
| September 2023 | $1.25B |
| March 2024 | $2.75B (completing initial $4B commitment) |
| November 2024 | $4B additional |

AWS is contractually designated as Anthropic's **"primary training partner and cloud provider."** Claude is available on Amazon Bedrock.

**Project Rainier** is the centerpiece: an **$11 billion** AWS data center campus on 1,200 acres in Indiana, housing **~500,000 Trainium2 chips** across 30 data centers (each 200,000 sq ft). Activated October 2025. Provides **5x the compute** used to train earlier Claude models. Target: over 1 million Trainium2 chips.

Architecture: UltraServers (4 physical servers × 16 Trainium2 chips = 64 chips per UltraCluster), connected via NeuronLinks.

**Hardware-software co-design**: Anthropic is not just a Trainium customer — they are essentially treating AWS's **Annapurna Labs** as a custom silicon partner. Anthropic engineers write low-level kernels directly interfacing with Trainium silicon, contribute to the AWS Neuron software stack, and provide direct input on chip design. **Trainium3** was developed in collaboration with Anthropic, with the company providing input on training speed, latency, and energy efficiency. Trainium3 promises 4x performance and 40% better energy efficiency over Trainium2.

**Sources:**

- [AWS Activates Project Rainier](https://www.aboutamazon.com/news/aws/aws-project-rainier-ai-trainium-chips-compute-cluster) (About Amazon, Oct 2025)
- [Anthropic on Amazon Trainium](https://www.anthropic.com/news/anthropic-amazon-trainium) (Anthropic)
- [Amazon's AI Resurgence: AWS & Anthropic's Multi-Gigawatt Trainium Expansion](https://newsletter.semianalysis.com/p/amazons-ai-resurgence-aws-anthropics-multi-gigawatt-trainium-expansion) (SemiAnalysis)

### Google Cloud — Up to 1 Million TPUs

Google has invested **~$3 billion** in Anthropic and holds approximately **14% equity**.

| Date | Event |
|------|-------|
| 2023 | Initial cloud partnership + $500M investment + $1.5B commitment. TPU v5e for Claude serving. |
| January 2025 | Additional $1B investment |
| October 2025 | Massive expansion: up to **1 million TPUs**, over **1 GW** of capacity online in 2026, worth tens of billions |

Anthropic will be among the first external customers for **TPU v6, v7 (Ironwood), and future generations**. Of the 1 million TPUs, approximately 400,000 chips are being purchased directly, with the remaining 600,000 leased through traditional Google Cloud contracts.

The Google relationship is very much alive despite AWS being the "primary" partner. SemiAnalysis estimates TPU Ironwood TCO is ~44% lower than equivalent NVIDIA Blackwell servers.

**Sources:**

- [Expanding Our Use of Google Cloud TPUs and Services](https://www.anthropic.com/news/expanding-our-use-of-google-cloud-tpus-and-services) (Anthropic, Oct 2025)
- [Google and Anthropic Announce Cloud Deal Worth Tens of Billions](https://www.cnbc.com/2025/10/23/anthropic-google-cloud-deal-tpu.html) (CNBC)

### Microsoft Azure — NVIDIA GPUs at Scale

In November 2025, Anthropic added a third cloud:

- Committed to **$30 billion in Azure compute capacity** (up to 1 GW)
- **Microsoft invested $5 billion** and **NVIDIA invested $10 billion** in Anthropic
- Infrastructure uses NVIDIA **Grace Blackwell** and upcoming **Vera Rubin** GPUs
- Claude became the only frontier model available on **all three major cloud providers**

**Sources:**

- [Microsoft, NVIDIA and Anthropic Announce Strategic Partnerships](https://blogs.microsoft.com/blog/2025/11/18/microsoft-nvidia-and-anthropic-announce-strategic-partnerships/) (Microsoft Blog)

### Why Triple-Cloud Works

The multi-cloud strategy gives Anthropic several advantages:

- **Negotiating leverage**: Credible alternatives mean better pricing from each provider
- **Capacity access**: In a market with massive chip shortages, multi-cloud avoids bottlenecks
- **Enterprise neutrality**: A bank wary of Amazon can use Claude through Google Cloud; a retailer wary of Google can use Claude through AWS; a Microsoft shop can use Claude through Azure
- **Architecture hedging**: If one chip architecture hits a dead end, Anthropic has alternatives
- **Resilience**: No single point of failure

The cost is engineering complexity — maintaining performance across three chip architectures (Trainium, TPUs, NVIDIA GPUs) requires separate optimization efforts for each.

## Own Data Centers

In November 2025, Anthropic announced a **$50 billion** commitment to build custom data centers in **Texas and New York** with UK-based neocloud provider **Fluidstack**. First sites coming online in 2026. This is Anthropic's first independent infrastructure, reducing dependence on any single hyperscaler.

**Source:** [Anthropic Invests $50 Billion in American AI Infrastructure](https://www.anthropic.com/news/anthropic-invests-50-billion-in-american-ai-infrastructure) (Anthropic, Nov 2025)

## Networking

Anthropic partners with **Arista Networks** for their ethernet networking needs — notably choosing ethernet over InfiniBand. Tom Brown (Chief Compute Officer) has been personally involved in the partnership.

## Compute Scale Summary

| Provider | Hardware | Scale | Deal Value |
|----------|----------|-------|------------|
| AWS | Trainium2 (→ Trainium3) | 500K chips → 1M+ | $8B equity + $11B facility |
| Google Cloud | TPU v5e/v5p (→ v6, v7 Ironwood) | Up to 1M TPUs | ~$3B equity + tens of billions cloud deal |
| Microsoft Azure | NVIDIA Blackwell / Vera Rubin | Up to 1 GW capacity | $30B compute commitment ($5B MSFT + $10B NVDA equity) |
| Fluidstack | Custom (likely NVIDIA) | Texas + New York DCs | $50B infrastructure commitment |

Total committed infrastructure: **$95B+** across all providers. Combined capacity approaching **multi-gigawatt scale** by 2026-2027.

## Funding

### All Rounds

| Round | Date | Amount | Valuation | Key Investors |
|-------|------|--------|-----------|---------------|
| Series A | May 2021 | $124M | — | Jaan Tallinn, Eric Schmidt |
| Series B | Apr 2022 | $580M | — | Sam Bankman-Fried / Alameda ($500M of $580M) |
| Series C | May 2023 | $450M | — | Spark Capital |
| Amazon tranche 1 | Sep 2023 | $1.25B | — | Amazon |
| Google investment | Oct–Nov 2023 | ~$2B | — | Google |
| Series D | Feb 2024 | $750M | — | Menlo Ventures |
| Amazon tranche 2 | Mar 2024 | $2.75B | — | Amazon |
| Amazon tranche 3 | Nov 2024 | $4B | — | Amazon |
| Google additional | Jan 2025 | $1B | — | Google |
| Series E | Mar 2025 | $3.5B | $61.5B | Lightspeed Venture Partners |
| Series F | Sep 2025 | $13B | $183B | Goldman Sachs Asset Management |
| Microsoft + NVIDIA | Nov 2025 | $15B | ~$350B | Microsoft ($5B), NVIDIA ($10B) |
| Series F Extension | Jan 2026 | $10–20B | $350B | Coatue, GIC |

**Total raised: ~$37 billion.**

**FTX backstory**: SBF invested $500M of allegedly stolen FTX customer funds into Anthropic's Series B. After FTX's collapse, the bankruptcy estate sold the stake in 2024 for ~$1.4B. At Anthropic's $183B September 2025 valuation, that stake would have been worth ~$14.6B.

### Revenue

- End of 2024: ~$1B ARR
- End of 2025: ~$9B ARR
- 2026 projection: $20–26B
- Projected break-even: 2027–2028

### Compute Spending

Through September 2025, Anthropic spent approximately **$2.66 billion on AWS alone** — roughly matching its $2.55B in revenue over the same period. By late 2025, AWS spend alone was running at **~$6.5B annualized**. Total cloud spending across all providers is likely significantly higher.

## Training Cost Trajectory

Dario Amodei has been unusually specific about training cost scaling (Lex Fridman interview, November 2024):

- Current-generation models (late 2024): ~$100M per training run
- Models in training at the time: ~$1B
- 2025: "a few billion"
- 2026: "above $10 billion"
- 2027: "hundred billion dollar clusters"

Project Rainier provides 5x the compute used for earlier Claude models, consistent with the jump from $100M-class to $1B-class training runs.

**Source:** [Dario Amodei on Lex Fridman Podcast #452](https://lexfridman.com/dario-amodei-transcript/) (Nov 2024)

## Key People

- **Dario Amodei** — CEO, co-founder. Former VP of Research at OpenAI (2016–2020). Led GPT-2 and GPT-3 development. PhD Computational Neuroscience, Princeton.
- **Daniela Amodei** — President, co-founder. Former VP of Safety & Policy at OpenAI.
- **Tom Brown** — Co-founder, Chief Compute Officer. Core developer behind GPT-3 at OpenAI. Oversees all compute infrastructure. Describes Anthropic's work as "humanity's largest infrastructure buildout ever."
- **Sam McCandlish** — Co-founder, Chief Architect. Co-authored the foundational scaling laws paper at OpenAI. PhD Theoretical Physics, Stanford.
- **Nick Joseph** — Head of Pre-training. One of the original 11 who left OpenAI. Manages 40+ person training team. Said: "the hardest problems in AI are often infrastructure problems, not ML problems."
- **Rahul Patil** — CTO (hired Oct 2025). Former CTO of Stripe, SVP Cloud Infrastructure at Oracle.
- **Jared Kaplan** — Co-founder, Chief Science Officer. Co-authored scaling laws papers.
- **Chris Olah** — Co-founder. Interpretability research lead. Pioneered neural network interpretability at Google Brain and OpenAI.
- **Tom Henighan** — Member of Technical Staff. One of Anthropic's first employees. Previously worked on scaling laws at OpenAI. Helped build core training/evaluation infrastructure.

### The OpenAI Exodus

Anthropic was founded in 2021 by 11 people who left OpenAI together, including Dario and Daniela Amodei, Tom Brown, Sam McCandlish, Jared Kaplan, Chris Olah, and others. The departure was driven by disagreements over OpenAI's safety practices and commercialization direction. Many of the founders had worked on the key infrastructure and research that produced GPT-2 and GPT-3 — they brought deep knowledge of large-scale training to Anthropic from day one.

## Comparison to OpenAI

| Dimension | Anthropic | OpenAI |
|-----------|-----------|--------|
| **Total infra commitment** | ~$95B+ (multi-provider) | $500B+ (Stargate) |
| **Primary chip** | Multi-arch (Trainium, TPU, NVIDIA) | NVIDIA GPUs (+ custom Titan chip planned) |
| **Cloud presence** | AWS + GCP + Azure (all three) | Azure only (via Microsoft) |
| **Training framework** | JAX (primary) + PyTorch + Triton | PyTorch (primary) + Triton |
| **Own data centers** | $50B planned (Fluidstack) | $500B Stargate (SoftBank, Oracle, MGX) |
| **Custom silicon** | Co-designs Trainium with Annapurna Labs | Designing Titan chip with Broadcom/TSMC |
| **Valuation** | $350B (Jan 2026) | ~$300B (late 2025) |
| **Revenue** | ~$9B ARR (end 2025) | ~$12B+ ARR (end 2025) |

The strategic difference: OpenAI concentrates on massive scale through a single infrastructure path (Microsoft/Azure/NVIDIA + Stargate). Anthropic distributes across multiple providers, trading maximum scale at any single point for resilience and optionality.

## External References

- [Anthropic on Amazon Trainium](https://www.anthropic.com/news/anthropic-amazon-trainium) — Trainium co-design details
- [AWS Activates Project Rainier](https://www.aboutamazon.com/news/aws/aws-project-rainier-ai-trainium-chips-compute-cluster) — Project Rainier activation (Oct 2025)
- [Expanding Our Use of Google Cloud TPUs](https://www.anthropic.com/news/expanding-our-use-of-google-cloud-tpus-and-services) — 1M TPU deal (Oct 2025)
- [Microsoft, NVIDIA and Anthropic Strategic Partnerships](https://blogs.microsoft.com/blog/2025/11/18/microsoft-nvidia-and-anthropic-announce-strategic-partnerships/) — Azure/NVIDIA deal (Nov 2025)
- [Anthropic Invests $50 Billion in American AI Infrastructure](https://www.anthropic.com/news/anthropic-invests-50-billion-in-american-ai-infrastructure) — Fluidstack data centers (Nov 2025)
- [Amazon's AI Resurgence: AWS & Anthropic's Multi-Gigawatt Trainium Expansion](https://newsletter.semianalysis.com/p/amazons-ai-resurgence-aws-anthropics-multi-gigawatt-trainium-expansion) — SemiAnalysis deep dive
- [Dario Amodei on Lex Fridman Podcast #452](https://lexfridman.com/dario-amodei-transcript/) — Training cost trajectory (Nov 2024)
- [How To Train An LLM with Anthropic's Head of Pretraining](https://www.ycombinator.com/library/Mw-how-to-train-an-llm-with-anthropic-s-head-of-pretraining) — Nick Joseph YC talk
- [Anthropic Co-founder: Building Claude Code, Lessons From GPT-3 & LLM System Design](https://www.ycombinator.com/library/Mp-anthropic-co-founder-building-claude-code-lessons-from-gpt-3-llm-system-design) — Tom Brown YC talk
- [Engineering Challenges in Interpretability](https://www.anthropic.com/research/engineering-challenges-interpretability) — Infrastructure details in interpretability work
- [Rahul Patil Joins Anthropic](https://www.anthropic.com/news/rahul-patil-joins-anthropic) — New CTO announcement (Oct 2025)
