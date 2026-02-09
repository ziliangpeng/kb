# Training Stability for Large Language Models

## Overview

Training stability becomes a critical challenge as language models scale beyond 100 billion parameters. A single loss spike—a sudden, dramatic increase in training loss—can waste days of compute on thousands of GPUs, costing hundreds of thousands of dollars. In extreme cases, a severe spike can destabilize training permanently, forcing a restart from an earlier checkpoint or even abandoning the run entirely.

The cost of instability scales with model size. For GPT-3 175B (2020), a training run required ~10,000 V100 GPUs for ~15 days at an estimated cost of $500K-$4.6M. For PaLM 540B (2022), even with advanced stability techniques, Google reported experiencing **~20 loss spikes** during training despite extensive precautions. Each spike risks data loss, requires manual intervention, and potentially wastes millions of dollars in compute.

The field has evolved significantly from GPT-3's conservative 2020 techniques to modern practices that address root causes rather than just symptoms. The difference: GPT-3 used gradient clipping and warmup to *prevent catastrophic failures*, while modern techniques like sequence length warmup and better floating-point precision actually *eliminate the conditions that cause spikes*.

## The Problem: Loss Spikes

**Loss spikes** are sudden, sharp increases in training loss that occur during pre-training. A typical pattern:

1. Loss decreases smoothly for hours or days
2. Suddenly, loss jumps by 2-10× in a single step
3. Training either recovers gradually or becomes permanently unstable

**Example from PaLM 540B (2022)**:

The PaLM paper explicitly documents loss spike behavior:

> "Despite the precautions taken [...] we observed approximately 20 loss spikes during training where the loss spiked significantly and then recovered."

These spikes occurred despite using state-of-the-art stability techniques, highlighting how challenging stability becomes at 500B+ parameter scale. The paper includes a training loss curve showing multiple visible spikes where loss suddenly jumped upward before recovering over subsequent steps.

**When spikes occur**:

- Almost always at **very large scale** (100B+ parameters)
- More frequent with **aggressive training settings** (large batches, high learning rates)
- Often triggered by **outlier batches** (unusually long sequences, rare tokens, numerical edge cases)

**Impact**:

- Wasted compute: training can't continue until spike is detected and addressed
- Manual intervention: requires engineers to monitor, diagnose, and potentially roll back
- Lost progress: may need to reload from checkpoint hours or days earlier
- In worst cases: entire training run becomes unstable and must be abandoned

## Root Causes

### Extreme Gradient Variance

At 100B+ parameters, small numerical errors compound across billions of operations. A single unusual batch (e.g., a sequence with rare tokens or extreme values) can produce gradients orders of magnitude larger than typical batches. Without intervention, these large gradients cause chaotic weight updates that destabilize training.

### Long Sequences Early in Training

Training on very long sequences (e.g., 2,048 or 4,096 tokens) from the start creates numerical challenges:

- More tokens per sequence = more operations per forward pass
- Larger intermediate activations to store
- Higher memory pressure leads to precision issues
- Early in training, when weights are poorly initialized, long sequences amplify instability

### Large Batch Sizes + Large Learning Rates

The tension between efficiency and stability:

- **Large batches** are computationally efficient (better GPU utilization, fewer gradient synchronization steps)
- **Large learning rates** speed up convergence
- But combining them creates instability: large gradients × large learning rates = chaotic weight updates

Training at scale requires pushing both as high as possible, but this increases spike risk.

### Numerical Precision Issues

**Float16 (FP16)** has a narrow dynamic range:

- Can represent values from ~6×10⁻⁸ to ~65,000
- Intermediate activations or gradients outside this range cause **overflow** (become infinity) or **underflow** (become zero)
- Large models have billions of operations—even rare overflow events accumulate

When intermediate values overflow, gradients become NaN (not a number), propagating through the network and destroying training.

## Basic Techniques (GPT-3 Era)

These are the "standard" techniques used by GPT-3 (2020) and most models from that era. They prevent catastrophic failures but don't eliminate spikes entirely.

### Gradient Clipping

**How it works**:

Compute the global L2 norm of all gradients across all parameters:

```
global_norm = sqrt(sum(grad²) for all parameters)
```

If `global_norm > threshold`, scale all gradients down proportionally:

```
grad = grad * (threshold / global_norm)
```

**Typical values**: Threshold = 1.0 (GPT-3, most models)

**Why it helps**: Prevents any single batch from causing extreme weight updates. Even if an outlier batch produces huge gradients, they're clamped to a safe range.

**Limitation**: This treats the symptom, not the cause. Clipping prevents disaster but doesn't stop spikes from occurring—it just limits their damage.

### Learning Rate Warmup

