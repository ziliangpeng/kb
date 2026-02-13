# InstructGPT Evaluation & Results

**Paper**: ["Training language models to follow instructions with human feedback"](https://arxiv.org/abs/2203.02155) (Ouyang et al., March 2022)

## Results

### The Headline Number

A 1.3B InstructGPT model is preferred over the 175B GPT-3 — 100x fewer parameters, but aligned.

- 175B InstructGPT vs 175B GPT-3: preferred **85±3%** of the time
- 175B InstructGPT vs 175B GPT-3 (few-shot prompted): preferred **71±4%**
- 1.3B PPO-ptx vs 175B GPT-3: preferred by held-out labelers

### Progression

GPT-3 < GPT-3 (prompted) < SFT < PPO ≈ PPO-ptx

### Specific Improvements

- More appropriate for customer assistant context
- Better at following explicit constraints
- Less likely to hallucinate on closed-domain tasks (21% vs 41%)
- More likely to attempt the correct instruction

### vs Other Instruction-Tuned Models

- InstructGPT preferred 78±4% over FLAN, 79±4% over T0
- Key insight: public NLP instruction-tuning datasets are not reflective of real user usage

### TruthfulQA

~2x more truthful and informative than GPT-3, without any special truthfulness training.

### Toxicity

~25% less toxic with "respectful" prompt. But no improvement on bias benchmarks (Winogender, CrowS-Pairs).

### Alignment Tax

PPO causes regressions on SQuAD, DROP, HellaSwag, translation. PPO-ptx mitigates most of this.

### Generalization

Follows instructions in non-English languages and answers code questions, despite these being rare in training data (~4% non-English).

## Limitations

### Simple Mistakes

1. **Assumes false premises are true**: "Why is it important to eat socks after meditating?" → tries to explain instead of pushing back
2. **Over-hedges simple questions**: "What happens if you fire a cannonball at a pumpkin?" → long uncertain answer instead of "it explodes"
3. **Degrades with multiple constraints**: "List 10 movies made in the 1930s set in France" → struggles to satisfy all constraints simultaneously

### Who Are You Aligning To?

The paper is unusually honest about this (Section 5.2):

- Not "human values" broadly — specifically the preferences of ~40 English-speaking contractors
- Influenced by three layers: labeler demographics, OpenAI's instructions to labelers, OpenAI's customer base (API Playground users)
- The alignment target is narrow and specific, not universal

### The Alignment Tax

- RLHF improves helpfulness but causes regressions on traditional NLP benchmarks
- PPO-ptx partially fixes this but doesn't fully eliminate it
- Implication: alignment has a cost, and the field needs low-cost alignment techniques

### Obedient to a Fault

- When explicitly told to produce toxic content, InstructGPT is **more toxic than GPT-3**
- The model learned to follow instructions — including harmful ones
- It can't distinguish "follow this instruction" from "refuse this instruction"
- This foreshadows the "refusal" problem that ChatGPT would later need to address with more aggressive safety training

## Historical Significance

### The Cost of Alignment Is Low

- SFT training: 4.9 petaflop/s-days
- PPO-ptx training: 60 petaflop/s-days
- GPT-3 pretraining: 3,640 petaflop/s-days
- Alignment is **~1.5%** the cost of pretraining

### Alignment > Scale

A 1.3B aligned model beats a 175B unaligned model on human preference. This fundamentally changed the industry's approach — instead of just making models bigger, invest in post-training alignment.

### The Pipeline That Became Standard

SFT → RM → PPO became the default recipe for Claude, LLaMA-2, and essentially every frontier model that followed.

### Direct Ancestor of ChatGPT

ChatGPT is essentially InstructGPT optimized for dialogue format. The core technique is the same.

### Key People

- Long Ouyang, Jeff Wu (also on the summarization paper)
- John Schulman (also on WebGPT, PPO inventor)
- Paul Christiano (RLHF pioneer, later Anthropic, then ARC)
- Amanda Askell (later Anthropic)

The flow of people from this work to Anthropic is notable — several key contributors to InstructGPT went on to build Claude using the same foundational techniques.

---

## Related Documents

- [[llm/models/gpt3/gpt3-to-chatgpt/instructgpt/training|InstructGPT Training]] - Training pipeline, data, and methodology
- [[llm/models/gpt3/gpt3-to-chatgpt/overview|GPT-3 to ChatGPT Overview]] - Timeline and evolution
- [[llm/models/gpt3/gpt3-to-chatgpt/summarization/evaluation|Summarization Evaluation]] - Results for the foundational RLHF paper
- [[llm/models/gpt3/gpt3-to-chatgpt/webgpt/evaluation|WebGPT Evaluation]] - Results for the preceding RLHF application
- [[llm/training-techniques/ppo|PPO for LLMs]] - Detailed PPO mechanics
