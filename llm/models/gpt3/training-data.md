# GPT-3 Training Data

Paper: ["Language Models are Few-Shot Learners"](paper.pdf) (Brown et al., 2020)

## Overview

GPT-3 was trained on **300 billion tokens** from a carefully curated mixture of five datasets. Unlike prior models that used datasets proportionally to their size, GPT-3 employed a **weighted sampling strategy** that intentionally oversampled high-quality sources and undersampled lower-quality ones.

The key philosophy: accept some overfitting on high-quality data in exchange for better overall model quality.

**The secrecy problem**: OpenAI disclosed the dataset composition but left critical implementation details vague or unstated. This lack of transparency frustrated researchers and motivated the [[llm/data-processing/open-replication-era|open replication movement]] that followed.

## Dataset Composition

| Dataset | Raw Size (tokens) | Training Weight | Epochs Seen | Source Type |
|---------|-------------------|-----------------|-------------|-------------|
| **Common Crawl (filtered)** | **410 billion** | **60%** | **0.44** | Web crawl |
| **WebText2** | **19 billion** | **22%** | **2.9** | Reddit-curated web |
| **Books1** | **12 billion** | **8%** | **1.9** | Book corpus |
| **Books2** | **55 billion** | **8%** | **0.43** | Book corpus |
| **Wikipedia** | **3 billion** | **3%** | **3.4** | Encyclopedia |

**Key insight**: Training weight ≠ raw size. WebText2 is only 19B tokens but gets 22% of training (seen 2.9×), while Books2 is 55B tokens but also gets only 8% (seen 0.43×). This reflects deliberate quality weighting.

## Dataset Details

### Common Crawl (60% of training)

**What it is**: The massive web crawl maintained by the Common Crawl foundation, containing petabytes of web pages.

**GPT-3's approach**:

- Downloaded from **41 shards of monthly Common Crawl** covering 2016-2019
- Started with **45TB of compressed plaintext**
- Filtered down to **570GB** after processing (~99% reduction)
- Final size: **~410 billion tokens**

**Why undersampled**: Despite being the largest dataset, Common Crawl has highly variable quality. GPT-3 trained for only 0.44 epochs (seeing less than half of it once) to avoid overexposure to lower-quality content.

### WebText2 (22% of training)

**What it is**: An expanded version of the [[llm/datasets/webtext|WebText]] corpus used for [[llm/models/gpt2/training|GPT-2]].

**Collection method**:

- Scrape all outbound links from Reddit posts with karma ≥ 3
- Use Reddit's upvote system as a distributed human quality filter
- WebText2 extends the collection period beyond WebText's December 2017 cutoff

**Size**: ~19 billion tokens (~8 million documents)

**Why oversampled**: High trust in Reddit-curated quality. The model saw WebText2 2.9× during training, accepting deliberate memorization in exchange for quality.

### Books1 (8% of training)

**What it is**: An internet-based books corpus.

**Size**: ~12 billion tokens

**Training**: Seen 1.9 epochs (nearly twice through the dataset)

**Details not disclosed**: The paper provides no information about:

- Source of books (likely to avoid copyright controversy similar to [[llm/datasets/bookscorpus|BooksCorpus]])
- Quality criteria
- Genre distribution
- Why it's separate from Books2

### Books2 (8% of training)

**What it is**: A second internet-based books corpus.

**Size**: ~55 billion tokens (4.6× larger than Books1)

**Training**: Seen only 0.43 epochs (less than half the dataset)

**Why undersampled**: Despite being much larger than Books1, Books2 gets the same training weight (8%). This suggests significantly lower quality or less curated content. The model deliberately saw Books1 more frequently per token than Books2.

**Details not disclosed**: Same information gaps as Books1.

### Wikipedia (3% of training)

**What it is**: English Wikipedia, the online encyclopedia.

**Size**: ~3 billion tokens

**Training**: Seen 3.4 epochs (over 3× through the dataset)

