# xAI Overview

Founded July 2023 by Elon Musk. Stated mission: build AI that is "maximally truth-seeking" and focused on understanding the universe. Headquartered in San Francisco, with primary compute infrastructure in Memphis, Tennessee.

## Founding Story

The origins trace back over a decade:

- **2012**: Musk and DeepMind co-founder Demis Hassabis discuss AI existential risk
- **2013**: Musk's birthday party — debates with Larry Page about AI safety (Page dismissed concerns as "sentimental nonsense")
- **2014**: Google acquires DeepMind (Musk tried to block it)
- **December 2015**: Musk co-founds OpenAI as a safety-focused counterweight
- **February 2023**: Musk publicly disassociates from OpenAI after its Microsoft partnership
- **March 9, 2023**: xAI incorporated
- **July 12, 2023**: xAI officially announced

Igor Babuschkin described the founding: he and Musk "talked for hours about AI and what the future might hold" and "both felt that a new AI company with a different kind of mission was needed."

## The 12 Co-Founders

| Name | Previous Affiliation | Background |
|------|---------------------|------------|
| **Elon Musk** | Tesla, SpaceX, OpenAI co-founder | CEO |
| **Igor Babuschkin** | DeepMind, OpenAI, CERN | Chief Engineer. Departed Aug 2025. |
| **Christian Szegedy** | Google (13 years) | Creator of Inception/GoogLeNet. Departed Feb 2025. |
| **Jimmy Ba** | University of Toronto | Co-author of Adam optimizer (95K+ citations). Studied under Hinton. |
| **Yuhuai (Tony) Wu** | Google, Stanford, UofT | Mathematical reasoning research |
| **Greg Yang** | Microsoft Research (5 years) | Creator of muP / Tensor Programs |
| **Toby Pohlen** | Google DeepMind (6+ years) | Staff research engineer |
| **Manuel Kroiss** | Google, DeepMind | Software engineer |
| **Guodong Zhang** | DeepMind, UofT PhD | ML researcher |
| **Zihang Dai** | Google (3+ years) | Research scientist, CMU PhD |
| **Kyle Kosic** | OpenAI | SRE / infrastructure. Departed Apr 2024. |
| **Ross Nordeen** | Tesla (~4 years) | TPM in ML/supercomputing |

The team is **heavily ex-Google/DeepMind** (at least 40 former Google employees hired), which directly influenced the choice of JAX over PyTorch.

## Key Executives

- **Daniel Rowland** — Head of Data Center Operations. Former Tesla hardware engineer (Dojo team).
- **Anthony Armstrong** — CFO (hired Oct 2025). Former Morgan Stanley investment banking vice chairman.
- **Dan Hendrycks** — Advisor. Director of the Center for AI Safety.

## X/Twitter Integration

- xAI was founded separately from X but with close ties — Grok uses X data for training and real-time retrieval
- Twitter's original ML team was largely gutted in the 2022 acquisition layoffs; xAI was built from scratch with external talent
- **March 2025**: xAI formally acquired X Corp. in an all-stock deal ($33B for X), consolidating into XAI Holdings
- **February 2026**: SpaceX acquired xAI in an all-stock transaction ($1.25T combined valuation)

## Funding

| Round | Date | Amount | Valuation | Key Investors |
|-------|------|--------|-----------|---------------|
| Series B | May 2024 | $6B | $24B | Sequoia, a16z, Valor |
| Series C | Dec 2024 | $6B | $50B | Fidelity, BlackRock, Sequoia |
| Series D | Sep 2025 | $10B ($5B equity + $5B debt) | $200B | Saudi PIF, QIA, Kingdom Holdings |
| Series E | Jan 2026 | $20B | $230B | NVIDIA, Cisco, Fidelity, QIA, MGX |

**Total raised**: ~$22B primary + $5B debt facility. Tesla invested $2B in the Series E.

### Revenue

- xAI standalone: ~$500M ARR (end 2025)
- After X acquisition (consolidated): ~$3.3B+ ARR
- **64 million** monthly Grok users (Sep 2025)
- Revenue streams: SuperGrok ($30/mo), SuperGrok Heavy ($300/mo), X Premium+ ($40/mo), Grok API, Grok Business/Enterprise, Telegram partnership ($300M deal)

## Grok Model Progression

| Model | Date | Params | Training Hardware | Notes |
|-------|------|--------|-------------------|-------|
| Grok-0 | Aug 2023 | 33B dense | Oracle Cloud | First model, months after founding |
| Grok-1 | Nov 2023 | 314B MoE (86B active) | ~16K H100 (Oracle) | Open-sourced Mar 2024 (Apache 2.0) |
| Grok-2 | Aug 2024 | ~270B MoE (~115B active) | ~20K H100 | Image generation via FLUX.1 |
| Grok-3 | Feb 2025 | Undisclosed | 100-200K H100 (Colossus) | 10x compute over Grok-2. "Think" mode. |
| Grok-4 | Jul 2025 | ~1.7T MoE | Full Colossus (200K+) | RL at pretraining scale. $490M training cost. |

## External References

- [xAI Official — Colossus](https://x.ai/colossus)
- [Igor Babuschkin Farewell Post](https://x.com/ibab/status/1955741698690322585)
- [Fortune — xAI Organizational Structure](https://fortune.com/2023/11/20/xai-organizational-structure-elon-musk-top-executives/)
- [Epoch AI — Grok 4 Training Resources](https://epoch.ai/data-insights/grok-4-training-resources)
