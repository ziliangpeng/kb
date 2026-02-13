# InstructGPT Training Pipeline

InstructGPT uses the same three-stage RLHF pipeline established in the summarization paper (Stiennon et al., 2020) and WebGPT, but applied to **all instructions** rather than narrow tasks. The pipeline: SFT → RM → PPO.

## The Problem

GPT-3's training objective (next-token prediction on internet text) is fundamentally different from what users want (follow instructions helpfully and safely). The paper's key claim: "Making language models bigger does not inherently make them better at following a user's intent." Scaling alone doesn't fix misalignment — you need to change the training objective.

## Stage 1: Supervised Fine-Tuning (SFT)

Fine-tune GPT-3 on human-written demonstrations of ideal responses to instructions. This is the same idea as Behavior Cloning (BC) in WebGPT — train the model to imitate human demonstrations via supervised learning. The difference is only the task domain: WebGPT BC demonstrated browsing actions, InstructGPT SFT demonstrates direct text responses.

- **Data**: ~13K prompts with labeler-written ideal responses
- **Training**: 16 epochs, cosine learning rate decay, 0.2 residual dropout
- **Model sizes**: 1.3B, 6B, 175B (all fine-tuned from GPT-3)

**Interesting finding**: The model overfits on validation loss after 1 epoch, but training for more epochs still improves human preference ratings. The standard ML metric (validation loss) doesn't capture what actually matters — human preference. SFT model selection was based on **RM score**, not validation loss.

## Stage 2: Reward Model (RM)

Train a model to predict which outputs humans would prefer. This becomes the "judge" that guides RL in Stage 3.

### Architecture

- **6B parameters only** — they tried 175B but it was unstable during training and "less suitable to be used as the value function during RL"
- **Initialized from the 6B SFT model** — they train SFT at multiple sizes; the RM always starts from the 6B SFT checkpoint specifically
- Remove the unembedding layer (the layer that maps hidden states → vocabulary), replace with a **scalar head** that outputs a single reward number

### Training Data and Ranking Approach

- ~33K prompts for RM training
- **Key difference from WebGPT**: Labelers **rank** K outputs at once (K = 4 to 9), rather than doing pairwise comparisons
- From each ranking of K outputs, extract all C(K,2) pairs as training data. A ranking of 4 outputs gives 6 pairs; a ranking of 9 gives 36 pairs. Much more data-efficient than pairwise labeling.
- **Critical detail**: All C(K,2) pairs from a single prompt are treated as a **single batch element**. Without this, the model overfits badly — because the same outputs appear in multiple pairs from the same ranking, treating them as independent examples lets the model memorize.

### Loss Function

Bradley-Terry model (same as WebGPT), averaged over all C(K,2) pairs per prompt:

```
loss(θ) = -1/C(K,2) · E[(x, y_w, y_l) ~ D] [log(σ(r_θ(x, y_w) - r_θ(x, y_l)))]
```

Where r_θ(x, y) is the scalar reward for prompt x and completion y, y_w is the preferred completion, and y_l is the less preferred completion.

## Stage 3: PPO (Reinforcement Learning)

Fine-tune the SFT model to produce outputs that the reward model scores highly, using Proximal Policy Optimization (PPO, Schulman et al., 2017).

- ~31K prompts for PPO training (from API — no human demonstrations needed, the RM provides the signal)
- Three model sizes: 1.3B, 6B, 175B
- The RM is always 6B regardless of policy size

### Four Models in Memory

PPO for LLMs requires keeping four models in GPU memory simultaneously:

1. **The policy** (the model being trained, e.g., 175B)
2. **The reference policy** (frozen copy of SFT model, for KL penalty)
3. **The reward model** (frozen 6B, scores complete outputs)
4. **The value function / critic** (initialized from RM, trained alongside policy — see [[llm/training-techniques/ppo|PPO]] for details)

### The PPO-ptx Objective

The full objective function:

```
objective(φ) = E[(x,y) ~ D_RL] [r_θ(x, y) - β · log(π_φ^RL(y|x) / π^SFT(y|x))]
               + γ · E[x ~ D_pretrain] [log(π_φ^RL(x))]
```

