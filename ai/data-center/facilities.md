# AI Training Data Center Facilities

This document catalogs dedicated AI training facilities globally — data centers purpose-built for large-scale AI/ML training with 50K+ GPUs or equivalent compute.

## Master Table

"Max (from power)" column = theoretical GPU capacity calculated from power using PUE 1.2 and ~1.78 kW/GPU for Blackwell-class, ~1.28 kW/GPU for H100-class. See [[ai/data-center/power-consumption]] for methodology.

| Facility | Owner | Location | Power | Reported GPUs | Max (from power) | Status | Year |
|----------|-------|----------|-------|---------------|------------------|--------|------|
| [[#xAI — Colossus (Memphis, Tennessee)\|Colossus]] | xAI | Memphis, TN, USA | 2 GW | 555K | ~1.3M | Operational | 2024 |
| [[#DeepSeek\|DeepSeek Hainan]] | DeepSeek | Lingshui, Hainan, China | TBD | 2K+ H800 | — | Operational | 2024 |
| [[#CoreWeave\|CoreWeave Total]] | CoreWeave | Multiple, USA | 2.9 GW contracted | 250K+ | ~1.4M | Operational | 2025 |
| [[#Amazon/AWS — Project Rainier (Indiana)\|Project Rainier]] | AWS/Anthropic | Indiana, USA | 2.2 GW | 500K-1M Trainium2 | ~1.4M | Operational | 2025 |
| [[#Microsoft — Azure AI Superfactory\|Azure Superfactory]] | Microsoft | Multiple, USA | 2 GW | 130K+ | ~1.3M | Operational | 2025 |
| [[#Ohio Region (Columbus Area)\|Columbus Cluster]] | Google | Ohio, USA | 1+ GW | Millions of TPUs | — | Operational | 2025 |
| [[#Iowa/Nebraska Region (Council Bluffs Area)\|Council Bluffs]] | Google | Iowa, USA | 1+ GW | Millions of TPUs | — | Operational | 2025 |
| [[#OpenAI/Stargate — Abilene, Texas (Primary Site)\|Stargate Abilene]] | OpenAI/Oracle | Texas, USA | 1.2 GW | 450K GB200 | ~560K | Operational | 2025 |
| CoreWeave Austin | CoreWeave | Texas, USA | 200 MW | TBD | ~93K | Operational | 2025 |
| CoreWeave Chester | CoreWeave | Virginia, USA | 120 MW | TBD | ~56K | Operational | 2025 |
| [[#ByteDance\|ByteDance Malaysia]] | ByteDance | Johor, Malaysia | 110 MW | TBD | ~72K | Operational | 2025 |
| [[#Nebius (ex-Yandex)\|Nebius Finland]] | Nebius | Mantsala, Finland | 75 MW | H100/H200/Blackwell | ~49K | Operational | 2025 |
| [[#Crusoe Energy\|Crusoe Iceland]] | Crusoe | Iceland | 57 MW | TBD | ~27K | Operational | 2025 |
| [[#Alibaba Cloud\|Alibaba Zhangbei]] | Alibaba | Hebei, China | TBD | 12 EFLOPS | — | Operational | 2025 |
| [[#Baidu\|Baidu Yangquan]] | Baidu | Shanxi, China | TBD | 280K servers | — | Operational | 2025 |
| Meta Kuna | Meta | Idaho, USA | 200 MW | TBD | ~93K | Completing 2025 | 2025 |
| [[#Nebius (ex-Yandex)\|Nebius New Jersey]] | Nebius | New Jersey, USA | 300 MW | TBD | ~140K | Announced | 2025 |
| CoreWeave Ellendale | CoreWeave/Applied | North Dakota, USA | 250-400 MW | TBD | ~140K | Under construction | 2025 |
| CoreWeave Denton | CoreWeave | Texas, USA | 260 MW | TBD | ~120K | Under construction | 2025 |
| [[#Crusoe Energy\|Crusoe Wyoming]] | Crusoe/Tallgrass | Wyoming, USA | 1.8 GW → 10 GW | 100K Blackwell | ~840K → 4.7M | Announced | 2025+ |
| CoreWeave Helios | CoreWeave/Galaxy | Dickens County, TX | 800 MW | TBD | ~375K | Under construction | 2025+ |
| [[#Prometheus (New Albany, Ohio)\|Prometheus]] | Meta | New Albany, OH, USA | 1 GW | TBD | ~470K | Opening 2026 | 2026 |
| Vantage Frontier | OpenAI/Vantage | Shackelford County, TX | 1.4 GW | TBD | ~655K | Under construction | 2026 |
| CoreWeave Cheyenne | CoreWeave/Related | Wyoming, USA | 302 MW | TBD | ~140K | Under construction | 2026 |
| [[#Nscale\|Nscale Texas]] | Nscale/Microsoft | Barstow, TX, USA | 240 MW | 104K GB300 | ~112K | Under construction | 2026 |
| [[#SoftBank — Japan Facilities\|SoftBank Hokkaido]] | SoftBank | Tomakomai, Japan | 300+ MW | 4K+ Blackwell | ~140K | Under construction | 2026 |
| [[#SoftBank — Japan Facilities\|SoftBank Osaka]] | SoftBank | Osaka, Japan | 150-400 MW | TBD | ~187K | Under construction | 2026 |
| Stargate Norway | OpenAI/Nscale | Narvik, Norway | 230 MW | 100K | ~108K | Announced | 2026 |
| [[#Stargate UAE (Abu Dhabi)\|Stargate UAE]] | G42/OpenAI | Abu Dhabi, UAE | 5 GW | TBD | ~2.3M | Under construction | 2026+ |
| Google Texas | Google | Armstrong/Haskell, TX | $40B investment | TBD | — | Announced | 2027 |
| Meta Lebanon | Meta | Indiana, USA | 1 GW | TBD | ~470K | Under construction | 2027 |
| CoreWeave Lancaster | CoreWeave | Pennsylvania, USA | 300 MW | TBD | ~140K | Under construction | 2027 |
| [[#Hyperion (Louisiana)\|Hyperion]] | Meta | Louisiana, USA | 5 GW | ~750K+ | ~2.3M | Under construction | 2028 |
| [[#Saudi Arabia — Humain\|Saudi AI Factory]] | Humain/NVIDIA | Saudi Arabia | 1.9 GW (2030) | 5K+ Blackwell | ~890K | Announced | 2030 |
| Google Kansas City | Google | Missouri, USA | 400 MW | TBD | ~187K | Announced | TBD |
| [[#Lambda Labs\|Lambda LA]] | Lambda Labs | Los Angeles, CA, USA | 3 GW | 1M+ target | ~1.4M | Announced | TBD |
