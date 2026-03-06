"""
==============================================================
Tier 3 — Performance Intelligence
==============================================================

Performance Intelligence introduces structural capability analysis
on top of Tier-1 (Canonical) and Tier-2 (Derived / Extended Metrics).

This layer does NOT replace load metrics.
It evaluates how the athlete expresses fitness under stress.

The module exposes three performance contracts:

------------------------------------------------------------------
1️⃣  WDRM — Anaerobic Repeatability
------------------------------------------------------------------
(W′ Depletion & Recovery Model)

Purpose:
    Measures how aggressively and repeatedly the athlete depletes
    anaerobic work capacity (W′) within the reporting window.

Core Signals:
    - icu_max_wbal_depletion
    - icu_pm_w_prime
    - icu_joules_above_ftp

Interpretation:
    • High max_depletion_pct → deep anaerobic efforts
    • Multiple high_depletion_sessions → repeatability capacity
    • Total joules above FTP → supra-threshold stress density

Weekly Scope:
    Acute anaerobic stress behavior (7-day FULL dataset)

Season Scope:
    Chronic depletion exposure (90-day LIGHT aggregation)
    + acute overlay (7-day FULL)

This is not sprint power.
This is repeated supra-threshold resilience.


------------------------------------------------------------------
2️⃣  ISDM — Durability
------------------------------------------------------------------
(Intensity Sustainability & Drift Model)

Purpose:
    Measures how well power output resists cardiac drift and fatigue
    over longer durations.

Core Signals:
    - decoupling
    - moving_time
    - long session count

Interpretation:
    • Higher mean_decoupling → aerobic drift present
    • High_drift_sessions → fatigue exposure
    • Long_sessions → structural durability load

Weekly Scope:
    Acute durability state (7-day FULL)

Season Scope:
    Chronic drift behavior (90-day LIGHT)


------------------------------------------------------------------
3️⃣  NDLI — Neural Density
------------------------------------------------------------------
(Neural Load Density Index)

Purpose:
    Measures clustering of high-intensity stress
    within the reporting window.

Core Signals:
    - icu_joules_above_ftp
    - IF
    - high intensity session frequency

Interpretation:
    • High rolling_joules → neural strain accumulation
    • High_intensity_days → clustering risk
    • Elevated mean IF → central fatigue pressure

Weekly Scope:
    Acute neural stress pattern

Season Scope:
    Chronic intensity distribution


------------------------------------------------------------------
ARCHITECTURAL PRINCIPLES
------------------------------------------------------------------

• Weekly reports use 7-day FULL dataset (highest fidelity).
• Season reports use 90-day LIGHT dataset for chronic analysis.
• Weekly resolution is NEVER degraded to match season scope.
• Season adds context — it does not replace weekly intelligence.
• All calculations are deterministic and controller-owned.
• Semantic builder only exposes the computed output.

Performance Intelligence is capability modelling,
not just load reporting.
"""


---

# 🧠 V6 DESIGN PRINCIPLES

1. Preserve deterministic URF backbone
2. Keep compute external (Cloudflare → Railway)
3. Add progression intelligence
4. Add durability intelligence
5. Add neural load intelligence
6. Enable adaptive prescription (closed loop)

V6 is not “more metrics.”
V6 is **structural intelligence.**

---

# 🏗 V6 SYSTEM ARCHITECTURE

Current:

```
User → GPT → Cloudflare → Railway → Semantic Graph → GPT Render
```

V6:

```
User → GPT
        ↓
Cloudflare (Data Layer)
        ↓
Railway Tier-0 (Normalization)
        ↓
Railway Tier-1 (Canonical Metrics)
        ↓
Railway Tier-2 (Derived Metrics)
        ↓
Railway Tier-3 (Progression + Durability + Neural Modeling)
        ↓
Decision Engine (Adaptive Layer)
        ↓
Semantic Graph v6
        ↓
GPT Deterministic Render
```

---

# 🧩 NEW MODULES IN V6

---

# 1️⃣ Energy System Progression Engine (ESPE)

### Purpose:

Track progression per energy system, not just total load.

### Track 5 Domains:

* Z2 Endurance Volume Quality
* Tempo / Sweet Spot Density
* Threshold Power Repeatability
* VO2max Capacity
* Anaerobic Repeatability

### Output:

```
ESPE:
  endurance_score
  threshold_score
  vo2_score
  anaerobic_score
  trend_direction
```

This solves:

> Repeating similar intensity without measurable adaptation.

---

# 2️⃣ W′ Durability & Recovery Model (WDRM)

### Current:

* Max W′ depletion
* Joules above FTP

### V6 Adds:

