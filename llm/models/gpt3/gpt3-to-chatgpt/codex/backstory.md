# Codex Backstory

## GPT-3's Accidental Discovery

When GPT-3's API launched in July 2020, developers quickly discovered it could write simple code — a capability that was never an explicit design goal. GPT-3 was trained on general internet text, which happened to include code from websites, documentation, and forums.

Web developer Sharif Shameem demonstrated GPT-3 creating web-page layouts from prompts like "a button that looks like a watermelon." John Carmack (legendary game programmer, CTO of Oculus VR) was notably unnerved: *"The recent, almost accidental, discovery that GPT-3 can sort of write code does generate a slight shiver."*

However, GPT-3's code abilities were crude. On the HumanEval benchmark (later introduced by the Codex paper), **GPT-3 scored 0%** — it could not reliably produce functionally correct programs from docstrings.

This accidental capability planted the seed: if a general text model could write simple code, what could a code-specialized model do?

## The Microsoft-GitHub-OpenAI Triangle

Codex wasn't born from pure research curiosity. Three corporate events created the perfect alignment:

**Microsoft acquired GitHub** (October 2018, $7.5 billion): Microsoft now owned the world's largest code repository — 54+ million public repositories.

**Microsoft invested $1 billion in OpenAI** (July 2019): This investment was driven by panic. Microsoft CTO Kevin Scott sent an email to CEO Satya Nadella and Bill Gates with the subject line "Thoughts on OpenAI," writing: *"As I dug in to try to understand where all of the capability gaps were between Google and us for model training, I got very, very worried"* and *"We are multiple years behind the competition in terms of ML scale."* Nadella immediately forwarded the email to his CFO, writing: *"This is why I want us to do this."* Within weeks, the $1 billion deal was signed.

**GPT-3 launched** (June 2020): Demonstrated the power of large language models and their accidental code generation ability.

The result: Microsoft had the data (GitHub), the model (OpenAI), and the strategic urgency. An AI coding assistant was the obvious product to build.

## Zaremba's Pivot from Robotics to Code

A key internal factor at OpenAI: **Wojciech Zaremba**, OpenAI co-founder, had been leading the robotics team. When OpenAI dissolved its robotics division in 2020 due to lack of accessible training data, Zaremba pivoted to leading the Codex/Copilot effort.

He explained the strategic reasoning on the Lex Fridman Podcast (#215): *"When we created robotics [systems], we thought that we could go very far with self-generated data and reinforcement learning. At the moment, I believe that pretraining [gives] model[s] 100 times cheaper 'IQ points.'"*

Code, unlike robotics, had virtually unlimited freely available training data on GitHub. The pivot made strategic sense: why struggle with scarce robotics data when 54 million repositories of code were freely available?

## Building GitHub Copilot

The development timeline reveals that **the product drove the research, not the other way around**:

- **Mid-2020**: GitHub team (including Oege de Moor) begins experimenting with GPT-3 for code. It successfully writes a JavaScript prime number function.
- **August 2020**: GitHub's fine-tuned model achieves 92% on coding exercises, 52% on real open-source Python code.
- **Early 2021**: Internal rollout at GitHub. Developers report Copilot writes ~25% of Python code in enabled files.
- **June 29, 2021**: **GitHub Copilot announced** as technical preview. Nat Friedman (GitHub CEO) tweets: *"We spent the last year working closely with OpenAI to build GitHub Copilot. We've been using it internally for months, and can't wait for you to try it out; it's like a piece of the future teleported back to 2021."*
- **July 7, 2021**: Codex paper posted to arXiv — 8 days **after** Copilot was announced.
- **August 10, 2021**: OpenAI formally announces Codex API private beta. Live demo by Greg Brockman, Ilya Sutskever, and Wojciech Zaremba, where they build a JavaScript game from natural language commands.

The Codex paper itself confirms this ordering: *"A distinct production version of Codex powers GitHub Copilot."* Copilot already existed when the paper was written.

## Product Before Paper

This is a significant departure from the GPT-1/2/3 pattern, where research papers came first and products followed later. With Codex:

1. The **business opportunity** was identified (Microsoft + GitHub + OpenAI)
2. The **product** was built (Copilot)
3. The **paper** was published to document the research

The academic paper served to formalize the methodology (especially the HumanEval benchmark and pass@k evaluation metric, which became industry standards), but the commercial product was the primary motivation.

## Why Code Was Uniquely Suited

Code turned out to be an ideal domain for LLMs:

- **Massive free training data**: 54 million public GitHub repositories
- **Objective evaluation**: Code either passes unit tests or it doesn't — unlike natural language where quality is subjective
- **High economic value**: Developer time is expensive; even modest productivity gains justify significant investment
- **Clear product pathway**: IDE plugins are a natural integration point
- **Existing demand**: TabNine (2019) and Kite (2014-2022) had already proven developers wanted AI coding assistance

## Copilot's Commercial Success

Copilot became one of the first major commercial successes of the LLM era:

- **June 2022**: Generally available at $10/month
- Rapid adoption during beta — over one million users within months
- Demonstrated that LLM-powered products could generate real revenue
- Validated the Microsoft-OpenAI partnership's commercial potential

This commercial success helped justify continued investment in larger language models and directly influenced the path toward ChatGPT.

## Legacy

Codex and Copilot established several important precedents:

- **Domain-specific fine-tuning works**: A 12B model fine-tuned on code massively outperforms a general 175B model
- **Product-first AI research**: The commercial application can drive the research, not just the other way around
- **HumanEval as standard**: The evaluation benchmark introduced in the Codex paper became the standard for measuring code generation quality
- **Code training improves general models**: The insight that training on code improves reasoning led to code being included in training data for GPT-3.5 and beyond

---

## Related Documents

- [[llm/models/gpt3/gpt3-to-chatgpt/codex/architecture|Codex]] - Technical details and model specifications
- [[llm/models/gpt3/gpt3-to-chatgpt/overview|GPT-3 to ChatGPT Overview]] - Timeline and evolution
- [[llm/code-model-evolution|Code Model Evolution]] - Broader code model landscape
- [[llm/models/gpt3/backstories|GPT-3 Backstories]] - GPT-3's context and impact
