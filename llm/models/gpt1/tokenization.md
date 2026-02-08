# GPT-1 Tokenization

Paper: ["Improving Language Understanding by Generative Pre-Training"](paper.pdf) (Radford et al., 2018)

## Overview

GPT-1 uses **character-level Byte Pair Encoding (BPE)** for tokenization. The tokenizer was trained on the same dataset used for pre-training (BooksCorpus).

**Key characteristics:**
- Character-level BPE (not byte-level like GPT-2)
- 478 base characters + 40,000 learned merges = 40,478 total vocabulary
- Trained on English text only
- Standard vocabulary size for 2018 (not innovative)

## Algorithm: Byte Pair Encoding (BPE)

GPT-1 uses [[llm/tokenization/bpe|BPE]], a subword tokenization algorithm originally developed for neural machine translation (Sennrich et al., 2016). BPE was already widely adopted by 2018 - GPT-1's use of it was standard practice, not an innovation.

## Training Data: BooksCorpus

**Dataset**: [[llm/datasets/bookscorpus|BooksCorpus]] - a collection of ~7,000-11,000 self-published books from [Smashwords.com](https://www.smashwords.com/)

**Size**: ~985 million words (~4-6 GB of text)

**Content**: Unpublished English novels across genres (romance, science fiction, fantasy, etc.)

**Current status**: The original BooksCorpus is **no longer publicly available** due to copyright concerns. See the [[llm/datasets/bookscorpus|BooksCorpus dataset page]] for the full story about why it was taken down and the controversy around its use.

**Why BooksCorpus**: Long-form narrative text provides better training data for learning long-range dependencies compared to shorter web text or news articles.

## Preprocessing Pipeline

Before applying BPE, the text underwent preprocessing:

1. **ftfy library** - Standardized punctuation, quotes, and whitespace
2. **spaCy tokenizer** - Pre-tokenized text into words
3. **BPE** - Learned 40,000 merge operations on the pre-tokenized text

This preprocessing approach was later simplified in GPT-2, which used byte-level BPE with regex-based pre-tokenization instead of spaCy.

## Vocabulary Composition

**Total vocabulary: 40,478 tokens**

- **Base vocabulary**: 478 characters
- **Learned merges**: 40,000 BPE operations
- **Special tokens**: `<unk>` for unknown tokens

### The 478 Base Characters

GPT-1 starts with 478 individual Unicode characters found in BooksCorpus. These break down into:

- **68 ASCII printable** characters (letters a-z, A-Z, digits 0-9, punctuation)
- **240 characters with `</w>` markers** (marks word boundaries - e.g., `t</w>` = "t at end of word")
- **170 Unicode characters** (accented letters like é, ñ, ü; symbols like ©, €, £, ∞; special chars like ♥, ♪)
- **1 special token**: `<unk>`

**Note**: The `</w>` (end-of-word) marker is a BPE convention that allows the tokenizer to distinguish between characters at word boundaries vs. within words.

See [extract_base_chars.py](extract_base_chars.py) for a Python script that extracts and displays all 478 base characters from the GPT-1 tokenizer.

## Character-Level vs Byte-Level BPE

**GPT-1 uses character-level BPE**, meaning:
- Base vocabulary consists of Unicode characters that appeared in the training data
- Limited to characters seen in BooksCorpus (primarily English with some European language accents)
- Cannot handle arbitrary Unicode characters not in the base vocabulary

**GPT-2 later switched to byte-level BPE**:
- Base vocabulary of exactly 256 bytes (UTF-8 encoding)
- Can represent any Unicode character as a sequence of bytes
- Universal across all languages

Character-level BPE made GPT-1 essentially **English-only** despite using Unicode characters.

## Vocabulary Size Comparison (2017-2018)

| Model | Year | Vocab Size | Tokenization Method |
|-------|------|------------|---------------------|
| Original Transformer | 2017 | 32K-37K | BPE on shared source-target vocabulary |
| GPT-1 | 2018 | **40,478** | Character-level BPE |
| BERT | 2018 | 30,000 | WordPiece |
| ELMo | 2018 | N/A | Character-level CNN |
| ULMFiT | 2018 | Varies | Word-level |

**Standard practice in 2018**: The 30K-40K vocabulary range was used in all 42 papers at the Conference of Machine Translation (WMT) during 2017-2018.

**Verdict**: GPT-1's vocabulary size of ~40K was **standard for the time, not innovative**. It fell within the established best practices for neural machine translation and language modeling.

## Implementation Details

### Determinism

BPE training is **theoretically deterministic** - given the exact same:
- Training data (same text, same order)
- Preprocessing (ftfy and spaCy versions and settings)
- BPE algorithm implementation
- Number of merges (40,000)

You would get the same tokenizer.

**However, in practice**, exact reproduction is difficult:
- **Tie-breaking**: When multiple byte pairs have the same frequency, different implementations may break ties differently
- **Preprocessing differences**: Exact tool versions matter
- **Data availability**: The original BooksCorpus is no longer available
- **Implementation variations**: Different BPE libraries may have subtle differences

### Special Tokens

- `<unk>`: Unknown token for characters/sequences not in the vocabulary
- Special token prediction was enabled in the model
- Start/end-of-sequence tokens were added for fine-tuning tasks

### Tokenizer Files

The GPT-1 tokenizer consists of:
- **vocab.json**: Maps tokens to integer IDs (40,478 entries)
- **merges.txt**: List of 40,000 BPE merge operations in order

These files are available from [HuggingFace's openai-gpt model](https://huggingface.co/openai-gpt).

## Key Takeaways

1. **Not innovative**: GPT-1's tokenization approach was standard practice for 2018
2. **English-centric**: Character-level BPE on English data made it unsuitable for multilingual use
3. **Standard vocabulary size**: 40K was the conventional choice, not a breakthrough
4. **Later improved**: GPT-2's byte-level BPE was a significant improvement for universality
5. **BooksCorpus unavailable**: The original training data is no longer accessible due to copyright issues

The real innovations in GPT-1 were in the **model architecture** (decoder-only transformer) and **training methodology** (pre-train → fine-tune paradigm), not in tokenization.