Three terms:

- **Term 1: `r_θ(x, y)`** — The reward model's score. This is what we're maximizing.
- **Term 2: `β · log(π_RL / π_SFT)`** — KL penalty from the SFT model. Prevents the policy from drifting too far and "reward hacking" (finding degenerate outputs that trick the RM). Same idea as WebGPT.
- **Term 3: `γ · E[log π_RL(x)]`** — **New in InstructGPT, not in WebGPT.** Mixes in pretraining gradients to prevent forgetting general capabilities. This is the "PPO-ptx" variant. For plain "PPO" models, γ = 0.

### Why PPO-ptx Matters

Plain PPO causes regressions on standard NLP benchmarks (SQuAD, HellaSwag, translation, etc.) — this is the **alignment tax**. The model gets better at following instructions but worse at general tasks. PPO-ptx mitigates this by mixing in pretraining data, essentially saying "keep being good at general language modeling while also learning to follow instructions."

### How PPO Training Works

See [[llm/training-techniques/ppo|PPO for LLMs]] for the detailed mechanics of how PPO converts reward scores into gradient updates (rollouts, advantage estimation, clipped loss, value function).

## Key Differences from WebGPT

| Aspect | WebGPT | InstructGPT |
|---|---|---|
| Task scope | Narrow (web browsing + QA) | Broad (any instruction) |
| RM size | Same as policy | Always 6B (175B unstable) |
| Comparison format | Pairwise | Rankings of K=4-9, all C(K,2) pairs |
| Rejection sampling | Yes (best-of-n) | No |
| Pretraining mix | No | Yes (PPO-ptx) |
| Data source | ELI5 questions | Real API user prompts |
| Tool use | Browser | None (pure text in/out) |

## The Data

### Prompt Sources

1. **Labeler-written prompts** (~13K, used for SFT bootstrapping): Early GPT-3 API users weren't submitting instruction-style prompts, so they needed to bootstrap the process. Labelers wrote three types:
   - **Plain**: Come up with any arbitrary task, ensuring diversity
   - **Few-shot**: Write an instruction plus multiple example input/output pairs
   - **User-based**: OpenAI shared use cases from API waitlist applications, labelers wrote prompts matching those use cases

2. **API prompts** (~20K+, used for RM and PPO): Real prompts from OpenAI Playground users who were already using early InstructGPT versions (trained on the SFT data). Deduplicated, PII filtered, max 200 per user, split by user ID so train/val/test never share users.

### Dataset Sizes

- SFT: ~13K training prompts (API + labeler-written)
- RM: ~33K training prompts (API + labeler-written)
- PPO: ~31K training prompts (API only)

### Task Distribution

- Generation: 45.6%
- Open QA: 12.4%
- Brainstorming: 11.2%
- Chat: 8.4%
- Rewrite: 6.6%
- Summarization: 4.2%
- Classification: 3.5%
- Other: 3.5%
- Closed QA: 2.6%
- Extract: 1.9%
- 96% English

### The Labeler Team

- ~40 contractors from Upwork and ScaleAI
- Selected via screening test for sensitivity to different demographics and ability to identify harmful outputs
- Inter-annotator agreement: 72.6% (training labelers), 77.3% (held-out labelers)
- Important policy choice: during **training**, labelers prioritize **helpfulness**. During **evaluation**, they prioritize **truthfulness and harmlessness**.

## References

- **Paper**: ["Training language models to follow instructions with human feedback"](https://arxiv.org/abs/2203.02155) (Ouyang et al., March 2022)
- **Evaluation**: [[llm/models/gpt3/gpt3-to-chatgpt/instructgpt/evaluation|InstructGPT Evaluation]]
- **Related**: [[llm/models/gpt3/gpt3-to-chatgpt/webgpt|WebGPT documentation]]
- **PPO details**: [[llm/training-techniques/ppo|PPO for LLMs]]
- **Overview**: [[llm/models/gpt3/gpt3-to-chatgpt/overview|GPT-3 to ChatGPT Overview]]
