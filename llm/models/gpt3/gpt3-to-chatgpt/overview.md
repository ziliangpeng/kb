# GPT-3 to ChatGPT: Evolution Overview

The path from GPT-3 (June 2020) to ChatGPT (November 2022) involved several key developments that explored different directions: code specialization, tool use, and instruction following. This directory documents each step in chronological order.

## Timeline

### Predecessor: Fine-Tuning Language Models from Human Preferences — September 2019

The first application of RLHF to a language model. Ziegler et al. applied the Christiano et al. (2017) RLHF framework — originally proven on Atari games and simulated robotics — to GPT-2 (774M parameters). Tested on four tasks: sentiment continuation, descriptive continuation, and summarization (TL;DR and CNN/DailyMail). Introduced the KL divergence penalty between the trained policy and the pretrained model, which became standard in all later RLHF work. Showed that RLHF works on language models but revealed labeler exploitation on summarization — the model learned to copy sentences rather than truly summarize. This directly motivated the summarization paper (Stiennon et al., 2020), which solved these issues at GPT-3 scale.

**Paper**: ["Fine-Tuning Language Models from Human Preferences"](https://arxiv.org/abs/1909.08593) (Ziegler et al., September 2019)

**See**: [[llm/models/gpt2/rlhf|GPT-2 RLHF documentation]]

---

### 1. **Learning to Summarize from Human Feedback** - September 2020

The first application of RLHF to a GPT-3 class model. **RLHF on GPT-3 for one specific task: summarization.** Fine-tuned GPT-3 (1.3B and 6.7B sizes) to summarize text using the full pipeline that would later power InstructGPT and ChatGPT: supervised fine-tuning on human demonstrations, training a reward model on human comparisons, then optimizing with PPO against the reward model. Published just 3 months after GPT-3, this was the proof of concept that RLHF works on large language models. Key authors (Long Ouyang, Jeff Wu) went on to author InstructGPT.

**Paper**: ["Learning to summarize from human feedback"](https://arxiv.org/abs/2009.01325) (Stiennon et al., September 2020, NeurIPS 2020)

**Impact**: Proved RLHF works on LLMs, established the SFT → RM → PPO pipeline that became the industry standard through InstructGPT and ChatGPT.

**See**: [[llm/models/gpt3/gpt3-to-chatgpt/summarization|Summarization documentation]]

---

### 2. **Codex** - July 2021

GPT-3 fine-tuned on code (159GB of Python code from GitHub). TabNine (2019) had already proved transformers could assist with coding by fine-tuning GPT-2, and GPT-3 itself showed accidental code-writing ability — Codex formalized this into a dedicated model, which powered GitHub Copilot as its first major commercial application.

**Paper**: ["Evaluating Large Language Models Trained on Code"](https://arxiv.org/abs/2107.03374) (Chen et al., July 2021)

**Models**: `code-davinci-001`, `code-cushman-001`

**Impact**: Powers GitHub Copilot, established code generation as a major LLM application.

**See**: [[llm/models/gpt3/gpt3-to-chatgpt/codex/architecture|Codex documentation]]

---

### 3. **WebGPT** - December 2021

**RLHF on GPT-3 for one specific task: question answering with web browsing.** The model issues commands (search, click, scroll, quote) to browse the web, collects references, then composes answers with citations. Tested on three GPT-3 sizes: 760M, 13B, and 175B.

Neither tool use nor RLHF originated here — RLHF was established by Christiano et al. (2017) and applied to summarization by Stiennon et al. (2020), while retrieval-augmented models like REALM and RAG (2020) preceded it. But WebGPT was an early major milestone that combined both in a complex, agentic setting: the model itself decides when and how to use tools, and is trained end-to-end with human feedback. This pattern (LLM issuing tool commands + RLHF) became foundational for ChatGPT's browsing mode, function calling, and modern agent systems.

**Training pipeline**: Used the same four-stage approach later seen in InstructGPT — behavior cloning (supervised fine-tuning on ~6,000 human browsing demonstrations), reward modeling (trained on ~21,500 human comparisons), reinforcement learning (PPO against the reward model), and rejection sampling (generate multiple answers, pick the one the reward model scores highest). Notably, the best model used BC + rejection sampling — RL provided only a small additional benefit when combined with rejection sampling.

**Key results**: The 175B best-of-64 model's answers were preferred over human demonstrators' answers **56%** of the time, and over Reddit's highest-voted answers **69%** of the time. On TruthfulQA, WebGPT answers were true 75% of the time (vs GPT-3's much lower scores) and both true and informative 54% of the time.

**Connection to InstructGPT**: John Schulman appears as an author on both papers. The RLHF pipeline (BC → RM → PPO) is identical. WebGPT proved this pipeline works for complex multi-step tasks (browsing + answer synthesis), building confidence to apply it to the more general instruction-following problem in InstructGPT one month later.

**Paper**: ["WebGPT: Browser-assisted question-answering with human feedback"](https://arxiv.org/abs/2112.09332) (Nakano et al., December 2021)

**Impact**: Early milestone for both agentic tool use and RLHF in LLMs. Its ideas were absorbed into later products (ChatGPT browsing) rather than becoming a standalone product. Never launched as a user-facing tool.

**See**: [[llm/models/gpt3/gpt3-to-chatgpt/webgpt|WebGPT documentation]]

---

### 4. **InstructGPT** - January 2022

**RLHF on GPT-3 for all tasks.** The summarization paper and WebGPT each applied RLHF to one specific task — InstructGPT's key insight was that you don't need a separate RLHF-trained model for each task. Train one model on diverse instructions and it generalizes. GPT-3 is trained to predict the next token on internet text, but users want it to follow instructions — these are different objectives. Scaling alone doesn't fix this; the paper's key claim is "making language models bigger does not inherently make them better at following a user's intent." The breakthrough that made ChatGPT possible, using the three-stage RLHF pipeline: Supervised Fine-Tuning → Reward Model → PPO optimization.

**Paper**: ["Training language models to follow instructions with human feedback"](https://arxiv.org/abs/2203.02155) (Ouyang et al., March 2022)

**Models**: `text-davinci-001` (deployed January 2022) — based on original GPT-3 (not code-trained)

**Impact**: Showed that a 1.3B parameter model with RLHF could outperform 175B GPT-3 on instruction following. Established RLHF as the standard post-training approach for all modern LLMs.

**See**: [[llm/models/gpt3/gpt3-to-chatgpt/instructgpt|InstructGPT documentation]]

---

### 5. **GPT-3.5 Series** - March-November 2022

A series of models trained on a blend of text and code (integrating Codex improvements) with various fine-tuning approaches. Retroactively named "GPT-3.5" when ChatGPT launched.

**Models**:

- **`code-davinci-002`** (March 15, 2022) — Base model, pre-trained on a blend of text and code. Not instruction-tuned. Despite the "code" prefix, this is a general-purpose base model — the foundation for the entire GPT-3.5 series. Same 175B architecture as GPT-3.
- **`text-davinci-002`** (March 15, 2022) — code-davinci-002 fine-tuned with FeedME (supervised fine-tuning on human demonstrations and model outputs rated 7/7 by labelers). Instruction-following model, but NOT trained with RLHF.
- **`text-davinci-003`** (November 28, 2022) — code-davinci-002 fine-tuned with full RLHF (SFT → RM → PPO). The first GPT-3.5 model to use the complete InstructGPT methodology. Recovered in-context learning abilities that text-davinci-002 had lost.

**Documentation**: [OpenAI API - davinci-002](https://platform.openai.com/docs/models/davinci-002)

**Impact**: Combined code training (from Codex) with instruction following (from InstructGPT), creating a more capable and versatile base model.

**See**: [[llm/models/gpt3/gpt3-to-chatgpt/gpt3.5|GPT-3.5 documentation]]

---

### 6. **ChatGPT** - November 30, 2022

A sibling model to text-davinci-003, not a wrapper around it. Both are fine-tuned from the GPT-3.5 base (code-davinci-002) with RLHF, but optimized for different use cases:

- **text-davinci-003** = RLHF optimized for **single-turn instruction following** ("do this task")
- **ChatGPT model** = RLHF optimized for **multi-turn dialogue** ("let's have a conversation")

The key difference is in the training data. ChatGPT's RLHF used dialogue data where human AI trainers played both sides of a conversation (user and assistant), mixed with InstructGPT data transformed into dialogue format. This taught the model conversation flow — follow-up questions, referring back to earlier messages, admitting mistakes, challenging incorrect premises.

The internal model slug `text-davinci-002-render-sha` (visible in the ChatGPT web interface) suggests it was fine-tuned from text-davinci-002, not text-davinci-003.

No paper was published. OpenAI's blog post describes it as using "the same methods as InstructGPT, but with slight differences in the data collection setup." The training methodology diagram is identical to InstructGPT's (SFT → RM → PPO). No dataset sizes, training details, or benchmarks were disclosed.

The product itself is a thin wrapper — a web chat interface that concatenates conversation history into the context window (4,096 tokens at launch). No special memory mechanism.

**Models**:

- **ChatGPT web product** (November 30, 2022) — launched as a free research preview, web-only. No API access for 3 months.
- **`gpt-3.5-turbo`** (March 1, 2023) — the ChatGPT model released as an API. OpenAI confirmed it is "the same model used in the ChatGPT product." Priced at $0.002/1K tokens — 10x cheaper than text-davinci-003, possibly through distillation to ~20B parameters (per a later-withdrawn Microsoft paper).

**The Chat API**: `gpt-3.5-turbo` introduced the new **Chat Completions endpoint** (`/v1/chat/completions`), replacing the old Completions endpoint (`/v1/completions`). Instead of sending a raw text prompt, developers send structured messages with roles (system/user/assistant). This was built on **ChatML** (Chat Markup Language), which uses special tokens (`<|im_start|>`, `<|im_end|>`) to mark message boundaries. All previous models (text-davinci-003 and earlier) were completion-only. All models from gpt-3.5-turbo onward are chat-only. By July 2023, 97% of API usage had moved to the chat endpoint.

**Announcement**: ["Introducing ChatGPT"](https://openai.com/index/chatgpt/) (OpenAI blog, November 30, 2022)

**Impact**:

- 1 million users in 5 days
- Fastest-growing consumer application in history
- Changed public perception of AI capabilities
- Launched the modern chatbot era
- The product innovation was the chat interface making LLMs accessible to non-technical users — the underlying technology had been available via API for months

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
