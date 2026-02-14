# Data Center Power Consumption

Understanding how power adds up from individual components to the full data center.

## Server-Level Breakdown

Using NVIDIA DGX H100 as reference (8-GPU server, ~10.2 kW total):

| Component | Count | Power Each | Total |
|-----------|-------|------------|-------|
| GPUs (H100) | 8 | 700W | 5,600W |
| CPUs (Intel Xeon Platinum 8480C) | 2 | ~350W | 700W |
| System memory (DDR5 DIMMs) | 32 | ~7W | ~224W |
| Networking NICs (ConnectX-7) | 8+ | ~20W | ~200W |
| Storage (NVMe SSDs) | 4-8 | ~15W | ~100W |
| **Subtotal (known components)** | | | ~6,824W |

**Gap to total system power (~10.2 kW):** ~3.4 kW unaccounted for, likely:

- NVSwitch chips (GPU-to-GPU communication within server)
- Power supply inefficiency (PSUs are ~90-95% efficient)
- Voltage regulators, motherboard
- Cooling fans

## GPU Power by Generation

| GPU | TDP |
|-----|-----|
| H100 | 700W |
| B200 | 1,200W |
| Blackwell Ultra | 1,400W |
| Feynman (2028, projected) | 4,400W |

## From Server to Data Center

### Power per GPU (including server overhead)

To estimate how many GPUs fit in a datacenter, divide total server power by GPU count:

| Server Type | Total Server Power | GPUs | Power per GPU |
|-------------|-------------------|------|---------------|
| DGX H100 | 10.2 kW | 8 | ~1.28 kW |
| Blackwell (estimated) | ~14.2 kW | 8 | ~1.78 kW |

### PUE (Power Usage Effectiveness)

PUE = Total facility power / IT equipment power

- PUE 1.0 = all power goes to compute (theoretical, impossible)
- PUE 1.2 = 20% overhead (good modern datacenter with liquid cooling)
- PUE 1.5 = 50% overhead (older or less efficient facilities)

Overhead includes: cooling systems, power distribution losses, lighting, building systems.

## Cooling Power Consumption

All IT power becomes heat. If servers use 100 kW, they generate 100 kW of heat that must be removed.

### COP vs Efficiency — Key Distinction

**COP (Coefficient of Performance)** applies only to chillers/heat pumps:
- Uses thermodynamic cycle to "pump" heat
- Moves MORE heat than electrical input (COP > 1)
- COP 5 means: 1 kW electricity moves 5 kW of heat

**Fans and pumps do NOT have COP:**
- They are fluid movers, not heat transfer devices
- Convert electrical energy to kinetic energy (moving air/water)
- Heat transfer happens via convection/evaporation — fans enable it but don't "multiply" it
- Measured by mechanical efficiency (60-85%), not COP

**Cooling towers and dry coolers:**
- Don't have true COP (no refrigeration cycle)
- But we can calculate "effective COP" = heat rejected / power consumed
- Very high because evaporation/convection does the work, fans just move air

### Chiller COP by Type

| Chiller Type | Full Load COP | Part Load COP (IPLV) |
|--------------|---------------|----------------------|
| Water-cooled centrifugal | 5.4-7.2 | 7-13 |
| Water-cooled screw | 5.0-6.4 | 6-9 |
| Air-cooled screw | 2.9-3.9 | 4-5 |
| Air-cooled scroll | 2.5-3.2 | 3-4 |

Water-cooled chillers achieve higher COP because water transfers heat better than air.

### Air Cooling

Traditional method, insufficient for AI workloads (max ~15-20 kW per rack).

| Component | Function | COP / Efficiency | Power per 100 kW IT load |
|-----------|----------|------------------|--------------------------|
| CRAC/CRAH fans | Circulate cold air | 70-80% efficiency | ~5-10 kW |
| Air-cooled chillers | Refrigeration cycle | COP 2.5-4 | 100 kW ÷ 3 = ~33 kW |
| Condenser fans | Reject heat from chiller | 70-80% efficiency | ~3-5 kW |
| **Total** | | | **~40-48 kW (40-48% overhead)** |

### Liquid Cooling — Evaporative (Cooling Towers)

Water evaporates to reject heat. Most efficient option, but consumes water continuously.

