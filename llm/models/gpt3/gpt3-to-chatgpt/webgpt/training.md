# WebGPT Training

**Paper**: ["WebGPT: Browser-assisted question-answering with human feedback"](https://arxiv.org/abs/2112.09332) (Nakano et al., December 2021)

WebGPT is GPT-3 fine-tuned to answer long-form questions by browsing the web. The model operates in a text-based browser environment, issuing commands to search, navigate, and collect references, then composing answers with citations. Training uses the same four-stage RLHF pipeline later adopted by InstructGPT and ChatGPT: behavior cloning, reward modeling, reinforcement learning (PPO), and rejection sampling.

## The Task

Given a question (primarily from ELI5, the "Explain Like I'm Five" subreddit), the model must:

1. **Browse the web** to find relevant information — searching, clicking links, reading pages
2. **Collect references** by quoting passages from web pages
3. **Compose an answer** with citations to the collected references

The model operates in two phases: a **browsing phase** (search and collect evidence) followed by an **answering phase** (write the final response using collected references).

## The Browser Environment

The model interacts with a text-based web browser. At each step, it receives a text representation of the current state — the question, the current page content at the cursor position, collected quotes so far, and remaining action budget — and must output one command as plain text.

### Available Commands

| Command | Effect |
|---|---|
| `Search <query>` | Send query to Bing API, display search results |
| `Clicked on link <link ID>` | Follow a link to a new page |
| `Find in page: <text>` | Find next occurrence of text, scroll to it |
| `Quote: <text>` | If text is found on current page, add it as a reference |
| `Scrolled down <1, 2, 3>` | Scroll down 1-3 times |
| `Scrolled up <1, 2, 3>` | Scroll up 1-3 times |
| `Top` | Scroll to top of page |
| `Back` | Go to previous page |
| `End: Answer` | End browsing, move to answering phase |
| `End: <Nonsense, Controversial>` | End browsing, skip answering (question is unanswerable) |

Commands are plain text strings, not special tokens. The environment parses them deterministically — if the model outputs `Search how to train crows`, the environment extracts the query and calls the Bing API. Invalid commands (anything not matching the formats above) still count toward the action budget but are otherwise ignored.

### Why Plain Text Commands

The model's vocabulary is just GPT-3's standard vocabulary. No special action tokens were added. This works because GPT-3 already knows how to generate structured text from pre-training. The commands are human-readable strings that are simple enough for the model to learn to produce reliably through fine-tuning.

### The Quote Mechanism

When the model issues a `Quote` command, the environment checks if the quoted text exists on the current page. If found, it records:

- The quoted text
- The page title
- The domain name

These become the references attached to the final answer. The model can collect multiple quotes across multiple pages. This citation mechanism serves two purposes:

1. **For the answer**: Provides evidence supporting the response
2. **For evaluation**: Makes it possible for humans (and the reward model) to judge factual accuracy by checking whether claims are supported by citations, rather than requiring independent fact-checking

### Browsing Constraints

- **Maximum actions**: 100 browsing actions per episode (randomized between 20-100 during RL training)
- **Maximum quote length**: Limited total reference length (measured in "quote tokens")
- **Termination**: Browsing ends when the model issues `End: Answer`, hits the action limit, or hits the quote limit. At least one reference is required to proceed to answering.

### State Representation

Each step, the model sees a text block structured roughly as:

```
<Question>
How can I train the crows in my neighborhood to bring me gifts?

<Quotes>
[1] Gifts From Crows | Outside My Window (www.birdsoutsidewindow.org)
Many animals give gifts to members of their own species but crows and
other corvids are the only ones known to give gifts to humans.

<Next action>
Search results for: how to train crows to bring you gifts

<Title>
Gifts From Crows | Outside My Window|www.birdsoutsidewindow.org

<Text>
[content of current page at cursor position]

<Actions left: 96>
<Next action>
```

The model generates the next command in response to this state. After each command, the environment updates and presents a fresh state. The model has no memory of previous steps beyond what's captured in the current state summary — making each step essentially a new context window.

## Training Data

### Questions

The vast majority of questions came from **ELI5** (Explain Like I'm Five), a Reddit dataset of long-form questions. A small number from **TriviaQA** were mixed in for diversity. Questions were split into disjoint sets for BC, RM, and RL — no question appeared in more than one training stage.

### Human Demonstrations (~6,000)

Human contractors used a graphical version of the same browser environment (showing the same information in a more user-friendly interface) to answer questions. They browsed the web, collected quotes, and wrote answers. These demonstrations were recorded as sequences of (state, action) pairs.

- ~6,000 total demonstrations
- 92% for ELI5 questions
- 4% held out as validation set
- Instructions emphasized: answers should be relevant, coherent, and supported by trustworthy references

### Human Comparisons (~21,500)

For the same question, two model-generated answers (each with their own references) were shown side by side. Human labelers picked which answer was better, judging:

- **Factual accuracy** — are claims supported by the cited references?
- **Coherence** — is the answer well-organized and easy to follow?
- **Overall usefulness** — does it actually answer the question?

Ties were allowed (treated as soft 50% labels in training).

- ~21,500 total comparisons
- 98% for ELI5 questions
- ~16,000 used for RM training, ~5,500 for evaluation
- Comparisons were generated from models of various sizes, using various training methods, combined into a single dataset for data efficiency

## Stage 1: Behavior Cloning (BC)

Supervised fine-tuning on the human demonstrations. The model learns to imitate human browsing and answering behavior.

**Input**: The text-based state at each step of a demonstration
**Target**: The command the human issued at that step
**Loss**: Standard next-token prediction on the command text

Three GPT-3 sizes were fine-tuned: **760M, 13B, and 175B**.

After BC, the model can browse and answer questions — but it's limited to human-level performance at best, since it's only imitating what demonstrators did.

## Stage 2: Reward Model (RM)

A model that scores the quality of a complete answer (browsing trajectory + final response with references). Used to provide automated feedback for RL and rejection sampling.

### Architecture

Built from the BC model by removing the language model output head (which predicts next tokens) and replacing it with a **single linear layer that outputs a scalar**. Same transformer weights as BC, just a different output projection.

The RM is always the **same size** as the policy model it scores — the 175B policy used a 175B reward model.

### Input and Output

- **Input**: The complete trajectory — question, entire browsing sequence, final answer with references. All as one text sequence.
- **Output**: A single scalar score (Elo-like)

### Training

The RM learns from pairwise human comparisons using the **Bradley-Terry model**:

Given a question Q with two answers A and B where a human preferred A:

1. Forward pass: feed (Q + trajectory_A) → get score_A
2. Forward pass: feed (Q + trajectory_B) → get score_B
3. Loss: `-log(sigmoid(score_A - score_B))`

The sigmoid converts the score difference into a probability: sigmoid(score_A - score_B) = P(A is preferred over B). The loss pushes this probability toward 1 when A was actually preferred.

**What the RM actually learns**: It does not verify factual accuracy. It learns a statistical approximation of human preferences — a "vibe check" for answer quality. Answers with good citations, relevant content, and coherent structure tend to score higher because those are the patterns humans preferred. But it can be fooled by confident-sounding answers with bad sources, or by answers that have the right style without the right substance.

The citation mechanism helps: instead of judging "is this fact true?" (impossible without external knowledge), the RM implicitly learns "does this answer look well-supported by its references?" — a much more tractable pattern to learn from text alone.

### Training Details

- Trained on ~16,000 pairwise comparisons (remaining ~5,500 used for evaluation)
- Following Stiennon et al. (2020), the reward represents an **Elo score** — the difference between two scores is the logit of the probability that one is preferred
- Ties treated as soft 50% labels (cross-entropy loss assigns 0.5 probability to each ordering)

## Stage 3: Reinforcement Learning (RL)

Fine-tunes the BC model using PPO (Proximal Policy Optimization, Schulman et al. 2017) with the reward model providing the reward signal.

### How It Works

1. The BC model (now the "policy") generates a complete browsing trajectory + answer for a question
2. The reward model scores the final answer
3. PPO updates the policy to produce higher-scoring answers

### Key Details

- **KL penalty**: Added a KL divergence penalty between the RL policy and the original BC model at each token. This prevents the model from drifting too far from coherent language — without it, the model could learn to "hack" the reward model by producing outputs that score high but are nonsensical.
- **Training questions**: 90% ELI5, 10% TriviaQA
- **Answering-only episodes**: After each full browsing episode, 15 additional answering-only episodes were inserted using the same references. This improved sample efficiency by ~2x, since the paper found that "answering explained slightly more of the variance in reward model score than browsing."
- **Randomized action budget**: Maximum browsing actions sampled uniformly from 20-100, to expose the model to varying constraints.

### Why RL Helped Less Than Expected

RL provided only a modest improvement over BC alone — the 175B RL model was preferred 58% of the time over the 175B BC model. Several reasons:

- **Unpredictable environment**: The web changes, search results vary. RL has to learn a policy that works across all possible web states. Rejection sampling can try many attempts and pick the best with hindsight.
- **Same reward model**: Both RL and rejection sampling optimize the same RM. RL is more prone to **reward hacking** (overoptimizing against RM flaws).
- **Entropy reduction**: RL reduces the diversity of outputs, which hurts exploration. With rejection sampling, the model maintains the full diversity of BC and just filters for quality.

## Stage 4: Rejection Sampling (Best-of-n)

The simplest optimization method — generate n answers, score all with the reward model, pick the highest-scored one. No additional training required.

### How It Works

1. For a given question, generate **n** complete answers (each with independent browsing)
2. Score each with the reward model
3. Return the highest-scoring answer

### Why It Works So Well

The 175B best-of-64 BC model was preferred **68%** of the time over the plain 175B BC model. This outperformed RL (58%), and adding RL on top of rejection sampling provided almost no additional benefit.

The key insight: rejection sampling trades **inference-time compute** for quality. Instead of spending compute on RL training (which has diminishing returns), you spend it at inference time generating multiple candidates. For tasks with an unpredictable environment (like web browsing), having many independent attempts is more valuable than a slightly better policy.

### Compute-Efficient Configurations

The paper analyzed the trade-off between model size and number of rejection samples for a fixed inference compute budget:

- **760M best-of-4**: Smallest model, few samples
- **13B best-of-16**: Medium model, moderate samples
- **175B best-of-64**: Largest model, most samples

These three configurations sit on the Pareto frontier — each is optimal for its compute budget.

## The Full Pipeline

```
GPT-3 (760M / 13B / 175B)
  │
  ├─→ Stage 1: Behavior Cloning
  │   (supervised fine-tuning on ~6,000 human demonstrations)
  │   └─→ BC model (can browse and answer)
  │
  ├─→ Stage 2: Reward Model
  │   (BC model + scalar head, trained on ~16,000 comparisons)
  │   └─→ RM (scores answer quality)
  │
  ├─→ Stage 3: RL (optional)
  │   (PPO against RM, with KL penalty from BC)
  │   └─→ RL model (slightly improved browsing/answering)
  │
  └─→ Stage 4: Rejection Sampling
      (generate n answers, pick highest RM score)
      └─→ Best model: BC + best-of-n (RL adds minimal value)
```

**Best configuration**: BC + rejection sampling. The paper's best model was the **175B BC model with best-of-64 rejection sampling**. RL was not needed when combined with rejection sampling.

## Connection to Later Work

This four-stage pipeline (BC → RM → RL → rejection sampling) is essentially the same one used by:

- **InstructGPT** (January 2022): Same pipeline, but for general instruction following instead of web browsing. John Schulman is an author on both papers.
- **ChatGPT** (November 2022): Built on InstructGPT's approach, optimized for dialogue.

The key difference: WebGPT applied the pipeline to a specific, narrow task (browsing + QA). InstructGPT generalized it to all instructions. But the RLHF machinery — human demonstrations for BC, pairwise comparisons for RM, PPO for RL — was proven and refined here first (alongside the earlier "Learning to Summarize" work by Stiennon et al., 2020).

---

## Related Documents

- [[llm/models/gpt3/gpt3-to-chatgpt/overview|GPT-3 to ChatGPT Overview]] - Timeline and evolution
- [[llm/models/gpt3/gpt3-to-chatgpt/codex/training|Codex Training]] - Different training approach (code fine-tuning, no RLHF)
- [[llm/models/gpt3/architecture|GPT-3 Architecture]] - The base model
