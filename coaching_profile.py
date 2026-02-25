#!/usr/bin/env python3
"""
coaching_profile.py — Unified Coaching Profile (v16.1-Sync)
Structured reference of frameworks, formulas, and methodology anchors.
Machine-synced with coach_profile.md (2025-11-03).
"""

def get_profile_metrics(context):
    """Return adaptive coaching metrics based on context and COACH_PROFILE."""
    return {
        "eff_factor": context.get("efficiency_factor", 1.9),
        "fatigue_resistance": context.get("fatigue_resistance", 0.95),
        "endurance_decay": context.get("aerobic_decay", 0.02),
        "z2_stability": context.get("z2_variance", 0.04),
        "aerobic_decay": context.get("aerobic_decay", 0.02),
    }

# coaching_profile.py

REPORT_CONTRACT = {
    "weekly": [
        "meta", "hours", "tss", "distance_km",
        "metrics", "extended_metrics",
        "performance_intelligence",
        "zones", "daily_load", "events", "wbal_summary",
        "wellness", "phases", "insights", "insight_view", "actions",
        "planned_events", "planned_summary_by_date",
        "future_forecast", "future_actions"
    ],

    "season": [
        "meta", "hours", "tss", "distance_km",
        "metrics", "extended_metrics",
        "adaptation_metrics", "trend_metrics",
        "performance_intelligence",
        "phases", "phases_summary",
        "wbal_summary", "performance_summary",
        "insights", "actions", "future_forecast", "future_actions"
    ],

    "summary": [
        "meta", "hours", "tss", "distance_km",
        "wellness", "insights",
        "phases", "phases_summary", "performance_summary"
    ],

    "wellness": [
        "meta", "wellness", "insights", "insight_view"
    ]
}


