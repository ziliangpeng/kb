# ChatGPT Training

ChatGPT used "the same methods as InstructGPT, but with slight differences in the data collection setup." The three-stage pipeline is identical: SFT → RM → PPO.

## What Was Different: Dialogue Data

For the SFT stage, AI trainers wrote **conversations** rather than single-turn instruction-response pairs. Key details:

- Trainers played **both sides** of the conversation — they wrote user messages and assistant responses
- They were given access to **model-written suggestions** to help compose responses (not purely from scratch)
- InstructGPT data was mixed in, **converted into dialogue format**

## The Conceptual Difference from InstructGPT

InstructGPT trainers wrote responses to isolated instructions — each example was independent. ChatGPT trainers had to maintain **coherence across turns**: referring back to earlier messages, handling follow-ups, corrections, and topic changes. This is a fundamentally different skill — the model needed to learn conversation *flow*, not just instruction completion.

## What We Don't Know

OpenAI never disclosed:

- How many dialogue demonstrations were collected
- The ratio of dialogue data vs. converted InstructGPT data
- Whether the reward model was retrained on dialogue-specific comparisons, or they reused InstructGPT's RM
- How many turns the training dialogues typically had
- Specific guidelines given to trainers for the dialogue task (beyond what was public for InstructGPT)

## Open Question

How much of ChatGPT's conversational ability came from this dialogue-specific RLHF vs. being an emergent capability of a strong enough base model (GPT-3.5) with any RLHF? text-davinci-003 could already handle multi-turn conversation if you manually formatted the prompt — ChatGPT may have just been optimized to do it more naturally.
