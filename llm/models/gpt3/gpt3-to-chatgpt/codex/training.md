# Codex Training

**Paper**: ["Evaluating Large Language Models Trained on Code"](https://arxiv.org/abs/2107.03374) (Chen et al., July 2021)

The Codex paper describes three models with increasingly specialized training: base Codex (code generation), Codex-S (function synthesis from docstrings), and Codex-D (docstring generation from code). The training method is the same throughout — next-token prediction — but the data preparation differs significantly.

## Base Codex

### Training Data

- **Source**: 54 million public GitHub repositories, collected May 2020
- **Scope**: Python files only, under 1MB each
- **Raw size**: 179GB of unique Python files
- **After filtering**: 159GB — removed auto-generated files, files with average line length >100, max line length >1000, or low percentage of alphanumeric characters

### Tokenizer

Not a new tokenizer — they modified GPT-3's existing BPE tokenizer. The main change was adding **whitespace run tokens** to handle Python indentation efficiently. Code uses far more structured whitespace than natural text, and encoding each space individually is wasteful. The additional tokens represent whitespace runs of different lengths, reducing token count by ~30% compared to the unmodified GPT-3 tokenizer.

### Training Method

Standard next-token prediction on raw Python files. No special formatting, no separator tokens between files, no fill-in-the-middle objective. The simplicity is notable — the power came from scale (159GB of code) rather than any clever training tricks.

### Starting Point

Models were fine-tuned from pre-trained GPT checkpoints. Surprisingly, fine-tuning from GPT **did not improve final performance** over training from scratch — the code dataset was large enough. However, fine-tuning from GPT **did speed up convergence**, so they used this approach for all experiments.

## Codex-S (Supervised Fine-Tuning)

Codex-S is fine-tuned from base Codex for a specific task: given a function signature and docstring, generate the function body. This is the task measured by HumanEval.

### Why Codex-S Was Needed

Base Codex was trained on all kinds of Python files — class definitions, config files, scripts, data files. Most of this code is unrelated to synthesizing functions from docstrings. This **distribution mismatch** hurts HumanEval performance. Codex-S narrows the training distribution to match the actual task.

### Data Sources

Two sources of standalone function problems:

**1. Competitive programming sites (~10,000 problems)**

- Collected problem statements, function signatures, and solutions from programming contest and interview preparation websites
- Problem descriptions become docstrings, solutions become function bodies
- Unit tests were created from examples in problem statements, or extracted by submitting incorrect solutions to reveal hidden test cases
- Natural fit: competitive programming already has clear descriptions, signatures, and verifiable solutions

**2. CI-traced functions (~40,000 candidates)**

- Targeted open-source repos that use CI frameworks (travis, tox) and pip packages from PyPI
- Used Python's `sys.setprofile` to hook into the CI test suite execution
- During test runs, captured the actual **inputs and outputs** of every function called
- These captured input/output pairs became **unit tests** for each function
- Ran in a sandboxed environment since projects contained untrusted code

The CI-traced inputs/outputs are **not training data** — they're unit tests used for filtering and evaluation. The actual training data is still the function's signature + docstring + body.

**Why both sources matter**: The paper notes they're complementary. Competitive programming problems test algorithms and data structures. CI-traced functions are "building blocks of command-line utilities" — everyday code that tests the model's ability to follow instructions. Together they broaden the task distribution.

**Limitation of CI tracing**: Only ~40,000 functions were collected despite millions being available, because most functions either don't accept serializable inputs/return serializable outputs, or their runtime objects couldn't be pickled and restored outside the sandbox.

### Data Filtering

A critical step using **Codex-12B itself** as a filter:

1. For each candidate problem, generate 100 code samples from Codex-12B
2. Run each sample against the unit tests
3. If **zero** samples pass → discard the problem as too ambiguous or too difficult
4. Re-run multiple times to also catch stateful or non-deterministic problems

This is essentially self-curation — the model decides which problems are clear enough to be worth training on.

### Training Format

- **Prompt** (loss masked): function signature + docstring
- **Completion** (loss computed): function body
- Loss masking means the model only learns to generate function bodies, not to reproduce signatures or docstrings it will always be given at inference time
- Shorter prompts in a batch are left-padded to align the start of completions

### Training Details

- Learning rate: 1/10 of the base Codex fine-tuning rate
- Same learning rate schedule as base Codex
- Trained until validation loss plateaus (less than 10B tokens)

## Codex-D (Docstring Generation)

Codex-D is the reverse of Codex-S: given code, generate a docstring describing it.

### Motivation

The paper frames this as a **safety** feature — if you can generate code, you should also be able to describe what generated code does so humans can review it.

### Training Data

Uses the **exact same problems** as Codex-S. No new data collection needed — just rearranged.

### Training Format

- **Prompt** (loss masked): function signature + function body (the reference solution)
- **Completion** (loss computed): docstring

Same data as Codex-S, reversed order. The docstring moves from the prompt to the completion.

### Evaluation

Evaluating docstring quality is hard — natural language is subjective. They used a clever **round-trip evaluation**:

1. Codex-D generates a docstring from code
2. Feed that generated docstring into Codex-S
3. Codex-S generates code from the docstring
4. Run that code against unit tests

If the generated docstring captures the function's intent well enough, Codex-S should be able to reproduce functionally correct code from it.

### Back-Translation Reranking

They also tried using Codex-D to pick the best Codex-S output: generate multiple code samples, then score each by P(original docstring | generated code). Code that accurately reflects the docstring should score higher. However, this underperformed simpler mean log-probability ranking.

## The Model Hierarchy

```
GPT (pretrained on text)
  └─→ fine-tuned on 159GB Python code
      └─→ Codex (base code model)
          ├─→ fine-tuned on (signature + docstring → body)
          │   └─→ Codex-S (function synthesis)
          └─→ fine-tuned on (signature + body → docstring)
              └─→ Codex-D (docstring generation)
```

---

## Related Documents

- [[llm/models/gpt3/gpt3-to-chatgpt/codex/architecture|Codex Architecture]] - Model sizes and specifications
- [[llm/models/gpt3/gpt3-to-chatgpt/codex/backstory|Codex Backstory]] - Why OpenAI built Codex
- [[llm/models/gpt3/gpt3-to-chatgpt/overview|GPT-3 to ChatGPT Overview]] - Timeline and evolution
