# AI Training Data Center Facilities

This document catalogs dedicated AI training facilities globally — data centers purpose-built for large-scale AI/ML training with 50K+ GPUs or equivalent compute.

## Master Table

"Max (from power)" column = theoretical GPU capacity calculated from power using PUE 1.2 and ~1.78 kW/GPU for Blackwell-class, ~1.28 kW/GPU for H100-class. See [[ai/data-center/power-consumption]] for methodology.

| Facility | Owner | Location | Power | Reported GPUs | Max (from power) | Status | Year |
|----------|-------|----------|-------|---------------|------------------|--------|------|
| Crusoe Wyoming | Crusoe/Tallgrass | Wyoming, USA | 1.8 GW → 10 GW | 100K Blackwell | ~840K → 4.7M | Announced | 2025+ |
| Hyperion | Meta | Louisiana, USA | 5 GW | ~750K+ | ~2.3M | Under construction | 2028 |
| Stargate UAE | G42/OpenAI | Abu Dhabi, UAE | 5 GW | TBD | ~2.3M | Under construction | 2026+ |
| Google Texas | Google | Armstrong/Haskell, TX | $40B investment | TBD | — | Announced | 2027 |
| CoreWeave Total | CoreWeave | Multiple, USA | 2.9 GW contracted | 250K+ | ~1.4M | Operational | 2025 |
| Project Rainier | AWS/Anthropic | Indiana, USA | 2.2 GW | 500K-1M Trainium2 | ~1.4M | Operational | 2025 |
| Colossus | xAI | Memphis, TN, USA | 2 GW | 555K | ~1.3M | Operational | 2024 |
| Azure Superfactory | Microsoft | Multiple, USA | 2 GW | 130K+ | ~1.3M | Operational | 2025 |
| Vantage Frontier | OpenAI/Vantage | Shackelford County, TX | 1.4 GW | TBD | ~655K | Under construction | 2026 |
| Columbus Cluster | Google | Ohio, USA | 1+ GW | Millions of TPUs | — | Operational | 2025 |
| Council Bluffs | Google | Iowa, USA | 1+ GW | Millions of TPUs | — | Operational | 2025 |
| Stargate Abilene | OpenAI/Oracle | Texas, USA | 1.2 GW | 450K GB200 | ~560K | Operational | 2025 |
| Prometheus | Meta | New Albany, OH, USA | 1 GW | TBD | ~470K | Opening 2026 | 2026 |
| Meta Lebanon | Meta | Indiana, USA | 1 GW | TBD | ~470K | Under construction | 2027 |
| Google Kansas City | Google | Missouri, USA | 400 MW | TBD | ~187K | Announced | TBD |
| CoreWeave Helios | CoreWeave/Galaxy | Dickens County, TX | 800 MW | TBD | ~375K | Under construction | 2025+ |
| CoreWeave Lancaster | CoreWeave | Pennsylvania, USA | 300 MW | TBD | ~140K | Under construction | 2027 |
| Nebius New Jersey | Nebius | New Jersey, USA | 300 MW | TBD | ~140K | Announced | 2025 |
| CoreWeave Ellendale | CoreWeave/Applied | North Dakota, USA | 250-400 MW | TBD | ~140K | Under construction | 2025 |
| CoreWeave Cheyenne | CoreWeave/Related | Wyoming, USA | 302 MW | TBD | ~140K | Under construction | 2026 |
| CoreWeave Denton | CoreWeave | Texas, USA | 260 MW | TBD | ~120K | Under construction | 2025 |
| Nscale Texas | Nscale/Microsoft | Barstow, TX, USA | 240 MW | 104K GB300 | ~112K | Under construction | 2026 |
| Stargate Norway | OpenAI/Nscale | Narvik, Norway | 230 MW | 100K | ~108K | Announced | 2026 |
| CoreWeave Austin | CoreWeave | Texas, USA | 200 MW | TBD | ~93K | Operational | 2025 |
| Meta Kuna | Meta | Idaho, USA | 200 MW | TBD | ~93K | Completing 2025 | 2025 |
| SoftBank Hokkaido | SoftBank | Tomakomai, Japan | 300+ MW | 4K+ Blackwell | ~140K | Under construction | 2026 |
| SoftBank Osaka | SoftBank | Osaka, Japan | 150-400 MW | TBD | ~187K | Under construction | 2026 |
| CoreWeave Chester | CoreWeave | Virginia, USA | 120 MW | TBD | ~56K | Operational | 2025 |
| ByteDance Malaysia | ByteDance | Johor, Malaysia | 110 MW | TBD | ~72K | Operational | 2025 |
| Nebius Finland | Nebius | Mantsala, Finland | 75 MW | H100/H200/Blackwell | ~49K | Operational | 2025 |
| Crusoe Iceland | Crusoe | Iceland | 57 MW | TBD | ~27K | Operational | 2025 |
| Lambda LA | Lambda Labs | Los Angeles, CA, USA | 3 GW | 1M+ target | ~1.4M | Announced | TBD |
| Saudi AI Factory | Humain/NVIDIA | Saudi Arabia | 1.9 GW (2030) | 5K+ Blackwell | ~890K | Announced | 2030 |
| Alibaba Zhangbei | Alibaba | Hebei, China | TBD | 12 EFLOPS | — | Operational | 2025 |
| Baidu Yangquan | Baidu | Shanxi, China | TBD | 280K servers | — | Operational | 2025 |
| DeepSeek Hainan | DeepSeek | Lingshui, Hainan, China | TBD | 2K+ H800 | — | Operational | 2024 |