| Component | Function | COP / Efficiency | Power per 100 kW IT load |
|-----------|----------|------------------|--------------------------|
| CDU pumps | Circulate coolant through servers | 75-85% efficiency | ~1-2 kW |
| Water-cooled chillers | Refrigeration cycle | COP 5-7 | 100 kW ÷ 6 = ~17 kW |
| Cooling tower | Evaporate water to reject heat | "Effective COP" ~35-50 | ~2-3 kW |
| Chilled water pumps | Circulate water to chillers | 75-85% efficiency | ~2-3 kW |
| **Total** | | | **~22-25 kW (22-25% overhead)** |

Water consumption: millions of gallons annually (evaporated water + blowdown).

Why cooling towers are so efficient: Evaporation uses latent heat of water vaporization — physics does the heavy lifting, fans just move air at ~0.02-0.08 kW per kW of heat rejected.

### Liquid Cooling — Dry (Non-Evaporative)

No water evaporation. Heat rejected via air convection only.

| Component | Function | COP / Efficiency | Power per 100 kW IT load |
|-----------|----------|------------------|--------------------------|
| CDU pumps | Circulate coolant through servers | 75-85% efficiency | ~1-2 kW |
| Air-cooled chillers | Refrigeration cycle | COP 2.5-4 | 100 kW ÷ 3 = ~33 kW |
| Dry cooler fans | Blow air across heat exchangers | "Effective COP" ~18-25 | ~4-6 kW |
| **Total** | | | **~38-41 kW (38-41% overhead)** |

Tradeoff: Uses ~60% more energy than evaporative, but near-zero water consumption. Makes sense where renewable energy is cheap and water is scarce (e.g., Crusoe's Stargate in West Texas).

### Free Cooling (Economizer)

Uses cold ambient air/water directly, bypassing chillers entirely.

| Component | Function | Power per 100 kW IT load |
|-----------|----------|--------------------------|
| CDU pumps | Circulate coolant | ~1-2 kW |
| Cooling tower or dry cooler | Reject heat directly to cold ambient | ~2-4 kW |
| **Total** | | **~3-6 kW (3-6% overhead)** |

"Effective COP" of free cooling: ~35-70. Only available when ambient temperature is low enough (varies by climate — 50-80% of hours in moderate climates).

### Cooling Comparison Summary

| Method | Chiller COP | System Overhead | Water Use | Best For |
|--------|-------------|-----------------|-----------|----------|
| Air cooling | 2.5-4 | 40-48% | None | Low-density only |
| Liquid + evaporative | 5-7 | 22-25% | High | Most efficient, water available |
| Liquid + dry | 2.5-4 | 38-41% | Near-zero | Water-scarce, cheap energy |
| Free cooling | N/A (no chiller) | 3-6% | Varies | Cold climates |

## Power Distribution Losses

Electricity passes through multiple conversion stages, each with efficiency losses:

| Stage | Function | Efficiency | Loss per 100 kW IT |
|-------|----------|------------|-------------------|
| Transformer | Step down from grid voltage | 98% | ~2 kW |
| UPS | Battery backup + AC/DC conversion | 95% | ~5 kW |
| PDU | Distribute to racks | 98% | ~2 kW |
| **Total** | | ~91% | **~9-10 kW** |

Power distribution adds ~10% overhead regardless of cooling method.

### Example: 1 GW Datacenter

**With liquid + evaporative cooling (PUE ~1.22-1.25):**
- IT equipment power: 1 GW ÷ 1.22 = ~820 MW
- Cooling overhead: ~22-25% of IT = ~180-200 MW
- Power distribution: ~10% of IT = ~80 MW

**With liquid + dry cooling (PUE ~1.38-1.41):**
- IT equipment power: 1 GW ÷ 1.38 = ~725 MW
- Cooling overhead: ~38-41% of IT = ~275-300 MW
- Power distribution: ~10% of IT = ~70 MW

**GPU capacity:**

| Cooling Method | IT Power | Power per GPU (H100) | Total H100s | Power per GPU (Blackwell) | Total Blackwells |
|----------------|----------|---------------------|-------------|--------------------------|------------------|
| Evaporative | ~820 MW | ~1.28 kW | ~640K | ~1.78 kW | ~460K |
| Dry cooling | ~725 MW | ~1.28 kW | ~566K | ~1.78 kW | ~407K |

Note: Dry cooling reduces GPU capacity by ~12-15% compared to evaporative, but eliminates water consumption.
