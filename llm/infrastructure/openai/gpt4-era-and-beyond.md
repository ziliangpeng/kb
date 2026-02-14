# OpenAI's Infrastructure

The evolution of OpenAI's internal training and inference stack — from TensorFlow on Google's TPUs to a custom PyTorch-based framework on 100,000+ GPU clusters across Microsoft Azure, serving 2.5 billion prompts per day.

OpenAI is unusually secretive about infrastructure. The GPT-4 technical report explicitly states: "this report contains no further details about the architecture (including model size), hardware, training compute, dataset construction, training method, or similar." Most of what's known comes from blog posts, the GPT-4 contributions page, job postings, one remarkably candid YouTube video, and one leak.

## The Stack Progression

| Era       | Framework            | Hardware                     | Cloud                                     |
| --------- | -------------------- | ---------------------------- | ----------------------------------------- |
| 2016-2017 | TensorFlow           | GPUs                         | AWS → Azure (migrated early 2017)         |
| 2018-2019 | TensorFlow           | Google Cloud TPUs            | Google Cloud (GPT-1, GPT-2)               |
| 2020      | Switched to PyTorch  | NVIDIA V100s                 | Microsoft Azure                           |
| 2020-2022 | Custom PyTorch stack | 10,000 V100s → A100s         | Microsoft Azure (dedicated supercomputer) |
| 2023-2024 | Custom PyTorch stack | ~25,000 A100s → H100s        | Microsoft Azure                           |
| 2025+     | Custom PyTorch stack | 100,000+ GPUs, multi-cluster | Microsoft Azure, multi-datacenter         |
| 2025+     | Custom PyTorch stack | GB300 NVL72 (Blackwell Ultra) | Microsoft Azure (first production cluster) |

## Phase 4: GPT-4 and the Predictable Scaling Breakthrough (2023)

The GPT-4 technical report revealed one infrastructure achievement: **predictable scaling**. OpenAI could predict GPT-4's final loss from models trained with 1,000x–10,000x less compute, using the power law `L(C) = aC^b + c`. This meant they could validate expensive architectural and training decisions cheaply — a critical capability when a single training run costs tens of millions of dollars.

### The GPT-4 Infrastructure Team

