# GPT-1 Architecture

Paper: ["Improving Language Understanding by Generative Pre-Training"](paper.pdf) (Radford et al., 2018)

## Model Specifications

- **Total Parameters**: 117 million
- **Layers**: 12 transformer decoder blocks
- **Hidden Size**: 768 dimensions
- **Attention Heads**: 12 heads (64 dimensions per head)
- **FFN Size**: 3,072 dimensions (4× hidden size)
- **Context Length**: 512 tokens maximum
- **Vocabulary Size**: 40,000 BPE tokens
- **Activation Function**: [[llm/activations/gelu|GELU]]
- **Positional Encoding**: Learned embeddings
- **Dropout**: 0.1 uniformly applied

## Architecture Type

**Decoder-only transformer** - simplified from the original Transformer by:

- Removing the entire encoder stack
- Removing cross-attention layers
- Using only causal (masked) self-attention

## Overall Data Flow

```
Input text
    ↓
Tokenization (BPE) → Token IDs
    ↓
Token Embedding (lookup table: vocab_size × 768)
    ↓
Positional Embedding (learned: 512 × 768)
    ↓
Sum: Token + Position → L × 768 matrix
    ↓
[12 × Transformer Blocks]
    ↓
Final Layer Norm
    ↓
Linear Projection (768 → 40,000 vocab)
    ↓
Logits (L × 40,000)
    ↓
Softmax + Sampling → Next token
```

## Before the Transformer Blocks

### 1. Tokenization
Raw text is split into token IDs using Byte Pair Encoding (BPE) with 40,000 merges.

Example: "Hello world" → [15496, 995]

### 2. Token Embedding
Each token ID is mapped to a 768-dimensional vector through a learned lookup table.

- Shape: vocabulary_size × 768
- Token ID 15496 → [0.23, -0.45, 0.87, ...] (768 values)
- 🔢 **Parameters**: 40,000 × 768 = **30,720,000**

### 3. Positional Embedding
Each position (0 to 511) has its own learned 768-dimensional vector.

- Shape: 512 × 768
- These are learned parameters, not fixed sinusoidal functions like the original Transformer
- Cannot extrapolate beyond 512 positions
- 🔢 **Parameters**: 512 × 768 = **393,216**

### 4. Combine Embeddings
The token embedding and positional embedding are added element-wise:

```
input[i] = token_embedding[token_id[i]] + position_embedding[i]
```

For a sequence of L tokens, this produces an **L × 768 matrix** that enters the first transformer block.

## Transformer Blocks (12 layers)

Each block is identical and contains two main components:

### 1. Multi-Head Attention (Causal/Masked)
- 12 attention heads
- Each head has 64 dimensions (768 / 12)
- Uses causal masking: token i can only attend to tokens 0..i
- Prevents looking at future tokens during training
- 🔢 **Parameters per block**:
  - Q, K, V projections (weights): 3 × (768 × 768) = 1,769,472
  - Q, K, V projections (biases): 3 × 768 = 2,304
  - Output projection (weights): 768 × 768 = 589,824
  - Output projection (bias): 768
  - **Total**: **2,362,368**

### 2. Feed-Forward Network (FFN)
- Two linear transformations with [[llm/activations/gelu|GELU]] activation
- Up-project: 768 → 3,072
- Down-project: 3,072 → 768
- 🔢 **Parameters per block**:
  - Up-projection (weights): 768 × 3,072 = 2,359,296
  - Up-projection (bias): 3,072
  - Down-projection (weights): 3,072 × 768 = 2,359,296
  - Down-projection (bias): 768
  - **Total**: **4,722,432**

### 3. Layer Normalization + Residual Connections
Each sub-layer (attention and FFN) is wrapped with:
- Residual connection (add input to output)
- Layer normalization

GPT-1 uses **Post-Norm** (same as the original Transformer):
```
x = LayerNorm(x + MultiHeadAttention(x))
x = LayerNorm(x + FFN(x))
```

The normalization is applied *after* adding the residual. GPT-2 later switched to Pre-Norm for better training stability at scale.

- 🔢 **Parameters per block**: 2 LayerNorms × (768 scale + 768 bias) = **3,072** (negligible)

### Total Parameters Per Block
- 🔢 Multi-head attention: 2,362,368
- 🔢 Feed-forward network: 4,722,432
- 🔢 Layer normalization: 3,072
- 🔢 **Total per block**: **7,087,872**
- 🔢 **All 12 blocks**: **85,054,464**

## After the Transformer Blocks

### 1. Final Layer Norm
The output from the 12th block is normalized using **LayerNorm** (same as used throughout the transformer blocks). This is consistent with the Post-Norm architecture pattern.

- 🔢 **Parameters**: 768 scale + 768 bias = **1,536** (negligible)

### 2. Linear Projection to Vocabulary
The 768-dimensional vectors are projected to vocabulary size (40,000):

- Weight matrix: 768 × 40,000
- Produces logits (raw scores) for each possible next token
- Output shape: L × 40,000
- 🔢 **Parameters**: Often **weight-tied** with token embedding (shares the same 30.7M parameters, so **0 additional parameters**)

### 3. Softmax and Sampling (Inference)
- Logits are converted to probabilities via softmax
- A sampling strategy (greedy, top-k, temperature) selects the next token
- During training, the model predicts all positions simultaneously using teacher forcing

## Key Design Choices

### Why Learned Positional Embeddings?
GPT-1 uses learned positional embeddings instead of the fixed sinusoidal encodings from the original Transformer. This allows the model to learn position-specific patterns but cannot extrapolate beyond the trained context length (512 tokens).

### Why GELU Instead of ReLU?
GELU (Gaussian Error Linear Unit) provides smoother gradients than ReLU. It's a soft approximation of ReLU that can output small negative values, which empirically improves training dynamics.

### Why 12 Heads with 64 Dimensions Each?
This splits the 768-dimensional space into 12 parallel attention computations. Each head can learn to focus on different aspects of the relationships between tokens. The 64-dimensional size per head is a convention from the original Transformer paper and works well in practice.

## Parameter Count Breakdown

### Summary by Component

**Before the transformer blocks:**
- 🔢 Token embedding: 30,720,000
- 🔢 Positional embedding: 393,216
- 🔢 **Subtotal**: **31,113,216**

**Transformer blocks (× 12):**
- 🔢 Multi-head attention per block: 2,362,368
- 🔢 Feed-forward network per block: 4,722,432
- 🔢 Layer normalization per block: 3,072
- 🔢 Total per block: 7,087,872
- 🔢 **Subtotal (all 12 blocks)**: **85,054,464**

**After the transformer blocks:**
- 🔢 Final layer norm: 1,536
- 🔢 Output projection: 0 (weight-tied with token embedding)
- 🔢 **Subtotal**: **1,536**

### Total Parameters
🔢 31,113,216 + 85,054,464 + 1,536 = **116,169,216** ≈ **117 million parameters**

The difference between 116.2M and the reported 117M likely comes from rounding convention in ML papers, where model sizes are typically reported to 2-3 significant figures.
