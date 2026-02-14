# OpenAI's Training Infrastructure

The evolution of OpenAI's internal training stack — from TensorFlow on Google's TPUs to a custom PyTorch-based framework on 100,000+ GPU clusters across Microsoft Azure.

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

## Phase 1: TensorFlow and Google Cloud (2016-2019)

OpenAI started on AWS with Kubernetes in 2016, migrated to Azure in early 2017 for the control plane (while keeping some nodes on-premises), but trained GPT-1 and GPT-2 on **Google Cloud**.

- **GPT-1** (2018): TensorFlow, 8 GPUs, trained for ~1 month
- **GPT-2** (2019): TensorFlow 1.x, 256 Google Cloud TPU v3 cores

This was before OpenAI's partnership with Microsoft. The TPU usage is notable — OpenAI was a Google Cloud customer for its most visible models. The Microsoft partnership ($1B, July 2019) changed this completely.

### Rapid: The RL Training Platform

OpenAI built **Rapid**, a general-purpose distributed RL training system, for the **OpenAI Five** Dota 2 project (2018-2019). Architecture: two layers — (1) spins up thousands of machines and handles inter-machine communication, (2) runs the training software. Rollout workers ran game copies on CPUs, experience was synced through Redis, and optimizer nodes performed synchronous gradient descent on GPUs. Scale: 256 P100 GPUs + 128,000 CPU cores on Google Cloud. Backends for Kubernetes, Azure, and GCP.

Rapid demonstrated OpenAI's infrastructure ambitions before LLMs became the focus. It's unclear whether Rapid evolved into or was replaced by whatever system runs LLM pre-training today.

## Phase 2: The PyTorch Switch (January 2020)

On **January 30, 2020**, OpenAI announced standardization on PyTorch. The reason: it "decreased iteration time on research ideas in generative modeling from **weeks to days**." They had previously used multiple frameworks depending on the project.

The timing matters. GPT-2 (February 2019) was the last major TensorFlow model. GPT-3 (June 2020) was the first major PyTorch model. The switch happened in between, which means **GPT-3's training infrastructure was built from scratch in PyTorch in roughly 5 months** (January–May 2020).

At the time of the announcement, OpenAI was already writing PyTorch bindings for their custom **blocksparse** GPU kernels (efficient block-sparse matrix multiplication), and Philippe Tillet was building `torch-blocksparse` — early work that would lead to Triton.

## Phase 3: GPT-3 and the Azure Supercomputer (2020)

Microsoft built one of the **top-5 supercomputers in the world** exclusively for OpenAI:

- **10,000 NVIDIA V100 GPUs**
- **285,000 CPU cores**
- **400 Gbps per GPU server** networking

This was the first dedicated Azure AI supercomputer, built specifically for GPT-3 training. The infrastructure was custom — **Jeffrey Wu** implemented the model-parallel strategies for GPT-3, with **Mark Chen** and **Rewon Child** prototyping an early version.

**OpenAI never used DeepSpeed**, despite Microsoft building it. OpenAI had deep in-house infrastructure expertise going back to their Kubernetes-based cluster management (2016-2017), custom CUDA kernels (blocksparse), and the Rapid platform. Microsoft provided the hardware; OpenAI provided the software.

### Kubernetes at Scale

OpenAI published a detailed blog post on **scaling Kubernetes to 7,500 nodes** (January 2021) for GPT-3, CLIP, and DALL-E training:

- **5 API servers and 5 etcd nodes** to spread load; up to 70GB of heap per API server
- Training jobs run **MPI** — all pods within a job participate in a single MPI communicator
- If **any pod dies, the entire job halts** and restarts from the last checkpoint
- Pods communicate via pod IP addresses with MPI over SSH, not service endpoints
- **Gang scheduling**: all StatefulSet members must be scheduled before training begins (MPI is sensitive to group membership changes)
- Jobs checkpoint regularly to **blob storage** and resume from the last checkpoint on restart
- Switched from Flannel to **native pod networking** for host-level throughput on Azure VMSSes

OpenAI also built a custom library of GPU tests (beyond NVIDIA's DCGM) that exercise GPUs to catch problems not visible through standard error codes. These run during instance creation and periodically via Kubernetes CronJobs.

**Sources:**

- [Scaling Kubernetes to 7,500 Nodes](https://openai.com/index/scaling-kubernetes-to-7500-nodes/) (OpenAI, Jan 2021)
- [Scaling Kubernetes to 2,500 Nodes](https://openai.com/index/scaling-kubernetes-to-2500-nodes/) (OpenAI, 2018)
- [Infrastructure for Deep Learning](https://openai.com/index/infrastructure-for-deep-learning/) (OpenAI, 2017)

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

**Source:** ["Pre-Training GPT-4.5"](https://www.youtube.com/watch?v=6nJZopacruq) (OpenAI YouTube channel)

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

### Custom Silicon: Titan

OpenAI is designing its own AI chip:

- **Codename**: Titan
- **Design partner**: Broadcom (ASIC design services)
- **Manufacturer**: TSMC, 3nm process
- **Expected deployment**: End of 2026
- **Initial focus**: Primarily inference, with some training capability
- **Second generation (Titan 2)**: Planned on TSMC's A16 process

### Multi-Datacenter Training

SemiAnalysis reported on OpenAI's multi-datacenter ambitions:

- **First major cluster (Iowa)**: ~25,000 A100 chips (GPT-3.5 era)
- **Second major cluster (Arizona)**: Scaled over time — first H100 building in 2023, H200s in 2024, GB200 buildings in 2025, totaling ~130,000 GPUs across four buildings
- Plans to interconnect ultra-large campuses and run distributed training runs across the country
- Approaching gigawatt-scale liquid-cooled datacenter campuses

**Source:** ["Multi-Datacenter Training: OpenAI's Ambitious Plan To Beat Google's Infrastructure"](https://newsletter.semianalysis.com/p/multi-datacenter-training-openais) (SemiAnalysis)

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
