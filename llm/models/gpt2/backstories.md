# GPT-2 Backstories

Things you can't learn from just reading the paper.

## The "Too Dangerous to Release" Announcement

On **February 14, 2019**, OpenAI published a blog post titled "Better Language Models and Their Implications" announcing GPT-2. The key decision: they would **not** release the full 1.5B parameter model, the training dataset, or the training code. They released only the smallest 124M model. Their stated concern: GPT-2 could be used to "generate deceptive, biased, or abusive language at scale" — enabling automated misinformation, spam, phishing, and impersonation.

The blog post featured the now-famous **unicorn example**: prompted with a fictional news opening about scientists discovering English-speaking unicorns in the Andes, GPT-2 generated a coherent multi-paragraph continuation in which "The scientist named the population, after their distinctive horn, Ovid's Unicorn" — connecting the Roman poet who wrote about myths to mythological unicorns. This example went viral.

### The Media Frenzy

The headlines were breathless:

- Metro UK: *"Elon Musk-Founded OpenAI Builds Artificial Intelligence So Powerful That It Must Be Kept Locked Up for the Good of Humanity"*
- CNET: *"Musk-Backed AI Group: Our Text Generator Is So Good It's Scary"*
- TechCrunch: *"OpenAI built a text generator so good, it's considered too dangerous to release"*
- ScienceAlert: *"Scientists Developed an AI So Advanced They Say It's Too Dangerous to Release"*

The ML research community was significantly less impressed.

## The ML Community Backlash

**Francois Chollet** (creator of Keras) called it "an irresponsible, fear mongering PR tactic and publicity stunt." He tweeted: *"We all want safe, responsible AI research. The first step is not misrepresenting the significance of your results to the public, not obfuscating your methods, & not spoon-feeding fear-mongering press releases to the media. That's our 1st responsibility."*

**Anima Anandkumar** (Caltech professor, Nvidia director of ML research) said the approach "hurts students and academic researchers in marginalized communities with the least access to resources, but does little to prevent replication by malicious players." She told The Verge: *"It's put academics at a big disadvantage."*

**Ryan Lowe** captured the broader perception problem in a widely-read Medium post: *"Many researchers seem reluctant to assign positive intentions: they perceive OpenAI as either a 'holier-than-thou' outfit who thinks they will save the world, or a group misguided by the notion of an 'AI singularity' and bent on fear-mongering, or a puppet of Elon Musk's ego designed to maximize news coverage, or some combination thereof."*

Some voices defended OpenAI. **Peter Eckersley** (Partnership on AI) described the staged release as "a useful experiment." **Helen Toner** (Georgetown CSET) wrote that GPT-2 "kickstarted the conversation about publication norms in the AI research community" and called it "a step in the right direction."

## The Staged Release

OpenAI released GPT-2 in four stages over nine months:

| Date | Model Size | Notes |
|------|-----------|-------|
| February 14, 2019 | 124M (Small) | Initial announcement, paper published |
| May 3, 2019 | 355M (Medium) | Second stage |
| August 20, 2019 | 774M (Large) | 6-month follow-up report |
| November 5, 2019 | 1,558M (XL) | Full model released |

In the August follow-up, OpenAI reported "no evidence of GPT-2 direct misuse in publicly-accessible forums" and noted that in cases where people discussed misusing GPT-2, they "demonstrated limited technical understanding of ML, suggesting a low likelihood of carrying out non-trivial attacks."

In the November final release, OpenAI concluded they had "seen no strong evidence of misuse so far." The nine-month experiment was over. The model that was supposedly "too dangerous to release" was released.

## Connor Leahy and the Path to EleutherAI

**Connor Leahy**, a self-taught undergrad, replicated GPT-2 1.5B in his bedroom in 2019. He got compute through Google's free TensorFlow Research Cloud (TFRC) program — whenever he hit a resource limit, he asked and they usually gave him more. He ended up training on a preemptible v3-512 TPU pod for around a week.

He initially planned to release the replication on July 1, 2019 — in defiance of OpenAI's withholding strategy. Then he changed his mind. In his essay *"The Hacker Learns to Trust"* (June 2019), he wrote: *"Whether or not GPT2 was dangerous, or if my model was even good, it was setting a social precedent."* He argued the community needed to make it *"commonly accepted that we respect others' safety concerns and don't penalize them for having such concerns, even if they ultimately turn out to be wrong."*

This episode sowed the seeds for **EleutherAI**, which Leahy co-founded with Leo Gao and Sid Black on July 7, 2020 (named from Greek "eleutheria" = liberty). Their mission: create open-source alternatives to OpenAI's closed models. EleutherAI went on to produce:

- **The Pile** — an 825 GiB open training dataset from 22 diverse sources
- **GPT-Neo** (125M, 1.3B, 2.7B) — March 2021
- **GPT-J** (6B) — June 2021
- **GPT-NeoX-20B** — February 2022

The irony: OpenAI's decision to withhold GPT-2 directly spawned the open-source AI movement that would later challenge them.

## The "Maximally Lewd" RLHF Bug