**How it works**:

Start training with learning rate = 0, then linearly increase to the target learning rate over N tokens or steps.

**Typical warmup schedules**:

- GPT-3: 375 million tokens
- Common alternative: 1,000-10,000 steps

**Why it helps**:

Early in training, weights are randomly initialized and gradients are highly variable. Starting with a high learning rate immediately can cause chaotic updates. Warmup gives the model time to "settle" into a reasonable region of parameter space before making large updates.

**Analogy**: Like accelerating a car gradually rather than flooring the gas pedal from a standstill.

### Cosine Decay vs Linear Decay

After warmup, gradually reduce the learning rate over the course of training.

**Cosine decay** (used by GPT-3):

```
lr = min_lr + 0.5 * (max_lr - min_lr) * (1 + cos(π * t / T))
```

- Smooth, gradual reduction
- Faster decay in the middle of training, slower at the end
- Generally preferred for large models

**Linear decay**:

```
lr = max_lr - (max_lr - min_lr) * (t / T)
```

- Constant rate of reduction
- Simpler but less smooth

**Why it helps**: Lower learning rates toward the end of training allow the model to fine-tune without overshooting good solutions.

### Weight Decay Regularization

**How it works**:

Add a penalty term to the loss function proportional to the L2 norm of weights:

```
loss_total = loss_data + λ * ||weights||²
```

**Typical values**: λ = 0.1 (GPT-3)

**Why it helps**: Prevents weights from growing unboundedly, which can lead to numerical instability. Keeps parameters in a reasonable range.

### Conservative Learning Rates for Larger Models

**The pattern** (from GPT-3):

| Model Size | Learning Rate |
|------------|---------------|
| 125M | 6.0e-4 |
| 1.3B | 2.0e-4 |
| 13B | 1.0e-4 |
| 175B | 0.6e-4 |

As model size increases 1,000×, learning rate decreases ~10×.

**Why it helps**: Larger models have more parameters, so each gradient update affects more of the network. Smaller learning rates compensate for this increased impact.

### Assessment: Basic Techniques

**What they achieve**:

- Prevent catastrophic training failures (total loss of progress)
- Allow training to complete successfully most of the time
- Sufficient for models up to ~100B parameters with conservative settings

**What they don't achieve**:

- Eliminate loss spikes (PaLM 540B still had ~20 spikes despite using all these techniques)
- Enable aggressive training settings (large batches + high learning rates)
- Address root causes (they manage symptoms instead)

## Advanced Techniques (Post-GPT-3)

These techniques, developed after GPT-3, attack the root causes of instability rather than just managing symptoms.

### Sequence Length Warmup (SLW)

**The key innovation**: Start training with short sequences, gradually increase to full length over the first portion of training.

**Example schedule**:

- Tokens 0-10B: 512-token sequences
- Tokens 10B-20B: 1,024-token sequences
- Tokens 20B-30B: 2,048-token sequences
- Tokens 30B onward: 4,096-token sequences (full length)

**Why it works**:

This addresses a root cause of instability: long sequences early in training when weights are poorly initialized. By starting with short sequences:

- Reduced memory pressure (fewer activations to store)
- Smaller numerical errors (fewer operations to compound)
- More stable gradients in the critical early phase
- Model learns basic patterns before facing full complexity

**Benefits**:

- Enables **8× larger batch sizes** (proven in research)
- Enables **4-40× larger learning rates** (depending on model size)
- Faster training (larger batches + higher learning rates = fewer steps to convergence)
- Fewer loss spikes

**Trade-off**: Early training on short sequences means the model initially sees less long-range context. But research shows the benefits far outweigh this temporary limitation.

**Adoption**: Sequence length warmup has become standard practice for training large models post-2022.

### Better Floating-Point Precision: bfloat16 vs float16

**The problem with float16** (FP16):

- Dynamic range: ~6×10⁻⁸ to ~65,000
- Narrow range causes frequent overflow/underflow
- Requires careful loss scaling to avoid gradient underflow

**bfloat16** (BF16):

- Same exponent range as float32 (FP32)
- Dynamic range: ~10⁻³⁸ to ~10³⁸
- Much larger range prevents most overflow/underflow issues
- Trades mantissa precision for range (8 bits mantissa vs 10 bits in FP16)

**Why it helps**:

For LLM training, **range matters more than mantissa precision**. Rare overflow events cause NaN gradients that destroy training. BF16's larger range prevents these events while maintaining training speed and memory benefits of 16-bit formats.

**Hardware support**:

- Google TPUs: Native BF16 support since TPU v2
- NVIDIA: A100 and newer GPUs support BF16
- Older hardware (V100): Only supports FP16, not BF16

