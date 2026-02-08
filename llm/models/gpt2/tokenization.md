# GPT-2 Tokenization

Paper: ["Language Models are Unsupervised Multitask Learners"](paper.pdf) (Radford et al., 2019)

## Overview

GPT-2 switched from [[llm/models/gpt1/tokenization|GPT-1's character-level BPE]] to **byte-level BPE**. This was a significant improvement that became the standard tokenization approach for subsequent language models.

## Vocabulary Breakdown

**Total vocabulary: 50,257 tokens**

- **256** base byte tokens (one for each possible byte value, 0x00-0xFF)
- **50,000** learned BPE merges
- **1** special end-of-text token (`<|endoftext|>`)

This breakdown matters. GPT-1 had 478 base characters + 40,000 merges = 40,478. GPT-2 has 256 base bytes + 50,000 merges + 1 = 50,257.

## Byte-Level vs Character-Level BPE

### GPT-1: Character-Level

GPT-1's BPE operated on Unicode characters. The base vocabulary was 478 characters found in BooksCorpus — English letters, digits, punctuation, and some accented characters. The problem: to handle *all* possible Unicode (130,000+ code points), you'd need an impractically large base vocabulary before any merges even start. In practice, any character not in those 478 was mapped to `<unk>`.

### GPT-2: Byte-Level

GPT-2's BPE operates on raw bytes. Any UTF-8 string is just a sequence of bytes, and there are only 256 possible byte values. So the base vocabulary is always exactly 256 — no `<unk>` token needed, any string in any language can be tokenized.

The tradeoff: multi-byte Unicode characters must be reconstructed through merges. For ASCII text (1 byte = 1 character), this makes no difference. But for non-ASCII:

- `é` is 2 bytes in UTF-8 → needs at least 1 merge to become a single token
- A Chinese character (e.g., `中`) is 3 bytes → needs at least 2 merges
- An emoji (e.g., `😀`) is 4 bytes → needs at least 3 merges

This means some of the 50,000 merges are "spent" reconstructing multi-byte characters that character-level BPE would have had for free. This likely explains part of why GPT-2 increased from 40,000 to 50,000 merges — the byte-level approach needs extra merges to compensate for the lower starting point.

## The Cross-Category Merge Problem

Naively applying BPE to bytes creates suboptimal merges. Common words like `dog` appear in many contexts: `dog.`, `dog!`, `dog?`, ` dog` (with leading space). Standard BPE would learn separate tokens for each of these, wasting vocabulary capacity on variants that only differ by punctuation or whitespace.

GPT-2's fix: a regex pattern that prevents BPE from merging across character categories. Letters can't merge with punctuation, digits can't merge with letters, etc. One exception: spaces are allowed to merge with letters, so common patterns like ` the` (space + word) become single tokens.

This preserves vocabulary capacity for meaningful subword units rather than wasting it on accidental combinations.

## What Byte-Level BPE Eliminated

GPT-1's preprocessing pipeline was:

```
Raw text → ftfy (fix encoding) → spaCy (tokenization) → BPE
```

GPT-2 replaced all of this with:

```
Raw text → regex pre-tokenization → byte-level BPE
```

No ftfy, no spaCy, no language-specific tools. Any raw byte sequence works. This made the tokenizer simpler, more universal, and independent of external NLP libraries.

## Comparison

| | [[llm/models/gpt1/tokenization\|GPT-1]] | GPT-2 |
|---|---|---|
| **BPE type** | Character-level | Byte-level |
| **Base vocabulary** | 478 Unicode characters | 256 byte values |
| **Learned merges** | 40,000 | 50,000 |
| **Total vocabulary** | 40,478 | 50,257 |
| **Preprocessing** | ftfy → spaCy → BPE | Regex → BPE |
| **Unknown tokens** | Yes (`<unk>`) | No — any byte sequence is valid |
| **Language support** | Effectively English-only | Any language (via UTF-8 bytes) |
| **Special tokens** | `<unk>`, task-specific tokens | `<\|endoftext\|>` |

## Legacy

GPT-2's byte-level BPE became the standard. GPT-3 used the same tokenizer (same 50,257 vocabulary). Later models increased vocabulary size further — GPT-4 went to ~100K tokens, LLaMA 3 to 128K — but the byte-level BPE approach introduced by GPT-2 remained the foundation.
