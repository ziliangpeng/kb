# GPT-2 Zero-Shot Task Performance

Paper: ["Language Models are Unsupervised Multitask Learners"](paper.pdf) (Radford et al., 2019)

## The Core Idea

GPT-2 has **no fine-tuning step**. After pre-training, the model is evaluated directly on downstream tasks — no task-specific heads, no labeled data, no weight updates. This is the fundamental shift from [[llm/models/gpt1/fine-tuning|GPT-1]], which required fine-tuning a separate model for each task.

The insight: if your training data ([[llm/datasets/webtext|WebText]]) is large and diverse enough, the model has already seen natural examples of people doing tasks — asking and answering questions, writing summaries, translating between languages. The model learns these patterns implicitly, purely from predicting the next token.

## Why This is Revolutionary

GPT-2's zero-shot capability represented a fundamental paradigm shift in how we think about training and deploying language models:

- **One model, many tasks**: Unlike GPT-1, which required training a separate fine-tuned model for each task, GPT-2 can handle multiple tasks out of the box
- **No labeled data needed**: Eliminates the bottleneck of collecting thousands of task-specific labeled examples
- **No gradient updates**: Tasks are performed purely through clever prompting, not through weight updates
- **Deployment simplicity**: Ship one model that works on any task, rather than managing dozens of specialized models

This challenged the prevailing wisdom in NLP at the time: **you don't need task-specific training if your pre-training is good enough**. The entire supervised learning pipeline—collecting labeled data, fine-tuning, evaluating, deploying—could potentially be replaced by just writing a good prompt.

The implications were profound: if zero-shot works at 1.5B parameters, what happens at 10B? 100B? This directly motivated the scaling experiments that led to GPT-3.

## Task Conditioning Through Text

GPT-1 specified tasks through architecture: special delimiter tokens (`[Start]`, `$`, `[Extract]`), task-specific linear heads, and input transformations.

GPT-2 specifies tasks through text. The paper formalizes this: instead of modeling `p(output | input)` (which is task-specific), model `p(output | input, task)` — where the task description is part of the input text itself. The task is in the text, not in the architecture.

This works because WebText naturally contains examples of task-like patterns: Reddit posts with `TL;DR:` summaries, Q&A threads, bilingual text, reading comprehension passages, and more. The model doesn't know it's "doing a task." It's just predicting the next token, same as during pre-training.

## Task-by-Task Examples

### 1. Language Modeling

The "home task" — literally what the model was trained to do. Feed it text, measure how well it predicts the next token (perplexity).

```
Input:  "The cat sat on the"
Output: "mat"
```

**Result**: SOTA on 7 out of 8 standard language modeling benchmarks, zero-shot.

### 2. Children's Book Test (CBT)

Task: predict a missing word in a passage. The model scores each candidate word by its probability given the context, and picks the highest.

```
Input: "Alice was beginning to get very tired of sitting by her
sister on the bank. She had peeped into the book her sister was
reading, but it had no pictures in it. 'What is the use of a
book,' thought Alice, 'without pictures or ___'"

Candidates: [conversations, pictures, Alice, sister, bank, ...]

Model computes: p("conversations" | context), p("pictures" | context), ...
Picks highest → "pictures"
```

No fine-tuning — just using next-token probabilities as a scoring function.

**Result**: 93.3% on common nouns, 89.1% on named entities (new SOTA).

### 3. LAMBADA

Task: predict the final word of a sentence that requires at least 50 tokens of context.

```
Input: "She had been paying close attention to the whole story,
and when he finished, she asked about the part where the hero
nearly died. 'That was my favorite part too,' said"

Model predicts: "she"
```

Interesting finding: most of GPT-2's errors were valid continuations of the text — the model didn't understand the constraint that it must predict the *final* word specifically. Adding a stop-word filter boosted accuracy from 52.66% to 63.24%.

**Result**: Perplexity improved from 99.8 to 8.6 (new SOTA). Accuracy: 63.24% (new SOTA).

### 4. Winograd Schema Challenge

Task: resolve ambiguous pronouns. The model scores each resolution by probability and picks the more likely one.

```
Sentence: "The trophy doesn't fit in the suitcase because it is too big."

Score: p("The trophy is too big.")   → higher
Score: p("The suitcase is too big.") → lower

Answer: "it" refers to the trophy
```

**Result**: 70.70% accuracy (+7% over previous SOTA).

### 5. Reading Comprehension (CoQA)