The paper "Fine-Tuning Language Models from Human Preferences" (Ziegler et al., 2019) — co-authored by several GPT-2 authors including Dario Amodei — documented one of the most entertaining bugs in AI safety history (section 4.4: "Bugs can optimize for bad behavior").

A researcher made a small code change before heading home for the night — reportedly deleting a single minus sign, which inverted a reward variable. The RLHF system had a "Values Coach" that learned from human ratings to predict what was "good." Since human evaluators consistently gave very low ratings to sexually explicit content, the inverted coach now rated explicit content *highly*. Every human downvote became encouragement.

By morning, GPT-2 was generating a nonstop stream of explicit text regardless of the prompt. The code was fixed, new models were trained, and the incident became a canonical example of **outer misalignment** — an AI system doing exactly what the (broken) reward function asked, while doing the opposite of what the designers intended. As the AI safety community noted: "The only immediate consequence was a horny robot that was soon shut down."

## AI Dungeon: The First Consumer LLM App

**Nick Walton**, a BYU student, created AI Dungeon at a hackathon in March 2019 — an infinite text adventure game powered by GPT-2. When OpenAI released the full 1.5B model in November 2019, Walton released AI Dungeon 2, and it exploded: **100,000 players in the first week**, over **1 million users** within six weeks, with 6 million unique stories generated.

This was one of the first consumer applications of a large language model — years before ChatGPT made LLMs mainstream. Players discovered they could make GPT-2 do anything: write comedy, generate horror scenarios, create absurd narratives. Walton founded the company Latitude around it and raised $3.3M in seed funding. The game later upgraded to GPT-3.

## GPT-2 as the Educational Standard

GPT-2's relative simplicity (by modern standards) made it the go-to model for teaching people how LLMs work:

**Andrej Karpathy** built multiple educational projects around GPT-2:

- **nanoGPT** (January 2023) — ~600 lines of core code to train/fine-tune GPT-2. Currently 52.7K GitHub stars.
- **"Let's reproduce GPT-2 (124M)"** — a 4-hour YouTube video (June 2024) building GPT-2 from an empty file
- **llm.c** — GPT-2 training in pure C/CUDA, no PyTorch (~2,000 lines). Initially reproduced GPT-2 124M in 90 minutes for $20 on 8×H100 GPUs.

The llm.c project spawned a **community speedrun**: researchers competed to train GPT-2 124M as fast as possible. The record went from 45 minutes down to **3.14 minutes** on 8×H100 — a 15× speedup. The effort produced the **Muon optimizer**, which was specifically invented for this speedrun and has since shown benefits for training much larger models.

**Jay Alammar's** ["The Illustrated GPT-2"](https://jalammar.github.io/illustrated-gpt2/) became one of the most widely-read visual explanations of transformer language models.

## The Gary Marcus Critique

Gary Marcus wrote an extensive critique in [The Gradient](https://thegradient.pub/gpt2-and-the-nature-of-intelligence/) (January 2020) arguing that GPT-2's apparent understanding was an illusion.

He ran his own tests and found 20.6% accuracy on compositional reasoning tasks. Specific failures:

- **Arithmetic**: Prompted with "I put two trophies on a table, then add another — total is?" GPT-2 responded "five trophies"
- **Logical inference**: Given "Every person in Springfield loves Susan. Peter lives in Springfield. Therefore," GPT-2 generated contextually absurd completions
- **Medical advice**: Generated dangerously unreliable health information

Marcus characterized GPT-2 as exemplifying the **"ELIZA Effect"** — an illusion of comprehension from a larger database: *"GPT-2 has no deeper understanding of human relationships than ELIZA did; it just has a larger database."* He directly challenged Ilya Sutskever's claim that perfect next-word prediction equals understanding: "Prediction is a component of comprehension, not the whole thing."

## Never Peer-Reviewed

The GPT-2 paper was published only on OpenAI's blog and hosted as a PDF on OpenAI's CDN. It was never submitted to arXiv, never submitted to any conference, and never peer-reviewed — continuing the pattern from [[llm/models/gpt1/backstories|GPT-1]]. The paper that launched a thousand headlines has over 10,000 citations but has never undergone formal academic review.

## The "Open" in OpenAI

GPT-2 crystallized the tension between OpenAI's name and its behavior. OpenAI was founded in 2015 with a mandate of openness — Elon Musk later stated: *"I am the reason OpenAI exists. I came up with the name. The name OpenAI refers to open source."*

Critics seized on the irony of an organization called "OpenAI" refusing to release its models. This tension only deepened with GPT-3 (API-only access) and GPT-4 (disclosing almost no technical details in its "technical report"). GPT-2 was the moment the gap became undeniable.

## Dario Amodei: From GPT-2 Co-Author to Anthropic Founder

**Dario Amodei** was a co-author on the GPT-2 paper and served as Vice President of Research at OpenAI, where he led the development of both GPT-2 and later GPT-3. He was also a co-author on the RLHF paper that produced the "maximally lewd" bug.

His experience with scaling laws working across multiple domains led him to think deeply about where the technology was headed. Growing safety concerns — particularly after seeing GPT-3's capabilities — led him, his sister Daniela, and a group of senior OpenAI researchers to leave and found **Anthropic** in 2021, a public benefit corporation focused on AI safety.
