# GPT-1 Fine-Tuning

Paper: ["Improving Language Understanding by Generative Pre-Training"](paper.pdf) (Radford et al., 2018)

## Overview

Fine-tuning is the second stage of GPT-1's two-stage approach. After pre-training one general model, it is **independently fine-tuned** for each downstream task. Each fine-tuning run starts from the same pre-trained weights and produces a separate task-specific model:

```
1 general pre-trained model → N specialized fine-tuned models
```

Before GPT-1, each NLP task required training a custom model from scratch. GPT-1 showed you could pre-train once (expensive) and fine-tune cheaply many times (3 epochs, small labeled data) to beat task-specific models.

## Fine-Tuning Objective

### Architecture Change

A single **linear layer** is added on top of the pre-trained model:

```
Input tokens → Pre-trained transformer (768-dim output) → New linear layer → Task prediction
```

The linear layer maps from the transformer's 768-dimensional output to the number of task-specific labels (e.g., 768 → 2 for binary classification). The prediction is made from the **last token's** representation.

### Loss Function

```
L₂(C) = Σ log P(y | x¹, ..., xᵐ)
```

- `C` — the labeled dataset
- `x¹, ..., xᵐ` — input tokens
- `y` — the correct label

This is standard supervised cross-entropy loss.

### What Changes During Fine-Tuning

- **All 117M parameters** are updated — both the pre-trained transformer weights AND the new linear layer
- **Learning rate**: 6.25 × 10⁻⁵ (4× lower than pre-training's 2.5 × 10⁻⁴) — the pre-trained weights change only slightly
- **Epochs**: 3 (vs 100 for pre-training)
- **Batch size**: 32

The key idea: the model already "understands" language from pre-training. Fine-tuning gently nudges it toward the specific task.

## Auxiliary Language Modeling Objective

During fine-tuning, GPT-1 doesn't just use the task loss. It **also keeps the pre-training loss** as an auxiliary objective:

```
L₃(C) = L₂(C) + λ × L₁(C)
```

- `L₂(C)` — supervised task loss (e.g., classify sentiment correctly)
- `L₁(C)` — language modeling loss (predict next token), applied to the same fine-tuning data
- `λ` — weighting factor controlling how much the LM objective matters

### Why Keep the LM Objective?

**Prevents catastrophic forgetting.** Without it, fine-tuning can overwrite the general language knowledge learned during pre-training. The LM loss acts as a regularizer — it keeps the model "remembering" how language works while learning the new task.

**Improves generalization.** The paper found this auxiliary objective:
- Helped particularly on larger datasets
- Accelerated convergence (model learned faster)

Practically, each fine-tuning step computes both losses, adds them together, and uses the combined gradients to update the weights. The task loss pushes toward solving the task, while the LM loss keeps the model grounded in general language understanding.

## Task-Specific Input Transformations

Instead of designing different architectures for different task types, GPT-1 keeps the **same model** and changes how the input is formatted. Special tokens are used to structure the input:

- `[Start]` — beginning of sequence
- `[Extract]` — end of sequence (prediction is made from this token's representation)
- `$` — delimiter between segments

### Classification

```
[Start] This movie was great [Extract]
                                  ↓
                            Linear → positive/negative
```

Wrap the text with start/end tokens. Predict from the last token.

### Entailment

"Does sentence A imply sentence B?"

```
[Start] The dog is sleeping $ The animal is resting [Extract]
                                                        ↓
                                                  Linear → entailment/contradiction/neutral
```

Concatenate premise and hypothesis with a delimiter `$` in between.

### Similarity

"Are these two sentences similar?"

```
[Start] Sentence A $ Sentence B [Extract] → representation 1
[Start] Sentence B $ Sentence A [Extract] → representation 2
                                                 ↓
                                          Sum both → Linear → similar/not
```

Process **both orderings** and add the representations. This handles the fact that similarity is symmetric (A similar to B means B similar to A).

### Multiple Choice

"Which answer is correct?"

```
[Start] Context $ Question $ Answer A [Extract] → score A
[Start] Context $ Question $ Answer B [Extract] → score B
[Start] Context $ Question $ Answer C [Extract] → score C
[Start] Context $ Question $ Answer D [Extract] → score D
                                                      ↓
                                                Softmax → pick highest
```

Process each answer option as a separate sequence, score each one, pick the highest.

### Why This Matters

Before GPT-1, each task type required a custom architecture. GPT-1 showed that **one architecture handles everything** — you only change the input format. The only new parameters per task are the linear head and the delimiter tokens.

## Results

GPT-1 was evaluated on **12 tasks** across 4 categories. It achieved state-of-the-art on **9 out of 12**.

### Natural Language Inference

"Given sentence A, does sentence B follow?"

| Task | GPT-1 | Previous Best | Improvement |
|------|-------|---------------|-------------|
| MNLI (matched) | 82.1% | — | — |
| SNLI | 89.9% | 89.3% | +0.6% |
| SciTail | 88.3% | 83.3% | +5.0% |
| QNLI | 88.1% | 82.3% | +5.8% |
| RTE | 56.0% | — | underperformed |

### Question Answering

| Task | Improvement |
|------|-------------|
| RACE | +5.7% over previous best |
| Story Cloze | +8.9% over previous best |

### Sentence Similarity

"Are these two sentences saying the same thing?"

Evaluated on QQP, MRPC, and STS-B — performed competitively.

### Text Classification

| Task | GPT-1 | Previous Best |
|------|-------|---------------|
| CoLA | 45.4 | 35.0 |
| SST-2 | — | competitive |

### Overall

- **GLUE benchmark score**: 72.8 (previous best: 68.9)
- **9 out of 12 tasks**: New state-of-the-art
- **Tasks where GPT-1 struggled** (e.g., RTE): Had very small datasets — not enough fine-tuning data to adapt well

### Key Takeaway

One pre-trained model, fine-tuned independently 12 times, beat specialized models that were each designed and trained from scratch for their specific task. This validated the entire pre-train → fine-tune paradigm.
