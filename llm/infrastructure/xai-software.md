# xAI Software Infrastructure

The software stack behind xAI's training and inference systems — JAX, Rust, Kubernetes, and the engineering that makes 100K+ GPU training work.

## The Stack

```
ML Framework:     JAX + dm-haiku
Control Plane:    Rust
Orchestration:    Kubernetes
Languages:        Python (ML), Rust (infra/backend), C++, Go
IaC:              Pulumi (primary), Terraform, Ansible
GitOps:           Flux, ArgoCD
Backend (grok.com): Rust or C++
Databases:        PostgreSQL, ClickHouse, CockroachDB
Communication:    gRPC (unary, streaming, bidirectional)
Inference:        SGLang (confirmed for Grok-2)
```

## JAX + dm-haiku

xAI uses **JAX** as the core ML framework, confirmed by:

- The [Grok-1 open-source repository](https://github.com/xai-org/grok-1): "trained from scratch by xAI using a custom training stack on top of JAX and Rust"
- The [Grok-1.5 announcement](https://x.ai/news/grok-1.5): "custom distributed training framework based on JAX, Rust, and Kubernetes"
- Igor Babuschkin's GTC 2024 talk: ["Scaling Grok with JAX and H100"](https://www.nvidia.com/en-us/on-demand/session/gtc24-s63257/)

The specific JAX library is **dm-haiku** (v0.0.12) — DeepMind's neural network library, NOT Flax. This aligns with the co-founders' DeepMind backgrounds (Babuschkin, Pohlen, Kroiss, Zhang all came from DeepMind).

### Why JAX Over PyTorch

xAI has not published an explicit rationale, but the reasons are clear:

- **Team expertise**: The founding team was heavily ex-DeepMind, where JAX is the primary framework
- **Composable parallelism**: JAX's `pjit` and `shard_map` map naturally to large GPU meshes. The Grok-1 code uses `PartitionSpec` for sharding across data and model axes.
- **XLA compilation**: JIT compilation via XLA provides hardware-level optimization for H100 GPUs
- **Functional purity**: Makes it easier to reason about distributed computation and automatic differentiation

### What Grok-1's Code Reveals

The open-source release (Apache 2.0, March 2024) is remarkably minimal — only 4 dependencies: JAX, Haiku, SentencePiece, NumPy. The code structure:

- `model.py` (~1,400 lines): All architecture code — Router, MoELayer, MultiHeadAttention, DecoderLayer, Transformer, RMSNorm, RotaryEmbedding
- `checkpoint.py`: Weight loading
- `run.py`: Inference entry point using `pjit.pjit`

**Distributed inference**: Uses `pjit` and `shard_map` for multi-device inference, with `PartitionSpec` for data/model axis sharding. Device mesh configured via `local_mesh_config` (within-host) and `between_hosts_config`.

**MoE implementation**: xAI explicitly noted the open-source MoE implementation is "not efficient" and was "chosen to avoid the need for custom kernels to validate the correctness of the model." The production training code likely uses custom CUDA/XLA kernels not included in the release.

**What was NOT released**: Training code, Rust control plane, Kubernetes orchestration, checkpointing system, data pipeline, RL/RLHF code.

## The Rust Control Plane

Rust is used extensively for non-ML infrastructure:

- **Training orchestration**: The Rust control plane orchestrates training jobs, monitors node health, and automates failure recovery. This is the critical reliability layer that sits between the ML training loop and the physical cluster.
- **Backend services**: The entire grok.com and API backend is built in Rust
- **Containerized infrastructure**: Job postings consistently require "writing scalable and highly available containerized applications in Rust"

Rust was chosen for its reliability, performance, and memory safety guarantees — critical when operating at 100K+ GPU scale where a bug in the orchestration layer can waste enormous compute.

## Distributed Training

### Three-Layer Architecture

1. **JAX modeling/training layer**: Provides composable parallelism primitives via `pjit` for model sharding and `shard_map` for distributed operations
2. **Rust control plane**: Orchestrates training jobs, monitors node health, automates failure recovery
3. **Kubernetes**: Manages scheduling and resource allocation across the cluster

### Parallelism

Confirmed from the Grok-1 code and infrastructure analyses:

- **Tensor parallelism**: Partitioning model weights across GPUs (likely within a node's 8 GPUs connected via NVLink)
- **Data parallelism**: Across nodes
- **Expert parallelism**: Native to the MoE architecture with top-2 expert routing

The **homogeneous cluster design** (thousands of identical 8-GPU nodes) "simplifies sharding strategies, fault detection and orchestration."

## Failure Recovery

At 100K+ GPU scale, failures are frequent. xAI's Grok-1.5 announcement described the challenge: "LLM training runs like a freight train thundering ahead; if one car derails, the entire train is dragged off the tracks."

### Solutions

- **Automatic node ejection**: The custom training orchestrator "automatically ejects problematic nodes from a training job" — no manual intervention required
- **Babuschkin's scheduling framework**: Igor Babuschkin personally wrote the scheduling system that reduced **interruption recovery time from 30 minutes to 90 seconds** — critical when failures happen multiple times per hour at this scale
- **Optimized checkpointing**: "Saving and restoring hundreds of gigabytes of parameters and optimizer states must be done incrementally and resiliently, or a single node failure can stall the entire run"
- **RDMA troubleshooting**: During the Memphis buildout, the team hit issues with RDMA communication between machines. Musk flew to the data center personally to help troubleshoot.

### GPU Failure Modes

xAI listed the types of failures encountered: manufacturing defects, loose connections, incorrect configuration, degraded memory chips, and random bit flips. At 100K+ GPU scale, these become frequent enough to require fully automated detection and recovery.

## muP (Maximal Update Parameterization)

Co-founder **Greg Yang** created muP, which assigns per-parameter hyperparameters (learning rate, initialization) so that optimal hyperparameters found on small "proxy" models transfer directly to large models. In one demonstration, a 200-sample search on a 40M model produced hyperparameters achieving GPT-3 6.7B-level performance — roughly **2x compute savings**.

Evidence in the Grok-1 codebase: multipliers consistent with muP-style scaling. Greg Yang's presence as co-founder makes it near-certain muP is deeply embedded in xAI's training pipeline. This is likely critical to their efficiency — allowing hyperparameter tuning on small models before committing to expensive runs on 100K+ GPUs.

## Inference: SGLang

Igor Babuschkin posted (August 2024) that Grok 2 mini was made **2x faster** after Lianmin Zheng and Saeed Maleki rewrote the inference stack from scratch using **SGLang** in 3 days, enabling multi-host inference for the larger Grok 2 model.

## Grok-4's RL Innovation

Grok-4 scaled RL compute **10x compared to Grok-3's RL stage**, approaching pretraining-scale investment. Infrastructure and algorithmic innovations increased compute efficiency by **6x**. Two key approaches:

- **Verifiable rewards (RLVR)**: Removes the reward model entirely for domains with verifiable answers. Model attempts problems hundreds/thousands of times; only correct solutions receive reward. Expanded from math/coding (Grok-3) to many domains (Grok-4).
- **Model-based graders**: For open-ended tasks without deterministic verification, uses frontier reasoning models as autonomous reward models at scale. A production example of model-based supervision in a closed-loop training system.

This differs from competitors: OpenAI uses outcome-based RL with RLHF; Anthropic uses Constitutional AI (automated feedback from principles); DeepSeek uses GRPO (Group Relative Policy Optimization) with verifiable rewards.

## What's Not Publicly Known

- Whether they fork or modify JAX
- Specifics of the Rust control plane architecture (beyond "orchestrates training, monitors health, automates recovery")
- Checkpointing frequency, synchronous vs. asynchronous approach
- Whether the 4 computing halls operate as a single training domain or independent 25K-GPU clusters
- Custom CUDA/XLA kernels used in production training (the open-sourced MoE code is explicitly not the efficient version)
- Details of the data pipeline and preprocessing

## External References

- [GitHub — xai-org/grok-1](https://github.com/xai-org/grok-1) — Open-source model code (JAX + Haiku)
- [xAI — Grok-1.5 Announcement](https://x.ai/news/grok-1.5) — Describes JAX/Rust/Kubernetes framework
- [NVIDIA GTC 2024 — Scaling Grok with JAX and H100](https://www.nvidia.com/en-us/on-demand/session/gtc24-s63257/) — Igor Babuschkin talk
- [Igor Babuschkin on X — SGLang Rewrite](https://x.com/ibab/status/1827047684714463603) — Grok 2 inference 2x speedup
- [Igor Babuschkin Farewell Post](https://x.com/ibab/status/1955741698690322585) — Scheduling framework, RDMA troubleshooting
- [xAI — Grok 4 Announcement](https://x.ai/news/grok-4) — RL at pretraining scale
- [Epoch AI — Grok 4 Training Resources](https://epoch.ai/data-insights/grok-4-training-resources) — Training cost/compute analysis
- [Interconnects — Grok 4 Analysis](https://www.interconnects.ai/p/grok-4-an-o3-look-alike-in-search) — Nathan Lambert's RL comparison
- [SemiAnalysis — xAI Colossus 2](https://newsletter.semianalysis.com/p/xais-colossus-2-first-gigawatt-datacenter) — "Unique RL methodology"
