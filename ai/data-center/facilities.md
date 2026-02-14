# AI Training Data Center Facilities

This document catalogs dedicated AI training facilities globally — data centers purpose-built for large-scale AI/ML training with 50K+ GPUs or equivalent compute.

## Master Table

| Facility | Owner | Location | Power | GPUs/Chips | Status | Year |
|----------|-------|----------|-------|------------|--------|------|
| Hyperion | Meta | Louisiana, USA | 5 GW | ~750K+ GPUs | Under construction | 2028 |
| Stargate UAE | G42/OpenAI | Abu Dhabi, UAE | 5 GW | TBD | Under construction | 2026+ |
| Project Rainier | AWS/Anthropic | Indiana, USA | 2.2 GW | 500K-1M Trainium2 | Operational | 2025 |
| Colossus | xAI | Memphis, TN, USA | 2 GW | 555K GPUs | Operational | 2024 |
| Azure Superfactory | Microsoft | Multiple, USA | 2 GW | 100K+ GPUs | Operational | 2025 |
| Columbus Cluster | Google | Ohio, USA | 1+ GW | Millions of TPUs | Operational | 2025 |
| Stargate Abilene | OpenAI/Oracle | Texas, USA | 1.2 GW | 450K GB200 | Operational | 2025 |
| Council Bluffs | Google | Iowa, USA | 1+ GW | Millions of TPUs | Operational | 2025 |
| Stargate Ohio | SoftBank | Lordstown, OH, USA | TBD | TBD | Under construction | 2026 |
| Stargate Wisconsin | Oracle/Vantage | Wisconsin, USA | TBD | TBD | Under construction | 2026 |
| Stargate New Mexico | Oracle | Dona Ana County, NM, USA | TBD | TBD | Under construction | 2026 |
| Stargate Norway | OpenAI | Narvik, Norway | 230 MW | 100K GPUs | Announced | 2026 |
| SoftBank Hokkaido | SoftBank | Tomakomai, Japan | 300+ MW | 4K+ Blackwell | Under construction | 2026 |
| SoftBank Osaka | SoftBank | Osaka, Japan | 150-400 MW | TBD | Under construction | 2026 |
| CoreWeave Kansas City | CoreWeave | Missouri, USA | 100 MW | 10K+ Blackwell Ultra | Under construction | 2026 |
| CoreWeave Oklahoma | CoreWeave | Muskogee, OK, USA | 100 MW | TBD | Under construction | 2026 |
| Nebius Finland | Nebius | Mantsala, Finland | 75 MW | H100/H200/Blackwell | Operational | 2025 |
| Lambda LA | Lambda Labs | Los Angeles, CA, USA | 3 GW | 1M+ target | Announced | TBD |
| Saudi AI Factory | Humain/NVIDIA | Saudi Arabia | 1.9 GW (2030) | 5K+ Blackwell | Announced | 2030 |
| DeepSeek Hainan | DeepSeek | Lingshui, Hainan, China | TBD | 2K+ H800 | Operational | 2024 |

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

## Meta — Hyperion (Louisiana)

**Status:** Under Construction

| Attribute | Details |
|-----------|---------|
| **Location** | Richland Parish, Louisiana |
| **Power Capacity** | 5 GW planned (1.5 GW Phase 1 by end of 2027) |
| **GPU Count** | ~750,000 GPUs estimated (extrapolated from power) |
| **Site Size** | 2,250 acres + 1,400 additional acres purchased |
| **Cooling** | Liquid immersion and evaporative systems |
| **Investment** | $27B total (Blue Owl Capital JV — 80% ownership) |
| **Power Source** | Behind-the-meter generation: 400 MW (2x 200 MW sites by Q3 2026); 2.25 GW from 3 new Entergy gas plants (~$4B) |

**Timeline:**

- Construction underway (3,700 workers, peak 5,000 by mid-2026)
- Phase 1 expected 2028
- Full buildout late 2027-2028

**Notable:** "Would cover a significant part of Manhattan" per Zuckerberg. World's largest individual campus when complete.

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

### Stargate Norway (Narvik)

