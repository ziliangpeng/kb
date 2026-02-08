# Decoder-Only Evolution

The evolution from the original Transformer to today's frontier decoder-only models.

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

## 2020: GPT-3 — The Scaling Breakthrough

175B params. The moment everything changed:

- **In-context learning**: give the model a few examples in the prompt and it can do the task, no fine-tuning needed
- Published **scaling laws** (Kaplan et al.): model performance improves predictably as a power law with compute, data, and parameters
- Architecturally identical to GPT-2, just much bigger. The lesson: you don't need architectural innovations, you need scale
- Spawned the entire "foundation model" paradigm

## 2022: Chinchilla — Fix the Scaling Recipe

DeepMind showed GPT-3 was **undertrained**. The Chinchilla paper demonstrated that for a fixed compute budget, you should scale parameters and training data roughly equally. GPT-3 had 175B params but was trained on only 300B tokens — Chinchilla used 70B params trained on 1.4T tokens and performed better.

This changed the industry: every model after Chinchilla trained on much more data relative to parameter count.

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

The standard recipe for a frontier LLM today:

- **Architecture**: Decoder-only, Pre-Norm with RMSNorm, SwiGLU FFN, RoPE, GQA or MLA
- **Pre-training**: Next-token prediction on trillions of tokens
- **Post-training**: SFT → preference optimization (RLHF or DPO) → possibly RL for reasoning
- **Optionally**: MoE for efficiency at scale
- **Context**: 128K+ tokens
- **Inference**: Reasoning traces for hard problems

The architecture itself has been relatively stable since LLaMA (2023). Most innovation now is in training data, post-training methods, MoE scaling, and inference-time reasoning.