**Why included**: Unlike [[llm/models/gpt2/training|GPT-2]], which deliberately **excluded** Wikipedia to avoid benchmark contamination, GPT-3 decided the benefits (high-quality factual knowledge) outweighed the contamination concerns.

**Why oversampled**: High trust in Wikipedia's editorial quality. Despite being the smallest dataset, it's heavily oversampled.

## Data Quality Filtering

The GPT-3 paper describes a **3-step filtering process** to improve data quality:

### 1. Similarity-Based Filtering

**Goal**: Filter Common Crawl for documents similar to known high-quality reference corpora.

**Method**: Train a classifier to identify high-quality text, then use it to filter Common Crawl.

**Details not disclosed**:

- What reference corpora were used as "high quality" examples
- What type of classifier (neural? logistic regression?)
- Similarity thresholds
- This is mentioned as described in "Appendix A" but those implementation details are not provided

### 2. Fuzzy Deduplication

**Goal**: Remove near-duplicate documents to prevent the model from memorizing repeated content.

**Scope**: Applied both **within** each dataset and **across** all datasets.

**Method**: Used fuzzy matching rather than exact deduplication (likely MinHash or similar LSH technique).

**Why this matters**: Without deduplication, the model would waste capacity memorizing the same information repeated across multiple sources.

**Details not disclosed**:

- Exact algorithm (MinHash? SimHash? Other LSH?)
- Similarity thresholds for considering documents "duplicates"
- How much data was removed by deduplication

### 3. Dataset Augmentation

**Goal**: Add curated high-quality datasets to increase diversity beyond Common Crawl.

**Result**: Added WebText2, Books1, Books2, and Wikipedia as deliberate augmentation to improve quality and domain coverage.

**Motivation**: Pure web crawl, even filtered, still lacks the long-form coherence of books and the factual density of Wikipedia.

## Data Contamination Problem

### The Issue

A **major methodological concern** explicitly acknowledged in the paper:

> "A major methodological concern with language models pretrained on a broad swath of internet data, particularly large models with the capacity to memorize vast amounts of content, is potential contamination of downstream tasks by having their test or development sets inadvertently seen during pre-training."

If GPT-3's training data contains test sets from evaluation benchmarks, the model's impressive performance might be partially due to **having seen the answers during training**, not true generalization.

### What They Did

**Attempted solution**: Search for and remove overlaps between training data and the development/test sets of all benchmarks studied in the paper.

**Critical bug**: A bug in the filtering code caused them to only remove duplicates found in the *training* sets, not validation/test sets of benchmarks. This means some test data likely remained in GPT-3's training corpus.

**Post-hoc analysis**: In Section 4 of the paper, they characterize the impact of remaining overlaps and attempt to quantify how much contamination affects results.

### What They Chose Not to Fix

> "Unfortunately, a bug in the filtering caused us to ignore some overlaps, and due to the cost of training it was not feasible to retrain the model."

**The decision**: Accept the contamination rather than spend millions of dollars retraining.

**Future work**: The paper notes that "in future work we will more aggressively remove data contamination."

### Why This Matters

GPT-3's zero-shot performance on benchmarks like:

- Penn Treebank (20.5 perplexity)
- LAMBADA (76.2% accuracy)
- Various SuperGLUE tasks

...might be inflated by having seen some test examples during training. The paper attempts to be transparent about this limitation, but the exact impact remains unclear.

## Training Philosophy: Quality Over Purity

GPT-3's data strategy represents a deliberate trade-off:

**Accept**:

- Some overfitting (Wikipedia seen 3.4×, WebText2 seen 2.9×)
- Some data contamination (due to filtering bugs)
- Unbalanced sampling (small high-quality datasets overweighted)

**In exchange for**:

- Higher average data quality
- Better domain diversity
- Stronger performance on real-world tasks

This philosophy is captured in the paper:

> "This essentially accepts a small amount of overfitting in exchange for higher quality training data."

## Comparison to GPT-2