| Attribute | Details |
|-----------|---------|
| **Location** | Narvik, Norway |
| **Power Capacity** | 230 MW initial |
| **GPU Count** | 100,000 NVIDIA GPUs by end 2026 |
| **Power Source** | Hydropower |
| **Status** | Announced |

### Stargate UK

| Attribute | Details |
|-----------|---------|
| **GPU Count** | 8,000 GPUs scaling to 31,000 |
| **Status** | Announced |
| **Timeline** | Early 2026 scaling |

---

## Google — TPU Clusters

### Columbus, Ohio

| Attribute | Details |
|-----------|---------|
| **Locations** | Columbus, New Albany, Lancaster |
| **Power Capacity** | 1 GW by end 2025 |
| **Status** | Operational |

**Notable:** Described as "largest AI supercomputer on Earth" with ~500 MW AI-dedicated.

### Council Bluffs, Iowa

| Attribute | Details |
|-----------|---------|
| **Power Capacity** | 1+ GW total (500+ MW AI) |
| **Status** | Operational |

### Lincoln, Nebraska

| Attribute | Details |
|-----------|---------|
| **Site Size** | ~580 acres |
| **Status** | Under construction |

### TPU Specifications

- **TPU v7 (Ironwood):** 9,216-chip pods delivering 42.5 exaFLOPS FP8
- **Deployment:** Millions of liquid-cooled TPUs, 1+ GW liquid-cooled AI capacity
- **Capability:** Gigawatt-scale training runs across multiple campuses (2025)
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
| **Total Facilities** | 32 data centers (2025); 10 new planned |
| **Total GPUs** | 250,000 GPUs (2025) |
| **Major Customers** | OpenAI, Meta ($14B deal), Microsoft |

### Key U.S. Locations

| Location | Capacity | Status |
|----------|----------|--------|
| Hillsboro, Oregon | 36 MW | Operational |
| Plano, Texas | 13 MW | Operational |
| Muskogee, Oklahoma | 100 MW | Under construction (2026) |
| Kansas City, Missouri | 100 MW | Under construction (early 2026); 10,000 Blackwell Ultra GPUs |
| Texas (Core Scientific) | 16,000 GPUs | Deployed (Jan 2026) |

### European Expansion

| Location | Investment | Status |
|----------|------------|--------|
| UK (Crawley, London Docklands) | Part of $2.2B | Operational (H200 GPUs) |
| Norway | Part of $2.2B | 2025 |
| Sweden | Part of $2.2B | 2025 |
| Spain | Part of $2.2B | 2025 |

**Notable:** First-to-market GB200 NVL72 (Feb 2025); first GB300 NVL72 deployment (July 2025). All new facilities include liquid cooling.

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

### Hokkaido (Tomakomai)

| Attribute | Details |
|-----------|---------|
| **Power Capacity** | 300+ MW |
| **Site Size** | 700,000 sqm |
| **Status** | Under construction |
| **Timeline** | Operations FY2026 |

### Osaka (Sharp Sakai plant)

| Attribute | Details |
|-----------|---------|
| **Power Capacity** | 150 MW initial, expanding to 400 MW |
| **Acquisition Cost** | $676M |
| **Status** | Under construction |

### Current Deployment

