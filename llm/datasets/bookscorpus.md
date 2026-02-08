# BooksCorpus: A Controversial Dataset

## Overview

BooksCorpus is a dataset of ~7,000-11,000 unpublished books that became one of the most widely used datasets in NLP research from 2015-2020. It was used to train landmark models including BERT, GPT-1, and many others.

However, it's also one of the most controversial datasets in machine learning due to copyright violations and ethical concerns around consent. The dataset is no longer officially available.

## History

### Creation (2015)

**Paper**: "Aligning Books and Movies: Towards Story-like Visual Explanations by Watching Movies and Reading Books" (Zhu et al., 2015)

**Source**: Researchers from University of Toronto and MIT scraped books from [Smashwords.com](https://www.smashwords.com/), a self-publishing platform.

**Collection method**:
- Targeted books marked as "free to read" on Smashwords
- Scraped ~7,000-11,000 books automatically
- Filtered for books longer than 20,000 words
- Total: ~985 million words (~4-6 GB of text)

**Genres**: Romance, science fiction, fantasy, and other popular fiction genres heavily represented.

### Rise to Prominence (2015-2019)

BooksCorpus became the go-to dataset for pre-training language models because:

1. **Long-form narrative text**: Better for learning long-range dependencies than news articles or web text
2. **Large scale**: Nearly 1 billion words of continuous text
3. **Publicly available**: Initially distributed freely by the researchers
4. **Easy to use**: Single, cohesive dataset rather than requiring scraping

**Major models trained on BooksCorpus**:
- **GPT-1 (2018)**: Used BooksCorpus exclusively for pre-training
- **BERT (2018)**: Combined BooksCorpus with English Wikipedia
- **RoBERTa (2019)**: Included BooksCorpus in training mix
- **Many others**: Became a standard benchmark dataset

### The Copyright Problem

**The fundamental issue**: The researchers never obtained permission from the book authors to:
- Redistribute their copyrighted works
- Use their creative writing in machine learning datasets
- Allow others to download and use their books

**Why this matters**:
- Being "free to read" on Smashwords ≠ permission to redistribute
- Authors retained full copyright to their works
- Many authors specifically chose NOT to allow their books on other platforms
- The dataset violated the terms of service of Smashwords
- Authors discovered their books in the dataset without their knowledge or consent

**Legal implications**:
- Direct copyright infringement for hundreds of books
- Violated distribution rights that authors explicitly retained
- Created derivatives (ML models) from copyrighted material without license

### Takedown (2019-2020)

**What happened**:
- Authors began discovering their books were in the dataset
- Copyright concerns were raised publicly
- The original researchers removed the official distribution
- The authors' website no longer hosts the dataset
- Smashwords became aware of the unauthorized scraping

**Official status**: No longer distributed by the creators. The paper remains, but the dataset download links are dead.

## Current Availability (2025)

### Official Status: NOT AVAILABLE

The original BooksCorpus is not officially distributed. The researchers have taken it down and do not provide access.

### Unofficial Mirrors

Despite the takedown, several unauthorized copies exist:

**HuggingFace Datasets**:
- [bookcorpus/bookcorpus](https://huggingface.co/datasets/bookcorpus/bookcorpus) - 74M+ rows, ~4.61 GB
- [rojagtap/bookcorpus](https://huggingface.co/datasets/rojagtap/bookcorpus) - Alternative mirror
- [lucadiliello/bookcorpusopen](https://huggingface.co/datasets/lucadiliello/bookcorpusopen) - "BookCorpusOpen" attempt
- [defunct-datasets/bookcorpusopen](https://huggingface.co/datasets/defunct-datasets/bookcorpusopen) - Marked defunct, taken down

**GitHub**:
- [soskek/bookcorpus](https://github.com/soskek/bookcorpus) - Crawler to reconstruct from Smashwords
- [Shawn Presser's 2020 snapshot](https://battle.shawwn.com/sdb/books1/books1.tar.gz) - 18k text files, ~6GB

**Important**: All these mirrors carry the same copyright and ethical problems as the original. Using them perpetuates the unauthorized distribution of copyrighted works.

## Dataset Quality Issues

Beyond copyright concerns, researchers have identified significant quality problems:

### 1. Duplicate Books
The dataset contains thousands of duplicated books - the same book appears multiple times. This inflates the effective dataset size and can skew model training.

### 2. Genre Bias
Heavy skew toward:
- Romance novels (disproportionately represented)
- Fantasy and science fiction
- Young adult fiction

Underrepresented:
- Non-fiction
- Technical writing
- Academic prose
- Diverse literary styles

### 3. Demographic Bias
Books from Smashwords' "free" category don't represent:
- Professional published literature
- Diverse authorship (selection bias toward who publishes free content)
- Global perspectives (heavily English-speaking, Western-centric)

### 4. Text Quality
Self-published books often lack professional editing, leading to:
- Grammatical errors
- Inconsistent formatting
- Typos and OCR-like errors (even though these were born-digital)

## Ethical and Legal Concerns

### Copyright Infringement
- **Direct violation**: Unauthorized redistribution of copyrighted works
- **Derivative use**: ML models trained on copyrighted data without license
- **Commercial exploitation**: Companies profited from models trained on authors' unpaid labor

### Author Consent
- **No permission sought**: Authors never agreed to have their books used this way
- **No attribution**: Individual authors aren't credited or compensated
- **Loss of control**: Authors lost control over how their creative work was used

### Broader Implications
BooksCorpus exemplifies a larger problem in AI:
- **"Move fast and break things" mentality**: Researchers prioritized convenience over ethics
- **Normalization of copyright violation**: The dataset's popularity made unauthorized use seem acceptable
- **Power imbalance**: Large organizations benefited while individual creators bore the cost
- **Reproducibility crisis**: Models trained on BooksCorpus can't be reproduced now that it's taken down

## Impact on Research

### Positive Impact
- Enabled breakthrough research in NLP (GPT-1, BERT, etc.)
- Demonstrated value of large-scale pre-training on narrative text
- Established benchmarks that pushed the field forward

### Negative Impact
- **Reproducibility**: Research using BooksCorpus can't be fully reproduced
- **Ethical precedent**: Normalized using copyrighted data without permission
- **Legal risk**: Organizations using the dataset face potential liability
- **Community trust**: Damaged trust between AI researchers and creative communities

## Alternatives for Modern Research

The research community has moved toward legally-clear alternatives:

### Recommended Datasets

1. **[Project Gutenberg](https://www.gutenberg.org/)**
   - Public domain books (published before 1928 in US)
   - ~70,000 books freely available
   - HuggingFace: [sedthh/gutenberg_english](https://huggingface.co/datasets/sedthh/gutenberg_english)
   - Legally sound, ethically clear

2. **[Common Crawl](https://commoncrawl.org/)**
   - Web-scraped text at massive scale
   - More diverse than BooksCorpus
   - Used by GPT-3, LLaMA, and modern models
   - Still has some copyright concerns but more defensible (public web content)

3. **Licensed datasets**
   - Obtain proper licenses from publishers
   - Pay for commercial datasets
   - Partner with authors/publishers for research access

4. **Synthetic/generated data**
   - Use existing models to generate training data
   - Avoids copyright issues (though has other concerns)

### What NOT to Use

- **BooksCorpus mirrors**: Still copyright infringement
- **Books3**: Another controversial dataset of 196,640 books, also taken down for copyright violations
- **LibGen/Sci-Hub dumps**: Pirated academic/book content
- **Unauthorized web scrapes**: Just because content is online doesn't mean you can use it

## Lessons Learned

### For Researchers
1. **Seek permission**: Copyright holders must consent to data use
2. **Use licensed data**: Pay for commercial datasets or use public domain sources
3. **Document provenance**: Be transparent about data sources
4. **Consider ethics early**: Don't assume "free to access" = "free to use"

### For the AI Community
1. **Copyright matters in AI**: Training data licensing is not optional
2. **Reproducibility requires legal data**: Science needs datasets that can be shared
3. **Creator consent is essential**: Artists, writers, and creators deserve agency
4. **Industry responsibility**: Companies must ensure legal compliance

### Ongoing Debates
- Is training on copyrighted data "fair use"? (Legal cases pending as of 2025)
- Should creators be compensated for AI training data use?
- How can we balance open research with creator rights?
- What's the path forward for legally-sound, large-scale training data?

## Current Status Summary

- **Official availability**: ❌ NOT AVAILABLE
- **Ethical to use**: ❌ NO (copyright infringement)
- **Legal to use**: ❌ NO (unauthorized distribution)
- **Recommended for new research**: ❌ NO (use alternatives like Project Gutenberg, Common Crawl)
- **Historical significance**: ✅ YES (enabled GPT-1, BERT, and NLP breakthroughs)

## References

- [BooksCorpus - Wikipedia](https://en.wikipedia.org/wiki/BookCorpus)
- [Dirty Secrets of BookCorpus - Medium](https://medium.com/data-science/dirty-secrets-of-bookcorpus-a-key-dataset-in-machine-learning-6ee2927e8650)
- [GitHub - soskek/bookcorpus](https://github.com/soskek/bookcorpus)
- Original paper: Zhu et al., "Aligning Books and Movies: Towards Story-like Visual Explanations by Watching Movies and Reading Books" (2015)
