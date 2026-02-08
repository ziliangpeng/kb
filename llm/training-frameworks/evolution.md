# Training Framework Evolution

The evolution of frameworks and infrastructure for training large language models.

## Phase 1: Data Parallelism Only (pre-2019)

When models fit on a single GPU (GPT-1 at 117M, BERT at 340M), the only parallelism needed was **data parallelism** — replicate the model on every GPU, each processes a different batch, average the gradients. The key tools:

- **Horovod** (Uber, 2017) — made distributed data-parallel training easy across frameworks using ring all-reduce (adapted from Baidu's 2017 implementation). Achieved ~90% scaling efficiency on 128 GPUs.
- **PyTorch DistributedDataParallel (DDP)** — built into PyTorch, became the default for single-node multi-GPU training.
- **TensorFlow's MirroredStrategy** — TensorFlow's equivalent.

The underlying breakthrough was **ring all-reduce** (Baidu, Feb 2017) — replacing parameter servers with a communication pattern that distributes the bandwidth load evenly across all GPUs. This was quickly absorbed into NVIDIA's **NCCL** library and became the standard.

This was sufficient when your model fit in one GPU's memory. The problem starts when it doesn't.

## Phase 2: Breaking the Single-GPU Barrier (2018-2020)

Models got too big for one GPU. Multiple approaches to splitting the model emerged simultaneously:

**Pipeline Parallelism** — split the model by layer groups, place different groups on different GPUs, pipeline micro-batches through:

- **GPipe** (Google, Nov 2018) — synchronous with micro-batch pipelining. Simple semantics but suffers from "pipeline bubble" overhead (GPUs idle waiting).
- **PipeDream** (Microsoft/CMU, SOSP 2019) — asynchronous pipelining with better hardware utilization but more complex (multiple weight versions for staleness).

**Tensor Parallelism / Megatron-LM** (NVIDIA, Sep 2019) — split individual layers (weight matrices) across GPUs within a node. More communication-intensive (needs NVLink bandwidth) but more compute-efficient per step. Trained an 8.3B model on 512 V100s.

**ZeRO / DeepSpeed** (Microsoft, Oct 2019 paper, Feb 2020 release) — a fundamentally different approach: don't split the model computation, just eliminate the redundant memory copies in data parallelism. ZeRO partitions optimizer states (Stage 1), gradients (Stage 2), and parameters (Stage 3) across GPUs. Achieves the memory efficiency of model parallelism with the simplicity of data parallelism.

**Mesh-TensorFlow** (Google/Shazeer, Nov 2018) — a language for specifying distributed tensor computation on multi-dimensional meshes of processors (TPUs). Google's path to model parallelism, used to train T5 (11B). Tied to the TensorFlow/TPU ecosystem.

The key realization was that you need **3D parallelism** — tensor parallelism within a node (needs NVLink), pipeline parallelism across nodes, and ZeRO data parallelism across groups. **Megatron-DeepSpeed** combined the two main GPU-side frameworks and became the standard recipe for training 100B+ parameter models.

## Phase 3: Framework Divergence (2021-2022)

Different organizations went in fundamentally different directions.

### Google: TensorFlow → JAX

Google shifted its large-model training stack from TensorFlow to JAX over ~2019-2021. DeepMind announced the shift to JAX around 2020, building Haiku (neural network library), Optax (optimizers), and other JAX-based tools. Google Research built **T5X** (late 2021) as the JAX replacement for the Mesh-TensorFlow-based T5 codebase.

Google also built **Pathways** (announced Oct 2021 by Jeff Dean) — a distributed runtime that sits beneath JAX and orchestrates training across thousands of TPU chips using asynchronous distributed dataflow. **PaLM** (Apr 2022, 540B params) was the first major Pathways model, trained on 6,144 TPU v4 chips at 57.8% hardware FLOPs utilization.

Google also developed **Pax/Paxml** (2022) for internal large-scale training and **MaxText** (2023) as an open-source JAX reference implementation.

Google's approach is fundamentally **compiler-first**: JAX programs are pure functions that XLA compiles end-to-end, giving automatic SPMD parallelism, communication optimization, and memory planning. This is architecturally years ahead of PyTorch's `torch.compile` for distributed training.

### Meta: FairScale → FSDP → PyTorch Core

Meta built **FairScale** (Jul 2020), a PyTorch extension library implementing FSDP (Fully Sharded Data Parallel) — essentially ZeRO Stage 3 reimplemented as a native PyTorch `nn.Module` wrapper. FSDP was merged into **PyTorch core in v1.11** (Mar 2022). This was significant because it absorbed DeepSpeed's core innovation directly into the framework, reducing the need for a separate library.

### Open-Source Community: Megatron-DeepSpeed

The community built on Megatron-DeepSpeed:

- **GPT-NeoX** (EleutherAI, 2021-2022) — a fork of Megatron-LM augmented with DeepSpeed. Trained GPT-NeoX-20B (Feb 2022) and the Pythia model suite.
- **BLOOM 176B** (BigScience/HuggingFace, mid-2022) — trained on a separate Megatron-DeepSpeed fork on the Jean Zay supercomputer.

### NVIDIA: NeMo

**NeMo** (originally released 2019 for conversational AI) integrated Megatron-LM in 2021, becoming NVIDIA's end-to-end framework for large model training. NeMo wraps Megatron-LM (now via Megatron-Core) with data preprocessing, fine-tuning recipes, and deployment tools. Megatron-LM is the engine; NeMo is the full car.

### OpenAI: Triton

**Triton** (OpenAI, Jul 2021) — a Python-like language for writing GPU kernels. Became hugely important when **PyTorch 2.0** (Mar 2023) adopted it as the backend for `torch.compile` / TorchInductor. Now every PyTorch 2.x user indirectly uses Triton. Also critical for AMD GPU support (via ROCm).

### HuggingFace: The Democratization Layer

HuggingFace built the most widely used stack for fine-tuning and moderate-scale training: **Transformers** (model hub) + **Accelerate** (Apr 2021, unified interface to FSDP/DeepSpeed) + **PEFT** (late 2022, LoRA and friends) + **TRL** (RLHF/DPO training). Not designed for frontier pre-training, but the go-to for everything else.

### MosaicML / LLM Foundry

**LLM Foundry** (May 2023) — production-ready open-source training code released alongside MPT-7B. Built on MosaicML's Composer library. One of the first high-quality, commercially usable open-source training frameworks. Databricks acquired MosaicML for $1.3B (Jul 2023).

## Phase 4: PyTorch 2.0 and the Compiler Era (2023-2024)

**PyTorch 2.0** (Mar 2023) introduced `torch.compile`, which uses TorchInductor to generate optimized Triton kernels for GPU execution. This brought compiler-based optimization to PyTorch for the first time — automatic kernel fusion, memory layout optimization, and reduced Python overhead.

For single-GPU and basic DDP/FSDP workloads, `torch.compile` delivers 1.5-2x speedups. However, as of mid-2025, it's still limited for advanced distributed training — DTensor + dynamic shapes + compile is "not well supported" (per Edward Yang at Meta). JAX/XLA remains ahead for compile-driven parallelism.

**Context parallelism** emerged as a standard 4th dimension of parallelism (alongside TP, PP, DP) for training with long sequences. Llama 3 used CP=16 for 128K context training, with each GPU processing 8K tokens.

**Expert parallelism** became critical as MoE architectures gained traction. Unlike the all-reduce operations used in dense training, MoE requires **all-to-all communication** for routing tokens to experts across GPUs — a fundamentally different communication pattern.

This brought the field to **4D parallelism**: tensor parallelism + pipeline parallelism + context parallelism + data parallelism (FSDP). For MoE models, expert parallelism adds a 5th dimension.

## Phase 5: Custom Frameworks and Frontier Divergence (2025-2026)

### What Frontier Labs Actually Use

Every frontier lab now runs a custom framework:

- **Meta (Llama 3/4)**: Custom stack built on FSDP + TP + PP + CP. Trained Llama 3 405B on 16K H100 GPUs. Llama 4 added a fully asynchronous online RL framework for post-training, decoupling policy, reward, and other components across separate GPU allocations.
- **DeepSeek (V3)**: Custom **HAI-LLM** framework on 2,048 H800 GPUs. Introduced **DualPipe** — a novel bidirectional pipeline parallelism algorithm that overlaps computation and communication. Used 16-way PP + 64-way EP + ZeRO-1 DP. Custom all-to-all kernels to saturate both InfiniBand and NVLink simultaneously.
- **Google (Gemini)**: JAX + XLA + Pathways on TPUs. The compiler-first approach.
- **ByteDance**: **MegaScale-MoE** (EuroSys 2026) — fine-grained operator decomposition for overlapping all-to-all with compute. Achieved 1.88x higher MFU than Megatron-LM on 1,440 Hopper GPUs.

None of them use off-the-shelf Megatron-DeepSpeed anymore.

### PyTorch Ecosystem Evolution

**FSDP2** replaced FSDP1 as the standard — built on DTensor with per-parameter sharding, ~7% less memory, and support for float8 all-gathers (up to 50% speedup on large models).

**SimpleFSDP** (experimental) is a compiler-based FSDP using `torch.compile` for full graph tracing. Shows 28% memory reduction and 68% throughput gain over FSDP2 eager. This is the future direction — making FSDP a compiler pass rather than an eager-mode runtime.

**TorchTitan** (Meta, ICLR 2025) is becoming the PyTorch reference implementation for LLM pre-training. Implements 4D parallelism using pure PyTorch APIs (DTensor, DeviceMesh, FSDP2). Supports Llama 3.1 models out of the box.

### DeepSpeed's Shifting Position

DeepSpeed was donated to the **Linux Foundation** (Feb 2025). Still actively maintained (v0.18.5, Jan 2026) with innovations like DeepCompile (torch.compile integration) and Arctic Long Sequence Training. But its core ZeRO innovation has been absorbed into PyTorch FSDP, narrowing its unique advantage. Strongest remaining niche: memory-constrained training with CPU/NVMe offloading, and as a plug-and-play solution via HuggingFace Accelerate.

### NVIDIA NeMo Restructuring

NeMo 2.0 (May 2025) is being deprecated in favor of two focused libraries:

- **NeMo AutoModel**: DTensor-native, for quick experiments and small-scale fine-tuning with HuggingFace model support.
- **NeMo Megatron-Bridge**: For massive-scale pre-training using Megatron-Core. Includes bidirectional conversion between HuggingFace and Megatron checkpoint formats.

### FP8 and Beyond

**FP8 training is now production-standard** — both DeepSeek-V3 and Llama 4 trained in FP8. NVIDIA's Blackwell architecture adds hardware FP4 support, with 3.2x faster training than Hopper FP8 on Llama 3.1 405B.

### The Central Optimization Problem

The biggest performance gains now come from **communication-computation overlap** — hiding the communication latency behind useful compute. DualPipe (DeepSeek), MegaScale-MoE's operator-level scheduling, SimpleFSDP's compiler-based reordering all target this. As models scale with more experts across more nodes, the ratio of communication to computation becomes the dominant bottleneck.

## Summary: The Two Paths

The training framework world has split into two philosophical camps:

**Compiler-first (Google/JAX)**: Write pure functions, let the compiler figure out parallelism, communication, and memory. Elegant, powerful, but tied to the JAX/XLA/TPU ecosystem.

**Eager-first with gradual compilation (PyTorch)**: Start with flexible eager-mode code, add distributed wrappers (FSDP, TP), and increasingly use `torch.compile` to optimize. More accessible, more ecosystem, but playing catch-up on the compiler story. SimpleFSDP and TorchTitan represent the convergence toward more compilation.

In practice, frontier labs transcend both — they build custom frameworks that combine hand-optimized kernels, custom communication patterns, and whatever compiler support helps, tailored to their specific model architecture and hardware topology.
