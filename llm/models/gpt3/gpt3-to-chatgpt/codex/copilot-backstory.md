# GitHub Copilot Backstory

The story of how GitHub Copilot — the first major commercial LLM product — was built by a small team, faced internal resistance, and became a defining product of the AI era.

## The Two Creators

Two people both claim the title of "creator" of GitHub Copilot:

### Oege de Moor — The Visionary

- **Role**: VP of GitHub Next (the R&D team that incubated Copilot)
- **Background**: Oxford computer science professor at Magdalen College. Founded Semmle (a security analysis company acquired by GitHub, which became GitHub Advanced Security). After the acquisition, became VP of GitHub Next.
- **June 2020**: First person to start typing code prompts into GPT-3 during an early-access call. Per Thomas Dohmke (later CEO): *"one of our team members, Oege de Moor, started typing things into the model, and everybody else was just looking what Oege would be doing."*
- **August 2020**: The team's fine-tuned model achieves 92% on coding exercises, 52% on real open-source Python code.
- **December 2020**: Wrote an internal memo sketching the vision for what would become Copilot.
- Describes himself as "Founder of GitHub Copilot."

### Alex Graveley — The Builder

- **Role**: Principal Engineer, Chief Architect of GitHub Copilot (April 2020 - November 2022)
- **Background**: Long-time friend of Nat Friedman (GitHub CEO at the time). They co-hosted a podcast called "Hacker Medley" and both worked at Ximian earlier in their careers.
- **January 2021**: Built the first "ghost text" prototype — the inline code suggestion UX that became Copilot's signature feature.
- **Key contributions**: Ghost text prototype, block-based termination logic, naming the product "Copilot," GitHub authentication, waitlist/onboarding, server architecture, and orchestrating the OpenAI-to-Azure migration.
- Acted as PM, EM, and designer simultaneously for 1.5 years.
- Describes himself as "Creator of GitHub Copilot."

## Building Copilot: A Tiny Team

The team that built Copilot was remarkably small — roughly **10 people**. Key members included Alex Graveley and Albert Ziegler, who developed the testing harness and pulled all-nighters to get GitHub approved for participation in the Microsoft-OpenAI deal.

The development moved fast:
- **June 2020**: GPT-3 early access, first code experiments
- **August 2020**: 92% on coding exercises
- **January 2021**: First ghost text prototype
- **Early 2021**: Internal rollout; developers report Copilot writes ~25% of Python code in enabled files
- **June 29, 2021**: Public technical preview launched

Nat Friedman (GitHub CEO) tweeted at launch: *"We spent the last year working closely with OpenAI to build GitHub Copilot. We've been using it internally for months, and can't wait for you to try it out; it's like a piece of the future teleported back to 2021."*

## Internal Resistance

The path to launch wasn't smooth. According to Graveley and Hacker News discussions, **Microsoft's own AI teams actively tried to block the GitHub team's work**, pushing their own smaller, inferior models instead of OpenAI's.

This is a recurring pattern in large companies: when a small team achieves something transformative using external technology, internal teams that were bypassed push back. The GitHub team had to fight to use OpenAI's models rather than Microsoft's in-house alternatives.

## The Compensation Controversy

On **June 20, 2023**, Alex Graveley posted a viral tweet thread:

> *"My total comp for creating GitHub Copilot, from inception to GA: +20k bonus and a title bump."*
>
> *"The VP who worked most against Copilot's creation, would later tell me I didn't deserve the promo. That person is now in charge of GitHub Copilot."*
>
> *"Join a startup."*

This generated massive discussion on Hacker News. Key points from the debate:

**In Graveley's defense**: He detailed acting as PM, EM, and designer simultaneously for 1.5 years, while facing internal resistance. A $20K bonus for creating a product that became GitHub's most important revenue driver felt grossly inadequate.

**Counter-argument**: A commenter claiming to work on Copilot responded: *"He wasn't even the first person inside Microsoft to use LLMs in an IDE completion experience. The work from prototype to product is an order of magnitude more than prototype alone."*

Graveley never publicly named the VP who opposed Copilot. Based on the timeline, **Mario Rodriguez** became VP of Copilot and later Chief Product Officer at GitHub, and has done extensive press discussing Copilot's growth.

## Leadership Changes

A critical turning point: **Nat Friedman stepped down as GitHub CEO** in November 2021, replaced by Thomas Dohmke. Friedman was Graveley's close personal friend and key champion within the company. Losing that executive sponsor likely changed the internal dynamics significantly.

**Timeline of departures:**
- **November 2021**: Nat Friedman steps down as CEO
- **November 2022**: Alex Graveley leaves GitHub (founded Minion.AI)
- **March 2023**: Oege de Moor quits GitHub

De Moor's departure was more graceful. He posted:

> *"I quit GitHub. I'm proud of GitHub Copilot and GitHub Advanced Security. Leading the creation of these products was exhilarating."*

He went on to found **XBOW**, an AI offensive security company backed by Sequoia Capital.

## Credit and Legacy

The story follows a pattern common in tech:

1. **A small team builds the prototype** under a champion (Nat Friedman)
2. **The product succeeds wildly** (1M+ users, $10/month, defining product of the AI era)
3. **Leadership changes** (Friedman leaves)
4. **New leadership scales and commercializes** the product
5. **Credit shifts** to the executives who scaled it, away from the original builders

Thomas Dohmke (new CEO) and Mario Rodriguez (VP/CPO) have done extensive press about Copilot's success. The original builders — Graveley and de Moor — both left within 18 months of Friedman's departure.

## Commercial Impact

Despite the internal drama, Copilot became one of the most successful AI products ever:

- **June 2022**: Generally available at $10/month
- Over **one million users** within months of the technical preview
- **92% of Fortune 500 companies** using GitHub (with Copilot as a key selling point)
- Validated the Microsoft-OpenAI partnership's commercial potential
- Became the template for AI-assisted development tools

Copilot's success demonstrated that LLM-powered products could generate real, recurring revenue — a crucial proof point that helped justify the massive investments in GPT-4 and beyond.

---

## Related Documents

- [[llm/models/gpt3/gpt3-to-chatgpt/codex/architecture|Codex]] - The model that powers Copilot
- [[llm/models/gpt3/gpt3-to-chatgpt/codex/backstory|Codex Backstory]] - Why OpenAI built Codex
- [[llm/models/gpt3/gpt3-to-chatgpt/overview|GPT-3 to ChatGPT Overview]] - Timeline and evolution
- [[llm/code-model-evolution|Code Model Evolution]] - Broader code model landscape
