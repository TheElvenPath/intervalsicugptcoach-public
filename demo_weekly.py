# demo_weekly.py

DEMO_WEEKLY = {
  "meta": {
    "framework": "V5.1 Unified Reporting Framework",
    "version": "v16.17",
    "methodology": {
      "source": "Unified Coaching Reference (Intervals + Seiler + Banister)",
      "summary": "Data-driven endurance coaching blending objective load metrics (TSS, CTL, ATL, HRV, VO\u2082max) with subjective readiness (RPE, mood, recovery). Implements evidence-based frameworks for phase-specific training adaptation.",
      "principles": [
        "Seiler 80/20 Polarisation",
        "Banister TRIMP",
        "Foster Monotony/Strain",
        "San Mill\u00e1n Zone 2",
        "Friel Periodisation",
        "Sandbakk Durability",
        "Skiba Critical Power",
        "Coggan Power Zones",
        "Noakes Central Governor"
      ]
    },
    "generated_at": {
      "local": "2026-02-23T00:15:28+01:00"
    },
    "timezone": "Europe/Par",
    "athlete": {
      "identity": {
        "id": "1234567",
        "name": "Demo Athlete",
        "firstname": "Demo",
        "lastname": "Athlete",
        "sex": "M",
        "dob": "1980-01-01",
        "country": "France",
        "city": "Paris",
        "timezone": "Europe/Paris",
        "profile_image": ""
      },
      "profile": {
        "ftp": 300,
        "eftp": 300,
        "ftp_kg": 4.11,
        "lthr": 157,
        "max_hr": 177,
        "threshold_pace": None,
        "pace_units": None,
        "primary_sport": "ride",
        "dominant_sport": "ride",
        "vo2max_garmin": 72,
        "lactate_mmol_l": 1.9,
        "lactate_power": 185
      },
      "profiles": {
        "ride": {
          "ftp": 300,
          "eftp": 300,
          "w_prime": 15600,
          "p_max": None,
          "lthr": 157,
          "max_hr": 177,
          "threshold_pace": None,
          "pace_units": None,
          "power_zones": [
            55,
            75,
            90,
            105,
            120,
            150
          ],
          "hr_zones": [
            126,
            140,
            146,
            156,
            160,
            165,
            177
          ],
          "pace_zones": None,
          "vo2max_garmin": 72,
          "lactate_mmol_l": 1.9,
          "lactate_power": 185
        },
        "run": {
          "ftp": 327,
          "eftp": None,
          "w_prime": None,
          "p_max": None,
          "lthr": 157,
          "max_hr": 177,
          "threshold_pace": 3.5714285,
          "pace_units": "M_PER_SEC",
          "power_zones": [
            55,
            75,
            90,
            105,
            120,
            150,
            999
          ],
          "hr_zones": [
            132,
            140,
            148,
            156,
            161,
            165,
            177
          ],
          "pace_zones": [
            77.5,
            87.7,
            94.3,
            100,
            103.4,
            111.5,
            999
          ],
          "vo2max_garmin": None,
          "lactate_mmol_l": None,
          "lactate_power": None
        },
        "swim": {
          "ftp": None,
          "eftp": None,
          "w_prime": None,
          "p_max": None,
          "lthr": 157,
          "max_hr": 177,
          "threshold_pace": None,
          "pace_units": "SECS_100M",
          "power_zones": None,
          "hr_zones": [
            132,
            140,
            148,
            156,
            161,
            165,
            177
          ],
          "pace_zones": None,
          "vo2max_garmin": None,
          "lactate_mmol_l": None,
          "lactate_power": None
        },
        "ski": {
          "ftp": None,
          "eftp": None,
          "w_prime": None,
          "p_max": None,
          "lthr": 157,
          "max_hr": 177,
          "threshold_pace": None,
          "pace_units": "MINS_KM",
          "power_zones": None,
          "hr_zones": [
            125,
            140,
            146,
            156,
            160,
            165,
            177
          ],
          "pace_zones": None,
          "vo2max_garmin": None,
          "lactate_mmol_l": None,
          "lactate_power": None
        }
      },
      "global": {
        "resting_hr": 42,
        "weight": 73,
        "height": 1.81,
        "sex": "M"
      },
      "context": {
        "platforms": {
          "garmin": True,
          "zwift": True,
          "wahoo": True,
          "strava": True,
          "polar": False,
          "suunto": None,
          "coros": False,
          "concept2": False
        },
        "wellness_features": {
          "sources": {
            "garmin": True,
            "whoop": False,
            "oura": False,
            "fitbit": False,
            "polar": False,
            "coros": False,
            "suunto": False
          },
          "wellness_keys": [
            "weight",
            "restingHR",
            "kcalConsumed",
            "sleep",
            "sleepScore",
            "sleepQuality",
            "vo2max",
            "spO2",
            "hrv",
            "steps",
            "bodyFat"
          ],
          "hrv_available": True,
          "hrv_source": "garmin",
          "weight_sync": "None",
          "resting_hr": 42
        },
        "training_environment": {
          "plan": "SUPPORTER",
          "beta_user": True,
          "coach_access": False,
          "language": "en",
          "timezone": "Europe/Zurich"
        },
        "equipment_summary": {
          "bike_count": 9,
          "shoe_count": 7,
          "primary_bike": None,
          "total_bike_distance_km": 139086.38700000002
        },
        "activity_scope": {
          "primary_sports": [
            [
              "Ride",
              "VirtualRide",
              "MountainBikeRide",
              "GravelRide",
              "TrackRide"
            ],
            [
              "Run",
              "VirtualRun",
              "TrailRun"
            ],
            [
              "Swim",
              "OpenWaterSwim"
            ],
            [
              "AlpineSki",
              "BackcountrySki"
            ],
            [
              "Other"
            ]
          ],
          "active_since": "2019-05-08T00:00:00.000+00:00",
          "last_seen": "2026-02-22T21:18:05.318+00:00"
        }
      }
    },
    "report_type": "weekly",
    "window_days": 6,
    "period": "2026-02-16 \u2192 2026-02-22",
    "report_header": {
      "title": "Weekly Training Report",
      "scope": "Detailed analysis of the last 7 days of training activity",
      "data_sources": "7-day full activities, 42-day wellness, 90 day light activities",
      "intended_use": "Day-to-day coaching decisions, intensity balance, short-term fatigue and recovery management"
    },
    "summary_card_ready": False,
    "events": {
      "is_event_block": True,
      "event_block_count": 8,
      "render": True,
      "notes": "Canonical activity/event block (URF v5.2) \u2014 intended for ChatGPT / structured UI rendering."
    },
    "planned_events": {
      "is_planned_events_block": True,
      "planned_events_block_count": 3,
      "notes": "Canonical planned events block (URF v5.2) \u2014 intended for ChatGPT / structured UI rendering."
    },
    "phases_summary": {
      "is_phase_block": True,
      "phase_block_count": 11,
      "notes": "Macro-level sequential phase summary, intended for ChatGPT / structured UI rendering."
    },
    "resolution": {
      "CTL": "authoritative",
      "ATL": "authoritative",
      "TSB": "authoritative",
      "zones": "authoritative",
      "derived_metrics": "full",
      "extended_metrics": "limited",
      "performance_intelligence": "acute_full_7d",
      "insights": "tactical"
    }
  },
  "metrics": {
    "Polarisation_variants": {
      "fused": {
        "name": "Polarisation_fused",
        "display_name": "Polarisation Index (Fused HR+Power, sport-specific)",
        "value": 0.952,
        "framework": "Seiler / St\u00f6ggl / Issurin (HR+Power fused)",
        "formula": "Normalized intensity-domain distribution (fused HR+Power)",
        "thresholds": {
          "green": [
            0.8,
            1.0
          ],
          "amber": [
            0.65,
            0.8
          ]
        },
        "phase_context": "Overreached",
        "classification": "green",
        "metric_confidence": "contextual",
        "interpretation": "Sport-specific Polarisation derived from fused HR+Power data. Represents how the athlete distributes intensity within the dominant discipline. Dominance reflects the sport providing the clearest and most internally consistent intensity (zone) signal \u2014 not the sport with the greatest volume, duration, or load. \u22650.80 = polarised, 0.65\u20130.79 = pyramidal, <0.65 = threshold-dominant. \u2699\ufe0f *HR fills gaps when power unavailable; low-intensity HR-only activities may dominate the signal when cycling intensity is spread across Z2\u2013Z4.*",
        "coaching_implication": "If fused Polarisation Index <0.65, the dominant sport is intensity-heavy \u2014 increase Z1/Z2 duration or insert a recovery microcycle. Maintain \u22650.80 for a robust endurance foundation.",
        "related_metrics": {
          "polarised": "\u2265 0.80",
          "pyramidal": "0.65\u20130.79",
          "threshold_dominant": "< 0.65"
        },
        "basis": "Fused HR+Power",
        "source": "zones.fused",
        "context_window": "7d"
      },
      "combined": {
        "name": "Polarisation_combined",
        "display_name": "Polarisation Index (Combined HR+Power, multi-sport)",
        "value": 0.638,
        "framework": "Seiler / St\u00f6ggl / Issurin (multi-sport combined)",
        "formula": "Normalized global intensity-domain distribution",
        "thresholds": {
          "green": [
            0.78,
            1.0
          ],
          "amber": [
            0.6,
            0.78
          ]
        },
        "phase_context": "Overreached",
        "classification": "amber",
        "metric_confidence": "informational",
        "interpretation": "Global HR+Power combined Polarisation Index across all sports. Reflects total weekly distribution and load balance for multi-sport athletes. Dominance reflects intensity signal strength, not training volume. \u22650.80 = polarised, 0.65\u20130.79 = pyramidal, <0.65 = threshold-heavy. \u2699\ufe0f *Cross-discipline index \u2014 lower precision, but best overall summary of load contrast.*",
        "coaching_implication": "If combined Polarisation Index <0.65, total weekly load is intensity-heavy. Add endurance-focused sessions or recovery days to preserve a healthy 80/20 ratio. Ideal global range \u22650.78 for mixed-sport athletes.",
        "related_metrics": {
          "polarised": "\u2265 0.80",
          "pyramidal": "0.65\u20130.79",
          "threshold_dominant": "< 0.65"
        },
        "basis": "Power where available, HR otherwise (multi-sport weighted)",
        "source": "zones.combined",
        "context_window": "7d"
      },
      "context_window": "unknown"
    },
    "ACWR": {
      "value": 1.13,
      "criteria": {
        "productive": "0.8\u20131.3",
        "recovery": "<0.8",
        "overload": ">1.5"
      },
      "state": "productive",
      "icon": "\ud83d\udfe2",
      "framework": "Banister Load Ratio",
      "notes": "EWMA Acute:Chronic Load Ratio \u2014 compares 7-day vs 28-day weighted loads. 0.8\u20131.3 = productive training, <0.8 = recovery or detraining, >1.5 = overload/injury risk.",
      "context_window": "rolling"
    },
    "Monotony": {
      "value": 1.96,
      "criteria": {
        "optimal": "0\u20132",
        "moderate": "2.1\u20132.5",
        "high": ">2.5"
      },
      "state": "optimal",
      "icon": "\ud83d\udfe2",
      "framework": "Foster 2001",
      "notes": "1\u20132 shows healthy variation; >2.5 means repetitive stress pattern.",
      "context_window": "rolling"
    },
    "Strain": {
      "value": 176.1,
      "criteria": {
        "optimal": "<600",
        "moderate": "600\u2013800",
        "high": ">800"
      },
      "state": "optimal",
      "icon": "\ud83d\udfe2",
      "framework": "Foster 2001",
      "notes": "Product of load \u00d7 monotony; >3500 signals potential overreach.",
      "context_window": "rolling"
    },
    "FatigueTrend": {
      "value": 4.2,
      "criteria": {
        "balanced": "-0.2\u2013+0.2",
        "accumulating": ">+0.2",
        "recovering": "<-0.2"
      },
      "state": "accumulating",
      "icon": "\ud83d\udd34",
      "framework": "Banister EWMA Delta",
      "notes": "FatigueTrend is calculated as the percentage change between the 7-day and 28-day moving averages. A 0% change indicates balance, while a positive percentage change indicates accumulating fatigue, and a negative percentage change indicates recovery.",
      "context_window": "90d"
    },
    "ZQI": {
      "value": 4.3,
      "criteria": {
        "optimal": "5\u201315",
        "moderate": "15\u201325",
        "low": "<5"
      },
      "state": "low",
      "icon": "\ud83d\udd34",
      "framework": "Seiler Intensity Distribution",
      "notes": "Zone Quality Index (%) 5-15 high-intensity time is normal <3% too easy, >20% too intense or erratic pacing.",
      "context_window": "7d"
    },
    "FatOxEfficiency": {
      "name": "FatOxEfficiency",
      "value": 0.732,
      "classification": "optimal",
      "interpretation": "0.4\u20130.8 means balanced fat oxidation; lower = carb dependence.",
      "coaching_implication": "If FatOxEfficiency is low (<0.6), focus on improving aerobic base with longer, low-intensity efforts.",
      "related_metrics": {},
      "context_window": "7d"
    },
    "PolarisationIndex": {
      "name": "PolarisationIndex",
      "value": 0.638,
      "classification": "computed",
      "interpretation": "Power-based normalized Polarisation Index (0\u20131). Reflects the proportion of total training time in Z1 + Z2 relative to total. \u22650.75 = strong aerobic bias, <0.60 = intensity-heavy. \u2699\ufe0f *Power-only metric; dependent on accurate FTP calibration.*",
      "coaching_implication": "If PolarisationIndex <0.60 during base, increase Z1 time to reinforce aerobic bias. If low in Build, acceptable for intensity focus. Target \u22650.75 in base and recovery blocks for efficient endurance adaptation.",
      "related_metrics": {},
      "context_window": "7d"
    },
    "FOxI": {
      "value": 73.2,
      "criteria": {
        "optimal": ">=70",
        "moderate": "50\u201369",
        "low": "<50"
      },
      "state": "optimal",
      "icon": "\ud83d\udfe2",
      "framework": "Internal Derived Metric",
      "notes": "FatOx index %; higher values mean more efficient aerobic base.",
      "context_window": "7d"
    },
    "CUR": {
      "name": "CUR",
      "value": 26.8,
      "classification": "optimal",
      "interpretation": "Carbohydrate Utilisation Ratio; 30-80 balanced metabolic use.",
      "coaching_implication": "If CUR is outside the green zone (30-70), adjust carbohydrate intake and fueling strategy to ensure balanced metabolic use during long sessions.",
      "related_metrics": {},
      "context_window": "7d"
    },
    "GR": {
      "name": "GR",
      "value": 1.95,
      "classification": "optimal",
      "interpretation": "Glucose Ratio; >2 indicates excess glycolytic bias.",
      "coaching_implication": "If GR exceeds 2.0, focus on reducing glycolytic intensity and increase aerobic work. Ensure sufficient recovery to avoid over-reliance on carbs.",
      "related_metrics": {},
      "context_window": "7d"
    },
    "MES": {
      "value": 22.5,
      "criteria": {
        "optimal": ">=20",
        "moderate": "10\u201319",
        "low": "<10"
      },
      "state": "optimal",
      "icon": "\ud83d\udfe2",
      "framework": "Internal Derived Metric",
      "notes": "Metabolic Efficiency Score; >20 is good endurance economy.",
      "context_window": "7d"
    },
    "LoadVariabilityIndex": {
      "name": "LoadVariabilityIndex",
      "value": 0.608,
      "classification": "optimal",
      "interpretation": {
        "description": "Composite metric reflecting the interaction between autonomic state (HRV) and training load balance (TSB), indicating how well current load variability aligns with physiological capacity."
      },
      "coaching_implication": {
        "coaching_guidance": "Low values indicate load is exceeding current physiological tolerance; moderate values suggest manageable stress; high values reflect positive load variability with adequate systemic capacity."
      },
      "related_metrics": {},
      "context_window": "unknown"
    },
    "StressTolerance": {
      "value": 2.0,
      "criteria": {
        "low_exposure": "<3",
        "optimal": "3\u20136",
        "high": ">6"
      },
      "state": "low_exposure",
      "icon": "\ud83d\udfe2",
      "framework": "Adaptive Load Tolerance",
      "notes": "2\u20138 indicates sustainable training strain capacity.",
      "context_window": "7d"
    },
    "Polarisation": {
      "name": "Polarisation",
      "display_name": "Polarisation (Power-based, Seiler ratio)",
      "value": 0.952,
      "framework": "Seiler 80/20 Model (Ratio)",
      "formula": "(Z1 + Z3) / (2 \u00d7 Z2)",
      "thresholds": {
        "green": [
          0.75,
          0.9
        ],
        "amber": [
          0.65,
          0.95
        ]
      },
      "phase_context": "",
      "classification": "red",
      "metric_confidence": "contextual",
      "interpretation": "Power-based Seiler Polarisation Ratio (Z1 + Z3) / (2 \u00d7 Z2), showing the balance between low- and high-intensity work relative to moderate (Z2) training. \u22651.0 = polarised (80/20), 0.7\u20130.99 = mixed, <0.7 = Z2-dominant. \u2699\ufe0f *Power-only metric \u2014 HR ignored.* Use primarily during power-measured cycling phases.",
      "coaching_implication": "If Polarisation <0.7 during base, this reflects aerobic Z2 dominance (\u2705 normal). If in Build/Peak, reduce Z2 time and increase Z1/Z3 contrast. Maintain \u22651.0 for ideal 80/20 balance in power-measured disciplines.",
      "related_metrics": {
        "polarised": "\u2265 1.0",
        "mixed": "0.7\u20130.99",
        "z2_base": "0.35\u20130.69",
        "threshold": "< 0.35"
      }
    }
  },
  "extended_metrics": {
    "lactate": {
      "available": True,
      "samples": 29,
      "mean_mmol": 1.92,
      "latest_mmol": 1.8,
      "range_mmol": [
        1.8,
        2.0
      ],
      "paired_with_power": True,
      "power_field": "HrtLndLt1p",
      "power_spread_w": [
        170.0,
        195.0
      ],
      "power_source": "activity_samples",
      "corr_with_power": 0.984,
      "corr_window_days": 90,
      "source": "df_light",
      "mean": 1.92,
      "latest": 1.8
    },
    "personalized_z2": {
      "start_w": 210,
      "end_w": 225,
      "start_pct": 70.0,
      "end_pct": 75.0,
      "method": "lactate_inferred",
      "mean_lactate": 1.92,
      "latest_lactate": 1.8,
      "samples": 29
    },
    "power_lactate": {
      "method": "lactate_inferred",
      "lt1_w": 210,
      "lt2_w": 300,
      "zones": {
        "z1": [
          0,
          210
        ],
        "z2": [
          210,
          225
        ],
        "z3": [
          225,
          300
        ]
      },
      "confidence_r": 0.984,
      "source": "extended_metrics"
    }
  },
  "performance_intelligence": {
    "acute": {
      "anaerobic_repeatability": {
        "max_depletion_pct_7d": {
          "name": "max_depletion_pct_7d",
          "display_name": "max_depletion_pct_7d",
          "value": 1.055576923076923,
          "framework": "W\u2032 Depletion & Repeatability Model (WDRM)",
          "formula": None,
          "thresholds": {},
          "phase_context": "",
          "classification": "informational",
          "metric_confidence": "contextual",
          "interpretation": "WDRM (W\u2032 Depletion & Repeatability Metric) quantifies depth and frequency of anaerobic reserve depletion across sessions. Higher values reflect repeated deep supra-threshold exposure.",
          "coaching_implication": {
            "low": "Anaerobic exposure controlled \u2014 maintain structure.",
            "moderate": "Moderate anaerobic load \u2014 ensure recovery spacing.",
            "high": "High W\u2032 depletion \u2014 monitor recovery and intensity stacking."
          },
          "related_metrics": {},
          "context_window": "7d"
        },
        "mean_depletion_pct_7d": {
          "name": "mean_depletion_pct_7d",
          "display_name": "mean_depletion_pct_7d",
          "value": 0.41445512820512825,
          "framework": "W\u2032 Depletion & Repeatability Model (WDRM)",
          "formula": None,
          "thresholds": {
            "green": [
              0.2,
              0.45
            ],
            "amber": [
              0.45,
              0.7
            ]
          },
          "phase_context": "",
          "classification": "green",
          "metric_confidence": "contextual",
          "interpretation": "WDRM (W\u2032 Depletion & Repeatability Metric) quantifies depth and frequency of anaerobic reserve depletion across sessions. Higher values reflect repeated deep supra-threshold exposure.",
          "coaching_implication": "<circular>",
          "related_metrics": {},
          "context_window": "7d"
        },
        "high_depletion_sessions_7d": {
          "name": "high_depletion_sessions_7d",
          "display_name": "high_depletion_sessions_7d",
          "value": 1,
          "framework": "W\u2032 Depletion & Repeatability Model (WDRM)",
          "formula": None,
          "thresholds": {
            "green": [
              0,
              2
            ],
            "amber": [
              3,
              4
            ]
          },
          "phase_context": "",
          "classification": "green",
          "metric_confidence": "contextual",
          "interpretation": "WDRM (W\u2032 Depletion & Repeatability Metric) quantifies depth and frequency of anaerobic reserve depletion across sessions. Higher values reflect repeated deep supra-threshold exposure.",
          "coaching_implication": "<circular>",
          "related_metrics": {},
          "context_window": "7d"
        },
        "total_joules_above_ftp_7d": {
          "name": "total_joules_above_ftp_7d",
          "display_name": "total_joules_above_ftp_7d",
          "value": 131333.0,
          "framework": "W\u2032 Depletion & Repeatability Model (WDRM)",
          "formula": None,
          "thresholds": {},
          "phase_context": "",
          "classification": "informational",
          "metric_confidence": "high",
          "interpretation": "WDRM (W\u2032 Depletion & Repeatability Metric) quantifies depth and frequency of anaerobic reserve depletion across sessions. Higher values reflect repeated deep supra-threshold exposure.",
          "coaching_implication": "<circular>",
          "related_metrics": {},
          "context_window": "7d"
        }
      },
      "model_diagnostics": {
        "w_prime_divergence_7d": {
          "name": "w_prime_divergence_7d",
          "display_name": "W\u2032 Model Coherence (7-day)",
          "value": 0.4370619658119658,
          "framework": "Skiba Critical Power",
          "formula": None,
          "thresholds": {
            "green": [
              0.0,
              0.2
            ],
            "amber": [
              0.2,
              0.5
            ],
            "red": [
              0.5,
              1.0
            ]
          },
          "phase_context": "",
          "classification": "amber",
          "metric_confidence": "informational",
          "interpretation": None,
          "coaching_implication": {},
          "related_metrics": {},
          "context_window": "7d"
        }
      },
      "durability": {
        "mean_decoupling_7d": {
          "name": "mean_decoupling_7d",
          "display_name": "mean_decoupling_7d",
          "value": 4.6579410999999995,
          "framework": "Intensity Stability & Durability Model (ISDM)",
          "formula": None,
          "thresholds": {
            "green": [
              0,
              5
            ],
            "amber": [
              5,
              8
            ]
          },
          "phase_context": "",
          "classification": "green",
          "metric_confidence": "contextual",
          "interpretation": "ISDM (Intensity Stability & Durability Metric) reflects decoupling behaviour under fatigue. Elevated values indicate cardiovascular drift or durability stress.",
          "coaching_implication": {
            "stable": "Durability stable \u2014 cardiovascular drift controlled.",
            "fatigue": "Elevated drift \u2014 consider aerobic consolidation.",
            "severe": "Significant durability stress \u2014 reduce load."
          },
          "related_metrics": {},
          "context_window": "7d"
        },
        "max_decoupling_7d": {
          "name": "max_decoupling_7d",
          "display_name": "max_decoupling_7d",
          "value": 23.422548,
          "framework": "Intensity Stability & Durability Model (ISDM)",
          "formula": None,
          "thresholds": {},
          "phase_context": "",
          "classification": "informational",
          "metric_confidence": "contextual",
          "interpretation": "ISDM (Intensity Stability & Durability Metric) reflects decoupling behaviour under fatigue. Elevated values indicate cardiovascular drift or durability stress.",
          "coaching_implication": "<circular>",
          "related_metrics": {},
          "context_window": "7d"
        },
        "high_drift_sessions_7d": {
          "name": "high_drift_sessions_7d",
          "display_name": "high_drift_sessions_7d",
          "value": 1,
          "framework": "Intensity Stability & Durability Model (ISDM)",
          "formula": None,
          "thresholds": {
            "green": [
              0,
              2
            ],
            "amber": [
              3,
              4
            ]
          },
          "phase_context": "",
          "classification": "green",
          "metric_confidence": "contextual",
          "interpretation": "ISDM (Intensity Stability & Durability Metric) reflects decoupling behaviour under fatigue. Elevated values indicate cardiovascular drift or durability stress.",
          "coaching_implication": "<circular>",
          "related_metrics": {},
          "context_window": "7d"
        },
        "long_sessions_7d": {
          "name": "long_sessions_7d",
          "display_name": "long_sessions_7d",
          "value": 2,
          "framework": "Intensity Stability & Durability Model (ISDM)",
          "formula": None,
          "thresholds": {},
          "phase_context": "",
          "classification": "informational",
          "metric_confidence": "high",
          "interpretation": "ISDM (Intensity Stability & Durability Metric) reflects decoupling behaviour under fatigue. Elevated values indicate cardiovascular drift or durability stress.",
          "coaching_implication": "<circular>",
          "related_metrics": {},
          "context_window": "7d"
        }
      },
      "neural_density": {
        "rolling_joules_above_ftp_7d": {
          "name": "rolling_joules_above_ftp_7d",
          "display_name": "rolling_joules_above_ftp_7d",
          "value": 131333.0,
          "framework": "Neural Density Load Index (NDLI)",
          "formula": None,
          "thresholds": {
            "green": [
              0,
              160000
            ],
            "amber": [
              160000,
              250000
            ],
            "red": [
              250000,
              1000000
            ]
          },
          "phase_context": "",
          "classification": "green",
          "metric_confidence": "contextual",
          "interpretation": "NDLI (Neural Density Load Index) captures clustering of high-intensity work within short time windows (e.g. 72h). High density increases recovery demand.",
          "coaching_implication": {
            "balanced": "Intensity density well distributed.",
            "clustered": "High short-term clustering \u2014 monitor recovery.",
            "overloaded": "Neural load accumulation high \u2014 reduce intensity density."
          },
          "related_metrics": {},
          "context_window": "7d"
        },
        "high_intensity_days_7d": {
          "name": "high_intensity_days_7d",
          "display_name": "high_intensity_days_7d",
          "value": 2,
          "framework": "Neural Density Load Index (NDLI)",
          "formula": None,
          "thresholds": {
            "green": [
              0,
              2
            ],
            "amber": [
              3,
              4
            ],
            "red": [
              5,
              7
            ]
          },
          "phase_context": "",
          "classification": "green",
          "metric_confidence": "contextual",
          "interpretation": "NDLI (Neural Density Load Index) captures clustering of high-intensity work within short time windows (e.g. 72h). High density increases recovery demand.",
          "coaching_implication": "<circular>",
          "related_metrics": {},
          "context_window": "7d"
        },
        "mean_if_7d": {
          "name": "mean_if_7d",
          "display_name": "mean_if_7d",
          "value": 0.8136274509803921,
          "framework": "Neural Density Load Index (NDLI)",
          "formula": None,
          "thresholds": {},
          "phase_context": "",
          "classification": "informational",
          "metric_confidence": "high",
          "interpretation": "NDLI (Neural Density Load Index) captures clustering of high-intensity work within short time windows (e.g. 72h). High density increases recovery demand.",
          "coaching_implication": "<circular>",
          "related_metrics": {},
          "context_window": "7d"
        }
      }
    },
    "chronic": {},
    "training_state": {
      "state_label": "Productive",
      "readiness": "You are in a productive training zone.",
      "adaptation": "Adaptation signals are stable.",
      "recommendation": "Maintain progression",
      "next_session": "Planned structured session",
      "confidence": "moderate",
      "phase_context": None
    }
  },
  "zones": {
    "power": {
      "label": "Cycling Power Zones",
      "description": "Distribution of training time by cycling power zones. Derived from Intervals.icu power zone times for Ride-based activities. SS = Sweetspot",
      "distribution": {
        "z1": 19.7,
        "z2": 23.1,
        "z3": 24.3,
        "z4": 14.5,
        "z5": 4.0,
        "z6": 1.5,
        "z7": 0.2,
        "SS": 12.6
      },
      "thresholds": "<circular>"
    },
    "hr": {
      "label": "Cycling Heart Rate Zones",
      "description": "Distribution of training time by heart rate zones. Restricted to Ride-based activities for physiological comparability.",
      "distribution": {
        "z1": 57.0,
        "z2": 22.2,
        "z3": 6.5,
        "z4": 10.8,
        "z5": 2.9,
        "z6": 0.6,
        "z7": 0.0
      },
      "thresholds": "<circular>"
    },
    "pace": {
      "label": "Run Pace Zones",
      "description": "Distribution of training time by pace zones. Used primarily for Run-based activities.",
      "distribution": {},
      "thresholds": []
    },
    "swim": {
      "label": "Swim Pace Zones",
      "description": "Distribution of training time by swim pace zones for pool and open water swims.",
      "distribution": {},
      "thresholds": []
    },
    "calibration": {
      "source": "lactate_test",
      "method": "physiological",
      "confidence": 0.984,
      "reason": "lactate correlation r=0.98",
      "lactate_thresholds": {
        "lt1_mmol": 2.0,
        "lt2_mmol": 4.0,
        "corr_threshold": 0.6,
        "notes": "Standard lab defaults (Mader & Heck, 1986). LT1\u22482 mmol/L corresponds to the first sustained rise in blood lactate, while LT2\u22484 mmol/L approximates the maximal lactate steady-state (MLSS). Override with athlete-specific testing or field protocols."
      }
    },
    "fused": {
      "per_sport": {
        "Ride": {
          "_fused_power_z1": 19.7,
          "_fused_power_z2": 23.1,
          "_fused_power_z3": 24.3,
          "_fused_power_z4": 14.5,
          "_fused_power_z5": 4.0,
          "_fused_power_z6": 1.5,
          "_fused_power_z7": 0.2,
          "_fused_power_SS": 12.6,
          "_fused_hr_z1": 0.0,
          "_fused_hr_z2": 0.0,
          "_fused_hr_z3": 0.0,
          "_fused_hr_z4": 0.0,
          "_fused_hr_z5": 0.0,
          "_fused_hr_z6": 0.0,
          "_fused_hr_z7": 0.0
        },
        "Run": {
          "_fused_hr_z1": 100.0,
          "_fused_hr_z2": 0.0,
          "_fused_hr_z3": 0.0,
          "_fused_hr_z4": 0.0,
          "_fused_hr_z5": 0.0,
          "_fused_hr_z6": 0.0,
          "_fused_hr_z7": 0.0,
          "_fused_power_z1": 0.0,
          "_fused_power_z2": 0.0,
          "_fused_power_z3": 0.0,
          "_fused_power_z4": 0.0,
          "_fused_power_z5": 0.0,
          "_fused_power_z6": 0.0,
          "_fused_power_z7": 0.0,
          "_fused_power_SS": 0.0
        },
        "Ski": {
          "_fused_hr_z1": 97.8,
          "_fused_hr_z2": 1.7,
          "_fused_hr_z3": 0.1,
          "_fused_hr_z4": 0.1,
          "_fused_hr_z5": 0.0,
          "_fused_hr_z6": 0.0,
          "_fused_hr_z7": 0.3,
          "_fused_power_z1": 0.0,
          "_fused_power_z2": 0.0,
          "_fused_power_z3": 0.0,
          "_fused_power_z4": 0.0,
          "_fused_power_z5": 0.0,
          "_fused_power_z6": 0.0,
          "_fused_power_z7": 0.0,
          "_fused_power_SS": 0.0
        }
      },
      "basis": "Sport-specific fusion of power and HR zones (power preferred, HR fallback)"
    },
    "combined": {
      "label": "Combined Intensity Distribution",
      "description": "Global distribution of training time across intensity zones for all endurance activities. Power is prioritised where available, heart rate otherwise. Normalised once across total training time (Seiler / St\u00f6ggl / Issurin methodology) SS = Sweetspot.",
      "distribution": {
        "z1": 42.8,
        "z2": 20.7,
        "z3": 14.5,
        "z4": 11.6,
        "z5": 3.1,
        "z6": 1.0,
        "z7": 0.1,
        "SS": 6.1
      },
      "basis": "Time-based intensity distribution across all endurance activities. Power used when available, HR otherwise. Normalised once across total training time (Seiler / St\u00f6ggl / Issurin methodology)."
    }
  },
  "daily_load": [
    {
      "date": "2026-02-16 00:00:00",
      "tss": 87.0
    },
    {
      "date": "2026-02-17 00:00:00",
      "tss": 64.0
    },
    {
      "date": "2026-02-18 00:00:00",
      "tss": 65.0
    },
    {
      "date": "2026-02-19 00:00:00",
      "tss": 71.0
    },
    {
      "date": "2026-02-20 00:00:00",
      "tss": 31.0
    },
    {
      "date": "2026-02-21 00:00:00",
      "tss": 177.0
    },
    {
      "date": "2026-02-22 00:00:00",
      "tss": 134.0
    }
  ],
  "events": [
    {
      "start_date_local": "2026-02-16T18:54:55",
      "name": "Zwift 3x12 Threshold",
      "type": "VirtualRide",
      "distance": 48530.7,
      "moving_time": 4302,
      "icu_training_load": 87,
      "IF": 0.8529411764705882,
      "average_heartrate": 132.0,
      "average_cadence": 75.46625,
      "icu_average_watts": 237.0,
      "icu_variability_index": 1.1012658,
      "icu_weighted_avg_watts": 261.0,
      "strain_score": 89.12982,
      "trimp": 110.028404,
      "hr_load": 88.0,
      "ss_cp": 88.81174,
      "icu_efficiency_factor": 1.9772727,
      "icu_intensity": 85.29412,
      "icu_power_hr": 1.7954545,
      "decoupling": 4.738121,
      "icu_pm_w_prime": 23364.0,
      "icu_w_prime": 15600.0,
      "icu_max_wbal_depletion": 1558.0,
      "icu_joules_above_ftp": 3425.0,
      "total_elevation_gain": 76.0,
      "calories": 973.0,
      "VO2MaxGarmin": 72.0,
      "source": "ZWIFT",
      "device_name": "ZWIFT",
      "wbal_engagement": "light",
      "wbal_pattern": "repeated",
      "wbal_depth_pct": 0.067,
      "event_efficiency": "efficient",
      "event_efficiency_value": 1.977
    },
    {
      "start_date_local": "2026-02-17T18:30:40",
      "name": "Zwift - Stage 2 - Tour de Zwift",
      "type": "VirtualRide",
      "distance": 41032.39,
      "moving_time": 3824,
      "icu_training_load": 64,
      "IF": 0.7777777777777778,
      "average_heartrate": 125.0,
      "average_cadence": 77.42644,
      "icu_average_watts": 230.0,
      "icu_variability_index": 1.0347826,
      "icu_weighted_avg_watts": 238.0,
      "strain_score": 75.339615,
      "trimp": 80.820076,
      "hr_load": 60.0,
      "ss_cp": 75.09485,
      "icu_efficiency_factor": 1.904,
      "icu_intensity": 77.77778,
      "icu_power_hr": 1.84,
      "decoupling": -2.5558727,
      "icu_pm_w_prime": 20974.0,
      "icu_w_prime": 15600.0,
      "icu_max_wbal_depletion": 1711.0,
      "icu_joules_above_ftp": 2613.0,
      "total_elevation_gain": 228.0,
      "calories": 874.0,
      "VO2MaxGarmin": 72.0,
      "source": "ZWIFT",
      "device_name": "ZWIFT",
      "wbal_engagement": "light",
      "wbal_pattern": "repeated",
      "wbal_depth_pct": 0.082,
      "event_efficiency": "efficient",
      "event_efficiency_value": 1.904
    },
    {
      "start_date_local": "2026-02-18T18:03:06",
      "name": "Zwift - Group Ride: Standard - Stage 1 - Tour de Zwift",
      "type": "VirtualRide",
      "distance": 37022.83,
      "moving_time": 3698,
      "icu_training_load": 65,
      "IF": 0.7941176470588235,
      "average_heartrate": 127.0,
      "average_cadence": 77.54575,
      "icu_average_watts": 239.0,
      "icu_variability_index": 1.0167364,
      "icu_weighted_avg_watts": 243.0,
      "strain_score": 75.71349,
      "trimp": 82.390884,
      "hr_load": 59.0,
      "ss_cp": 75.70624,
      "icu_efficiency_factor": 1.9133859,
      "icu_intensity": 79.411766,
      "icu_power_hr": 1.8818898,
      "decoupling": -1.7090102,
      "icu_pm_w_prime": 20672.0,
      "icu_w_prime": 15600.0,
      "icu_max_wbal_depletion": 43.0,
      "icu_joules_above_ftp": 79.0,
      "total_elevation_gain": 329.0,
      "calories": 845.0,
      "VO2MaxGarmin": 72.0,
      "source": "ZWIFT",
      "device_name": "ZWIFT",
      "wbal_engagement": "light",
      "wbal_pattern": "single",
      "wbal_depth_pct": 0.002,
      "event_efficiency": "efficient",
      "event_efficiency_value": 1.913
    },
    {
      "start_date_local": "2026-02-19T18:01:51",
      "name": "Zwift -  Short - Stage 1 - Tour de Zwift",
      "type": "VirtualRide",
      "distance": 38109.94,
      "moving_time": 3697,
      "icu_training_load": 71,
      "IF": 0.8333333333333334,
      "average_heartrate": 128.0,
      "average_cadence": 76.682236,
      "icu_average_watts": 224.0,
      "icu_variability_index": 1.1383928,
      "icu_weighted_avg_watts": 255.0,
      "strain_score": 80.85059,
      "trimp": 84.55204,
      "hr_load": 69.0,
      "ss_cp": 78.48704,
      "icu_efficiency_factor": 1.9921875,
      "icu_intensity": 83.333336,
      "icu_power_hr": 1.75,
      "decoupling": 23.422548,
      "icu_pm_w_prime": 23884.0,
      "icu_w_prime": 15600.0,
      "icu_max_wbal_depletion": 10532.0,
      "icu_joules_above_ftp": 17572.0,
      "total_elevation_gain": 249.0,
      "calories": 809.0,
      "VO2MaxGarmin": 72.0,
      "source": "ZWIFT",
      "device_name": "ZWIFT",
      "wbal_engagement": "heavy",
      "wbal_pattern": "progressive",
      "wbal_depth_pct": 0.441,
      "event_efficiency": "efficient",
      "event_efficiency_value": 1.992
    },
    {
      "start_date_local": "2026-02-20T16:06:06",
      "name": "Ski tour",
      "type": "BackcountrySki",
      "distance": 5622.2,
      "moving_time": 3878,
      "icu_training_load": 31,
      "average_heartrate": 106.0,
      "trimp": 48.72897,
      "hr_load": 31.0,
      "icu_intensity": 52.96631,
      "total_elevation_gain": 446.0,
      "calories": 593.0,
      "source": "GARMIN_CONNECT",
      "device_name": "Garmin epix (Gen 2)",
      "wbal_engagement": "None",
      "wbal_pattern": "None",
      "wbal_depth_pct": 0.0,
      "event_efficiency": "unknown",
      "event_efficiency_value": None
    },
    {
      "start_date_local": "2026-02-21T11:35:58",
      "name": "Zwift - Alpe x 2",
      "type": "VirtualRide",
      "distance": 55338.69,
      "moving_time": 8484,
      "icu_training_load": 159,
      "IF": 0.8202614379084967,
      "average_heartrate": 124.0,
      "average_cadence": 74.48357,
      "icu_average_watts": 223.0,
      "icu_variability_index": 1.1255605,
      "icu_weighted_avg_watts": 251.0,
      "strain_score": 206.74442,
      "trimp": 178.2623,
      "hr_load": 141.0,
      "ss_cp": 201.15364,
      "icu_efficiency_factor": 2.0241935,
      "icu_intensity": 82.026146,
      "icu_power_hr": 1.798387,
      "decoupling": 2.071911,
      "icu_pm_w_prime": 24969.0,
      "icu_w_prime": 15600.0,
      "icu_max_wbal_depletion": 16467.0,
      "icu_joules_above_ftp": 34879.0,
      "total_elevation_gain": 2105.0,
      "calories": 1810.0,
      "VO2MaxGarmin": 72.0,
      "source": "ZWIFT",
      "device_name": "ZWIFT",
      "wbal_engagement": "heavy",
      "wbal_pattern": "progressive",
      "wbal_depth_pct": 0.659,
      "event_efficiency": "efficient",
      "event_efficiency_value": 2.024
    },
    {
      "start_date_local": "2026-02-21T16:00:28",
      "name": "Dog walk",
      "type": "Hike",
      "distance": 4844.33,
      "moving_time": 3026,
      "icu_training_load": 18,
      "average_heartrate": 96.0,
      "average_cadence": 57.353634,
      "trimp": 28.37516,
      "hr_load": 18.0,
      "icu_intensity": 44.09302,
      "icu_w_prime": 19440.0,
      "total_elevation_gain": 71.0,
      "calories": 409.0,
      "source": "GARMIN_CONNECT",
      "device_name": "Garmin epix (Gen 2)",
      "wbal_engagement": "None",
      "wbal_pattern": "None",
      "wbal_depth_pct": 0.0,
      "event_efficiency": "unknown",
      "event_efficiency_value": None
    },
    {
      "start_date_local": "2026-02-22T13:15:31",
      "name": "Sunday Road ride",
      "type": "Ride",
      "distance": 60523.07,
      "moving_time": 7492,
      "icu_training_load": 134,
      "IF": 0.8033333333333333,
      "average_heartrate": 120.0,
      "average_cadence": 83.94883,
      "icu_average_watts": 196.0,
      "icu_variability_index": 1.2295918,
      "icu_weighted_avg_watts": 241.0,
      "strain_score": 140.62323,
      "trimp": 140.01181,
      "hr_load": 118.0,
      "ss_cp": 132.02733,
      "icu_efficiency_factor": 2.0083334,
      "icu_intensity": 80.333336,
      "icu_power_hr": 1.6333333,
      "decoupling": 1.9799495,
      "icu_pm_w_prime": 20646.0,
      "icu_w_prime": 15600.0,
      "icu_max_wbal_depletion": 8482.0,
      "icu_joules_above_ftp": 72765.0,
      "total_elevation_gain": 776.0,
      "calories": 1637.0,
      "VO2MaxGarmin": 71.85045623779297,
      "source": "GARMIN_CONNECT",
      "device_name": "Garmin Edge 840",
      "wbal_engagement": "heavy",
      "wbal_pattern": "stochastic",
      "wbal_depth_pct": 0.411,
      "event_efficiency": "efficient",
      "event_efficiency_value": 2.008
    }
  ],
  "wellness": {
    "ctl": 77.8993,
    "atl": 90.13108,
    "tsb": -12.23178,
    "hrv_mean": 50.2,
    "hrv_latest": 43.0,
    "hrv_trend_7d": 4.1,
    "hrv_source": "garmin",
    "hrv_available": True,
    "hrv_samples": 41,
    "hrv_series": [
      {
        "date": "2026-01-12",
        "hrv": 47.0
      },
      {
        "date": "2026-01-13",
        "hrv": 51.0
      },
      {
        "date": "2026-01-14",
        "hrv": 43.0
      },
      {
        "date": "2026-01-15",
        "hrv": 47.0
      },
      {
        "date": "2026-01-16",
        "hrv": 79.0
      },
      {
        "date": "2026-01-17",
        "hrv": 44.0
      },
      {
        "date": "2026-01-18",
        "hrv": 41.0
      },
      {
        "date": "2026-01-19",
        "hrv": 48.0
      },
      {
        "date": "2026-01-20",
        "hrv": 42.0
      },
      {
        "date": "2026-01-21",
        "hrv": 46.0
      },
      {
        "date": "2026-01-22",
        "hrv": 46.0
      },
      {
        "date": "2026-01-23",
        "hrv": 40.0
      },
      {
        "date": "2026-01-24",
        "hrv": 40.0
      },
      {
        "date": "2026-01-25",
        "hrv": 42.0
      },
      {
        "date": "2026-01-26",
        "hrv": 60.0
      },
      {
        "date": "2026-01-27",
        "hrv": 49.0
      },
      {
        "date": "2026-01-28",
        "hrv": 49.0
      },
      {
        "date": "2026-01-29",
        "hrv": 41.0
      },
      {
        "date": "2026-01-30",
        "hrv": 49.0
      },
      {
        "date": "2026-02-01",
        "hrv": 44.0
      },
      {
        "date": "2026-02-02",
        "hrv": 49.0
      },
      {
        "date": "2026-02-03",
        "hrv": 54.0
      },
      {
        "date": "2026-02-04",
        "hrv": 72.0
      },
      {
        "date": "2026-02-05",
        "hrv": 49.0
      },
      {
        "date": "2026-02-06",
        "hrv": 59.0
      },
      {
        "date": "2026-02-07",
        "hrv": 54.0
      },
      {
        "date": "2026-02-08",
        "hrv": 37.0
      },
      {
        "date": "2026-02-09",
        "hrv": 44.0
      },
      {
        "date": "2026-02-10",
        "hrv": 52.0
      },
      {
        "date": "2026-02-11",
        "hrv": 58.0
      },
      {
        "date": "2026-02-13",
        "hrv": 58.0
      },
      {
        "date": "2026-02-14",
        "hrv": 56.0
      },
      {
        "date": "2026-02-15",
        "hrv": 46.0
      },
      {
        "date": "2026-02-16",
        "hrv": 65.0
      },
      {
        "date": "2026-02-17",
        "hrv": 64.0
      },
      {
        "date": "2026-02-18",
        "hrv": 51.0
      },
      {
        "date": "2026-02-19",
        "hrv": 56.0
      },
      {
        "date": "2026-02-20",
        "hrv": 54.0
      },
      {
        "date": "2026-02-21",
        "hrv": 48.0
      },
      {
        "date": "2026-02-22",
        "hrv": 43.0
      }
    ],
    "subjective": {},
    "CTL": 77.8993,
    "ATL": 90.13108,
    "TSB": -12.23178
  },
  "hours": 10.67,
  "tss": 629.0,
  "distance_km": 291.0,
  "wbal_summary": {
    "mean_wbal_depletion_pct": 0.277,
    "mean_anaerobic_contrib_pct": 0.989,
    "sessions_with_wbal_data": 6,
    "basis": "per-session mean (W\u2032-capable sessions only)",
    "window": "weekly",
    "temporal_pattern": {
      "2026-02-16": "low",
      "2026-02-17": "low",
      "2026-02-18": "low",
      "2026-02-19": "high",
      "2026-02-21": "high",
      "2026-02-22": "high"
    },
    "dominant_pattern": "clustered_weekend"
  },
  "planned_events": [
    {
      "id": 92130818,
      "uid": "8fce309b-26e5-4549-a21b-bd21e55b538b",
      "category": "WORKOUT",
      "name": "Aerobic Endurance",
      "description": "- 10m Ramp 60-70% FTP\n- 90m 65-70% FTP steady\n- 10m Ramp 70-45% FTP",
      "start_date_local": "2026-02-23T00:00:00",
      "end_date_local": "2026-02-24T00:00:00",
      "duration_minutes": 110.0,
      "icu_training_load": 81,
      "strain_score": 111.06773,
      "day_of_week": "Monday"
    },
    {
      "id": 92130819,
      "uid": "d83ac83b-8974-471d-be62-d263935dd0ed",
      "category": "WORKOUT",
      "name": "Short Activation",
      "description": "- 10m Ramp 60-75% FTP\n- 5m 55% FTP easy\n- 3m 105% FTP controlled\n- 5m 55% FTP recovery\n- 3m 105% FTP controlled\n- 5m 55% FTP recovery\n- 10m Ramp 70-45% FTP",
      "start_date_local": "2026-02-24T00:00:00",
      "end_date_local": "2026-02-25T00:00:00",
      "duration_minutes": 41.0,
      "icu_training_load": 36,
      "strain_score": 42.131294,
      "day_of_week": "Tuesday"
    },
    {
      "id": 92128988,
      "uid": "90328539-0796-4fe2-872b-7e384f2470c8",
      "category": "NOTE",
      "name": "OFF",
      "description": "-OFF",
      "start_date_local": "2026-02-24T00:00:00",
      "end_date_local": "2026-02-25T00:00:00",
      "duration_minutes": 1440.0,
      "day_of_week": "Tuesday"
    }
  ],
  "planned_summary_by_date": {
    "2026-02-23": {
      "total_events": 1,
      "total_duration": 110.0,
      "total_load": 81,
      "categories": [
        "WORKOUT"
      ]
    },
    "2026-02-24": {
      "total_events": 2,
      "total_duration": 1481.0,
      "total_load": 36,
      "categories": [
        "NOTE",
        "WORKOUT"
      ]
    }
  },
  "future_forecast": {
    "start_date": "2026-02-22",
    "end_date": "2026-03-01",
    "horizon_days": 7,
    "CTL_future": 69.0,
    "ATL_future": 44.35,
    "TSB_future": 24.65,
    "load_trend": "declining",
    "fatigue_class": "transition"
  },
  "future_actions": [
    {
      "priority": "low",
      "title": "Transition / Recovery",
      "reason": "Training load is low; focus on maintaining activity and recovery.",
      "label": "Very fresh \u2014 light training phase",
      "color": "#66ccff",
      "date_range": "2026-02-22 \u2192 2026-03-01"
    }
  ],
  "actions": [
    "\u2705 FatigueTrend 4.20 \u2014 rising fatigue, monitor intensity.",
    "\u2705 Durability improving (1.00) \u2014 maintain current long-ride structure.",
    "\u2705 IF Drift stable (0.00%) \u2014 aerobic durability solid.",
    "\ud83d\udfe0 Load Variability Index moderate (0.61) \u2014 load manageable but monitor fatigue accumulation and ACWR trend."
  ],
  "insights": {
    "fatigue_trend": {
      "value_pct": 15.7,
      "window": "7d",
      "basis": "ATL vs CTL",
      "classification": "amber",
      "confidence": "high",
      "thresholds": {
        "green": [
          -10,
          10
        ],
        "amber": [
          -20,
          20
        ]
      },
      "interpretation": "FatigueTrend is calculated as the percentage change between the 7-day and 28-day moving averages. A 0% change indicates balance, while a positive percentage change indicates accumulating fatigue, and a negative percentage change indicates recovery.",
      "coaching_implication": "If FatigueTrend is negative (e.g., below -0.2), this indicates a recovering state. Continue with controlled training load and focus on recovery to ensure sustained progress. Avoid aggressive increases in load."
    },
    "fat_oxidation_index": {
      "value": 73.2,
      "window": "7d",
      "basis": "FOxI",
      "classification": "green",
      "interpretation": "FatOx index %; higher values mean more efficient aerobic base.",
      "coaching_implication": "If FOxI is increasing, continue to prioritize low-intensity work to enhance fat metabolism. If it decreases, consider increasing your Zone 2 training duration."
    },
    "fitness_phase": {
      "phase": "green",
      "basis": "ACWR",
      "window": "rolling",
      "interpretation": "EWMA Acute:Chronic Load Ratio \u2014 compares 7-day vs 28-day weighted loads. 0.8\u20131.3 = productive training, <0.8 = recovery or detraining, >1.5 = overload/injury risk.",
      "coaching_implication": "If ACWR > 1.5, reduce intensity and focus on recovery to avoid overload. If ACWR < 0.8, gradually increase training load with controlled progression to build endurance."
    },
    "fatigue_resistance": {
      "value": 0.95,
      "window": "7d",
      "basis": "EndurancePower / ThresholdPower",
      "classification": "green",
      "interpretation": "Ratio of endurance (long-duration) power to threshold (short-duration) power. Values near 1.0 indicate strong fatigue resistance \u2014 ability to sustain output under fatigue. <0.9 suggests drop-off under endurance load.",
      "coaching_implication": "If FatigueResistance <0.9, add longer sub-threshold intervals or extended endurance sessions. Maintain >0.95 to support long-duration performance."
    },
    "efficiency_factor": {
      "value": 1.9,
      "window": "7d",
      "basis": "Power / HeartRate",
      "classification": "green",
      "interpretation": "Ratio of power to heart rate, representing aerobic efficiency. Higher values indicate improved aerobic conditioning and cardiovascular economy. Values between 1.8\u20132.2 are typical for trained endurance athletes.",
      "coaching_implication": "If EfficiencyFactor is declining, focus on aerobic conditioning and recovery. Stable or increasing EF indicates improving endurance efficiency."
    }
  },
  "insight_view": {
    "critical": [],
    "watch": [
      {
        "name": "fatigue_trend",
        "classification": "amber",
        "interpretation": "FatigueTrend is calculated as the percentage change between the 7-day and 28-day moving averages. A 0% change indicates balance, while a positive percentage change indicates accumulating fatigue, and a negative percentage change indicates recovery.",
        "coaching_implication": "If FatigueTrend is negative (e.g., below -0.2), this indicates a recovering state. Continue with controlled training load and focus on recovery to ensure sustained progress. Avoid aggressive increases in load."
      }
    ],
    "positive": [
      {
        "name": "fat_oxidation_index",
        "classification": "green",
        "interpretation": "FatOx index %; higher values mean more efficient aerobic base.",
        "coaching_implication": "If FOxI is increasing, continue to prioritize low-intensity work to enhance fat metabolism. If it decreases, consider increasing your Zone 2 training duration."
      },
      {
        "name": "fatigue_resistance",
        "classification": "green",
        "interpretation": "Ratio of endurance (long-duration) power to threshold (short-duration) power. Values near 1.0 indicate strong fatigue resistance \u2014 ability to sustain output under fatigue. <0.9 suggests drop-off under endurance load.",
        "coaching_implication": "If FatigueResistance <0.9, add longer sub-threshold intervals or extended endurance sessions. Maintain >0.95 to support long-duration performance."
      },
      {
        "name": "efficiency_factor",
        "classification": "green",
        "interpretation": "Ratio of power to heart rate, representing aerobic efficiency. Higher values indicate improved aerobic conditioning and cardiovascular economy. Values between 1.8\u20132.2 are typical for trained endurance athletes.",
        "coaching_implication": "If EfficiencyFactor is declining, focus on aerobic conditioning and recovery. Stable or increasing EF indicates improving endurance efficiency."
      }
    ]
  },
  "phases": [
    {
      "week": "2025-W48",
      "start": "2025-11-24",
      "end": "2025-11-30",
      "distance_km": 240.0,
      "hours": 7.9,
      "tss": 444.0,
      "ctl": 87.97,
      "atl": 82.22,
      "tsb": 5.75,
      "classification": "Fresh"
    },
    {
      "week": "2025-W49",
      "start": "2025-12-01",
      "end": "2025-12-07",
      "distance_km": 167.5,
      "hours": 5.1,
      "tss": 200.0,
      "ctl": 80.77,
      "atl": 59.24,
      "tsb": 21.53,
      "classification": "Transition"
    },
    {
      "week": "2025-W50",
      "start": "2025-12-08",
      "end": "2025-12-14",
      "distance_km": 236.7,
      "hours": 9.3,
      "tss": 414.0,
      "ctl": 76.59,
      "atl": 56.01,
      "tsb": 20.58,
      "classification": "Transition"
    },
    {
      "week": "2025-W51",
      "start": "2025-12-15",
      "end": "2025-12-21",
      "distance_km": 210.8,
      "hours": 9.7,
      "tss": 428.0,
      "ctl": 74.71,
      "atl": 61.35,
      "tsb": 13.36,
      "classification": "Transition"
    },
    {
      "week": "2025-W52",
      "start": "2025-12-22",
      "end": "2025-12-28",
      "distance_km": 303.3,
      "hours": 17.0,
      "tss": 570.0,
      "ctl": 72.98,
      "atl": 64.29,
      "tsb": 8.68,
      "classification": "Fresh"
    },
    {
      "week": "2026-W1",
      "start": "2025-12-29",
      "end": "2026-01-04",
      "distance_km": 279.7,
      "hours": 17.1,
      "tss": 642.0,
      "ctl": 75.14,
      "atl": 79.68,
      "tsb": -4.54,
      "classification": "Grey"
    },
    {
      "week": "2026-W2",
      "start": "2026-01-05",
      "end": "2026-01-11",
      "distance_km": 205.8,
      "hours": 12.7,
      "tss": 456.0,
      "ctl": 75.78,
      "atl": 78.84,
      "tsb": -3.06,
      "classification": "Grey"
    },
    {
      "week": "2026-W3",
      "start": "2026-01-12",
      "end": "2026-01-18",
      "distance_km": 275.5,
      "hours": 13.6,
      "tss": 592.0,
      "ctl": 75.98,
      "atl": 78.66,
      "tsb": -2.68,
      "classification": "Grey"
    },
    {
      "week": "2026-W4",
      "start": "2026-01-19",
      "end": "2026-01-25",
      "distance_km": 234.5,
      "hours": 10.6,
      "tss": 432.0,
      "ctl": 76.22,
      "atl": 79.1,
      "tsb": -2.88,
      "classification": "Grey"
    },
    {
      "week": "2026-W5",
      "start": "2026-01-26",
      "end": "2026-02-01",
      "distance_km": 168.5,
      "hours": 9.4,
      "tss": 436.0,
      "ctl": 73.22,
      "atl": 67.71,
      "tsb": 5.51,
      "classification": "Fresh"
    },
    {
      "week": "2026-W6",
      "start": "2026-02-02",
      "end": "2026-02-08",
      "distance_km": 341.2,
      "hours": 15.7,
      "tss": 689.0,
      "ctl": 74.0,
      "atl": 77.0,
      "tsb": -3.0,
      "classification": "Grey"
    },
    {
      "week": "2026-W7",
      "start": "2026-02-09",
      "end": "2026-02-15",
      "distance_km": 282.1,
      "hours": 8.5,
      "tss": 493.0,
      "ctl": 76.45,
      "atl": 86.37,
      "tsb": -9.93,
      "classification": "Optimal"
    },
    {
      "week": "2026-W8",
      "start": "2026-02-16",
      "end": "2026-02-22",
      "distance_km": 291.0,
      "hours": 10.7,
      "tss": 629.0,
      "ctl": 75.86,
      "atl": 79.05,
      "tsb": -3.19,
      "classification": "Grey"
    }
  ],
  "renderer_instructions": "You are a deterministic URF renderer.\n\n    You must render a **Weekly Training Report** using the embedded system context.\n    This report follows the **Unified Reporting Framework (URF v5.1)**.\n\n    **Scope:** Detailed analysis of the last 7 days of training activity\n    **Data Sources:** 7-day full activities, 42-day wellness, 90 day light activities\n    **Intended Use:** Day-to-day coaching decisions, intensity balance, short-term fatigue and recovery management\n\n    HARD RULES:\n  DEMO MODE (NON-NEGOTIABLE OVERRIDE):\n- If semantic.meta.demo == true, render a bold DEMO MODE banner at the VERY TOP of the report.\n- This banner MUST appear before the state banner.\n- It MUST include semantic.meta.demo_reason.\n- This rule overrides state presentation ordering.\n\n  - Render exactly ONE report.\n- Do NOT add numeric prefixes to section headers.\n- Use emoji-based section headers only.\n- Preserve section order exactly as defined by the contract.\n- Metric context MUST be derived exclusively from each metric\u2019s `context_window` and `confidence_model` fields.\n\n    INTERPRETATION RULES:\n    - Interpretations may be descriptive or conditional, not predictive.\n- If semantic.wbal_summary.temporal_pattern exists, render a one-line anaerobic load timeline using block symbols (\u2582 \u2583 \u2587) mapped to None/low/moderate/high.\n- If semantic.daily_load exists, render it as a compact monoblock map timeline with weekday labels, relative load blocks, and numeric TSS values aligned underneath. Do NOT render daily_load as a list or table.\n- If semantic.daily_load exists AND semantic.wellness.CTL and semantic.wellness.ATL are present, a second symbolic fatigue-pressure row MAY be rendered using \u2191 \u2193 \u2014 symbols based ONLY on the sign of (ATL \u2212 CTL). No magnitude, thresholds, or new calculations are permitted.\n- All rows in the daily load timeline MUST use a fixed-width column per day to ensure vertical alignment across labels, blocks, symbols, and numeric values.\n- If session-level signal icons are rendered in the EVENTS table, a single legend line MUST be rendered once per report directly below the EVENTS section header.\n- If zone distribution data exists (e.g. zone_dist_power, zone_dist_hr, zone_dist_fused), render zone distribution as fixed-width ASCII proportional bars (one bar per zone), with the exact percentage shown. Bars are presentational only and do not constitute derived metrics.\n- If performance_intelligence exists, render three subsections: Anaerobic Repeatability (WDRM), Durability (ISDM), Neural Density (NDLI). Use provided values only. Do NOT recompute or merge with other metrics.\n- If high_dep_sessions > 0 and high_drift_sessions > 0 in the same week, describe this as high neuromuscular + metabolic strain overlap.\n\n    COACHING INTERPRETATION RULES:\n- You MAY include up to 5 short coaching sentence(s) per section.\n- Coaching sentences MUST be directly anchored to values, states, or interpretation fields in that section.\n- Coaching sentences MUST be descriptive or conditional, not predictive.\n- Coaching sentences MUST appear immediately after the section\u2019s data and before the next divider.\n- Coaching sentences MUST NOT introduce new metrics.\n\n    ALLOWED ENRICHMENT:\n        - Restate semantic interpretation fields.\n- Explain what a value indicates within its known threshold or state.\n- derive_stepwise_forecast\n\n    STATE PRESENTATION:\n- Present a concise, single-sentence state banner at the top of the report.\n- Use ONLY semantic states already present in the data.\n- Do NOT derive, compute, or infer new states.\n- Style: single_sentence_banner\n\n    EMPHASIS GUIDANCE:\n        The following sections should receive proportional narrative and visual emphasis.\n        This does NOT change section order, inclusion, or data fidelity.\n        - metrics: high\n- actions: high\n- events: medium\n- wellness: medium\n\n    FRAMING INTENT:\n- Interpret and summarise this report through the following intent:\n  tactical_weekly_control\n- This intent guides prioritisation and narrative focus only.\n\n    SECTION HANDLING RULES:\n        - events: full\n- daily_load: full\n- metrics: full\n- extended_metrics: full\n- performance_intelligence: full\n- zones: full\n- wellness: full\n- phases: forbid\n- planned_events: full\n- planned_summary_by_date: full\n- actions: full\n- future_actions: full\n\n        Handling meanings:\n        - full: render entire section exactly as provided\n        - summary: summarise using existing semantic aggregates only\n        - forbid: do NOT render this section\n\n        EVENTS (WEEKLY \u2014 NON-NEGOTIABLE):\n        - The events section MUST be rendered as a Markdown table.\n        - EVERY event in the semantic JSON MUST appear as exactly one row.\n        - The events section MUST NOT be summarised, renamed, grouped, or rewritten.\n        - Bullet points, highlights, or narrative descriptions of events are FORBIDDEN.\n        - Coaching sentences for events, if enabled, MUST appear AFTER the table.\n        - Convert duration from seconds to minutes at render time.\n        - Display as integer minutes by default.\n        - Use one decimal only if duration < 30 minutes and precision is useful.\n        - Label column as Duration (min).\n        - In the EVENTS table, session-level signal icons MAY be rendered in the 1st column (Signals) using the following canonical mapping derived ONLY from existing semantic fields.\n        - Icons represent independent session signals and MAY appear together for a single event.\n        - When multiple icons apply, they MUST be rendered together in the following fixed order (left \u2192 right):\n        1) \u26a1 Efficient (optimal efficiency factor)\n        2) \ud83d\udfe2 Aerobic (low IF with stable decoupling)\n        3) \ud83d\udca5 Anaerobic (heavy W\u2032 engagement)\n        4) \ud83d\udd01 Repeated (repeated W\u2032 depletion pattern)\n        5) \ud83d\udcc8 Progressive (progressive W\u2032 engagement)\n        6) \ud83e\uddd8 Recovery (very low intensity recovery session)\n        - Icons are visual aliases only and must not replace numeric values, suppress other applicable icons, or reduce table rows.\n        PLANNED EVENTS (WEEKLY \u2014 NON-NEGOTIABLE):\n        - The planned_events section MUST be rendered as a Markdown table.\n        - EVERY planned event in the semantic JSON MUST appear as exactly one row.\n        - The planned_events section MUST NOT be summarised, renamed, grouped, or rewritten.\n        - Narrative descriptions of planned events are FORBIDDEN.\n        - Coaching sentences for planned_events, if enabled, MUST appear AFTER the table.\n\n    LIST RENDERING RULES (NON-NEGOTIABLE):\n    - If a section value is a JSON array (list), render it as a Markdown table.\n- Render EVERY element in the array.\n- Preserve one row per array element.\n- Do NOT summarise the list unless explicitly allowed by section handling.\n- Do NOT replace lists with prose unless explicitly allowed.\n- Do NOT omit rows for brevity.\n\n    TONE AND STYLE:\n    - Keep tone factual, supportive, neutral, and coach-like.\n\n    SECTION ORDER (INSTRUCTIONAL \u2014 DO NOT NUMBER HEADERS):\n    1. meta\n2. hours\n3. tss\n4. distance_km\n5. metrics\n6. extended_metrics\n7. performance_intelligence\n8. zones\n9. daily_load\n10. events\n11. wbal_summary\n12. wellness\n13. phases\n14. insights\n15. insight_view\n16. actions\n17. planned_events\n18. planned_summary_by_date\n19. future_forecast\n20. future_actions\n\n    End with a factual coaching closing note on recovery or adaptation\n    based strictly on the provided data. For Weekly and Season reports, if performance_intelligence.training_state\n    is present in the semantic JSON, use it to anchor the closing interpretation."
}
