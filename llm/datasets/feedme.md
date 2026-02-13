# FeedME

FeedME is OpenAI's internal name for a supervised fine-tuning approach used to create text-davinci-002 (the first GPT-3.5 instruction-following model). Not a dataset in the traditional sense — it's a data curation + training method.

## Method

FeedME uses two sources of training data:

- **Human-written demonstrations**: Contractors write ideal responses to prompts (same approach as InstructGPT's SFT stage)
- **Model outputs rated 7/7**: The model generates responses, human labelers score them on a 1-7 scale, and only perfect-scoring outputs are kept as training data

The model is then fine-tuned with standard supervised learning (next-token prediction) on this curated dataset. No reward model, no PPO — just SFT on high-quality examples.

## Significance

- Simpler and cheaper than full RLHF
- Produced text-davinci-002, which was a capable instruction-following model
- But text-davinci-003 (full RLHF) was noticeably better, especially at creative tasks and recovering in-context learning ability
- Initially the community assumed text-davinci-002 used RLHF (as described in the InstructGPT paper), but OpenAI later clarified it used FeedME instead

## Related Documents

- [[llm/models/gpt3/gpt3-to-chatgpt/overview|GPT-3 to ChatGPT Overview]] — where FeedME fits in the timeline
- [[llm/models/gpt3/gpt3-to-chatgpt/instructgpt/training|InstructGPT Training]] — the full RLHF pipeline that FeedME is a simplification of
