# GPT-1 Backstories

Things you can't learn from just reading the paper.

## The Origin Story: The Sentiment Neuron

GPT-1's first author, **Alec Radford**, joined OpenAI in 2016 with just a bachelor's degree from Olin College — no PhD, no master's. He described joining OpenAI as "similar to joining a graduate program."

His first attempt was training a language model on **2 billion Reddit comments**. It failed. Greg Brockman (OpenAI's president) told him "No problem, try again." Due to limited compute, Radford pivoted to a single domain: Amazon product reviews.

The result was the **Sentiment Neuron** paper (April 2017). He trained a character-level LSTM on 82 million Amazon reviews, just predicting the next character. The stunning discovery: a **single neuron** in the model had spontaneously learned to represent sentiment with state-of-the-art accuracy (91.8%).

This was the intellectual seed for GPT-1: if predicting the next character can produce a sentiment classifier for free, what else might a bigger model learn?

Radford is notably introverted and rarely appears in public. Sam Altman has called him an "Einstein-level genius." His papers have over 190,000 citations. He left OpenAI in late 2024 to pursue independent research.

## Never Peer-Reviewed

GPT-1 was **never submitted to a conference or journal**. It was released as a technical report on OpenAI's website, labeled "Preprint. Work in progress." It's not even on arXiv.

This was unusual — landmark NLP papers of that era went through venues like ACL, EMNLP, or NAACL. ELMo won Best Paper at NAACL 2018; ULMFiT was published at ACL 2018. GPT-1 just appeared on a blog.

This set a pattern that OpenAI continued with GPT-2, GPT-3, and GPT-4 — increasingly moving away from traditional academic publishing. In hindsight, this non-peer-reviewed technical report turned out to be more influential than most peer-reviewed papers in history.

## The Community Reaction: Underwhelmed

The [Hacker News thread (June 12, 2018)](https://news.ycombinator.com/item?id=17286810) captures the immediate reaction:

- **Jeremy Howard** (fast.ai / ULMFiT) praised it but framed it as an advance over ULMFiT. He presciently noted "there's almost no reason for anyone else to create their own model from scratch."
- Others called it **"not that novel"** — essentially "just replacing word vectors with a pre-trained model."
- One commenter found the "1 month on 8 GPUs" cost psychologically daunting.
- Another pointed out ULMFiT achieved comparable results in "~5 hours on my GTX1070."

**Nobody in the thread predicted this would be the beginning of the most transformative series of AI models in history.**

## BERT Stole the Spotlight

BERT was released in October 2018, just ~4 months after GPT-1, and completely overshadowed it.

The community reaction to BERT was dramatically different:
- "So many projects were dropped on the floor when BERT was released" — Sam Bowman (NYU)
- A flurry of "BERTology" papers followed — everyone was writing about BERT
- GPT-1 was referred to as "a lesser-known model from OpenAI"
- The consensus was: "Transformers aren't going to get much better than BERT"

The key debate was **bidirectional (BERT) vs unidirectional (GPT)**. BERT's bidirectional attention seemed obviously superior. GPT's forward-only approach was seen as "a step backward from ELMo's bidirectional approach."

**The irony**: The community bet on BERT's encoder architecture. History proved that GPT's decoder-only approach was the one that would scale to billions of parameters and dominate the field. Encoder-only models cannot generate text, cannot be prompted, and turned out to be a dead end for the most impactful applications.

## NLP's ImageNet Moment

Sebastian Ruder wrote an influential blog post in July 2018 titled ["NLP's ImageNet Moment Has Arrived"](https://www.ruder.io/nlp-imagenet/), grouping GPT-1 with ELMo and ULMFiT as three approaches that proved transfer learning works for NLP.

His prediction: "It is very likely that in a year's time NLP practitioners will download pretrained language models rather than pretrained word embeddings." This turned out to be exactly right.

But nobody singled out GPT as the one that would matter most.

## GPT-1 Birthed Hugging Face

GPT-1 was originally implemented by OpenAI in **TensorFlow**. Thomas Wolf (Hugging Face co-founder) reimplemented it in **PyTorch**, which was gaining popularity in the research community for being more intuitive. The community response was overwhelming. When Google released BERT, they quickly converted that too, then merged their GPT-1 and BERT code into a single library — which became the **Transformers library**.

This library, born from a GPT-1 reimplementation, is now arguably the most important piece of open-source infrastructure in all of AI.

## Sutskever's Scaling Conviction

Ilya Sutskever, GPT-1's last author, had what colleagues described as a "religious level of belief in scaling laws" from the very beginning. His conviction: "If you have a large dataset and you train a very big neural network, then success is guaranteed!"

GPT-1 at 117M parameters was modest, but the architecture was chosen with scaling in mind. The decoder-only design was simpler and more scalable than encoder-decoder alternatives. This was intentional.

## What GPT-1 Got Wrong

Looking back, several design choices were later superseded:

- **The fine-tuning paradigm**: GPT-1 assumed you'd always fine-tune for each task. GPT-2 showed you could skip fine-tuning; GPT-3 showed prompting alone could work.
- **Task-specific input transformations**: The elaborate schemes for restructuring different task inputs were inelegant and later abandoned in favor of simply prompting.
- **Unidirectional limitation**: For the NLU benchmarks of the era, BERT's bidirectional approach was genuinely better. GPT's approach only "won" when models got big enough that the limitation stopped mattering.
- **Scale**: 117M params and 512 context — Karpathy later described GPT-1 as a model that "barely generates coherent text."

## The "GPT" Name

"Generative Pre-trained Transformer" — purely descriptive, each word maps to a technical component. No dramatic naming story. The model wasn't even called "GPT-1" at the time; it was just "GPT." The "-1" was applied retroactively after GPT-2 was released.

## The BooksCorpus Controversy

GPT-1's popularity (along with BERT, which also used BooksCorpus) brought scrutiny to its training data. Researchers discovered that [[llm/datasets/bookscorpus|BooksCorpus]] — ~7,000 self-published books scraped from Smashwords — had serious problems: over 200 books explicitly prohibited redistribution, thousands of duplicates existed, and authors were never asked for consent.

Both foundational language models (GPT-1 and BERT) shared this legally questionable dataset. The controversy became a precursor to the much larger copyright debates that would erupt around later models trained on web-scale data.

## Retrospective: Nobody Saw It Coming

The NLP community was astonished by GPT-3 in 2020, not by GPT-1 in 2018. GPT-1 was received as an interesting contribution among several, not as the beginning of a revolution.

- "Looking back, these things seem obvious in hindsight but were hard to know ahead of time." — Jason Wei (Google Brain / OpenAI)
- "Everyone concluding, 'No, they're clearly just a flash in the pan'" — R. Thomas McCoy (Yale)
- "I didn't realize that if you trained that very [conceptually wrong] model with sufficient data, it could excel." — Ray Mooney (UT Austin)

The revolution was only recognized retroactively.
