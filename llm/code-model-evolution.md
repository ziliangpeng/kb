# Code Model Evolution

The evolution of transformer-based models specialized for code, from the first code completion tools to modern code generation systems.

## 2019: First Coding Transformers

### TabNine (July 2019)

The first commercial product applying a transformer model to code. Created by Jacob Jackson (University of Waterloo student), TabNine fine-tuned **GPT-2** on approximately 2 million GitHub files for code autocompletion. It supported 22 programming languages and worked as an IDE plugin.

TabNine proved the concept: transformer language models could meaningfully assist with coding.

### CuBERT (December 2019)

Google's **CuBERT** was the first academic transformer pre-trained specifically on code. It applied BERT-style pre-training (masked language modeling + next sentence prediction) to 7.4 million Python files from GitHub. Published at ICML 2020.

As an encoder-only model, CuBERT was designed for code **understanding** tasks (bug detection, code classification) rather than code generation.

## 2020: The Encoder Era

The initial wave of code transformers was dominated by **encoder-based** (BERT-style) models focused on code understanding, plus a few smaller generative models.

### CodeBERT (February 2020)

Microsoft's bimodal pre-trained model for both natural language and programming language. Pre-trained on NL-PL pairs across 6 languages (Python, Java, JavaScript, PHP, Ruby, Go). More capable than CuBERT due to bimodal training and multi-language support. Published at EMNLP 2020.

### IntelliCode Compose / GPT-C (May 2020)

Microsoft's **GPT-2 variant** trained from scratch on 1.2 billion lines of code in Python, C#, JavaScript, and TypeScript. Deployed as a cloud-based service in VS Code. One of the first production-grade generative code models from an academic/corporate lab.

### GraphCodeBERT (September 2020)

Microsoft's follow-up to CodeBERT. Added data flow information (semantic-level structure of code) to the pre-training process, going beyond token-level understanding. Published at ICLR 2021.

### PyMT5 (October 2020)

Applied the T5 encoder-decoder architecture to Python code. Pre-trained on 26 million Python snippets with span masking. 374M parameters. Could generate methods from docstrings and vice versa. Published at EMNLP 2020.

## 2021: The Scale Breakthrough

### CodeGPT (February 2021)

Microsoft's decoder-only transformer following GPT-2 architecture, pre-trained on CodeSearchNet (Python and Java). Part of the CodeXGLUE benchmark suite. Two variants: CodeGPT (trained from scratch on code) and CodeGPT-adapted (initialized from GPT-2 checkpoint).

### GPT-J 6B (June 2021)

EleutherAI's open-source 6B parameter model. **Not code-specialized** — trained on The Pile (a general corpus that included code). Despite no code-specific training, achieved 11.6% pass@1 on HumanEval, roughly equivalent to Codex-300M (a model with 20x fewer parameters but fine-tuned on code). This demonstrated both the latent coding ability of general models and the massive efficiency gains from domain-specific fine-tuning.

### Codex (July 2021)

OpenAI's breakthrough: GPT fine-tuned on 159GB of Python code from 54 million GitHub repositories. The largest model (Codex-12B) achieved **28.8% pass@1** on HumanEval — compared to 0% for GPT-3 175B and 11.6% for GPT-J 6B.

Codex's key contribution was **scale**: previous code models were mostly encoder-based (for understanding) or small generative models (100M-400M params). Codex showed that scaling a decoder-only model to 12B parameters with massive code data produced dramatically better code generation.

A production version of Codex powered **GitHub Copilot**, launched as a technical preview on June 29, 2021. While TabNine pioneered the concept of transformer-assisted coding, Codex/Copilot was the first code-specialized transformer to achieve massive adoption — surpassing one million users within months and becoming one of the earliest commercially successful LLM products.

See [[llm/models/gpt3/gpt3-to-chatgpt/codex/architecture|Codex]] for detailed documentation.

## Key Insight: Two Eras

The pre-Codex landscape had two distinct approaches:

- **Encoder models** (BERT-style): CuBERT, CodeBERT, GraphCodeBERT — focused on code *understanding* (search, classification, bug detection)
- **Small generative models**: TabNine, IntelliCode Compose, PyMT5, CodeGPT — code *generation* at small scale (100M-400M params)

Codex bridged the gap by showing that a large-scale decoder-only model could generate functionally correct code at practically useful rates. This shifted the field toward large generative models for code.

## Post-Codex (TBD)

- AlphaCode (DeepMind, February 2022) — competitive programming
- CodeGen (Salesforce, 2022)
- StarCoder (BigCode, 2023)
- Code Llama (Meta, 2023)
- DeepSeek-Coder (2023-2024)
- And more...

---

## Related Documents

- [[llm/models/gpt3/gpt3-to-chatgpt/codex/architecture|Codex]] - Detailed documentation
- [[llm/architecture-evolution|LLM Architecture Evolution]] - General architecture timeline
- [[llm/industry-timeline|LLM Industry Timeline]] - Broader market context
