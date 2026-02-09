# Why GPT-3 Was Never Reproduced (And What Changed)

## Overview

When OpenAI released the GPT-3 paper in June 2020, it provided unprecedented detail about training a 175 billion parameter language model—complete hyperparameter tables, infrastructure specifications, and data composition. Yet despite this transparency, **no external research group successfully reproduced GPT-3 at full 175B scale** in the years immediately following its release.

This wasn't for lack of trying. Multiple well-funded research labs and open-source communities attempted reproduction, but all fell significantly short of the full model size. The closest successful attempts—EleutherAI's GPT-NeoX 20B (2022)—reached only 11% of GPT-3's parameter count.

However, the industry **did eventually match and exceed GPT-3's capabilities**—just not through direct reproduction. DeepMind's **Chinchilla 70B** (March 2022) was the first to definitively beat GPT-3 175B on benchmarks, using only 40% of the parameters by training on 4.7× more data. Google's **PaLM 540B** (April 2022) exceeded GPT-3 at larger scale with better training efficiency. Meta's **LLaMA** (February 2023) became the first transparent, widely accessible model to match GPT-3, with LLaMA-13B achieving GPT-3-175B level performance using only 7.4% of the parameters.

This opacity and the resulting frustration sparked a **transparency movement in AI research**. The community's response—projects like The Pile, LLaMA, and RedPajama—proved that full dataset documentation and reproducible training were not only possible but essential for scientific progress. Today's open model ecosystem exists largely because GPT-3 showed what *not* to do.

## Timeline: Who Beat GPT-3 and When

While GPT-3 was never exactly reproduced, several models **matched or exceeded its capabilities** through better approaches:

| Model | Release Date | Parameters | Key Achievement |
|-------|-------------|------------|-----------------|
| **GPT-3** | June 2020 | 175B | Baseline to beat |
| **Chinchilla** | March 2022 | 70B | **First to beat GPT-3** - proved smaller models + more data works |
| **PaLM** | April 2022 | 540B | Exceeded GPT-3 at larger scale with better efficiency |
| **BLOOM** | July 2022 | 176B | Matched GPT-3 scale with full openness (multilingual) |
| **LLaMA** | February 2023 | 13B-65B | **First transparent model to match GPT-3** - LLaMA-13B matched GPT-3-175B |

**Key insight**: The industry succeeded not by reproducing GPT-3 exactly, but by realizing that **exact reproduction was the wrong goal**. Better training efficiency (Chinchilla scaling) + transparency (LLaMA) beat brute-force parameter scaling.

## The Fundamental Barriers

### Compute Cost

**Training GPT-3 175B required**:

- ~10,000 NVIDIA V100 GPUs
- ~14.8 days of training
- ~3,640 petaflop/s-days of compute (~3.14×10²³ FLOPs)
- Estimated cost: **$500K-$4.6M** (depending on infrastructure and cloud pricing)

**Who could afford this in 2020-2021?**

- Large tech companies: Google, Microsoft, Meta, Amazon
- Well-funded AI labs: OpenAI, DeepMind, Anthropic
- A few research consortia with government funding

**Who couldn't**:

- Academic research labs (typical budgets: $10K-$100K for compute)
- Open-source communities (relying on donations and volunteer compute)
- Most startups (limited runway and investor pressure for ROI)

Even for organizations that *could* afford it, spending millions on a reproduction attempt—without guarantee of success—was a hard sell.

### Infrastructure Requirements

Training 10,000 GPUs simultaneously isn't just expensive—it requires **supercomputer-class infrastructure**:

**Networking**:

- GPT-3 used **400 Gbps networking** between nodes
- Standard cloud instances: 10-25 Gbps (16-40× slower)
- Slow networking creates bottlenecks during gradient synchronization
- Result: training either fails or runs 2-10× slower than expected

**Coordination**:

- 10,000 GPUs must synchronize gradients every training step
- Any failure (GPU crash, network hiccup, OOM error) can halt the entire run
- Requires sophisticated fault-tolerance systems
- OpenAI/Microsoft had this infrastructure; most others didn't

**Power and Cooling**:

- 10,000 V100s draw ~3.2 megawatts at full load
- Requires dedicated datacenter capacity
- Standard cloud regions can't provide this concentration of GPUs

Most organizations attempting reproduction had to settle for 100-1,000 GPUs, forcing them to train much smaller models.

