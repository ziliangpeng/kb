# Transformer Architecture Styles

There are three main architecture styles built on the Transformer: encoder-only, encoder-decoder, and decoder-only. They share the same core components (Q/K/V attention, FFN, residual connections, normalization) but differ in **attention masking**, which changes what each token can see.

## The Core Difference: Masking

| Style | Masking | What each token sees |
|---|---|---|
| Encoder-only | No mask | All tokens (bidirectional) |
| Decoder-only | Causal mask | Only previous tokens (left-to-right) |
| Encoder-decoder | Encoder: no mask. Decoder: causal mask + cross-attention to encoder | Encoder is bidirectional. Decoder sees own previous tokens + full encoder output |

This is the fundamental structural difference. Everything else — Q/K/V projections, FFN, residual connections, normalization — is the same across all three.

## Encoder-Only (BERT-style)

**How it works:** Takes input, produces a rich representation of every token. Bidirectional — every token attends to every other token, including future tokens. The full L x L attention matrix is used. It sees the whole input at once.

**Cannot generate text.** It's a reader, not a writer.

**Use cases:**

- Text classification (sentiment analysis, spam detection)
- Named entity recognition
- Semantic search and retrieval (encode queries and documents into vectors, find nearest match)
- Sentence embeddings

**Key models:** BERT, RoBERTa, DeBERTa

**Why encoder-only is better for these tasks:** Bidirectional attention gives strictly richer representations for understanding a fixed input. Consider embedding "The bank by the river was steep" — the meaning of "bank" depends on "river" which comes after it. An encoder sees both simultaneously. A decoder processes "bank" before ever seeing "river," so the representation of "bank" at its own position is built without that context.

At the same parameter count, an encoder-only model will generally produce better embeddings and classifications than a decoder-only model, because bidirectional attention uses parameters more efficiently for pure understanding tasks.

**Why it didn't become the LLM:** It cannot generate text autoregressively. Its pre-training objective (masked language modeling — mask 15% of tokens, predict them) is also less natural and less efficient than next-token prediction.

## Encoder-Decoder (T5-style)

**How it works:** Two separate components. The encoder reads the full input bidirectionally (no mask). The decoder generates output autoregressively with causal masking. The decoder also has **cross-attention** layers where every decoder token can attend to every encoder position (no mask on the cross-attention).

So each decoder block has three sub-layers:

1. **Causal self-attention** — decoder attends to its own previous tokens
2. **Cross-attention** — decoder attends to the encoder's full output
3. **Feed-forward network**

**Use cases:**

- Machine translation (the original Transformer use case — encode source language, decode target language)
- Summarization (encode long document, decode short summary)
- Speech-to-text (Whisper — encode audio, decode text)
- Any task where input and output are structurally different

**Key models:** Original Transformer, T5, BART, Whisper

**Why it made sense:** When input and output are clearly separate (French → English, audio → text), having a dedicated encoder to fully digest the input bidirectionally and a separate decoder to produce the output is a natural fit.

**Why it lost to decoder-only for LLMs:**

1. **Scaling complexity.** Two separate components with different attention patterns. Harder to scale, train, and reason about than one uniform architecture.
2. **Less general.** You must decide what goes to the encoder vs. the decoder. Decoder-only avoids this — everything is one sequence.

## Decoder-Only (GPT-style)

**How it works:** Processes everything as one sequence with causal masking. Each token attends only to previous tokens (lower triangular attention matrix). Generates output one token at a time.

**Use cases:** Everything.

- Conversational AI (ChatGPT, Claude)
- Code generation
- Reasoning
- Translation, summarization, classification — all framed as "given this prefix, generate the answer"

**Key models:** GPT-2/3/4, Claude, Llama, DeepSeek, Gemini, Mistral

**Why it won:**

1. **One architecture, any task.** Frame everything as next-token prediction. Translation? Put source text in context. Classification? Put text in context and generate the label. No architectural decisions per task.
2. **Scaling laws favor it.** One simple architecture means you can pour all compute into making it bigger. Performance improves predictably with scale.
3. **Emergent abilities.** At sufficient scale, capabilities appear that nobody explicitly trained for — reasoning, chain-of-thought, in-context learning.
4. **Natural pre-training objective.** Next-token prediction on internet text is simple, self-supervised, and works on unlimited data.

## Can Decoder-Only Replace the Other Two?

Yes — decoder-only can do everything the other two do. The question is efficiency.

**Replacing encoder-only:** Decoder-only can classify and embed text, but bidirectional attention is more parameter-efficient for pure understanding tasks. A 110M encoder-only model will likely beat a 110M decoder-only model on embedding quality. At very large scale, the gap narrows but doesn't fully disappear. Encoder-only survives where cost matters — embedding billions of documents is far cheaper with a small encoder than a large decoder.

**Replacing encoder-decoder:** Decoder-only handles translation and summarization fine by putting the input in context. The input tokens are processed with causal attention (each input token only sees previous input tokens), which is theoretically worse than bidirectional encoding. In practice, at sufficient scale, this doesn't seem to matter.

## Industry Convergence

Every frontier LLM today is decoder-only: GPT-4, Claude, Llama, Gemini, DeepSeek, Mistral, Qwen.

The other architectures survive in niches:

- **Encoder-only**: embeddings, search, classification (where small/fast/cheap matters)
- **Encoder-decoder**: speech-to-text (Whisper), some specialized translation systems

For general-purpose AI, decoder-only won decisively. The simplicity of one uniform architecture that scales predictably and handles any task outweighed the theoretical advantages of specialized architectures.
