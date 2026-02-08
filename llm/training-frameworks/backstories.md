# Training Framework Backstories

The human stories, motivations, and context behind the major training frameworks.

## Megatron-LM (NVIDIA, 2019)

### The Baidu Reunion

The Megatron-LM team was largely a reunion of researchers from **Baidu's Silicon Valley AI Lab (SVAIL)** — the lab founded by Andrew Ng. When Ng left Baidu in 2017, many of these researchers ended up at NVIDIA:

- **Bryan Catanzaro** (VP, Applied Deep Learning Research) — had been at NVIDIA early (2008), helped create cuDNN, left for Baidu, then Jensen Huang personally called him back in 2016 to found the ADLR (Applied Deep Learning Research) lab. He was the only member when the lab started. By 2019, it had grown to ~40 researchers; by 2024, ~500.
- **Mohammad Shoeybi** — PhD from Stanford in Mechanical Engineering / Computational Fluid Dynamics. A notable pivot from aerospace to deep learning. Previously at DeepMind and Baidu USA.
- **Mostofa Patwary** — from Bangladesh (BUET), PhD from University of Bergen. Previously at Baidu SVAIL.
- **Patrick LeGresley** — PhD from Stanford in Aeronautics and Astronautics. Another aerospace-to-AI pivot. Also a Baidu SVAIL alum.
- **Jared Casper** — PhD from Stanford in Computer Architecture. Baidu SVAIL.
- **Raul Puri** — BS from UC Berkeley. Later went to OpenAI.

### Strategic Motivation