### Data Curation Mystery

The GPT-3 paper disclosed **what datasets** were used but left critical details vague or unstated:

**Common Crawl filtering**:

- Paper: "We filtered Common Crawl using a classifier trained on high-quality reference corpora"
- Not disclosed:
  - What reference corpora? (Books? Wikipedia? News articles?)
  - What classifier architecture? (Transformer? Logistic regression?)
  - What similarity thresholds?
  - Which 41 monthly shards? (Shards vary significantly in quality)

**Books1 and Books2**:

- Paper: "Two internet-based books corpora"
- Not disclosed:
  - **Where did the books come from?** (Avoiding BooksCorpus-style copyright controversy)
  - Why two separate corpora?
  - Why does Books2 (4.6× larger) get undersampled relative to Books1?
  - What quality criteria differentiate them?

**Fuzzy deduplication**:

- Paper: "We used fuzzy deduplication to remove near-duplicates"
- Not disclosed:
  - Algorithm? (MinHash? SimHash? Custom?)
  - Similarity thresholds?
  - How much data was removed?

**The impact**: Without these details, reproduction attempts had to guess at filtering heuristics, leading to different data quality and potentially different model behavior.

### Training Instability at Scale

Training 175B parameters presents challenges that don't occur at smaller scales:

**Loss spikes**:

- Sudden jumps in training loss that can destabilize or derail training
- More frequent at 100B+ parameter scale
- The GPT-3 paper doesn't discuss any loss spikes or how they were handled
- Did they experience spikes? If so, how did they recover?
- What checkpointing strategy did they use?

**Hyperparameter sensitivity**:

- Small changes in learning rate, batch size, or warmup schedule can have outsized effects at 175B scale
- The paper provides final hyperparameters but not how they were tuned
- Did they run smaller-scale ablations? How did settings transfer from smaller to larger models?

**Unknown debugging techniques**:

- When training fails at 175B scale, diagnosis is difficult
- What monitoring did OpenAI use?
- How did they detect and respond to instability?
- These operational details are never documented in papers

**The result**: Even with the published hyperparameters, reproduction attempts faced trial-and-error debugging that wasted compute and often failed.

### Hyperparameter Sensitivity

The paper provides a complete hyperparameter table, but critical context is missing:

**Questions reproduction teams faced**:

- Were these values tuned specifically for 175B, or extrapolated from smaller models?
- How sensitive is performance to small changes? (e.g., does learning rate 0.5e-4 vs 0.6e-4 matter?)
- What's the tuning methodology? (Grid search? Bayesian optimization? Expert intuition?)
- Do these hyperparameters assume specific hardware (V100s)? How do they transfer to A100s or TPUs?

**The problem**: Without understanding the tuning process, reproduction teams couldn't adapt hyperparameters to their different hardware, data, or infrastructure—they had to use GPT-3's values blindly and hope for the best.

### Sparse Attention Details

The [[llm/models/gpt3/architecture|GPT-3 architecture]] uses **alternating dense and locally-banded sparse attention**:

**What the paper says**:

> "We alternated dense and locally banded sparse attention patterns in the layers of the transformer, similar to the Sparse Transformer"

**What the paper doesn't say**:

- Exactly which layers use dense vs sparse attention?
- What is the "band" width for local attention? (How many tokens in the local window?)
- Does the band width change by layer or stay constant?
- How does this affect training dynamics? (Does sparse attention require different initialization or learning rates?)

**The impact**: Reproduction attempts had to either implement their best guess at the sparse attention pattern, or skip it entirely and use dense attention everywhere (increasing memory and compute requirements).

## Reproduction Attempts

Despite the barriers, several research groups attempted to reproduce GPT-3 or train comparable models. Here's what happened:

### EleutherAI: GPT-J 6B and GPT-NeoX 20B

**Who**: A grassroots open-source collective of researchers, engineers, and volunteers

**Goal**: Train open-source GPT-3 equivalents with fully transparent data and code

**Models trained**:

- **GPT-J 6B** (June 2021):
  - 6 billion parameters (3.4% of GPT-3 175B)
  - Trained on [[llm/datasets/the-pile|The Pile]] (800GB, fully documented)
  - 402 GPUs for ~5 weeks
  - Achieved strong performance for its size
  - Fully open-source (weights, code, data)

