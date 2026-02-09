# LLM Architecture Evolution

The technical evolution of decoder-only transformer architectures from 2017 to present, focusing on architectural innovations and training infrastructure.

For model releases, company movements, and market dynamics, see [[llm/industry-timeline|LLM Industry Timeline]].

## 2017: The Original Transformer

"Attention Is All You Need" (Vaswani et al.) introduced the Transformer as an encoder-decoder model for machine translation. The key innovation: **self-attention** replacing recurrence entirely, allowing every token to attend to every other token in parallel. This eliminated the sequential bottleneck of RNNs/LSTMs and enabled massively parallel training on GPUs.

The architecture established all the core components that remain today: Q/K/V attention, multi-head attention, feed-forward networks, residual connections, and layer normalization. See [[llm/original-transformer-architecture]] for full details.

## 2018: [[llm/models/gpt1/architecture|GPT-1]] — The Start of Decoder-Only

OpenAI took the Transformer decoder, dropped the encoder and cross-attention, and pre-trained it on unlabeled text with next-token prediction. 117M params, 12 layers. The idea: pre-train on lots of text, then fine-tune for specific tasks. This was novel — before this, NLP models were typically trained from scratch per task.

## 2019: [[llm/models/gpt2/architecture|GPT-2]] — Scale Brings Zero-Shot Abilities

1.5B params. Same architecture but bigger. Key findings:

- The model could do tasks **zero-shot** (no fine-tuning, no examples) — just from the prompt
- Introduced **Pre-Norm** (LayerNorm before sublayers), which became standard because it trains more stably
- Showed that scale itself unlocks capabilities

## 2016-2019: Scaling Infrastructure

GPT-2 showed that scale unlocks capabilities, but getting to GPT-3 scale (175B params, ~10,000 GPUs) required a stack of infrastructure breakthroughs. The key innovations:

**Mixed-Precision Training** (NVIDIA, 2017): Training in FP16 with FP32 master weights. This roughly halves memory usage and doubles throughput on NVIDIA's Tensor Cores (introduced with the V100 GPU in 2017). Loss scaling prevents small gradients from underflowing to zero in FP16. Every large model training run uses this.

**Gradient Checkpointing** (Chen et al., 2016): Instead of storing all intermediate activations for backpropagation, save only periodic checkpoints and recompute the rest during the backward pass. Trades ~20-33% more compute for dramatically less memory — enabling 2-10x larger models per GPU. Universally adopted.

**Tensor Parallelism / Megatron-LM** (NVIDIA, Sep 2019): Splitting individual transformer layers across multiple GPUs. Before this, you were limited to models that fit on a single GPU's memory. NVIDIA demonstrated this by training an 8.3B parameter model (GPT-2 architecture, 5.6x larger) on 512 V100s. The released codebase also became a widely-used **training framework** (Megatron-LM) for large transformer models — Microsoft used it to train **Turing-NLG** (17B params, Feb 2020), which held the scale record until GPT-3. The collaboration later culminated in **Megatron-Turing NLG 530B** (Oct 2021), the largest dense language model at the time.

**ZeRO / DeepSpeed** (Microsoft, Oct 2019 paper, Feb 2020 release): In standard data parallelism, every GPU redundantly stores a full copy of optimizer states, gradients, and parameters — 16 bytes per parameter with Adam. ZeRO partitions this across GPUs: Stage 1 partitions optimizer states (~4x savings), Stage 2 adds gradients, Stage 3 adds parameters themselves. This achieves the memory efficiency of model parallelism with the simplicity of data parallelism. Combined with Megatron's tensor parallelism, this became the standard recipe for training 100B+ parameter models.