RENDERER_PROFILES = {

    # ==============================================================
    # Global rules (apply to ALL report types)
    # ==============================================================
    "global": {
        "hard_rules": [
#           "Treat the provided semantic JSON as canonical truth.",
#           "Do NOT modify canonical metrics.",
            "Render exactly ONE report.",
            "Do NOT add numeric prefixes to section headers.",
            "Use emoji-based section headers only.",
            "Preserve section order exactly as defined by the contract.",
            "Metric context MUST be derived exclusively from each metric’s `context_window` and `confidence_model` fields."
        ],
        "list_rules": [
            "If a section value is a JSON array (list), render it as a Markdown table.",
            "Render EVERY element in the array.",
            "Preserve one row per array element.",
            "Do NOT summarise the list unless explicitly allowed by section handling.",
            "Do NOT replace lists with prose unless explicitly allowed.",
            "Do NOT omit rows for brevity."
        ],
        "tone_rules": [
            "Keep tone factual, supportive, neutral, and coach-like.",
        ],

        # NEW (presentation only)
        "state_presentation": {
            "enabled": True,
            "style": "single_sentence_banner",
            "source": "semantic_states_only",   # no derivation
        }
    },

    # ==============================================================
    # Weekly report (FULL DETAIL, SESSION-LEVEL)
    # ==============================================================
    "weekly": {
        "coaching_sentences": {
            "enabled": True,
            "max_per_section": 5,
            "placement": "after_data"
        },
        "interpretation_rules": [
            "Interpretations may be descriptive or conditional, not predictive.",
            "If semantic.wbal_summary.temporal_pattern exists, render a one-line anaerobic load timeline using block symbols (▂ ▃ ▇) mapped to none/low/moderate/high.",
            "If semantic.daily_load exists, render it as a compact monoblock map timeline with weekday labels, relative load blocks, and numeric TSS values aligned underneath. Do NOT render daily_load as a list or table.",
            "If semantic.daily_load exists AND semantic.wellness.CTL and semantic.wellness.ATL are present, a second symbolic fatigue-pressure row MAY be rendered using ↑ ↓ — symbols based ONLY on the sign of (ATL − CTL). No magnitude, thresholds, or new calculations are permitted.",
            "All rows in the daily load timeline MUST use a fixed-width column per day to ensure vertical alignment across labels, blocks, symbols, and numeric values.",
            "If session-level signal icons are rendered in the EVENTS table, a single legend line MUST be rendered once per report directly below the EVENTS section header.",
            "If zone distribution data exists (e.g. zone_dist_power, zone_dist_hr, zone_dist_fused), render zone distribution as fixed-width ASCII proportional bars (one bar per zone), with the exact percentage shown. Bars are presentational only and do not constitute derived metrics.",
            "If performance_intelligence exists, render three subsections: Anaerobic Repeatability (WDRM), Durability (ISDM), Neural Density (NDLI). Use provided values only. Do NOT recompute or merge with other metrics.",
            "If high_dep_sessions > 0 and high_drift_sessions > 0 in the same week, describe this as high neuromuscular + metabolic strain overlap."
        ],
        "allowed_enrichment": [
            "Restate semantic interpretation fields.",
            "Explain what a value indicates within its known threshold or state.",
            "derive_stepwise_forecast"
        ],
        "section_handling": {
            "events": "full",
            "daily_load": "full",
            "metrics": "full",
            "extended_metrics": "full",
            "performance_intelligence": "full",
            "zones": "full",
            "wellness": "full",
            "phases": "forbid",
            "planned_events": "full",
            "planned_summary_by_date": "full",
            "actions": "full",
            "future_actions": "full"
        },

            "emphasis": {
            "metrics": "high",
            "actions": "high",
            "events": "medium",
            "wellness": "medium"
        },

        "framing": {
            "intent": "tactical_weekly_control"
        },
        "closing_note": {
            "required": True,
            "verdict_rule": "State clearly whether last week’s training load was handled appropriately.",
            "classification_required": [
                "Handled Appropriately",
                "Near Capacity",
                "Exceeded Tolerance"
            ],
            "focus": "tactical_alignment",
            "anchor_metrics": [
                "ACWR",
                "FatigueTrend",
                "NDLI",
                "Durability",
                "performance_intelligence.training_state"
            ],
            "intent_rule": "Assess whether acute load and recovery state align with immediate training intent.",
            "max_sentences": 4
        }
    },

    # ==============================================================
    # Season report (PHASE-LEVEL, STRATEGIC)
    # ==============================================================
    "season": {
        "coaching_sentences": {
            "enabled": True,
            "max_per_section": 5,
            "placement": "after_data"
        },
        "interpretation_rules": [
            "Focus on trends, phases, and accumulated load.",
            "Avoid session-level or daily commentary.",
            "If performance_intelligence exists, render chronic_state first (90d), then acute_overlay (7d). Emphasise contrast between chronic capacity and acute stress.",
        ],
        "allowed_enrichment": [
            "Restate phase descriptors already present in semantic data."
        ],
        "section_handling": {
            "events": "forbid",
            "daily_load": "forbid",
            "weekly_phases": "forbid",
            "phases": "full",
            "metrics": "full",
            "extended_metrics": "full",
            "performance_intelligence": "full",
            "zones": "summary",
            "wellness": "summary",
            "actions": "full",
            "future_actions": "full"
        },

        "emphasis": {
            "phases": "high",
            "trend_metrics": "high",
            "metrics": "medium"
        },

        "framing": {
            "intent": "medium_term_block_assessment"
        },
        "closing_note": {
            "required": True,
            "verdict_rule": "Classify the training block adaptation trajectory.",
            "classification_required": [
                "Expansion",
                "Consolidation",
                "Plateau"
            ],
            "focus": "adaptation_trajectory",
            "anchor_metrics": [
                "load_trend",
                "fitness_trend",
                "fatigue_trend",
                "Efficiency_Factor",
                "Fatigue_Resistance",
                "phases"
            ],
            "intent_rule": "Determine whether the training block reflects expansion, consolidation, or plateau.",
            "max_sentences": 6
        }
    },

    # ==============================================================
    # Wellness report (PROD-ALIGNED, SIGNAL-FIRST)
    # ==============================================================
    "wellness": {
        "coaching_sentences": {
            "enabled": True,
            "max_per_section": 5,
            "placement": "after_data"
        },
        "interpretation_rules": [
            "Interpret recovery using trends, means, and latest values together.",
            "Explain HRV behaviour (variability, clustering, suppression) when present.",
            "Integrate HRV with CTL, ATL, and TSB within the same section.",
            "Avoid day-by-day narration when aggregates or trends exist."
        ],
        "allowed_enrichment": [
            "Summarise HRV behaviour using peaks, troughs, variability, and clustering.",
            "Explain physiological meaning of HRV suppression vs personal baseline.",
            "Describe maintenance-under-load states when CTL≈ATL and HRV is falling.",
            "Highlight absence of subjective recovery data if present in semantic data.",
            "Include short, non-predictive coach recommendations grounded in signals.",
            "include sleep and RHR Analysis if available"
        ],
        "section_handling": {
            "meta": "full",
            "wellness": "full",
            "hrv_daily": "summary",
            "insights": "full",
            "insight_view": "full",
            "events": "forbid",
            "daily_load": "forbid",
            "metrics": "forbid",
            "extended_metrics": "forbid",
            "zones": "forbid",
            "phases": "forbid"
        },

        # NEW
        "emphasis": {
            "wellness": "high",
            "insights": "high"
        },

        "framing": {
            "intent": "recovery_signal_interpretation"
        },
        "closing_note": {
            "required": True,
            "verdict_rule": "State clearly whether current recovery status supports or constrains ongoing training.",
            "classification_required": [
                "Supported",
                "Borderline",
                "Constrained"
            ],
            "focus": "recovery_validation",
            "anchor_metrics": [
                "HRV",
                "HRV_stability",
                "Autonomic_ratio",
                "Resting_HR_delta",
                "Sleep_score",
                "CTL",
                "ATL",
                "TSB"
            ],
            "intent_rule": "Assess whether autonomic and recovery markers support or constrain training intent.",
            "max_sentences": 4
        }
    },

    # ==============================================================
    # Summary report (ANNUAL / EXECUTIVE)
    # ==============================================================
    "summary": {
        "coaching_sentences": {
            "enabled": True,
            "max_per_section": 5,
            "placement": "after_data"
        },
        "interpretation_rules": [
            "High-level descriptive interpretation only.",
            "Avoid granular metrics or micro-coaching."
        ],
        "allowed_enrichment": [
            "Restate high-level trends explicitly present in semantic data.",
            "show full phases in markdown table."
        ],
        "section_handling": {
            "events": "forbid",
            "daily_load": "forbid",
            "metrics": "summary",
            "extended_metrics": "summary",
            "zones": "summary",
            "wellness": "summary",
            "phases": "full"
        },

        # NEW
        "emphasis": {
            "phases": "high",
            "phases_summary": "high",
            "performance_summary": "high",
            "metrics": "low"
        },

        "framing": {
            "intent": "annual_system_health_review"
        },
        "closing_note": {
            "required": True,
            "verdict_rule": "Deliver a clear system-level sustainability verdict.",
            "classification_required": [
                "Sustainable Growth",
                "Stable Maintenance",
                "Drift Risk"
            ],
            "focus": "system_health",
            "anchor_metrics": [
                "phases",
                "performance_summary",
                "wellness_summary"
            ],
            "intent_rule": "Assess overall system health and sustainability across the review period.",
            "max_sentences": 5
        }
    }
}