---

## xAI — Colossus (Memphis, Tennessee)

**Status:** Operational (Phase 1 & 2), Expanding (Phase 3)

| Attribute | Details |
|-----------|---------|
| **Location** | Memphis, Tennessee (3 buildings) + power infrastructure in Southaven, Mississippi |
| **Power Capacity** | 2 GW total (as of Jan 2026 expansion) |
| **GPU Count** | 555,000 NVIDIA GPUs purchased (~$18B); currently deployed: 150K H100 + 50K H200 + 30K GB200 |
| **Target** | 1 million GPUs |
| **Cooling** | Air-cooled chillers (119 units, ~200 MW cooling capacity); $80M wastewater treatment facility for water reuse (13M gallons/day) |
| **Power Source** | Solaris Energy Infrastructure turbines (400 MW on-site, 1.1 GW by Q2 2027); 7x 35 MW turbines at Mississippi site |

**Timeline:**

- Colossus 1 operational Aug 2024
- Colossus 2 operational late 2024
- 2 GW expansion announced Jan 2026

**Notable:** Fastest data center build in history — 122 days for initial 100K GPUs. Uses mobile turbine generators and Tesla Megapacks for power storage. Controversy over unpermitted turbine operations.

---

## Meta AI Data Centers

### Hyperion (Louisiana)

**Status:** Under Construction

| Attribute | Details |
|-----------|---------|
| **Location** | Richland Parish, Louisiana |
| **Power Capacity** | 5 GW planned (1.5 GW Phase 1 by end of 2027) |
| **GPU Count** | ~750,000 GPUs estimated (extrapolated from power) |
| **Site Size** | 2,250 acres + 1,400 additional acres purchased (~3,650 acres total) |
| **Cooling** | Liquid immersion and evaporative systems |
| **Investment** | $27-50B total (Blue Owl Capital JV — 80% ownership) |
| **Power Source** | Behind-the-meter generation: 400 MW (2x 200 MW sites by Q3 2026); 2.25 GW from 3 new Entergy gas plants (~$4B) |

**Timeline:**

- Construction underway (3,700 workers, peak 5,000 by mid-2026)
- Phase 1 expected 2028
- Full buildout late 2027-2028

**Notable:** "Would cover a significant part of Manhattan" per Zuckerberg. World's largest individual campus when complete.

### Prometheus (New Albany, Ohio)

**Status:** Opening 2026

