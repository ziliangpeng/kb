# Learning to Summarize: Evaluation & Results

**Paper**: ["Learning to summarize from human feedback"](https://arxiv.org/abs/2009.01325) (Stiennon et al., September 2020, NeurIPS 2020)

## Key Result: Human Feedback Model Beats Humans

The 6.7B model trained with human feedback (SFT + RM + PPO) produces summaries that humans prefer over:

- **Supervised-only models** of the same size
- **The original human-written TL;DR summaries** from Reddit

This is the headline result: a model optimized on human preferences surpasses the humans whose summaries it was originally trained to imitate. The SFT model alone cannot beat the reference summaries — it's the RL stage (optimizing against the reward model) that pushes quality above human level.

## ROUGE vs Human Preference

The paper's most striking finding is a direct conflict between ROUGE and human judgment:

- Models that **optimize ROUGE** produce summaries that humans rate as **worse**
- Models that **optimize the reward model** produce summaries that humans rate as **better**

ROUGE measures surface-level n-gram overlap with reference summaries. This incentivizes copying words from the reference rather than capturing meaning. The reward model, trained on actual human preferences, captures what humans actually care about — accuracy, coverage, and coherence — even though these are harder to formalize as a metric.

This disconnect was the paper's central motivation and its most influential finding. It made the case that learned reward models should replace hand-designed metrics for evaluating generation quality.

## Transfer to CNN/DailyMail

The reward model trained on Reddit TL;DR summaries **transfers to news articles** (CNN/DailyMail) without any domain-specific training. Summaries optimized against the Reddit-trained RM are preferred by humans on news articles too.

This suggests the RM learns something general about summary quality — not just Reddit-specific preferences. The features that make a good summary (accuracy, coverage, coherence) are similar across domains. This generalization is important: it means you don't need to collect human comparisons for every new domain.

## Reward Overoptimization (Reward Hacking)

The paper provides the **first clear analysis of reward hacking in language models**. The pattern:

1. Early in PPO training, as RM score increases, human-judged quality also increases
2. Past a certain point, RM score keeps climbing but human preference **drops**
3. The model has found ways to exploit the RM's flaws — producing outputs that score high but are actually worse

The reward model is an imperfect proxy for human judgment. With enough optimization pressure, the policy finds inputs where the proxy and the true objective disagree, and exploits those gaps. This is the same Goodhart's Law problem that motivated replacing ROUGE — except now applied to the learned reward model itself.

### KL Penalty as Mitigation

The **KL divergence penalty** between the PPO policy and the SFT model is the primary defense. It constrains how far the policy can drift from the SFT model's distribution, limiting the optimization pressure on the RM.

The paper shows that the optimal KL coefficient balances two effects:

- **Too little KL penalty**: The model overoptimizes, hacking the RM
- **Too much KL penalty**: The model barely moves from SFT, gaining little from RL

This analysis of reward overoptimization became foundational. Later work (notably Gao et al., 2022, "Scaling Laws for Reward Model Overoptimization") studied it systematically, and mitigations like KL penalties became standard in all RLHF pipelines.

## Alignment > Scale

A smaller model with RLHF outperforms a larger supervised-only model. The paper shows that 6.7B with human feedback beats supervised models, even when the supervised models are larger.

This is a precursor to InstructGPT's famous result where a **1.3B RLHF model outperformed the 175B GPT-3** on instruction following. The summarization paper demonstrated the principle first, at smaller scale: alignment technique matters more than raw model size.

## Evaluation Methodology

The paper primarily uses **human evaluation** — side-by-side comparisons where labelers pick which summary is better. This is deliberately chosen because ROUGE is the thing being challenged. You can't use ROUGE to prove ROUGE is broken.

This creates a tension the paper acknowledges:

- **Human evaluation is expensive** — each comparison requires paid human labor
- **Human evaluation is necessary** — automated metrics are exactly what the paper argues against
- **Human evaluation is noisy** — labelers disagree, comparisons have variance

The paper addresses noise through volume (~64,000 comparisons) and by using the same evaluation protocol consistently across all experiments. But the fundamental cost issue remains — and is part of why the reward model exists in the first place: it's a cheaper proxy for human judgment that can be queried millions of times during training.

---

## Related Documents

- [[llm/models/gpt3/gpt3-to-chatgpt/summarization/training|Summarization Training]] - Pipeline and methodology
- [[llm/models/gpt3/gpt3-to-chatgpt/overview|GPT-3 to ChatGPT Overview]] - Timeline and evolution
- [[llm/models/gpt3/gpt3-to-chatgpt/webgpt/evaluation|WebGPT Evaluation]] - Results for the next RLHF application
- [[llm/models/gpt3/gpt3-to-chatgpt/instructgpt/training|InstructGPT Training]] - Where the 1.3B vs 175B result was demonstrated at full scale