The [GPT-4 contributions page](https://openai.com/contributions/gpt-4/) is one of the few windows into OpenAI's infrastructure organization:

| Role | Person |
|------|--------|
| Infrastructure lead | Greg Brockman |
| Supercomputing lead | Christopher Berner |
| Model distribution, systems & networking lead | Amin Tootoonchian |
| Triton lead | Phil Tillet |
| Throughput lead | Trevor Cai |
| Infrastructure usability co-leads | Chris Hesse, Shantanu Jain |
| Software correctness lead | Mikhail Pavlov |
| Hardware correctness lead | Michael Petrov |
| Execution lead | Nikolas Tezak |
| Optimization lead | Jakub Pachocki |

**Distributed Training Infrastructure Team**: Trevor Cai, Yunxing Dai, Chris Hesse, Brandon Houghton, Yongjik Kim, Lukasz Kondraciuk, Mikhail Pavlov, Raul Puri, Nikolas Tezak, Amin Tootoonchian, Tianhao Zheng.

**Compute Cluster Scaling Team**: Christopher Berner, Oleg Boiko, Andrew Cann, Ben Chess, Christian Gibson, Mateusz Litwin, Emy Parparita, Henri Roussez, Eric Sigler, Akila Welihinda.

### The SemiAnalysis Leak (July 2023)

In July 2023, **Dylan Patel and Gerald Wong** at SemiAnalysis published a detailed article claiming to reveal GPT-4's architecture and training infrastructure. Key infrastructure-related claims:

- **~25,000 A100 GPUs** for the training run
- **90–100 days** training duration
- **~13 trillion tokens** of training data (text and code)
- **MFU (Model FLOPs Utilization)** of only 32–36%, indicating significant overhead from communication, pipeline bubbles, etc.
- Estimated cost: **~$63 million** (A100 compute hours alone)
- Suspected heterogeneous cluster connectivity (800G/1.6T within segments, 200G/400G between segments)

The article's claims were corroborated by George Hotz and PyTorch co-founder Soumith Chintala. SemiAnalysis also noted: "Due to the importance of fault tolerant training, publishing of methods has effectively stopped. When OpenAI and others tell the hardware industry about these issues, they are very vague and high level so as to not reveal any of their distributed systems tricks."

**Source:** ["GPT-4 Architecture, Infrastructure, Training Dataset, Costs, Vision, MoE"](https://semianalysis.com/2023/07/10/gpt-4-architecture-infrastructure/) (SemiAnalysis, Jul 2023)

## Phase 5: GPT-4.5 and Multi-Cluster Training (2025)

The most detailed look at OpenAI's current infrastructure came from a **46-minute YouTube video** — "Pre-Training GPT-4.5" — featuring Sam Altman interviewing three key people:

- **Amin Tootoonchian** — Chief System Architect (systems & networking)
- **Alex Paino** — pre-training ML algorithm lead for GPT-4.5
- **Daniel Selsam** — data efficiency and algorithms

### Multi-Cluster Training

The single most important revelation: GPT-4.5 required **more compute than was available in any single cluster**, forcing OpenAI to move to multi-cluster training. Tootoonchian stated: "state management, our approach with state management changed — we had to scale to more compute and that compute was not available as part of one cluster, we had to go to multicluster training."

This was a critical departure from GPT-4, which trained on a single cluster. GPT-4.5 used **over 100,000 GPUs** across multiple clusters.

### Failure at Unprecedented Scale

At 100,000 GPUs, OpenAI encountered failure patterns **"that even hardware vendors hadn't encountered because of the sheer sample size."** One example: a bug in PyTorch's `torch.sum` function that occurred infrequently and was data-distribution-dependent, causing illegal memory accesses roughly once per hundred to thousand steps. The bug manifested with seemingly distinct symptoms across the system, making it extremely hard to diagnose.

Initial failure rates were "quite significant" but improved substantially once root causes were identified. The team noted: "Almost everything needs to work as expected for the result to hold."

### De-Risking Runs

The team conducted a dedicated large de-risking run **6–9 months** before the actual training launch. Changes were carefully sequenced from a "known good config" (GPT-4). Multiple large de-risking runs validated ML choices at scale before committing to the full training run.

### Scale and Effort

- "It took like hundreds of people, almost all of OpenAI's effort to do GPT-4.5"
- Project inception approximately **two years** before execution
- Alex Paino stated that retraining GPT-4 could now be accomplished with just **5–10 people**, compared to the hundreds needed originally — reflecting accumulated infrastructure maturity
- On the future of 10 million GPU synchronous training runs: it would need to be "semi-synchronous" due to "laws of nature" preventing full synchrony at that scale — "more decentralized with 10 million GPUs working together but not all necessarily communicating with each other"

### Cluster Networking at 100K Scale

Scaling to 100,000 GPUs exposed fundamental networking limitations:

**InfiniBand vs Ethernet radix problem:**

- InfiniBand NDR Quantum-2 switches have only **64 ports at 400G**, while NVIDIA Spectrum-X Ethernet switches have **128 ports at 400G** — double the radix
- With a 3-tier fat tree topology, InfiniBand maxes out at **65,536 GPUs** fully connected
- Beyond that requires a 4-tier IB network with **7:1 oversubscription** — 4 pods of ~24,576 GPUs each, where cross-pod bandwidth is 1/7th of within-pod
- At least one 100K H100 cluster was deployed with **Spectrum-X Ethernet** instead of InfiniBand — a notable departure from HPC tradition

**Dual-network architecture:**

- **Backend network**: GPU-to-GPU communication (all-reduce, all-gather during training)
- **Frontend network**: Data loading from storage + checkpointing to blob storage
- Separation prevents checkpoint writes from interfering with gradient synchronization

**Server-level networking:**

- Microsoft/OpenAI use a **Cedar Fever-7 networking module** per server instead of 8 individual PCIe ConnectX-7 cards, consolidating into 4 OSFP cages instead of 8

**Sources:**

- ["Pre-Training GPT-4.5"](https://www.youtube.com/watch?v=6nJZopacruq) (OpenAI YouTube channel)
- ["100,000 H100 Clusters: Power, Network, Reliability"](https://newsletter.semianalysis.com/p/100000-h100-clusters-power-network) (SemiAnalysis)

## Phase 6: GPT-5 and the Blackwell Era (2025+)

GPT-5 marked a strategic shift: Epoch AI estimates it used roughly **10x less pre-training compute than GPT-4.5** (~50,000 H100s maximum), because OpenAI found that scaling **post-training** (reinforcement learning, RLHF, chain-of-thought training) had better marginal returns than scaling pre-training further. This is a significant departure from the "just make pre-training bigger" paradigm.

Meanwhile, the underlying hardware generation leaped forward with NVIDIA's Blackwell architecture.

### GB300 NVL72 Cluster (Late 2025)

Microsoft Azure deployed the **world's first production NVIDIA GB300 NVL72 supercomputing cluster**, purpose-built for OpenAI:

- ~64 racks, **over 4,600 Blackwell Ultra GPUs**
- Each rack: **72 Blackwell Ultra GPUs + 36 Grace CPUs**
- **37 TB of fast memory** and **1.44 exaflops of FP4** per VM
- **Within-rack networking**: NVLink at **130 TB/s** all-to-all bandwidth between 72 GPUs — effectively treating an entire rack as one giant GPU for communication
- **Between-rack networking**: NVIDIA Quantum-X800 InfiniBand at **800 Gb/s per GPU**, with ConnectX-8 SuperNICs
- **Cooling**: AI-designed microfluidics cooling system developed with Corintis — liquid cooling at the chip level
- **Performance**: Up to **5x higher throughput per GPU** vs Hopper on DeepSeek-R1 671B

The NVL72 design is a fundamental shift: previously NVLink only connected 8 GPUs within a single server. Now 72 GPUs in an entire rack share ultra-high-bandwidth interconnect, allowing tensor parallelism to span a full rack instead of just one node.

**Sources:**

- [NVIDIA Blog — Azure GB300 NVL72](https://blogs.nvidia.com/blog/microsoft-azure-worlds-first-gb300-nvl72-supercomputing-cluster-openai/) (Q4 2025)
- [Azure Blog](https://azure.microsoft.com/en-us/blog/microsoft-azure-delivers-the-first-large-scale-cluster-with-nvidia-gb300-nvl72-for-openai-workloads/) (Q4 2025)
- [Epoch AI — Why GPT-5 used less training compute than GPT-4.5](https://epoch.ai/gradient-updates/why-gpt5-used-less-training-compute-than-gpt45-but-gpt6-probably-wont)

## What the Stack Looks Like Today

OpenAI has never publicly named or detailed their LLM training framework. What is confirmed from public sources:

### Confirmed

- **PyTorch** as the base framework (since Jan 2020)
- **Triton** for GPU kernels — OpenAI's own open-source GPU programming language, maintained by Phil Tillet. Also became the backend for PyTorch 2.0's `torch.compile`. See [[llm/training-frameworks/backstories|Triton backstory]].
- **Kubernetes** for cluster orchestration (scaled to 7,500+ nodes)
- **MPI** for inter-process communication in training jobs
- **NCCL/UCX** for collective communication (from job postings)
- **Custom GPU health checks** beyond standard DCGM/NVML
- **Checkpointing to blob storage** for fault tolerance
- **Azure** as the primary cloud provider (with Microsoft-built dedicated supercomputers)

### From Job Postings

Job postings reveal the contours of what OpenAI builds internally:

- **Training Performance Engineer**: "high-performance, asynchronous, zero-copy tensor and optimizer-state-aware data movement"; "performant, high-uptime, fault-tolerant training frameworks (training loop, state management, resilient checkpointing, deterministic orchestration, observability)"; "distributed process management"
- **GPU Infrastructure - HPC**: Fleet reliability, PCIe, InfiniBand, networking, power management, kernel performance tuning
- **Inference - CUDA/Kernels**: Custom CUDA kernels for inference (fused matmuls, custom activations, memory layout transforms)
- **Supercomputing**: "The Supercomputing team owns the entire process of building OpenAI's compute and infrastructure, which includes hardware sourcing and system design, deployment of huge clusters using Kubernetes and Azure, and building the internal experiment platform"

Required skills across postings: Python, C++, CUDA, familiarity with NCCL/MPI/UCX, experience with large-scale data loading and checkpointing, training runtime and distributed scheduling.

### Not Publicly Disclosed

- The name or architecture of their internal distributed training framework
- Whether they fork or modify PyTorch/NCCL
- Specifics of custom communication collectives
- Checkpointing frequency or implementation details
- Whether "Rapid" is still in use or has been replaced
- Internal distributed systems "tricks" for fault tolerance (SemiAnalysis notes this is deliberately kept secret)

## Compute Spending (2024)

> [!note] External analysis by Epoch AI, not confirmed by OpenAI. Based on OpenAI's financials and public information.

OpenAI spent roughly **$7 billion** on compute in 2024:

| Category | Amount | % of Total |
|----------|--------|-----------|
| Experiments & research | ~$4.5B | ~65% |
| Inference (serving ChatGPT, API) | ~$1.8B | ~26% |
| GPT-4.5 final training run | ~$400M | ~6% |
| Other model final training runs | ~$80M | ~1% |

**Over 70% of compute went to experiments** — not final training runs of released models. The GPT-4.5 final run cost ~$400M, but the experimentation that led up to it (de-risking runs, hyperparameter sweeps, architecture exploration, failed attempts) cost more than 10x that.

Training compute estimates for specific models:

| Model | Estimated FLOP range |
|-------|---------------------|
| GPT-4o | 1e25 – 5e25 |
| GPT-4o mini | 1e24 – 1e25 |
| Sora Turbo | 1e24 – 1e26 |
| o-series (o1, o3) post-training | 1–30% of base model pre-training |

**Source:** [Epoch AI — OpenAI Compute Spend](https://epoch.ai/data-insights/openai-compute-spend) (2025)

## Inference Infrastructure

### Scale of Operations (Mid-2025)

- **2.5 billion prompts per day** (330M from US users)
- **500+ million weekly active users** for ChatGPT
- Azure processed **100+ trillion tokens in Q1 2025** — 5x year-over-year, with **50 trillion tokens in a single month**

### Multi-Cloud Strategy

OpenAI was Azure-exclusive until January 2025, when the Stargate restructuring changed Microsoft's role to **right of first refusal**. Since then, OpenAI has diversified aggressively:

| Provider | Deal Size | Purpose | Date |
|----------|-----------|---------|------|
| Microsoft Azure | $13B+ cumulative | Training + inference (primary) | 2019–ongoing |
| AWS | $38B | NVIDIA GPU clusters | Late 2025 |
| Google Cloud | undisclosed | ChatGPT global expansion | June 2025 |
| Oracle (OCI) | undisclosed | Training, dedicated datacenter | 2025 |

The practical driver: at 2.5B prompts/day with reasoning models consuming up to 100x more compute per request, no single provider can supply enough GPUs.

### Cerebras Inference

OpenAI's first production model on non-NVIDIA hardware:

- **GPT-5.3-Codex-Spark** running on Cerebras Wafer Scale Engine 3 (February 2026)
- WSE-3: single chip the size of a dinner plate, **4 trillion transistors**, hundreds of thousands of AI cores
- **Over 1,000 tokens/sec**, 80% reduction in per-request overhead, 50% reduction in time-to-first-token

**Source:** [Cerebras Blog](https://www.cerebras.ai/blog/openai-codexspark) (Feb 2026)

### Reasoning Model Compute Challenge

The o1/o3 reasoning models create a fundamentally different inference problem:

- They generate **orders of magnitude more tokens** internally before producing a response
- Jensen Huang estimates **up to 100x more compute per request** than standard models
- Industry projection: inference demand projected to **exceed training demand by 118x by 2026**
- Analysts project inference will claim **75% of total AI compute by 2030**

This is the primary driver behind OpenAI's multi-cloud and multi-hardware diversification.

### Batch API

OpenAI separates inference into two tiers:

- **Real-time API**: low latency, higher cost (analogous to OLTP)
- **Batch API**: **50% cost discount**, up to 50K requests per file, 24-hour turnaround, separate rate limit pool (analogous to OLAP)

The separation allows filling GPU idle capacity with batch jobs, improving overall utilization.

## The Microsoft Relationship

| Date | Event |
|------|-------|
| July 2019 | "Exclusive computing partnership" — **$1B** from Microsoft |
| 2020 | Microsoft builds dedicated Azure supercomputer for OpenAI (10K V100s, 285K CPUs, top-5 supercomputer) |
| 2021 | Additional investment (~$2B); GitHub Copilot launched with OpenAI Codex |
| January 2023 | Multi-year extension — **~$10B** |
| January 2025 | Stargate Project announced; Microsoft's exclusivity changed to **right of first refusal** |

Total Microsoft investment: **over $13 billion**.

The relationship dynamic: Microsoft provides hardware and datacenter infrastructure; OpenAI builds all training software internally. This is why OpenAI never used DeepSpeed — the partnership was about compute, not software.

## Stargate and Custom Silicon

### Stargate Project

Announced **January 21, 2025** by President Trump. Stargate LLC — SoftBank has financial responsibility, OpenAI has operational responsibility.

- **Total planned investment**: $500 billion over four years
- **Equity funders**: SoftBank, OpenAI, Oracle, MGX
- **Technology partners**: Arm, Microsoft, NVIDIA, Oracle, OpenAI
- **Data center sites**: Shackelford County TX, Dona Ana County NM, Lordstown OH, Milam County TX, plus an undisclosed Midwestern site
- **Planned capacity**: Nearly 7 gigawatts
- **First data center**: Opened in Texas (September 23, 2025)
- Microsoft's role shifted from exclusive cloud provider to right of first refusal

### Fairwater Datacenter Design

Microsoft's next-generation datacenter architecture, built for AI workloads:

- Each campus has **two building types**: a standard CPU & storage facility (48 MW) and an ultra-dense **2-story 300 MW GPU building** housing **over 150,000 GB200 GPUs**
- Microsoft also designed **600+ MW individual buildings** (2x Fairwater scale) with double CPU/storage and diesel generators
- Full buildout targets **over 2 GW of IT capacity** per campus

To put the scale in perspective: GPT-4.5's multi-cluster training used roughly 50–100 MW across clusters. One Fairwater campus at 2 GW is 20–40x that.

**Source:** ["Microsoft's AI Strategy Deconstructed"](https://newsletter.semianalysis.com/p/microsofts-ai-strategy-deconstructed) (SemiAnalysis — based on satellite imagery and industry sources)

### Custom Silicon and Hardware Partnerships

OpenAI now has **six simultaneous hardware partnerships**:

| Partner | Purpose | Timeline | Notes |
|---------|---------|----------|-------|
| NVIDIA (via Azure) | Training + inference (H100, GB200, GB300) | Current | InfiniBand networking |
| AMD | Training + inference (MI300X → MI450 → MI500) | MI300X current; MI450 H2 2026 | Direct 6 GW deal (Oct 2025), $100B+ projected revenue, warrant for 160M AMD shares (~10% stake) |
| Broadcom ("Titan") | Custom inference ASIC | End of 2026 | TSMC 3nm; Titan 2 planned on A16 process |
| Cerebras | Inference (Wafer Scale Engine 3) | 2026+ | $10B deal; first non-NVIDIA production model (GPT-5.3-Codex-Spark) |
| AMD (via Azure) | Inference (MI300X, 192 GB HBM) | Current | Through Microsoft, predates direct deal |
| Microsoft Maia | Some first-party Copilot workloads | Current | In-house Microsoft chip |

**Sources:**

- [AMD and OpenAI announce strategic partnership](https://openai.com/index/openai-amd-strategic-partnership/) (OpenAI, Oct 2025)
- [OpenAI and Broadcom announce strategic collaboration](https://openai.com/index/openai-and-broadcom-announce-strategic-collaboration/) (OpenAI)
- [OpenAI and Cerebras partnership](https://openai.com/index/cerebras-partnership/) (OpenAI, Jan 2025)

### Multi-Datacenter Training

> [!todo] Research datacenter training network topologies in depth — fat-tree, rail-optimized, InfiniBand vs Ethernet at scale, DWDM for inter-site links, DiLoCo and other semi-synchronous approaches.

SemiAnalysis reported on OpenAI's multi-datacenter ambitions:

- **First major cluster (Iowa)**: ~25,000 A100 chips (GPT-3.5 era)
- **Second major cluster (Arizona)**: Scaled over time — first H100 building in 2023, H200s in 2024, GB200 buildings in 2025, totaling ~130,000 GPUs across four buildings
- Plans to interconnect ultra-large campuses and run distributed training runs across the country
- Approaching gigawatt-scale liquid-cooled datacenter campuses

**Inter-site interconnect:** Microsoft signed deals **north of $10 billion with fiber companies** to connect datacenters for multi-site training. Uses dedicated fiber paths with **wavelength-division multiplexing (DWDM)** for terabits of aggregate inter-site bandwidth.

**Synchronization approach:** The communication hierarchy means different parallelism strategies at each level:

1. **Within NVL72 rack** (~130 TB/s via NVLink): tensor parallelism
2. **Within datacenter** (400–800 Gb/s per GPU via IB/Ethernet): pipeline and data parallelism
3. **Between datacenters** (DWDM fiber, much lower bandwidth): infrequent synchronization — likely **DiLoCo-style**, where each site performs local gradient synchronization frequently and only exchanges "pseudo-gradients" with other sites every ~500 steps, reducing inter-site data exchange by **~500x**

**Sources:**

- ["Multi-Datacenter Training: OpenAI's Ambitious Plan To Beat Google's Infrastructure"](https://newsletter.semianalysis.com/p/multi-datacenter-training-openais) (SemiAnalysis)
- [Windows Central — Microsoft fiber deals](https://www.windowscentral.com/microsoft/a-researcher-claims-microsoft-and-openai-may-have-cracked-multi-datacenter-distributed-training-for-their-ai-models-based-on-their-actions-microsoft-has-signed-deals-north-of-usd10-billion-with-fiber-companies-to-connect-data-centers)

## Key People

- **Greg Brockman** — Co-founder, CTO/President. Built Stripe's infrastructure before OpenAI. Infrastructure lead for GPT-4. Currently leading OpenAI's infrastructure build-out (targeting 30 GW of compute capacity).
- **Amin Tootoonchian** — Chief System Architect. PhD from University of Toronto in SDN/networking. Former Intel Labs researcher. Led model distribution and systems/networking for GPT-4; led multi-cluster training for GPT-4.5.
- **Christopher Berner** — Supercomputing lead. Built the Kubernetes scaling infrastructure. Discussed the "Rapid" platform on the TWIML podcast (2018).
- **Philippe Tillet** — Triton lead. Created Triton during his PhD at Harvard, joined OpenAI in 2020. See [[llm/training-frameworks/backstories|Triton backstory]].
- **Jeffrey Wu** — Co-author of GPT-2 and GPT-3 papers. Implemented model-parallel strategies for GPT-3. Now at Anthropic.
- **Mark Chen** — SVP of Research (Sep 2024), then Chief Research Officer (Mar 2025). Co-developed early model-parallel strategy with Rewon Child. Previously at Jane Street Capital.
- **Rewon Child** — Co-author of GPT-2. Co-developed early model-parallel strategy. Author of "Generating Long Sequences with Sparse Transformers." Later co-founded Inflection.
- **Sam McCandlish** — Former Research Lead (AI Safety). Co-authored "Scaling Laws for Neural Language Models" (2020) with Jared Kaplan. Now co-founder at Anthropic.
- **Jakub Pachocki** — Optimization lead for GPT-4. Later became Chief Scientist at OpenAI (May 2024).

## External References

- [Pre-Training GPT-4.5](https://www.youtube.com/watch?v=6nJZopacruq) — OpenAI YouTube, 46-minute video with Amin Tootoonchian, Alex Paino, and Daniel Selsam
- [GPT-4 Architecture, Infrastructure, Training Dataset, Costs, Vision, MoE](https://semianalysis.com/2023/07/10/gpt-4-architecture-infrastructure/) — SemiAnalysis leak (Dylan Patel & Gerald Wong, Jul 2023)
- [Multi-Datacenter Training: OpenAI's Ambitious Plan To Beat Google's Infrastructure](https://newsletter.semianalysis.com/p/multi-datacenter-training-openais) — SemiAnalysis
- [100,000 H100 Clusters: Power, Network, Reliability](https://newsletter.semianalysis.com/p/100000-h100-clusters-power-network) — SemiAnalysis
- [Scaling Kubernetes to 7,500 Nodes](https://openai.com/index/scaling-kubernetes-to-7500-nodes/) — OpenAI blog (Jan 2021)
- [OpenAI Standardizes on PyTorch](https://openai.com/index/openai-pytorch/) — OpenAI blog (Jan 2020)
- [Infrastructure for Deep Learning](https://openai.com/index/infrastructure-for-deep-learning/) — OpenAI blog (2017)
- [GPT-4 Contributions](https://openai.com/contributions/gpt-4/) — OpenAI
- [Dota 2 with Large Scale Deep Reinforcement Learning](https://arxiv.org/abs/1912.06680) — Rapid platform paper
- [Triton: An Intermediate Language and Compiler for Tiled Neural Network Computations](https://openai.com/index/triton/) — OpenAI blog (Jul 2021)
