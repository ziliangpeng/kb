# WebText

## Overview

WebText is a web text corpus created by OpenAI in 2018-2019, used to train [[llm/models/gpt2/architecture|GPT-2]]. It contains slightly over 8 million documents totaling approximately 40GB of text (~9-10 billion BPE tokens).

OpenAI never released WebText publicly.

## Construction Pipeline

The core idea: use Reddit as a distributed human quality filter.

1. **Scrape Reddit links** — Collect all outbound URLs from Reddit posts that received at least 3 karma (upvotes minus downvotes). The intuition: if multiple users upvoted a link, the content is likely interesting, educational, or at least engaging. This yielded 45 million links.

2. **Extract text** — Download pages and extract text content using a combination of the Dragnet and Newspaper Python libraries.

3. **Filter non-English** — Remove non-English pages using Facebook's FastText language classifier.

4. **Deduplicate** — Identify near-duplicate documents using Local Sensitivity Hashing (LSH). Documents with a similarity threshold greater than 0.5 were removed.

5. **Minimum length** — Remove documents with fewer than 128 tokens.

6. **Remove Wikipedia** — Deliberately exclude all Wikipedia documents to avoid data contamination, since Wikipedia is commonly used in evaluation benchmarks.

**Note**: The GPT-2 paper used a preliminary version of WebText that excluded links created after December 2017.

## Dataset Statistics

- **Raw links scraped**: 45 million
- **Documents after cleaning**: slightly over 8 million
- **Total size**: ~40GB of text
- **Estimated tokens**: ~9-10 billion BPE tokens

## Comparison to BooksCorpus

| | [[llm/datasets/bookscorpus|BooksCorpus]] | WebText |
|---|---|---|
| **Size** | ~5GB (~985M words) | ~40GB (~9-10B tokens) |
| **Documents** | ~7,000-11,000 books | ~8 million web pages |
| **Domain** | Fiction books (single domain) | Multi-domain web content |
| **Quality signal** | Self-published on Smashwords | Reddit karma ≥ 3 |
| **Diversity** | Low (romance, sci-fi, fantasy) | High (whatever Reddit users link to) |
| **Used by** | GPT-1, BERT | GPT-2 |

The ~10× jump in scale and massive increase in domain diversity were key factors in GPT-2's improved capabilities over GPT-1.

## Never Released

OpenAI never released WebText, the training code, or (initially) the full model. This became a significant point of contention in the research community.

## Open-Source Replications

### OpenWebText

Aaron Gokaslan and Vanya Cohen, two Brown University master's students, created [OpenWebText](https://github.com/jcpeterson/openwebtext) as an open-source replication. Their version used Pushshift.io archives of Reddit data and replicated the same filtering pipeline.

Four years later, Gokaslan noted: "The dataset has only become more important and a de facto industry standard because OpenAI never released the dataset used to train their GPT-2 model or any of the training code."

Available on Hugging Face: [Skylion007/openwebtext](https://huggingface.co/datasets/Skylion007/openwebtext)

### OpenWebText2

EleutherAI later created OpenWebText2, an expanded version of the dataset, as part of their effort to build open-source language models (GPT-Neo, GPT-J, GPT-NeoX).