These four are the critical enablers, but the full stack included more: **NVIDIA V100 GPUs** (2017) with Tensor Cores provided the raw hardware; **NVLink/NVSwitch** (2016-2018) gave ~10-20x PCIe bandwidth for GPU-to-GPU communication, making tensor parallelism practical; **pipeline parallelism** (GPipe from Google 2018, PipeDream from Microsoft 2019) enabled splitting models by layer groups across nodes; **AdamW** (Loshchilov & Hutter, 2017) fixed Adam's weight decay and became the standard LLM optimizer; **learning rate warmup** (Goyal et al., 2017) made large-batch training stable; **NCCL and ring all-reduce** (NVIDIA/Baidu, 2017) provided efficient multi-GPU gradient synchronization; and **Google's TPU v2/v3** (2017-2018) offered an alternative hardware path with native bfloat16 support that powered BERT and T5.

## 2020: [[llm/models/gpt3/architecture|GPT-3]] — The Scaling Breakthrough

175B params. Validated the scaling hypothesis:

- **In-context learning**: give the model a few examples in the prompt and it can do the task, no fine-tuning needed
- Published **scaling laws** (Kaplan et al.): model performance improves predictably as a power law with compute, data, and parameters
- Architecturally identical to GPT-2, just much bigger. The lesson: at this stage, scale mattered more than architectural innovations
- Training infrastructure: Combined Megatron-LM (tensor parallelism) + DeepSpeed (ZeRO) to train on ~10,000 V100 GPUs

See [[llm/models/gpt3/backstories|GPT-3 Backstories]] for development context and market impact.

## 2022: Chinchilla — Fix the Scaling Recipe

DeepMind showed GPT-3 was **undertrained**. The Chinchilla paper demonstrated that for a fixed compute budget, you should scale parameters and training data roughly equally. GPT-3 had 175B params but was trained on only 300B tokens — Chinchilla used 70B params trained on 1.4T tokens and performed better.

**Key finding**: The optimal ratio is roughly 20 tokens per parameter. GPT-3 was trained on 1.7 tokens/param, well below optimal. Models after Chinchilla train on much more data relative to parameter count.

## 2022: PaLM — Architectural Refinements

Google's 540B param model introduced several refinements that became standard:

- **SwiGLU activation** in FFN (replacing ReLU) — a gated activation function that gives better performance
- **RoPE** (Rotary Positional Embeddings) — replaced sinusoidal positional encoding. Encodes position through rotation of Q/K vectors, naturally captures relative position, and extrapolates better to longer sequences
- **Parallel attention + FFN** — computing attention and FFN in parallel within each block instead of sequentially, for faster training
- **No bias terms** — removing bias parameters from linear layers, simplifies the model with negligible quality impact

## 2022: ChatGPT / InstructGPT — Post-Training Revolution

The base model is good at predicting text but bad at following instructions. OpenAI introduced a three-stage post-training pipeline:

1. **Supervised Fine-Tuning (SFT)** — train on (instruction, high-quality response) pairs
2. **Reward Model** — train a separate model to score responses by human preference
3. **RLHF** (Reinforcement Learning from Human Feedback) — use PPO to optimize the base model against the reward model

This is what turned "text predictor" into "useful assistant." Every chatbot since uses some version of this.

## 2023: LLaMA — The Open-Source Template

Meta's LLaMA (7B to 65B) consolidated the best known practices into one clean, open architecture:

- Pre-Norm with **RMSNorm** (simpler than LayerNorm, drops mean-centering)
- **SwiGLU** activation
- **RoPE** positional embeddings
- No bias terms
- Trained on more data per parameter (following Chinchilla)

This became the **de facto standard architecture** that nearly every open-source model follows: Llama 2, Llama 3, Mistral, Qwen, DeepSeek, Yi, etc. The architectural differences between these models are minor.

## 2023: Llama 2 — Grouped-Query Attention (GQA)

In standard multi-head attention, each head has its own Q, K, and V. In GQA, multiple Q heads share the same K and V heads. For example, 32 Q heads but only 8 K/V heads.

