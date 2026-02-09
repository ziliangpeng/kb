# GPT-3 Training

Paper: ["Language Models are Few-Shot Learners"](paper.pdf) (Brown et al., 2020)

## Training Hyperparameters

The GPT-3 paper provided a complete table of training hyperparameters for all 8 model sizes:

| Model | Parameters | Layers | d_model | Batch Size | Learning Rate |
|---|---|---|---|---|---|
| GPT-3 Small | 125M | 12 | 768 | 0.5M tokens | 6.0e-4 |
| GPT-3 Medium | 350M | 24 | 1,024 | 0.5M tokens | 3.0e-4 |
| GPT-3 Large | 760M | 24 | 1,536 | 0.5M tokens | 2.5e-4 |
| GPT-3 XL | 1.3B | 24 | 2,048 | 1M tokens | 2.0e-4 |
| GPT-3 2.7B | 2.7B | 32 | 2,560 | 1M tokens | 1.6e-4 |
| GPT-3 6.7B | 6.7B | 32 | 4,096 | 2M tokens | 1.2e-4 |
| GPT-3 13B | 13.0B | 40 | 5,140 | 2M tokens | 1.0e-4 |
| GPT-3 175B | 175.0B | 96 | 12,288 | 3.2M tokens | 0.6e-4 |

**Key observation**: As model size increases, learning rate decreases and batch size increases. The largest model (175B) uses a learning rate roughly 10× smaller than the smallest (125M).

### Optimizer

**Adam** with the following parameters:

- β₁ = 0.9
- β₂ = 0.95
- ε = 10⁻⁸

This is slightly different from standard Adam (β₂ = 0.999). Using β₂ = 0.95 means the running average of squared gradients decays faster, making the optimizer respond more quickly to recent gradient changes.

### Learning Rate Schedule

**Warmup + Cosine Decay**:

1. **Warmup phase**: Linear increase from 0 to max learning rate over the first **375 million tokens**
2. **Cosine decay phase**: After warmup, learning rate follows cosine decay down to **10% of its maximum value** over tokens 260B → 300B
3. **Final plateau**: Learning rate stays at 10% for the last portion of training

The paper notes that learning rate was decayed "approximately" to 10% during training on 260B-300B tokens, suggesting some flexibility in the exact schedule.

### Gradient Clipping

**Global norm clipping at 1.0**: If the global norm of all gradients exceeds 1.0, scale all gradients down proportionally. This prevents destabilizing gradient spikes during training.

### Weight Decay

**0.1** applied to all weights to prevent overfitting.

### Context Length

