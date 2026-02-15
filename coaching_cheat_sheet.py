#!/usr/bin/env python3
"""
coaching_cheat_sheet.py — Unified v16.17 Coaching Reference
Contains static thresholds, labels, and helper summaries for derived metrics.
"""
import pandas as pd

# --- Global Coaching Cheat Sheet Dictionary ---
CHEAT_SHEET = {}

CHEAT_SHEET["meta"] = {
    "framework": "V5.1 Unified Reporting Framework",
    "version": "v16.17",
    "last_updated": "2026-02-05",
    "source": "Unified Coaching Reference (Intervals + Seiler + Banister)"
}

# === Thresholds ===
CHEAT_SHEET["thresholds"] = {
    "ACWR": {"green": (0.8, 1.3), "amber": (0.6, 1.5)},
    "Monotony": {"green": (1.0, 2.0), "amber": (0.8, 2.5)},
    "Strain": {"green": (0, 3000), "amber": (3000, 4000)},
    "FatigueTrend": {"green": (-10, 10), "amber": (-20, 20)},  # Updated to percentage scale
    "StressTolerance": {"green": (2.0, 8.0), "amber": (1.0, 10.0)},
    "LIR": {"green": (0.8, 1.2), "amber": (0.6, 1.4), "red": (0.0, 0.6)},
    "EnduranceReserve": {"green": (1.2, 2.0), "amber": (0.8, 1.2), "red": (0.0, 0.8)},
    "FatOxEfficiency": {"green": (0.4, 0.8), "amber": (0.3, 0.9)},
    "FOxI": {"green": (30, 80), "amber": (20, 90)},          # FatOx Index %
    "CUR": {"green": (30, 70), "amber": (20, 80)},        # Carbohydrate Utilisation Ratio
    "GR": {"green": (0.5, 2.0), "amber": (0.3, 3.0)},         # Glucose Ratio
    "MES": {"green": (20, 100), "amber": (10, 120)},          # Metabolic Efficiency Score
    "ACWR_Risk": {"green": (0, 1), "amber": (1, 1)},          # Placeholder to silence undefined
    "ZQI": {"green": (5, 15), "amber": (3, 20)},               #% now
    "Durability": {"green": (0.9, 1.2),"amber": (0.7, 0.9),"red": (0.0, 0.7)},
    "IFDrift": {"green": (0.0, 0.05), "amber": (0.05, 0.10), "red": (0.10, 1.0)},
    "Lactate": {"lt1_mmol": 2.0,"lt2_mmol": 4.0,"corr_threshold": 0.6},
    "FatigueResistance": {"green": (0.9, 1.1), "amber": (0.8, 1.2)},  # ratio of long vs short power
    "EfficiencyFactor": {"green": (1.8, 2.2), "amber": (1.5, 2.5)},   # Power-to-HR ratio
    # === Wellness Metrics ===
    "HRV": {"green": (60, 90), "amber": (40, 60)},  # ms
    "RestingHR": {"green": (40, 55), "amber": (56, 65)},  # bpm
    "RestingHRDelta": {
        "green": (-2, 2),
        "amber": (2, 5),
        "red": (5, 50)
    },
    "SleepQuality": {"green": (80, 100), "amber": (65, 80)},  # score out of 100
    "RecoveryIndex": {"green": [0.9, 1.3],"amber": [0.8, 0.9],"red": [0.0, 0.8]},
    # --- HRV family ---
    "HRVBalance": {"green": [1.0, 1.3],"amber": [0.9, 1.0],"red": [0.0, 0.9]},
    "HRVStability": {"green": (0.85, 1.0), "amber": (0.7, 0.85)},
    "HRVTrend": {"green": (0.0, 5.0), "amber": (-2.0, 0.0)},
    # --- Performance Intelligence ---
    "mean_depletion_pct_7d": {"green":[0.2,0.45],"amber":[0.45,0.7]},
    "high_depletion_sessions_7d": {"green":[0,2],"amber":[3,4]},
    "mean_depletion_pct_90d": {"green":[0.15,0.35],"amber":[0.35,0.55]},
    "high_depletion_sessions_90d": {"green":[0,6],"amber":[6,10]},
    "mean_decoupling_7d": {"green":[0,5],"amber":[5,8]},
    "high_drift_sessions_7d": {"green":[0,2],"amber":[3,4]},
    "mean_decoupling_90d": {"green":[0,4],"amber":[4,7]},
    "high_drift_sessions_90d": {"green":[0,10],"amber":[10,20]},
    "rolling_joules_above_ftp_7d": {"green":[60000,160000],"amber":[160000,250000]},
    "high_intensity_days_7d": {"green":[2,4],"amber":[4,6]},
    "high_intensity_sessions_90d": {"green":[8,25],"amber":[25,40]},
    "mean_training_load_90d": {"green":[40,70],"amber":[70,90]},
    # --- W′ Balance / Anaerobic Load (Weekly) ---
    "WBalDepletion": {
        "green": (0.0, 0.25),
        "amber": (0.25, 0.45),
        "red": (0.45, 1.0),
    },
    "AnaerobicContribution": {
        "green": (0.0, 0.70),
        "amber": (0.70, 0.90),
        "red": (0.90, 1.0),
    },
    # ---HRV ---
    "HRVDeviation": {
        "green": (-5, 15),
        "amber": (-15, -5),
        "red": (-100, -15),
        "high_spike": (15, 40)
    },
    "AutonomicStatus": {
        "green": (0.97, 1.20),
        "amber": (0.92, 0.97),
        "red": (0.00, 0.92)
    },

    # ================== POLARISATION THRESHOLDS ==================
    # IMPORTANT SEMANTIC NOTE:
    # - "Polarisation" (power-based) follows the Seiler ratio definition:
    #     (Z1 + Z3) / (2 × Z2)
    #   Canonical Seiler polarisation requires ≥ 1.0.
    #   Green / amber ranges below are *heuristic coaching bands* for weekly feedback,
    #   not strict physiological definitions.
    #
    # - "PolarisationIndex" is a normalized 0–1 power-only index (Z1+Z2 share),
    #   interpreted contextually by training phase.
    #
    # - "Polarisation_fused" and "Polarisation_combined" are normalized intensity
    #   distribution indices derived using Seiler / Stöggl / Issurin methodology.
    #   Their green / amber bands represent polarised vs pyramidal vs threshold-dominant
    #   patterns at the *weekly* level (not session-level judgments).

    # --- Power-based (Seiler ratio; power only) ---
    "Polarisation": {
        "green": (0.75, 0.90),
        "amber": (0.65, 0.95),
    },  # Canonical polarised ≥1.0; UI bands are coaching heuristics
    # --- Power-only normalized index (Z1 + Z2 proportion) ---
    "PolarisationIndex": {
        "green": (0.75, 1.00),
        "amber": (0.60, 0.75),
    },  # Aerobic bias vs intensity focus (phase-dependent)
    # --- Fused HR + Power (sport-specific, normalized) ---
    "Polarisation_fused": {
        "green": (0.80, 1.00),
        "amber": (0.65, 0.80),
    },  # Seiler / Stöggl / Issurin (dominant-sport signal)
    # --- Combined HR + Power (multi-sport, normalized) ---
    "Polarisation_combined": {
        "green": (0.78, 1.00),
        "amber": (0.60, 0.78),
    },  # Global descriptor; lower precision than sport-specific
    "TSB": {
        "transition": [10, 999],     # Very fresh, low load (fitness declining)
        "fresh": [5, 10],            # Race-ready freshness
        "grey": [-5, 5],             # Balanced / neutral training
        "optimal": [-30, -5],        # Productive training fatigue (good zone)
        "high_risk": [-999, -30],    # Overreached / excessive fatigue
    },
    # ================================================================
    # 🧠 SCIENTIFICALLY VALIDATED PHASE DETECTION (v17.4)
    # ================================================================
    # These PhaseBoundaries are based on:
    # - Banister et al. (1975–1991): Impulse-Response Model (CTL/ATL → TSB)
    # - Mujika & Padilla (2003, 2010): Tapering and Performance Maintenance
    # - Seiler (2010, 2020): Endurance Intensity Distribution (Base/Build/Peak)
    # - Issurin (2008): Block Periodisation Model
    # - Friel (2009): Practical endurance periodisation framework
    #
    # In this model:
    #   trend_min / trend_max  → week-to-week % change in training load (TSS)
    #   acwr_max               → acute:chronic workload ratio (ATL/CTL) ceiling
    #   ri_min                 → Recovery Index (fatigue balance) floor
    #
    # These values align with both academic sources and Intervals.icu's
    # TSB (Training Stress Balance) fatigue-freshness mapping:
    #     transition: [10, 999]   → very fresh / detraining
    #     fresh: [5, 10]          → race-ready
    #     grey: [-5, 5]           → balanced / neutral
    #     optimal: [-30, -5]      → productive fatigue
    #     high_risk: [-999, -30]  → overreached
    # ================================================================

    "PhaseBoundaries": {
        # 🧱 BASE → Stable or gently rising CTL; small week-to-week variance
        "Base": {
            "trend_min": -0.05,
            "trend_max": 0.10,
            "acwr_max": 1.2,
            "ri_min": 0.75
        },
        # 📈 BUILD → Progressive overload; productive fatigue zone
        "Build": {
            "trend_min": 0.10,
            "trend_max": 0.40,
            "acwr_max": 1.3,
            "ri_min": 0.65
        },
        # 🏁 PEAK → Stabilised high CTL, ATL dropping, RI improving
        "Peak": {
            "trend_min": -0.10,
            "trend_max": 0.05,
            "acwr_max": 1.15,
            "ri_min": 0.8
        },
        # 📉 TAPER → Rapid ATL drop, load reduced 30–50%
        "Taper": {
            "trend_min": -0.50,
            "trend_max": -0.15,
            "acwr_max": 1.1,
            "ri_min": 0.8
        },
        # 💤 RECOVERY → Heavy unload / detraining period
        "Recovery": {
            "trend_min": -1.0,
            "trend_max": -0.50,
            "acwr_max": 1.0,
            "ri_min": 0.6
        },
        # 🧘 DELOAD → Short mid-block unloads; prevents overreach
        "Deload": {
            "trend_min": -0.25,
            "trend_max": -0.10,
            "acwr_max": 1.2,
            "ri_min": 0.7
        },
        # 🔁 CONTINUOUS LOAD → fallback when variation truly minimal (<5%)
        "Continuous Load": {
            "trend_min": -0.05,
            "trend_max": 0.05
        }
    },
}

