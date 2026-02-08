# GPT-3 Architecture

Paper: ["Language Models are Few-Shot Learners"](paper.pdf) (Brown et al., 2020)

## Model Specifications

GPT-3 is a family of 8 models ranging from 125M to 175B parameters. The flagship model is GPT-3 175B (also known as "Davinci" in the OpenAI API).

| Model | Parameters | Layers | d_model | Heads | d_head | FFN Size | Context | Batch Size | Learning Rate |
|---|---|---|---|---|---|---|---|---|---|
| **GPT-1** | **117M** | **12** | **768** | **12** | **64** | **3,072** | **512** | **—** | **2.5e-4** |
| **GPT-2 Small** | **124M** | **12** | **768** | **12** | **64** | **3,072** | **1,024** | **0.5M** | **—** |
| **GPT-2 Medium** | **355M** | **24** | **1,024** | **16** | **64** | **4,096** | **1,024** | **0.5M** | **—** |
| **GPT-2 Large** | **774M** | **36** | **1,280** | **20** | **64** | **5,120** | **1,024** | **0.5M** | **—** |
| **GPT-2 XL** | **1.5B** | **48** | **1,600** | **25** | **64** | **6,400** | **1,024** | **0.5M** | **—** |
| GPT-3 Small | 125M | 12 | 768 | 12 | 64 | 3,072 | 2,048 | 0.5M | 6.0e-4 |
| GPT-3 Medium | 350M | 24 | 1,024 | 16 | 64 | 4,096 | 2,048 | 0.5M | 3.0e-4 |
| GPT-3 Large | 760M | 24 | 1,536 | 16 | 96 | 6,144 | 2,048 | 0.5M | 2.5e-4 |
| GPT-3 XL | 1.3B | 24 | 2,048 | 24 | 128 | 8,192 | 2,048 | 1M | 2.0e-4 |
| GPT-3 2.7B | 2.7B | 32 | 2,560 | 32 | 80 | 10,240 | 2,048 | 1M | 1.6e-4 |
| GPT-3 6.7B | 6.7B | 32 | 4,096 | 32 | 128 | 16,384 | 2,048 | 2M | 1.2e-4 |
| GPT-3 13B | 13.0B | 40 | 5,140* | 40 | 128 | 20,560 | 2,048 | 2M | 1.0e-4 |
| GPT-3 175B | 175.0B | 96 | 12,288 | 96 | 128 | 49,152 | 2,048 | 3.2M | 0.6e-4 |

*Note: The paper lists d_model=5,140 for the 13B model, which is almost certainly a typo for 5,120 (40 heads × 128 = 5,120). No official erratum exists.

All models share:

- **Vocabulary Size**: 50,257 (same byte-level BPE as [[llm/models/gpt2/tokenization|GPT-2]])
- **Activation Function**: [[llm/activations/gelu|GELU]]
- **Positional Encoding**: Learned embeddings (2,048 × d_model)
- **FFN Expansion Ratio**: 4× d_model
- **Training Tokens**: 300 billion tokens

API name mapping: Ada ≈ 350M, Babbage ≈ 1.3B, Curie ≈ 6.7B, Davinci ≈ 175B.

## What Changed from GPT-2

The GPT-3 paper explicitly states: *"We use the same model and architecture as GPT-2, including the modified initialization, pre-normalization, and reversible tokenization described therein."*

This means GPT-3 inherits from [[llm/models/gpt2/architecture|GPT-2]]:

- Pre-Norm (LayerNorm before each sub-layer)
- Residual weight scaling (1/√N at initialization)
- Byte-level BPE tokenizer (50,257 vocabulary)

However, there are a few actual differences:

### 1. Alternating Dense and Locally Banded Sparse Attention

This is the only architectural change explicitly called out in the paper. GPT-2 used dense attention in all layers — every token attends to all previous tokens. GPT-3 alternates between two attention patterns across its layers:

- **Dense attention layers** (standard): Every token attends to all previous tokens in the 2,048-token context window. This is normal causal self-attention.
- **Locally banded sparse attention layers**: Each token attends only to a local window of nearby tokens, not the full sequence. This creates a "band" pattern in the attention matrix.

The layers alternate between these two types — roughly half use dense (global) attention and half use locally banded (local) attention. This approach comes from OpenAI's Sparse Transformer paper (Child et al., 2019). The motivation: reduce memory and compute from O(n²) to approximately O(n√n) while preserving both local and long-range dependencies.

Sparse attention **does not change the parameter count** — it only changes which tokens attend to which other tokens. It's a compute/memory optimization, not a capacity change.

Interestingly, this means sliding-window attention — often presented as a recent innovation in models like Mistral (2023) — was already used in GPT-3 back in 2020.

### 2. Context Length: 1,024 → 2,048

Doubled from GPT-2. Since GPT-3 uses learned positional embeddings, this means the positional embedding table is now 2,048 × d_model.

### 3. Weight Tying Removed

GPT-2 tied the token embedding and output projection weights (the same matrix was used for both, saving ~38M parameters). GPT-3 uses **separate (untied) weights** for these two matrices. At 175B scale, the embedding matrix (~617M parameters) is less than 0.4% of total parameters, so untying adds negligible overhead but gives the model more flexibility.

### 4. Variable Head Dimensions

GPT-2 used d_head=64 uniformly across all model sizes. GPT-3 varies it depending on model size: 64, 80, 96, or 128. The 175B model uses 128-dimensional heads.

### 5. Scale

The massive jump from 1.5B to 175B parameters — a ~117× increase. This is the main story of GPT-3. The paper demonstrated that this scale produces **in-context learning** capabilities that smaller models don't exhibit: give the model a few examples in the prompt, and it can do the task without any weight updates.

## What Stayed the Same

- Decoder-only transformer with causal masked self-attention
- Pre-Norm architecture (inherited from GPT-2)
- [[llm/activations/gelu|GELU]] activation in FFN
- Learned positional embeddings
- 4× FFN expansion ratio
- Same byte-level BPE tokenizer as GPT-2

## The "Just Bigger" Narrative

GPT-3 is often described as "architecturally identical to GPT-2, just bigger." This is *mostly* true. The core transformer block structure — Pre-Norm decoder-only transformer with GELU, learned positional embeddings, 4× FFN expansion — is identical. The sparse attention alternation is the only real structural change, and even that preserves the parameter count.

The key insight of the GPT-3 paper was that **scale alone** (175B parameters, 300B training tokens) produces qualitatively new capabilities (in-context learning) without architectural innovation. You don't need a better architecture — you need a bigger model trained on more data.

## Overall Data Flow

Same as [[llm/models/gpt2/architecture|GPT-2]], with the attention pattern change:

```
Input text
    ↓
Tokenization (byte-level BPE) → Token IDs
    ↓
Token Embedding (50,257 × d_model, untied from output)
    ↓
Positional Embedding (2,048 × d_model)
    ↓
Sum: Token + Position
    ↓
[96 × Transformer Blocks]
  Layers alternate between:
    Dense:  LayerNorm → Multi-Head Attention (full context) → Add residual
            LayerNorm → FFN → Add residual
    Sparse: LayerNorm → Multi-Head Attention (local window) → Add residual
            LayerNorm → FFN → Add residual
    ↓
Final Layer Norm
    ↓
Linear Projection (d_model → 50,257 vocab, untied weights)
    ↓
Logits → Softmax → Next token
```