REPORT_RESOLUTION = {
    "weekly": {
        "CTL": "authoritative",
        "ATL": "authoritative",
        "TSB": "authoritative",
        "zones": "authoritative",
        "derived_metrics": "full",
        "extended_metrics": "limited",
        "performance_intelligence": "acute_full_7d",
        "insights": "tactical",
    },

    "season": {
        "CTL": "authoritative",
        "ATL": "authoritative",
        "TSB": "authoritative",
        "zones": "not_available",
        "derived_metrics": "trend_only",
        "extended_metrics": "full",
        "performance_intelligence": "acute_overlay_plus_chronic_90d",
        "insights": "strategic",
    },

    "wellness": {
        "CTL": "icu_only",
        "ATL": "icu_only",
        "TSB": "icu_only",
        "zones": "not_applicable",
        "derived_metrics": "wellness_only",
        "extended_metrics": "none",
        "insights": "recovery",
    },

    "summary": {
        "CTL": "icu_only",
        "ATL": "icu_only",
        "TSB": "icu_only",
        "zones": "suppressed",
        "derived_metrics": "suppressed",
        "extended_metrics": "suppressed",
        "insights": "executive",
    },
}

REPORT_HEADERS = {
    "weekly": {
        "title": "Weekly Training Report",
        "scope": "Detailed analysis of the last 7 days of training activity",
        "data_sources": "7-day full activities, 42-day wellness, 90 day light activities",
        "intended_use": (
            "Day-to-day coaching decisions, intensity balance, "
            "short-term fatigue and recovery management"
        ),
    },

    "season": {
        "title": "Season Training Overview",
        "scope": "Medium-term fitness, fatigue and progression trends",
        "data_sources": "90-day light activities, 42-day wellness, weekly aggregates",
        "intended_use": (
            "Strategic assessment of training progression, "
            "load management and phase direction"
        ),
    },

    "wellness": {
        "title": "Wellness & Recovery Status",
        "scope": "Physiological and subjective recovery indicators",
        "data_sources": "42-day wellness records (Intervals native)",
        "intended_use": (
            "Monitoring readiness, recovery balance "
            "and non-training stress"
        ),
    },

    "summary": {
        "title": "Training Summary",
        "scope": "High-level overview of current training state",
        "data_sources": "Authoritative totals, wellness indicators, derived insights",
        "intended_use": (
            "Executive summary and coaching narrative synthesis"
        ),
    },
}


