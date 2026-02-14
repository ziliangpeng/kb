# OpenAI Training Infrastructure Evolution (2015-2023)

A chronological account of the hardware, software, and organizational infrastructure behind OpenAI's models from founding through ChatGPT.

## 1. Founding and Early Days (2015-2018)

### The Beginning

OpenAI was co-founded in December 2015 by Sam Altman, Greg Brockman, Ilya Sutskever, Elon Musk, and others. The company initially operated from Greg Brockman's living room.

### The DGX-1 Donation (August 2016)

NVIDIA CEO Jensen Huang personally hand-delivered the very first DGX-1 AI supercomputer to OpenAI's San Francisco office. This was a $129,000 system containing **8x NVIDIA Tesla P100 (Pascal) GPUs**, capable of ~170 TFLOPS (FP16). Elon Musk publicly thanked NVIDIA "in support of democratizing AI technology." Huang had originally built it for NVIDIA's own engineers, but when Musk heard about it at a conference, he told Huang "I want one of those."

Source: [NVIDIA delivers DGX-1 to OpenAI (TOP500)](https://www.top500.org/news/nvidia-delivers-dgx-1-supercomputer-in-a-box-to-openai/)

### Kubernetes and Cloud (2016-2017)

OpenAI began running Kubernetes on **AWS** in 2016 as a batch scheduling system. In early 2017, they migrated to a **hybrid model**:

- Kubernetes control planes (API servers, etcd) ran in **Azure**
- Kubernetes nodes ran in **OpenAI's own on-premise data centers**
- GPU-intensive workloads (e.g., training ImageNet models) ran on-prem where costs were lower and hardware access was better
- CPU-heavy workloads ran in Azure cloud

This hybrid approach --- cloud for orchestration, on-prem for GPU compute --- was common at the time and reflected the reality that GPU cloud pricing was still unattractive for large-scale training.

Source: [Kubernetes Case Study - OpenAI](https://kubernetes.io/case-studies/openai/)

### GPT-1 (June 2018)

- 117M parameters, 12-layer Transformer
- Trained on **8 GPUs** (likely P100 or V100) for about 1 month
- Training data: BooksCorpus (~7,000 unpublished books)

Tiny by later standards.

### OpenAI Five / Dota 2 (2018-2019)

OpenAI's largest compute project before GPT-3:

- **256 NVIDIA Tesla P100 GPUs** + **128,000 CPU cores**
- Ran on **Google Cloud Platform** (not Azure --- OpenAI was still multi-cloud)
- Custom distributed RL training framework called **"Rapid"**
- Played 180 years of Dota gameplay per day against itself
- Single continuous training run from June 30, 2018 to April 22, 2019 (~10 months)
- Total compute: **770 +/- 50 PFlop/s-days**

Source: [OpenAI Five blog post](https://openai.com/index/openai-five/)

### Scaling Kubernetes to 2,500 Nodes (January 2018)

OpenAI published a blog post detailing pushing Kubernetes to **2,500+ nodes** on Azure (D15v2 and NC24 VMs). Major challenges:

- **etcd breakdowns** beyond 500 nodes
- **KubeDNS hotspots** (exceeded Azure's ~200 QPS limit for external domain lookups)
- **Docker image pull times** (the Dota game image was ~17GB, taking 30+ minutes on fresh nodes)
- **ARP cache overflows** on machines

Source: [OpenAI Blog - Scaling Kubernetes to 2,500 Nodes](https://openai.com/index/scaling-kubernetes-to-2500-nodes/)

### "AI and Compute" (May 2018)

OpenAI published a landmark analysis showing compute in the largest AI training runs had been **doubling every 3.4 months** since 2012 --- a 300,000x increase. This directly shaped OpenAI's strategic thinking about scaling.

Greg Brockman and team began writing down hardware projections that "suddenly dwarfed early assumptions." Brockman recalled: **"We started to think, 'Okay, maybe we'll need $10 billion worth of hardware.'"** This was years before the Microsoft deal.

Source: [OpenAI - AI and Compute](https://openai.com/index/ai-and-compute/), [Fortune profile of Brockman (Nov 2025)](https://fortune.com/2025/11/05/openai-greg-brockman-ai-infrastructure-data-center-master-builder/)

---

## 2. GPT-2 Era and the Microsoft Deal (2019)

### GPT-2 (February 2019)

- 1.5B parameters
- Trained on **256 Google Cloud TPU v3 cores** (= 32 TPU v3 chips, 8 cores per chip)
- Training data: WebText dataset (~40GB of high-quality web pages)

GPT-2 was trained on **Google TPUs, not NVIDIA GPUs**. OpenAI was still using Google Cloud infrastructure at this point, before the exclusive Microsoft deal. (For context: Andrej Karpathy noted in 2024 that you can now reproduce GPT-2 training for ~$672, on one 8xH100 node in 24 hours.)

### Scaling Laws (January 2020)

Jared Kaplan et al. published "Scaling Laws for Neural Language Models," establishing that loss scales as a **power law** with model size, dataset size, and compute. Key implication: as computational budget increases, it should be spent **primarily on larger models** rather than dramatically more training time or data. This directly justified GPT-3's scale decision.

Source: [arXiv:2001.08361](https://arxiv.org/abs/2001.08361)

### Microsoft $1 Billion Investment (July 22, 2019)

The transformative deal:

- **Not a lump sum**: Could be delivered anytime over the next decade, in installments
- **Microsoft became OpenAI's exclusive cloud provider**
- **Microsoft became "preferred partner for commercializing new AI technologies"**
- The companies would **"jointly develop new Azure AI supercomputing technologies"**
- A hardware and software platform within Azure would be built **"to scale to AGI"**

This gave OpenAI access to massive compute while giving Microsoft an exclusive relationship with the leading AI lab. It also ended OpenAI's multi-cloud era --- no more Google TPUs, no more GCP.

Source: [Microsoft announcement (July 2019)](https://news.microsoft.com/source/2019/07/22/openai-forms-exclusive-computing-partnership-with-microsoft-to-build-new-azure-ai-supercomputing-technologies/)

---

## 3. The First Microsoft Supercomputer: GPT-3 Era (2020)

### Microsoft Supercomputer (May 2020)

Microsoft announced one of the **top-5 publicly disclosed supercomputers in the world**, built exclusively for OpenAI:

- **10,000 NVIDIA V100 Tensor Core GPUs**
- **285,000+ CPU cores** (AMD)
- **400 Gbps network connectivity per GPU server**
- **InfiniBand** across nodes
- **NVLink** via NVSwitch within each node
- Located in **West Des Moines, Iowa** (Microsoft data centers)
- Built collaboratively by Microsoft engineering, Microsoft Research, OpenAI, and NVIDIA

The system was described as "a single system" --- a unified supercomputer, not a loosely coupled cloud.

Source: [Microsoft announcement (May 2020)](https://news.microsoft.com/source/features/ai/openai-azure-supercomputer/)

### GPT-3 Training (2020)

- 175B parameters
- Trained on **"part of a high-bandwidth cluster provided by Microsoft"** (the paper's exact words --- they did not use all 10,000 GPUs)
- Training framework: **PyTorch**
- Parallelism: model parallelism within each matrix multiply + model parallelism across layers of the network
- Total compute: **3,640 petaflop/s-days** (compared to ~tens of PF-days for GPT-2)
- Training data: ~300B tokens from Common Crawl, WebText2, Books1, Books2, Wikipedia

**Cost estimates** (not officially confirmed by OpenAI):

- At theoretical 28 TFLOPS per V100 and lowest 3-year reserved cloud pricing: ~**$4.6M** for a single training run
- Other estimates range $500K-$4.6M depending on utilization assumptions
- Using 10,000 V100s: ~14.8 days of training

The phrase "part of" the cluster is notable --- the rest was likely used for other experiments, inference, and smaller model variants.

Source: [GPT-3 paper (arXiv:2005.14165)](https://arxiv.org/abs/2005.14165), [Lambda blog cost analysis](https://lambda.ai/blog/demystifying-gpt-3)

---

## 4. The V100-to-A100 Transition (2021-2022)

### Kubernetes Scaling to 7,500 Nodes (2021)

OpenAI published a follow-up blog post describing scaling from 2,500 to **7,500 nodes** in a single Kubernetes cluster. Major challenges:

- etcd heap usage reached **70GB per API server** (5 API servers, 5 etcd nodes)
- Flannel networking couldn't scale --- switched to **native Azure VMSS pod networking** with CNI plugins for host-level network throughput
- Prometheus TSDB couldn't handle the metrics volume

This cluster supported GPT-3, CLIP, and DALL-E.

Source: [OpenAI Blog - Scaling Kubernetes to 7,500 Nodes](https://openai.com/index/scaling-kubernetes-to-7500-nodes/)

### A100 Arrival (2021)

Microsoft debuted the **"Voyager" supercomputer** at #10 on the November 2021 Top500 list, running on **Azure ND A100 v4** nodes. This marked the V100-to-A100 transition.

The A100 (released May 2020 by NVIDIA) offered major improvements over V100:

- **Memory**: 40GB or 80GB HBM2e (vs 16/32GB HBM2 on V100)
- **Tensor Core performance**: Significantly higher throughput
- **BF16 support**: Better numerical format for training (V100 only had FP16)
- **Sparsity support**: 2:4 structured sparsity acceleration
- **MIG (Multi-Instance GPU)**: Partitioning for inference workloads

Customers reported **2-3x compute performance improvement** over V100 systems with no engineering changes required.

Source: [Azure Blog - A100 GA](https://azure.microsoft.com/en-us/blog/azure-announces-general-availability-of-scaleup-scaleout-nvidia-a100-gpu-instances-claims-title-of-fastest-public-cloud-super/)

### Triton Compiler (2021)

Philippe Tillet joined OpenAI full-time in 2020 to develop **Triton** --- an open-source Python-like language for writing GPU kernels. Triton could match cuBLAS performance for FP16 matmul in under 25 lines of code. Released under MIT license.

This was a strategic infrastructure investment: rather than relying entirely on NVIDIA's closed-source CUDA/cuBLAS libraries, OpenAI developed its own GPU programming layer. This gave them more control over kernel optimization and reduced dependency on NVIDIA.

Source: [OpenAI Triton blog](https://openai.com/index/triton/), [Triton GitHub](https://github.com/triton-lang/triton)

---

## 5. GPT-3.5 as Infrastructure Test Run (2022)

The GPT-3.5 series was not just a product update --- it was a **deliberate infrastructure validation exercise** for GPT-4.

From OpenAI's GPT-4 research page:

> "We trained GPT-3.5 as a first 'test run' of the system. We found and fixed some bugs and improved our theoretical foundations. As a result, our GPT-4 training run was unprecedentedly stable, becoming our first large model whose training performance we were able to accurately predict ahead of time."

OpenAI had rebuilt their **"entire deep learning stack"** and co-designed a new supercomputer with Azure. What "rebuilt entire deep learning stack" entailed:

- **Hardware transition**: V100 clusters to A100 clusters, with fundamentally different memory capacity, precision formats (BF16), and interconnects
- **New distributed training code**: OpenAI uses a custom proprietary framework (not Megatron-LM or DeepSpeed), which had to be rewritten or substantially adapted for A100 architecture
- **New checkpointing systems**: Critical at scale --- at 20K+ GPUs, hardware failures occur every few hours, so robust checkpoint/restart is essential
- **Improved parallelism strategies**: GPT-4 later used 8-way tensor parallelism + 15-way pipeline parallelism, likely refined during GPT-3.5 runs
- **Scaling law prediction infrastructure**: Methods to predict final model loss from models trained at 1/10,000th of the compute

GPT-3.5 let them find and fix bugs in all of these systems before committing the vastly larger compute budget for GPT-4. The result: GPT-4's training was "unprecedentedly stable."

For more detail on what GPT-3.5 validated, see: [[llm/models/gpt3/gpt3-to-chatgpt/gpt3.5-backstories#GPT-3.5 Was a Test Run for GPT-4|GPT-3.5 Backstories]]

---

## 6. GPT-4 Training (February-August 2022)

### Timeline

- **Training started**: ~February 2022
- **Training completed**: August 2022
- **Post-training** (alignment, red-teaming): August 2022 - March 2023
- **Public release**: March 14, 2023

### What OpenAI Officially Disclosed

The GPT-4 technical report deliberately withholds almost everything: *"This report contains no further details about the architecture (including model size), hardware, training compute, dataset construction, training method, or similar."*

What they did share:

- A core achievement was "infrastructure and optimization methods that have very predictable behavior across multiple scales"
- They could predict GPT-4's final loss from models trained with **1/10,000th of the compute**
- The GPT-3.5 test run enabled this by finding bugs and improving theoretical foundations

### Architecture (from leaks)

Leaked details (primarily via George Hotz and SemiAnalysis, widely regarded as accurate):

- **Architecture**: Mixture of Experts (MoE)
- **Total parameters**: ~1.8 trillion across 120 layers
- **Expert configuration**: 16 experts, each ~111B parameters (MLP)
- **Routing**: 2 experts active per forward pass
- **Training data**: ~13 trillion tokens (text + code)

(George Hotz originally leaked 8x 220B experts; SemiAnalysis later reported 16x ~111B. The discrepancy may reflect different counting methods or model evolution.)

Source: [SemiAnalysis - GPT-4 Architecture](https://newsletter.semianalysis.com/p/gpt-4-architecture-infrastructure), [The Decoder](https://the-decoder.com/gpt-4-architecture-datasets-costs-and-more-leaked/)

### Training Infrastructure (from leaks)

- **GPUs**: ~20,000-25,000 NVIDIA A100s
- **Training duration**: 90-100 days
- **Parallelism**: 8-way tensor parallelism + 15-way pipeline parallelism
- **Inference parallelism**: 128 GPUs, 8-way tensor + 16-way pipeline
- **Total compute**: ~2.15 x 10^25 BF16 FLOP
- **MFU (Model FLOPs Utilization)**: 32-36% --- described as low **"due to an absurd number of failures requiring checkpoints that needed to be restarted from"**
- **Estimated hardware cost**: ~$63M (at ~$1/A100-hour, hardware only)
- **Location**: West Des Moines, Iowa

At ~20K A100 scale, GPU failures occur every few hours. The low MFU reflects the reality of checkpoint restarts at scale. Despite this, the GPT-3.5 test run had validated the infrastructure well enough that loss predictions held.

### Water Consumption

In **July 2022** (month before GPT-4 training completed), Microsoft pumped approximately **11.5 million gallons of water** into the Iowa datacenter cluster for cooling --- about **6% of all water used in the local water district** that also supplies residential drinking water. Microsoft's total water use grew **34% in 2022**, largely attributable to AI workloads. Water-based cooling was used when outside temperature exceeded 29.3 C (85 F); otherwise, outside air cooling sufficed.

Source: [AP/KCCI investigative report](https://www.kcci.com/article/ai-technology-behind-chatgpt-built-in-west-des-moines-iowa-microsoft/45081445)

---

## Software Stack

| Component | Technology | Notes |
|-----------|-----------|-------|
| Training framework | PyTorch | Confirmed in GPT-3 paper |
| Distributed training | Custom proprietary | Not Megatron-LM or DeepSpeed; never open-sourced |
| GPU kernels | Triton | Open-source, reduces CUDA dependency |
| Cluster management | Kubernetes | Scaled from 2,500 to 7,500 nodes |
| Networking | InfiniBand (inter-node), NVLink/NVSwitch (intra-node) | Fat-tree topology |

OpenAI has not open-sourced or publicly documented their core distributed training framework.

---

## GPU Count Evolution

| Year | Model/Project | GPU Type | Count |
|------|--------------|----------|-------|
| 2016 | Early research | P100 (DGX-1) | 8 |
| 2018 | GPT-1 | P100/V100 | 8 |
| 2018-19 | OpenAI Five | P100 | 256 (+128K CPU cores) |
| 2019 | GPT-2 | Google TPU v3 | 32 chips (256 cores) |
| 2020 | GPT-3 | V100 | Part of 10,000 cluster |
| 2022 | GPT-3.5 | A100 | Unknown (likely thousands) |
| 2022 | GPT-4 | A100 | ~20,000-25,000 |

---

## Training Cost Evolution

| Model | Estimated Cost | Year | Confidence |
|-------|---------------|------|------------|
| GPT-1 | Minimal (8 GPUs, 1 month) | 2018 | Confirmed |
| GPT-2 | ~$50K-$250K | 2019 | Estimated |
| GPT-3 | ~$4.6M (single run) | 2020 | Estimated |
| GPT-4 | ~$63M (hardware only) | 2022 | Likely (from leaks) |

---

## Key People in Infrastructure

| Person | Role | Key Contribution |
|--------|------|-----------------|
| **Greg Brockman** | CTO, co-founder | Early hardware projections ("$10B worth of hardware"), datacenter strategy. Previously built Stripe's engineering infrastructure. |
| **Christopher Berner** | Head of Compute | Scaled Kubernetes 2,500 to 7,500 nodes. Led supercomputer cluster builds. |
| **Jakub Pachocki** | Chief Scientist (2024-), formerly Research Director | Led GPT-4 pretraining. Built "much of the infrastructure that enabled OpenAI's scientific discoveries." |
| **Philippe Tillet** | Triton compiler lead | Created the Triton GPU programming language. PhD from Harvard on GPU compilers. |
| **Ilya Sutskever** | Co-founder, Chief Scientist (2015-2024) | Drove the scaling vision. Departed May 2024 for Safe Superintelligence Inc. |
| **Jared Kaplan** | Research | Published foundational scaling laws paper. Later co-founded Anthropic. |

---

## Azure Supercomputer Generations

| Generation | Year | GPU Type | Key Specs |
|-----------|------|----------|-----------|
| Gen 1 | 2020 | V100 | 10,000 GPUs, 285K CPU cores, 400 Gbps InfiniBand |
| Gen 2 | 2021-2022 | A100 | "Voyager" class, #10 on Top500 (Nov 2021) |
| Gen 3 | 2023 | H100 | NVLink 4.0, 400 Gb/s Quantum-2 CX7 InfiniBand per GPU, 3.2 Tb/s per VM |

---

## The Microsoft Partnership

### Investment Timeline

- **$1B** announced July 2019 (installments over up to a decade)
- **~$13B total** by January 2023 (across multiple rounds)
- Microsoft held an **observer seat on OpenAI's board** (until July 2024)

### Degree of Integration (2019-2024)

Extremely tight:

- All training ran on custom Azure supercomputers
- All inference ran on Azure infrastructure
- The OpenAI API was served through Azure
- Azure built purpose-built hardware specifically for OpenAI
- Microsoft and OpenAI co-designed multiple supercomputer generations

### The Relationship Begins Fraying (2024-2025)

- OpenAI partnered with **Oracle** for additional compute (June 2024)
- Microsoft dropped its board observer seat (July 2024)
- OpenAI announced the **$500B Stargate project** (January 2025), ending Microsoft's exclusive cloud status
- OpenAI signed a **$38B AWS deal** (2025)
- OpenAI began using **Google TPUs** for some workloads again
- OpenAI executives reportedly discussed accusing Microsoft of anticompetitive behavior

Source: [TechCrunch (June 2025)](https://techcrunch.com/2025/06/16/the-cracks-in-the-openai-microsoft-relationship-are-reportedly-widening/)

---

## Datacenter Locations

| Period | Location | Purpose |
|--------|----------|---------|
| 2016-2017 | San Francisco (own office/datacenter) + AWS | Early research, on-prem GPU cluster |
| 2017-2019 | Azure + own datacenters (hybrid) | Kubernetes hybrid model |
| 2019-2023 | **West Des Moines, Iowa** (Microsoft) | GPT-3 and GPT-4 training supercomputer |
| 2023+ | Multiple Azure regions | Expanded inference and training |

Iowa was chosen by Microsoft for: available land, skilled workforce, large fiber optic network, and reliable/renewable energy resources.

---

## Related Documents

- [[llm/models/gpt3/gpt3-to-chatgpt/gpt3.5-backstories|GPT-3.5 Backstories]] --- Includes the "test run" story and other behind-the-scenes context
- [[llm/models/gpt3/gpt3-to-chatgpt/overview|GPT-3 to ChatGPT Overview]] --- The model evolution timeline
- [[llm/models/gpt3/architecture|GPT-3 Architecture]] --- The base model
- [[llm/models/gpt3/training|GPT-3 Training]] --- Original training approach
