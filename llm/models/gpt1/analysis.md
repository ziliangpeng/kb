# GPT-1 Analysis

Paper: ["Improving Language Understanding by Generative Pre-Training"](paper.pdf) (Radford et al., 2018)

## Overview

Section 5 of the GPT-1 paper presents experimental findings that validate the model's design choices. Three key analyses: layer transfer impact, zero-shot behaviors, and ablation studies.

## Impact of Number of Layers Transferred

They tested transferring only the first N layers from the pre-trained model (instead of all 12) and randomly initializing the rest.

**Results** (on MultiNLI and RACE):
- Transferring just the embeddings (0 layers) already helps
- Each additional layer improves performance further
- Full 12-layer transfer gives up to **9% improvement** over embeddings-only on MultiNLI
- The improvement is roughly linear — no single layer is dramatically more important than others

**Takeaway**: Every layer in the pre-trained model learns something useful for downstream tasks. It's not only the early layers (basic syntax) that matter — later layers (higher-level semantics) contribute meaningfully too.

## Zero-Shot Behaviors

They tested whether the pre-trained model (WITHOUT any fine-tuning) can perform tasks using only its language modeling ability.

### Heuristic Methods

Since the model only knows how to predict next tokens, they designed heuristics to convert tasks into language modeling problems:

- **Sentiment (SST-2)**: Append "very" to the text, check if the model assigns higher probability to "positive" or "negative"
- **Question answering (RACE)**: Pick the answer choice where the model assigns the highest average token probability when conditioned on context + question
- **Commonsense (Winograd)**: Replace a pronoun with each candidate, pick whichever gives higher probability for the rest of the sentence
- **Linguistic acceptability (CoLA)**: Use the average token log-probability as a grammaticality score

### Findings

- Zero-shot performance **steadily improves** throughout pre-training (more training = better zero-shot)
- Performance is still much worse than fine-tuned models
- The Transformer shows higher variance in zero-shot performance compared to LSTM, suggesting the transformer architecture has stronger inductive bias for transfer

### Significance

This foreshadows GPT-2, which focused entirely on zero-shot performance. GPT-1 showed the seed of the idea — pre-training alone gives some task ability — but it wasn't good enough yet. GPT-2 (1.5B params, 10× bigger) later showed that with more scale, zero-shot becomes actually useful.

## Ablation Studies

Three ablations, each validating one design choice:

### A. Remove Auxiliary LM Objective During Fine-Tuning

Without the `λ × L₁(C)` term in the fine-tuning loss:

- **Larger datasets** (NLI, QQP) got worse — the auxiliary objective helps as a regularizer
- **Smaller datasets** didn't benefit from it

This makes sense: with small data, the fine-tuning signal is already weak, adding another objective just adds noise. With large data, the LM objective provides useful regularization that prevents overfitting.

### B. Replace Transformer with LSTM

Same framework (pre-train → fine-tune), but use a single-layer 2048-unit LSTM instead of the 12-layer Transformer:

- **5.6 average score drop** across all tasks
- LSTM only beat the Transformer on one dataset (MRPC)

This validates the choice of Transformer over LSTM — self-attention is better at capturing the representations needed for transfer learning.

### C. Remove Pre-Training Entirely

Train the Transformer directly on downstream tasks from random initialization:

- **14.8% decrease** compared to the full pre-trained model

This is the most important finding — it validates the entire paper's premise that pre-training is essential. Without it, even the same architecture performs dramatically worse.

## Summary

| Ablation | Impact |
|----------|--------|
| Remove auxiliary LM objective | Hurts on large datasets |
| Replace Transformer with LSTM | 5.6% average drop |
| Remove pre-training | 14.8% drop |
