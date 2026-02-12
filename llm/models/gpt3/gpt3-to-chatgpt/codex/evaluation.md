# Codex Evaluation & Results

**Paper**: ["Evaluating Large Language Models Trained on Code"](https://arxiv.org/abs/2107.03374) (Chen et al., July 2021)

## HumanEval Results

All models evaluated on the [[llm/datasets/humaneval|HumanEval]] benchmark (164 hand-written Python problems). Samples generated with temperature T=0.2 for pass@1 and T=0.8 for pass@100, using nucleus sampling (top_p=0.95). 200 samples generated per problem.

### Base Codex (All Model Sizes)

| Model | Parameters | pass@1 | pass@10 | pass@100 |
|-------|-----------|--------|---------|----------|
| Codex-12M | 12M | 2.00% | 3.62% | 8.58% |
| Codex-25M | 25M | 3.21% | 7.10% | 12.89% |
| Codex-42M | 42M | 5.06% | 8.80% | 15.55% |
| Codex-85M | 85M | 8.22% | 12.81% | 22.40% |
| Codex-300M | 300M | 13.17% | 20.37% | 36.27% |
| Codex-679M | 679M | 16.22% | 25.70% | 40.95% |
| Codex-2.5B | 2.5B | 21.36% | 35.42% | 59.50% |
| Codex-12B | 12B | 28.81% | 46.81% | 72.31% |

Performance scales smoothly from 12M to 12B — no sudden jumps, roughly proportional improvement with each ~10x parameter increase.

### Codex-S (Supervised Fine-Tuned)

| Model | pass@1 | pass@100 |
|-------|--------|----------|
| Codex-12B | 28.81% | 72.31% |
| Codex-S-12B | 37.7% | 77.5% |

Codex-S improves over base Codex by ~6.5 percentage points on pass@1 and ~15.1 points on pass@100 averaged across all model sizes.

### Comparison with Non-Codex Models

| Model | Parameters | pass@1 | pass@10 | pass@100 |
|-------|-----------|--------|---------|----------|
| GPT-3 | 175B | 0% | — | — |
| GPT-Neo | 125M | 0.75% | 1.88% | 2.97% |
| GPT-Neo | 1.3B | 4.79% | 7.47% | 16.30% |
| GPT-Neo | 2.7B | 6.41% | 11.27% | 21.37% |
| GPT-J | 6B | 11.62% | 15.74% | 27.74% |
| TabNine | — | 2.58% | 4.35% | 7.59% |
| **Codex** | **12B** | **28.81%** | **46.81%** | **72.31%** |

Key comparisons:

- **GPT-3 175B = 0%**: A general 175B model cannot solve a single HumanEval problem without code fine-tuning
- **GPT-J 6B ≈ Codex-300M**: A general 6B model matches a code-specialized model with 20x fewer parameters — quantifies the value of code fine-tuning

## Temperature and Sampling Strategy

- **T=0.2**: Best for pass@1 — conservative, deterministic outputs give the best single shot
- **T=0.8**: Best for pass@100 — diverse outputs maximize the chance that at least one sample is correct
- **T=0.6**: Practical compromise when evaluating across all k values

### The Generate-and-Filter Insight

| Strategy | Accuracy |
|----------|----------|
| Single sample (pass@1) | 28.81% |
| Mean log-probability ranking (pick best of 100, no tests needed) | 44.5% |
| Oracle selection (pick correct one of 100, needs unit tests) | 72.31% |

The jump from 28.8% to 72.3% shows the model can solve ~72% of problems — it just doesn't do it reliably on the first try. Even without unit tests, mean log-probability ranking (picking the sample where the model was most confident) significantly improves over single-shot generation.

## APPS Benchmark Results

Codex-12B was also tested on APPS, a competitive programming benchmark — much harder than HumanEval:

| Difficulty | pass@1 | pass@100 |
|-----------|--------|----------|
| Introductory | 4.14% | 20.20% |
| Interview | 0.14% | 2.04% |
| Competition | 0.02% | 1.05% |

The contrast with HumanEval (28.8% pass@1) shows that Codex handles simple function-level tasks but struggles badly with harder algorithmic problems.

## Limitations

### Chain Degradation

The paper tested synthetic problems by chaining basic operations from a set of 13 building blocks (e.g., "convert to lowercase", "remove every third character", "reverse the string"). Each docstring chains multiple operations together.

**Finding: each additional chained operation drops the pass rate by roughly 2-3x.** A task with 2 operations might have 40% pass rate, 3 operations ~15%, 4 operations ~5%, and so on.

This exponential degradation is "uncharacteristic of a human programmer" — humans can follow longer instruction chains without such dramatic drops. It suggests Codex doesn't truly compose operations but rather pattern-matches partial sequences.

### Variable Binding

Codex struggles to track which operations apply to which variables. The paper gives a specific example with a function called `do_work`:

> Docstring: "Add 3 to y, then subtract 4 from both x and w. Return the product of the four numbers."

Codex-12B **fails to decrement the variable w** and **returns the wrong product**. The model correctly handles operations on some variables but loses track of others.

This is analogous to a known problem in image generation — models struggle to bind attributes to the right objects (e.g., "a red cube and a blue sphere" where colors get swapped). In code, it's binding operations to the right variables.

### Docstring Sensitivity

The model "struggles to parse through increasingly long and higher-level or system-level specifications." Specifically:

- Longer, more complex docstrings hurt performance disproportionately
- If the prompt contains subtle bugs or typos, Codex tends to produce worse code
- This persists even when the prompt also includes explicit instructions to write correct code

The model is sensitive to the surface form of the specification, not just its meaning.

---

## Related Documents

- [[llm/datasets/humaneval|HumanEval]] - The benchmark dataset
- [[llm/models/gpt3/gpt3-to-chatgpt/codex/architecture|Codex Architecture]] - Model sizes and specifications
- [[llm/models/gpt3/gpt3-to-chatgpt/codex/training|Codex Training]] - Training data and methodology
