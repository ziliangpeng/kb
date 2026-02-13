# Chat API & ChatML

## The Problem

Before ChatGPT's API, there was only the **Completions** endpoint — you sent a raw text string and the model continued it. For multi-turn conversation, developers manually formatted prompts (e.g., stuffing `User: ...\nAssistant: ...` into the text). There was no standard format.

## ChatML (Chat Markup Language)

OpenAI invented ChatML as the **token-level format** for encoding multi-turn conversations. It was announced on **March 1, 2023**, alongside gpt-3.5-turbo — not with ChatGPT itself (November 2022). ChatGPT launched as a web-only product with no API.

### The Format

ChatML uses special tokens to delimit messages:

```
<|im_start|>system
You are a helpful assistant.<|im_end|>
<|im_start|>user
What's the capital of France?<|im_end|>
<|im_start|>assistant
Paris.<|im_end|>
```

- `<|im_start|>` and `<|im_end|>` are **single special tokens** in the vocabulary, not character sequences — users cannot inject them through normal text
- `im` stands for "imaginary monologue" (per some OpenAI documentation; sources conflict — some say "input message")
- The specification was labeled **"ChatML v0"**

### Documentation History

The specification lived as `chatml.md` in the [`openai-python`](https://github.com/openai/openai-python/blob/v0.28.1/chatml.md) GitHub repo. It was removed when the library was rewritten for v1.0. By August 2023, OpenAI announced they would stop documenting changes to the internal format. There was no standalone blog post — ChatML was part of the gpt-3.5-turbo launch announcement.

## The Chat Completions API

The new endpoint (`/v1/chat/completions`) replaced the old Completions endpoint (`/v1/completions`). Instead of sending a raw text prompt, developers send structured messages:

```json
{
  "messages": [
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": "Hello"},
    {"role": "assistant", "content": "Hi! How can I help?"},
    {"role": "user", "content": "What's 2+2?"}
  ]
}
```

The API is **stateless** — each request sends the full conversation history. "Memory" is just concatenating prior messages into context. The 4,096 token limit at launch meant conversations had to be short or older messages dropped.

### Key Implications

- **Standardized multi-turn format** — everyone uses the same structure instead of ad-hoc prompt engineering
- **Role separation** — the model can distinguish developer instructions (system) from user input, which matters for safety
- **Backward-incompatible** — all models from gpt-3.5-turbo onward are chat-only. The old completions endpoint was eventually deprecated. By July 2023, **97% of API usage** had moved to chat

## Industry Adoption: Two Layers

The Chat API's influence on the industry splits into two distinct layers with very different adoption stories.

### Layer 1: API Format (Strong Convergence)

The JSON messages array (`{"role": ..., "content": ...}`) became the **de facto industry standard**. Nearly every provider and inference tool adopted it:

- **Inference frameworks**: vLLM, Ollama, LM Studio, SGLang all expose "OpenAI-compatible" endpoints
- **Cloud providers**: Together AI, Fireworks, Groq offer OpenAI-compatible APIs
- **Other labs**: Anthropic and Google use structurally similar formats (with minor differences — e.g., Anthropic has `system` as a separate API parameter, Google uses `"model"` instead of `"assistant"`)

### Layer 2: Token-Level Templates (No Convergence)

Every model family uses **different special tokens** internally to encode conversations:

| Model Family | Token Format |
|---|---|
| OpenAI (GPT) | `<\|im_start\|>` / `<\|im_end\|>` (ChatML) |
| Qwen, Yi | `<\|im_start\|>` / `<\|im_end\|>` (adopted ChatML) |
| Llama 3 | `<\|start_header_id\|>` / `<\|end_header_id\|>` / `<\|eot_id\|>` |
| Mistral | `[INST]` / `[/INST]` |
| DeepSeek | `<\|User\|>` / `<\|Assistant\|>` / `<\|end_of_sentence\|>` |
| Claude (legacy) | `\n\nHuman:` / `\n\nAssistant:` |

ChatML's `im_start`/`im_end` tokens were directly adopted by **Qwen** (Alibaba) and **Yi** (01.AI), plus community fine-tunes like **OpenHermes**. But Llama, Mistral, and DeepSeek all invented their own formats.

### The Glue: HuggingFace Chat Templates

HuggingFace standardized a **meta-layer** — a Jinja-based `chat_template` field in each model's `tokenizer_config.json`. This doesn't standardize the tokens themselves, but standardizes how templates are *described and applied*.

The practical architecture that emerged:

1. **Application layer** — developers write code using the OpenAI-compatible messages format
2. **Serving layer** — inference engines (vLLM, Ollama) expose OpenAI-compatible endpoints
3. **Template layer** — the serving engine reads the model's HuggingFace `chat_template` (Jinja)
4. **Token layer** — the Jinja template produces the model-specific token sequence