CHEAT_SHEET["metric_groups"] = {
    # --- WDRM ---
    "mean_depletion_pct_7d": "AnaerobicRepeatability",
    "max_depletion_pct_7d": "AnaerobicRepeatability",
    "high_depletion_sessions_7d": "AnaerobicRepeatability",
    "mean_depletion_pct_90d": "AnaerobicRepeatability",
    "high_depletion_sessions_90d": "AnaerobicRepeatability",
    # --- ISDM ---
    "mean_decoupling_7d": "DurabilityProfile",
    "max_decoupling_7d": "DurabilityProfile",
    "high_drift_sessions_7d": "DurabilityProfile",
    "mean_decoupling_90d": "DurabilityProfile",
    "high_drift_sessions_90d": "DurabilityProfile",
    # --- NDLI ---
    "rolling_joules_above_ftp_7d": "NeuralDensity",
    "high_intensity_days_7d": "NeuralDensity",
    "high_intensity_sessions_90d": "NeuralDensity",
    # --- Alignment ---
    "delta_ratio": "LoadAlignment",
}


# === Phase-Aware Threshold Adjustments (optional overrides) ===
CHEAT_SHEET["phase_thresholds"] = {
    "Polarisation": {
        "base":  {"green": (0.60, 0.80), "amber": (0.50, 0.90)},
        "build": {"green": (0.75, 1.00), "amber": (0.60, 0.75)},
        "peak":  {"green": (0.80, 1.00), "amber": (0.65, 0.80)},
        "recovery": {"green": (0.70, 0.95), "amber": (0.55, 0.75)},
    },
    "PolarisationIndex": {
        "base":  {"green": (0.60, 0.80), "amber": (0.50, 0.90)},
        "build": {"green": (0.75, 1.00), "amber": (0.60, 0.75)},
        "peak":  {"green": (0.80, 1.00), "amber": (0.65, 0.80)},
        "recovery": {"green": (0.70, 0.95), "amber": (0.55, 0.75)},
    },
}
# === Polarisation Model Mapping (canonical) ===
CHEAT_SHEET["polarisation_models"] = {
    "PolarisationIndex": [
        {"label": "polarised", "range": (0.75, 1.00), "description": "80/20 intensity structure — strong aerobic bias"},
        {"label": "pyramidal", "range": (0.65, 0.75), "description": "Mixed Z2/Z3 structure — transitional base conditioning"},
        {"label": "threshold", "range": (0.00, 0.65), "description": "Threshold-heavy distribution — higher anaerobic load"},
    ],
    "Polarisation": [
        {"label": "polarised", "range": (1.00, 9.99), "description": "Classic Seiler ratio (Z1+Z3)/(2×Z2) ≥1 — clear 80/20 split"},
        {"label": "pyramidal", "range": (0.70, 1.00), "description": "Moderate-intensity dominant — typical base adaptation phase"},
        {"label": "threshold", "range": (0.00, 0.70), "description": "Z2-heavy structure — use intentionally for aerobic foundation"},
    ],
}

