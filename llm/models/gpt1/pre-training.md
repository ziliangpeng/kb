# GPT-1 Pre-Training

Paper: ["Improving Language Understanding by Generative Pre-Training"](paper.pdf) (Radford et al., 2018)

## Overview

Pre-training is the **core innovation** of GPT-1. The key insight: train a decoder-only transformer on massive unlabeled text using next-token prediction, then fine-tune it on specific tasks. Neither next-token prediction nor the decoder-only architecture was new — the innovation was combining them into a pre-train → fine-tune paradigm using a transformer.

**Language**: GPT-1 was trained exclusively on **English text**. It is an English-only model.

## Training Objective

The objective is **next-token prediction** (also called causal language modeling). Given all previous tokens, predict the next one.

### Mathematical Formulation

```
L₁(U) = Σᵢ log P(uᵢ | u₁, ..., uᵢ₋₁; Θ)
```

- `U = {u₁, u₂, ..., uₙ}` — the entire training corpus
- `uᵢ` — token at position i
- `u₁, ..., uᵢ₋₁` — all previous tokens (the context)
- `Θ` — model parameters (all 117M weights)
- `P(uᵢ | ...)` — probability the model assigns to the correct next token

The loss is the **negative log-likelihood (cross-entropy)** averaged over all tokens. The model outputs a probability distribution over all 40,000 vocabulary tokens at each position, and training pushes it to assign high probability to the actual next token.

### Not a GPT-1 Invention

Next-token prediction existed long before GPT-1:
- Used in n-gram models (1990s)
- Used in neural language models with RNNs/LSTMs (2000s-2010s)

GPT-1's contribution was showing that this simple objective, applied to a **transformer** pre-trained on large unlabeled text, produces representations that transfer well to many downstream tasks.

## Training Data

### Dataset: BooksCorpus

- **Dataset**: [[llm/datasets/bookscorpus|BooksCorpus]] — ~7,000-11,000 self-published books from Smashwords.com
- **Size**: ~985 million words (~4-6 GB of text)
- **Language**: English only
- **Content**: Novels across genres (romance, science fiction, fantasy, etc.)
- **Why books**: Long-form narrative text provides better training data for learning long-range dependencies compared to shorter web text or news articles

### 100 Epochs

GPT-1 trained over the same BooksCorpus data **100 times** (100 epochs). This is notable because:

- The dataset is relatively small (~1B words) — repeating it compensated for limited data
- Later models moved in the opposite direction: GPT-3 trained ~1 epoch on 300B tokens
- Chinchilla (2022) later showed that **more data with fewer epochs** is better than repeating small data many times
- Modern frontier models train on trillions of tokens, typically for ~1 epoch

### Preprocessing Pipeline

Before training, the text was preprocessed in three steps:

1. **ftfy** — A Python library that standardizes punctuation, quotes, and whitespace (e.g., fixing curly quotes, Unicode normalization)
2. **spaCy** — Tokenized text into words (pre-tokenization before BPE)
3. **[[llm/tokenization/bpe|BPE]]** — Applied 40,000 merge operations to produce the final token sequence

This preprocessing pipeline was later simplified in GPT-2, which dropped ftfy and spaCy in favor of byte-level BPE with regex-based pre-tokenization.

See [[llm/models/gpt1/tokenization|GPT-1 Tokenization]] for full details.

## Training Process

### Optimizer

[[llm/optimizers/adam|Adam]] optimizer with:
- Learning rate: 2.5 × 10⁻⁴ (peak)
- Weight decay: L2 regularization on non-bias weights

### Learning Rate Schedule

Two-phase schedule across the **entire training run** (not per epoch):

**Phase 1 — Linear Warmup (steps 0 → 2,000):**

Learning rate increases linearly from 0 to 2.5 × 10⁻⁴.

Why warmup: At the start of training, weights are random and gradients are large and noisy. A high learning rate would cause erratic updates and destabilize training. Warming up gradually lets the model settle into a reasonable region first.

**Phase 2 — Cosine Annealing (step 2,000 → end):**

Learning rate decreases following a cosine curve from 2.5 × 10⁻⁴ down to 0:

```
LR(t) = ½ × LR_max × (1 + cos(π × t / T))
```

The cosine shape decreases slowly at first, faster in the middle, and slowly again near zero. This spends more time at moderate learning rates (the useful range) compared to linear decay.

Why decay: Early in training, large LR helps make big progress and learn broad patterns. Late in training, small LR fine-tunes the details and helps converge precisely.

**Early adopter of this combination**: Neither warmup (from the original Transformer, 2017) nor cosine annealing (Loshchilov & Hutter, 2016) was new. But GPT-1 was an early adopter of combining **linear warmup + cosine annealing** for language model training. This combination became the **de facto standard** for LLM training — GPT-2/3, LLaMA, and most modern LLMs use this same pattern.

### Other Hyperparameters

- **Batch size**: 64 sequences
- **Sequence length**: 512 tokens
- **Tokens per step**: 64 × 512 = 32,768
- **Epochs**: 100
- **Dropout**: 0.1 (applied to attention, residual connections, and embeddings)

### Regularization

- **Dropout (0.1)**: Randomly zeros out 10% of activations during training to prevent overfitting
- **Weight decay**: L2 regularization on non-bias weights
- **Layer normalization**: Stabilizes activations throughout the network
- **Residual connections**: Facilitate gradient flow, preventing vanishing gradients

## Training Dynamics

These are not GPT-1 specific — they apply to all decoder-only transformer training:

- **Teacher forcing**: During training, the model receives the full ground-truth sequence as input and predicts the next token at every position simultaneously (in one forward pass), rather than feeding tokens one at a time
- **Causal masking**: An attention mask ensures each position can only attend to itself and previous positions, preventing "cheating" by looking at future tokens
- **Parallel processing**: Teacher forcing + causal masking together allow training on all positions in a sequence in parallel, making training much faster than autoregressive generation

## Why Pre-Training Works

### What does next-token prediction learn?

To predict the next word well, the model is forced to learn rich representations of language:

- `"The cat sat on the ___"` → **syntax** (what can grammatically follow)
- `"Paris is the capital of ___"` → **world knowledge**
- `"She was happy because ___"` → **causality and sentiment**
- `"In chapter one, the hero... [500 tokens later]... he ___"` → **long-range context**

The simple objective implicitly requires the model to build internal representations that capture syntax, semantics, world knowledge, and reasoning patterns.

### Unlabeled data is abundant, labeled data is scarce

Before GPT-1, NLP models were trained from scratch on small labeled datasets (thousands to tens of thousands of examples per task). GPT-1's insight: use the vast amount of unlabeled text (985M words from BooksCorpus, no human labeling needed) to learn general language understanding first, then adapt to specific tasks with small labeled data.

### How knowledge transfers

The model's internal representations (768-dimensional vectors at each layer) become **general-purpose language encodings** during pre-training. These encodings capture syntax, semantics, and relationships that are useful across many tasks. Fine-tuning then adjusts these representations slightly for the specific downstream task, rather than learning everything from scratch.
