# GPT-3 Few-Shot Learning (In-Context Learning)

*From "Language Models are Few-Shot Learners" (Brown et al., 2020)*

## The Core Idea

**In-context learning** is GPT-3's signature capability: the model learns to perform tasks during inference by observing examples provided in the prompt, without any weight updates or gradient descent.

The paper evaluates three settings:

- **Zero-shot**: Task description only, no examples
  ```
  Translate English to French:
  cheese =>
  ```

- **One-shot**: Task description + 1 example
  ```
  Translate English to French:
  sea otter => loutre de mer
  cheese =>
  ```

- **Few-shot**: Task description + multiple examples (typically 10-100)
  ```
  Translate English to French:
  sea otter => loutre de mer
  peppermint => menthe poivrée
  plush giraffe => girafe peluche
  cheese =>
  ```

The key distinction: the model sees examples only at inference time through the context window. No fine-tuning, no weight updates—just forward passes.

## Why This is Revolutionary

Few-shot learning represented a paradigm shift from **fine-tuning** to **prompting**:

- **Same model, infinite tasks**: One 175B parameter model handles translation, question answering, arithmetic, and more—just by changing the prompt
- **No labeled datasets needed**: Users provide a few examples inline, not thousands in a training set
- **No task-specific training**: Eliminates the need for gradient updates on task-specific data
- **API-first deployment**: Enabled the GPT-3 API business model where users access one general model

This capability launched the "prompt engineering" era and became the foundation for ChatGPT and all modern LLM interactions.

## The Scaling Story: Why Size Matters

The paper's most striking finding: **in-context learning emerges at scale**.

Figure 1.2 shows that larger models make "increasingly efficient use of in-context information":

- **175B (GPT-3)**: Steep meta-learning curves—dramatic improvement from 0 → 10 → 100 examples
- **13B**: Moderate improvement from examples
- **1.3B (similar to GPT-2)**: Nearly flat curves—few-shot barely helps

The capability didn't exist in GPT-2 (1.5B parameters). It began emerging around 13B parameters and became highly effective at 175B.

This validated the **scaling hypothesis**: capabilities that don't work at small scales can suddenly emerge at larger scales.

## Performance Gains from Few-Shot

Figure 1.3 aggregates results across 42 benchmarks, showing consistent ordering: **few-shot > one-shot > zero-shot**, with the gap widening for larger models.

Task-specific examples:

**LAMBDA** (language modeling):
- Zero-shot: 68.0%
- One-shot: 72.5%
- Few-shot (K=15): **86.4%**

**TriviaQA** (question answering):
- Zero-shot: 64.3%
- One-shot: 68.0%
- Few-shot (K=64): **71.2%** (matches fine-tuned SOTA)

**Translation (En→Fr)**:
- Zero-shot: 25.2 BLEU
- One-shot: 28.3 BLEU
- Few-shot (K=64): **32.6 BLEU**

Not all tasks benefit equally. **Winograd Schema Challenge**:
- Zero-shot: 88.3%
- One-shot: 89.7%
- Few-shot (K=32): 88.6% (minimal gain, task already near-saturated)

## How It Works (Theory)

The paper doesn't provide a mechanistic explanation, but offers this hypothesis:

> "During pre-training, a language model develops a broad set of skills and pattern recognition abilities. Then at inference time, it uses those abilities at run-time to rapidly adapt to or recognize the desired task."

Key mechanisms:

1. **Context as task specification**: Examples clarify the format, style, and intent beyond what a task description can convey
2. **Pattern matching from pre-training**: The model recognizes task patterns it encountered during training across 300B tokens
3. **Meta-learning hypothesis**: The model learns "how to learn" during pre-training by seeing many tasks in different contexts

The paper describes this as "meta-learning"—the model isn't learning the task during inference (no weight updates), but rather recognizing which of its pre-trained capabilities to activate.

## Limitations

Few-shot learning isn't magic:

- **Novel reasoning**: Still struggles on tasks requiring reasoning patterns not seen during pre-training
- **Diminishing returns**: After K≈100 examples, gains plateau (likely due to context window limits)
- **Context length**: 2048 tokens total, including prompt and completion—limits how many examples fit
- **Task-dependent**: Some tasks (like word sense disambiguation) show minimal benefit from examples

Example: **4-digit arithmetic** accuracy remains at 25.5% few-shot, suggesting the model hasn't learned the algorithmic pattern even with examples.

## The Progression: GPT-1 → GPT-2 → GPT-3

| Model | Paradigm | Requires Labeled Data? | Weight Updates? |
|-------|----------|----------------------|----------------|
| **GPT-1** | Fine-tuning | Yes (thousands of examples) | Yes (gradient descent) |
| **GPT-2** | Zero-shot | No (task description only) | No |
| **GPT-3** | Few-shot | No (just prompt examples) | No |

Each generation expanded what's possible without task-specific training:

- **GPT-1**: Showed pre-training helps, but still needs fine-tuning
- **GPT-2**: Showed zero-shot works for some tasks, but vague task specifications limit performance
- **GPT-3**: Showed few-shot bridges the gap—clear task specification without training data

Importantly, GPT-3 didn't lose zero-shot capability; it **added** few-shot on top. Users can choose the appropriate setting.

## Impact on the Field

Few-shot learning fundamentally changed how we interact with language models:

- **Prompt engineering era**: Spawned an entire field of crafting effective prompts and examples
- **Instruction-following**: Enabled ChatGPT by showing the model can follow instructions given as examples
- **API-first products**: Made it practical to serve one general model via API rather than distributing fine-tuned models
- **Democratized AI**: Users without ML expertise can adapt models by providing examples, not by training

This capability is why GPT-3 became a platform (the GPT-3 API) rather than just a research artifact.

---

## Related Documents

- [[llm/models/gpt3/architecture|GPT-3 Architecture]] - Model specs and what changed from GPT-2
- [[llm/models/gpt3/training|GPT-3 Training]] - Hyperparameters, infrastructure, costs
- [[llm/models/gpt3/training-data|GPT-3 Training Data]] - Dataset composition
- [[llm/models/gpt3/experiments|GPT-3 Experiments]] - Benchmark results across task categories
- [[llm/models/gpt2/zero-shot|GPT-2 Zero-Shot]] - The previous generation's capability
- [[llm/models/gpt1/experiments|GPT-1 Experiments]] - Fine-tuning baseline for comparison