"""
Scientific alignment (URF v5.3)
-------------------------------
• Issurin, V. (2008) – Block Periodization of Training Cycles
• Seiler, S. (2010, 2019) – Hierarchical Organization of Endurance Training
• Mujika & Padilla (2003) – Tapering and Peaking for Performance
• Banister, E.W. (1975) – Impulse–Response Model of Training
• Foster, C. et al. (2001) – Monitoring Training Load with Session RPE

Summary:
✅ phases         → macro-level blocks (Base, Build, Peak, etc.)
✅ phases_detail  → weekly micro-level metrics (TSS, hours, distance)
"""

COACH_PROFILE = {
    "version": "v16.17",
    "bio": {
        "summary": (
            "Data-driven endurance coaching blending objective load metrics "
            "(TSS, CTL, ATL, HRV, VO₂max) with subjective readiness (RPE, mood, recovery). "
            "Implements evidence-based frameworks for phase-specific training adaptation."
        ),
        "domains": [
            "Triathlon", "Cycling", "Running", "Endurance", "Ironman", "Gran Fondo", "Marathon"
        ],
        "principles": [
            "Seiler 80/20 Polarisation", "Banister TRIMP", "Foster Monotony/Strain",
            "San Millán Zone 2", "Friel Periodisation", "Sandbakk Durability",
            "Skiba Critical Power", "Coggan Power Zones", "Noakes Central Governor"
        ]
    },

    "skills_matrix": {
        "load_management": [
            "ACWR", "Strain", "Monotony", "CTL", "ATL", "Form", "TRIMP", "W′/CP Modeling"
        ],
        "recovery_analysis": [
            "LoadVariabilityIndex", "HRV Integration", "Fatigue Detection", "Sleep Quality", "Readiness Tracking"
        ],
        "training_quality": [
            "PolarisationIndex", "DurabilityIndex", "SessionQualityRatio", "FatOxidationIndex"
        ],
        "performance_benchmarking": [
            "BenchmarkIndex", "SpecificityIndex", "ConsistencyIndex", "AgeFactor", "MicrocycleRecoveryWeek"
        ]
    },

    "markers": {
        "ACWR": {
            "framework": "Banister Load Ratio",
            "formula": "EWMA(Acute) / EWMA(Chronic)",
            "criteria": {
                "productive": "0.8–1.3",
                "recovery": "<0.8",
                "overload": ">1.5"
            },
        },
        "Monotony": {
            "framework": "Foster 2001",
            "formula": "Mean_7d / SD_7d",
            "criteria": {
                "optimal": "0–2",
                "moderate": "2.1–2.5",
                "high": ">2.5"
            },
        },
        "Strain": {
            "framework": "Foster 2001",
            "formula": "Monotony × ΣLoad_7d",
            "criteria": {
                "optimal": "<600",
                "moderate": "600–800",
                "high": ">800"
            },
        },
        "FatigueTrend": {
            "framework": "Banister EWMA Delta",
            "formula": "Mean(7d) – Mean(28d)",
            "criteria": {
                "balanced": "-0.2–+0.2",
                "accumulating": ">+0.2",
                "recovering": "<-0.2"
            },
        },
        "StressTolerance": {
            "framework": "Adaptive Load Tolerance",
            "formula": "(strain / monotony) / 100",
            "criteria": {
                "low_exposure": "<3",
                "optimal": "3–6",
                "high": ">6"
            }
        },
        "FatigueResistance": {
            "framework": "Durability / Endurance Resilience Model",
            "formula": "EndurancePower / ThresholdPower",
            "criteria": {
                "low": "<0.9",
                "stable": "0.9–1.0",
                "high": ">1.0"
            },
            "interpretation": (
                "Ratio of endurance to threshold power. "
                "High values indicate preserved performance over long durations."
            ),
            "coaching_implication": (
                "If below 0.9, increase steady endurance work; maintain 0.95–1.0 for optimal durability."
            ),
        },
        "EfficiencyFactor": {
            "framework": "Aerobic Efficiency Index",
            "formula": "Power / HeartRate",
            "criteria": {
                "low": "<1.6",
                "moderate": "1.6–1.8",
                "optimal": "1.8–2.2",
                "high": ">2.2"
            },
            "interpretation": (
                "Power-to-HR ratio indicating aerobic conditioning. "
                "Higher EF suggests improved aerobic efficiency and cardiac economy."
            ),
            "coaching_implication": (
                "If EF decreases, focus on aerobic base and recovery. "
                "Stable or rising EF = strong aerobic fitness trend."
            ),
        },
        "LoadVariabilityIndex": {
            "framework": "Foster Load Variability (Inverse Monotony)",
            "formula": "1 - (Monotony / 5)",
            "criteria": {
                "optimal": "0.7–1.0",
                "moderate": "0.4–0.69",
                "low": "<0.4"
            }
        },
        "FatOxidationIndex": {
            "framework": "San Millán Zone 2 Model",
            "formula": "(1 - |IF - 0.7| / 0.1) × (1 - Decoupling / 10)",
            "criteria": {
                "optimal": ">=0.80",
                "moderate": "0.60–0.79",
                "low": "<0.60"
            },
            "placement": "Training Quality section",
        },
        "FatOxEfficiency": {
            "framework": "San Millán 2020",
            "formula": "Derived from IF × 0.9",
            "criteria": {
                "optimal": "0.6–0.8",
                "low": "<0.5"
            },
        },
                "FOxI": {
            "framework": "Internal Derived Metric",
            "formula": "FatOxEfficiency × 100",
            "criteria": {
                "optimal": ">=70",
                "moderate": "50–69",
                "low": "<50"
            },
            "placement": "Training Quality section"
        },
        "CUR": {
            "framework": "Internal Derived Metric",
            "formula": "100 - FOxI",
            "criteria": {
                "optimal": "20–60",
                "high": ">80",
                "low": "<20"
            },
            "placement": "Training Quality section"
        },
        "GR": {
            "framework": "Internal Derived Metric",
            "formula": "IF × 2.4",
            "criteria": {
                "optimal": "1.5–2.1",
                "moderate": "1.2–1.49",
                "high": ">2.1",
                "low": "<1.2"
            },
            "placement": "Metabolic section"
        },
        "MES": {
            "framework": "Internal Derived Metric",
            "formula": "(FatOxEfficiency × 60) / GR",
            "criteria": {
                "optimal": ">=20",
                "moderate": "10–19",
                "low": "<10"
            },
            "placement": "Metabolic section"
        },
        "ZQI": {
            "framework": "Seiler Intensity Distribution",
            "formula": "High-intensity time (%)",
            "criteria": {
                "optimal": "5–15",
                "moderate": "15–25",
                "low": "<5"
            },
            "placement": "Training Quality section",
        },
        "DurabilityIndex": {
            "framework": "Sandbakk Durability",
            "formula": "1 - (PowerDrop% / 100)",
        },
        "Polarisation": {
            "framework": "Seiler 80/20 Model (Ratio)",
            "formula": "(Z1 + Z3) / (2 × Z2)",
            "criteria": {
                "z2_dominant": "< 0.65",
                "mixed": "0.65–0.84",
                "polarised": "0.85–1.15",
                "high_contrast": "> 1.15"
            },
            "interpretation": (
                "Seiler Polarisation Ratio showing the balance of low- and high-intensity "
                "training (Z1 + Z3) relative to moderate-intensity work (Z2). "
                "<0.65 = Z2-dominant distribution (aerobic or threshold-heavy structure), "
                "0.65–0.84 = mixed intensity distribution, "
                "0.85–1.15 = balanced polarised structure (classic 80/20), "
                ">1.15 = high-contrast polarisation with minimal Z2 exposure. "
                "Dominance reflects intensity distribution characteristics, not training volume."
            ),
            "coaching_implication": (
                "If Polarisation <0.65 in Base, interpret as aerobic/Z2-dominant (acceptable). "
                "If <0.65 in Build or Peak, reduce mid-zone accumulation. "
                "0.85–1.15 reflects structurally balanced 80/20. "
                ">1.15 indicates strong contrast; ensure fatigue and recovery are monitored."
            ),
            "confidence_model": "contextual",
            "confidence_note": (
                "Evaluated at weekly level. Most actionable during Build and Peak phases; "
                "descriptive during Base and Recovery blocks."
            )
        },
        "PolarisationIndex": {
            "framework": "Z1+Z2 Normalized Index",
            "formula": "(Z1 + Z2) / Total zone time",
            "criteria": {
                "aerobic": "≥ 0.75",
                "mixed": "0.6–0.74",
                "intensity_focused": "< 0.6"
            },
            "interpretation": (
                "Normalized time-in-zone index (0–1) representing the proportion of training "
                "spent in low and moderate intensities (Z1+Z2). ≥0.75 = strong aerobic bias "
                "(ideal for Base/Recovery), 0.60–0.74 = balanced, <0.60 = intensity-focused "
                "(typical in Build or Peak phases)."
            ),
            "coaching_implication": (
                "If PolarisationIndex <0.60 and current block = Base, rebalance toward Z1 endurance "
                "and reduce Z2. If <0.60 in Build/Peak, acceptable due to intensity focus. "
                "Target ≥0.75 for strong aerobic adaptation in Base/Recovery."
            ),
            "confidence_model": "contextual",
            "confidence_note": (
                "Weekly distribution signal. Interpretation depends on phase intent "
                "(aerobic accumulation vs intensity expression)."
            ),
        },
        "Polarisation_fused": {
            "framework": "Seiler / Stöggl / Issurin (HR+Power fused)",
            "formula": "Normalized intensity-domain distribution (fused HR+Power)",
            "criteria": {
                "polarised": "≥ 0.80",
                "pyramidal": "0.65–0.79",
                "threshold_dominant": "< 0.65"
            },
            "interpretation": (
                "Derived per sport from HR+Power fusion. Reflects dominant-sport load separation. "
                "Dominant sport is defined by clarity of zone-distribution signal (HR or power), "
                "not by total duration, distance, or training load."
            ),
            "coaching_implication": (
                "If <0.7 in Base → aerobic focus (✅). "
                "If <0.7 in Build/Peak → excessive mid-zone; rebalance toward Z1/Z3 contrast."
            ),
            "confidence_model": "contextual",
            "confidence_note": (
                "Valid when one sport clearly dominates intensity signalling. "
                "Less reliable with evenly mixed multi-sport weeks."
            ),
        },
        "Polarisation_combined": {
            "framework": "Seiler / Stöggl / Issurin (multi-sport combined)",
            "formula": "Normalized global intensity-domain distribution",
            "criteria": {
                "polarised": "≥ 0.80",
                "pyramidal": "0.65–0.79",
                "threshold_dominant": "< 0.65"
            },
            "interpretation": (
                "Weighted mean of sport-specific fused indices. Represents overall cross-sport "
                "intensity distribution. Dominance reflects intensity signal weighting, "
                "not primary sport or training volume."
            ),
            "coaching_implication": (
                "Maintain ≥0.8 global balance for healthy load variation. "
                "If <0.65 → add Z1 endurance days or rest."
            ),
            "confidence_model": "contextual",
            "confidence_note": (
                "High-level weekly descriptor only. Not intended for session-level judgement."
            ),
        },
        "TRIMP": {
            "framework": "Banister Load Model",
            "formula": "Duration × HR_ratio × e^(1.92 × HR_ratio)",
        },
        "Readiness": {
            "framework": "Noakes Central Governor",
            "formula": "0.3×Mood + 0.3×Sleep + 0.2×Stress + 0.2×Fatigue",
        },
        "BenchmarkIndex": {
            "framework": "Friel Functional Benchmarking",
            "formula": "(FTP_current / FTP_prior) - 1",
            "criteria": {
                "productive": "+2–5%",
                "stagnant": "0%",
                "regression": ">−3%"
            },
        },
        "SpecificityIndex": {
            "framework": "Friel Specificity Ratio",
            "formula": "race_specific_hours / total_hours",
            "criteria": {
                "peak": "0.70–0.90",
                "build": "0.50–0.69",
                "base": "<0.50"
            },
        },
        "ConsistencyIndex": {
            "framework": "Friel Consistency Metric",
            "formula": "completed_sessions / planned_sessions",
            "criteria": {
                "consistent": ">=0.90",
                "variable": "0.75–0.89",
                "inconsistent": "<0.75"
            },
        },
        "AgeFactor": {
            "framework": "Friel Aging Adaptation",
            "formula": "ATL_adj = ATL × (1 - 0.005 × (Age - 40))",
        },
        # --- Supplemental markers synced from CHEAT_SHEET thresholds ---
        "Durability": {
            "framework": "Sandbakk Durability",
            "formula": "Power_stability under fatigue",
            "criteria": {
                "optimal": ">=0.90",
                "moderate": "0.70–0.89",
                "low": "<0.70"
            }
        },
        "LIR": {
            "framework": "Load Intensity Ratio",
            "formula": "Intensity / Duration",
            "criteria": {
                "balanced": "0.8–1.2",
                "high": ">1.2",
                "low": "<0.8"
            }
        },
        "EnduranceReserve": {
            "framework": "Durability Reserve Index",
            "formula": "AerobicDurability / FatigueIndex",
            "criteria": {
                "strong": ">=1.2",
                "moderate": "0.8–1.19",
                "depleted": "<0.8"
            }
        },
        "IFDrift": {
            "framework": "Efficiency Drift",
            "formula": "ΔIF over time",
            "criteria": {
                "stable": "0.0–0.05",
                "moderate": "0.05–0.10",
                "high": ">0.10"
            }
        },
        "Lactate": {
            "framework": "Mader-Heck 1986",
            "formula": "LT1/LT2 correlation threshold",
            "criteria": {
                "low": "<2.0",
                "moderate": "2.0–4.0",
                "high": ">4.0"
            }
        },
        "LoadVariabilityIndex": {
            "framework": "Autonomic–Load Coupling Index",
            "formula": "(HRV / HRV_mean) × (TSB / 10)",
            "criteria": {
                "low": "<0.5",
                "moderate": "0.5–0.6",
                "optimal": "0.6–0.9",
                "high": ">0.9"
            }
        },
        "HRV": {
            "framework": "Autonomic Recovery Model",
            "formula": "Mean vs Latest HRV (ms)",
            "criteria": {
                "optimal": ">=60",
                "moderate": "40–59",
                "low": "<40"
            }
        },
        "RestingHR": {
            "framework": "Cardiac Recovery Model",
            "formula": "Resting HR (bpm)",
            "criteria": {
                "optimal": "32–60",
                "moderate": "61–70",
                "high": ">70"
            }
        },
        "RestingHRDelta": {
            "framework": "Cardiac Recovery Trend",
            "formula": "Δ7–28 day Resting HR",
            "criteria": {
                "optimal": "-2–2",
                "moderate": "2–5",
                "high": ">5"
            }
        },
        "SleepQuality": {
            "framework": "Sleep Hygiene & Recovery Model",
            "formula": "Average Sleep Score (14 days)",
            "criteria": {
                "optimal": "80–100",
                "moderate": "65–79",
                "low": "<65"
            }
        },
        "HRVBalance": {
            "framework": "Autonomic Recovery Model",
            "formula": "Latest HRV / Mean HRV",
            "criteria": {
                "optimal": "1.0–1.3",
                "moderate": "0.9–0.99",
                "low": "<0.9"
            }
        },
        "HRVStability": {
            "framework": "Variability Index",
            "formula": "1 - (std / mean) (14d)",
            "criteria": {
                "optimal": ">=0.85",
                "moderate": "0.7–0.84",
                "low": "<0.7"
            }
        },
        "HRVTrend": {
            "framework": "Short-Term HRV Trend",
            "formula": "Linear slope (7d)",
            "criteria": {
                "optimal": ">=0",
                "moderate": "-2–-0.01",
                "low": "<-2"
            }
        },
    },

    "metadata": {
        "framework_chain": [
            "Seiler", "Banister", "Foster", "San Millán", "Friel",
            "Sandbakk", "Skiba", "Coggan", "Noakes"
        ],
        "unified_framework": "v5.1",
        "audit_validation": "Tier-2 verified, event-only totals enforced",
        "variance": "<= 2%",
        "last_revision": "2025-11-03"
    }
}

# Alias for compatibility with derived metrics imports
PROFILE_DATA = COACH_PROFILE