**Adoption**: Most modern large models (PaLM, LLaMA, GPT-4 likely) use BF16 instead of FP16 for base precision.

### Architecture Modifications (PaLM Approach)

The PaLM 540B paper (2022) documented several architectural changes specifically for stability:

**Modified Optimizer: Adafactor**:

- Alternative to Adam with better memory efficiency
- More conservative gradient updates
- Lower risk of instability at extreme scale

**Scaled Pre-Softmax Logits**:

- Before applying softmax in attention, scale logits down by a constant factor
- Prevents logits from growing too large (which causes overflow)
- Simple change with significant stability impact

**Auxiliary Losses**:

- Additional loss terms beyond the main language modeling objective
- Help regularize training and provide gradient signal stability

**No Dropout During Pre-Training**:

- Dropout (randomly zeroing activations) can increase gradient variance
- Removing it during pre-training improves stability
- Can still use dropout during fine-tuning if needed

**Result**: Despite PaLM 540B having ~3× more parameters than GPT-3 175B, it achieved **57.8% FLOPs utilization** (extremely high efficiency) and successfully completed training, though still experiencing ~20 loss spikes.

### Checkpoint Strategies

**Frequent Checkpointing**:

- Save model state every N steps (e.g., every 1,000 steps or every hour)
- Enables rolling back to before a loss spike
- Cost: storage overhead (checkpoints are large), I/O overhead (saving takes time)

**Automatic Spike Detection and Rollback**:

- Monitor training loss in real-time
- If loss increases by more than X% in a single step, automatically:
  1. Halt training
  2. Reload from last stable checkpoint
  3. Resume training (potentially with adjusted hyperparameters)

- Reduces manual intervention and wasted compute
- Requires robust detection heuristics (avoid false positives)

**Trade-off**: More frequent checkpoints = more storage and I/O cost, but less wasted compute if spike occurs.

## Evolution Timeline

### GPT-3 Era (2020)

**Conservative techniques**:

- Gradient clipping (1.0)
- Learning rate warmup (375M tokens)
- Cosine decay to 10% of max LR
- Weight decay (0.1)
- Smaller learning rates for larger models

**Result**: Successful training of 175B model, but likely experienced spikes (not documented in paper).

**Note**: While GPT-3 was never directly reproduced, later models matched or exceeded its capabilities using improved stability techniques. See [[llm/training-techniques/gpt3-reproduction-challenges#Timeline: Who Beat GPT-3 and When|the timeline]] for how Chinchilla (March 2022), PaLM (April 2022), and LLaMA (February 2023) succeeded where reproduction attempts failed.

### PaLM Era (2022)

**Advanced stability techniques**:

- All GPT-3 techniques plus:
- Adafactor optimizer
- Scaled pre-softmax logits
- Auxiliary losses
- No dropout during pre-training
- Likely sequence length warmup (not explicitly confirmed)
- BF16 precision (trained on TPU v4)

**Result**: Successfully trained 540B model with 57.8% FLOPs utilization, but still experienced ~20 loss spikes.

### Modern Practices (2023+)

**Standard approach**:

- Sequence length warmup (now widely adopted)
- BF16 as default precision on supported hardware
- Large batch sizes + high learning rates (enabled by SLW)
- Automatic spike detection and rollback
- Frequent checkpointing with robust storage systems

**Result**: Training runs complete more reliably, faster (higher throughput), and with fewer manual interventions.

**Impact on GPT-3-level models**: These modern techniques enabled models like LLaMA (2023) to match GPT-3's capabilities with far fewer parameters and more stable training. See [[llm/training-techniques/gpt3-reproduction-challenges#How Later Models Succeeded|how later models succeeded]] for details.

## Key Takeaways

1. **Stability is expensive**: Loss spikes at large scale can waste millions of dollars in compute
2. **Symptoms vs root causes**: Gradient clipping treats symptoms; sequence length warmup addresses root causes
3. **Evolution of techniques**: The field moved from "prevent disasters" (2020) to "eliminate spikes" (2023+)
4. **Precision matters**: BF16's larger dynamic range prevents most numerical issues that plague FP16
5. **No silver bullet**: Even PaLM 540B with state-of-the-art techniques still experienced ~20 spikes
6. **Checkpointing is essential**: Frequent saves allow recovery from spikes without losing days of progress
7. **Efficiency gains**: Better stability techniques (especially SLW) enable faster training via larger batches and learning rates

For GPT-3's specific stability approach, see [[llm/models/gpt3/training|GPT-3 training.md]]. For how stability challenges affected reproduction efforts, see [[llm/training-techniques/gpt3-reproduction-challenges|gpt3-reproduction-challenges.md]].
