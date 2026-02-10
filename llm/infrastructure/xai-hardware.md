# xAI Hardware Infrastructure

The physical infrastructure behind xAI's Colossus supercomputer — from a repurposed appliance factory to the world's largest AI training cluster.

## Colossus Buildout Timeline

| Phase | Date | GPUs | Power | Time |
|-------|------|------|-------|------|
| Phase 1 | Sep 2024 | 100,000 H100 | ~150 MW | **122 days** (vs. 12-24 month industry norm) |
| Phase 1 expansion | ~Dec 2024 | 200,000 (150K H100 + 50K H200) | ~250 MW | 92 more days |
| GB200 addition | Late 2025 | +30,000 GB200 | — | — |
| Colossus 2 (Southaven, MS) | 2025 | ~110,000 GB200 NVL72 | ~1 GW | — |
| Third building | Jan 2026 | — | Up to 2 GW total | — |
| **Total (Jan 2026)** | | **555,000 GPUs** | **2 GW** | **~$18B in GPUs** |

Target: 1 million GPUs by late 2026. Musk's 5-year target: 50 million "H100-equivalent" GPUs.

## The Memphis Facility

Colossus is housed in a **former Electrolux appliance factory** at 3231 Paul R. Lowry Road, South Memphis, Tennessee. The 785,000 sq ft facility was opened by Electrolux in 2012 and shut down in 2020. Advantages: existing warehouse shell, initial 8 MW industrial power connection, proximity to wastewater treatment for cooling water.

The facility has **4 computing halls**, each with ~25,000 GPUs, each operating autonomously with its own storage, networking, and power.

### How They Built It in 122 Days

- Rejected new construction (18-24 month quotes) in favor of repurposing existing industrial space
- 19 days from project conception to construction-ready
- 19 days from first rack to first training run
- Average **1,600 workers on-site daily**, 50% from Shelby County
- Leased approximately **25% of the U.S.'s mobile cooling capacity**
- Used pre-assembled rack-scale components from Supermicro
- Tesla Megapacks provided immediate power buffering while permanent infrastructure was built
- Described as **10x faster** than anything Microsoft or Meta had delivered

**Key contractor**: Gresham Smith (architecture/engineering for factory-to-datacenter conversion).

### Expansion: Colossus 2 / MACROHARDRR

- **Southaven, Mississippi** — acquired a former Duke Energy power plant, 6 miles from Memphis
- $20 billion pledged for the MACROHARDRR facility (name is a jab at Microsoft)
- ~110,000 GB200 NVL72 GPUs, targeting ~1.1 PFlops FP8 compute
- Combined with Memphis, targeting 2 GW total capacity

Additional xAI data center presence in Austin TX, Hillsboro OR, and Atlanta GA.

## Server Hardware

Two vendors split the 100K GPU deployment 50/50:

### Supermicro (Liquid-Cooled Half)

**Server**: Supermicro SYS-421GU-TNXR (4U Universal GPU)