# ------------------------------------------------------------
# Qualitative → Traffic-light classification aliases
# ------------------------------------------------------------
# These map descriptive metric "state" or "status" labels
# (e.g. "productive", "optimal", "fatigued") to UI colors.
# Used by build_insight_view() and other semantic builders.
# ------------------------------------------------------------

CLASSIFICATION_ALIASES = {
    # --- Green (good / optimal states)
    "productive": "green",
    "optimal": "green",
    "recovering": "green",
    "good": "green",
    "balanced": "green",
    "healthy": "green",
    "normal": "green",
    "low_exposure": "green",
    # --- Amber (watch / moderate / caution)
    "amber": "amber",
    "moderate": "amber",
    "borderline": "amber",
    "watch": "amber",
    "fatigued": "amber",
    "pyramidal": "amber",
    "threshold": "amber",        # Low polarisation; phase-dependent (not inherently bad)
    # --- Red (critical / bad)
    "red": "red",
    "poor": "red",
    "overreached": "red",
    "critical": "red",
    "intensity-focused": "red",
    #--- Performance Intelligence 
    "spiking": "red",
    "clustered": "amber",
    "overreach": "red",
    "aligned": "green",
}

# === Context ===
CHEAT_SHEET["context"] = {
    "ACWR": (
    "EWMA Acute:Chronic Load Ratio — compares 7-day vs 28-day weighted loads. "
    "0.8–1.3 = productive training, <0.8 = recovery or detraining, >1.5 = overload/injury risk."
),
    "Monotony": "1–2 shows healthy variation; >2.5 means repetitive stress pattern.",
    "Strain": "Product of load × monotony; >3500 signals potential overreach.",
    "FatigueTrend": "FatigueTrend is calculated as the percentage change between the 7-day and 28-day moving averages. A 0% change indicates balance, while a positive percentage change indicates accumulating fatigue, and a negative percentage change indicates recovery.",
    "ZQI": "Zone Quality Index (%) 5-15 high-intensity time is normal <3% too easy, >20% too intense or erratic pacing.",
    "FatOxEfficiency": "0.4–0.8 means balanced fat oxidation; lower = carb dependence.",
    "FOxI": "FatOx index %; higher values mean more efficient aerobic base.",
    "CUR": "Carbohydrate Utilisation Ratio; 30-80 balanced metabolic use.",
    "GR": "Glucose Ratio; >2 indicates excess glycolytic bias.",
    "MES": "Metabolic Efficiency Score; >20 is good endurance economy.",
    "ACWR_Risk": "Used internally for stability check.",
    "StressTolerance": "2–8 indicates sustainable training strain capacity.",
    "Durability": "Durability index — ratio of power/HR stability under fatigue; >0.9 indicates good endurance robustness.",
    "LIR": "Load Intensity Ratio — ratio of total intensity to total duration; 0.8–1.2 indicates balanced training intensity distribution.",
    "EnduranceReserve": "Endurance Reserve — ratio of aerobic durability to fatigue index; >1.2 indicates strong endurance foundation.",
    "IFDrift": "IF Drift — change in Intensity Factor (power vs HR) over time; <5% stable, >10% indicates endurance fatigue or overheating.",
    "Lactate": (
        "Standard lab defaults (Mader & Heck, 1986). "
        "LT1≈2 mmol/L corresponds to the first sustained rise in blood lactate, "
        "while LT2≈4 mmol/L approximates the maximal lactate steady-state (MLSS). "
        "Override with athlete-specific testing or field protocols."),
    "FatigueResistance": (
        "Ratio of endurance (long-duration) power to threshold (short-duration) power. "
        "Values near 1.0 indicate strong fatigue resistance — ability to sustain output under fatigue. "
        "<0.9 suggests drop-off under endurance load."
    ),
    "EfficiencyFactor": (
        "Ratio of power to heart rate, representing aerobic efficiency. "
        "Higher values indicate improved aerobic conditioning and cardiovascular economy. "
        "Values between 1.8–2.2 are typical for trained endurance athletes."
    ),
    "HRV": "Heart-rate variability balance — indicator of parasympathetic recovery.",
    "RestingHR": "Resting heart rate trend — elevated HR indicates fatigue or stress.",
    "SleepQuality": "Average Garmin sleep score — proxy for sleep recovery and readiness.",
    "RecoveryIndex": "Composite of HRV and TSB to reflect overall readiness to train.",
    "HRVBalance": "HRV compared to 42-day mean — shows short-term recovery status.",
    "HRVStability": "Consistency of HRV — lower variability = better physiological stability.",
    "HRVTrend": "Direction of HRV change — rising indicates improving recovery.",
    # --- Polarisation Variants (clarified sources) ---
    "Polarisation": (
        "Power-based Seiler Polarisation Ratio (Z1 + Z3) / (2 × Z2), showing the balance "
        "between low- and high-intensity work relative to moderate (Z2) training. "
        "≥1.0 = polarised (80/20), 0.7–0.99 = mixed, <0.7 = Z2-dominant. "
        "⚙️ *Power-only metric — HR ignored.* Use primarily during power-measured cycling phases."
    ),
    "PolarisationIndex": (
        "Power-based normalized Polarisation Index (0–1). Reflects the proportion of total training "
        "time in Z1 + Z2 relative to total. ≥0.75 = strong aerobic bias, <0.60 = intensity-heavy. "
        "⚙️ *Power-only metric; dependent on accurate FTP calibration.*"
    ),
    "Polarisation_fused": (
        "Dominant-sport Polarisation Index derived from fused HR+Power data. "
        "Represents how the athlete distributes intensity within the dominant discipline. "
        "Dominance reflects the sport providing the clearest and most internally consistent "
        "intensity (zone) signal — not the sport with the greatest volume, duration, or load. "
        "≥0.80 = polarised, 0.65–0.79 = pyramidal, <0.65 = threshold-dominant. "
        "⚙️ *HR fills gaps when power unavailable; low-intensity HR-only activities may dominate "
        "the signal when cycling intensity is spread across Z2–Z4.*"
    ),
    "Polarisation_combined": (
        "Global HR+Power combined Polarisation Index across all sports. "
        "Reflects total weekly distribution and load balance for multi-sport athletes. "
        "Dominance reflects intensity signal strength, not training volume. "
        "≥0.80 = polarised, 0.65–0.79 = pyramidal, <0.65 = threshold-heavy. "
        "⚙️ *Cross-discipline index — lower precision, but best overall summary of load contrast.*"
    ),
    "WBalDepletion": (
        "Mean weekly W′ balance depletion expressed as a fraction of total W′ capacity. "
        "Represents how deeply anaerobic reserves are typically drawn during W′-capable sessions. "
        "<25% indicates light or controlled anaerobic exposure; >45% indicates repeated deep depletion."
    ),

    "AnaerobicContribution": (
        "Proportion of work above critical power relative to total W′ capacity during W′-engaged sessions. "
        "Values >0.90 indicate highly anaerobic-dominant intensity distribution when intensity is present."
    ),

    "WBalPattern": (
        "Temporal distribution pattern of W′ depletion across the reporting window. "
        "Used to identify clustering (e.g. weekend stacking) versus evenly distributed anaerobic stress."
    ),
    "AnaerobicRepeatability": (
        "WDRM (W′ Depletion & Repeatability Metric) quantifies depth and frequency "
        "of anaerobic reserve depletion across sessions. Higher values reflect repeated "
        "deep supra-threshold exposure."
    ),
    "DurabilityProfile": (
        "ISDM (Intensity Stability & Durability Metric) reflects decoupling behaviour "
        "under fatigue. Elevated values indicate cardiovascular drift or durability stress."
    ),
    "NeuralDensity": (
        "NDLI (Neural Density Load Index) captures clustering of high-intensity "
        "work within short time windows (e.g. 72h). High density increases recovery demand."
    ),
    "LoadAlignment": (
        "Acute vs Chronic alignment compares current 7-day load expression "
        "against 90-day baseline. Ratios >1.4 suggest overload; <0.8 under-stimulation."
    ),
    "HRVDeviation": (
        "Percentage deviation of latest HRV from 42-day mean. "
        "Positive values suggest improved autonomic readiness; "
        "negative values suggest suppression."
    ),
    "AutonomicStatus": (
        "Ratio of latest HRV to 42-day mean. "
        "Values near 1.0 indicate stable autonomic balance. "
        "Suppression below 0.92 may indicate fatigue."
    ),
    "RestingHRDelta": "Resting heart rate trend — elevated HR indicates fatigue or stress.",
}