* W′ recovery rate between spikes
* Depletion velocity
* Repeatability decay curve
* % recovery before next supra effort

### Output:

```
WDRM:
  repeatability_index
  recovery_efficiency
  depletion_depth_trend
  stochastic_durability_score
```

This identifies:

* CNS stress
* Race-readiness
* Anaerobic fatigue accumulation

---

# 3️⃣ Neural Load Density Index (NLDI)

This is new and important.

Current system flags fatigue accumulation.
But does not quantify *stochastic clustering.*

### V6 tracks:

* Consecutive days with W′ > X%
* Joules > FTP density over rolling 72h
* Sessions with high variability index
* CNS strain clustering

Output:

```
NLDI:
  clustering_score
  neural_strain_flag
  recovery_priority_level
```

This would have flagged your recent weekend spike automatically.

---

# 4️⃣ Intra-Session Durability Model (ISDM)

Inspired by WKO.

### Track:

* First 30min vs last 30min power
* Late-ride 5min best vs early-ride 5min best
* Power drift independent of HR drift

Output:

```
ISDM:
  fatigue_resistance_score
  late_power_decay
  durability_trend
```

Essential for:

* Gran fondo
* Climbing events
* Stage racing

---

# 5️⃣ Metabolic Drift Tracking (MDT)

You already have lactate-inferred Z2.

V6 adds:

* LT1 power trend over time
* FatOx trend slope
* Carb reliance shift during high load blocks

Output:

```
MDT:
  aerobic_efficiency_trend
  substrate_shift_index
  metabolic_stability_flag
```

---

# 6️⃣ Adaptive Decision Engine (ADE)

This is the biggest evolution.

Instead of descriptive coaching, V6 adds rule-based prescription logic.

Example:

IF:

* NLDI high
* WDRM repeatability decreasing
* FatigueTrend > 20%

THEN:

* Reduce planned VO2 duration by 15%
* Convert tempo to endurance
* Insert OFF day

This keeps deterministic structure.
No GPT improvisation.
Rules live in Railway.

---

# 📊 V6 SEMANTIC GRAPH ADDITIONS

Add new block:

```
adaptive_layer:
  progression_state
  neural_state
  durability_state
  metabolic_state
  prescription_adjustment
```

---

# 🎯 USER EXPERIENCE TIERS

V6 supports dual views:

### Coach Mode (Full URF)

Deep metrics, density charts, W′ modeling.

### Athlete Mode (Decision Dashboard)

* Today readiness
* Green / Amber / Red
* What to modify
* Why

---

# 🧬 STRATEGIC SHIFT

V5 = Tactical Monitoring Engine
V6 = Adaptive Performance Engine

V5 tells you what happened.
V6 influences what happens next.

---

# 🚀 PRIORITY IMPLEMENTATION ORDER

If building incrementally:

Phase 1:

* W′ Recovery Modeling
* Neural Load Density Index

Phase 2:

* Energy System Progression Engine

Phase 3:

* Adaptive Decision Engine

Metabolic Drift Tracking can be layered after.

---

# 🧠 What This Unlocks

For your current training pattern:

* Detect when race-style load is adaptive vs destructive
* Identify when anaerobic depth increases but repeatability drops
* Control intensity clustering automatically
* Transition blocks without overreaching

---

# 🏁 Final Thought

Your current system is analytically elite.

V6 should not add complexity.
It should add *decision intelligence.*

---

If you'd like, next we can:

* Design the Neural Load Density algorithm mathematically
* Or draft the exact data schema changes for V6 implementation
* Or simulate how V6 would have handled your last 10 days differently



----------------

PHASE 2
# Energy System Progression Engine (ESPE)

## Overview

The Energy System Progression Engine (ESPE) is a Tier-3 physiology module that evaluates adaptation trends using deterministic power curve comparisons.

ESPE does not store data.  
It operates entirely on prefetched power curve windows injected into the report context.

It is:

- Stateless  
- Deterministic  
- Versioned independently (`espe_v1`)  
- Sport-aware (Ride, Run supported; Swim excluded unless real power exists)  


---
Scope (Phase 2)

Current scope:
Ride power curves (fully supported)
Run power curves (supported if real power exists)
Swim excluded unless mechanical power data available
Future phases may include:
Fatigued curve comparison (-kj1)
CP / W′ integration
Volatility overlay (42-day vs 84-day comparison)
Forecast weighting based on adaptation bias
---

# Architecture

## Data Flow

### Production

1. Cloudflare Worker:
   - Computes curve windows
   - Calls Intervals `/power-curves`
   - Extracts anchor durations (5s, 30s, 1m, 5m, 20m, 60m)
   - Injects structured `power_curve` block into payload

2. Railway `app.py`:
   - Normalizes payload into context
   - Does not fetch curves

