# Data Center Cooling

## Learning Roadmap

### Tier 1: Foundations

- **Thermodynamics basics** — Heat transfer (conduction, convection, radiation), sensible vs latent heat, heat flux (W/cm²)
- **Cooling architectures** — Room-level → row-level → rack-level → chip-level; hot/cold aisle containment; CRAC vs CRAH

### Tier 2: Core Systems

- **Liquid cooling** — Direct-to-chip (cold plates) vs immersion; single-phase vs two-phase; coolant types
- **Heat rejection** — Vapor compression cycle (how chillers work); cooling towers; dry coolers; economizer modes
- **Control & optimization** — ASHRAE guidelines; delta-T optimization; variable frequency drives (VFDs)

### Tier 3: Design & Operations

- **Design considerations** — Redundancy (N, N+1, 2N); climate impact; water treatment
- **Metrics** — PUE, WUE, CUE; monitoring best practices

### Tier 4: Emerging Tech

- **Rear-door heat exchangers (RDHx)** — Retrofit option for existing facilities
- **Advanced immersion** — Single-phase and two-phase variants
- **Microfluidic cooling** — AI-designed channels etched into silicon (Microsoft/Corintis)

## Key Numbers to Remember

| Metric | Value |
|--------|-------|
| Air cooling max density | ~15-20 kW/rack |
| Direct-to-chip liquid cooling | up to 200 kW/rack |
| Immersion cooling | 200+ kW/rack |
| Immersion PUE | 1.01-1.03 |
| Each 1°C higher supply temp | ~4% cooling cost reduction |
| VFD at 50% speed | 87.5% power reduction (cube law) |
| Water-cooled chiller COP | 5-7 |
| Air-cooled chiller COP | 2.5-4 |
| Cooling tower "effective COP" | ~35-50 |

## Cooling Methods by Density

| Method | Max Density | PUE | Water Use |
|--------|-------------|-----|-----------|
| Air cooling | 15-20 kW/rack | 1.4-1.8 | None |
| Direct-to-chip + evaporative | 200 kW/rack | 1.1-1.2 | High |
| Direct-to-chip + dry cooling | 200 kW/rack | 1.2-1.4 | Near-zero |
| Single-phase immersion | 200+ kW/rack | 1.02-1.03 | None |
| Two-phase immersion | 200+ kW/rack | 1.01-1.02 | None |

## Immersion Cooling

Servers are submerged in dielectric (non-conductive) fluid instead of using air or cold plates.

### Single-Phase Immersion

- Fluid remains liquid at all times
- Uses hydrocarbon-based fluids (mineral oil derivatives)
- Fluid cost: $20-50/gallon
- Heat removed by circulating fluid to external heat exchanger
- Simpler tanks, easier maintenance
- Fluid lasts 15+ years

### Two-Phase Immersion

- Fluid boils at component surface, vapor rises and condenses on heat exchanger
- Uses fluorocarbon-based engineered fluids (low boiling point)
- Fluid cost: $200-500/gallon
- Exploits latent heat — massive heat transfer capability (up to 1500 W/cm²)
- More complex sealed systems
- 5x heat rejection capability vs single-phase

### Why Immersion Matters for AI

- Handles extreme heat densities that air and even cold plates struggle with
- PUE approaching theoretical minimum (1.01-1.03)
- No fans needed — quieter, fewer moving parts
- Enables higher chip performance (less thermal throttling)
- Challenges: serviceability, fluid cost, industry standardization still emerging

## GPU Power Progression and Cooling Requirements

**Key insight:** The cooling limit is **heat flux (W/cm²)**, not total power. A chip's coolability depends on power divided by die area.

| GPU | TDP | Die Size | Heat Flux | Cooling Required |
|-----|-----|----------|-----------|------------------|
| H100 | 700W | 814mm² | ~86 W/cm² | Air or cold plates |
| B200 | 1,200W | ~800mm² | ~150 W/cm² | Cold plates (liquid mandatory) |
| Blackwell Ultra | 1,400W | ~800mm² | ~175 W/cm² | Cold plates + advanced liquid |
| Rubin (2026) | 1,800-2,300W | TBD | TBD | Two-phase immersion |
| Rubin Ultra (2027) | 3,600W | TBD | TBD | Likely microfluidics |
| Feynman (2028) | 4,400W | ~800mm² | ~550 W/cm² | Microfluidics required |
| Beyond (2030+) | 6,000-15,000W | TBD | TBD | Definitely microfluidics |