CHEAT_SHEET["coaching_links"] = {
    # --- Derived Metric Coaching Links ---
    "ACWR": "If ACWR > 1.5, reduce intensity and focus on recovery to avoid overload. If ACWR < 0.8, gradually increase training load with controlled progression to build endurance.",
    "Monotony": "If Monotony > 2.5, introduce more variation in training or implement a deload week to reduce repetitive stress.",
    "Strain": "If Strain > 3000, monitor for signs of overreach and consider more rest or deloading. If Strain > 3500, consider reducing volume or intensity temporarily.",
    "FatigueTrend": "If FatigueTrend is negative (e.g., below -0.2), this indicates a recovering state. Continue with controlled training load and focus on recovery to ensure sustained progress. Avoid aggressive increases in load.",
    "FatOxEfficiency": "If FatOxEfficiency is low (<0.6), focus on improving aerobic base with longer, low-intensity efforts.",
    "ZQI": "If ZQI > 20%, review pacing strategy; excessive high-intensity time could indicate erratic pacing or overtraining. Aim for 5-15% ZQI for balanced training.",
    "FOxI": "If FOxI is increasing, continue to prioritize low-intensity work to enhance fat metabolism. If it decreases, consider increasing your Zone 2 training duration.",
    "CUR": "If CUR is outside the green zone (30-70), adjust carbohydrate intake and fueling strategy to ensure balanced metabolic use during long sessions.",
    "GR": "If GR exceeds 2.0, focus on reducing glycolytic intensity and increase aerobic work. Ensure sufficient recovery to avoid over-reliance on carbs.",
    "MES": "If MES is below 20, work on improving metabolic efficiency by increasing endurance training with a focus on aerobic base and fat metabolism.",
    "StressTolerance": "If StressTolerance is high (>8), reduce overall load and increase recovery time. If it's low (<2), ensure proper training load progression.",
    "FatigueResistance": "If FatigueResistance <0.9, add longer sub-threshold intervals or extended endurance sessions. Maintain >0.95 to support long-duration performance.",
    "EfficiencyFactor": "If EfficiencyFactor is declining, focus on aerobic conditioning and recovery. Stable or increasing EF indicates improving endurance efficiency.",
    "RecoveryIndex": "If RecoveryIndex is low, ensure adequate rest and recovery. If high, maintain load and monitor for overreaching.",
    # --- Polarisation Variants Coaching Links ---
    "Polarisation": (
        "If Polarisation <0.7 during base, this reflects aerobic Z2 dominance (✅ normal). "
        "If in Build/Peak, reduce Z2 time and increase Z1/Z3 contrast. "
        "Maintain ≥1.0 for ideal 80/20 balance in power-measured disciplines."
    ),
    "PolarisationIndex": (
        "If PolarisationIndex <0.60 during base, increase Z1 time to reinforce aerobic bias. "
        "If low in Build, acceptable for intensity focus. "
        "Target ≥0.75 in base and recovery blocks for efficient endurance adaptation."
    ),
    "Polarisation_fused": (
        "If fused Polarisation Index <0.65, the dominant sport is intensity-heavy — "
        "increase Z1/Z2 duration or insert a recovery microcycle. "
        "Maintain ≥0.80 for a robust endurance foundation."
    ),
    "Polarisation_combined": (
        "If combined Polarisation Index <0.65, total weekly load is intensity-heavy. "
        "Add endurance-focused sessions or recovery days to preserve a healthy 80/20 ratio. "
        "Ideal global range ≥0.78 for mixed-sport athletes."
    ),
    "WBalDepletion": (
        "High W′ depletion (>45%) indicates repeated deep anaerobic stress. "
        "If clustered, monitor recovery closely; if sustained week-over-week, consider redistributing intensity."
    ),
    "AnaerobicContribution": (
        "Very high anaerobic contribution (>90%) means intensity sessions are highly glycolytic. "
        "This is appropriate for race-specific or VO₂ blocks but should not dominate base phases."
    ),
    "WBalPattern": (
        "Clustered anaerobic patterns (e.g. weekend stacking) increase short-term fatigue risk "
        "but can be effective when followed by sufficient recovery."
    ),
    "AnaerobicRepeatability": (
        "If WDRM high week-over-week, monitor recovery and avoid stacking "
        "deep W′ sessions without adequate low-intensity support."
    ),
    "DurabilityProfile": (
        "If durability drift rising, extend aerobic steady work or reduce "
        "high-intensity density to stabilise cardiovascular efficiency."
    ),
    "NeuralDensity": (
        "If neural density clustered, insert recovery microcycles or "
        "redistribute intensity to prevent cumulative fatigue."
    ),
    "LoadAlignment": (
        "If acute > chronic (>1.4), reduce intensity density or volume. "
        "If acute < chronic (<0.8), consider progressive overload."
    ),
    "HRVStability": (
        "If HRV stability drops below 0.85, recovery variability is increasing. "
        "Ensure consistent sleep and reduce high-intensity density."
    ),
    "AutonomicStatus": (
        "If autonomic ratio drops below 0.92, reduce intensity density. "
        "Stable or elevated values support normal training."
    ),
    "HRVDeviation": (
        "If HRV deviation is negative beyond -10%, reduce intensity "
        "and prioritise sleep. Positive deviation suggests readiness."
),

}

