# GPT-3 Experimental Results

*From "Language Models are Few-Shot Learners" (Brown et al., 2020)*

## Overview

GPT-3 was evaluated on **9 major task categories** spanning language modeling, question answering, translation, reasoning, and more. All evaluation used **zero-shot, one-shot, or few-shot** settings—no fine-tuning.

**Model sizes tested**: 8 models from 125M → 175B parameters

**Training data**: 300 billion tokens across all model sizes (see [[llm/models/gpt3/training-data|GPT-3 Training Data]])

**Evaluation paradigm**: Demonstrate that a single general-purpose model can handle diverse tasks through in-context learning alone (see [[llm/models/gpt3/few-shot-learning|GPT-3 Few-Shot Learning]])

## The Scaling Story

Figure 3.1 in the paper shows validation loss follows a **power law**: L = 2.57 · C^-0.048

Key findings:
- Smooth improvement across 4+ orders of magnitude of compute
- No saturation even at 175B parameters—suggests larger models would improve further
- Larger models benefit more from few-shot examples (see Figure 1.2)

This scaling relationship held across benchmarks, validating the hypothesis that drove GPT-3's development.

## Task-by-Task Results

### 3.1 Language Modeling

**Penn Treebank (zero-shot)**:
- GPT-3 175B: **20.5 perplexity**
- Previous SOTA: 35.8 perplexity
- GPT-3 exceeds fine-tuned baselines without task-specific training

**LAMBDA** (language modeling with difficult-to-predict words):
- Zero-shot: 68.0%
- One-shot: 72.5%
- Few-shot (K=15): **86.4%**
- Shows dramatic benefit from examples

**HellaSwag** (commonsense sentence completion):
- Few-shot: **79.3%**
- Fine-tuned SOTA: 85.6%
- Close to supervised performance

### 3.2 Closed-Book Question Answering

Testing the model's ability to answer factual questions without access to external documents:

| Dataset | Zero-Shot | One-Shot | Few-Shot | Fine-Tuned SOTA |
|---------|-----------|----------|----------|----------------|
| **TriviaQA** | 64.3% | 68.0% | **71.2%** | 71.2% |
| **WebQuestions** | 14.4% | 25.3% | **41.5%** | 45.5% |
| **Natural Questions** | 14.6% | 23.0% | **29.9%** | 45.5% |

**TriviaQA**: GPT-3 few-shot **matches fine-tuned SOTA**—remarkable given no task-specific training

**WebQuestions**: Approaches SOTA, showing the model retained substantial factual knowledge

**Natural Questions**: Significant gap remains, suggesting limitations in complex fact retrieval

### 3.3 Translation

Evaluated on 6 language pairs (English ↔ French, German, Romanian):

**French → English**:
- Zero-shot: 21.2 BLEU
- One-shot: 33.7 BLEU
- Few-shot (K=64): **39.2 BLEU**

**English → French**:
- Zero-shot: 25.2 BLEU
- One-shot: 28.3 BLEU
- Few-shot (K=64): **32.6 BLEU**

**Key findings**:
- Translation **into English** consistently stronger than from English (likely due to English-heavy training data)
- Figure 3.4 shows smooth improvement across all model sizes
- Few-shot dramatically outperforms zero-shot, showing examples clarify task format
- Still below supervised neural MT systems (typically 40-45 BLEU)

### 3.4 Winograd Schema Challenge

Testing pronoun disambiguation requiring commonsense reasoning:

**WSC273** (original benchmark):
- Zero-shot: 88.3%
- One-shot: 89.7%
- Few-shot (K=32): 88.6%
- Minimal benefit from few-shot (task already near-saturated)

**Winogrande** (larger, harder version):
- Zero-shot: 70.2%
- One-shot: 73.2%
- Few-shot (K=50): **77.7%**
- Fine-tuned SOTA: 84.6%

Shows GPT-3 has strong commonsense reasoning, but few-shot doesn't always guarantee gains.

### 3.5 Common Sense Reasoning

**PhysicalQA (PIQA)** - physical commonsense:
- Few-shot: **82.8%**
- Fine-tuned SOTA: 79.4%
- **Exceeds supervised SOTA**—a key success for GPT-3

**ARC (Challenge set)** - grade-school science:
- Few-shot: **51.5%**
- Fine-tuned SOTA: 78.5%
- Large gap remains

**OpenBookQA** - open-book science exam:
- Few-shot: **65.4%**
- Fine-tuned SOTA: 87.2%
- Large gap remains

### 3.6 Reading Comprehension

Evaluated on 5 datasets testing comprehension of passages:

| Dataset | Zero-Shot | One-Shot | Few-Shot | Fine-Tuned SOTA |
|---------|-----------|----------|----------|----------------|
| **CoQA** | 81.5 F1 | 84.0 F1 | **85.0 F1** | 90.7 F1 |
| **DROP** | 27.6 F1 | 28.6 F1 | **36.5 F1** | 89.1 F1 |
| **QuAC** | 39.6 F1 | 44.3 F1 | **44.9 F1** | 73.7 F1 |
| **SQuADv2** | 59.5 F1 | 62.6 F1 | **69.8 F1** | 92.2 F1 |
| **RACE-h** | 45.5% | 46.0% | **46.8%** | 90.0% |