| Aspect | GPT-2 | GPT-3 |
|--------|-------|-------|
| **Total tokens** | ~10 billion | 300 billion (30× larger) |
| **Primary dataset** | [[llm/datasets/webtext\|WebText]] (40GB) | Common Crawl (570GB filtered) |
| **Number of sources** | 1 (WebText only) | 5 (diverse mix) |
| **Wikipedia included?** | No (deliberately excluded) | Yes (3%, oversampled) |
| **Weighted sampling?** | No (single source) | Yes (quality-based weighting) |
| **Data contamination** | Avoided by excluding Wikipedia | Acknowledged and partially addressed |

## What Is Not Disclosed

**This section is critical to understanding GPT-3's impact on the field.** The vague or missing details below became a major source of frustration for researchers trying to replicate GPT-3's results. This opacity directly motivated the [[llm/data-processing/open-replication-era|open replication era]] (2021-2023), where projects like The Pile, RedPajama, and LLaMA proved that full transparency was both possible and beneficial for research.

The paper is notably silent on several key details, likely for competitive and legal reasons:

### Books1 and Books2

- **Source**: Where did these books come from? (Avoiding BooksCorpus-style copyright controversy)
- **Distinction**: Why two separate book corpora? What makes Books1 different from Books2?
- **Quality criteria**: Why does Books2 (4.6× larger) get heavily undersampled while Books1 gets oversampled?
- **Legality**: What copyright arrangement allows this data to be used?

### Common Crawl Filtering

- **Reference corpora**: What was used as "high quality" reference for similarity filtering?
- **Classifier details**: What model? How was it trained?
- **Similarity thresholds**: What cutoffs were used to include/exclude documents?
- **Deduplication algorithm**: MinHash? SimHash? Exact thresholds?

### Sampling Strategy

- **How were the weights chosen?** Was 60/22/8/8/3 empirically tuned, or based on intuition?
- **Ablation studies**: Did they try other weight combinations?
- **Optimal trade-offs**: How do you decide when overfitting on high-quality data becomes harmful?

### Training Compute

- **Total cost**: The paper shows ~3,640 petaflop/s-days for GPT-3 175B, but doesn't disclose dollar cost
- **Hardware**: Trained on V100 GPUs via Microsoft cluster, but how many GPUs? For how long?

## Impact on Later Models

GPT-3's data strategy influenced subsequent models:

**Chinchilla (2022)**: Showed GPT-3 was actually **undertrained**. For a fixed compute budget, you should scale parameters and data together. GPT-3 had 175B params but only 300B tokens (1.7 tokens per parameter). Chinchilla used 70B params on 1.4T tokens (20 tokens per parameter) and performed better.

**LLaMA (2023)**: Followed Chinchilla's insight, training smaller models on much more data. Also moved away from books corpora due to copyright concerns, focusing on publicly documented datasets. Importantly, Meta disclosed all sources completely—no Books1/Books2 mystery—setting a new transparency standard.

For detailed coverage of how these and other projects approached data transparency, see [[llm/data-processing/open-replication-era|The Open Replication Era]].

**Post-2023 models**: Most now train on trillions of tokens with more transparent dataset documentation, avoiding the "Books1/Books2" style secrecy.

## Key Takeaways

1. **Quality weighting matters**: Don't sample datasets proportionally—oversample high-quality sources
2. **Diversity matters**: Multi-domain data (web + books + encyclopedia) beats single-domain
3. **Deduplication is critical**: Remove repetition to prevent memorization waste
4. **Data contamination is hard**: Even well-funded teams make filtering mistakes
5. **Trade-offs are acceptable**: Some overfitting on high-quality data is better than no exposure
6. **Scale is expensive**: Bugs that would require retraining are too costly to fix at this scale
7. **Transparency is limited**: Competitive and legal pressures prevent full disclosure

## The Response: Open Replication

GPT-3's secrecy, particularly around Books1/Books2 and filtering details, frustrated the research community and motivated a transparency movement. For how the field responded, see [[llm/data-processing/open-replication-era|The Open Replication Era]].