CHEAT_SHEET["display_names"] = {
    "Polarisation": "Polarisation (Power-based, Seiler ratio)",
    "PolarisationIndex": "Polarisation Index (Power-based, normalized)",
    "Polarisation_fused": "Polarisation Index (Fused HR+Power, sport-specific)",
    "Polarisation_combined": "Polarisation Index (Combined HR+Power, multi-sport)",
    "WBalDepletion": "W′ Balance Depletion (Weekly Mean)",
    "AnaerobicContribution": "Anaerobic Contribution (W′-engaged)",
    "WBalPattern": "Anaerobic Load Pattern",
    "anaerobic_repeatability": "Anaerobic Repeatability (WDRM)",
    "durability_profile": "Durability Profile (ISDM)",
    "neural_density": "Neural Load Density (NDLI)",
    "load_alignment": "Acute vs Chronic Load Alignment",
    "wdrm_7d": "Anaerobic Repeatability (7-day)",
    "wdrm_90d": "Anaerobic Repeatability (90-day)",
}

CHEAT_SHEET["advice"] = {
    # --- Durability ---
    "Durability": {
        "low": "⚠ Durability low ({:.2f}) — extend steady-state endurance or increase time-in-zone.",
        "improving": "✅ Durability improving ({:.2f}) — maintain current long-ride structure."
    },
    # --- Load Intensity Ratio (LIR) ---
    "LIR": {
        "high": "⚠ Load intensity too high (LIR={:.2f}) — reduce intensity or monitor recovery.",
        "low": "⚠ Load intensity low (LIR={:.2f}) — add tempo or sweet-spot intervals.",
        "balanced": "✅ Load intensity balanced (LIR={:.2f})."
    },
    # --- Endurance Reserve ---
    "EnduranceReserve": {
        "depleted": "⚠ Endurance reserve depleted ({:.2f}) — add recovery or split long sessions.",
        "strong": "✅ Endurance reserve strong ({:.2f})."
    },
    # --- Efficiency Drift ---
    "IFDrift": {
        "stable": "✅ IF Drift stable ({:.2%}) — aerobic durability solid.",
        "high": "⚠ IF Drift high ({:.2%}) — improve aerobic durability or reduce fatigue load."
    },
    # Base metric: Polarisation (Power-only)
    "Polarisation": {
        "low": (
            "⚠ Seiler Polarisation ratio low ({:.2f}) — increase Z1–Z3 contrast "
            "unless this is an intentional base or durability-focused week."
        ),
        "z2_base": (
            "🧱 Seiler Z2-base dominant ({:.2f}) — expected during aerobic foundation "
            "or endurance development phases."
        ),
        "optimal": (
            "✅ Seiler 80/20 Polarisation optimal ({:.2f}) — clear low–high intensity separation."
        )
    },
    # Fused HR+Power variant (sport-specific)
    "Polarisation_fused": {
        "low": (
            "⚠ Seiler / Stöggl / Issurin methodology (HR+Power fused): polarisation low ({:.2f}) — "
            "dominant sport intensity-domain distribution is threshold-heavy; "
            "add endurance work only if this is not phase-intentional."
        ),
        "z2_base": (
            "🧱 Seiler / Stöggl / Issurin methodology (HR+Power fused): ({:.2f}) — "
            "Z2-base dominant intensity distribution, normal for aerobic development."
        ),
        "optimal": (
            "✅ Seiler / Stöggl / Issurin methodology (HR+Power fused): optimal ({:.2f}) — "
            "healthy intensity-domain contrast within the dominant sport."
        )
    },
    # Multi-sport combined variant
    "Polarisation_combined": {
        "low": (
            "⚠ Seiler / Stöggl / Issurin methodology (multi-sport combined): polarisation low ({:.2f}) — "
            "global weekly intensity-domain distribution is threshold-heavy; "
            "increase endurance ratio if not phase-intentional."
        ),
        "z2_base": (
            "🧱 Seiler / Stöggl / Issurin methodology (multi-sport combined): ({:.2f}) — "
            "pyramidal intensity distribution, acceptable in build or mixed-focus weeks."
        ),
        "optimal": (
            "✅ Seiler / Stöggl / Issurin methodology (multi-sport combined): optimal ({:.2f}) — "
            "balanced global endurance–intensity contrast across sports."
        )
    },
    # --- Recovery Index ---
    "RecoveryIndex": {
        "poor": "⚠ Recovery Index suppressed ({:.2f}) — prioritise sleep, nutrition, and reduce intensity density.",
        "moderate": "🟠 Recovery Index moderate ({:.2f}) — monitor fatigue trend.",
        "healthy": "✅ Recovery Index healthy ({:.2f})."
    },
    # --- FatigueTrend ---
    "FatigueTrend": {
        "recovery": "⚠ FatigueTrend ({:.2f}%) — Recovery phase detected. Maintain steady training load and prioritize recovery.",
        "increasing": "✅ FatigueTrend ({:.2f}%) — Increasing fatigue trend. Consider adjusting intensity or recovery."
    },
    # --- Phase Detection --- (Seasonal Phase Advice)
    "PhaseAdvice": {
        "Base": "🧱 **Base phase detected** — focus on aerobic volume (Z1–Z2 ≥ 70%), maintain ACWR ≤ 1.0.",
        "Build": "📈 **Build phase detected** — progressive overload active; maintain ACWR ≤ 1.3.",
        "Peak": "🏁 **Peak phase detected** — high-intensity emphasis; monitor fatigue (RI ≥ 0.6).",
        "Taper": "📉 **Taper phase detected** — reduce ATL by 30–50%, maintain intensity; expected RI ↑.",
        "Recovery": "💤 **Recovery phase detected** — active regeneration; target RI ≥ 0.8 and low monotony.",
        "Deload": "🧘 **Deload phase detected** — reduced load, maintain frequency; transition readiness improving.",
        "Continuous Load": "🔁 **Continuous Load** — steady training; insert variation if fatigue rises."
    },
    #Lactate-based training advice and reasoning
    "Lactate": {
        "low": (
            "Average lactate <2 mmol/L — effort likely below LT1. "
            "Excellent for aerobic base work and fat-oxidation efficiency."
        ),
        "moderate": (
            "Lactate 2–4 mmol/L — around the aerobic-anaerobic transition (Z2–Z3). "
            "Good for tempo and extensive endurance; monitor fatigue."
        ),
        "high": (
            "Lactate >4 mmol/L — above LT2 (anaerobic). "
            "Limit sustained exposure; use for threshold or VO₂ intervals."
        ),
        "correlation_strong": (
            "Lactate-power correlation strong (r > 0.6) — physiological calibration reliable."
        ),
        "correlation_weak": (
            "Lactate-power correlation weak — revert to FTP-based zones until more data available."
        ),
        "no_data": (
            "No lactate data detected — FTP defaults used for zone calibration."
        ),
    },
    "AnaerobicRepeatability": {
        "low": "Anaerobic exposure controlled — maintain structure.",
        "moderate": "Moderate anaerobic load — ensure recovery spacing.",
        "high": "High W′ depletion — monitor recovery and intensity stacking."
    },
    "DurabilityProfile": {
        "stable": "Durability stable — cardiovascular drift controlled.",
        "fatigue": "Elevated drift — consider aerobic consolidation.",
        "severe": "Significant durability stress — reduce load."
    },
    "NeuralDensity": {
        "balanced": "Intensity density well distributed.",
        "clustered": "High short-term clustering — monitor recovery.",
        "overloaded": "Neural load accumulation high — reduce intensity density."
    },
    "LoadAlignment": {
        "underload": "Acute below baseline — safe to build.",
        "aligned": "Acute aligned with chronic baseline.",
        "overreach": "Acute significantly above baseline — recovery advised."
    },
}

