# GPT-3 to ChatGPT: Evolution Overview

The path from GPT-3 (June 2020) to ChatGPT (November 2022) involved several key developments that explored different directions: code specialization, tool use, and instruction following. This directory documents each step in chronological order.

## Timeline

### 1. **Learning to Summarize from Human Feedback** - September 2020

The first application of RLHF to a GPT-3 class model. Fine-tuned GPT-3 (1.3B and 6.7B sizes) to summarize text using the full pipeline that would later power InstructGPT and ChatGPT: supervised fine-tuning on human demonstrations, training a reward model on human comparisons, then optimizing with PPO against the reward model. Published just 3 months after GPT-3, this was the proof of concept that RLHF works on large language models. Key authors (Long Ouyang, Jeff Wu) went on to author InstructGPT.

**Paper**: ["Learning to summarize from human feedback"](https://arxiv.org/abs/2009.01325) (Stiennon et al., September 2020, NeurIPS 2020)

**Impact**: Proved RLHF works on LLMs, established the SFT → RM → PPO pipeline that became the industry standard through InstructGPT and ChatGPT.

---

### 2. **Codex** - July 2021

GPT-3 fine-tuned on code (159GB of Python code from GitHub). TabNine (2019) had already proved transformers could assist with coding by fine-tuning GPT-2, and GPT-3 itself showed accidental code-writing ability — Codex formalized this into a dedicated model, which powered GitHub Copilot as its first major commercial application.

**Paper**: ["Evaluating Large Language Models Trained on Code"](https://arxiv.org/abs/2107.03374) (Chen et al., July 2021)

**Impact**: Powers GitHub Copilot, established code generation as a major LLM application.

**See**: [[llm/models/gpt3/gpt3-to-chatgpt/codex/architecture|Codex documentation]]

---

### 3. **WebGPT** - December 2021

GPT-3 fine-tuned to use a text-based web browser for question answering. The model issues commands (search, click, scroll, quote) to browse the web, collects references, then composes answers with citations. Tested on three GPT-3 sizes: 760M, 13B, and 175B.

Neither tool use nor RLHF originated here — RLHF was established by Christiano et al. (2017) and applied to summarization by Stiennon et al. (2020), while retrieval-augmented models like REALM and RAG (2020) preceded it. But WebGPT was an early major milestone that combined both in a complex, agentic setting: the model itself decides when and how to use tools, and is trained end-to-end with human feedback. This pattern (LLM issuing tool commands + RLHF) became foundational for ChatGPT's browsing mode, function calling, and modern agent systems.

**Training pipeline**: Used the same four-stage approach later seen in InstructGPT — behavior cloning (supervised fine-tuning on ~6,000 human browsing demonstrations), reward modeling (trained on ~21,500 human comparisons), reinforcement learning (PPO against the reward model), and rejection sampling (generate multiple answers, pick the one the reward model scores highest). Notably, the best model used BC + rejection sampling — RL provided only a small additional benefit when combined with rejection sampling.

**Key results**: The 175B best-of-64 model's answers were preferred over human demonstrators' answers **56%** of the time, and over Reddit's highest-voted answers **69%** of the time. On TruthfulQA, WebGPT answers were true 75% of the time (vs GPT-3's much lower scores) and both true and informative 54% of the time.

**Connection to InstructGPT**: John Schulman appears as an author on both papers. The RLHF pipeline (BC → RM → PPO) is identical. WebGPT proved this pipeline works for complex multi-step tasks (browsing + answer synthesis), building confidence to apply it to the more general instruction-following problem in InstructGPT one month later.

**Paper**: ["WebGPT: Browser-assisted question-answering with human feedback"](https://arxiv.org/abs/2112.09332) (Nakano et al., December 2021)

**Impact**: Early milestone for both agentic tool use and RLHF in LLMs. Its ideas were absorbed into later products (ChatGPT browsing) rather than becoming a standalone product. Never launched as a user-facing tool.

**See**: [[llm/models/gpt3/gpt3-to-chatgpt/webgpt|WebGPT documentation]]

---

### 4. **InstructGPT** - January 2022

The breakthrough that made ChatGPT possible. Introduced the three-stage RLHF (Reinforcement Learning from Human Feedback) pipeline: Supervised Fine-Tuning → Reward Model → PPO optimization.

**Paper**: ["Training language models to follow instructions with human feedback"](https://arxiv.org/abs/2203.02155) (Ouyang et al., March 2022)

**Models**: `text-davinci-001` (deployed January 2022)

**Impact**: Showed that a 1.3B parameter model with RLHF could outperform 175B GPT-3 on instruction following. Established RLHF as the standard post-training approach for all modern LLMs.

**See**: [[llm/models/gpt3/gpt3-to-chatgpt/instructgpt|InstructGPT documentation]]

---

### 5. **GPT-3.5 Series** - March-November 2022

A series of models trained on a blend of text and code (integrating Codex improvements) with various fine-tuning approaches. Retroactively named "GPT-3.5" when ChatGPT launched.

**Models**:
- **`code-davinci-002`** (March 15, 2022) - Base model trained on text + code, foundation for the series
- **`text-davinci-002`** (March 15, 2022) - Fine-tuned from code-davinci-002 using supervised learning (FeedME method)
- **`text-davinci-003`** (November 28, 2022) - Trained with full RLHF (PPO), closest to InstructGPT methodology

**Documentation**: [OpenAI API - davinci-002](https://platform.openai.com/docs/models/davinci-002)

**Impact**: Combined code training (from Codex) with instruction following (from InstructGPT), creating a more capable and versatile base model.

**See**: [[llm/models/gpt3/gpt3-to-chatgpt/gpt3.5|GPT-3.5 documentation]]

---

### 6. **ChatGPT** - November 30, 2022

Fine-tuned from the GPT-3.5 series (likely `text-davinci-003`) with additional conversational optimization. Added dialogue format and launched as a free web interface.

**Announcement**: ["Introducing ChatGPT"](https://openai.com/index/chatgpt/) (OpenAI blog, November 30, 2022)

**Impact**:
- 1 million users in 5 days
- Fastest-growing consumer application in history
- Changed public perception of AI capabilities
- Launched the modern chatbot era

**See**: [[llm/models/gpt3/gpt3-to-chatgpt/chatgpt|ChatGPT documentation]]

---

## The Convergence

ChatGPT represents the convergence of three parallel research directions:

```
GPT-3 (June 2020)
  ├─→ Summarization RLHF (Sept 2020) ────→ proved RLHF works on LLMs
  │                                              ↓
  ├─→ Codex (code training) ─────────────┐  WebGPT (Dec 2021)
  │                                      │  (tool use + RLHF experience)
  └─→ InstructGPT (RLHF methodology) ────┼─→ Combine code + RLHF
                                          │
                                          ↓
                                   GPT-3.5 series
                                   (text-davinci-003)
                                          ↓
                                      ChatGPT
```

**Key insight**: ChatGPT isn't just "GPT-3 with RLHF" - it's GPT-3 trained on code (via Codex) THEN aligned with RLHF (via InstructGPT methodology) THEN optimized for conversation.

---

## Related Documents

- [[llm/models/gpt3/architecture|GPT-3 Architecture]] - The base model
- [[llm/models/gpt3/training|GPT-3 Training]] - Original training approach
- [[llm/models/gpt3/backstories|GPT-3 Backstories]] - Context and controversies
- [[llm/industry-timeline|LLM Industry Timeline]] - Broader market context