| Attribute | Details |
|-----------|---------|
| **Power Capacity** | 1 GW (world's first gigawatt-capable data center) |
| **Design** | Five rapid deployment structures (large tent-like facilities) connected via 300-foot-wide utility corridor with 20-acre power generation yard |

### Other Meta AI Facilities

| Facility | Location | Power | Investment | Status |
|----------|----------|-------|------------|--------|
| Lebanon | Indiana | 1 GW | $10B+ | Under construction (2027) |
| Temple | Texas | — | $800M+ | Under construction |
| Kuna | Idaho | 200 MW | ~$1B | Completing 2025 |

### Research SuperCluster (RSC)

**Status:** Operational

| Attribute | Details |
|-----------|---------|
| **Location** | Believed to be Henrico County, Virginia |
| **Hardware** | 2,000 DGX A100 systems (16,000 A100 GPUs total) |
| **Storage** | Up to half an exabyte |
| **Network** | One of the largest flat InfiniBand fabrics (48,000 links, 2,000 switches) |

### Other GPU Clusters

- **129K H100 Cluster:** Meta emptied 5 production data centers to create a single 129,000 H100 GPU cluster ("history's largest forklift upgrade")
- **Two 24K GPU Clusters:** One RoCE (used for Llama 3), one InfiniBand
- **Tent-Based Deployments:** Using tents to deploy GPU clusters faster while permanent facilities are built

---

## OpenAI/Stargate — Abilene, Texas (Primary Site)

**Status:** Operational

| Attribute | Details |
|-----------|---------|
| **Partners** | OpenAI, Oracle, SoftBank, Crusoe/Lancium |
| **Location** | Abilene, Texas (1,100 acres) |
| **Power Capacity** | 1.2 GW secured; 200 MW deployed (as of Jan 2025) |
| **GPU Count** | 450,000+ NVIDIA GB200 GPUs planned; 100,000 Blackwell operational |
| **Cooling** | Direct-to-chip liquid cooling (closed-loop) |
| **Power Source** | On-site battery storage; dedicated solar farm; 360 MW natural gas backup |

**Timeline:**

- Operational Sept 2025
- 2 buildings live, expanding to 20
- Remaining buildings by mid-2026

**Notable:** First operational Stargate site. Uses Crusoe's dry cooling approach — one-time water fill, near-zero ongoing consumption.

---

## OpenAI/Stargate — Other U.S. Sites

| Location | Lead Partner | Status | Expected |
|----------|--------------|--------|----------|
| Shackelford County, Texas | Oracle | Under construction | 2026 |
| Dona Ana County, New Mexico | Oracle | Under construction | 2026 |
| Wisconsin | Oracle/Vantage | Under construction | 2026 |
| Lordstown, Ohio | SoftBank | Under construction | 2026 |
| Milam County, Texas | SoftBank | Announced | TBD |
| Saline Township, Michigan | Related Digital | Announced | Early 2026 |

**Total Stargate Target:** $500B investment, 10 GW by 2029

### OpenAI Infrastructure Partnerships (Beyond Stargate)

Total committed: **Over $1 trillion** in hardware and cloud agreements.

| Partner | Capacity/Value | Notes |
|---------|---------------|-------|
| Microsoft Azure | ~130K GPUs (Phoenix, AZ) | H100/H200/GB200 across 4 buildings |
| CoreWeave | 6 GW, $22.4B | Through 2029 |
| AWS | $38B | Late 2025 |
| Google Cloud | TPU access | June 2025 |
| AMD | 6 GW MI450 GPUs | H2 2026+ |
| Oracle (non-Stargate) | 4.5 GW, ~$300B | Separate from Stargate JV |
| Vantage "Frontier" | 1.4 GW, $25B | Shackelford County, TX |
| Cerebras | $10B | WSE-3 for inference |
| Broadcom "Titan" | Custom ASIC | TSMC 3nm, end 2026 |

---

## OpenAI/Stargate — International Sites

### Stargate UAE (Abu Dhabi)

| Attribute | Details |
|-----------|---------|
| **Partners** | G42, OpenAI, Oracle, Cisco, SoftBank, NVIDIA |
| **Location** | Abu Dhabi (10 sq mile campus) |
| **Power Capacity** | 5 GW total campus; 1 GW initial cluster |
| **GPUs** | NVIDIA GB300 systems |
| **Status** | Under construction |

**Timeline:** First 200 MW by 2026; full 1 GW in 3 years.

### Other Stargate International Sites

| Location | Power | GPUs | Power Source | Status |
|----------|-------|------|--------------|--------|
| Norway (Narvik) | 230 MW | 100K | Hydropower | Announced |
| UK | — | 8K → 31K | — | Announced |

---

## Google — TPU Clusters

Google operates two primary multi-datacenter regions optimized for large-scale AI training, plus major expansion facilities.

### Ohio Region (Columbus Area)

| Attribute | Details |
|-----------|---------|
| **Locations** | Columbus, New Albany, Lancaster |
| **Power Capacity** | ~1 GW total across 3 campuses (by end 2025) |
| **Investment** | $2.3B+, with $1.7B expansion announced |
| **TPU Generations** | TPU v4, v5, v6 |
| **Cloud Zone** | us-east5 |

**Notable:** One of only two regions with three Google data centers. Described as "largest AI supercomputer on Earth" with ~500 MW AI-dedicated.

### Iowa/Nebraska Region (Council Bluffs Area)

| Attribute | Details |
|-----------|---------|
| **Council Bluffs Power** | >1 GW total campus (500+ MW AI-dedicated) |
| **Investment** | $4-5B total, plus $7B for Cedar Rapids expansion |
| **Cloud Zone** | us-central1 (hosts TPU7x, v5p, v6e) |

### Other Major Google Facilities

| Location | Investment | Power | Notes |
|----------|------------|-------|-------|
| Texas (Armstrong/Haskell) | **$40B** through 2027 | TBD | Three new AI-dedicated campuses |
| Kansas City, Missouri | $10B | 400 MW | 500 acres, clean energy |
| Mayes County, Oklahoma | $9B | — | AI hub, Anthropic TPU partnership |
| Berkeley County, SC | $9B through 2027 | — | Major campus expansion |
| Lincoln, Nebraska | $4.7B+ | — | Will be Google's largest individual site |
| Henderson, Nevada | $2.3B+ | 60 MW | 750K sq ft |
| The Dalles, Oregon | $1.8B | — | First Google DC (2006), hydropower |

### TPU Specifications

- **TPU v7 (Ironwood):** 9,216-chip pods delivering 42.5 exaFLOPS FP8
- **TPU v6e (Trillium):** 4.7x v5e performance
- **Deployment:** Millions of liquid-cooled TPUs, 1+ GW liquid-cooled AI capacity
- **Capability:** Gigawatt-scale training runs across multiple campuses (used for Gemini)
- **Anthropic Deal:** Up to 1 million TPU chips, 1+ GW capacity online in 2026

---

## Amazon/AWS — Project Rainier (Indiana)

**Status:** Operational

| Attribute | Details |
|-----------|---------|
| **Location** | New Carlisle, Indiana |
| **Investment** | $11 billion |
| **Power Capacity** | 2.2 GW (full buildout) |
| **Site Size** | 1,200 acres; 30 buildings (200K sq ft each) |
| **Chip Count** | ~500,000 Trainium2 chips operational; scaling to 1 million by end 2025 |
| **Partner** | Anthropic (primary user for Claude training) |

**Timeline:**

- Construction started Sept 2024
- 7 buildings operational Oct 2025

**Notable:** Largest capital investment in Indiana history. Co-designed silicon with Anthropic.

### AWS Trainium Roadmap

- **Trainium2:** 64 chips per UltraServer via NeuronLink
- **Trainium3:** 2.52 PFLOPS/chip, 144 GB HBM3e, 4.9 TB/s bandwidth; 4x performance improvement (late 2025)
- **Trainium4:** In development

---

## Microsoft — Azure AI Superfactory

**Status:** Operational and Expanding

### Wisconsin (Milwaukee) — Primary Site

| Attribute | Details |
|-----------|---------|
| **Power Capacity** | 350+ MW |
| **Investment** | $7.3B total |
| **Site Size** | 315 acres |
| **Cooling** | Zero-water liquid cooling |
| **Status** | Operational |

**Notable:** Described as "world's most powerful AI data center."

### Other Fairwater Sites

- Atlanta (under construction)
- 5+ additional sites nationwide (under construction)

### International Expansion (via Nscale partnership)

| Location | GPUs | Timeline |
|----------|------|----------|
| Norway | 52,000 GB300 | 2026-2027 |
| UK (Loughton) | 23,000 GB300 | Q1 2027 |
| Portugal (Sines) | 12,600 GB300 | Q1 2026 |
| Texas | 104,000 GB300 | Q3 2026 |

**Total Nscale deal:** ~200,000 NVIDIA GB300 GPUs, ~$17.4B

### Architecture

- **Scale:** 2 GW multi-site AI data center
- **Network:** Planet-scale AI superfactory integrating 400+ global Azure data centers via AI WAN across 70 regions
- **Rubin deployment:** First major cloud provider to deploy Vera Rubin-based instances (2026)

---

## CoreWeave

**Status:** Operational and Expanding Rapidly

| Attribute | Details |
|-----------|---------|
| **Total Facilities** | 33 data centers (Q3 2025) |
| **Total GPUs** | 250,000+ GPUs |
| **Active Power** | 590 MW (Q3 2025), targeting 850+ MW by end 2025 |
| **Contracted Power** | 2.9 GW |
| **Revenue Backlog** | $55.6B |
| **2026 CapEx** | $24-28B (doubling 2025) |

### Major Contracts

| Customer | Value | Term |
|----------|-------|------|
| OpenAI | $22.4B | Through 2029 |
| Meta | $14.2B | Through 2031 |
| Microsoft | ~$10B | Through 2030 |
| NVIDIA | $6.3B + $2B investment | Through 2032 |

### Major U.S. Facilities

| Location | Capacity | Investment | Status |
|----------|----------|------------|--------|
| Helios (Dickens County, TX) | 800 MW total | Galaxy partnership | Under construction |
| Lancaster, Pennsylvania | 100-300 MW | $6B | Under construction (2027) |
| Ellendale, North Dakota | 250-400 MW | $7B revenue | Under construction |
| Cheyenne, Wyoming | 302 MW | $1.2B (Related Digital) | Under construction (2026) |
| Denton, Texas | 260 MW | $1.2B | Under construction |
| Austin, Texas | 200 MW | Core Scientific | Operational |
| Chester, Virginia | 120 MW | Chirisa | Operational |
| Kenilworth, New Jersey | 392K sq ft | $1.8B | Under construction (2027) |
| Plano, Texas | — | $1.6B (NVIDIA) | Operational (3,500+ H100) |
| Volo, Illinois | 14 MW | Bloom Energy fuel cells | 2025 |
| Hillsboro, Oregon | 36 MW | Digital Realty | Operational |
| Muskogee, Oklahoma | 100 MW | Core Scientific | Under construction |

### European Facilities

| Location | Capacity | Status |
|----------|----------|--------|
| Crawley, UK | 24 MW | Operational (Oct 2024) |
| London Docklands | 224 MVA | Operational (Dec 2024) |
| Barcelona, Spain | 10,224 H200 GPUs | Operational (2025) |
| Norway | Part of $2.2B | 2025 |
| Sweden | Part of $2.2B | 2025 |

**UK Investment:** £2.5B total committed

### Canada

| Location | Details |
|----------|---------|
| Cambridge, Ontario | Cohere anchor customer; $240M federal funding |

**Notable:** First-to-market GB200 NVL72 (Feb 2025); first GB300 NVL72 deployment (July 2025). MLPerf record with 2,496 GB200 GPUs.

---

## Oracle

**Status:** Major cloud infrastructure provider with Stargate partnership

| Initiative | Details |
|------------|---------|
| **Stargate Partnership** | Primary infrastructure partner for OpenAI Stargate sites |
| **AMD MI450 Cluster** | 50,000 GPUs starting Q3 2026 (Helios racks with 72 MI450 chips each, 432 GB HBM4) |
| **DOE Partnership** | Building largest DOE AI supercomputer (Solstice: 100K Blackwell GPUs; Equinox: 10K Blackwell GPUs in 2026) |
| **CapEx** | $6.9B (2024) -> $21.2B (2025) -> ~$35B projected (2026) |

---

## Tesla — Dojo

**Status:** Shut down (Aug 2025), restarting with new chip iteration

| Attribute | Details |
|-----------|---------|
| **Original Locations** | San Jose, CA; Sacramento, CA (NTT facility); Buffalo, NY ($500M planned) |
| **Hardware** | D1 chip (TSMC 7nm, 50B transistors, 645mm^2); ExaPODs (10 cabinets, 3,000 D1 chips each) |
| **Shutdown Reason** | Musk: "All paths converged to AI6" (Samsung deal for next-gen chips, $16.5B) |

**Notable:** Restart announced Jan 2026 with new chip iteration.

---

## Anthropic

**Status:** Multi-cloud strategy with new owned infrastructure

| Infrastructure | Details |
|----------------|---------|
| **AWS Project Rainier** | 500K to 1M Trainium2 chips |
| **Google Cloud TPUs** | Up to 1 million TPU chips; 1+ GW capacity (2026) |
| **Microsoft Azure** | $30B commitment ($15B from NVIDIA/Microsoft) |
| **Fluidstack Partnership** | $50B over multiple years; Texas and New York facilities (2026) |

**Timeline:** First Fluidstack sites live in 2026; 800 permanent jobs, 2,000+ construction jobs.

---

## SoftBank — Japan Facilities

| Facility | Location | Power | Status |
|----------|----------|-------|--------|
| Hokkaido | Tomakomai | 300+ MW | Under construction (FY2026) |
| Osaka | Sharp Sakai plant | 150-400 MW | Under construction ($676M acquisition) |

**Current Deployment:** 1,224 NVIDIA Blackwell GPUs (Dec 2025) scaling to 4,000+. Target: 10.6 ExaFLOPS (one of Japan's largest).

**Oracle Partnership:** Eastern Japan DC (April 2026), Western Japan (Oct 2026).

---

## Chinese Players

### Alibaba Cloud

| Attribute | Details |
|-----------|---------|
| **Investment** | $69B (480B yuan) over 3 years for AI infrastructure |
| **Custom Chips** | Zhenwu 810E (comparable to NVIDIA H20); tens of thousands deployed |

#### Key Facilities

| Facility | Location | Capacity |
|----------|----------|----------|
| Zhangbei Super Intelligent Computing Center | Hebei Province | 12 EFLOPS |
| Ulanqab Data Center | Inner Mongolia | 3 EFLOPS |
| Hangzhou Data Center | Zhejiang Province | Hyperscale |
| Nantong Data Center | Jiangsu Province | Hyperscale |

**Global Expansion (2025-2026):** Brazil, France, Netherlands, Mexico, Japan, South Korea, Malaysia, Dubai

### Tencent

| Attribute | Details |
|-----------|---------|
| **Network** | Xingmai 2.0: supports 100,000+ GPUs in single cluster |
| **Custom Chips** | Zixiao AI chip (internal use, 2x competitor performance) |
| **CapEx Trend** | Declining due to GPU access constraints |

#### Key Facilities

| Facility | Location | Notes |
|----------|----------|-------|
| Guizhou Cave Data Center | Gui'an New Area | 30,000 sqm tunneled into hillside, bomb-shelter design |
| Tianjin Data Center | Tianjin | 10.54 MW microgrid, serves QQ/WeChat for northern China |

### ByteDance

| Attribute | Details |
|-----------|---------|
| **2026 CapEx** | $23B (160B yuan) |
| **NVIDIA Investment** | $14B for chips, $7B for overseas GPU leasing |
| **Strategy** | Leasing overseas data centers to access advanced NVIDIA GPUs |
| **Custom Chips** | Two custom AI GPUs with Broadcom/TSMC (2026 debut) |

#### Overseas Facilities

| Facility | Location | Capacity |
|----------|----------|----------|
| Bridge MY06 | Johor, Malaysia | 110 MW (anchor tenant) |
| AirTrunk SGP2 | Singapore | 78 MW |
| Additional Malaysia | Johor | $2.1-2.4B expansion |

### Baidu

| Attribute | Details |
|-----------|---------|
| **Market Share** | 40.4% of China's GPU cloud market (leading) |
| **Kunlun Cluster** | 30,000+ Kunlun P800 chips |
| **Target** | 1 million-chip Kunlun cluster by 2030 |
| **Chip Roadmap** | M100 (2026), M300 (2027), N-series (2029) |

#### Key Facilities

| Facility | Location | Scale |
|----------|----------|-------|
| Yangquan Cloud Computing Center | Shanxi Province | 280,000 servers planned (largest single DC in Asia) |
| Baoding Data Center | Hebei Province | Mega cloud computing center |

### Huawei

| Attribute | Details |
|-----------|---------|
| **Ascend Chip Production** | 600K Ascend 910C (2025) → 1.6M (2026) |
| **Roadmap** | Ascend 950PR (Q1 2026), 950DT (Q4 2026), 960 (Q4 2027) |
| **SuperPods** | Atlas 950 SuperPoD: 8,192 chips (Q4 2026); Atlas 960 SuperPoD: 15,488 chips (Q4 2027) |
| **Market Share** | 30.1% of China's GPU cloud market |

### DeepSeek

| Attribute | Details |
|-----------|---------|
| **Training Infrastructure** | 256 server nodes, 2,048 GPUs (H800); R1 trained for $5.6M with 2,000 H800s |
| **Unique Infrastructure** | Underwater data center off Lingshui, Hainan Island (400+ servers) |
| **Backbone** | 3 intelligent computing centers in Hohhot |
| **International** | Aramco Digital Data Center, Dammam, Saudi Arabia |

---

## Middle East Sovereign Efforts

### UAE — Stargate UAE / G42

| Attribute | Details |
|-----------|---------|
| **Partners** | G42, OpenAI, Oracle, Cisco, SoftBank, NVIDIA |
| **Location** | Abu Dhabi (10 sq mile campus) |
| **Power Capacity** | 5 GW total campus; 1 GW initial cluster |
| **GPUs** | NVIDIA GB300 systems |
| **Status** | Under construction (civil/structural advanced; first mechanical deliveries received) |

**Timeline:** First 200 MW by 2026; full 1 GW in 3 years.

### Saudi Arabia — Humain

| Attribute | Details |
|-----------|---------|
| **Entity** | Humain (state-backed AI entity); SDAIA |
| **Investment** | $77B infrastructure strategy |
| **Target Capacity** | 1.9 GW by 2030 |
| **NVIDIA Partnership** | Up to 5,000 Blackwell GPUs for sovereign AI factory |
| **AWS Partnership** | Major expansion planned |

---

## European Players

### Nebius (ex-Yandex)

| Attribute | Details |
|-----------|---------|
| **Power Secured** | 400+ MW current, 2.5 GW contracted by end 2026 |
| **Target** | 800 MW - 1 GW operational by end 2026 |
| **Partnerships** | Meta ($3B deal); Microsoft ($17.4B deal) |

#### Facilities

| Location | Capacity | Status | Notes |
|----------|----------|--------|-------|
| Mäntsälä, Finland | 75 MW (expanding from 25 MW) | Operational | PUE 1.1, 20K MWh/year heat recovery |
| New Jersey, USA | Up to 300 MW | Summer 2025 | DataOne partnership |
| Keflavik, Iceland | 10 MW | End of March 2025 | 100% renewable (geothermal/hydro) |

### Mistral AI

| Attribute | Details |
|-----------|---------|
| **Sweden Data Center** | €1.2B ($1.43B), EcoDataCenter in Borlänge, opening 2026 |
| **France Data Center** | Hosted by Eclairion with FluidStack |
| **Mistral Compute** | 18,000 NVIDIA Grace Blackwell Superchips (full deployment 2026) |
| **Training Infrastructure** | Trained Mixtral on Scaleway's Nabu cluster (1,016 H100 GPUs) |

### Cerebras

| Initiative | Details |
|------------|---------|
| **New Data Centers** | 6 facilities across North America and Europe (by end 2025) |
| **First Site** | Scale Datacenter, Oklahoma City (June 2025); 300+ CS-3 systems |
| **Montreal** | Operational July 2025 |
| **OpenAI Deal** | 750 MW compute through 2028; $10B+ transaction value |
| **Capacity** | 40M Llama 70B tokens/second; 20x capacity expansion |

### Nscale

| Attribute | Details |
|-----------|---------|
| **Funding** | $1.1B Series B (largest in European history) + $433M Pre-Series C |
| **Microsoft Deal** | ~200,000 NVIDIA GB300 GPUs |
| **Locations** | Texas (104K GPUs, 240 MW); UK; Portugal; Norway |

---

## Lambda Labs

**Status:** Rapidly expanding "Superintelligence Cloud" provider

| Location | Capacity | Status |
|----------|----------|--------|
| Columbus, Ohio (Cologix) | — | Operational (June 2025) |
| San Francisco, CA (ECL) | — | Operational |
| Allen, Texas | — | Operational |
| Vernon, CA (LAX01) | 21 MW | Announced (Nov 2025) |
| Kansas City, Missouri | 100 MW | Under construction (early 2026); 10K Blackwell Ultra, $500M |
| Chicago, IL | — | Planned (EdgeConneX) |
| Atlanta, GA | — | Planned (EdgeConneX) |
| Dallas-Fort Worth | — | Planned (Aligned) |

**Scale:** Clusters from 4,000 to 165,000+ GPUs. Vision: 2 GW+ by end of decade.

**Microsoft Deal:** Multi-billion dollar, multi-year; tens of thousands of GB300 NVL72 systems

**Funding:** $1.5B raise for "Superintelligence Cloud"

---

## Crusoe Energy

**Status:** Lead developer for Stargate project; focus on sustainable AI infrastructure

| Attribute | Details |
|-----------|---------|
| **Role** | Develops and operates data centers, leases to Oracle/OpenAI |
| **Power Pipeline** | 4.5 GW of natural gas secured via turbine JV |

### Facilities

| Location | Power | Status | Notes |
|----------|-------|--------|-------|
| **Wyoming (Tallgrass)** | 1.8 GW initial → 10 GW | Announced (July 2025) | Natural gas + renewables + CO2 sequestration |
| **Abilene, Texas** (Stargate) | 1.2 GW | Operational (Sept 2025) | 980K sq ft live, 8 buildings planned |
| **Iceland (ICE02)** | 57 MW | Operational | 100% geothermal/hydro, DGX GB200 NVL72 |
| **Norway (Polar)** | 12-52 MW | Announced | 100% hydroelectric |

**Notable:** Crusoe's Wyoming facility with Tallgrass could become the largest single-site data center at 10 GW potential.

---

## Other GPU Cloud Providers

### Together AI

GPU cloud provider via 5C partnership. 36,000 GB200 NVL72 deployed (supports 100K GPUs per cluster). 5C has 2 GW+ roadmap with 800 MW available 2025-2026. Facilities in Maryland (B200) and Memphis (GB200/GB300, early 2026).

### Voltage Park

AI cloud non-profit (merged with Lightning AI). 24,000 H100 GPUs + B200/GB300. 30 MW across 7 Tier 3+ data centers in WA, VA, UT, TX. Founded by Jed McCaleb.

---

## Other Notable Players

### NVIDIA (Owned Facilities)

AI Factory Research Center in Virginia (first Vera Rubin infrastructure). HPE AI Factory Lab in Grenoble, France.

### Apple

Different approach — vertical integration. Houston manufacturing hub (250K sq ft) shipping AI servers since Oct 2025. Currently trains on Google TPUs (2,048 TPUv5p + 8,192 TPUv4). Apple-designed AI server chips in mass production H2 2026. Uses RDMA over Thunderbolt 5 for distributed local training (94% cost reduction vs. cloud).

---

## Confidence Notes

- **High confidence:** xAI Colossus, Project Rainier, Stargate Abilene, Google Ohio/Iowa (multiple corroborating sources, official announcements)
- **Medium confidence:** Meta Hyperion capacity projections, Chinese company GPU counts (based on extrapolations and estimates)
- **Uncertain/Conflicting:** Exact GPU counts at many facilities (companies often don't disclose); power capacity sometimes stated as "potential" vs "deployed"
- **Rapidly changing:** This is a fast-moving space; numbers may be outdated within months
