# GPT-2 Training

Paper: ["Language Models are Unsupervised Multitask Learners"](paper.pdf) (Radford et al., 2019)

## Objective

Same as [[llm/models/gpt1/pre-training|GPT-1]]: next-token prediction (autoregressive language modeling). No changes to the training objective.

## Training Data: WebText

GPT-1 used [[llm/datasets/bookscorpus|BooksCorpus]] — a single domain (fiction books), ~1B words, trained for 100 epochs. GPT-2 needed something much larger and more diverse.

The GPT-2 authors wanted "as large and diverse a dataset as possible" to train a general-purpose language model. Common Crawl was the obvious candidate, but they found its content quality was poor ("mostly unintelligible"). Instead, they built [[llm/datasets/webtext|WebText]] — scraping all outbound links from Reddit posts with ≥3 karma, using Reddit users as a distributed human quality filter.

The result: ~8 million documents, ~40GB of text (~10B tokens). This was a ~10× increase over BooksCorpus in scale and a massive increase in domain diversity.

Key decisions:

- **Wikipedia excluded** — deliberately removed to avoid data contamination with evaluation benchmarks
- **Preliminary version** — the paper used a version excluding links created after December 2017
- **No language-specific preprocessing** — paired with the new byte-level BPE tokenizer, the pipeline was simpler and more universal than GPT-1's ftfy → spaCy → BPE chain

### The Shift: Large Data, Fewer Epochs

GPT-1 trained over BooksCorpus for ~100 epochs — repeating the same ~1B words over and over to compensate for limited data. GPT-2 moved to a much larger dataset and likely trained for far fewer epochs. The paper notes that all models still underfit WebText, meaning even the 1.5B model hadn't saturated the data.

This shift from "small data, many epochs" to "large data, fewer epochs" was a precursor to the Chinchilla insight (2022) that data scaling matters as much as parameter scaling.

## Training Procedure

The GPT-2 paper was unusually sparse on training details. Here is what was confirmed from the paper and released code:

- **Batch size**: 512 sequences × 1024 tokens = ~0.5M tokens per batch
- **Context length**: 1024 tokens
- **Hardware**: 256 TPU v3 cores
- **Learning rate**: Manually tuned per model size for best perplexity on a 5% held-out sample of WebText. Specific values were not disclosed.
- **Weight initialization**: Standard weights initialized with stddev=0.02. Residual layer weights scaled by 1/√N at initialization, where N is the number of residual layers. This prevents the residual stream from growing too large in deeper models.
- **LayerNorm epsilon**: 1e-5 (from released code)

### What the Paper Didn't Disclose

The following details were not provided in the paper or released code:

- Optimizer (GPT-1 used Adam)
- Learning rate schedule (GPT-1 used warmup + cosine annealing)
- Specific learning rate values for each model size
- Dropout rate (GPT-1 used 0.1)
- Gradient clipping
- Number of training steps or epochs
- Total training duration
- Mixed precision settings (though TPU v3 natively supports bfloat16)

## Underfitting WebText

An important observation from the paper: all four model sizes still underfit WebText. Both training and test perplexity continued improving as model size increased, with no signs of saturation. This meant the dataset still had more to teach even the largest 1.5B model.

This directly foreshadowed GPT-3 — if GPT-2 was still underfit, then training an even larger model on even more data should yield further gains. And it did.

## No Fine-Tuning

GPT-2 was evaluated purely zero-shot — no task-specific fine-tuning at all. This was a deliberate philosophical choice, not a limitation. The goal was to test whether pre-training alone, at sufficient scale, could produce task capabilities without any adaptation.

This was the opposite of GPT-1, which required fine-tuning with task-specific heads and input transformations for each downstream task.

## Comparison to GPT-1 Training

| | GPT-1 | GPT-2 |
|---|---|---|
| **Dataset** | [[llm/datasets/bookscorpus\|BooksCorpus]] (~1B words) | [[llm/datasets/webtext\|WebText]] (~10B tokens) |
| **Data diversity** | Single domain (fiction books) | Multi-domain (web pages) |
| **Epochs** | ~100 | Unknown (likely far fewer) |
| **Batch size** | 64 sequences | 512 sequences (~0.5M tokens) |
| **Context length** | 512 tokens | 1024 tokens |
| **Hardware** | 8 GPUs, ~1 month | 256 TPU v3 cores |
| **Fine-tuning** | Yes (task-specific heads) | None (zero-shot only) |
