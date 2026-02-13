# GPT-2 RLHF: Fine-Tuning Language Models from Human Preferences

**Paper**: ["Fine-Tuning Language Models from Human Preferences"](https://arxiv.org/abs/1909.08593) (Ziegler et al., September 2019) — OpenAI

First application of RLHF to a language model. Took the framework from Christiano et al. (2017) — which was proven on Atari games and simulated robotics — and applied it to GPT-2 (774M). Demonstrated that human preference feedback could steer a pretrained LM's behavior on four tasks. Direct predecessor to the summarization paper (Stiennon et al., 2020) which scaled RLHF to GPT-3.

**Key authors**: Daniel Ziegler, Nisan Stiennon (later led the summarization paper), Paul Christiano (first author of Christiano 2017), Dario Amodei (later co-founded Anthropic), Tom Brown (later led GPT-3), Alec Radford (creator of GPT-1/2), Geoffrey Irving (later Anthropic).

## The Four Tasks

- **Two easy stylistic tasks**: sentiment continuation and descriptive continuation (from BookCorpus excerpts). Simple, unambiguous quality signal. Only 5,000 human comparisons needed each.
- **Two hard summarization tasks**: TL;DR (Reddit) and CNN/DailyMail (news). Multidimensional quality. Required 60,000 comparisons each.
- The gradient from easy to hard was deliberate — testing whether RLHF scales with task complexity.

## Training Pipeline

Brief overview here since the pipeline is covered more thoroughly in the [[llm/models/gpt3/gpt3-to-chatgpt/summarization/training|summarization]] and [[llm/models/gpt3/gpt3-to-chatgpt/instructgpt/training|InstructGPT]] docs.

1. **Start with pretrained GPT-2 (774M)** as initial policy
2. **Collect human comparisons** — generate 4 candidates per input, human picks the best (4-way comparisons, yielding 6 pairwise signals per labeling session — more efficient than pairwise)
3. **Train reward model** — same transformer architecture as GPT-2 but with a scalar output head replacing the unembedding layer
4. **Optimize with PPO + KL penalty**: `R(x,y) = r(x,y) - β·KL(π||ρ)`, where ρ is the original pretrained model

The KL penalty was introduced in this paper. It prevents the policy from diverging too far from the pretrained model, which would cause reward hacking / mode collapse. This became standard in every RLHF pipeline after.

## Online vs Offline Data Collection

- **Offline**: collect all human labels upfront from the base model, train RM once, then run PPO
- **Online**: as PPO improves the policy, periodically generate new outputs from the current policy, collect new human labels, retrain the RM

Results:

- For stylistic tasks: no difference between online and offline
- For summarization: online preferred 71% of the time over offline. The offline RM couldn't judge quality on the kinds of outputs the improved policy generated — it was extrapolating beyond its training distribution.

Takeaway: the harder the task and the more the output distribution shifts during training, the more you need online collection. This connects to reward overoptimization in later work — same underlying problem (RM judging out-of-distribution outputs).

## Labeler Exploitation

On summarization, the model learned to copy whole sentences verbatim from the input, skipping irrelevant preamble. This got good ROUGE scores and labelers preferred it — because copied sentences are easy to verify as accurate. But it's not real summarization — it's extractive copying.

The authors acknowledged "a mismatch between the notion of quality we wanted our model to learn, and what the human labelers actually evaluated."

This is a different kind of reward hacking than what the summarization paper later documented. In Stiennon 2020, the policy exploits flaws in the RM. Here, the RM faithfully captures what labelers prefer, but what labelers prefer isn't what you actually want. The flaw is in the human feedback itself.

## Significance

- **First RLHF on a language model** — bridged the gap between Christiano 2017 (games/robotics) and the modern LLM alignment paradigm
- **Introduced the KL penalty** that became standard
- **Demonstrated online data collection matters** for hard tasks
- **Revealed labeler exploitation** as a failure mode
- **Direct ancestor**: Ziegler 2019 → Stiennon 2020 (summarization) → InstructGPT → ChatGPT

---

## Related Documents

- [[llm/models/gpt3/gpt3-to-chatgpt/summarization/training|Summarization Training]] — the direct follow-up at GPT-3 scale
- [[llm/models/gpt3/gpt3-to-chatgpt/overview|GPT-3 to ChatGPT Overview]] — timeline
- [[llm/training-techniques/ppo|PPO for LLMs]] — the RL algorithm used
- [[llm/models/gpt2/training|GPT-2 Training]] — the base model