# =========================================================
# 🏷️ SPORT GROUP CANONICAL MAPS (Intervals.icu canonical)
# Used for zones, fusion, polarisation, reporting
# =========================================================
CHEAT_SHEET["sport_groups"] = {

    # -----------------------------
    # 🚴 CYCLING (POWER FIRST)
    # -----------------------------
    "Ride": [
        "Ride",
        "VirtualRide",
        "GravelRide",
        "MountainBikeRide",
        "TrackCycling",
        "EBikeRide",
        "EMountainBikeRide",
        "Handcycle",
        "Velomobile",
    ],

    # -----------------------------
    # 🏃 RUNNING (HR / PACE)
    # -----------------------------
    "Run": [
        "Run",
        "TrailRun",
        "VirtualRun",
        "Walk",
        "Hike",
        "Snowshoe",
    ],

    # -----------------------------
    # 🏊 SWIMMING
    # -----------------------------
    "Swim": [
        "Swim",
        "OpenWaterSwim",
        "VirtualSwim",
    ],

    # -----------------------------
    # ⛷️ SKI / SNOW
    # -----------------------------
    "Ski": [
        "AlpineSki",
        "BackcountrySki",
        "NordicSki",
        "RollerSki",
        "Snowboard",
        "VirtualSki",
    ],

    # -----------------------------
    # 🚣 ROWING
    # -----------------------------
    "Row": [
        "Row",
        "VirtualRow",
    ],

    # -----------------------------
    # 🚫 EXCLUDED FROM ZONE / POL
    # -----------------------------
    "Excluded": [
        "WeightTraining",
        "Crossfit",
        "Yoga",
        "Pilates",
        "Golf",
        "Workout",
        "HIIT",
        "Elliptical",
        "StairStepper",
        "Tennis",
        "TableTennis",
        "Squash",
        "Padel",
        "Pickleball",
        "Badminton",
        "Soccer",
        "Hockey",
        "Rugby",
        "RockClimbing",
        "Kayaking",
        "StandUpPaddling",
        "Surfing",
        "Windsurf",
        "Sail",
        "Canoeing",
    ],
}
CHEAT_SHEET["zone_semantics"] = {
    "power": {
        "label": "Cycling Power Zones",
        "description": (
            "Distribution of training time by cycling power zones. Derived from Intervals.icu power zone times for Ride-based activities. "
            "SS = Sweetspot"
        ),
    },
    "hr": {
        "label": "Cycling Heart Rate Zones",
        "description": "Distribution of training time by heart rate zones. Restricted to Ride-based activities for physiological comparability."
    },
    "pace": {
        "label": "Run Pace Zones",
        "description": "Distribution of training time by pace zones. Used primarily for Run-based activities."
    },
    "swim": {
        "label": "Swim Pace Zones",
        "description": "Distribution of training time by swim pace zones for pool and open water swims."
    },
    "fused": {
        "label": "Fused Intensity Zones",
        "description": (
            "Sport-specific fusion of power and heart-rate intensity zones. "
            "Within each activity, power is used when available; heart rate is "
            "used otherwise. Time-in-zone is normalised per sport before aggregation. "
            "This follows established endurance physiology practice where intensity "
            "distribution is defined by time spent in intensity domains, with sensors "
            "treated as interchangeable proxies rather than distinct categories "
            "(Seiler 2010; Stöggl & Sperlich 2015; Issurin 2008) "
            "SS = Sweetspot."
        ),
    },
    "combined": {
        "label": "Combined Intensity Distribution",
        "description": (
            "Global distribution of training time across intensity zones "
            "for all endurance activities. Power is prioritised where available, "
            "heart rate otherwise. Normalised once across total training time "
            "(Seiler / Stöggl / Issurin methodology) "
            "SS = Sweetspot."
        ),
    },
}

