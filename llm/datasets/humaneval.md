# HumanEval

## Overview

HumanEval is a benchmark dataset of **164 hand-written Python programming problems** for evaluating code generation models. Introduced in the [[llm/models/gpt3/gpt3-to-chatgpt/codex/architecture|Codex]] paper (Chen et al., July 2021), it became the standard benchmark for measuring code generation quality.

**Paper**: ["Evaluating Large Language Models Trained on Code"](https://arxiv.org/abs/2107.03374)
**Repository**: [openai/human-eval](https://github.com/openai/human-eval) (MIT license)
**Hugging Face**: [openai/openai_humaneval](https://huggingface.co/datasets/openai/openai_humaneval)

## Format

Each problem contains:

| Field | Description |
|---|---|
| `task_id` | Identifier, e.g., `"HumanEval/0"` through `"HumanEval/163"` |
| `prompt` | Function signature + docstring (what the model sees) |
| `canonical_solution` | Reference implementation (hidden from model) |
| `test` | A `check(candidate)` function with assert statements (hidden from model) |
| `entry_point` | The function name |

The model receives only the **prompt** and must generate the **function body**. The generated code is then executed against the hidden unit tests.

## Example Problem

**What the model sees (prompt):**
```python
from typing import List

def has_close_elements(numbers: List[float], threshold: float) -> bool:
    """Check if in given list of numbers, are any two numbers
    closer to each other than given threshold.
    >>> has_close_elements([1.0, 2.0, 3.0], 0.5)
    False
    >>> has_close_elements([1.0, 2.8, 3.0, 4.0, 5.0, 2.0], 0.3)
    True
    """
```

**What the model generates:** the function body.

**Hidden unit tests (model never sees these):**
```python
def check(candidate):
    assert candidate([1.0, 2.0, 3.9, 4.0, 5.0, 2.2], 0.3) == True
    assert candidate([1.0, 2.0, 3.9, 4.0, 5.0, 2.2], 0.05) == False
    assert candidate([1.0, 2.0, 5.9, 4.0, 5.0], 0.95) == True
    assert candidate([1.0, 2.0, 5.9, 4.0, 5.0], 0.8) == False
    # ... (7 assertions total)
```

## Dataset Statistics

- **Problems**: 164
- **Language**: Python only
- **Average unit tests per problem**: 7.7
- **Difficulty distribution**: ~85% easy, ~15% medium, <1% hard
- **Topics**: Mathematics, control flow, basic data structures, string manipulation, simple algorithms
- **Missing concepts**: Trees, graphs, dynamic programming, OOP, backtracking — 14 of 38 programming concepts are absent

## Execution and Evaluation

**Code execution pipeline:**

1. Concatenate: prompt + model completion + hidden test function
2. Execute via Python `exec()` in a subprocess with timeout
3. Dangerous operations blocked (`os.remove`, `subprocess.Popen`, etc.)
4. OpenAI internally used **gVisor** container sandboxing
5. Result: "passed" (all assertions succeed), "timed out", or "failed"

**The pass@k metric:**

Rather than generating one sample, generate **n samples** per problem (paper uses n=200), count how many pass all tests (c), then compute:

```
pass@k = 1 - C(n-c, k) / C(n, k)
```

This is an **unbiased estimator** introduced by the Codex paper. `C(n-c, k) / C(n, k)` is the probability that all k randomly chosen samples are wrong; subtracting from 1 gives the probability that at least one is correct. The final pass@k for the model is the average across all 164 problems.

Standard reporting uses k = 1, 10, and 100.

## Why Hand-Written

The problems were hand-written by OpenAI researchers specifically to avoid **data contamination**. Codex was trained on 54 million GitHub repositories, which already contain solutions to existing benchmarks (LeetCode, Codeforces, Project Euler, etc.). Hand-writing new problems was the only way to ensure the model hadn't seen the answers during training.

## Why It Became the Standard

- **Functional correctness**: Code must actually run and pass tests — a major improvement over BLEU-score evaluation, which the paper showed is unreliable for code
- **Simple and reproducible**: 164 problems, clear format, MIT license, open-source evaluation harness
- **First-mover advantage**: Bundled with the influential Codex paper that powered GitHub Copilot
- **pass@k metric**: Became the universal reporting format for code generation results

## Known Criticisms

- **Too easy / saturated**: Top models now score 95%+ on pass@1. The benchmark has lost discriminative power between frontier models.
- **Too narrow**: Python only, single functions only. No multi-file projects, no OOP, no real-world library usage.
- **Insufficient tests**: EvalPlus showed that adding 80x more tests dropped pass rates by 19-29% — many "passing" solutions were actually wrong with only 7.7 tests per problem.
- **Benchmark bugs**: EvalPlus found 18 defects (11% of problems) in the original ground-truth solutions.
- **Data contamination risk**: The problems have spread across GitHub forks, blog posts, and Hugging Face, potentially leaking into later models' training data.

## Successors

| Year | Benchmark | What Changed |
|---|---|---|
| 2021 | **MBPP** (Google) | 974 basic Python problems, tests visible in prompt |
| 2021 | **APPS** | Competitive programming, much harder |
| 2022 | **CodeContests** (DeepMind) | Competition-level algorithmic problems |
| 2023 | **HumanEval+** (EvalPlus) | 80x more tests for HumanEval, caught many false positives |
| 2023 | **HumanEval-X** | Multilingual (Python, C++, Java, JS, Go) |
| 2024 | **SWE-bench** | Real GitHub issues, multi-file changes |
| 2024 | **LiveCodeBench** | Continuously updated to prevent contamination |

The trajectory: single-function puzzles → competitive programming → real-world software engineering → continuously updated live benchmarks.

## Data Format

Stored as `HumanEval.jsonl.gz` — one JSON object per line, gzipped. Each line:

```json
{
  "task_id": "HumanEval/0",
  "prompt": "from typing import List\n\ndef has_close_elements(...",
  "canonical_solution": "    for idx, elem in enumerate(numbers):\n        ...",
  "test": "def check(candidate):\n    assert candidate(...",
  "entry_point": "has_close_elements"
}
```

---

## Related Documents

- [[llm/models/gpt3/gpt3-to-chatgpt/codex/evaluation|Codex Evaluation & Results]] - Codex's performance on HumanEval
- [[llm/models/gpt3/gpt3-to-chatgpt/codex/architecture|Codex Architecture]] - The model evaluated on this benchmark