- 1,224 NVIDIA Blackwell GPUs (Dec 2025), scaling to 4,000+
- Performance target: 10.6 ExaFLOPS when fully scaled (one of Japan's largest)

### Oracle Partnership

- Eastern Japan data center (April 2026)
- Western Japan (Oct 2026)

---

## Chinese Players

### ByteDance

| Attribute | Details |
|-----------|---------|
| **2026 GPU Investment** | $14B on NVIDIA chips (100B yuan); $23B total CapEx |
| **Strategy** | Leasing overseas data centers (Brazil, Thailand, Finland, Malaysia, Norway) to access advanced NVIDIA GPUs |
| **Custom Chips** | Two custom AI GPUs with Broadcom/TSMC (2026 debut); internal chip matching H20 performance |

### Huawei

| Attribute | Details |
|-----------|---------|
| **Ascend Chip Production** | 600K Ascend 910C (2025) -> 1.6M (2026) |
| **Roadmap** | Ascend 950PR (Q1 2026), 950DT (Q4 2026), 960 (Q4 2027) |
| **SuperPods** | Atlas 950 SuperPoD: 8,192 chips (Q4 2026); Atlas 960 SuperPoD: 15,488 chips (Q4 2027) |
| **Market Share** | 30.1% of China's GPU cloud market |

### Baidu

| Attribute | Details |
|-----------|---------|
| **Market Share** | 40.4% of China's GPU cloud market (leading position) |
| **Chip Roadmap** | M100 (2026, inference-optimized); M300 (2027, training + inference) |
| **Revenue Projection** | Chip sales $1.1B by 2026 (JPMorgan forecast) |
| **Current Hardware** | Kunlun P800 chips for Ernie AI |

### DeepSeek

| Attribute | Details |
|-----------|---------|
| **Training Infrastructure** | 256 server nodes, 2,048 GPUs (H800); R1 trained for $5.6M with 2,000 H800s |
| **Unique Infrastructure** | Underwater data center off Lingshui, Hainan Island (400+ servers, 30K gaming PC equivalent) |
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

### Nebius (ex-Yandex) — Finland

| Attribute | Details |
|-----------|---------|
| **Location** | Mantsala, Finland |
| **Power Capacity** | 25 MW, expanding to 75 MW by early 2026 |
| **GPUs** | H100, H200, Blackwell |
| **Sustainability** | PUE 1.1; 20,000 MWh/year heat recovery for district heating |

### Nebius — New Jersey

| Attribute | Details |
|-----------|---------|
| **Power Capacity** | Up to 300 MW |
| **Status** | Announced |

**Partnerships:** Meta ($3B deal); Microsoft ($17.4B deal)

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
| Columbus, Ohio (Cologix) | TBD | Operational (June 2025) |
| San Francisco, CA (ECL) | TBD | Operational |
| Allen, Texas | TBD | Operational |
| Dallas-Fort Worth (DFW-04) | TBD | New liquid-cooled facility |
| Kansas City, Missouri | 100 MW | Under construction (early 2026); 10,000+ Blackwell Ultra GPUs |
| Los Angeles (Prime LAX01) | 3 GW | Target 1M+ NVIDIA GPUs |

**Microsoft Deal:** Multi-billion dollar, multi-year; tens of thousands of GB300 NVL72 systems

**Funding:** $1.5B raise for "Superintelligence Cloud"

---

## NVIDIA (Owned Facilities)

| Initiative | Details |
|------------|---------|
| **AI Factory Research Center** | Virginia; first Vera Rubin infrastructure; Omniverse DSX blueprint |
| **HPE AI Factory Lab** | Grenoble, France (EU-based validation facility) |
| **Rubin Platform** | Full production; available H2 2026 from AWS, Google Cloud, Microsoft, OCI, CoreWeave, Lambda, Nebius, Nscale |

---

## Apple

**Status:** Different strategic approach — vertical integration focus

| Attribute | Details |
|-----------|---------|
| **Houston Manufacturing Hub** | 250,000 sq ft AI server manufacturing; shipping since Oct 2025 |
| **Investment** | $600B 4-year U.S. commitment |
| **Current Training** | Google TPUs (2,048 TPUv5p for device models; 8,192 TPUv4 for server models) |
| **Future Chips** | Apple-designed AI server chips mass production H2 2026; data centers operational 2027 |

**Notable:** Uses RDMA over Thunderbolt 5 for distributed local training (94% cost reduction vs. cloud).

---

## Confidence Notes

- **High confidence:** xAI Colossus, Project Rainier, Stargate Abilene, Google Ohio/Iowa (multiple corroborating sources, official announcements)
- **Medium confidence:** Meta Hyperion capacity projections, Chinese company GPU counts (based on extrapolations and estimates)
- **Uncertain/Conflicting:** Exact GPU counts at many facilities (companies often don't disclose); power capacity sometimes stated as "potential" vs "deployed"
- **Rapidly changing:** This is a fast-moving space; numbers may be outdated within months