**Key findings**:
- **CoQA** closest to SOTA (85.0 vs 90.7)—conversational QA benefits from few-shot
- **DROP** and **RACE** show large gaps—discrete reasoning and complex comprehension remain challenging
- Consistent gains from 0→1→few-shot across all datasets

### 3.7 SuperGLUE

8-task benchmark suite testing diverse language understanding:

| Task | Few-Shot | Fine-Tuned SOTA | Description |
|------|----------|----------------|-------------|
| **COPA** | **90.2%** | 94.8% | Cause/effect reasoning |
| **RTE** | **91.1%** | 93.3% | Textual entailment |
| **BoolQ** | **76.4%** | 91.0% | Yes/no questions |
| **ReCoRD** | **89.1 F1** | 94.1 F1 | Reading comprehension |
| **MultiRC** | **69.3 F1** | 88.1 F1 | Multi-sentence reasoning |
| **WSC** | **80.1%** | 93.8% | Winograd schemas |
| **CB** | **75.6 F1** | 93.9 F1 | Natural language inference |
| **WiC** | **49.4%** | 80.1% | Word sense disambiguation |

**Average**: 49.4 few-shot vs 89.0 fine-tuned SOTA

**Key findings**:
- **COPA** and **RTE** very close to SOTA—simple pattern matching tasks
- **WiC** at random chance (49.4%)—notable weak spot requiring fine-grained semantic understanding
- Figure 3.8 shows dramatic improvement with more examples (K=0.1 → K=32)

### 3.8 Natural Language Inference

**ANLI (Adversarial NLI)** - Round 3:
- Few-shot: **40.0%**
- Fine-tuned SOTA: 48.4%

The paper notes GPT-3 is "only just beginning to show signs of progress" on adversarial NLI, suggesting this capability requires more than pattern matching.

### 3.9 Synthetic & Qualitative Tasks

**Arithmetic**:
- 2-digit addition: **100% accuracy**
- 3-digit addition: **80.4% accuracy**
- 4-digit addition: **25.5% accuracy**
- 5-digit addition: **9.3% accuracy**

Shows the model learned some arithmetic patterns but didn't learn the general algorithm.

**Word scrambling and manipulation**:
- Cycle letters (T1L): 66.9%
- Anagrams (T2L): 15.1%
- Results vary widely depending on task complexity

**SAT analogies**:
- Few-shot: **65.2%**
- College applicant average: 57%
- GPT-3 exceeds human average without specific training

**News article generation**:
- Human detection accuracy: **52%** (barely above random 50%)
- Indicates GPT-3 can generate highly convincing fake news—a safety concern

**Novel word learning ("Gigamuru")**:
- Successfully learns and uses novel words defined in context
- Shows genuine in-context learning beyond simple pattern matching

## Where GPT-3 Excelled

Tasks where few-shot GPT-3 matched or approached SOTA:

- **Closed-book QA (TriviaQA)**: Matches fine-tuned SOTA at 71.2%
- **Physical reasoning (PIQA)**: Exceeds fine-tuned SOTA (82.8% vs 79.4%)
- **Commonsense reasoning (COPA, RTE)**: Very close to SOTA
- **Simple arithmetic**: 100% on 2-digit, 80% on 3-digit
- **News generation**: Fools humans (52% detection)
- **Language modeling**: Beats baselines on Penn Treebank

## Where GPT-3 Struggled

Tasks with large gaps to SOTA:

- **Complex reading comprehension (RACE)**: 46.8% vs 90.0%
- **Discrete reasoning (DROP)**: 36.5% vs 89.1%
- **Natural language inference (ANLI)**: 40% vs 48%
- **Complex arithmetic (4+ digits)**: <30% accuracy
- **Word sense disambiguation (WiC)**: Random chance (49.4%)
- **Adversarial benchmarks**: Large gaps on adversarially-constructed datasets

## Comparison to Fine-Tuned Models

The paper shows few-shot GPT-3 "sometimes competitive with or occasionally surpasses fine-tuned models" but:

- **Closest on pattern matching**: Tasks requiring recognizing formats or simple mappings
- **Largest gaps on novel reasoning**: Tasks requiring reasoning patterns not seen during pre-training
- **Trade-off**: Generality (one model, all tasks) vs peak performance (specialized fine-tuning)

The authors argue the **generality** of few-shot learning—handling any task with just examples—is more valuable than peak performance on a fixed benchmark set.

## The Scaling Hypothesis Validated

Figure 1.3 aggregates results across 42 benchmarks, showing:
- **Smooth power-law relationship** between model size and performance
- **No saturation** at 175B parameters—suggests 500B or 1T parameter models would improve further
- **Few-shot > one-shot > zero-shot** consistently, with gap widening for larger models

This directly motivated GPT-4 (though outside the scope of this document).

---

## Related Documents

- [[llm/models/gpt3/few-shot-learning|GPT-3 Few-Shot Learning]] - Explanation of in-context learning capability
- [[llm/models/gpt3/architecture|GPT-3 Architecture]] - Model specs and changes from GPT-2
- [[llm/models/gpt3/training|GPT-3 Training]] - Hyperparameters, infrastructure, costs
- [[llm/models/gpt3/training-data|GPT-3 Training Data]] - Dataset composition
- [[llm/models/gpt2/zero-shot|GPT-2 Zero-Shot]] - Previous generation's zero-shot results
- [[llm/models/gpt1/experiments|GPT-1 Experiments]] - Fine-tuning baseline for comparison
