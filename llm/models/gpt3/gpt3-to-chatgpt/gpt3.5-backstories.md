# GPT-3.5 Backstories

Behind-the-scenes context and historical details about the GPT-3.5 series.

## Code Improving Reasoning Was Accidental

The original Codex (July 2021) was built as a code-generation model --- GPT-3 fine-tuned on Python code from GitHub. The goal was programming assistance, not general reasoning improvement.

The discovery that code training dramatically improved reasoning on non-code tasks appears to have been a surprise. Yao Fu's influential December 2022 analysis, "How does GPT Obtain its Ability?", explicitly called complex reasoning with chain-of-thought "a magical side product of training on code." His key observation: the original GPT-3 was not trained on code and could not do chain-of-thought. code-davinci-002 was trained on both text and code, and that code training gave it reasoning abilities that GPT-3 lacked entirely.

The mechanism makes intuitive sense in retrospect --- code is structured, sequential, and requires step-by-step logical reasoning. Models trained on code implicitly learn to decompose problems. But at the time of Codex's development, this was not the stated goal. OpenAI set out to build a better Codex successor; what they got was a fundamentally more capable base model for everything.

## GPT-3.5 Was a Test Run for GPT-4

The GPT-4 technical report contains a remarkable disclosure: OpenAI "trained GPT-3.5 as a first 'test run' of the system" roughly a year before GPT-4's release. GPT-3.5 was not just an incremental product update --- it was a critical infrastructure validation exercise.

OpenAI had rebuilt their "entire deep learning stack" and co-designed a supercomputer with Azure. GPT-3.5 let them find and fix bugs, validate scaling predictions, and improve their theoretical foundations before committing the vastly larger compute budget for GPT-4. A core achievement of the GPT-4 project was developing "infrastructure and optimization methods that have very predictable behavior across multiple scales," allowing them to predict GPT-4's performance from models trained with 1/1,000th of the compute.

GPT-3.5 was the dress rehearsal.

## FeedME Shipped Because RLHF Was Too Finicky

When OpenAI shipped text-davinci-002 in March 2022, it used FeedME (supervised fine-tuning) rather than full RLHF. Text-davinci-003 with full RLHF didn't ship until November 2022 --- eight months later.

The gap suggests significant implementation challenges. RLHF with PPO is notoriously finicky in practice --- it involves training a separate reward model, dealing with reward hacking, and carefully tuning the RL optimization to avoid collapse. OpenAI's own InstructGPT paper acknowledged that the PPO model hallucinated "much more" compared to SFT in some evaluations.

FeedME was likely the pragmatic choice: a simpler, more reliable method that could be shipped quickly while the team continued wrestling with making full RLHF stable enough for production. As one analysis noted, the extended timeline between publishing the InstructGPT RLHF results (January/March 2022) and actually shipping a PPO-trained model (November 2022) suggests PPO proved "finicky in practice."

## The Mode Collapse Confusion

One of the more fascinating episodes in AI alignment research.

A researcher known as janus published "Mysteries of mode collapse" on LessWrong, documenting striking observations about text-davinci-002 --- for instance, when asked to generate random numbers, the model showed dramatically sharper bias toward certain outputs (97% preference for its top choice) compared to the base model. The post attributed these phenomena to RLHF, and was originally titled "Mysteries of mode collapse due to RLHF."

The entire community assumed text-davinci-002 was an RLHF model. Researchers were building alignment conclusions on top of this assumption.

Then janus received evidence from "multiple credible sources" that text-davinci-002 was not RLHF-trained at all --- it used FeedME (supervised fine-tuning). The original post was corrected. The ironic twist: the mode collapse phenomena that everyone attributed to RLHF did not reproduce in text-davinci-003, which was trained with RLHF. The actual RLHF model exhibited higher entropy outputs --- the opposite of what was assumed. Supervised fine-tuning (FeedME) was the culprit all along.

This episode had real consequences. External researchers comparing their work against OpenAI models had unknowingly used versions trained with simpler methods than assumed, potentially compromising their conclusions about instruction-tuning effectiveness.

## The Retroactive Naming

The models we now call "GPT-3.5" shipped to the API months before getting that name:

- **March 15, 2022**: code-davinci-002 and text-davinci-002 released. Described as "new versions of GPT-3 and Codex." No "GPT-3.5" branding.
- **November 28, 2022**: text-davinci-003 released.
- **November 30, 2022**: ChatGPT launched. OpenAI's blog post described it as "fine-tuned from a model in the GPT-3.5 series" --- the first time "GPT-3.5" appeared.

TechCrunch described GPT-3.5 as "a previously-unannounced, improved version of GPT-3" --- the name was new even though the models weren't. This was almost certainly a marketing decision for ChatGPT's launch: it signaled improvement over GPT-3, created a clear product narrative, and implicitly set up anticipation for GPT-4.

## ChatGPT Backstories

The ChatGPT-specific backstories (nearly shelved, the 10-day sprint, the naming, the viral surprise, the Altman firing, competitor reactions, and more) have been moved to their own document: [[llm/models/gpt3/gpt3-to-chatgpt/chatgpt/backstories|ChatGPT Backstories]].

---

## Related Documents

- [[llm/models/gpt3/gpt3-to-chatgpt/gpt3.5|GPT-3.5 Series]] --- Technical overview
- [[llm/models/gpt3/gpt3-to-chatgpt/overview|GPT-3 to ChatGPT Overview]] --- Full timeline
- [[llm/models/gpt3/gpt3-to-chatgpt/codex/backstory|Codex Backstory]] --- Why OpenAI built Codex
- [[llm/models/gpt3/backstories|GPT-3 Backstories]] --- Context and controversies
