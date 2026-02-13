# GPT-3.5 Series

Not a single model but a series of three models, released March--November 2022. GPT-3.5 is the convergence of two research lines: code training (from Codex) and instruction tuning (from InstructGPT), built on the same 175B transformer architecture as GPT-3. The "GPT-3.5" name didn't exist until ChatGPT launched on November 30, 2022 --- before that, these models were available on the API as new GPT-3/Codex models. The name was applied retroactively to group the models that shared code-davinci-002 as their base.

No technical paper was published for the GPT-3.5 series. What we know comes from OpenAI API documentation, blog posts, and community analysis.

## The Three Models

- **`code-davinci-002`** (March 15, 2022) --- The base model. Pre-trained on a blend of text and code. Not instruction-tuned. Despite the "code" prefix, this is a general-purpose base model, not a code specialist like Codex. It's the foundation for the entire GPT-3.5 series --- both text-davinci-002 and text-davinci-003 are fine-tuned from it. Same 175B architecture as GPT-3. The exact training details (text-to-code ratio, whether trained from scratch or further pre-trained from GPT-3) were never disclosed.

- **`text-davinci-002`** (March 15, 2022) --- code-davinci-002 fine-tuned with FeedME: supervised fine-tuning on human-written demonstrations and model outputs rated 7/7 by human labelers. This is SFT only --- no reward model, no PPO. Turns the base model into an instruction-following assistant. Initially assumed by the community to use RLHF (as described in the InstructGPT paper), but OpenAI later clarified it used the simpler FeedME approach.

- **`text-davinci-003`** (November 28, 2022) --- code-davinci-002 fine-tuned with full RLHF (SFT → RM → PPO), the complete InstructGPT methodology applied to the GPT-3.5 base. Released just 2 days before ChatGPT. Recovered in-context learning abilities that text-davinci-002 had lost through supervised fine-tuning.

### Lineage

```
GPT-3 davinci (175B, text only, June 2020)
    │
    ├──→ Codex / code-davinci-001 (fine-tuned on code, July 2021)
    │
    └──→ code-davinci-002 (pre-trained on text + code, March 2022)
             │           [GPT-3.5 BASE]
             │
             ├──→ text-davinci-002 (FeedME: SFT only, March 2022)
             │
             ├──→ text-davinci-003 (full RLHF, November 28, 2022)
             │
             └──→ ChatGPT / gpt-3.5-turbo (RLHF + dialogue, November 30, 2022)
```

## Code Training Improves Reasoning

The most important insight of the GPT-3.5 era: training on a blend of text and code made the base model fundamentally more capable at non-code tasks. code-davinci-002 and text-davinci-002 were the first models to exhibit strong chain-of-thought reasoning ability --- none of the earlier models (including text-davinci-001 / InstructGPT) demonstrated this.

The improvements showed up in:

- Chain-of-thought reasoning
- Following complex multi-step instructions
- Logical deduction
- Structured output generation

The intuition for why code helps:

- Code is highly structured --- strict syntax, clear logic flow, explicit variable tracking
- Code requires precise sequential reasoning --- each line depends on previous lines, state must be tracked
- Code has unambiguous ground truth --- it either runs or it doesn't, providing a cleaner training signal than natural language
- Programming inherently involves decomposing problems into steps --- which is exactly what chain-of-thought is

This is why GPT-3.5 felt like such a leap over GPT-3 --- it wasn't just RLHF on top, the base model itself was more capable because of code training. The RLHF (text-davinci-003) then made it better at following instructions, but the reasoning ability came from the base.

Caveat: OpenAI never published a rigorous ablation proving exactly why code training helps reasoning. This is the widely accepted explanation, primarily from Yao Fu et al.'s analysis ("How does GPT Obtain its Ability?", December 2022), supported by the observed performance gap between GPT-3 (no code) and code-davinci-002 (text + code) on reasoning benchmarks.

## FeedME vs RLHF

Two approaches to turning the base model into an assistant:

**text-davinci-002 (FeedME --- SFT only)**:

- Better at following instructions in zero-shot settings
- But lost in-context learning ability --- worse at few-shot prompting than the base code-davinci-002
- Traded versatility for instruction compliance

**text-davinci-003 (full RLHF)**:

- Better at creative and structured writing (poetry, rhyming)
- Produced longer, more detailed responses
- Recovered in-context learning that FeedME had lost
- Better zero-shot classification (~30% higher accuracy than text-davinci-002)

The alignment tax: both fine-tuning approaches improved instruction following but caused regressions on some tasks. RLHF (text-davinci-003) had a smaller alignment tax than FeedME (text-davinci-002) --- it was better at maintaining general capabilities while adding instruction following.

Link to [[llm/datasets/feedme|FeedME]] for details on the FeedME method.

## The Naming

Timeline of how "GPT-3.5" came to exist:

- **March 15, 2022**: code-davinci-002 and text-davinci-002 released on the API. Described as "new versions of GPT-3 and Codex." No "GPT-3.5" branding.
- **November 28, 2022**: text-davinci-003 released.
- **November 30, 2022**: ChatGPT launched. OpenAI's blog post described it as "fine-tuned from a model in the GPT-3.5 series" --- the first time "GPT-3.5" appeared as an official name.

The distinguishing characteristic: GPT-3 models (davinci, text-davinci-001) were trained on text only. GPT-3.5 models (code-davinci-002 and its derivatives) were trained on text + code. The code training is what makes it "3.5."

---

## Related Documents

- [[llm/models/gpt3/gpt3-to-chatgpt/overview|GPT-3 to ChatGPT Overview]] --- Full timeline
- [[llm/models/gpt3/gpt3-to-chatgpt/codex/training|Codex Training]] --- The code-only predecessor
- [[llm/models/gpt3/gpt3-to-chatgpt/instructgpt/training|InstructGPT Training]] --- The RLHF methodology applied in text-davinci-003
- [[llm/datasets/feedme|FeedME]] --- The supervised fine-tuning method used for text-davinci-002
- [[llm/models/gpt3/gpt3-to-chatgpt/chatgpt|ChatGPT]] --- Fine-tuned from this series
