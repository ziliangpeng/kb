# Data Center Scaling Bottlenecks

The practical upper limit for a single data center site (as of 2025) is approximately **1-2 GW of power capacity**, supporting hundreds of thousands to over a million GPUs. However, this is the upper bound — most datacenters are much smaller:

| Category | Power | Approximate GPUs |
|----------|-------|------------------|
| Traditional hyperscale | 10-100 MW | 10K-100K |
| New AI-focused facilities | 100-300 MW | 100K-300K |
| Mega-scale (exceptional) | 1+ GW | 500K-1M+ |

The 1 GW+ mega-datacenters (xAI Colossus, Stargate, Microsoft Fairwater) are exceptional projects that take years to build. Most available AI compute today is in smaller 100-300 MW facilities.

## Bottlenecks (by severity)

### 1. Power / Grid Access (Most Severe)

**Why it's a bottleneck:** You can't just "add" hundreds of megawatts of demand to a location. The power has to come from somewhere — new generation (power plants), new transmission lines, or existing spare capacity. Building this infrastructure takes years.

**The grid interconnection process:**

1. Application — Submit request to utility for X megawatts
2. Queue — Enter interconnection queue (years-long backlog in popular markets)
3. Feasibility study — Utility assesses if grid can handle it
4. System impact study — Engineering analysis of required upgrades
5. Facilities study — Design substations, transmission lines, transformers
6. Construction — Build the infrastructure
7. Testing and commissioning

Total timeline: **4-7+ years** in established markets. Over 90% of industry professionals cite this as the #1 obstacle.

**Local impact:** A 500 MW data center consumes as much power as a small city (~400,000 homes). This strains local grid reliability, may raise electricity prices, and utility upgrades get paid for by all ratepayers.

**Workarounds:**

- Behind-the-meter generation (gas turbines, on-site nuclear) — xAI used this for Colossus
- Site near existing power plants — Amazon bought a campus next to a nuclear plant
- Go to less congested locations — rural Texas, Ohio have shorter queues
- Secure grid capacity years in advance for future needs

### 2. Cooling Capacity

**Why it's a bottleneck:** Air cooling physically cannot remove heat fast enough from AI racks. Liquid cooling is mandatory, but the infrastructure (plumbing, coolant distribution, retrofits) has limited supply and deployment capacity.

**Air cooling no longer works** (server power ≈ heat generated):

- Air cooling: handles up to ~15-20 kW per rack
- AI training racks: 80-120 kW per rack, some reaching 600 kW
- GPU TDP: H100 (700W) → B200 (1,200W) → Blackwell Ultra (1,400W) → Feynman 2028 (4,400W)

**Heat rejection options** (chip-level cooling is closed-loop, but heat must go somewhere):

- **Evaporative cooling towers** — Water evaporates to reject heat. Very efficient, but consumes millions of gallons annually. This is where "water consumption" comes from.
- **Dry cooling (air-cooled chillers)** — Like a car radiator. No water consumed, but uses 40-50% more energy and needs 3-4x more equipment. Works better in cold climates.

Crusoe's Stargate facility uses dry cooling — one-time water fill, near-zero ongoing consumption — accepting higher energy costs in exchange. This tradeoff makes sense in West Texas where renewable energy is cheap but water is scarce.

**The actual bottleneck:** Supply and deployment of liquid cooling infrastructure, not cooling physics itself.

### 3. Network Topology

**Why it's a bottleneck:** There's a limit to how many GPUs can communicate at full bandwidth simultaneously. Beyond that limit, you either have oversubscribed links (reduced bandwidth between some GPUs) or multiple separate clusters.

- InfiniBand 3-tier fat tree maxes out at ~65,536 GPUs fully connected
- Beyond that requires 4-tier network with 7:1 oversubscription between pods
- Ethernet (Spectrum-X) has 2x the port density (128 vs 64 ports), pushing limits higher

**Why oversubscription hurts training:** Collective operations (all-reduce, all-gather) require communication across all GPUs. With 7:1 oversubscription, cross-pod communication is 7x slower than within-pod. The entire operation is bottlenecked by the slowest link, so all GPUs sit idle waiting. This directly reduces MFU.

**Note:** This is a **cluster limit**, not a data center limit. A 1 GW+ data center can host multiple clusters, or one larger cluster with oversubscribed links between pods. You design parallelism strategy to keep heavy communication (tensor parallelism) within the fully-connected boundary.

### 4. Permitting / Regulatory

**Why it's a bottleneck:** Building a massive industrial facility requires multiple government approvals, each taking months to years.

**Types of approvals needed:**

- **Zoning** — Land must be zoned for industrial/data center use; rezoning requires public hearings
- **Environmental reviews** — Water usage, noise, air quality (diesel generators), habitat impact
- **Building permits** — Standard construction permits, complex at massive scale
- **Water permits** — If using evaporative cooling, permits for usage and discharge

**Why communities push back:**

- Data centers use huge resources (power, water) but create few permanent jobs (50-100 for a massive facility)
- A factory using the same power might employ thousands
- Benefits go to distant tech companies; impacts stay local

**Relationship to power:** Grid interconnection involves separate utility permitting. You can have building permits but wait years for grid connection, or vice versa.

Timeline: 18-36 months for land use permits; $64 billion of US projects currently blocked or delayed.

### 5. Physical Space (Least Constraining)

**Why it's NOT much of a bottleneck:** For AI workloads, power limits you before space does. At 100+ kW per rack, you need far fewer racks (thus less floor space) to consume your power budget compared to traditional data centers.

- Greenfield sites can be 100-1,000+ acres
- Constraining mainly in urban/established markets (Northern Virginia, Singapore, Dublin) where land is scarce or expensive

## Why Multi-Datacenter Training Becomes Necessary

**Key distinction:** Multi-cluster (same datacenter) vs multi-datacenter (across cities).

If a training run needs 300K GPUs but your site only has 100K, you have two options:

1. **Multi-cluster in same datacenter** — Preferred if you have a large enough site. Lower latency (microseconds), simpler.
2. **Multi-datacenter across cities** — Required when no single site has enough capacity. Higher latency (20-100+ ms), requires techniques like DiLoCo.

**Why multi-datacenter happens in practice:**

- Most available sites today are 100-300 MW (100K-300K GPUs)
- The 1 GW mega-datacenters are still being built and take years
- Rather than wait, companies use existing capacity across multiple smaller sites
- Also provides geographic redundancy (natural disasters, power failures)

Multi-datacenter is often a **practical necessity** given current infrastructure, not a preferred choice. The mega-datacenters being built aim to avoid this complexity by providing enough capacity in one location.
