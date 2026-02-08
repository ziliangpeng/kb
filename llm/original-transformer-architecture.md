# The Original Transformer Architecture

Paper: "Attention Is All You Need" (Vaswani et al., 2017)

## Overview

The Transformer was proposed as a replacement for RNN/LSTM-based sequence models. Its key innovation is the **self-attention mechanism**, which allows every token to attend to every other token in parallel — eliminating the sequential bottleneck of recurrent models.

The original Transformer was designed for machine translation and uses an **encoder-decoder** structure. Modern LLMs (GPT, Llama, Claude) are **decoder-only**, using only the decoder half with causal masking.

## Data Flow

### 1. Tokenization

Raw text is split into tokens using a tokenizer. A few characters map to one token. This controls the vocabulary size and improves efficiency — the model works with a fixed set of integer token IDs rather than raw characters.

### 2. Embedding

Each token ID is mapped to a learned embedding vector of dimension E (E=512 in the original paper). An input of L tokens becomes an **L x E matrix**.

### 3. Positional Encoding

Since attention has no inherent notion of position (unlike RNNs), positional information is added explicitly. The original paper uses fixed sinusoidal functions — each position gets a unique vector of dimension E, which is **added** element-wise to the token embedding.

### 4. Transformer Blocks (repeated N times)

Each block takes an L x E input and produces an L x E output. The original paper uses N=6 blocks.

Each block contains two sub-layers:

#### Sub-layer 1: Multi-Head Attention

The input X (L x E) is projected into Q, K, V for each attention head:

- **Q = X · W_Q** (query)
- **K = X · W_K** (key)
- **V = X · W_V** (value)

With h=8 heads and d_k = E/h = 64, each head's Q, K, V are L x 64.

Each head computes attention independently:

```
Attention(Q, K, V) = softmax(Q · K^T / sqrt(d_k)) · V
```

- **Q · K^T** produces an L x L attention score matrix
- **/ sqrt(d_k)** scales the scores to prevent large dot products from pushing softmax into saturated regions with tiny gradients
- **softmax** normalizes each row to a probability distribution (each token's attention over all other tokens)
- **· V** produces a weighted combination of value vectors

The h head outputs (each L x 64) are **concatenated** back to L x E, then multiplied by an output projection matrix W_O (E x E).

In the decoder, a **causal mask** is applied before softmax — future positions are set to negative infinity, so after softmax they become zero. This ensures token i can only attend to tokens 0..i, enabling autoregressive generation.

#### Sub-layer 2: Feed-Forward Network (FFN)

Applied independently to each token position (same weights, different inputs):

```
FFN(x) = W_2 · [[llm/activations/relu|ReLU]](W_1 · x + b_1) + b_2
```

- **W_1**: E → 4E (up-projection, expanding the representation)
- **ReLU**: nonlinear activation
- **W_2**: 4E → E (down-projection, compressing back)

#### Residual Connections and Layer Normalization

Each sub-layer is wrapped with a residual connection and normalization. The original paper uses **Post-Norm**:

```
output = LayerNorm(x + Sublayer(x))
```

So each block has two residual + norm steps: one after attention, one after FFN.

### 5. Final Output

After all N blocks, the final L x E output is projected to vocabulary size via a linear layer, producing **logits** (one score per vocabulary token, for each position). A sampling strategy (greedy, top-k, top-p, temperature) selects the next token ID.

## Encoder-Decoder Structure (Original Paper)

The original Transformer has two halves:

- **Encoder**: Processes the full input with **bidirectional** self-attention (every token attends to every other token). Used for the source sentence in translation.
- **Decoder**: Generates output autoregressively with **causal masking** (each token only attends to previous tokens). Also includes **cross-attention** layers that attend to the encoder's output.

Modern LLMs dropped the encoder and use **decoder-only** with causal masking throughout.

## Key Dimensions (Original Paper)

| Parameter | Value |
|---|---|
| Embedding dim (E) | 512 |
| Number of heads (h) | 8 |
| Head dim (d_k = E/h) | 64 |
| FFN inner dim | 2048 (4x E) |
| Number of layers (N) | 6 |

---

## Q&A

### Why is the QKV projection a down-projection (E → d_k) instead of an up-projection?

It's not really "down" in total — it's a **split**. With E=512 and 8 heads, each head gets d_k=64, but across all 8 heads you're still covering the full E-dimensional space.

The attention matrix is L x L per head — that's where the main cost is. Making each head's dimension larger doesn't help much because the information bottleneck in attention is the L x L score matrix, not the dimension of Q/K. 64 dimensions is enough for each head to decide "how relevant is token j to token i." The expressiveness comes from having multiple heads with different learned projections, not from making each head large.

This is confirmed by modern architectures like GQA (Grouped-Query Attention in Llama), which use even fewer K/V heads than Q heads to save memory — and it works fine.

### Why does the FFN up-project (E → 4E) then down-project (4E → E)?

Attention mixes information **across tokens** (the L dimension). The FFN transforms **each token's representation independently** (the E dimension).

The up-projection expands into a higher-dimensional space where nonlinear transformations are more effective. In E dimensions, the representation is packed and entangled. By projecting to 4E, the model spreads things out — the ReLU can selectively activate or suppress different features in this expanded space. The down-projection then compresses back to E so data can flow to the next layer.

The 4x ratio is a convention from the original paper. Modern models vary:

- Llama uses ~2.7x with SwiGLU (a gating mechanism that uses some expanded dimensions for gating)
- The ratio is a hyperparameter trading off model capacity vs. compute

### Pre-Norm vs Post-Norm: What's the difference and which is better?

**Post-Norm** (original Transformer):
```
output = LayerNorm(x + Sublayer(x))
```

**Pre-Norm** (GPT-2 onwards):
```
output = x + Sublayer(LayerNorm(x))
```

The industry moved decisively to **Pre-Norm** because of training stability at scale:

- With Post-Norm, gradients must flow through LayerNorm at every layer during backpropagation. As models get deeper (48, 96+ layers), this causes gradient flow problems and requires careful learning rate warmup.
- With Pre-Norm, the residual connection provides a clean gradient highway — gradients flow directly through `x + ...` without passing through normalization.

Post-Norm may produce slightly better results *when training is stable*, since it forces tighter integration at each layer. But Pre-Norm's stability advantage is non-negotiable at 100B+ parameters.

Nearly all modern LLMs use Pre-Norm: GPT-2/3/4, Llama, Claude, PaLM. Some architectures like DeepNorm attempt to get the benefits of Post-Norm with modified scaling to stabilize training.

Modern models also tend to use **RMSNorm** (drops mean-centering, just normalizes by variance) instead of full LayerNorm, for computational efficiency.
