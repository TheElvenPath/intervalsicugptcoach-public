#!/usr/bin/env python3
"""
coaching_profile.py — Unified Coaching Profile (v17-Sync)
Structured reference of frameworks, formulas, and methodology anchors. UPD
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
        "meta",

        # 🧭 TRAINING LOAD
        "training_volume",
        "metrics",
        "daily_load",
        "events",

        # 🫀 PHYSIOLOGY RESPONSE
        "wellness",
        "insight_view",

        # ⚙️ PERFORMANCE INTELLIGENCE
        "performance_intelligence",
        "wbal_summary",

        # 📈 ADAPTATION
        "energy_system_progression",
        "physiology",
        "zones",

        # 🎯 ADAPTIVE DECISIONS
        "actions",
        "planned_events",
        "planned_summary_by_date",
        "current_ISO_weekly_microcycle",
        "future_forecast",
        "future_actions",

        # hidden narrative (not rendered)
        "phases",
        "insights",
    ],


    "season": [
        "meta",

        # 🧭 TRAINING LOAD
        "training_volume",
        "metrics",
        "trend_metrics",

        # 🫀 PHYSIOLOGY RESPONSE
        "adaptation_metrics",
        "insight_view",

        # ⚙️ PERFORMANCE INTELLIGENCE
        "performance_intelligence",
        "wbal_summary",

        # 📈 ADAPTATION
        "energy_system_progression",
        "physiology",
        "phases",
        "phases_summary",

        # 🎯 ADAPTIVE DECISIONS
        "actions",
        "future_forecast",
        "future_actions",

        # hidden narrative
        "insights",
    ],


    "summary": [
        "meta",

        # 🧭 TRAINING LOAD
        "training_volume",

        # 🫀 PHYSIOLOGY RESPONSE
        "wellness",

        # ⚙️ PERFORMANCE INTELLIGENCE
        "performance_summary",

        # 📈 ADAPTATION
        "phases",
        "phases_summary",

        # hidden narrative
        "insights",
    ],


    "wellness": [
        "meta",

        # 🫀 PHYSIOLOGY RESPONSE
        "wellness",
        "insights",
        "insight_view",

        # ⚙️ PERFORMANCE INTELLIGENCE
        "performance_intelligence",
    ]
}

RENDERER_PROFILES = {

    # ==============================================================
    # Global rules (apply to ALL report types)
    # ==============================================================
    "global": {
        "hard_rules": [
            "Render exactly ONE report.",
            "All sections MUST appear under their corresponding stack layer header.",
            "Stack layer headers MUST be rendered using the provided stack labels in uppercase.",
            "Do NOT add numeric prefixes to section headers.",
            "Use emoji-based section headers only.",
            "Preserve section order exactly as defined by the contract.",
            "Metric context MUST be derived exclusively from each metric’s `context_window` and `confidence_model` fields.",
            "When both wellness signals and performance_intelligence metrics are present, interpret recovery state as the physiological response to recent training stress. Insights should reconcile these layers rather than repeating them independently."
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
        "stack_structure": {
            "meta_context": [
                "meta"
            ],
            "training_load": [
                "training_volume",
                "metrics",
                "daily_load",
                "events"
            ],

            "physiology_response": [
                "wellness",
                "insight_view",
            ],

            "performance_intelligence": [
                "performance_intelligence",
                "wbal_summary",
            ],

            "adaptation": [
                "energy_system_progression",
                # physiological calibration
                "physiology",
                "zones",
            ],

            "adaptive_decisions": [
                "actions",
                "planned_events",
                "planned_summary_by_date",
                "current_ISO_weekly_microcycle",
                "future_forecast",
                "future_actions",
            ]
        },
        "stack_labels": {
            "meta_context": "📊 REPORT CONTEXT",
            "training_load": "🧭 TRAINING LOAD",
            "physiology_response": "🫀 PHYSIOLOGY RESPONSE",
            "performance_intelligence": "⚙️ PERFORMANCE INTELLIGENCE",
            "adaptation": "📈 ADAPTATION",
            "adaptive_decisions": "🎯 ADAPTIVE DECISIONS"
        },
        "coaching_sentences": {
            "enabled": True,
            "max_per_section": 5,
            "placement": "after_data"
        },
        "interpretation_rules": [
            "Interpretations may be descriptive or conditional, not predictive.",
            "If semantic.training_volume exists, render it under the header 'Training Volume' with three stacked metrics: Hours, Training Load (TSS), Distance.",
            "If semantic.wbal_summary.temporal_pattern exists, render a one-line anaerobic load timeline using block symbols (▂ ▃ ▇) mapped to none/low/moderate/high.",
            "If semantic.daily_load exists, render it as a compact monoblock map timeline with weekday labels, relative load blocks, and numeric TSS values aligned underneath. Do NOT render daily_load as a list or table.",
            "If semantic.daily_load exists AND semantic.wellness.CTL and semantic.wellness.ATL are present, a second symbolic fatigue-pressure row MAY be rendered using ↑ ↓ — symbols based ONLY on the sign of (ATL − CTL). No magnitude, thresholds, or new calculations are permitted.",
            "All rows in the daily load timeline MUST use a fixed-width column per day to ensure vertical alignment across labels, blocks, symbols, and numeric values.",
            "If session-level signal icons are rendered in the EVENTS table, a single legend line MUST be rendered once per report directly below the EVENTS section header.",
            "If zone distribution data exists (e.g. zone_dist_power, zone_dist_hr, zone_dist_fused), render zone distribution as fixed-width ASCII proportional bars (one bar per zone), with the exact percentage shown. Bars are presentational only and do not constitute derived metrics.",
            "If semantic.zones.lactate_calibration exists and lactate.available is true, render a Lactate Calibration subsection summarising mean mmol/L, latest mmol/L, sample count, and inferred LT1 power. This is descriptive only and must not derive new values.",
            "If performance_intelligence exists, render three subsections: Anaerobic Repeatability (WDRM), Durability (ISDM), Neural Density (NDLI). Use provided values only. Do NOT recompute or merge with other metrics.",
            "If high_dep_sessions > 0 and high_drift_sessions > 0 in the same week, describe this as high neuromuscular + metabolic strain overlap.",
            "Interpretation may combine signals across sections when they describe the same physiological process (e.g. fatigue, adaptation, durability).",
            "When energy_system_progression exists, generate at least one sentence summarising the current adaptation direction using system_status and adaptation_state.",
            "Insights SHOULD prioritise adaptation signals (ESPE) before repeating metric definitions.",
            "When activity_link exists inside energy_system_progression.power_curve_anchors.values, the corresponding power value MUST be rendered as a Markdown link using the format: [<power> W](activity_link).",
            "If activity_link is missing, the power value MUST be rendered normally without a link."
        ],
        "allowed_enrichment": [
            "Restate semantic interpretation fields.",
            "Explain what a value indicates within its known threshold or state.",
            "derive_stepwise_forecast"
        ],
        "section_handling": {
            "meta": "full",
            "training_volume": "full",
            "events": "full",
            "current_ISO_weekly_microcycle": "full",
            "daily_load": "full",
            "metrics": "summary",
            "extended_metrics": "forbid",
            "performance_intelligence": "full",
            "energy_system_progression": "full",
            "zones": "forbid",
            "physiology": "full",
            "wellness": "summary",
            "phases": "forbid",
            "planned_events": "full",
            "planned_summary_by_date": "forbid",
            "actions": "full",
            "future_actions": "full",
            "insights": "forbid",
            "insight_view": "summary"
        },

        "emphasis": {
            "metrics": "high",
            "actions": "high",
            "events": "medium",
            "wellness": "medium",
            "adaptation": "high"
        },

        "events_rule": {
            "column_order": [
                "Date",
                "Activity",
                "Duration (min)",
                "Distance",
                "TSS",
                "IF",
                "NP",
                "HRR60"
            ],

            "duration_conversion": [
                "The semantic field `duration_seconds` MUST be converted to minutes at render time.",
                "This conversion applies ONLY to duration.",
                "Display as integer minutes by default.",
                "Use one decimal only if duration < 30 minutes and precision is useful.",
                "Label column as Duration (min). Show HRR60 column when values exist."
            ],

            "icons": [
                "⚡ Efficient (optimal efficiency factor)",
                "🟢 Aerobic (low IF with stable decoupling)",
                "💥 Anaerobic (heavy W′ engagement)",
                "🔁 Repeated (repeated W′ depletion pattern)",
                "📈 Progressive (progressive W′ engagement)",
                "🧘 Recovery (very low intensity recovery session)",
                "❤️ Heart_rate_recovery_60s (Heart Rate Recovery within 60s)"
            ],

            "rules": [
                "The events section MUST be rendered as a Markdown table.",
                "EVERY event in the semantic JSON MUST appear as exactly one row.",
                "The events section MUST NOT be summarised, renamed, grouped, or rewritten.",
                "Bullet points, highlights, or narrative descriptions of events are FORBIDDEN.",
                "Coaching sentences for events, if enabled, MUST appear AFTER the table.",
                "The EVENTS table MUST use the defined column order.",
                "In the EVENTS table, session-level signal icons MAY be rendered within the Activity column as a prefix using the canonical mapping derived ONLY from existing semantic fields.",
                "Icons represent independent session signals and MAY appear together for a single event.",
                "Add rpe_emoji and feel_emoji to the right of TSS value tightly coupled.",
                "When multiple icons apply, they MUST be rendered together in the defined fixed order.",
                "Icons are visual aliases only and must not replace numeric values, suppress other applicable icons, or reduce table rows.",
                "When `activity_link` exists, the Activity column MUST render the activity name as a Markdown link: [name](activity_link).",
                "Icons MUST appear before the link inside the same Activity cell.",
                "Show icon legends underneath the table tightly coupled."
            ]
        },

        "planned_events_rule": [
            "The planned_events section MUST be rendered as a Markdown table.",
            "EVERY planned event in the semantic JSON MUST appear as exactly one row.",
            "The planned_events section MUST NOT be summarised, renamed, grouped, or rewritten.",
            "Narrative descriptions of planned events are FORBIDDEN.",
            "Coaching sentences for planned_events, if enabled, MUST appear AFTER the table."
        ],

        "framing": {
            "intent": "tactical_weekly_control"
        },
        "question_rule": {
            "fatigue",
            "adaptation",
            "training load",
            "perceived exertion (RPE / feel)"
        },
        "closing_note": {
            "required": True,
            "verdict_rule": "State clearly whether last week’s training load was handled appropriately.",
            "classification_required": [
                "Productive",
                "High Strain",
                "Overreached"
            ],
            "focus": "tactical_alignment",
            "anchor_metrics": [
                "ACWR",
                "FatigueTrend",
                "NDLI",
                "Durability",
                "performance_intelligence.training_state",
                "energy_system_progression"
            ],
            "intent_rule": "Assess whether acute load and recovery state align with immediate training intent.",
            "max_sentences": 4
        }
    },

    # ==============================================================
    # Season report (PHASE-LEVEL, STRATEGIC)
    # ==============================================================
    "season": {
        "stack_structure": {
            "meta_context": [
                "meta"
            ],
            "training_load": [
                "training_volume",
                "metrics",
                "trend_metrics"
            ],

            "physiology_response": [
                "adaptation_metrics",
                "insights_view"
            ],

            "performance_intelligence": [
                "performance_intelligence",
                "wbal_summary"
            ],

            "adaptation": [
                "energy_system_progression",
                "physiology",
                "phases",
                "phases_summary"
            ],

            "adaptive_decisions": [
                "actions",
                "future_forecast",
                "future_actions"
            ]
        },

        "stack_labels": {
            "meta_context": "📊 REPORT CONTEXT",
            "training_load": "🧭 TRAINING LOAD",
            "physiology_response": "🫀 PHYSIOLOGY RESPONSE",
            "performance_intelligence": "⚙️ PERFORMANCE INTELLIGENCE",
            "adaptation": "📈 ADAPTATION",
            "adaptive_decisions": "🎯 ADAPTIVE DECISIONS"
        },

        "coaching_sentences": {
            "enabled": True,
            "max_per_section": 5,
            "placement": "after_data"
        },
        "interpretation_rules": [
            "If semantic.training_volume exists, render it under the header 'Training Volume' with three stacked metrics: Hours, Training Load (TSS), Distance.",
            "Focus on trends, phases, and accumulated load.",
            "Avoid session-level or daily commentary.",
            "If performance_intelligence exists, render chronic signals (90d) first, then acute signals (7d). Emphasise contrast between long-term capacity and current stress.",
            "Interpretation may combine signals across sections when they describe the same physiological process (e.g. fatigue, adaptation, durability).",
            "When energy_system_progression exists, generate at least one sentence summarising the current adaptation direction using system_status and adaptation_state.",
            "Insights SHOULD prioritise adaptation signals (ESPE) before repeating metric definitions.",
        ],
        "allowed_enrichment": [
            "Restate phase descriptors already present in semantic data."
        ],
        "section_handling": {
            "meta": "full",
            "training_volume": "full",
            "events": "forbid",
            "daily_load": "forbid",
            "weekly_phases": "forbid",
            "phases": "summary",
            "phases_summary": "full",
            "metrics": "table_summary",
            "extended_metrics": "forbid",
            "performance_intelligence": "full",
            "energy_system_progression": "summary",
            "physiology": "summary",
            "wellness": "summary",
            "actions": "full",
            "future_actions": "full",
            "insights": "forbid",
            "insight_view": "summary"
        },

        "emphasis": {
            "phases_summary": "high",
            "trend_metrics": "high",
            "metrics": "medium",
            "adaptation": "high"
        },

        "framing": {
            "intent": "medium_term_block_assessment"
        },
        "question_rule": {
            "adaptation",
            "training progression",
            "durability",
            "fatigue accumulation"
        },
        "closing_note": {
            "required": True,
            "verdict_rule": "Classify the training block adaptation trajectory.",
            "classification_required": [
                "Adaptive Growth",
                "Adaptive Maintenance",
                "Adaptive Saturation"
            ],
            "focus": "adaptation_trajectory",
            "anchor_metrics": [
                "load_trend",
                "fitness_trend",
                "fatigue_trend",
                "Efficiency_Factor",
                "Fatigue_Resistance",
                "phases_summary",
                "performance_intelligence.chronic",
                "performance_intelligence.acute",
                "performance_intelligence.training_state",
                "energy_system_progression",
            ],
            "intent_rule": "Determine whether the training block reflects expansion, consolidation, or plateau.",
            "max_sentences": 6
        }
    },

    # ==============================================================
    # Wellness report (URF v5.2 — SIGNAL-FIRST, MULTI-LAYER RECOVERY)
    # ==============================================================
    "wellness": {

        "stack_structure": {
            "meta_context": [
                "meta"
            ],
            "physiology_response": [
                "wellness",
                "insight_view"
            ],

            "performance_intelligence": [
                "performance_intelligence"
            ]
        },

        "stack_labels": {
            "meta_context": "📊 REPORT CONTEXT",
            "physiology_response": "🫀 PHYSIOLOGY RESPONSE",
            "performance_intelligence": "⚙️ TRAINING STRESS CONTEXT"
        },

        "coaching_sentences": {
            "enabled": True,
            "max_per_section": 4,
            "placement": "after_data"
        },

        # ----------------------------------------------------------
        # Signal hierarchy (used by prompt builder)
        # ----------------------------------------------------------

        "signal_hierarchy": [
            "Autonomic signals (HRV, HRV stability, resting HR, sleep)",
            "Load context (CTL, ATL, TSB, FatigueTrend)",
            "Training stress mechanisms (from performance_intelligence: neural density, durability drift, anaerobic depletion)"
        ],

        # ----------------------------------------------------------
        # Interpretation rules
        # ----------------------------------------------------------

        "interpretation_rules": [
            "Interpret recovery primarily using autonomic and subjective signals (HRV, resting HR, sleep, subjective recovery scores).",
            "Prioritise autonomic signals over training load metrics when determining recovery state.",
            "Explain HRV behaviour using trends, means, variability, and recent values relative to baseline.",
            "Use CTL, ATL, and TSB only as contextual load indicators, not as primary fatigue determinants.",
            "Avoid day-by-day narration when aggregates or trends exist.",
            "When HRV remains stable despite elevated ATL, describe this as maintenance-under-load adaptation.",
            "When autonomic signals disagree with load signals, prioritise autonomic interpretation.",
            "Performance intelligence metrics must only provide context explaining training stress exposure.",
            "When rendered in a wellness report, performance intelligence MUST appear as a single condensed headline-style block (maximum 3–4 indicators).",
            "Do NOT analyse training performance, workout structure, or detailed training metrics in this report."
        ],

        # ----------------------------------------------------------
        # Allowed enrichment
        # ----------------------------------------------------------

        "allowed_enrichment": [
            "Summarise HRV behaviour using peaks, troughs, variability, and clustering.",
            "Explain physiological meaning of HRV suppression relative to personal baseline.",
            "Describe maintenance-under-load states when CTL≈ATL and HRV is stable.",
            "Explain interaction between HRV behaviour and training load.",
            "Include sleep and resting heart rate analysis when available.",
            "Highlight absence of subjective recovery data when relevant.",
            "Describe possible neural or durability fatigue only when supported by insight metrics.",
            "Reference performance_intelligence stress metrics when explaining recovery tolerance."
        ],

        # ----------------------------------------------------------
        # Section rendering
        # ----------------------------------------------------------

        "section_handling": {
            "meta": "full",
            "wellness": "full",
            "hrv_daily": "table_summary",
            "performance_intelligence": "headine",
            "insights": "forbid",
            "insight_view": "full",
            "events": "forbid",
            "daily_load": "forbid",
            "metrics": "forbid",
            "extended_metrics": "forbid",
            "zones": "forbid",
            "phases": "forbid"
        },

        # ----------------------------------------------------------
        # Narrative emphasis
        # ----------------------------------------------------------

        "emphasis": {
            "wellness": "high",
            "insight_view": "high",
            "autonomic_signals": "high",
            "performance_intelligence": "low",
            "load_context": "low",
            "stress_mechanisms": "low"
        },

        # ----------------------------------------------------------
        # Framing intent
        # ----------------------------------------------------------

        "framing": {
            "intent": "recovery_signal_interpretation",
            "model": "multi_layer_recovery"
        },

        # ----------------------------------------------------------
        # Fatigue interpretation guardrails
        # ----------------------------------------------------------

        "fatigue_logic": [
            "Do not infer fatigue from load metrics alone.",
            "FatigueTrend represents load equilibrium relative to the baseline window.",
            "Autonomic suppression combined with elevated ATL indicates recovery pressure.",
            "Stable HRV despite elevated ATL indicates productive adaptation under load."
        ],
        "question_rule": {
            "recovery",
            "fatigue perception",
            "sleep quality",
            "morning readiness"
        },

        # ----------------------------------------------------------
        # Closing note
        # ----------------------------------------------------------

        "closing_note": {

            "required": True,

            "classification_required": [
                "Adapting Well",
                "Adaptation Under Pressure",
                "Maladaptation Risk"
            ],

            "verdict_rule":
                "State clearly whether current recovery status supports or constrains ongoing training.",

            "focus": "recovery_validation",

            "anchor_metrics": [
                "HRV",
                "HRV_stability",
                "Autonomic_ratio",
                "Resting_HR_delta",
                "Sleep_score",
                "CTL",
                "ATL",
                "TSB",
                "performance_intelligence"
            ],

            "intent_rule":
                "Assess whether autonomic and recovery markers support or constrain training intent.",

            "exact_sentences": 5,

            "sentence_structure": [
                "1. State classification.",
                "2. Describe HRV behaviour relative to baseline.",
                "3. Describe interaction with CTL, ATL, and TSB.",
                "4. Explain physiological meaning (autonomic balance or strain).",
                "5. Translate into plain language (how the body is coping).",
                "6. Provide concrete guidance for the next 24–72 hours."
            ]
        }
    },

    # ==============================================================
    # Summary report (ANNUAL / EXECUTIVE)
    # ==============================================================
    "summary": {
        "stack_structure": {

            "meta_context": [
                "meta"
            ],

            "training_load": [
                "training_volume"
            ],

            "physiology_response": [
                "wellness"
            ],

            "performance_intelligence": [
                "performance_summary"
            ],

            "adaptation": [
                "phases",
                "phases_summary"
            ]
        },

        "stack_labels": {
            "meta_context": "📊 REPORT CONTEXT",
            "training_load": "🧭 TRAINING LOAD",
            "physiology_response": "🫀 PHYSIOLOGY RESPONSE",
            "performance_intelligence": "⚙️ PERFORMANCE INTELLIGENCE",
            "adaptation": "📈 ADAPTATION"
        },

        "coaching_sentences": {
            "enabled": True,
            "max_per_section": 5,
            "placement": "after_data"
        },
        "interpretation_rules": [
            "If semantic.training_volume exists, render it under the header 'Training Volume' with three stacked metrics: Hours, Training Load (TSS), Distance.",
            "High-level descriptive interpretation only.",
            "Avoid granular metrics or micro-coaching."
        ],
        "allowed_enrichment": [
            "Restate high-level trends explicitly present in semantic data.",
            "show full phases in markdown table."
        ],
        "section_handling": {
            "meta": "full",
            "training_volume": "full",
            "daily_load": "forbid",
            "wellness": "summary",
            "phases": "forbid",
            "phases_summary": "full",
            "insight_view": "forbid",
            "insights": "forbid",
        },
        
        "emphasis": {
            "phases": "high",
            "phases_summary": "high",
            "performance_summary": "high",
            "metrics": "low"
        },

        "framing": {
            "intent": "annual_system_health_review"
        },
        "question_rule": {
            "long-term training sustainability",
            "adaptation progression",
            "training consistency",
            "fatigue management across the season"
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
        "extended_metrics": "none",
        "performance_intelligence": "acute_full_7d",
        "energy_system_progression": "full",
        "insights": "tactical",
    },

    "season": {
        "CTL": "authoritative",
        "ATL": "authoritative",
        "TSB": "authoritative",
        "zones": "not_available",
        "derived_metrics": "trend_only",
        "extended_metrics": "none",
        "performance_intelligence": "acute_7d_plus_chronic_90d",
        "energy_system_progression": "adaptation",
        "insights": "strategic",
    },

    "wellness": {
        "CTL": "icu_only",
        "ATL": "icu_only",
        "TSB": "icu_only",
        "zones": "not_applicable",
        "derived_metrics": "wellness_only",
        "extended_metrics": "none",
        "performance_intelligence": "acute_full_7d",
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
            "Seiler 3-Zone Polarisation","Treff Polarization-Index (2019)", "Banister TRIMP", "Foster Monotony/Strain",
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
            "Polarisation (Seiler 3-zone)",
            "PolarisationIndex (Treff 2019)",
            "DurabilityIndex",
            "SessionQualityRatio",
            "FatOxidationIndex"
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
                "recovery": "<0.8",
                "productive": "0.8–1.3",
                "aggressive": "1.3–1.5",
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
            "framework": "Modified Foster 2001 (TSS-based)",
            "formula": "Monotony × ΣTSS_7d",
            "criteria": {
                "low": "<2000",
                "moderate": "2000–3000",
                "high": "3000–4000",
                "very_high": ">4000"
            }
        },
        "FatigueTrend": {
            "framework": "Banister EWMA Delta",
            "formula": "(Mean_7d - Mean_28d) / Mean_28d × 100",
            "criteria": {
                "balanced": "-10–10",
                "moderate_low": "-20–-10",
                "moderate_high": "10–20",
                "accumulating": "20–40",
                "extreme_accumulation": ">40",
                "recovering": "<-20"
            }
        },
        "StressTolerance": {
            "framework": "Banister Capacity-Adjusted Load Ratio",
            "formula": "ΣTSS_7d / (CTL × 7)",
            "criteria": {
                "underload": "<0.8",
                "optimal": "0.8–1.2",
                "aggressive": "1.2–1.4",
                "overreach_risk": ">1.4"
            },
        },
        "FatigueResistance": {
            "framework": "Durability / Endurance Resilience Model",
            "formula": "EndurancePower / ThresholdPower",
            "criteria": {
                "low": "<0.8",
                "stable": "0.8–0.9",
                "optimal": "0.9–1.1",
                "high": "1.1–1.2",
                "extreme": ">1.2"
            },
        },
        "EfficiencyFactor": {
            "framework": "Aerobic Efficiency Index",
            "formula": "Power / HeartRate",
            "criteria": {
                "low": "<1.5",
                "moderate": "1.5–1.8",
                "optimal": "1.8–2.2",
                "high": "2.2–2.5",
                "extreme": ">2.5"
            },
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
                "optimal": "0.60–0.80",
                "moderate": "0.50–0.59",
                "low": "<0.50"
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
                "balanced": "30–70",
                "moderate_low": "20–29",
                "moderate_high": "71–80",
                "low_carb_bias": "<20",
                "high_carb_bias": ">80"
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
            "formula": "Z3+ time (%) from 3-zone collapsed model",
            "criteria": {
                "low": "<5",
                "optimal": "5–15",
                "high": "15–25",
                "excessive": ">25"
            },
        },
        "DurabilityIndex": {
            "framework": "Sandbakk Durability",
            "formula": "1 - (PowerDrop% / 100)",
        },
        "Polarisation": {
            "framework": "Seiler 3-Zone Contrast Model",
            "formula": "(Z1 + Z3+) / (2 × Z2)  (3-zone collapsed, renormalised)",
            "criteria": {
                "z2_dominant": "< 0.65",
                "pyramidal": "0.65–0.84",
                "polarised": "0.85–1.25",
                "high_contrast": "> 1.25"
            },
        },
        "PolarisationIndex": {
            "framework": "Treff 2019 Polarization-Index",
            "formula": "log10( Z1 / (Z2 × Z3) × 100 )  (3-zone collapsed)",
            "criteria": {
                "threshold_dominant": "< 1.5",
                "pyramidal": "1.5–1.99",
                "polarised": "≥ 2.0"
            },
        },
        "Polarisation_fused": {
            "framework": "Seiler / Stöggl / Issurin (HR+Power fused)",
            "formula": "Normalized intensity-domain distribution (fused HR+Power)",
            "criteria": {
                "polarised": "≥ 0.80",
                "pyramidal": "0.65–0.79",
                "threshold_dominant": "< 0.65"
            },
        },
        "Polarisation_combined": {
            "framework": "Seiler / Stöggl / Issurin (multi-sport combined)",
            "formula": "Normalized global intensity-domain distribution",
            "criteria": {
                "polarised": "≥ 0.78",
                "pyramidal": "0.65–0.77",
                "threshold_dominant": "< 0.65"
            },
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
        "vo2_reserve_ratio": {
            "framework": "Critical Power / VO₂ Reserve Model",
            "formula": "P5m / CP",
            "interpretation": "Ratio of 5-minute power to Critical Power reflecting VO₂ headroom above threshold.",
            "coaching_implication": "Lower ratios indicate fatigue or VO₂ limitation.",
        },

        "pdr_5m": {
            "framework": "Power Duration Reserve",
            "formula": "P5m − CP",
            "interpretation": "Difference between 5-minute power and Critical Power representing VO₂ reserve capacity.",
            "coaching_implication": "Higher reserve suggests strong VO₂ capacity above threshold.",
        },

        "durability_gradient": {
            "framework": "Durability Gradient Model",
            "formula": "P60 / P20",
            "interpretation": "Ratio of 60-minute power to 20-minute power reflecting fatigue resistance across prolonged efforts.",
            "coaching_implication": "Lower gradients indicate durability decline during long efforts.",
        },

        "glycolytic_bias_ratio": {
            "framework": "Energy System Balance Model",
            "formula": "P1m / CP",
            "interpretation": "Ratio of short-duration power to threshold power indicating glycolytic dominance.",
            "coaching_implication": "High values suggest anaerobic bias relative to aerobic capacity.",
        },

        "aerobic_durability_ratio": {
            "framework": "Durability / Endurance Model",
            "formula": "P60 / CP",
            "interpretation": "Ratio of 60-minute power to 5-minute power reflecting endurance durability across prolonged efforts.",
            "coaching_implication": "Lower ratios suggest fatigue-driven endurance drop-off.",
        },

        "system_balance_score": {
            "framework": "Energy System Balance Composite",
            "formula": "Composite ESPE score across anaerobic, VO₂, threshold and durability systems",
            "interpretation": "Composite indicator describing balance of energy system development.",
            "coaching_implication": "Values closer to 1 indicate balanced development across systems.",
        },
        "LoadRecoveryState": {
            "framework": "HRV–Load Interaction Model (Plews 2013; Banister 1975)",
            "formula": "HRV_autonomic_ratio interpreted alongside ATL − CTL load pressure",
            "interpretation": (
                "Qualitative state describing the interaction between autonomic recovery "
                "(HRV relative to baseline) and current training load pressure (ATL vs CTL)."
            ),
            "criteria": {
                "balanced": "Recovery signals aligned with training load.",
                "productive_load": "Training load elevated but autonomic recovery stable.",
                "adaptation_pressure": "Autonomic recovery suppressed under elevated load.",
                "maladaptation_risk": "Recovery breakdown relative to training stress."
            },
            "coaching_implication": (
                "Helps determine whether current training load is being productively absorbed "
                "or whether recovery capacity is being exceeded."
            )
        },
    },
    "metadata": {
        "framework_chain": [
            "Seiler", "Treff 2019", "Banister", "Foster", "San Millán",
            "Friel", "Sandbakk", "Skiba", "Coggan", "Noakes","Plews–Banister Interaction Framework"
        ],
        "unified_framework": "v5.1",
        "audit_validation": "Tier-2 verified, event-only totals enforced",
        "variance": "<= 2%",
        "last_revision": "2025-11-03"
    }
}

# Alias for compatibility with derived metrics imports
PROFILE_DATA = COACH_PROFILE
