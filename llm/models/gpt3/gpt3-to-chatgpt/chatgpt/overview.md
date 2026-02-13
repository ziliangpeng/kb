# ChatGPT

ChatGPT is a sibling model to text-davinci-003, not a wrapper around it. Both are fine-tuned from the GPT-3.5 base (code-davinci-002) with RLHF, but optimized for different use cases:

- **text-davinci-003** = RLHF optimized for **single-turn instruction following**
- **ChatGPT** = RLHF optimized for **multi-turn dialogue**

The key difference is in the training data — ChatGPT's RLHF used dialogue data where human AI trainers played both sides of a conversation, mixed with InstructGPT data converted to dialogue format.

No paper was published. OpenAI's blog post describes it as using "the same methods as InstructGPT, but with slight differences in the data collection setup."

## Timeline

- **November 30, 2022** — ChatGPT launches as a free research preview, web-only. No API access.
- **March 1, 2023** — `gpt-3.5-turbo` released as an API. OpenAI confirmed it is "the same model used in the ChatGPT product." Priced at $0.002/1K tokens — 10x cheaper than text-davinci-003, possibly through distillation to ~20B parameters (per a later-withdrawn Microsoft paper). This launch also introduced the Chat Completions API and ChatML.

## Model Identity and Size

The internal model slug `text-davinci-002-render-sha` (visible in the ChatGPT web interface) suggests it was fine-tuned from text-davinci-002, not text-davinci-003.

The product itself is a thin wrapper — a web chat interface that concatenates conversation history into the context window (4,096 tokens at launch). No special memory mechanism.

### The ~20B Parameter Mystery

All davinci-class models (text-davinci-001/002/003, code-davinci-001/002) are 175B. But strong indirect evidence suggests **gpt-3.5-turbo is much smaller — likely ~20B parameters**, distilled from the 175B base.

OpenAI has never confirmed or denied the parameter count. The secrecy itself is notable — if it were simply 175B (same as GPT-3), there would be little reason to hide it.

#### The "Microsoft Leak" (CodeFusion Paper)

A Microsoft Research paper, "CodeFusion: A Pre-trained Diffusion Model for Code Generation" ([arXiv:2310.17680](https://arxiv.org/abs/2310.17680), October 2023), listed gpt-3.5-turbo as 20B in a comparison table. It was **withdrawn within days**. The arXiv notice states the authors "relied solely on [a Forbes article]" and "do not have direct knowledge or verification." This was not a Microsoft insider leak — it was a researcher copying an unverified number from a speculative press article.

A second Microsoft paper (MEDEC, December 2024) listed parameter estimates for other models (GPT-4o: ~200B, GPT-4o-mini: ~8B, o1-preview: ~300B) but notably did not list a count for gpt-3.5-turbo.

#### Evidence For ~20B

**Pricing** (the strongest evidence): gpt-3.5-turbo launched at $0.002/1K tokens — **10x cheaper** than text-davinci-003 at $0.02/1K. Inference cost scales roughly with parameter count. OpenAI said they achieved "a 90% cost reduction for ChatGPT since December" through "system-wide optimizations" but did not elaborate.

**Latency**: gpt-3.5-turbo was significantly faster than text-davinci-003 (~91 tokens/second, 0.41s time to first token). Speed characteristics are more consistent with a model in the tens-of-billions range than 175B.

**Sam Altman's statements**: "I think we're at the end of the era where it's going to be these giant, giant models. We'll make them better in other ways" (MIT event, April 2023). Also: "I think there's been way too much focus on parameter count."

**GPT-4o-mini precedent**: OpenAI's official replacement for gpt-3.5-turbo is GPT-4o-mini, estimated at only ~8B parameters. If the replacement is 8B, the model it replaced being ~20B is plausible.

**MoE speculation**: gpt-3.5-turbo exhibits non-determinism at temperature=0, whereas original GPT-3 davinci is deterministic at temperature=0. This is consistent with sparse Mixture of Experts routing (84% probability on Manifold prediction market).

**Distillation precedent**: OpenAI's own InstructGPT paper showed a 1.3B RLHF model beating 175B GPT-3. OpenAI later launched model distillation as an official product feature.

#### Evidence Against

- The only primary source (CodeFusion) was withdrawn and traced to unverified speculation
- Infrastructure optimizations alone (quantization, batching) could account for some of the cost reduction
- Maintaining performance parity at ~9x fewer parameters would be impressive, even with distillation
- Manifold prediction market for "<25B parameters" sat at only 44% — not a strong consensus

#### Most Likely Scenario

OpenAI probably distilled a smaller model (~20B dense, or a sparse MoE with ~20B active parameters) from the 175B GPT-3.5 base. Combined with infrastructure optimizations, this achieved the 10x cost reduction. The original ChatGPT web product (November 2022) may have used the full 175B model, with the optimized smaller version arriving as gpt-3.5-turbo in March 2023.

**Sources**: [HN: Microsoft says GPT 3.5 has 20B?](https://news.ycombinator.com/item?id=38068328), [Artificial Analysis: GPT-3.5 Turbo](https://artificialanalysis.ai/models/gpt-35-turbo), [OpenAI Community: How many parameters?](https://community.openai.com/t/how-many-parameters-does-gpt-3-5-have/648417), [Manifold: <25B parameters?](https://manifold.markets/CalebW/does-gpt35turbo-have-25b-parameters)

## Impact

- 1 million users in 5 days
- Fastest-growing consumer application in history
- The product innovation was the chat interface making LLMs accessible to non-technical users — the underlying technology had been available via API for months

## Documentation

- [[llm/models/gpt3/gpt3-to-chatgpt/chatgpt/training|Training]]
- [[llm/models/gpt3/gpt3-to-chatgpt/chatgpt/chat-api|Chat API & ChatML]]
- [[llm/models/gpt3/gpt3-to-chatgpt/chatgpt/system-prompt|System Prompt]]
- [[llm/models/gpt3/gpt3-to-chatgpt/chatgpt/product-and-launch|Product & Launch]]
- [[llm/models/gpt3/gpt3-to-chatgpt/chatgpt/safety|Safety]]
- [[llm/models/gpt3/gpt3-to-chatgpt/chatgpt/backstories|Backstories]]

**Announcement**: ["Introducing ChatGPT"](https://openai.com/index/chatgpt/) (OpenAI blog, November 30, 2022)
