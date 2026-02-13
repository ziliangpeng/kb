# PPO for LLMs

Proximal Policy Optimization (PPO) is a reinforcement learning algorithm from Schulman et al. (2017), originally designed for game/robotics environments. It became the standard RL algorithm for LLM alignment through the summarization paper (Stiennon et al., 2020), WebGPT, and InstructGPT, and remained the default until alternatives like DPO emerged.

This document covers the mechanics of how PPO works in the LLM context — how a single reward score for a complete response gets turned into gradient updates for the model.

## The Core Loop

1. **Rollout**: The policy generates a complete response to a prompt (autoregressive, token by token)
2. **Score**: The reward model scores the complete response → one scalar R
3. **Compute advantages**: Spread credit to individual tokens using the value function
4. **Compute loss**: Use the advantages + token log-probabilities to compute the PPO clipped loss
5. **Update**: Backprop and update the policy weights
6. Repeat

## Step 1: Rollout

The policy generates tokens autoregressively — T separate forward passes, each producing one token. The log-probability of each token is saved as **π_old**. No activations need to be stored; this is pure inference.

The output of this step: the generated text + the π_old log-probabilities at each token position.

## Step 2: Score

The reward model takes the complete (prompt, response) pair and outputs a single scalar reward R. This is the only signal from the RM — it cannot score partial responses.

## Step 3: Compute Per-Token Rewards and Advantages

### Per-token rewards

The RM gives one reward for the entire sequence. This is distributed as:

- For tokens t < T (all except last): `r(t) = -β · KL_t`
- For the last token T: `r(T) = R - β · KL_T`

Where KL_t is the per-token KL divergence between the RL policy and the reference (SFT) policy. The KL penalty at every position discourages the policy from drifting from the SFT model.

### The value function (critic)

The value function V(s_t) is a separate model that predicts: "given the prompt and tokens generated so far, what reward do I expect at the end?"

**Key details**:

- In InstructGPT, it is **initialized from the reward model** but is a separate copy that gets further trained during PPO
- The RM was trained to score **complete** outputs — it was never trained to make predictions at intermediate token positions. So even though the value function starts as a copy of the RM, it needs further training to learn mid-sequence prediction.
- It's trained alongside the policy using a simple regression loss: `L_value = (V(s_t) - actual_return)²`

### Advantage computation

The advantage at each token position tells you: "was this token better or worse than expected?"

Using temporal difference:

```
A(t) = r(t) + γ · V(s_{t+1}) - V(s_t)
```

This is: what I actually got (r(t)) + what I expect going forward (γ · V(s_{t+1})) - what I expected before this step (V(s_t)).

In practice, GAE (Generalized Advantage Estimation) is used, which smooths this over multiple timesteps for more stable estimates. The core idea remains the same — the value function propagates the end-of-sequence reward backward to earlier tokens.

## Step 4: Compute the PPO Clipped Loss

### Why a separate forward pass is needed

The rollout (Step 1) generated the text and saved π_old, but for the loss computation we need a **training forward pass**: one forward pass over the entire (prompt + response) sequence at once, with **activations stored** for backpropagation. This gives us log-probabilities at every token position connected to the current model weights.

This is different from the rollout in important ways:

| | Rollout | Training forward pass |
|---|---|---|
| Purpose | Generate text | Compute loss for backprop |
| Passes | T sequential passes (one per token) | 1 pass over full sequence |
| Stores activations? | No | Yes (needed for backprop) |
| Output | Generated tokens + π_old | Gradients for weight update |

**Why activations must be stored**: Backpropagation requires the intermediate values from the forward pass. For example, computing the gradient through a ReLU requires knowing whether the input was positive or negative. The loss alone (a single scalar) doesn't contain enough information to reconstruct what happened at every layer. This is why training uses much more GPU memory than inference.

**Gradient checkpointing**: A memory optimization where activations are stored only at every Nth layer, and recomputed on the fly during backprop from the nearest checkpoint. Trades compute for memory. Everything stays in GPU memory (not disk).

### The loss function

For each token at position t:

**1. Compute the probability ratio:**

```
ratio(t) = π_new(token_t | context) / π_old(token_t | context)
         = exp(log π_new - log π_old)
```

**2. Compute the clipped loss:**

```
L(t) = -min(ratio(t) · A(t), clip(ratio(t), 1-ε, 1+ε) · A(t))
```

Where ε is typically 0.2 (so the ratio is clamped to [0.8, 1.2]).

**How it works**:

- If A(t) > 0 (good token): we want to increase its probability (ratio > 1), but clip prevents going above 1+ε
- If A(t) < 0 (bad token): we want to decrease its probability (ratio < 1), but clip prevents going below 1-ε
- The min takes the more pessimistic estimate, preventing overly aggressive updates

**On the first update**: π_new = π_old, so the ratio is 1.0 everywhere. The loss simplifies to `L(t) = -A(t)`. But the gradient of the ratio with respect to the weights is not zero — backprop pushes weights to increase probability of positive-advantage tokens and decrease probability of negative-advantage tokens.

### Multiple updates per rollout

PPO does **multiple gradient updates** (mini-epochs) on the same batch of rollout data. This is the whole point of PPO — it's more sample-efficient than vanilla policy gradient because it reuses data. After the first update, the weights change, so π_new ≠ π_old, and the clipping starts actively constraining updates. This prevents the policy from drifting too far from the version that generated the data.

## Step 5: Backprop and Update

The loss depends on log π_new(token_t), which is connected to the model weights through the training forward pass. The advantages and π_old are treated as **constants** — no gradients flow through them. They're just numbers from the rollout.

Gradients flow: `L → ratio → log π_new → model weights`

## Deterministic Inference

A subtle but important engineering concern: the rollout forward pass and the training forward pass must produce **identical logits** for the same input with the same weights. If they don't (due to floating-point non-associativity from different batching/parallelism), then π_old saved from the rollout won't match what the training pass computes, and the ratio is wrong from the start.

This effectively turns on-policy RL into off-policy RL:

- **On-policy**: Learn from data generated by your current policy. PPO assumes this.
- **Off-policy**: Learn from data generated by a different policy. Requires corrections and is less stable.

In practice, PPO's clipping provides robustness against small nondeterministic discrepancies. InstructGPT (2022) was trained successfully without addressing this. It became a focus in 2025 (SGLang team) when RL training at much larger scale made the accumulated noise matter more.

## Why PPO Was Eventually Challenged

PPO for LLMs is complex and expensive:

- Requires four models in memory (policy, reference policy, reward model, value function)
- Rollout generation is slow (autoregressive)
- Many hyperparameters to tune for stability
- The value function adds complexity and potential instability

This motivated simpler alternatives like **DPO** (Direct Preference Optimization), which converts preference data directly into a supervised loss — skipping the reward model, value function, and RL loop entirely.

## References

- **PPO paper**: ["Proximal Policy Optimization Algorithms"](https://arxiv.org/abs/1707.06347) (Schulman et al., 2017)
- **Applied in InstructGPT**: [[llm/models/gpt3/gpt3-to-chatgpt/instructgpt/training|InstructGPT Training Pipeline]]
- **Deterministic inference**: ["Towards Deterministic Inference in SGLang and Reproducible RL Training"](https://lmsys.org/blog/2025-09-22-sglang-deterministic/) (LMSYS, 2025)