- **GPT-NeoX 20B** (February 2022):
  - 20 billion parameters (11% of GPT-3 175B)
  - Also trained on The Pile
  - Used Megatron-LM framework for parallelism
  - Best open-source model at the time
  - Performance comparable to GPT-3 13B (which has 65% of NeoX's parameters)

**Why they stopped at 20B**:

- **Compute cost**: Training beyond 20B required infrastructure EleutherAI couldn't afford
- **Diminishing returns**: Chinchilla paper (2022) showed that training smaller models on more data was more efficient than scaling parameters
- **Mission accomplished**: Proved that open, reproducible training was possible

**Key innovation**: [[llm/datasets/the-pile|The Pile]]—a fully documented, high-quality 800GB dataset assembled from 22 sources. This solved the "Books1/Books2 mystery" by using only publicly documented data sources.

**Impact**: EleutherAI demonstrated that transparency was feasible and valuable. Their work directly inspired later projects like LLaMA and RedPajama.

### BigScience: BLOOM 176B

**Who**: A collaborative research project involving 1,000+ researchers from 70+ countries, coordinated by Hugging Face

**Goal**: Train a fully open, multilingual model comparable to GPT-3

**Model**:

- **BLOOM 176B** (July 2022):
  - 176 billion parameters (slightly larger than GPT-3 175B)
  - Trained on 366B tokens from the ROOTS corpus
  - 384 NVIDIA A100 GPUs for ~4 months
  - **Multilingual**: 46 natural languages + 13 programming languages
  - Fully open-source (weights, code, data, training process)

**Why this counts as a "reproduction"**:

While BLOOM differs from GPT-3 in several ways (multilingual, different architecture choices, more training tokens), it proved that training a 175B+ parameter model was feasible for the research community with sufficient coordination.

**Key differences from GPT-3**:

- Different data (ROOTS, not Common Crawl + Books)
- Multilingual (not English-only)
- Different architecture (ALiBi positional embeddings instead of learned embeddings)
- Trained longer (366B tokens vs 300B)

**Impact**: Showed that with enough coordination and resources, the open research community could match GPT-3's scale. However, it required massive international collaboration and significant funding.

### Google: LaMDA, PaLM, Gemini

**Who**: Google Brain / DeepMind

**Models**:

- **LaMDA 137B** (May 2021): Dialogue-focused model, not a direct GPT-3 replication
- **PaLM 540B** (April 2022): 540B parameters, significantly larger than GPT-3, with 57.8% FLOPs utilization
- **Gemini** (2023+): Next-generation models

**Why these aren't "reproductions"**:

Google wasn't trying to reproduce GPT-3—they were building better models using newer techniques. PaLM, in particular, demonstrated that GPT-3's training was inefficient:

- Better parallelism strategies
- Advanced stability techniques (see [[llm/training-techniques/training-stability|training-stability.md]])
- Higher hardware utilization (57.8% vs GPT-3's estimated ~30-40%)
- Better performance per parameter

**Impact**: Proved that GPT-3's approach was not optimal. With better training techniques, you could achieve better results with the same compute budget.

### Meta: OPT 175B and LLaMA

**OPT 175B** (May 2022):

- Meta's first attempt at reproducing GPT-3 scale
- 175 billion parameters (exact match)
- Trained on a mix of datasets, partially documented
- Released with limited openness (model weights and logbooks, but not full training code or data)

**LLaMA** (February 2023):

- **Not a reproduction**—intentionally went a different direction
- Models: 7B, 13B, 33B, 65B (all smaller than GPT-3 175B)
- Trained on **1.4 trillion tokens** (4.7× more data than GPT-3)
- Key insight: Following Chinchilla's findings, smaller models trained on more data outperform larger models trained on less data
- **Fully documented dataset sources**: No "Books1/Books2" mystery—every source disclosed
- **Performance**: LLaMA 13B matched or exceeded GPT-3 175B on many benchmarks despite having 7.4% of the parameters

**Why LLaMA matters more than OPT**:

OPT proved Meta *could* train a 175B model, but LLaMA proved you *didn't need to*. By training smaller, longer, and transparently, Meta set a new standard for the field.

### Other Attempts

**Tsinghua University: GLM 130B** (October 2022):

- 130B parameters
- Trained on 400B tokens
- Bilingual (English + Chinese)
- Different architecture (GLM uses bidirectional attention with autoregressive generation)

**Yandex: YaLM 100B** (June 2022):

- 100B parameters
- English + Russian
- Released with partial documentation

**AI21 Labs: Jurassic-1 178B** (2021):

- Commercial model, not fully open
- Limited technical details released

## The "Secret Sauce" Problem

Even with extensive documentation, GPT-3 likely used undocumented techniques discovered through experience:

**Undocumented tricks likely employed**:

**Common Crawl filtering heuristics**:

- Specific rules for detecting high-quality documents
- Custom text cleaning pipelines (removing boilerplate, ads, navigation)
- Domain blacklists/whitelists refined over time
- These heuristics come from trial and error, not first principles

**Checkpoint selection during loss spikes**:

- When a loss spike occurs, which checkpoint do you roll back to?
- Do you adjust hyperparameters after rollback?
- How do you detect spikes in real-time?

**Hyperparameter adjustments mid-training**:

- Did they keep learning rate constant, or adjust it based on training dynamics?
- Did they modify batch size during training?
- These operational decisions rarely appear in papers

**Data mixing ratios from experiments**:

- The 60/22/8/8/3 split was presented as final, but:
- How many alternative splits were tested?
- What guided the choice? (Perplexity on a validation set? Downstream task performance?)

**Infrastructure optimizations**:

- Custom kernel implementations for attention, FFN, embedding layers
- Gradient compression techniques to reduce communication overhead
- Memory optimization tricks (activation checkpointing, mixed precision strategies)

**Quote from frustrated researchers**: *"The paper gives the recipe, but not the cooking technique."*

## Industry Impact: The Transparency Movement

GPT-3's opacity—despite its detailed paper—frustrated the research community and catalyzed a major shift in AI research culture.

### The Frustration

**Before GPT-3** (GPT-1, GPT-2, BERT):

- Research community accepted that some details would be proprietary
- Papers provided directional guidance, not full reproduction recipes
- Limited expectations for openness

**After GPT-3**:

- The paper's extensive detail *raised expectations* for full transparency
- Providing dataset names without sources felt deliberately obfuscatory
- "Books1" and "Books2" became symbols of corporate secrecy
- Researchers felt that AI progress was being gatekept by a few organizations

**Key quote** from the community: *"If you're going to tell us what you used, tell us where to get it. Otherwise, what's the point?"*

### The Response: Open Replication Era (2021-2023)

The community's answer was to build **fully transparent alternatives** to GPT-3's training data:

**EleutherAI's [[llm/datasets/the-pile|The Pile]]** (December 2020):

- 800GB, fully documented dataset from 22 sources
- Every source disclosed, with URLs and access methods
- Explicit philosophy: "No mystery datasets"
- Became the standard training corpus for open models (GPT-J, GPT-NeoX, BLOOM partially)

**RedPajama** (April 2023):

- 1.2 trillion tokens, fully open reproduction of LLaMA's training data
- Documented processing pipelines for each data source
- Proved that high-quality, trillion-token datasets could be fully transparent

**BigScience ROOTS** (2022):

- 1.6TB multilingual dataset for BLOOM
- Full documentation of collection, filtering, and licensing
- Included data governance frameworks and ethical considerations

For detailed coverage of these projects and the broader movement, see [[llm/data-processing/open-replication-era|The Open Replication Era]].

### The New Standard

By 2023, the transparency movement had succeeded in shifting industry norms:

**What became expected**:

- Full dataset documentation with sources
- Reproducible data processing pipelines
- Open training code (at least for research models)
- Training run transparency (loss curves, compute used, challenges faced)

**Models that set this standard**:

- **LLaMA** (2023): Fully documented data sources, no "Books1/Books2" mystery
- **BLOOM** (2022): Open training process with detailed logs
- **Mistral** (2023+): Open weights and transparent architecture
- **Llama 2** (2023): Even more open than LLaMA 1, including fine-tuning details

**GPT-3's legacy**: By being *partially* transparent, GPT-3 inadvertently showed the research community what full transparency should look like—and motivated them to demand it.

## How Later Models Succeeded

While GPT-3 was never directly reproduced, later models **matched or exceeded its capabilities** through different approaches. Here's what changed:

### Chinchilla (2022, DeepMind): The First to Beat GPT-3

**Released**: March 2022

**Key finding**: GPT-3 was **undertrained** relative to its parameter count.

**Optimal scaling law** (Chinchilla paper):

For a fixed compute budget, you should train with:

- **20 tokens per parameter** (not GPT-3's 1.7 tokens per parameter)

**Example**:

- GPT-3 175B: 175B params × 1.7 = 300B tokens
- Chinchilla-optimal: 70B params × 20 = 1.4T tokens

**Result**: Chinchilla 70B (trained on 1.4T tokens) **uniformly and significantly outperformed GPT-3 175B** on a large range of downstream evaluation tasks despite having only 40% of the parameters.

**Benchmark performance**:

- 67.5% on MMLU benchmark (7% improvement over Gopher 280B, and better than GPT-3)
- State-of-the-art results across most benchmarks tested

**Why this was the breakthrough**: Chinchilla was **the first model to definitively demonstrate** that you could beat GPT-3 175B with a much smaller model by training on more data. This validated the hypothesis that GPT-3 was undertrained and fundamentally changed the industry's approach to scaling.

**Impact**: This fundamentally changed how the industry thought about scaling. Instead of "bigger models," the focus shifted to "smaller models trained longer on more data."

### LLaMA (2023, Meta): First Transparent Model to Match GPT-3

**Released**: February 2023 (11 months after Chinchilla, 10 months after PaLM)

**What made LLaMA special**: While Chinchilla and PaLM proved that GPT-3-level (or better) performance was achievable, they were closed models from large corporations. **LLaMA was the first widely accessible model with full transparency** to match GPT-3's capabilities.

**What LLaMA did differently**:

1. **Followed Chinchilla's insight**: Train smaller models on more data
   - LLaMA 65B: trained on 1.4T tokens (20 tokens/param)
   - LLaMA 13B: trained on 1T tokens (77 tokens/param)

2. **Fully documented data sources**:
   - CommonCrawl (specific dumps and filtering documented)
   - C4 (publicly available)
   - GitHub (public repositories)
   - Wikipedia (dump dates specified)
   - Books (Gutenberg, Books3 from The Pile)
   - ArXiv papers
   - StackExchange

   **No mystery datasets**—every source was disclosed with access methods.

3. **Efficient training**:
   - Used modern techniques (better parallelism, stability methods)
   - Trained on 2,048 A100 GPUs (more efficient than V100s)

**Performance**:

- **LLaMA 13B** matched or exceeded GPT-3 175B on most benchmarks
- **LLaMA 65B** significantly outperformed GPT-3 175B

**Cost comparison**:

- GPT-3 175B: ~$500K-$4.6M
- LLaMA 65B: Estimated ~$2-3M (similar cost, better performance)
- LLaMA 13B: Estimated ~$500K (much cheaper, similar performance)

**Impact**: LLaMA proved that:

- Transparency didn't sacrifice competitiveness
- Chinchilla's scaling laws held in practice
- Smaller models trained longer were more efficient than large undertrained models

### PaLM (2022, Google): Exceeding GPT-3 at Larger Scale

**Released**: April 2022 (one month after Chinchilla)

**What PaLM proved**: GPT-3's training was **inefficient**, and better engineering could achieve superior results.

**Model**: 540 billion parameters (3× larger than GPT-3 175B)

**PaLM improvements**:

1. **Better parallelism**: Custom TPU v4 pods with optimized communication
2. **Advanced stability techniques**: See [[llm/training-techniques/training-stability|training-stability.md]]
3. **Higher utilization**: 57.8% FLOPs utilization (vs GPT-3's estimated 30-40%)

**Performance**: PaLM 540B **outperformed GPT-3 on 28 of 29 benchmarks** including:

- 58% on GSM8K math reasoning (vs GPT-3's 55% achieved with fine-tuning + calculator)
- State-of-the-art on BIG-Bench tasks
- Superior few-shot learning across NLP tasks

**Why this matters**: Even without reproducing GPT-3 exactly, Google showed that better engineering could achieve superior results. PaLM used roughly 10× more compute than GPT-3 but achieved much better efficiency and performance.

### The Key Insight: You Don't Need to Reproduce GPT-3

By 2023, the industry realized:

**Reproducing GPT-3 exactly is the wrong goal.**

Instead:

- Train smaller models on more data (Chinchilla scaling)
- Use transparent, high-quality datasets (Pile, RedPajama)
- Apply modern training techniques (sequence length warmup, BF16, better parallelism)
- Open-source everything (weights, data, code)

**Result**: Models like LLaMA 13B achieve GPT-3-level performance with:

- 7.4% of the parameters (13B vs 175B)
- Fully documented data
- Open weights and code
- Lower training cost

## Modern Training Practices (2023+)

Today's state-of-the-art training has moved far beyond GPT-3's approach:

### Fully Documented Datasets

**Standard practice**:

- Disclose all data sources with access methods
- Document filtering pipelines with code and thresholds
- Provide dataset statistics and composition
- Address copyright and licensing explicitly

**Examples**:

- LLaMA / Llama 2: Every source documented
- Mistral: Training data composition disclosed
- RedPajama: Fully reproducible pipeline from raw sources

**No more "Books1" situations**: Mystery datasets are no longer acceptable in research.

### Train on Trillions of Tokens

**Chinchilla scaling in practice**:

| Model | Parameters | Training Tokens | Tokens per Param |
|-------|-----------|-----------------|------------------|
| GPT-3 | 175B | 300B | 1.7 |
| LLaMA | 65B | 1.4T | 21.5 |
| LLaMA 2 | 70B | 2T | 28.6 |
| Mistral 7B | 7B | Undisclosed (estimated ~1T+) | ~140+ |

**The pattern**: Modern models train far longer relative to their size than GPT-3 did.

### Better Efficiency Techniques

**Standard toolkit**:

- **Sequence length warmup**: Start with short sequences, gradually increase
- **BF16 precision**: Larger dynamic range prevents overflow
- **FlashAttention**: Memory-efficient attention implementation (2-4× speedup)
- **Optimized parallelism**: Tensor parallelism + pipeline parallelism + data parallelism
- **Automatic mixed precision**: Dynamic loss scaling for stability

**Result**: Modern training runs are 2-5× more efficient than GPT-3 era for the same model size.

### Open Model Releases

**The new standard** (established by LLaMA, Mistral, BLOOM):

- Release model weights publicly
- Document architecture completely
- Provide inference code and evaluation scripts
- Disclose training process and challenges
- Specify licensing clearly

**Impact**: This openness accelerates research by letting the community build on each model's innovations.

## Key Takeaways

### Why Reproductions Failed

1. **Compute cost**: $4-12M limited reproduction to a few organizations
2. **Infrastructure gap**: Most groups lacked 400 Gbps networking and 10,000-GPU orchestration
3. **Data mystery**: "Books1/Books2" and vague Common Crawl filtering details prevented exact replication
4. **Training expertise**: Undocumented stability handling and hyperparameter tuning knowledge
5. **Wrong goal**: By the time groups had resources to attempt it, Chinchilla showed that exact reproduction wasn't the right target

### How the Industry Evolved

1. **Chinchilla breakthrough (March 2022)**: First model to beat GPT-3, proved smaller models + more data > larger undertrained models
2. **PaLM advancement (April 2022)**: Exceeded GPT-3 at larger scale with 57.8% FLOPs utilization, proved better engineering matters
3. **Transparency movement (2021-2023)**: Community demanded and built fully documented alternatives (The Pile, BLOOM, RedPajama)
4. **LLaMA democratization (February 2023)**: First transparent model to match GPT-3, made Chinchilla scaling accessible
5. **Better training techniques**: Sequence length warmup, BF16, FlashAttention improved efficiency 2-5×
6. **New standards (2023+)**: Full dataset documentation and open weights became expected, not exceptional

### The Lasting Impact on AI Research Culture

**Before GPT-3**:

- Proprietary data and models were accepted
- Partial transparency was sufficient
- Secrecy was expected from industry labs

**After GPT-3**:

- Full transparency became the community expectation
- Mystery datasets ("Books1") seen as anti-scientific
- Open models (weights + data + code) became competitive
- Research culture shifted toward reproducibility

**GPT-3's paradox**: By being *partially* transparent, it raised expectations for *full* transparency. The frustration it caused ultimately accelerated the shift to open AI research.

For technical details on GPT-3's training, see [[llm/models/gpt3/training|training.md]]. For the stability challenges that complicated reproduction, see [[llm/training-techniques/training-stability|training-stability.md]]. For how the community responded with open datasets, see [[llm/data-processing/open-replication-era|open-replication-era.md]].