**Cooling technology limits:**

| Technology | Max Heat Flux |
|------------|---------------|
| Air cooling | ~10 W/cm² |
| Single-phase immersion | ~20-30 W/cm² |
| Two-phase immersion | ~100-200 W/cm² (CHF limit) |
| Microchannels | 500-1,000 W/cm² |
| Jet-enhanced microchannels | ~3,000 W/cm² |

**Feynman example:**
- Single die at 4,400W / 8 cm² = 550 W/cm² — exceeds immersion limit (~200 W/cm²)
- Even as dual-die module: 4,400W / 16 cm² = 275 W/cm² — still too high
- Requires microfluidics or must spread heat across even larger area

## Beyond Immersion: Microfluidic Cooling

When chips exceed ~200 W/cm², immersion cooling hits its physical limit (Critical Heat Flux — vapor forms insulating film). The next generation is **microfluidic/microchannel cooling**:

**How it works:**
- Channels (10-500 μm wide) etched directly into silicon backside
- Coolant flows millimeters from heat-generating transistors
- Eliminates thermal interface materials (often the bottleneck)
- Extremely high surface area-to-volume ratio

**Performance:**
- Standard microchannels: 500-1,000 W/cm²
- Jet-enhanced microchannels: up to 3,000 W/cm² (state of the art)
- Microsoft/Georgia Tech demonstrated 3x better than cold plates

**Key players:**
- Microsoft/Corintis: AI-designed microfluidic channels
- TSMC: Leading direct-to-silicon cooling integration
- Georgia Tech: Research on jet-enhanced microchannels

**Timeline:**
- 2024-2025: Cold plates dominant
- 2026-2027: Two-phase immersion widespread
- 2028-2030: Microfluidics adoption begins
- 2030+: Embedded microfluidics co-designed with silicon

The transition from immersion to microfluidics is the next major inflection point in data center cooling, driven by chips exceeding 2,000-3,000W.

## Immersion Cooling History

| Year | Milestone |
|------|-----------|
| 1940s | First used for high-voltage transformers |
| 2005 | Iceotope founded (UK) — one of earliest immersion companies |
| 2009 | GRC (Green Revolution Cooling) founded — commercial single-phase begins |
| 2012 | Allied Control (now LiquidStack) founded for Bitcoin mining data centers |
| 2014 | First large two-phase deployment (500kW Hong Kong, 95% cooling energy savings) |
| 2021 | Microsoft — first cloud provider with two-phase immersion in production |
| 2025 | Liquid cooling considered "fully mainstream" for AI workloads |

Early adoption driven by cryptocurrency miners (2012-2014), then HPC and supercomputing.

## Who Uses Immersion Cooling Today

| Company | Status |
|---------|--------|
| Microsoft | Production — first hyperscaler with two-phase immersion (2021) |
| Meta | Production — $800M investment, deploying two-phase for AI |
| Google | ~1GW liquid cooling capacity across TPU deployments |
| CoreWeave | All new facilities from 2025 designed for liquid cooling |

Market: $790M (2023) → projected $6-8B by 2029 (~25% CAGR)

## Key Companies in Liquid/Immersion Cooling

### Immersion Cooling Specialists

| Company | Founded | Specialty |
|---------|---------|-----------|
| GRC | 2009, Austin TX | Single-phase immersion |
| LiquidStack | 2012, Netherlands | Two-phase, up to 250kW/rack |
| Submer | 2015, Barcelona | Single-phase pods |
| Iceotope | 2005, UK | Precision immersion (oldest specialist) |

### Direct-to-Chip Leaders

CoolIT Systems, Asetek, Boyd, Motivair

### Large Infrastructure Players

| Company | Cooling Market Share | Liquid/Immersion Offerings |
|---------|---------------------|---------------------------|
| Vertiv | 23% | CDUs up to 600kW; CoolCenter Immersion (240kW) |
| Schneider Electric | 22% | Broad liquid cooling portfolio |
| Eaton | - | Power and cooling systems |

Vertiv acquired CoolTera Ltd (Dec 2023) to expand liquid cooling; liquid cooling revenue doubled YoY in Q1 2025.