**2,048 tokens** for all models (doubled from GPT-2's 1,024).

## Training Data

GPT-3 was trained on **300 billion tokens** from a weighted mixture of five datasets:

| Dataset | Training Weight | Epochs Seen |
|---------|-----------------|-------------|
| Common Crawl (filtered) | 60% | 0.44 |
| WebText2 | 22% | 2.9 |
| Books1 | 8% | 1.9 |
| Books2 | 8% | 0.43 |
| Wikipedia | 3% | 3.4 |

The key insight: high-quality datasets (WebText2, Wikipedia) are deliberately oversampled even though it causes the model to see them multiple times. The paper explicitly states this trade-off: *"This essentially accepts a small amount of overfitting in exchange for higher quality training data."*

For full details on data composition, filtering, and the transparency challenges this created, see [[llm/models/gpt3/training-data|training-data.md]].

## Training Infrastructure

**Hardware**:

- **10,000 NVIDIA V100 GPUs** (32GB each)
- Hosted on **Microsoft Azure** supercomputing infrastructure
- **285,000+ CPU cores**
- **400 Gbps networking** between nodes

**Training Duration**:

- Approximately **14.8 days** for the 175B model
- Total compute: **~3,640 petaflop/s-days** (~3.14×10²³ FLOPs)

**Cost Estimates**:

The paper doesn't disclose the actual cost, but external estimates range from:

- **Lower bound**: ~$500K (assuming deeply discounted Azure rates for Microsoft partnership)
- **Upper bound**: ~$4.6M (using standard Azure cloud pricing for V100 instances)

The true cost is likely somewhere in the middle, accounting for infrastructure overhead, power, cooling, and engineering time.

## Parallelism Strategy

Training a 175B parameter model on 10,000 GPUs requires sophisticated parallelism. GPT-3 used a **hybrid approach**:

**Model Parallelism (Tensor Parallelism)**:

- Split individual layers across multiple GPUs
- Each GPU computes a portion of each matrix multiplication
- Required because the model is too large to fit on a single GPU (175B parameters × 4 bytes ≈ 700GB, far exceeding V100's 32GB memory)

**Data Parallelism**:

- Different GPUs process different batches of data
- Gradients are averaged across all data-parallel replicas

The paper doesn't provide implementation details, but this approach likely resembles the strategy used in [[llm/training-frameworks/megatron|Megatron-LM]], which was developed by NVIDIA around the same time for training large transformer models.

## Training Stability

Large-scale training at 175B parameters presents significant stability challenges. GPT-3 used several techniques to maintain stable training:

**Techniques employed**:

- **Gradient clipping** (global norm = 1.0): Prevents gradient explosions
- **Learning rate warmup** (375M tokens): Gradual learning rate increase prevents early instability
- **Cosine decay**: Smooth learning rate reduction toward the end of training
- **Weight decay** (0.1): Regularization to prevent overfitting

These represent the "conservative" stability techniques available in 2020. The paper doesn't discuss any advanced techniques like sequence length warmup or special handling of loss spikes.

For a comprehensive overview of training stability techniques (including post-GPT-3 innovations), see [[llm/training-techniques/training-stability|training-stability.md]].

## Reproduction Challenges

Despite the paper's level of detail, GPT-3 was **never successfully reproduced at full 175B scale** by any external research group. The closest attempts (GPT-J 6B, GPT-NeoX 20B) fell far short of the full model size.

However, the industry did eventually match and exceed GPT-3's capabilities through different approaches:

- **Chinchilla 70B** (March 2022): First model to beat GPT-3 using only 40% of the parameters
- **PaLM 540B** (April 2022): Exceeded GPT-3 at larger scale with better efficiency
- **LLaMA 13B** (February 2023): First transparent model to match GPT-3 with only 7.4% of the parameters

**Why direct reproduction failed**:

- Compute cost ($4-12M) limited to well-funded organizations
- Missing implementation details (exact Common Crawl filtering, Books1/Books2 sources)
- Training instability at 175B scale requires undocumented expertise
- No checkpoints or validation curves to know if reproduction is on track

This opacity frustrated the research community and sparked a transparency movement. For the complete timeline of which models beat GPT-3 and how, see [[llm/training-techniques/gpt3-reproduction-challenges#Timeline: Who Beat GPT-3 and When|gpt3-reproduction-challenges.md]].

## Comparison to GPT-2 Training

| Aspect | GPT-2 | GPT-3 |
|---|---|---|
| **Largest model** | 1.5B parameters | 175B parameters (117× larger) |
| **Training tokens** | ~10B (WebText) | 300B (30× more) |
| **Context length** | 1,024 | 2,048 |
| **Batch size** | 0.5M tokens (all sizes) | 0.5M → 3.2M (scales with model) |
| **Learning rate** | Not disclosed | 6.0e-4 → 0.6e-4 (decreases with size) |
| **Hardware** | 256 TPU v3 cores | 10,000 V100 GPUs |
| **Compute** | Unknown | ~3,640 petaflop/s-days |
| **Cost** | Unknown | ~$500K-$4.6M (estimated) |
| **Data sources** | 1 (WebText) | 5 (weighted mixture) |
| **Training details disclosed** | Minimal | Extensive (but still gaps) |

The key difference: GPT-3 provided far more training details than GPT-2, including complete hyperparameter tables and infrastructure specifications. However, critical implementation details (data filtering, training stability handling) remained undisclosed.

## Key Takeaways

1. **Scale requires care**: Larger models need smaller learning rates and larger batch sizes
2. **Conservative stability**: Gradient clipping + warmup + decay were sufficient for GPT-3 (2020), but later models developed more advanced techniques
3. **Quality over quantity**: Deliberately oversample high-quality data even if it means overfitting
4. **Compute is expensive**: 10,000 GPUs for 2 weeks costs millions of dollars
5. **Opacity has consequences**: Despite extensive documentation, missing details prevented successful reproduction and frustrated researchers

For architectural details, see [[llm/models/gpt3/architecture|architecture.md]]. For data composition and the transparency issues it created, see [[llm/models/gpt3/training-data|training-data.md]].
