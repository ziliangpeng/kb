# Codex

**Paper**: ["Evaluating Large Language Models Trained on Code"](https://arxiv.org/abs/2107.03374) (Chen et al., July 2021)

## Model Sizes

The paper evaluated 8 Codex model sizes, all fine-tuned on code from GitHub:

| Model | Parameters | HumanEval pass@1 |
|-------|-----------|-----------------|
| Codex-12M | 12M | 2.00% |
| Codex-25M | 25M | 3.21% |
| Codex-42M | 42M | 5.06% |
| Codex-85M | 85M | 8.22% |
| Codex-300M | 300M | 13.17% |
| Codex-679M | 679M | 16.22% |
| Codex-2.5B | 2.5B | 21.36% |
| Codex-12B | 12B | 28.81% |

For comparison, **GPT-3 175B scored 0%** on HumanEval without code fine-tuning. Code training on a 12B model massively outperforms a general 175B model on code tasks.

### Relationship to GPT-3 Sizes

The paper states models were fine-tuned "from the GPT-3 model family," but the Codex sizes **don't match** the standard [[llm/models/gpt3/architecture|GPT-3 model sizes]] (125M, 350M, 760M, 1.3B, 2.7B, 6.7B, 13B, 175B). This suggests OpenAI had internal models at non-standard sizes, or these were effectively trained from scratch at these sizes.

Notably, the paper found that **fine-tuning from pre-trained GPT did not improve final performance** over training from scratch — possibly because the code dataset (159GB) was large enough. However, fine-tuning from GPT **did speed up convergence**, so they used this approach for all experiments.

### The code-davinci-002 Mystery

The production model `code-davinci-002` (March 2022), which later became the base for the [[llm/models/gpt3/gpt3-to-chatgpt/gpt3.5|GPT-3.5 series]], has an **undisclosed parameter count**. OpenAI never confirmed whether it was 12B (like the paper's largest model) or 175B (like GPT-3 Davinci). The "davinci" naming convention suggests 175B, but this is unconfirmed.

---

## Related Documents

- [[llm/models/gpt3/gpt3-to-chatgpt/overview|GPT-3 to ChatGPT Overview]] - Timeline and evolution
- [[llm/models/gpt3/architecture|GPT-3 Architecture]] - Base model specifications