# === Labels ===
CHEAT_SHEET["labels"] = {
    "acwr_risk": "EWMA Acute:Chronic Load Ratio",
    "strain": "Load × Monotony",
    "fatigue_trend": "EMA(Load, decay=0.2) (Percentage change)",
}

CHEAT_SHEET["future_actions"] = {
    "transition": {
        "title": "Transition / Recovery",
        "reason": "Training load is low; focus on maintaining activity and recovery.",
        "priority": "low"
    },
    "fresh": {
        "title": "Freshness high",
        "reason": "You are well recovered; training is going well.",
        "priority": "normal"
    },
    "grey": {
        "title": "Grey Zone / Balanced Training",
        "reason": "Training stimulus and recovery are balanced; neutral load trend.",
        "priority": "normal"
    },
    "optimal": {
        "title": "Optimal training zone",
        "reason": "Form indicates productive training load; continue structured progression.",
        "priority": "normal"
    },
    "high_risk": {
        "title": "High Risk / Overreaching",
        "reason": "Form suggests significant fatigue; consider recovery actions.",
        "priority": "high"
    },
}

CHEAT_SHEET["future_labels"] = {
    "transition": "Very fresh — light training phase",
    "fresh": "Fresh — well recovered",
    "grey": "Neutral — balanced load",
    "optimal": "Optimal — productive training zone",
    "high_risk": "High fatigue — risk of overreaching"
}

CHEAT_SHEET["future_colors"] = {
    "transition": "#66ccff",
    "fresh": "#99ff99",
    "grey": "#cccccc",
    "optimal": "#ffcc66",
    "high_risk": "#ff6666"
}

CHEAT_SHEET["wbal_patterns"] = {
    "even": {
        "label": "Evenly Distributed",
        "description": "Anaerobic load spread consistently across the week."
    },
    "clustered_weekend": {
        "label": "Weekend Clustered",
        "description": "Anaerobic stress concentrated late in the week."
    },
    "single_day_spike": {
        "label": "Single-Day Spike",
        "description": "One dominant anaerobic session defines weekly load."
    },
}

