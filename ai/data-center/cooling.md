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

| GPU | TDP | Cooling Required |
|-----|-----|------------------|
| H100 | 700W | Air or cold plates |
| B200 | 1,200W | Cold plates (liquid mandatory) |
| Blackwell Ultra | 1,400W | Cold plates + advanced liquid |
| Feynman (2028 projected) | 4,400W | Immersion or microfluidics |

**Feynman example:**
- 8 GPUs × 4,400W = 35,200W just for GPUs
- Plus CPUs, memory, networking: ~40-45 kW per server
- Air cooling maxes out at 15-20 kW per rack (not server) — impossible
- Cold plates technically work but require extreme coolant flow
- Immersion or microfluidics become practical necessities

The industry is preparing now — immersion standardization efforts, pre-fab pods, and Microsoft/Corintis microfluidic cooling (channels etched into silicon) represent paths forward for next-generation chips.
