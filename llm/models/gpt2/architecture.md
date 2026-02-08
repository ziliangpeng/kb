# GPT-2 Architecture

Paper: ["Language Models are Unsupervised Multitask Learners"](paper.pdf) (Radford et al., 2019)

## Model Specifications

GPT-2 is a family of 4 models. The flagship model is GPT-2 XL (1.5B).

| | GPT-1 | Small | Medium | Large | XL |
|---|---|---|---|---|---|
| **Parameters** | 117M | 124M | 355M | 774M | 1.5B |
| **Layers** | 12 | 12 | 24 | 36 | 48 |
| **Hidden Size** | 768 | 768 | 1024 | 1280 | 1600 |
| **Attention Heads** | 12 | 12 | 16 | 20 | 25 |
| **Head Dimension** | 64 | 64 | 64 | 64 | 64 |
| **FFN Size** | 3,072 | 3,072 | 4,096 | 5,120 | 6,400 |

All models share:

- **Context Length**: 1,024 tokens
- **Vocabulary Size**: 50,257 (byte-level BPE)
- **Activation Function**: [[llm/activations/gelu|GELU]]
- **Positional Encoding**: Learned embeddings
- **FFN Expansion Ratio**: 4× hidden size

## What Changed from GPT-1

The GPT-2 paper explicitly states the architecture is largely the same as [[llm/models/gpt1/architecture|GPT-1]]. The actual architectural changes are minimal but important:

### 1. Pre-Norm (the main architectural change)

GPT-1 used **Post-Norm**, the same as the original Transformer — LayerNorm is applied *after* the residual addition:

```
x = LayerNorm(x + MultiHeadAttention(x))
x = LayerNorm(x + FFN(x))
```

GPT-2 switched to **Pre-Norm** — LayerNorm is applied *before* each sub-layer:

```
x = x + MultiHeadAttention(LayerNorm(x))
x = x + FFN(LayerNorm(x))
```

Why this matters: In Post-Norm, the residual branch adds unnormalized activations, and the subsequent LayerNorm must handle the combined variance. Gradients flowing back through this normalization can become unstable at larger scale. With Pre-Norm, the residual stream stays cleaner — the main signal passes through the residual connection without being distorted by normalization. This made it possible to train the deeper models (36 and 48 layers) that GPT-1's 12-layer Post-Norm design would have struggled with.

An additional LayerNorm is added after the final transformer block (before the output projection).

### 2. Residual Weight Scaling

The weights of residual layers are scaled at initialization by a factor of 1/√N, where N is the number of residual layers. This prevents the residual stream from growing too large as layers stack up — another stability measure that complements Pre-Norm for training deeper models.

### 3. Context Length: 512 → 1,024

Doubled from GPT-1. Since GPT-2 uses learned positional embeddings, this means the positional embedding table is now 1,024 × d_model instead of 512 × 768.

### 4. Vocabulary: 40,000 → 50,257 (Byte-Level BPE)

GPT-1 used character-level BPE with spaCy preprocessing. GPT-2 switched to byte-level BPE, which:

- Can encode any arbitrary string (no unknown tokens ever)
- Doesn't require language-specific preprocessing (no spaCy, no ftfy)
- Uses 256 base byte values instead of 478 base characters

See [[llm/models/gpt1/tokenization|GPT-1 Tokenization]] for the comparison.

### 5. Scale

GPT-1 was a single 117M model. GPT-2 introduced a family of 4 sizes, with the largest (1.5B) being ~13× the size of GPT-1. This was the first clear demonstration that scaling decoder-only transformers unlocks qualitatively new capabilities (zero-shot task performance).

## What Stayed the Same

- Decoder-only transformer (causal masked self-attention)
- [[llm/activations/gelu|GELU]] activation in FFN
- Learned positional embeddings
- 4× FFN expansion ratio
- Weight tying between token embedding and output projection
- 64 dimensions per attention head

## Comparing GPT-2 Small to GPT-1

GPT-2 Small is the most direct comparison to GPT-1 — same number of layers (12), same hidden size (768), same number of heads (12). The ~7M parameter difference (124M vs 117M) comes entirely from the larger vocabulary embedding:

- GPT-1 token embedding: 40,000 × 768 = 30.7M
- GPT-2 token embedding: 50,257 × 768 = 38.6M
- Difference: ~7.9M parameters

This makes GPT-2 Small useful as a controlled comparison: any performance difference between GPT-1 and GPT-2 Small comes from Pre-Norm, the new tokenizer, longer context, and the training data/procedure — not from model capacity.

## Overall Data Flow

The data flow is the same as [[llm/models/gpt1/architecture|GPT-1]], with the LayerNorm placement changed:

```
Input text
    ↓
Tokenization (byte-level BPE) → Token IDs
    ↓
Token Embedding (50,257 × d_model)
    ↓
Positional Embedding (1,024 × d_model)
    ↓
Sum: Token + Position
    ↓
[N × Transformer Blocks]
  Each block:
    LayerNorm → Multi-Head Attention → Add residual
    LayerNorm → FFN → Add residual
    ↓
Final Layer Norm
    ↓
Linear Projection (d_model → 50,257 vocab)
    ↓
Logits → Softmax → Next token
```