3. Report Controller:
   - Calls `tier3_espe.run_espe()`
   - Stores output in `context["energy_system_progression"]`

4. Semantic Builder:
   - Renders ESPE output without modification

### Local (T0)

- T0 fetches curves directly from Intervals
- Builds identical `power_curve` contract
- Skips fetch if prefetch exists

---

# Window Strategy
Weekly ESPE → 84-day non-overlapping comparison
Season ESPE → s1 vs s0 comparison
All-time and 42-day windows excluded from baseline progression logic

## Weekly Report

Purpose: Microcycle-level adaptation tracking.

Window definition:

- Current: Last 84 days
- Previous: 84 days immediately before current window

Implementation:

curves = r.prevStart.prevEnd , r.currStart.currEnd


Rationale:

- 84 days ≈ 12-week macro block
- Stable enough to reflect physiological adaptation
- Responsive enough to detect directional change
- Matches Intervals UI native option (“Last 84 days”)

Not used:

- 42 days (too reactive)
- All time (represents lifetime peak, not adaptation slope)

---

## Season Report

Purpose: Macrocycle progression tracking.

Window definition:

curves = s1 , s0


Where:
- s0 = current season
- s1 = previous season

Rationale:

- Season-aligned comparison
- No manual date math required
- Clean macrocycle narrative

---

# Power Curve Contract

Injected into context as:

```json
{
  "power_curve": {
    "Ride": {
      "current": { "5s": ..., "30s": ..., "1m": ..., "5m": ..., "20m": ..., "60m": ... },
      "previous": { ... },
      "window_days": 84
    },
    "Run": { ... }
  }
}

ESPE does not access raw curve arrays.
Only anchor durations are used.

{
  "version": "espe_v1",
  "sports": {
    "Ride": {
      "delta_percent": {...},
      "system_status": {...},
      "derived_metrics": {...},
      "plateau_detected": true|false,
      "adaptation_bias": "vo2_dominant|threshold_dominant|balanced"
    }
  }
}
This is rendered into the final report under:

energy_system_progression

ESPE v1

energy_system_progression
 └─ sports
     └─ Ride
         ├─ curve_window
         ├─ delta_percent
         ├─ system_status
         ├─ system_status_timeline
         ├─ derived_metrics  ← contextualised objects
         ├─ curve_regression
         ├─ curve_quality
         ├─ power_model
         ├─ plateau_detected
         ├─ adaptation_bias
         ├─ adaptation_state
         └─ curve_profile


ESPE v1/v2 assumes **two power-curve windows** only. If the endpoint returns multiple curves, you must select the correct pair before normalization.

## Curves used by ESPE

ESPE compares **two rolling windows**:

| curve    | purpose                      |
| -------- | ---------------------------- |
| previous | baseline physiological state |
| current  | recent physiological state   |

The delta is:

```
(current − previous) / previous
```

This is what produces:

* `delta_percent`
* `system_status`
* `adaptation_state`

## Which Intervals curves to use

From the `power-curves-ext` endpoint you normally receive curves like:

| field    | meaning        |
| -------- | -------------- |
| best     | all-time curve |
| season   | season best    |
| rolling  | rolling window |
| current  | recent window  |
| previous | prior window   |

For ESPE the correct pair is:

```
current
previous
```

Those correspond to two **rolling windows of equal length** (usually 84–90 days).

## The Worker already prepares the correct pair

Your T0 normalization already does the right thing:

```python
normalized = {
    "Ride": {
        "previous": {...},
        "current": {...},
        "window_days": prev.get("days"),
    }
}
```

So ESPE receives exactly the two curves it needs.

## Why other curves are not used

These are intentionally ignored:

| curve    | reason                                  |
| -------- | --------------------------------------- |
| best     | contaminated by historical peaks        |
| season   | mixes early and late season adaptations |
| lifetime | not physiologically meaningful          |
| event    | race-specific                           |

ESPE is designed to measure **adaptation velocity**, so it must compare **two recent rolling windows**.

## Example pipeline

Worker → returns multiple curves

```
power-curves-ext
```

Worker normalization selects:

```
previous window (90d)
current window (90d)
```

Railway ESPE computes:

```
delta(current vs previous)
```

Which produced your current result:

```
threshold +1.99%
aerobic durability +5.11%
anaerobic −4.7%
```

## What ESPE v2 will additionally use

From the **same two curves**:

* full curve map
* regression slope
* regression R²

Still **only current vs previous**.

No additional curve sets are required.

---

## Short answer

ESPE uses exactly **two curves**:

```
previous (baseline)
current (recent)
```

All other curves returned by Intervals should be ignored for ESPE analysis.