- Dual-socket Intel Xeon Scalable (LGA-4677)
- 32 DIMM slots, up to 8TB DDR5
- **8x NVIDIA H100 GPUs** on HGX baseboard
- **9x 400GbE connections**: 8 BlueField-3 SuperNICs (one per GPU) + 1 ConnectX-7 (CPU)
- 4x Broadcom PCIe Gen5 switches with **custom liquid cooling blocks** (unusual — most competitors don't liquid-cool PCIe switches)
- 6x 2.5" hot-swap NVMe/SATA bays + 2x M.2
- 3000W (2+2) redundant PSU

**Rack layout**: 8 servers per rack = **64 GPUs per rack**. Racks grouped in sets of 8 (512 GPUs per mini-cluster). Total: ~1,500+ GPU racks.

### Dell (Air-Cooled Half)

**Server**: Dell PowerEdge XE9680 (6U)

- Also 8x H100 per server
- Air-cooled (less detailed public specs for xAI's configuration)

## Cooling

### Supermicro Direct-to-Chip Liquid Cooling

Ground-up D2C design (not a retrofit):

- **In-rack CDU** (Coolant Distribution Unit) at bottom of each rack: 4U rackmount, 1+1 redundant hot-swappable pumps, up to 100 kW per rack (250 kW option available)
- **Coolant**: Propylene glycol, supports up to 45°C facility water inlet
- **1U rack manifold** at top distributes cold liquid and collects heated return
- **Cold plates** cover CPUs, GPUs, DIMMs, and PCIe switches
- **Quick-disconnect fittings** allow one-handed server removal without draining the rack
- **Rear-door heat exchangers (RDHx)** make each rack "cooling neutral to the room" — air-cooled component exhaust passes through liquid-cooled rear doors
- Heat transfers: cold plates → CDU → chilled water loop → external cooling towers

At buildout, xAI leased ~25% of the U.S.'s mobile cooling capacity to get operational before permanent cooling was installed.

## Networking

xAI chose **Ethernet over InfiniBand** — making Colossus one of the largest Ethernet-based AI training clusters ever built.

### Hardware

- **Switches**: NVIDIA Spectrum SN5600 (Spectrum-4 ASIC), 51.2 Tbps, **64 ports of 800GbE** in 2U
- **GPU NICs**: NVIDIA BlueField-3 SuperNICs, 400GbE each — one per GPU
- **CPU NIC**: NVIDIA ConnectX-7, 400GbE — one per server
- **Per-server bandwidth**: 8 × 400GbE (GPU) + 1 × 400GbE (CPU) = **3.6 Tbps total**

### Topology

**Three-tier fat-tree, rail-optimized design**:

- Switches are in **separate racks at end-of-row positions**, not in compute racks (confirmed by Glenn Klockwood)
- Each "rail" corresponds to one GPU position (GPU 0, GPU 1, etc.) across all nodes in a group — each rail has its own leaf switch
- Three tiers: T0 (leaf/rail), T1 (spine/aggregation), T2 (core/super-spine)

### Performance

- **Zero application latency degradation** or packet loss from flow collisions across all three tiers
- **95% data throughput** (vs. ~60% with standard Ethernet at this scale)
- Achieved via: RDMA over Converged Ethernet (RoCE), adaptive routing (local + global network state), telemetry-based congestion control, high-speed packet reordering in both switch ASIC and NIC, NVIDIA Direct Data Placement

### Why Ethernet Over InfiniBand?

- Multi-tenant capabilities and standards-based approach
- NVIDIA Spectrum-X brings InfiniBand-class performance to Ethernet
- Easier integration at hyperscale
- Possibly influenced by InfiniBand supply constraints

### Comparison to Meta and Google

| | xAI Colossus | Meta H100 Clusters | Google TPU v5p Pods |
|---|---|---|---|
| Scale | 100K GPUs (single cluster) | 2x ~25K GPUs | ~9K TPU chips per pod |
| Interconnect | Spectrum-X Ethernet (400GbE/GPU) | RoCE (Arista) + InfiniBand (Quantum-2) | Custom ICI @ 4,800 Gbps/chip |
| Topology | 3-tier fat-tree, rail-optimized | 3-tier fat-tree | 3D torus with Optical Circuit Switching |
| Per-chip BW | 400 Gbps | 400 Gbps | 4,800 Gbps |
| Key difference | Ethernet at unprecedented scale | Dual-fabric comparison | 12x per-chip BW, but smaller pods |

xAI's cluster is **4x larger** than Meta's biggest single cluster. Meta's RoCE cluster had congestion issues requiring 2:1 overprovisioning at T0-T1; xAI's Spectrum-X achieves 95% throughput without the same overprovisioning. Google's per-chip bandwidth is 12x higher but within tightly-coupled torus pods of ~9K chips, not 100K-scale fat-trees.

## Storage

Dual-vendor strategy:

### VAST Data (Phase 1 — Grok-3 Training)

- Primary storage for training data loading, checkpointing, and data storage
- Runs on Supermicro/Dell hardware
- Will supply **multiple exabytes** for the full Colossus expansion
- Claimed 50% TCO reduction for AI workloads

### DDN (Phase 2 — 200K GPU Expansion)

- **DDN EXAScaler**: Lustre-based parallel filesystem — high-bandwidth parallel I/O for training data and checkpoints. Sustains **TB/s write speeds**.
- **DDN Infinia**: Petabyte-scale object storage — long-term storage and data lakes
- Claims 95% data throughput efficiency during training

## Power

### The Layered Power Architecture

Colossus uses a combination of grid power, on-site gas turbines, and battery storage:

**Grid power (TVA/MLGW)**:

- Started at just **8 MW** (the factory's original industrial connection)
- MLGW upgraded to 50 MW ($760K taxpayer cost; xAI spent $24M on a new 150 MW substation)
- **150 MW** substation operational early 2025 via Tennessee Valley Authority
- After substation came online, approximately half the gas turbines were removed

**On-site gas turbines**:

- **35 Solar Turbines Titan-350** methane gas turbines, each 35-38 MW, combined ~421 MW capacity
- Initially operated without permits (classified as "non-road engines" — loophole closed by EPA in Jan 2026)
- Solaris Energy Infrastructure joint venture (49.9% xAI, 50.1% Solaris) manages power generation
- Colossus 2 in Southaven targets 41 turbines (~1.2 GW)

**Tesla Megapacks**:

- **168 Megapacks** at Colossus 1 (3.9 MWh each = ~150 MW / 600+ MWh total, ~4 hours backup)
- **200 Megapacks** planned for Colossus 2 (~1 GWh buffering)
- Tesla sold **$430 million** of Megapacks to xAI in 2025

### The Power-Checkpointing Problem

A unique challenge at GW-scale AI training: during checkpointing, all GPUs simultaneously write state to storage then idle, causing **instantaneous power drops of 50-100+ MW**. When training resumes, all GPUs spike back up simultaneously. Gas turbines cannot ramp fast enough — Tesla Megapacks absorb these fluctuations. This power transient problem doesn't exist in typical data center workloads.

## External References

- [xAI Official — Colossus](https://x.ai/colossus)
- [Supermicro Case Study (PDF)](https://www.supermicro.com/CaseStudies/Success_Story_xAI_Colossus_Cluster.pdf)
- [ServeTheHome — Inside 100K GPU xAI Colossus](https://www.servethehome.com/inside-100000-nvidia-gpu-xai-colossus-cluster-supermicro-helped-build-for-elon-musk/)
- [Glenn Klockwood — Colossus Technical Analysis](https://www.glennklockwood.com/garden/systems/Colossus)
- [NVIDIA Newsroom — Spectrum-X and xAI](https://nvidianews.nvidia.com/news/spectrum-x-ethernet-networking-xai-colossus)
- [The Register — xAI Picked Ethernet Over InfiniBand](https://www.theregister.com/2024/10/29/xai_colossus_networking/)
- [DDN Press Release — Storage for Colossus](https://www.ddn.com/press-releases/ddns-data-platform-propels-xais-colossus-to-world-class-performance/)
- [VAST Data — The Story of VAST and xAI](https://www.vastdata.com/blog/the-story-of-vast-and-xai)
- [HPCwire — xAI Colossus: The Elon Project](https://www.hpcwire.com/2024/09/05/xai-colossus-the-elon-project/)
- [SemiAnalysis — xAI Colossus 2: First Gigawatt Datacenter](https://newsletter.semianalysis.com/p/xais-colossus-2-first-gigawatt-datacenter)
- [TIME — Inside Memphis' Battle Against xAI](https://time.com/7308925/elon-musk-memphis-ai-data-center/)