Task: answer questions about a document. Feed the document, conversation history, and an `A:` prompt. The model generates the answer via greedy decoding.

```
Input: "The 2018 Winter Olympics were held in Pyeongchang, South
Korea. Norway led the medal count with 39 total medals, followed
by Germany with 31.

Q: Where were the 2018 Winter Olympics held?
A: Pyeongchang, South Korea.
Q: Who led the medal count?
A: Norway.
Q: How many medals did they win?
A:"

Model generates: " 39 total medals."
```

The `A:` token is the task signal — the model has seen Q&A formatted this way in web text.

**Result**: 55 F1 — matched or exceeded 3 out of 4 supervised baselines that were trained on 127,000+ labeled examples. Zero-shot vs 127K labeled examples, and GPT-2 was competitive.

### 6. Summarization (CNN/Daily Mail)

Task: summarize an article. Append `TL;DR:` — a pattern common on Reddit where users summarize long posts.

```
Input: "[Full news article about a car crash in downtown Chicago
that injured 3 people, involved 2 vehicles, and closed traffic
for 4 hours...]

TL;DR:"

Model generates: "A car crash in downtown Chicago injured three
people and closed traffic for several hours."
```

`TL;DR:` is the task specification. Removing it dropped ROUGE scores by 6.4 points — proof the model understood it as a summarization signal.

**Result**: ROUGE scores only slightly above a random-3-sentences baseline. Not competitive with supervised models, but demonstrated the model understood the task concept.

### 7. Translation (WMT-14 English-French)

Task: translate between languages. Condition on example pairs using `=` as delimiter.

```
Input: "I love you = Je t'aime
Hello, how are you? = Bonjour, comment allez-vous?
The weather is nice today = Le temps est beau aujourd'hui
Where is the nearest hospital ="

Model generates: "Où est l'hôpital le plus proche"
```

This is technically few-shot (providing examples in the prompt), not pure zero-shot. Surprisingly, it worked at all — OpenAI deliberately filtered non-English content from WebText, and only ~10MB of French text remained.

**Result**: 5 BLEU (En→Fr), 11.5 BLEU (Fr→En). Rudimentary, but the model picked up translation from minimal bilingual exposure.

### 8. Question Answering (Natural Questions)

Task: answer factoid questions. Seed with example Q&A pairs to teach the format.

```
Input: "Q: Who wrote the origin of species?
A: Charles Darwin
Q: Who is the founder of the ubuntu project?
A: Mark Shuttleworth
Q: Who came up with the theory of relativity?
A:"

Model generates: "Albert Einstein"
```

The model answers purely from knowledge stored in its weights during pre-training. No retrieval, no database — just what it "memorized" from WebText.

**Result**: 4.1% exact match overall. But on the 1% of questions the model was most confident about, accuracy was 63.1% — it knew what it knew. Fun footnote from the paper: Alec Radford tested himself on the same questions and got 17 out of 100 correct.

## The Scaling Story

The paper evaluated 4 model sizes: **124M, 355M, 774M, and 1.5B parameters**. Across all tasks, performance scaled log-linearly with model size—every task improved as models grew larger, with no signs of saturation.

Specific examples:

**Children's Book Test (Common Nouns)**:
- 124M: 83.4%
- 355M: 87.1%
- 774M: 88.8%
- 1.5B: **93.3%** (new SOTA)

**LAMBADA (accuracy)**:
- 124M: 42.3%
- 355M: 51.2%
- 774M: 54.3%
- 1.5B: **63.2%** (with stop-word filter)

**Winograd Schema Challenge**:
- 124M: 62.9%
- 355M: 65.4%
- 774M: 67.3%
- 1.5B: **70.7%** (new SOTA)

**Reading Comprehension (CoQA F1)**:
- 124M: 38
- 355M: 46
- 774M: 50
- 1.5B: **55** (competitive with supervised baselines)

Every task followed this pattern. No task plateaued at 1.5B. And critically, all model sizes still underfit WebText—the training loss continued to decrease, suggesting the models hadn't fully absorbed the knowledge in the training data.

The paper's conclusion: "performance on these tasks depends on model capacity" and larger models would likely yield further gains. This **scaling hypothesis** directly foreshadowed GPT-3: if bigger models always do better, and current models haven't saturated the data, then the obvious next step is to scale up dramatically (which OpenAI did, jumping from 1.5B to 175B).

## Where GPT-2 Excelled

Tasks where zero-shot GPT-2 matched or exceeded supervised baselines:

