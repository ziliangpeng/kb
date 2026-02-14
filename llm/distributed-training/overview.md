# Distributed Training Overview

Distributed training enables training models across many GPUs. As clusters scale to tens or hundreds of thousands of GPUs, efficiency challenges emerge.

## Efficiency Challenges at Scale

### MFU Degradation

MFU (Model FLOPs Utilization) = actual FLOPs achieved / theoretical peak FLOPs.

In synchronized training, all GPUs must finish each step before anyone proceeds. At scale, MFU drops because:

- **Straggler probability increases** — With more GPUs, the chance that at least one is slow at any moment increases. Causes include thermal throttling, hardware variability (silicon lottery), transient errors, and network hiccups.
- **Communication overhead grows** — Collective operations (all-reduce) across more GPUs take longer.
- **Failure recovery overhead** — At scale, failures are frequent. Checkpointing and recovery add overhead.

### Collective Operation Bottlenecks

Training relies on collective operations (all-reduce, all-gather) to synchronize gradients across GPUs. With network oversubscription (e.g., 7:1 between pods), cross-pod communication is slower, bottlenecking the entire operation and causing GPU idle time.

## Semi-Synchronous Training

At extreme scale, fully synchronous training becomes impractical. Approaches like DiLoCo synchronize every ~500 steps instead of every step, reducing communication overhead at the cost of some gradient staleness.