Why this matters: during inference, the **KV cache** (stored K and V from previous tokens) is the main memory bottleneck. GQA reduces KV cache size by 4x (in this example) with minimal quality loss. This is critical for serving long-context models.

## 2023-2024: Mixture of Experts (MoE)

**Mixtral** (Mistral) and **DeepSeek-V2** popularized MoE for LLMs:

- Instead of one FFN per block, have multiple "expert" FFNs (e.g., 8 experts)
- A learned router picks the top-k experts per token (e.g., top-2)
- Total parameter count is much larger (more capacity), but per-token compute stays the same (only k experts run)

This decouples model capacity from inference cost. A 47B-total-parameter MoE with 2-of-8 experts active has roughly the inference cost of a 13B dense model but the knowledge capacity closer to a much larger model.

## 2024: DeepSeek-V2/V3 — Multi-head Latent Attention (MLA)

DeepSeek introduced MLA, which compresses the KV cache even further than GQA. Instead of caching full K/V vectors, it caches a **low-rank compressed representation** and reconstructs K/V on the fly during inference. This reduces KV cache memory dramatically while maintaining quality.

Combined with aggressive MoE (e.g., 256 experts, top-8 routing in DeepSeek-V3), this allows very large models to serve efficiently.

## 2024: Context Length Explosion

Models went from 2K (GPT-2) to 4K (GPT-3) to 8K to 32K to 128K (GPT-4, Claude) to 1M+ (Gemini). Key enablers:

- **RoPE** naturally supports length extrapolation with techniques like YaRN, NTK-aware scaling
- **Flash Attention** — an exact attention algorithm that's IO-aware, reducing memory usage from O(L²) to O(L) while being faster. An implementation breakthrough, not an architectural change.
- Better training data with long documents

## 2024-2025: Reasoning Models

A paradigm shift from "scale pre-training" to "scale inference-time compute":

- Train the model to produce explicit **chain-of-thought reasoning** before giving a final answer
- Use **RL** (reinforcement learning) to improve the reasoning process — reward correct final answers, let the model learn what reasoning steps help
- The model can "think longer" on harder problems by generating more reasoning tokens

Key models: OpenAI o1/o3, DeepSeek-R1. The architecture is still decoder-only — the innovation is in training methodology and how inference is structured.

## 2025: DPO and Post-Training Simplification

**DPO** (Direct Preference Optimization) emerged as a simpler alternative to RLHF:

- Instead of training a separate reward model and doing RL, directly optimize the model on preference pairs (winning response vs losing response)
- Simpler pipeline, fewer moving parts, competitive results
- Many open-source models now use DPO or variants (IPO, KTO) instead of full RLHF

## Current State (2025)

The standard architectural recipe for a frontier LLM today:

- **Architecture**: Decoder-only, Pre-Norm with RMSNorm, SwiGLU FFN, RoPE, GQA or MLA
- **Pre-training**: Next-token prediction on trillions of tokens (following Chinchilla scaling: ~20 tokens per parameter)
- **Post-training**: SFT → preference optimization (RLHF or DPO) → possibly RL for reasoning
- **Optionally**: MoE for efficiency at scale
- **Context**: 128K+ tokens standard, up to 1M+ in some models
- **Inference**: Reasoning traces for hard problems

The core architecture has been relatively stable since LLaMA (2023). Most innovation now is in:
- Training efficiency (MoE, better parallelism strategies)
- Post-training methods (DPO variants, RL for reasoning)
- Inference optimization (KV cache compression, speculative decoding)
- Scaling laws refinement (optimal data/compute trade-offs)

---

## Related Documents

- [[llm/industry-timeline|LLM Industry Timeline]] - Model releases, companies, and market dynamics
- [[llm/original-transformer-architecture|Original Transformer Architecture]] - The 2017 foundation
- [[llm/models/gpt3/architecture|GPT-3 Architecture]] - The scaling breakthrough
- [[llm/models/gpt3/backstories|GPT-3 Backstories]] - Context and impact