Catanzaro has been candid: Megatron-LM was simultaneously a research contribution, a product demonstration, and an ecosystem play. The project explicitly **countered assertions from competitors that large language models required non-NVIDIA hardware** (likely a reference to Google's TPUs). By open-sourcing it, NVIDIA made their GPUs the default choice — expanding AI adoption benefits their core GPU business.

### The Name

"Megatron" is a reference to the villain from the Transformers franchise — the team was building "the biggest and baddest transformer."

### Why It Worked

The technical elegance was key: tensor parallelism was implemented as just **a few all-reduce operations inserted into standard PyTorch code**. No new compiler, no new library, no code restructuring. The MLP block is split column-wise for the first linear layer and row-wise for the second, requiring only one all-reduce per forward/backward pass. This simplicity is what made it so widely adopted.

---

## DeepSpeed / ZeRO (Microsoft, 2019-2020)

### The Team

The core team sat within **Microsoft Research** but was unusually product-oriented — their work powered Bing, Office, Dynamics, Azure, and Ads:

- **Yuxiong He** (Partner Research Manager) — led the team. Background in performance optimization of parallel/distributed systems.
- **Samyam Rajbhandari** — PhD from Ohio State in communication-optimal tensor contraction algorithms. System architect for DeepSpeed and lead author of the ZeRO paper.
- **Jeff Rasley** — PhD from Brown. Did multiple internships at MSR before joining full-time. Became DeepSpeed's top code contributor.
- **Olatunji (Tunji) Ruwase** — PhD from CMU under Todd Mowry. Background spanning compilers, OS, and hardware accelerators.

### The ZeRO Insight

The insight was deceptively simple: in standard data parallelism with mixed-precision Adam, every GPU redundantly stores 16 bytes per parameter (2B params fp16, 2B gradients fp16, 12B optimizer states fp32). With 64 GPUs, you have 64 identical copies. ZeRO partitions these across GPUs instead of replicating them, then communicates the needed pieces just-in-time. Stage 1 alone gives ~4x memory reduction with **zero additional communication** over standard data parallelism.

### Built for Microsoft, Not OpenAI

A common misconception is that Microsoft built DeepSpeed for OpenAI. It wasn't. **DeepSpeed was built for Microsoft's own AI models** — the **Turing model family** that powered Bing, Office, Dynamics, and Ads. Microsoft's AI strategy had two separate, parallel arms:

1. **Invest in OpenAI** ($1B in 2019) and provide Azure compute — OpenAI builds their own training stack
2. **Build Microsoft's own AI models** (Turing family) using DeepSpeed — for Microsoft's products

DeepSpeed was open-sourced in February 2020 alongside **Turing-NLG (17B)** — Microsoft's own model, not OpenAI's. This was a deliberate launch strategy: demonstrate the technology with a record-breaking model, then release the tools. DeepSpeed made Turing-NLG trainable with 4x fewer GPUs and 3x higher throughput compared to Megatron alone.

**OpenAI never used DeepSpeed.** They built fully custom training infrastructure — Jeffrey Wu implemented the model-parallel strategies for GPT-3, with Mark Chen and Rewon Child prototyping an early version. OpenAI had deep in-house infrastructure expertise going back to their Kubernetes-based cluster management (2016-2017), custom CUDA kernels (blocksparse library), and the Rapid distributed training platform built for OpenAI Five. Microsoft provided the hardware (10,000 V100s on Azure); OpenAI provided the software.

### The Arc: Build, Open-Source, Get Absorbed, Move On

DeepSpeed's greatest impact was probably on the **open-source community** rather than on either Microsoft's own models or OpenAI's. BLOOM 176B (BigScience), GPT-NeoX 20B (EleutherAI), and countless HuggingFace fine-tuning workflows all ran on DeepSpeed. But its core innovation (ZeRO) was reimplemented by Meta as **PyTorch FSDP** and merged into PyTorch core — absorbing DeepSpeed's unique advantage into the platform itself.

In late 2023, the entire core team left Microsoft together for **Snowflake** to build AI infrastructure for their data cloud:

- Yuxiong He → Distinguished Engineer at Snowflake
- Samyam Rajbhandari → Principal Architect
- Jeff Rasley → Senior Engineer, AI Research
- Olatunji Ruwase → Principal Software Engineer (continues as Lead of the DeepSpeed Project)

They were involved in building **Snowflake Arctic** and other AI initiatives. After the founders left, Microsoft donated DeepSpeed to the **Linux Foundation** (Feb 2025), then the **PyTorch Foundation** (May 2025). The GitHub org moved from `microsoft/DeepSpeed` to `deepspeedai/DeepSpeed`.

The full arc is a common pattern in infrastructure: internal team builds tool for internal needs → open-source for ecosystem adoption → it becomes widely used → the core innovation gets absorbed into the platform → the founding team moves on → the project gets donated to a foundation for community maintenance.

---

## Horovod (Uber, 2017)

### NCCL and the Ring All-Reduce Story

The timeline here is nuanced. **NCCL** (NVIDIA Collective Communications Library) existed first — NVIDIA released NCCL 1 around **2015** with single-node multi-GPU collective operations. But the conceptual breakthrough for deep learning came from **Baidu**.

In **February 2017**, **Andrew Gibiansky** at Baidu's SVAIL published a blog post on bringing HPC techniques to deep learning. The key idea: replace **parameter servers** (which create networking bottlenecks) with **ring all-reduce** (a well-known HPC technique where GPUs communicate only with neighbors in a logical ring, achieving bandwidth-optimal gradient synchronization). Baidu demonstrated near-linear scaling across 40 GPUs. Gibiansky is currently at OpenAI.

### Uber's Pain

**Alexander Sergeev** (studied AI in Moscow, previously at Microsoft Bing) joined Uber to support self-driving car perception training. They went through three iterations:

1. Users packaged code and waited 10 minutes for results. Cumbersome.
2. Interactive training with TensorFlow parameter servers. "Even the engineers who built it were struggling with using it."
3. **Horovod** — adopted Baidu's ring all-reduce, using **NCCL as the communication backend** underneath, but wrapping it in a user-friendly API requiring only **4 modifications** to single-GPU code.

The name comes from a **traditional Russian folk dance** where performers dance with linked arms in a circle — a metaphor for distributed processes communicating in a ring.

### Success and Absorption

Horovod achieved 88% scaling efficiency on 128 GPUs, roughly double standard distributed TensorFlow. Meanwhile, **NCCL 2** (2017) added multi-node support and incorporated optimized ring all-reduce algorithms, partly influenced by the Baidu/Horovod work. Eventually PyTorch DDP built directly on the improved NCCL, making Horovod's wrapper layer unnecessary. By 2024, Horovod was classified as an inactive project. The pattern: NCCL was the low-level plumbing from the start, Baidu/Horovod popularized ring all-reduce for deep learning on top of it, then NCCL absorbed those optimizations and PyTorch built directly on NCCL — making the middle layer redundant.

---

## JAX (Google, 2018+)

### From Harvard Autograd to Google

JAX's story begins at Harvard, in Ryan Adams' HIPS group. **Dougal Maclaurin** (physics PhD student) built **Autograd** — a Python library for automatic differentiation of native Python/NumPy code. Key contributors included **David Duvenaud**, **Matt Johnson**, and **Jamie Townsend**.

Matt Johnson and Maclaurin both ended up at **Google Brain**, joined by **Roy Frostig** (Stanford) and **Chris Leary** (XLA compiler engineer). The key insight: combine Autograd's elegant AD with Google's **XLA compiler**. The result was simultaneously familiar (NumPy API), differentiable (Autograd-style), fast (XLA-compiled), and composable (function transformations: `jit`, `grad`, `vmap`, `pmap`).

JAX was open-sourced in **December 2018**. The name stands for **"Just After eXecution"**.

A remarkable footnote: **Adam Paszke**, one of the original creators of PyTorch, left Meta and joined Google in **March 2020** to work on JAX-related projects. Having a co-creator of PyTorch move to work on JAX speaks to its technical appeal.

### The TensorFlow-to-JAX Shift

The shift was partly an admission that TensorFlow had lost the research war. TF 1.x's static graph paradigm was widely disliked. PyTorch captured researchers' hearts with eager execution. Google tried to fix this with TF 2.0 (2019), but the damage was done — by 2022, only ~14% of HuggingFace models supported TensorFlow.

Rather than making TensorFlow compete with PyTorch, Google pivoted to JAX — a fundamentally different approach playing to Google's strengths (TPU hardware, XLA compiler). The philosophical bet: by constraining programs to be **functionally pure**, you unlock composable transformations (differentiate, JIT, vectorize, parallelize) that a compiler can optimize end-to-end.

**DeepMind** was an early enthusiastic adopter, building Haiku, Optax, RLax, and other JAX libraries starting ~2020. Their organizational independence (they had always used their own Sonnet layer API rather than Keras) made the JAX switch easier. **AlphaFold 2** (2020-2021) used JAX for the core computation.

By 2022, all major new Google models (PaLM, Gemini) were JAX-based. Beyond Google, JAX has been adopted by **Anthropic**, **xAI**, and **Apple**.

---

## Pathways (Google, 2021)

### The Grand Vision

In **October 2021**, Jeff Dean published an ambitious blog post laying out three problems with existing AI: single-purpose models, single-modality, and dense/inefficient activation. Pathways would solve all of them with one model handling thousands of tasks, natively multimodal, with sparse activation where "only small pathways through the network are called into action."

The systems paper was led by **Paul Barham** and included heavyweights like Jeff Dean and **Sanjay Ghemawat** (co-creator of MapReduce, GFS, BigTable).

### What Actually Shipped vs. What Was Promised

**Pathways the infrastructure system** (distributed TPU orchestrator) genuinely shipped and works. PaLM (Apr 2022) was the first large-scale use — 540B params across 6,144 TPU v4 chips. Gemini models also use it.

**Pathways the AI vision** was overpromised. Gemini 1.0 was a **dense model**, not sparsely activated. Gemini 1.5 adopted MoE (closer to the sparse vision), but MoE was already well-known, not novel Pathways-style routing. The "one model, many tasks" vision essentially became... large language models, which the entire industry converged on independently.

In practice, Pathways is the infrastructure layer beneath JAX — when you run JAX at scale on TPU pods, Pathways orchestrates the distributed computation.

---

## Triton (OpenAI, 2021)

### Philippe Tillet's Journey

**Philippe Tillet** has a remarkable trajectory through GPU computing:

- **2011**: Contributor to ViennaCL (open-source linear algebra on CUDA/OpenCL)
- **2012**: B.S. from Telecom SudParis (France)
- **2014**: M.S. from NCTU (Taiwan)
- **2014-2020**: PhD at Harvard with H.T. Kung and David Cox

The critical moment came in 2018 during his PhD. Tillet was writing auto-tuners for matrix multiplications in CUDA and became deeply frustrated. Writing efficient GPU code required simultaneously managing memory coalescing, shared memory staging, thread block scheduling, bank conflicts — all manually. His research question: **what if you operate on "tiles" (multi-dimensional sub-arrays) instead of individual threads, and let a compiler handle the low-level optimization?**

### From PhD to OpenAI to PyTorch's Backbone

Tillet joined OpenAI full-time in 2020. His colleagues' constant experimentation with novel architectures "stressed his compiler to the limit," motivating rapid iteration. He described himself as "the power user" of his own compiler.

OpenAI released Triton in **July 2021**. The headline: FP16 matrix multiplication matching cuBLAS performance in **under 25 lines of Python-like code**.

The pivotal development: when Meta built **PyTorch 2.0** (Mar 2023), they chose Triton as the code generation backend for **TorchInductor** because "users were already writing high-performance custom kernels using the Triton language." Now every PyTorch 2.x user indirectly uses Triton.

### Breaking the CUDA Moat

Triton compiles through **LLVM**, not directly to CUDA, meaning it can target NVIDIA (NVPTX), AMD (AMDGPU), and Intel GPUs. Since PyTorch's TorchInductor generates Triton code, and Triton can compile to AMD GPUs via ROCm, **PyTorch models can run on AMD hardware through torch.compile without AMD-specific kernels**. This is strategically the most important crack in NVIDIA's CUDA ecosystem lock-in.

---

## FairScale → FSDP (Meta, 2020-2022)

### The Strategic Reimplementation of ZeRO

Meta's FSDP was **explicitly inspired by ZeRO Stage 3** — the documentation acknowledges this directly. But Meta reimplemented it rather than using DeepSpeed for strategic reasons:

1. **Ecosystem ownership**: Meta owns PyTorch. Depending on Microsoft's library for a core training capability would cede control to a competitor.
2. **Technical integration**: FSDP manipulates PyTorch's autograd graph directly as a native `nn.Module` wrapper, rather than being an external engine.
3. **Production needs**: Meta was training massive models internally and needed tight infrastructure integration.

### The Team

**FairScale** (Jul 2020) was built by Myle Ott, Sam Shleifer, Min Xu, Priya Goyal, and others at FAIR. Notably, **Myle Ott** was one of the original authors of fairseq and later became part of the founding team at **Character AI**.

**PyTorch FSDP** was upstreamed to PyTorch 1.11 (Mar 2022) by a 17+ person team including Yanli Zhao, Andrew Gu, Rohan Varma, Less Wright, and others.

### The FSDP2 Rewrite

**Andrew Gu** led the ground-up rewrite. FSDP1's core abstraction (FlatParameter — concatenating multiple parameters into a flat tensor) made it nearly impossible to freeze individual parameters, apply mixed precision, or generate sharded checkpoints cleanly. FSDP2 replaced this with **DTensor**-based per-parameter sharding (spearheaded by **Wanchao Liang**), reducing the codebase from ~14K to ~3K lines of non-test code.

---

## HuggingFace

### From Chatbot to ML Platform

HuggingFace was founded in **2016** in New York by three French entrepreneurs:

- **Clement Delangue** (CEO)
- **Julien Chaumond** (CTO)
- **Thomas Wolf** (CSO) — trained scientist who became a patent lawyer

Chaumond and Wolf knew each other from **a band they played in together**. The three reconnected through an online Stanford engineering course. Their first product was a **consumer chatbot app targeting teenagers** — an "AI best friend." Named after the hugging face emoji.

### The BERT Pivot

The transformative moment came in **late 2018** when Google released BERT. Thomas Wolf produced a **PyTorch implementation of BERT within a week** (`pytorch-pretrained-bert`). Google's BERT was TensorFlow-only, and the PyTorch community was hungry for an implementation. The repo rapidly gained thousands of stars. This "clarified the company's direction" — HuggingFace pivoted from consumer chatbot to open-source ML infrastructure. The chatbot was discontinued by 2019.

The library evolved: `pytorch-pretrained-bert` → `pytorch-transformers` (mid 2019, added GPT/GPT-2/XLNet) → `Transformers` (late 2019, added TF support). The Hub grew to **2.4+ million models** by January 2026.

### Sylvain Gugger: Math Teacher to Accelerate Creator

**Sylvain Gugger** was a **mathematics and computer science teacher in France for seven years**, teaching in CPGE (prep courses for France's elite engineering schools). ENS Paris alumnus. Wrote **10 math textbooks**. Discovered deep learning through **fast.ai's MOOC** by Jeremy Howard, joined fast.ai as a research scientist, co-authored "Deep Learning for Coders with fastai and PyTorch," then joined HuggingFace.

He created **Accelerate** (Apr 2021) with a pragmatic design philosophy: **5 lines of code** to make any PyTorch training script work across CPU, single GPU, multi-GPU, TPU, and mixed precision. He left HuggingFace in August 2023.

### TRL: Side Project to RLHF Standard

**Leandro von Werra** (physics background, data scientist, lives in Bern, Switzerland) started TRL in **2020** as a **personal reproduction project** — he wanted to reproduce OpenAI's "Fine-Tuning Language Models from Human Preferences" using PPO to learn NLP. After ChatGPT made RLHF a hot topic in late 2022, TRL became the go-to open-source library for alignment training (15K+ GitHub stars, 1M+ monthly pip installs). Von Werra is now Head of Research at HuggingFace.

### PEFT: Making Fine-Tuning Affordable

**Sourab Mangrulkar** led the creation of **PEFT** (late 2022), which made LoRA trivially easy to use. Instead of fine-tuning all parameters (requiring cluster-scale GPUs), LoRA trains only ~0.19% of parameters. This meant researchers with consumer GPUs could fine-tune models that previously required clusters.

---

## TorchTitan (Meta, 2024-2025)

### 7,000 Lines vs. 93,000

The core team was led by **Wanchao Liang** (Tech Lead, PyTorch Distributed at Meta), with leadership acknowledgments to **Soumith Chintala** (PyTorch creator). The team identified that Megatron-LM had grown to **93,000 lines of code** with non-composable abstractions. TorchTitan implements the same 4D parallelism (TP + PP + CP + FSDP) in **7,000 lines** using pure PyTorch APIs (DTensor, DeviceMesh, FSDP2).

The key insight: the root cause of non-composability in existing frameworks was the absence of unified tensor and device abstractions. DTensor and DeviceMesh (both developed by the PyTorch distributed team) provided exactly this foundation.

Accepted at **ICLR 2025**. Performance: 65% acceleration on Llama 3.1 8B (128 GPUs), 30% on 405B (512 GPUs) over optimized baselines.

---

## Recurring Themes

**The Baidu diaspora**: Both Megatron-LM (NVIDIA) and the ring all-reduce concept (Baidu → Horovod) trace back to Baidu's Silicon Valley AI Lab under Andrew Ng. When the lab wound down, its alumni seeded key infrastructure projects across the industry.

**Blog posts as catalysts**: Gibiansky's ring all-reduce post, Wolf's BERT implementation tweet — single publications triggered ecosystem shifts.

**Side projects becoming infrastructure**: Von Werra's TRL reproduction project, Horovod as an internal Uber tool, Tillet's PhD frustration → Triton. The most impactful tools often start as someone scratching their own itch.

**Non-traditional backgrounds**: Gugger (math teacher), von Werra (physics → insurance), Shoeybi and LeGresley (aerospace engineering), Wolf (patent lawyer). The training framework world was built by people who pivoted into ML.

**Absorption as success**: Horovod's ring all-reduce → absorbed into NCCL/PyTorch DDP. ZeRO → absorbed into PyTorch FSDP. Triton → absorbed into PyTorch 2.0. The most successful innovations become part of the platform and the original library fades.

**Strategic reimplementation**: Meta reimplemented ZeRO as FSDP not primarily from NIH syndrome but because owning core distributed training in PyTorch was existentially important. Google built JAX rather than fixing TensorFlow. Frontier labs all build custom frameworks rather than using off-the-shelf tools.