# ============================================================
# 🔎 Metric Confidence & Applicability Rules (Contextual Model)
# ============================================================
# These rules define WHEN a metric is actionable vs contextual.
# They do NOT change values, thresholds, or classifications.
# ============================================================

CHEAT_SHEET["metric_confidence"] = {

    # --- Power-only Seiler Ratio ---
    "Polarisation": {
        "default": "contextual",
        "high_confidence_when": {
            "phases": ["Build", "Peak"],
            "min_sessions": 4,
            "min_intensity_sessions": 2
        },
        "notes": (
            "Power-based Seiler polarisation is only actionable when "
            "intensity contrast is intentionally prescribed. "
            "Z2-dominant values are expected during base, recovery, "
            "or durability-focused weeks."
        )
    },
    # --- Power-normalised index ---
    "PolarisationIndex": {
        "default": "contextual",
        "high_confidence_when": {
            "phases": ["Build", "Peak"],
            "min_sessions": 3
        },
        "notes": (
            "Normalised polarisation reflects aerobic bias rather than "
            "intensity contrast. Best used directionally."
        )
    },
    # --- Fused HR + Power (dominant sport) ---
    "Polarisation_fused": {
        "default": "contextual",
        "high_confidence_when": {
            "phases": ["Build", "Peak"],
            "dominant_sport_required": True,
            "min_sessions": 4
        },
        "notes": (
            "Fused polarisation reflects intensity distribution within "
            "the dominant sport. Confidence depends on signal quality, "
            "not volume."
        )
    },
    # --- Combined multi-sport ---
    "Polarisation_combined": {
        "default": "informational",
        "notes": (
            "Combined polarisation is a global summary metric and "
            "should never trigger corrective actions on its own."
        )
    },
    # --- W bal -------
    "WBalDepletion": {
    "default": "contextual",
    "high_confidence_when": {
        "phases": ["Build", "Peak"],
        "min_intensity_sessions": 2,
        "min_sessions": 4,
    },
    "notes": (
        "W′ balance metrics are only meaningful when sufficient supra-threshold "
        "work is present. Low values during base or recovery are expected."
    ),
    },
    "AnaerobicContribution": {
        "default": "contextual",
        "high_confidence_when": {
            "min_intensity_sessions": 2,
        },
    },
    "AnaerobicRepeatability": {
        "default": "contextual",
        "high_confidence_when": {
            "min_intensity_sessions": 2,
            "min_sessions": 4
        },
        "notes": (
            "WDRM requires repeated supra-threshold exposure to be meaningful. "
            "Low values during base or recovery are expected."
        )
    },
    "DurabilityProfile": {
        "default": "contextual",
        "high_confidence_when": {
            "min_sessions": 3
        },
        "notes": (
            "Durability (ISDM) meaningful when steady-state aerobic work "
            "exists. Not valid in short, high-intensity-only weeks."
        )
    },
    "NeuralDensity": {
        "default": "contextual",
        "high_confidence_when": {
            "min_intensity_sessions": 2
        },
        "notes": (
            "NDLI reflects clustering of high-intensity sessions. "
            "Interpret relative to recovery spacing."
        )
    },
    "LoadAlignment": {
        "default": "informational",
        "notes": (
            "Acute vs chronic alignment is directional. "
            "Should not trigger action in isolation."
        )
    },
    "HRVDeviation": {
        "default": "high",
        "high_confidence_when": {"min_samples": 7},
    },

    "HRVStability": {
        "default": "high",
        "high_confidence_when": {"min_samples": 10},
    },

    "RestingHRTrend": {
        "default": "moderate",
        "high_confidence_when": {"min_samples": 7},
    },

    "SleepQuality": {
        "default": "moderate",
        "high_confidence_when": {"min_samples": 7},
    },
}



# --- Backward compatibility aliases ---
if "IFDrift" in CHEAT_SHEET["advice"]:
    CHEAT_SHEET["advice"]["EfficiencyDrift"] = CHEAT_SHEET["advice"]["IFDrift"]
if "IFDrift" in CHEAT_SHEET["thresholds"]:
    CHEAT_SHEET["thresholds"]["EfficiencyDrift"] = CHEAT_SHEET["thresholds"]["IFDrift"]

CHEAT_SHEET["primary_messages"] = {
    "build_deload": {
        "status": (
            "Your training structure and durability are improving, "
            "but recovery is lagging slightly."
        ),
        "action": (
            "Take a short 10–15% deload to consolidate gains."
        ),
        "next": (
            "Once recovered, resume progression with slightly more "
            "intensity contrast and continued Zone 2 focus."
        ),
    },
    "overreach_deload": {
        "status": (
            "Training load has exceeded recovery capacity and fatigue "
            "is accumulating."
        ),
        "action": (
            "Apply a stronger 30–40% deload to restore recovery."
        ),
        "next": (
            "Resume training conservatively once recovery stabilises."
        ),
    },
}



# === Cheat Sheet Accessor ===
def summarize_load_block(context):
    """
    Summarize current training block load distribution using CHEAT_SHEET_RULES.
    Supports both numeric and structured ACWR contexts.
    """

    load = context.get("totalTss", 0)
    duration = context.get("totalHours", 0)
    acwr_raw = context.get("ACWR", 1.0)

    # Handle new structured ACWR (dict with ratio)
    if isinstance(acwr_raw, dict):
        acwr = float(acwr_raw.get("ratio", 1.0) or 1.0)
    else:
        try:
            acwr = float(acwr_raw or 1.0)
        except (TypeError, ValueError):
            acwr = 1.0

    # --- Classification ---
    if acwr > 1.5:
        load_type = "🚨 High Load / Overreaching"
    elif acwr < 0.8:
        load_type = "🟢 Recovery / Underload"
    else:
        load_type = "⚖️ Stable / Productive"

    return {
        "summary": f"{load_type} — {load:.1f} TSS over {duration:.1f} h (ACWR={acwr:.2f})",
        "load_type": load_type,
        "acwr": acwr,
    }