- **Language modeling**: SOTA on 7 out of 8 benchmarks (Penn Treebank, WikiText, etc.)
- **Children's Book Test**: 93.3% common nouns, 89.1% named entities (new SOTA)
- **LAMBADA**: Perplexity 8.6 (new SOTA), accuracy 63.2% (new SOTA)
- **Winograd Schema Challenge**: 70.7% (new SOTA, +7% over previous best)
- **Reading comprehension (CoQA)**: 55 F1 (matched 3 out of 4 supervised baselines trained on 127K examples)

These results demonstrated that for tasks involving pattern recognition, commonsense reasoning, and language understanding, zero-shot performance was surprisingly competitive.

## Limitations

The paper was honest about where zero-shot struggled:

- **Summarization**: ROUGE scores barely above extractive baselines (random 3 sentences); often confused specific details or generated generic summaries
- **Translation**: 5 BLEU (En→Fr) and 11.5 BLEU (Fr→En) far below neural MT systems (typically 35-40 BLEU); minimal bilingual data in WebText (~10MB French)
- **Question answering**: 4.1% exact match on Natural Questions vs 30-50% for retrieval-based systems; model lacked comprehensive factual knowledge
- **Task ambiguity**: Zero-shot relies on vague hints like `TL;DR:` or `A:`—the model sometimes misunderstood the task format

The paper concluded: "the zero-shot performance of GPT-2 is still far from use-able" for most practical tasks. The results were a proof of concept, not a production system. Tasks requiring precise factual recall, complex reasoning over multiple steps, or exposure to non-English languages remained challenging.

## Impact on the Field

GPT-2's zero-shot capability had far-reaching consequences:

- **Launched prompt engineering**: Showed that task specification through natural language (like `TL;DR:`) could replace architectural modifications, spawning the field of prompt design
- **Validated scaling laws**: Demonstrated log-linear improvement across 4 orders of magnitude (124M → 1.5B), suggesting continued scaling would yield better results
- **Questioned fine-tuning necessity**: Challenged the assumption that task-specific training is required for good performance
- **Enabled API-first models**: Made it practical to deploy one general model accessible via API, rather than distributing fine-tuned checkpoints
- **Safety concerns**: GPT-2's text generation quality raised concerns about synthetic text and disinformation, leading to OpenAI's staged release strategy
- **Inspired GPT-3**: The clear scaling trend and lack of saturation directly motivated the 100x scale-up to 175B parameters

The paradigm shift from "pre-train then fine-tune" to "just pre-train well enough" became the foundation for modern LLM development.

## The Progression: GPT-1 → GPT-2 → GPT-3

GPT-2's zero-shot approach is the conceptual bridge in a three-step evolution:

| | [[llm/models/gpt1/fine-tuning\|GPT-1]] (2018) | GPT-2 (2019) | GPT-3 (2020) |
|---|---|---|---|
| **Paradigm** | Pre-train + fine-tune | Zero-shot | Few-shot (in-context learning) |
| **Task specification** | Special tokens + linear head | Natural language hints | Examples in the prompt |
| **Per-task parameters** | Yes (linear head) | None | None |
| **Per-task training** | Yes (3 epochs on labeled data) | None | None |
| **Per-task labeled data** | Required | Not required | Not required (a few examples help) |

GPT-2 proved the concept: tasks can emerge from pre-training alone. GPT-3 refined it: a few examples in the prompt dramatically boost performance without any weight updates.

### An Important Clarification

The table above can be misleading. It's not that GPT-2 "does zero-shot" and GPT-3 "does few-shot" as if they are different capabilities. GPT-3 can do zero-shot too — and better than GPT-2 at it. The GPT-3 paper actually evaluated all three settings: zero-shot, one-shot, and few-shot.

The difference is in what each paper *chose to emphasize*:

- **GPT-2's contribution**: proved that zero-shot task performance is possible at all. The paper deliberately tested only zero-shot to make the strongest claim — you don't need any fine-tuning.
- **GPT-3's contribution**: systematically showed that putting a few examples in the prompt (few-shot) dramatically improves over zero-shot, without any weight updates. This is what they called "in-context learning."

Few-shot helps for an intuitive reason: giving the model a couple of examples clarifies exactly what format and behavior you want. Zero-shot relies on the model guessing the right format from a vague hint like `TL;DR:` or `A:`. Few-shot removes that ambiguity.

GPT-3 didn't lose zero-shot ability — it gained few-shot ability on top. Each generation expanded the range of what's possible without task-specific training.
