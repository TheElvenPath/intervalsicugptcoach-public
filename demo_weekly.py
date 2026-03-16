# demo_weekly.py

DEMO_WEEKLY = {
  "meta": {
        "framework": "V5.1 Unified Reporting Framework",
        "version": "v16.17",
        "methodology": {
          "source": "Unified Coaching Reference (Intervals + Seiler + Banister + Treff)",
          "summary": "Data-driven endurance coaching blending objective load metrics (TSS, CTL, ATL, HRV, VO\u2082max) with subjective readiness (RPE, mood, recovery). Implements evidence-based frameworks for phase-specific training adaptation.",
          "principles": [
            "Seiler 3-Zone Polarisation",
            "Treff Polarization-Index (2019)",
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
          "local": "2026-03-16T14:14:53+01:00"
        },
        "timezone": "Europe/Zurich",
        "athlete": {
          "identity": {
            "id": "1914741",
            "name": "Clive King",
            "firstname": "Clive",
            "lastname": "King",
            "sex": "M",
            "dob": "1965-02-19",
            "country": "Switzerland",
            "city": "Jongny",
            "timezone": "Europe/Zurich",
            "profile_image": "https://storage.googleapis.com/intervals-icu-images/profile_pics/2eaed503-0e10-40a4-b7dc-b63768fecbef"
          },
          "profile": {
            "ftp": 300,
            "eftp": 300,
            "ftp_kg": 4.12,
            "lthr": 157,
            "max_hr": 177,
            "threshold_pace": null,
            "pace_units": null,
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
              "w_prime": 24198,
              "p_max": 942,
              "lthr": 157,
              "max_hr": 177,
              "threshold_pace": null,
              "pace_units": null,
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
              "pace_zones": null,
              "vo2max_garmin": 72,
              "lactate_mmol_l": 1.9,
              "lactate_power": 185
            },
            "run": {
              "ftp": 327,
              "eftp": null,
              "w_prime": null,
              "p_max": null,
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
              "vo2max_garmin": null,
              "lactate_mmol_l": null,
              "lactate_power": null
            },
            "swim": {
              "ftp": null,
              "eftp": null,
              "w_prime": null,
              "p_max": null,
              "lthr": 157,
              "max_hr": 177,
              "threshold_pace": null,
              "pace_units": "SECS_100M",
              "power_zones": null,
              "hr_zones": [
                132,
                140,
                148,
                156,
                161,
                165,
                177
              ],
              "pace_zones": null,
              "vo2max_garmin": null,
              "lactate_mmol_l": null,
              "lactate_power": null
            },
            "ski": {
              "ftp": null,
              "eftp": null,
              "w_prime": null,
              "p_max": null,
              "lthr": 157,
              "max_hr": 177,
              "threshold_pace": null,
              "pace_units": "MINS_KM",
              "power_zones": null,
              "hr_zones": [
                125,
                140,
                146,
                156,
                160,
                165,
                177
              ],
              "pace_zones": null,
              "vo2max_garmin": null,
              "lactate_mmol_l": null,
              "lactate_power": null
            }
          },
          "global": {
            "resting_hr": 41,
            "weight": 72.9,
            "height": 1.81,
            "sex": "M"
          },
          "context": {
            "platforms": {
              "garmin": true,
              "zwift": true,
              "wahoo": true,
              "strava": true,
              "polar": false,
              "suunto": null,
              "coros": false,
              "concept2": false
            },
            "wellness_features": {
              "sources": {
                "garmin": true,
                "whoop": false,
                "oura": false,
                "fitbit": false,
                "polar": false,
                "coros": false,
                "suunto": false
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
              "hrv_available": true,
              "hrv_source": "garmin",
              "weight_sync": "NONE",
              "resting_hr": 41
            },
            "training_environment": {
              "plan": "SUPPORTER",
              "beta_user": true,
              "coach_access": false,
              "language": "en",
              "timezone": "Europe/Zurich"
            },
            "equipment_summary": {
              "bike_count": 9,
              "shoe_count": 7,
              "primary_bike": null,
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
              "last_seen": "2026-03-16T08:01:47.316+00:00"
            }
          }
        },
        "report_type": "weekly",
        "window_days": 6,
        "period": "2026-03-10 \u2192 2026-03-15",
        "report_header": {
          "title": "Weekly Training Report",
          "scope": "Detailed analysis of the last 7 days of training activity",
          "data_sources": "7-day full activities, 42-day wellness, 90 day light activities",
          "intended_use": "Day-to-day coaching decisions, intensity balance, short-term fatigue and recovery management"
        },
        "summary_card_ready": false,
        "events": {
          "is_event_block": true,
          "event_block_count": 8,
          "render": true,
          "notes": "Canonical activity/event block (URF v5.2) \u2014 intended for ChatGPT / structured UI rendering."
        },
        "planned_events": {
          "is_planned_events_block": true,
          "planned_events_block_count": 14,
          "notes": "Canonical planned events block (URF v5.2) \u2014 intended for ChatGPT / structured UI rendering."
        },
        "phases_summary": {
          "is_phase_block": true,
          "phase_block_count": 7,
          "notes": "Macro-level sequential phase summary, intended for ChatGPT / structured UI rendering."
        },
        "resolution": {
          "CTL": "authoritative",
          "ATL": "authoritative",
          "TSB": "authoritative",
          "zones": "authoritative",
          "derived_metrics": "full",
          "performance_intelligence": "acute_full_7d",
          "energy_system_progression": "full",
          "insights": "tactical"
        }
      },
      "metrics": {
        "Polarisation_variants": {
          "fused": {
            "name": "Polarisation_fused",
            "display_name": "Polarisation Index (Fused HR+Power, sport-specific)",
            "value": 0.573,
            "framework": "Seiler / St\u00f6ggl / Issurin (HR+Power fused)",
            "formula": "Normalized intensity-domain distribution (fused HR+Power)",
            "thresholds": {
              "red": [
                0.0,
                0.64
              ],
              "green": [
                0.8,
                3.0
              ],
              "amber": [
                0.65,
                0.8
              ]
            },
            "phase_context": "Overreached",
            "classification": "red",
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
            "value": 2.073,
            "framework": "Seiler / St\u00f6ggl / Issurin (multi-sport combined)",
            "formula": "Normalized global intensity-domain distribution",
            "thresholds": {
              "red": [
                0.0,
                0.59
              ],
              "green": [
                0.78,
                3.0
              ],
              "amber": [
                0.6,
                0.78
              ]
            },
            "phase_context": "Overreached",
            "classification": "green",
            "metric_confidence": "informational",
            "interpretation": "Global HR+Power combined Polarisation Index across all sports. Reflects total weekly distribution and load balance for multi-sport athletes. Dominance reflects intensity signal strength, not training volume. \u22650.80 = polarised, 0.65\u20130.79 = pyramidal, <0.65 = threshold-heavy. \u2699\ufe0f *Cross-discipline index \u2014 lower precision, but best overall summary of load contrast.*",
            "coaching_implication": "If combined Polarisation Index <0.65, total weekly load is intensity-heavy. Add endurance-focused sessions or recovery days to preserve a healthy 80/20 ratio. Ideal global range \u22650.78 for mixed-sport athletes.",
            "related_metrics": {
              "polarised": "\u2265 0.78",
              "pyramidal": "0.65\u20130.77",
              "threshold_dominant": "< 0.65"
            },
            "basis": "Power where available, HR otherwise (multi-sport weighted)",
            "source": "zones.combined",
            "context_window": "7d"
          },
          "context_window": "unknown"
        },
        "ACWR": {
          "value": 1.07,
          "criteria": {
            "recovery": "<0.8",
            "productive": "0.8\u20131.3",
            "aggressive": "1.3\u20131.5",
            "overload": ">1.5"
          },
          "state": "green",
          "icon": "\ud83d\udfe2",
          "framework": "Banister Load Ratio",
          "notes": "EWMA Acute:Chronic Load Ratio \u2014 compares 7-day vs 28-day weighted loads. 0.8\u20131.3 = productive training, <0.8 = recovery or detraining, >1.5 = overload/injury risk.",
          "context_window": "rolling"
        },
        "Monotony": {
          "value": 1.4,
          "criteria": {
            "optimal": "0\u20132",
            "moderate": "2.1\u20132.5",
            "high": ">2.5"
          },
          "state": "green",
          "icon": "\ud83d\udfe2",
          "framework": "Foster 2001",
          "notes": "1\u20132 shows healthy variation; >2.5 means repetitive stress pattern.",
          "context_window": "rolling"
        },
        "Strain": {
          "value": 1062.6,
          "criteria": {
            "low": "<2000",
            "moderate": "2000\u20133000",
            "high": "3000\u20134000",
            "very_high": ">4000"
          },
          "state": "green",
          "icon": "\ud83d\udfe2",
          "framework": "Modified Foster 2001 (TSS-based)",
          "notes": "Modified Foster Strain (\u03a3TSS_7d \u00d7 Monotony). Values >3500 indicate elevated combined load and variability risk; interpret relative to athlete baseline.",
          "context_window": "rolling"
        },
        "FatigueTrend": {
          "value": 8.8,
          "criteria": {
            "balanced": "-10\u201310",
            "moderate_low": "-20\u2013-10",
            "moderate_high": "10\u201320",
            "accumulating": "20\u201340",
            "extreme_accumulation": ">40",
            "recovering": "<-20"
          },
          "state": "green",
          "icon": "\ud83d\udfe2",
          "framework": "Banister EWMA Delta",
          "notes": "FatigueTrend is calculated as the percentage change between the 7-day and 28-day moving averages. A 0% change indicates balance, while a positive percentage change indicates accumulating fatigue, and a negative percentage change indicates recovery.",
          "context_window": "90d"
        },
        "ZQI": {
          "value": 3.2,
          "criteria": {
            "low": "<5",
            "optimal": "5\u201315",
            "high": "15\u201325",
            "excessive": ">25"
          },
          "state": "green",
          "icon": "\ud83d\udfe2",
          "framework": "Seiler Intensity Distribution",
          "notes": "Zone Quality Index (%) 5-15 high-intensity time is normal <3% too easy, >20% too intense or erratic pacing.",
          "context_window": "7d"
        },
        "FatOxEfficiency": {
          "name": "FatOxEfficiency",
          "value": 0.619,
          "classification": "green",
          "interpretation": "0.4\u20130.8 means balanced fat oxidation; lower = carb dependence.",
          "coaching_implication": "If FatOxEfficiency is low (<0.6), focus on improving aerobic base with longer, low-intensity efforts.",
          "related_metrics": {},
          "context_window": "7d"
        },
        "PolarisationIndex": {
          "name": "PolarisationIndex",
          "value": 2.073,
          "classification": "computed",
          "interpretation": "Treff Polarization-Index (2019). Calculated as log10(Z1 / (Z2 \u00d7 Z3) \u00d7 100) after collapsing to the 3-zone Seiler model. >2.0 = polarised distribution, 1.5\u20132.0 = pyramidal, <1.5 = threshold-heavy. \u2699\ufe0f Power-only metric using 3-zone collapsed distribution.",
          "coaching_implication": "If PolarisationIndex <1.5, training is threshold-heavy. Between 1.5\u20132.0 reflects pyramidal distribution. Target >2.0 for classical polarised structure during build or peak phases.",
          "related_metrics": {},
          "context_window": "7d"
        },
        "FOxI": {
          "value": 61.9,
          "criteria": {
            "optimal": ">=70",
            "moderate": "50\u201369",
            "low": "<50"
          },
          "state": "amber",
          "icon": "\ud83d\udfe0",
          "framework": "Internal Derived Metric",
          "notes": "FatOx index %; higher values mean more efficient aerobic base.",
          "context_window": "7d"
        },
        "CUR": {
          "name": "CUR",
          "value": 38.1,
          "classification": "green",
          "interpretation": "Carbohydrate Utilisation Ratio; 30\u201370 indicates balanced metabolic use.",
          "coaching_implication": "If CUR is outside the green zone (30-70), adjust carbohydrate intake and fueling strategy to ensure balanced metabolic use during long sessions.",
          "related_metrics": {},
          "context_window": "7d"
        },
        "GR": {
          "name": "GR",
          "value": 1.65,
          "classification": "green",
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
          "state": "green",
          "icon": "\ud83d\udfe2",
          "framework": "Internal Derived Metric",
          "notes": "Metabolic Efficiency Score; >20 is good endurance economy.",
          "context_window": "7d"
        },
        "LoadVariabilityIndex": {
          "name": "LoadVariabilityIndex",
          "value": 0.72,
          "classification": "green",
          "interpretation": "Inverse Monotony model (Foster 2001): 1 - (Monotony / 5). Represents weekly load variability. Higher values indicate healthier variation in daily training load.",
          "coaching_implication": "Low values indicate load is exceeding current physiological tolerance; moderate values suggest manageable stress; high values reflect positive load variability with adequate systemic capacity.",
          "related_metrics": {},
          "context_window": "unknown"
        },
        "StressTolerance": {
          "value": 1.22,
          "criteria": {
            "underload": "<0.8",
            "optimal": "0.8\u20131.2",
            "aggressive": "1.2\u20131.4",
            "overreach_risk": ">1.4"
          },
          "state": "amber",
          "icon": "\ud83d\udfe0",
          "framework": "Banister Capacity-Adjusted Load Ratio",
          "notes": "Capacity-adjusted weekly load ratio (\u03a3TSS_7d / (CTL \u00d7 7)). 1.0 indicates weekly load equals chronic fitness baseline. Values >1.2 reflect overload relative to adaptive capacity; <0.8 indicates under-stimulation.",
          "context_window": "7d"
        },
        "Polarisation": {
          "name": "Polarisation",
          "display_name": "Polarisation (Power-based, Seiler ratio)",
          "value": 0.573,
          "framework": "Seiler 3-Zone Contrast Model",
          "formula": "(Z1 + Z3+) / (2 \u00d7 Z2)  (3-zone collapsed, renormalised)",
          "thresholds": {
            "red": [
              0.0,
              0.65
            ],
            "amber": [
              0.65,
              0.85
            ],
            "green": [
              0.85,
              3.0
            ]
          },
          "phase_context": "",
          "classification": "red",
          "metric_confidence": "contextual",
          "interpretation": "Power-based Seiler Polarisation Ratio (Z1 + Z3) / (2 \u00d7 Z2), showing the balance between low- and high-intensity work relative to moderate (Z2) training. <0.65 = Z2-dominant distribution, 0.65\u20130.84 = mixed intensity distribution, 0.85\u20131.25 = balanced polarised structure (classic 80/20), >1.25 = high-contrast polarisation with minimal Z2 exposure. \u2699\ufe0f *Power-only metric \u2014 HR ignored.* Use primarily during power-measured cycling phases.",
          "coaching_implication": "If Polarisation <0.65 during base, this reflects aerobic Z2 dominance (\u2705 normal). If in Build/Peak, reduce Z2 time and increase Z1/Z3 contrast. Maintain \u22650.85 for ideal 80/20 balance in power-measured disciplines.",
          "related_metrics": {
            "z2_dominant": "< 0.65",
            "pyramidal": "0.65\u20130.84",
            "polarised": "0.85\u20131.25",
            "high_contrast": "> 1.25"
          }
        }
      },
      "performance_intelligence": {
        "acute": {
          "anaerobic_repeatability": {
            "max_depletion_pct_7d": {
              "name": "max_depletion_pct_7d",
              "display_name": "Max W\u2032 Depletion (7-day)",
              "value": 0.5366145962476238,
              "framework": "W\u2032 Depletion & Repeatability Model (WDRM)",
              "formula": null,
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
              "display_name": "Mean W\u2032 Depletion (7-day)",
              "value": 0.20790285698542585,
              "framework": "W\u2032 Depletion & Repeatability Model (WDRM)",
              "formula": null,
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
              "coaching_implication": {
                "low": "Anaerobic exposure controlled \u2014 maintain structure.",
                "moderate": "Moderate anaerobic load \u2014 ensure recovery spacing.",
                "high": "High W\u2032 depletion \u2014 monitor recovery and intensity stacking."
              },
              "related_metrics": {},
              "context_window": "7d"
            },
            "moderate_depletion_sessions_7d": {
              "name": "moderate_depletion_sessions_7d",
              "display_name": "Moderate W\u2032 Depletion Sessions (7-day)",
              "value": 1,
              "framework": "W\u2032 Depletion & Repeatability Model (WDRM)",
              "formula": null,
              "thresholds": {
                "green": [
                  0,
                  3
                ],
                "amber": [
                  4,
                  6
                ],
                "red": [
                  7,
                  10
                ]
              },
              "phase_context": "",
              "classification": "green",
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
            "high_depletion_sessions_7d": {
              "name": "high_depletion_sessions_7d",
              "display_name": "High W\u2032 Depletion Sessions (7-day)",
              "value": 0,
              "framework": "W\u2032 Depletion & Repeatability Model (WDRM)",
              "formula": null,
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
              "coaching_implication": {
                "low": "Anaerobic exposure controlled \u2014 maintain structure.",
                "moderate": "Moderate anaerobic load \u2014 ensure recovery spacing.",
                "high": "High W\u2032 depletion \u2014 monitor recovery and intensity stacking."
              },
              "related_metrics": {},
              "context_window": "7d"
            },
            "total_joules_above_ftp_7d": {
              "name": "total_joules_above_ftp_7d",
              "display_name": "Total Work Above FTP (7-day)",
              "value": 124833.0,
              "framework": "W\u2032 Depletion & Repeatability Model (WDRM)",
              "formula": null,
              "thresholds": {},
              "phase_context": "",
              "classification": "informational",
              "metric_confidence": "high",
              "interpretation": "WDRM (W\u2032 Depletion & Repeatability Metric) quantifies depth and frequency of anaerobic reserve depletion across sessions. Higher values reflect repeated deep supra-threshold exposure.",
              "coaching_implication": {
                "low": "Anaerobic exposure controlled \u2014 maintain structure.",
                "moderate": "Moderate anaerobic load \u2014 ensure recovery spacing.",
                "high": "High W\u2032 depletion \u2014 monitor recovery and intensity stacking."
              },
              "related_metrics": {},
              "context_window": "7d"
            }
          },
          "model_diagnostics": {
            "w_prime_divergence_7d": {
              "name": "w_prime_divergence_7d",
              "display_name": "W\u2032 Utilisation Divergence (7-day)",
              "value": -0.09209714301457414,
              "framework": "Skiba Critical Power",
              "formula": null,
              "thresholds": {
                "green": [
                  -0.1,
                  0.15
                ],
                "amber": [
                  0.15,
                  0.3
                ],
                "red": [
                  0.3,
                  1.0
                ]
              },
              "phase_context": "",
              "classification": "green",
              "metric_confidence": "contextual",
              "interpretation": "Difference between observed W\u2032 depletion behaviour and expected endurance baseline. Positive values indicate higher-than-normal anaerobic utilisation, while negative values indicate lower-than-expected supra-threshold engagement.",
              "coaching_implication": {
                "green": "Anaerobic utilisation within normal endurance range.",
                "amber": "Elevated W\u2032 usage \u2014 indicates VO\u2082max or anaerobic stimulus.",
                "red": "Very high W\u2032 utilisation \u2014 likely race load or repeated high-intensity sessions."
              },
              "related_metrics": {},
              "context_window": "7d"
            }
          },
          "durability": {
            "mean_decoupling_7d": {
              "name": "mean_decoupling_7d",
              "display_name": "Mean Decoupling (7-day)",
              "value": 6.352027183333334,
              "framework": "Intensity Stability & Durability Model (ISDM)",
              "formula": null,
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
              "classification": "amber",
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
              "display_name": "Max Decoupling (7-day)",
              "value": 13.139739,
              "framework": "Intensity Stability & Durability Model (ISDM)",
              "formula": null,
              "thresholds": {},
              "phase_context": "",
              "classification": "informational",
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
            "high_drift_sessions_7d": {
              "name": "high_drift_sessions_7d",
              "display_name": "High Drift Sessions (7-day)",
              "value": 4,
              "framework": "Intensity Stability & Durability Model (ISDM)",
              "formula": null,
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
              "classification": "amber",
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
            "long_sessions_7d": {
              "name": "long_sessions_7d",
              "display_name": "Long Endurance Sessions (7-day)",
              "value": 1,
              "framework": "Intensity Stability & Durability Model (ISDM)",
              "formula": null,
              "thresholds": {},
              "phase_context": "",
              "classification": "informational",
              "metric_confidence": "high",
              "interpretation": "ISDM (Intensity Stability & Durability Metric) reflects decoupling behaviour under fatigue. Elevated values indicate cardiovascular drift or durability stress.",
              "coaching_implication": {
                "stable": "Durability stable \u2014 cardiovascular drift controlled.",
                "fatigue": "Elevated drift \u2014 consider aerobic consolidation.",
                "severe": "Significant durability stress \u2014 reduce load."
              },
              "related_metrics": {},
              "context_window": "7d"
            }
          },
          "neural_density": {
            "rolling_joules_above_ftp_7d": {
              "name": "rolling_joules_above_ftp_7d",
              "display_name": "Rolling Work Above FTP (7-day)",
              "value": 124833.0,
              "framework": "Neural Density Load Index (NDLI)",
              "formula": null,
              "thresholds": {
                "green": [
                  0,
                  150000
                ],
                "amber": [
                  150000,
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
              "display_name": "High-Intensity Days (7-day)",
              "value": 2,
              "framework": "Neural Density Load Index (NDLI)",
              "formula": null,
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
              "coaching_implication": {
                "balanced": "Intensity density well distributed.",
                "clustered": "High short-term clustering \u2014 monitor recovery.",
                "overloaded": "Neural load accumulation high \u2014 reduce intensity density."
              },
              "related_metrics": {},
              "context_window": "7d"
            },
            "mean_if_7d": {
              "name": "mean_if_7d",
              "display_name": "Mean Intensity Factor (7-day)",
              "value": 0.68757149625,
              "framework": "Neural Density Load Index (NDLI)",
              "formula": null,
              "thresholds": {},
              "phase_context": "",
              "classification": "informational",
              "metric_confidence": "high",
              "interpretation": "NDLI (Neural Density Load Index) captures clustering of high-intensity work within short time windows (e.g. 72h). High density increases recovery demand.",
              "coaching_implication": {
                "balanced": "Intensity density well distributed.",
                "clustered": "High short-term clustering \u2014 monitor recovery.",
                "overloaded": "Neural load accumulation high \u2014 reduce intensity density."
              },
              "related_metrics": {},
              "context_window": "7d"
            },
            "mean_efficiency_factor_7d": {
              "name": "mean_efficiency_factor_7d",
              "display_name": "Mean Efficiency Factor (7-day)",
              "value": 1.9321036333333332,
              "framework": "Neural Density Load Index (NDLI)",
              "formula": null,
              "thresholds": {},
              "phase_context": "",
              "classification": "informational",
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
            "mean_variability_index_7d": {
              "name": "mean_variability_index_7d",
              "display_name": "Mean Variability Index (7-day)",
              "value": 1.1135323166666666,
              "framework": "Neural Density Load Index (NDLI)",
              "formula": null,
              "thresholds": {},
              "phase_context": "",
              "classification": "informational",
              "metric_confidence": "contextual",
              "interpretation": "NDLI (Neural Density Load Index) captures clustering of high-intensity work within short time windows (e.g. 72h). High density increases recovery demand.",
              "coaching_implication": {
                "balanced": "Intensity density well distributed.",
                "clustered": "High short-term clustering \u2014 monitor recovery.",
                "overloaded": "Neural load accumulation high \u2014 reduce intensity density."
              },
              "related_metrics": {},
              "context_window": "7d"
            }
          }
        },
        "chronic": {},
        "version": "PI_v1.3",
        "training_state": {
          "framework": "Autonomic\u2013Load Interaction Model",
          "interpretation": "Load\u2013Recovery state describing the interaction between training load (ATL vs CTL) and autonomic recovery (HRV ratio). Balanced indicates load and recovery aligned. Productive_load indicates elevated load with stable recovery. Adaptation_pressure indicates recovery suppression under load. Maladaptation_risk indicates recovery breakdown relative to training stress.",
          "coaching_implication": "Recovery stable under elevated load \u2014 productive adaptation likely.",
          "context_window": "current_microcycle",
          "classification": "green",
          "classification_source": "load_recovery_state",
          "state_label": "Productive Load",
          "operational_state": "load_accepting",
          "confidence": "moderate",
          "signals": {
            "readiness_signal": "Training load is being absorbed effectively.",
            "adaptation_signal": "Durability strain rising \u2014 aerobic consolidation advised.",
            "load_recovery_state": "productive_load",
            "hrv_ratio": 1.16,
            "atl": 114.37624,
            "ctl": 89.03907
          },
          "operational_context": {
            "framework": "Autonomic\u2013Load Interaction Model",
            "model_basis": "Operational coaching mode derived from autonomic recovery and training load interaction.",
            "signals_used": {
              "hrv_ratio": 1.16,
              "atl": 114.37624,
              "ctl": 89.03907,
              "load_pressure": 25.33717
            },
            "physiological_state": "productive_load",
            "operational_state": "load_accepting",
            "decision_logic": "recovery_priority only when maladaptation risk is detected; otherwise athlete remains in load_accepting mode"
          },
          "recommended_action": {
            "recommendation": "Continue load progression",
            "next_session": "Execute planned structured session"
          },
          "phase_context": null
        }
      },
      "zones": {
        "power": {
          "label": "Cycling Power Zones",
          "description": "Distribution of training time by cycling power zones. Derived from Intervals.icu power zone times for Ride-based activities. SS = Sweetspot",
          "distribution": {
            "z1": 17.8,
            "z2": 43.7,
            "z3": 18.3,
            "z4": 9.6,
            "z5": 3.6,
            "z6": 0.6,
            "z7": 0.2,
            "SS": 6.2
          },
          "thresholds": [
            55,
            75,
            90,
            105,
            120,
            150
          ]
        },
        "hr": {
          "label": "Cycling Heart Rate Zones",
          "description": "Distribution of training time by heart rate zones. Restricted to Ride-based activities for physiological comparability.",
          "distribution": {
            "z1": 75.1,
            "z2": 13.3,
            "z3": 2.7,
            "z4": 6.6,
            "z5": 2.2,
            "z6": 0.0,
            "z7": 0.0
          },
          "thresholds": [
            126,
            140,
            146,
            156,
            160,
            165,
            177
          ]
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
          "confidence": 0.979,
          "reason": "lactate correlation r=0.98",
          "lactate_thresholds": {}
        },
        "fused": {
          "per_sport": {
            "Ride": {
              "_fused_power_z1": 17.8,
              "_fused_power_z2": 43.7,
              "_fused_power_z3": 18.3,
              "_fused_power_z4": 9.6,
              "_fused_power_z5": 3.6,
              "_fused_power_z6": 0.6,
              "_fused_power_z7": 0.2,
              "_fused_power_SS": 6.2,
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
            }
          },
          "basis": "Sport-specific fusion of power and HR zones (power preferred, HR fallback)"
        },
        "combined": {
          "label": "Combined Intensity Distribution",
          "description": "Global distribution of training time across intensity zones for all endurance activities. Power is prioritised where available, heart rate otherwise. Normalised once across total training time (Seiler / St\u00f6ggl / Issurin methodology) SS = Sweetspot.",
          "distribution": {
            "z1": 47.8,
            "z2": 27.8,
            "z3": 10.3,
            "z4": 7.8,
            "z5": 2.8,
            "z6": 0.3,
            "z7": 0.1,
            "SS": 3.1
          },
          "basis": "Time-based intensity distribution across all endurance activities. Power used when available, HR otherwise. Normalised once across total training time (Seiler / St\u00f6ggl / Issurin methodology)."
        }
      },
      "daily_load": [
        {
          "date": "2026-03-10 00:00:00",
          "tss": 117.0
        },
        {
          "date": "2026-03-11 00:00:00",
          "tss": 76.0
        },
        {
          "date": "2026-03-12 00:00:00",
          "tss": 75.0
        },
        {
          "date": "2026-03-13 00:00:00",
          "tss": 119.0
        },
        {
          "date": "2026-03-14 00:00:00",
          "tss": 257.0
        },
        {
          "date": "2026-03-15 00:00:00",
          "tss": 115.0
        }
      ],
      "events": [
        {
          "id": "i131018911",
          "start_date_local": "2026-03-10T17:49:12",
          "name": "Zwift - : Threshold 4x12",
          "type": "VirtualRide",
          "activity_id": "i131018911",
          "activity_link": "https://intervals.icu/activities/i131018911",
          "IF": 0.87,
          "paired_event_id": 95094556.0,
          "compliance": 97.5,
          "distance": 61932.43,
          "moving_time": 5561,
          "icu_training_load": 117,
          "average_heartrate": 135.0,
          "average_cadence": 79.22953,
          "icu_average_watts": 230.0,
          "icu_variability_index": 1.1347826,
          "icu_weighted_avg_watts": 261.0,
          "strain_score": 115.82623,
          "trimp": 155.73944,
          "hr_load": 119.0,
          "ss_cp": 114.664894,
          "icu_efficiency_factor": 1.9333333,
          "icu_intensity": 87.0,
          "icu_power_hr": 1.7037038,
          "decoupling": 6.821523,
          "icu_pm_w_prime": 23557.0,
          "icu_w_prime": 24198.0,
          "icu_max_wbal_depletion": 4542.0,
          "icu_joules_above_ftp": 12174.0,
          "total_elevation_gain": 95.0,
          "calories": 1227.0,
          "VO2MaxGarmin": 72.0,
          "source": "ZWIFT",
          "device_name": "ZWIFT",
          "icu_rpe": 6.0,
          "feel": 3.0,
          "rpe_emoji": "6\ufe0f\u20e3",
          "feel_emoji": "\ud83d\ude10",
          "wbal_engagement": "light",
          "wbal_pattern": "repeated",
          "wbal_depth_pct": 0.193,
          "event_efficiency": "efficient",
          "event_efficiency_value": 1.933,
          "heart_rate_recovery_60s": 34.0,
          "heart_rate_recovery_start_bpm": 161.0,
          "heart_rate_recovery_end_bpm": 127.0
        },
        {
          "id": "i131306402",
          "start_date_local": "2026-03-11T18:49:53",
          "name": "Zwift - Intervals.icu: VO2 Max 2x(5x3min) legs said no",
          "type": "VirtualRide",
          "activity_id": "i131306402",
          "activity_link": "https://intervals.icu/activities/i131306402",
          "IF": 0.867,
          "paired_event_id": 97802277.0,
          "compliance": 65.51724,
          "distance": 18262.77,
          "moving_time": 3653,
          "icu_training_load": 76,
          "average_heartrate": 124.0,
          "average_cadence": 77.36182,
          "icu_average_watts": 217.0,
          "icu_variability_index": 1.1981567,
          "icu_weighted_avg_watts": 260.0,
          "strain_score": 80.24019,
          "trimp": 75.97004,
          "hr_load": 66.0,
          "ss_cp": 75.452385,
          "icu_efficiency_factor": 2.096774,
          "icu_intensity": 86.666664,
          "icu_power_hr": 1.75,
          "decoupling": 13.139739,
          "icu_pm_w_prime": 21102.0,
          "icu_w_prime": 24198.0,
          "icu_max_wbal_depletion": 12985.0,
          "icu_joules_above_ftp": 41703.0,
          "total_elevation_gain": 937.0,
          "calories": 759.0,
          "VO2MaxGarmin": 72.0,
          "source": "ZWIFT",
          "device_name": "ZWIFT",
          "icu_rpe": 8.0,
          "feel": 4.0,
          "rpe_emoji": "8\ufe0f\u20e3",
          "feel_emoji": "\ud83d\ude41",
          "wbal_engagement": "heavy",
          "wbal_pattern": "stochastic",
          "wbal_depth_pct": 0.615,
          "event_efficiency": "efficient",
          "event_efficiency_value": 2.097,
          "heart_rate_recovery_60s": 33.0,
          "heart_rate_recovery_start_bpm": 157.0,
          "heart_rate_recovery_end_bpm": 124.0
        },
        {
          "id": "i131573077",
          "start_date_local": "2026-03-12T18:12:31",
          "name": "Zwift - : Aerobic Endurance",
          "type": "VirtualRide",
          "activity_id": "i131573077",
          "activity_link": "https://intervals.icu/activities/i131573077",
          "IF": 0.683,
          "paired_event_id": 95094642.0,
          "compliance": 60.0,
          "distance": 65231.33,
          "moving_time": 5815,
          "icu_training_load": 75,
          "average_heartrate": 115.0,
          "average_cadence": 80.04679,
          "icu_average_watts": 201.0,
          "icu_variability_index": 1.0199004,
          "icu_weighted_avg_watts": 205.0,
          "strain_score": 98.71681,
          "trimp": 94.724365,
          "hr_load": 78.0,
          "ss_cp": 98.661736,
          "icu_efficiency_factor": 1.7826087,
          "icu_intensity": 68.333336,
          "icu_power_hr": 1.7478261,
          "decoupling": 1.1519938,
          "icu_pm_w_prime": 18185.0,
          "icu_w_prime": 24198.0,
          "icu_max_wbal_depletion": 437.0,
          "icu_joules_above_ftp": 574.0,
          "total_elevation_gain": 311.0,
          "calories": 1118.0,
          "VO2MaxGarmin": 72.0,
          "source": "ZWIFT",
          "device_name": "ZWIFT",
          "icu_rpe": 4.0,
          "feel": 4.0,
          "rpe_emoji": "4\ufe0f\u20e3",
          "feel_emoji": "\ud83d\ude41",
          "wbal_engagement": "light",
          "wbal_pattern": "single",
          "wbal_depth_pct": 0.024,
          "event_efficiency": "efficient",
          "event_efficiency_value": 1.783
        },
        {
          "id": "i131752105",
          "start_date_local": "2026-03-13T15:05:31",
          "name": "Afternoon Ride",
          "type": "Ride",
          "activity_id": "i131752105",
          "activity_link": "https://intervals.icu/activities/i131752105",
          "IF": 0.79,
          "compliance": 0.0,
          "distance": 54462.67,
          "moving_time": 6840,
          "icu_training_load": 119,
          "average_heartrate": 120.0,
          "average_cadence": 82.33567,
          "icu_average_watts": 194.0,
          "icu_variability_index": 1.2216495,
          "icu_weighted_avg_watts": 237.0,
          "strain_score": 122.14721,
          "trimp": 123.40932,
          "hr_load": 110.0,
          "ss_cp": 114.58652,
          "icu_efficiency_factor": 1.975,
          "icu_intensity": 79.0,
          "icu_power_hr": 1.6166667,
          "decoupling": -1.5174943,
          "icu_pm_w_prime": 19283.0,
          "icu_w_prime": 24198.0,
          "icu_max_wbal_depletion": 10056.0,
          "icu_joules_above_ftp": 62935.0,
          "total_elevation_gain": 855.0,
          "calories": 1483.0,
          "VO2MaxGarmin": 67.62835693359375,
          "source": "GARMIN_CONNECT",
          "device_name": "Garmin Edge 840",
          "icu_rpe": 4.0,
          "feel": 3.0,
          "rpe_emoji": "4\ufe0f\u20e3",
          "feel_emoji": "\ud83d\ude10",
          "wbal_engagement": "heavy",
          "wbal_pattern": "stochastic",
          "wbal_depth_pct": 0.521,
          "event_efficiency": "efficient",
          "event_efficiency_value": 1.975,
          "heart_rate_recovery_60s": 55.0,
          "heart_rate_recovery_start_bpm": 158.0,
          "heart_rate_recovery_end_bpm": 103.0
        },
        {
          "id": "i131960957",
          "start_date_local": "2026-03-14T10:53:56",
          "name": "Zwift - Intervals.icu: Long Endurance",
          "type": "VirtualRide",
          "activity_id": "i131960957",
          "activity_link": "https://intervals.icu/activities/i131960957",
          "IF": 0.727,
          "paired_event_id": 95094644.0,
          "compliance": 98.01588,
          "distance": 141171.62,
          "moving_time": 16842,
          "icu_training_load": 247,
          "average_heartrate": 119.0,
          "average_cadence": 78.1721,
          "icu_average_watts": 211.0,
          "icu_variability_index": 1.0331753,
          "icu_weighted_avg_watts": 218.0,
          "strain_score": 303.22375,
          "trimp": 306.3233,
          "hr_load": 242.0,
          "ss_cp": 302.74667,
          "icu_efficiency_factor": 1.8319328,
          "icu_intensity": 72.666664,
          "icu_power_hr": 1.7731092,
          "decoupling": 6.023952,
          "icu_pm_w_prime": 20396.0,
          "icu_w_prime": 24198.0,
          "icu_max_wbal_depletion": 1327.0,
          "icu_joules_above_ftp": 4984.0,
          "total_elevation_gain": 2386.0,
          "calories": 3394.0,
          "VO2MaxGarmin": 72.0,
          "source": "ZWIFT",
          "device_name": "ZWIFT",
          "icu_rpe": 7.0,
          "feel": 3.0,
          "rpe_emoji": "7\ufe0f\u20e3",
          "feel_emoji": "\ud83d\ude10",
          "wbal_engagement": "light",
          "wbal_pattern": "repeated",
          "wbal_depth_pct": 0.065,
          "event_efficiency": "efficient",
          "event_efficiency_value": 1.832
        },
        {
          "id": "i131987034",
          "start_date_local": "2026-03-14T16:10:15",
          "name": "otto walk",
          "type": "Hike",
          "activity_id": "i131987034",
          "activity_link": "https://intervals.icu/activities/i131987034",
          "IF": 0.316,
          "distance": 5000.0,
          "moving_time": 3600,
          "icu_training_load": 10,
          "icu_intensity": 31.622776,
          "icu_w_prime": 19440.0,
          "calories": 438.0,
          "source": "GARMIN_CONNECT",
          "device_name": "GARMIN CONNECT",
          "icu_rpe": 3.0,
          "feel": 3.0,
          "rpe_emoji": "3\ufe0f\u20e3",
          "feel_emoji": "\ud83d\ude10",
          "wbal_engagement": "none",
          "wbal_pattern": "none",
          "wbal_depth_pct": 0.0,
          "event_efficiency": "unknown",
          "event_efficiency_value": null
        },
        {
          "id": "i132108891",
          "start_date_local": "2026-03-15T08:19:57",
          "name": "Otto walk",
          "type": "Hike",
          "activity_id": "i132108891",
          "activity_link": "https://intervals.icu/activities/i132108891",
          "IF": 0.518,
          "distance": 5926.23,
          "moving_time": 4144,
          "icu_training_load": 33,
          "average_heartrate": 106.0,
          "average_cadence": 55.041786,
          "trimp": 51.252613,
          "hr_load": 33.0,
          "icu_intensity": 51.767757,
          "icu_w_prime": 19440.0,
          "total_elevation_gain": 148.0,
          "calories": 628.0,
          "source": "GARMIN_CONNECT",
          "device_name": "Garmin epix (Gen 2)",
          "icu_rpe": 3.0,
          "feel": 3.0,
          "rpe_emoji": "3\ufe0f\u20e3",
          "feel_emoji": "\ud83d\ude10",
          "wbal_engagement": "none",
          "wbal_pattern": "none",
          "wbal_depth_pct": 0.0,
          "event_efficiency": "unknown",
          "event_efficiency_value": null
        },
        {
          "id": "i132220963",
          "start_date_local": "2026-03-15T15:26:32",
          "name": "Zwift - Alpe",
          "type": "VirtualRide",
          "activity_id": "i132220963",
          "activity_link": "https://intervals.icu/activities/i132220963",
          "IF": 0.73,
          "paired_event_id": 95094555.0,
          "compliance": 82.828285,
          "distance": 33752.22,
          "moving_time": 5534,
          "icu_training_load": 82,
          "average_heartrate": 111.0,
          "average_cadence": 77.73662,
          "icu_average_watts": 204.0,
          "icu_variability_index": 1.0735294,
          "icu_weighted_avg_watts": 219.0,
          "strain_score": 96.474556,
          "trimp": 79.36288,
          "hr_load": 74.0,
          "ss_cp": 96.23019,
          "icu_efficiency_factor": 1.972973,
          "icu_intensity": 73.0,
          "icu_power_hr": 1.8378378,
          "decoupling": 9.457461,
          "icu_pm_w_prime": 20099.0,
          "icu_w_prime": 24198.0,
          "icu_max_wbal_depletion": 838.0,
          "icu_joules_above_ftp": 2463.0,
          "total_elevation_gain": 1229.0,
          "calories": 1078.0,
          "VO2MaxGarmin": 72.0,
          "source": "ZWIFT",
          "device_name": "ZWIFT",
          "wbal_engagement": "light",
          "wbal_pattern": "repeated",
          "wbal_depth_pct": 0.042,
          "event_efficiency": "efficient",
          "event_efficiency_value": 1.973
        }
      ],
      "wellness": {
        "hrv_ratio": 1.16,
        "rest_hr": 42.1,
        "hrv_trend": 27.0,
        "rest_days": 0,
        "ctl": 89.03907,
        "atl": 114.37624,
        "tsb": -25.33717,
        "coverage": {
          "unit": "proportion",
          "hrv_pct": 0.977,
          "resting_hr_pct": 1.0,
          "sleep_pct": 0.977,
          "subjective_pct": 0.14,
          "total_days": 43
        },
        "hrv_mean": 53.4,
        "hrv_latest": 62.0,
        "hrv_trend_7d": 2.0,
        "hrv_source": "garmin",
        "hrv_available": true,
        "hrv_samples": 42,
        "hrv_series": [
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
          },
          {
            "date": "2026-02-23",
            "hrv": 52.0
          },
          {
            "date": "2026-02-24",
            "hrv": 58.0
          },
          {
            "date": "2026-02-25",
            "hrv": 55.0
          },
          {
            "date": "2026-02-26",
            "hrv": 46.0
          },
          {
            "date": "2026-02-27",
            "hrv": 56.0
          },
          {
            "date": "2026-02-28",
            "hrv": 53.0
          },
          {
            "date": "2026-03-01",
            "hrv": 43.0
          },
          {
            "date": "2026-03-02",
            "hrv": 47.0
          },
          {
            "date": "2026-03-03",
            "hrv": 57.0
          },
          {
            "date": "2026-03-04",
            "hrv": 65.0
          },
          {
            "date": "2026-03-05",
            "hrv": 51.0
          },
          {
            "date": "2026-03-06",
            "hrv": 54.0
          },
          {
            "date": "2026-03-07",
            "hrv": 54.0
          },
          {
            "date": "2026-03-08",
            "hrv": 43.0
          },
          {
            "date": "2026-03-09",
            "hrv": 53.0
          },
          {
            "date": "2026-03-10",
            "hrv": 55.0
          },
          {
            "date": "2026-03-11",
            "hrv": 61.0
          },
          {
            "date": "2026-03-12",
            "hrv": 63.0
          },
          {
            "date": "2026-03-13",
            "hrv": 55.0
          },
          {
            "date": "2026-03-14",
            "hrv": 57.0
          },
          {
            "date": "2026-03-15",
            "hrv": 35.0
          },
          {
            "date": "2026-03-16",
            "hrv": 62.0
          }
        ],
        "subjective": {
          "fatigue": {
            "value": 2.0,
            "label": "avg"
          },
          "stress": {
            "value": 1.8,
            "label": "avg"
          },
          "soreness": {
            "value": 1.8,
            "label": "avg"
          },
          "mood": {
            "value": 2.7,
            "label": "ok"
          },
          "motivation": {
            "value": 2.8,
            "label": "avg"
          },
          "injury": {
            "value": 1.0,
            "label": "none"
          },
          "hydration": {
            "value": 2.0,
            "label": "ok"
          }
        },
        "CTL": 89.03907,
        "ATL": 114.37624,
        "TSB": -25.33717
      },
      "training_volume": {
        "hours": 14.44,
        "tss": 759.0,
        "distance_km": 385.7
      },
      "physiology": {
        "lactate_calibration": {
          "lactate": {
            "available": true,
            "samples": 35,
            "mean_mmol": 1.92,
            "latest_mmol": 1.8,
            "range_mmol": [
              1.8,
              2.0
            ],
            "paired_with_power": true,
            "power_field": "HrtLndLt1p",
            "power_spread_w": [
              170.0,
              195.0
            ],
            "power_source": "activity_samples",
            "corr_with_power": 0.979,
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
            "samples": 35
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
            "confidence_r": 0.979,
            "source": "extended_metrics"
          }
        }
      },
      "wbal_summary": {
        "mean_wbal_depletion_pct": 0.243,
        "mean_anaerobic_contrib_pct": 1.026,
        "sessions_with_wbal_data": 6,
        "basis": "per-session mean (W\u2032-capable sessions only)",
        "window": "weekly",
        "temporal_pattern": {
          "2026-03-10": "moderate",
          "2026-03-11": "high",
          "2026-03-12": "low",
          "2026-03-13": "high",
          "2026-03-14": "low",
          "2026-03-15": "low"
        },
        "dominant_pattern": "distributed"
      },
      "planned_summary_by_iso_week": {
        "2026-W12": {
          "total_events": 7,
          "total_duration_minutes": 630.0,
          "total_load": 544,
          "categories": [
            "WORKOUT"
          ]
        },
        "2026-W13": {
          "total_events": 7,
          "total_duration_minutes": 859.0,
          "total_load": 780,
          "categories": [
            "WORKOUT"
          ]
        }
      },
      "planned_events": [
        {
          "id": 95094646,
          "uid": "1d5f93d3-ca0e-4a98-b860-e13ea4f3cc03",
          "category": "WORKOUT",
          "name": "Aerobic Endurance",
          "description": "- 10m 60% FTP easy\n- 100m 72% FTP steady\n- 10m 60% FTP easy",
          "start_date_local": "2026-03-16T00:00:00",
          "end_date_local": "2026-03-17T00:00:00",
          "duration_minutes": 120.0,
          "icu_training_load": 99,
          "strain_score": 127.91555,
          "day_of_week": "Monday"
        },
        {
          "id": 95094647,
          "uid": "9b5141fd-e3ae-40c5-8d0c-645c544ba218",
          "category": "WORKOUT",
          "name": "Threshold 3x20",
          "description": "- 15m Ramp 60-85% FTP\n- 20m 100% FTP\n- 8m 60% FTP recovery\n- 20m 100% FTP\n- 8m 60% FTP recovery\n- 20m 100% FTP\n- 14m 65% FTP steady",
          "start_date_local": "2026-03-17T00:00:00",
          "end_date_local": "2026-03-18T00:00:00",
          "duration_minutes": 105.0,
          "icu_training_load": 142,
          "strain_score": 144.54582,
          "day_of_week": "Tuesday"
        },
        {
          "id": 95094648,
          "uid": "e0a83781-8b54-453d-974b-2577ed119684",
          "category": "WORKOUT",
          "name": "Endurance Easy",
          "description": "- 10m 60% FTP easy\n- 70m 68% FTP steady\n- 10m 60% FTP easy",
          "start_date_local": "2026-03-18T00:00:00",
          "end_date_local": "2026-03-19T00:00:00",
          "duration_minutes": 90.0,
          "icu_training_load": 66,
          "strain_score": 89.73626,
          "day_of_week": "Wednesday"
        },
        {
          "id": 95094649,
          "uid": "74775898-7f80-412a-a501-7dc486c3b6f3",
          "category": "WORKOUT",
          "name": "Openers",
          "description": "- 15m 60% FTP easy\n- 3m 110% FTP\n- 3m 60% FTP recovery\n- 3m 110% FTP\n- 3m 60% FTP recovery\n- 3m 110% FTP\n- 30m 65% FTP steady",
          "start_date_local": "2026-03-19T00:00:00",
          "end_date_local": "2026-03-20T00:00:00",
          "duration_minutes": 60.0,
          "icu_training_load": 59,
          "strain_score": 67.30607,
          "day_of_week": "Thursday"
        },
        {
          "id": 95094650,
          "uid": "376b13cd-625c-44fa-87a7-42636ec3d31e",
          "category": "WORKOUT",
          "name": "Endurance Easy",
          "description": "- 10m 60% FTP easy\n- 55m 68% FTP steady\n- 10m 60% FTP easy",
          "start_date_local": "2026-03-20T00:00:00",
          "end_date_local": "2026-03-21T00:00:00",
          "duration_minutes": 75.0,
          "icu_training_load": 54,
          "strain_score": 74.30852,
          "day_of_week": "Friday"
        },
        {
          "id": 95094651,
          "uid": "59df9dc2-c38c-4cb3-b10c-b08443de4040",
          "category": "WORKOUT",
          "name": "Aerobic Endurance",
          "description": "- 10m 60% FTP easy\n- 100m 70% FTP steady\n- 10m 60% FTP easy",
          "start_date_local": "2026-03-21T00:00:00",
          "end_date_local": "2026-03-22T00:00:00",
          "duration_minutes": 120.0,
          "icu_training_load": 94,
          "strain_score": 124.23236,
          "day_of_week": "Saturday"
        },
        {
          "id": 95094652,
          "uid": "76887458-94b2-4b53-b766-ceb24a764d57",
          "category": "WORKOUT",
          "name": "Recovery Ride",
          "description": "- 60m 55% FTP easy",
          "start_date_local": "2026-03-22T00:00:00",
          "end_date_local": "2026-03-23T00:00:00",
          "duration_minutes": 60.0,
          "icu_training_load": 30,
          "strain_score": 48.10585,
          "day_of_week": "Sunday"
        },
        {
          "id": 95094653,
          "uid": "4a29c420-314a-4d80-a2a6-58dc6e927ed8",
          "category": "WORKOUT",
          "name": "Endurance Easy",
          "description": "- 10m 60% FTP easy\n- 40m 65% FTP steady\n- 10m 60% FTP easy",
          "start_date_local": "2026-03-23T00:00:00",
          "end_date_local": "2026-03-24T00:00:00",
          "duration_minutes": 60.0,
          "icu_training_load": 40,
          "strain_score": 56.727695,
          "day_of_week": "Monday"
        },
        {
          "id": 95094654,
          "uid": "88c083c4-2532-442a-9a34-09dae9615e85",
          "category": "WORKOUT",
          "name": "Recovery Spin",
          "description": "- 45m 55% FTP easy",
          "start_date_local": "2026-03-24T00:00:00",
          "end_date_local": "2026-03-25T00:00:00",
          "duration_minutes": 45.0,
          "icu_training_load": 23,
          "strain_score": 36.079388,
          "day_of_week": "Tuesday"
        },
        {
          "id": 97805567,
          "uid": "2f5c730a-0ce5-49b0-9fbc-dda43bed5cf6",
          "category": "WORKOUT",
          "name": "VO2 Max 2x(5x3min) @115% FTP",
          "description": "- 12m Ramp 60-85% FTP\n- 3m 115% FTP\n- 3m 55% FTP recovery\n- 3m 115% FTP\n- 3m 55% FTP recovery\n- 3m 115% FTP\n- 3m 55% FTP recovery\n- 3m 115% FTP\n- 3m 55% FTP recovery\n- 3m 115% FTP\n- 6m 55% FTP recovery\n- 3m 115% FTP\n- 3m 55% FTP recovery\n- 3m 115% FTP\n- 3m 55% FTP recovery\n- 3m 115% FTP\n- 3m 55% FTP recovery\n- 3m 115% FTP\n- 3m 55% FTP recovery\n- 3m 115% FTP\n- 10m Ramp 70-40% FTP cooldown",
          "start_date_local": "2026-03-25T00:00:00",
          "end_date_local": "2026-03-26T00:00:00",
          "duration_minutes": 82.0,
          "icu_training_load": 114,
          "strain_score": 125.75104,
          "day_of_week": "Wednesday"
        },
        {
          "id": 97805568,
          "uid": "9f235bdc-4140-45ce-9012-fefbe4200528",
          "category": "WORKOUT",
          "name": "Aerobic Endurance + Neuromuscular Sprints",
          "description": "- 15m 60% FTP easy\n- 10s 220% FTP sprint\n- 5m 55% FTP recovery\n- 10s 220% FTP sprint\n- 5m 55% FTP recovery\n- 10s 220% FTP sprint\n- 5m 55% FTP recovery\n- 10s 220% FTP sprint\n- 5m 55% FTP recovery\n- 10s 220% FTP sprint\n- 5m 55% FTP recovery\n- 10s 220% FTP sprint\n- 90m 72% FTP steady\n- 10m 60% FTP easy",
          "start_date_local": "2026-03-26T00:00:00",
          "end_date_local": "2026-03-27T00:00:00",
          "duration_minutes": 141.0,
          "icu_training_load": 115,
          "strain_score": 148.05183,
          "day_of_week": "Thursday"
        },
        {
          "id": 97805569,
          "uid": "c2380efd-90ff-42f8-a633-bfa52c33cd9c",
          "category": "WORKOUT",
          "name": "Aerobic Endurance",
          "description": "- 10m 60% FTP easy\n- 120m 72% FTP steady\n- 10m 60% FTP easy",
          "start_date_local": "2026-03-27T00:00:00",
          "end_date_local": "2026-03-28T00:00:00",
          "duration_minutes": 140.0,
          "icu_training_load": 117,
          "strain_score": 149.95064,
          "day_of_week": "Friday"
        },
        {
          "id": 97805570,
          "uid": "2918365d-583f-4107-a64b-6d4f36417c84",
          "category": "WORKOUT",
          "name": "Threshold 4x12",
          "description": "- 15m Ramp 60-85% FTP\n- 12m 100% FTP\n- 6m 60% FTP recovery\n- 12m 100% FTP\n- 6m 60% FTP recovery\n- 12m 100% FTP\n- 6m 60% FTP recovery\n- 12m 100% FTP\n- 10m 65% FTP steady",
          "start_date_local": "2026-03-28T00:00:00",
          "end_date_local": "2026-03-29T00:00:00",
          "duration_minutes": 91.0,
          "icu_training_load": 119,
          "strain_score": 122.421074,
          "day_of_week": "Saturday"
        },
        {
          "id": 97805571,
          "uid": "e7c227d3-3751-43da-ac02-9e39ff349189",
          "category": "WORKOUT",
          "name": "Long Endurance",
          "description": "- 20m 60% FTP easy\n- 240m 72% FTP steady\n- 40m 70% FTP steady",
          "start_date_local": "2026-03-29T00:00:00",
          "end_date_local": "2026-03-30T00:00:00",
          "duration_minutes": 300.0,
          "icu_training_load": 252,
          "strain_score": 324.75806,
          "day_of_week": "Sunday"
        }
      ],
      "planned_summary_by_date": {
        "2026-03-16": {
          "total_events": 1,
          "total_duration": 120.0,
          "total_load": 99,
          "categories": [
            "WORKOUT"
          ]
        },
        "2026-03-17": {
          "total_events": 1,
          "total_duration": 105.0,
          "total_load": 142,
          "categories": [
            "WORKOUT"
          ]
        },
        "2026-03-18": {
          "total_events": 1,
          "total_duration": 90.0,
          "total_load": 66,
          "categories": [
            "WORKOUT"
          ]
        },
        "2026-03-19": {
          "total_events": 1,
          "total_duration": 60.0,
          "total_load": 59,
          "categories": [
            "WORKOUT"
          ]
        },
        "2026-03-20": {
          "total_events": 1,
          "total_duration": 75.0,
          "total_load": 54,
          "categories": [
            "WORKOUT"
          ]
        },
        "2026-03-21": {
          "total_events": 1,
          "total_duration": 120.0,
          "total_load": 94,
          "categories": [
            "WORKOUT"
          ]
        },
        "2026-03-22": {
          "total_events": 1,
          "total_duration": 60.0,
          "total_load": 30,
          "categories": [
            "WORKOUT"
          ]
        },
        "2026-03-23": {
          "total_events": 1,
          "total_duration": 60.0,
          "total_load": 40,
          "categories": [
            "WORKOUT"
          ]
        },
        "2026-03-24": {
          "total_events": 1,
          "total_duration": 45.0,
          "total_load": 23,
          "categories": [
            "WORKOUT"
          ]
        },
        "2026-03-25": {
          "total_events": 1,
          "total_duration": 82.0,
          "total_load": 114,
          "categories": [
            "WORKOUT"
          ]
        },
        "2026-03-26": {
          "total_events": 1,
          "total_duration": 141.0,
          "total_load": 115,
          "categories": [
            "WORKOUT"
          ]
        },
        "2026-03-27": {
          "total_events": 1,
          "total_duration": 140.0,
          "total_load": 117,
          "categories": [
            "WORKOUT"
          ]
        },
        "2026-03-28": {
          "total_events": 1,
          "total_duration": 91.0,
          "total_load": 119,
          "categories": [
            "WORKOUT"
          ]
        },
        "2026-03-29": {
          "total_events": 1,
          "total_duration": 300.0,
          "total_load": 252,
          "categories": [
            "WORKOUT"
          ]
        }
      },
      "future_forecast": {
        "start_date": "2026-03-16",
        "end_date": "2026-03-30",
        "horizon_days": 14,
        "CTL_future": 91.2,
        "ATL_future": 111.08,
        "TSB_future": -19.88,
        "load_trend": "increasing",
        "fatigue_class": "productive_fatigue"
      },
      "future_actions": [
        {
          "priority": "normal",
          "title": "Productive training fatigue",
          "reason": "Training load is high but within a productive overload zone.",
          "label": "Productive fatigue \u2014 overload zone",
          "color": "#ffcc66",
          "date_range": "2026-03-16 \u2192 2026-03-30"
        }
      ],
      "actions": [
        {
          "type": "state_action",
          "label": "Training State",
          "source": "tier3_training_state",
          "model": "Seiler Load Governance",
          "recommendation": "Continue load progression",
          "readiness_signal": "Training load is being absorbed effectively.",
          "state_label": "Productive Load",
          "operational_state": "load_accepting",
          "operational_context": {
            "framework": "Autonomic\u2013Load Interaction Model",
            "model_basis": "Operational coaching mode derived from autonomic recovery and training load interaction.",
            "signals_used": {
              "hrv_ratio": 1.16,
              "atl": 114.37624,
              "ctl": 89.03907,
              "load_pressure": 25.33717
            },
            "physiological_state": "productive_load",
            "operational_state": "load_accepting",
            "decision_logic": "recovery_priority only when maladaptation risk is detected; otherwise athlete remains in load_accepting mode"
          }
        },
        {
          "type": "system_guidance",
          "label": "Energy System Direction",
          "sport": "Ride",
          "source": "energy_system_progression",
          "model": "Energy System Progression Engine",
          "system_state": "aerobic_consolidation",
          "message": "Aerobic development progressing while VO\u2082 capacity drifts \u2014 reintroduce VO\u2082 stimulus within the next microcycle."
        },
        {
          "type": "reflection",
          "source": "montis_question_engine",
          "signal": "durability_pressure",
          "question": "Is durability progressing as training volume increases?"
        }
      ],
      "energy_system_progression": {
        "version": "espe_v1.1",
        "sports": {
          "Ride": {
            "supported": true,
            "curve_window": {
              "current_days": 85,
              "previous_days": 85,
              "comparison": "85d_vs_85d",
              "anchor": "report_end",
              "curve_source": "FFT_CURVES"
            },
            "power_curve_anchors": {
              "context": {
                "window_days": 85,
                "description": "Best power values recorded within the last 85 days"
              },
              "values": {
                "5s": {
                  "power": 826,
                  "activity_id": "i130433348",
                  "activity_link": "https://intervals.icu/activities/i130433348"
                },
                "1m": {
                  "power": 466,
                  "activity_id": "i119106703",
                  "activity_link": "https://intervals.icu/activities/i119106703"
                },
                "5m": {
                  "power": 333,
                  "activity_id": "i120238341",
                  "activity_link": "https://intervals.icu/activities/i120238341"
                },
                "20m": {
                  "power": 307,
                  "activity_id": "i126785019",
                  "activity_link": "https://intervals.icu/activities/i126785019"
                },
                "60m": {
                  "power": 288,
                  "activity_id": "i122292136",
                  "activity_link": "https://intervals.icu/activities/i122292136"
                }
              }
            },
            "delta_percent": {
              "5s": -1.2,
              "1m": -4.7,
              "5m": -7.24,
              "20m": 1.99,
              "60m": 5.11
            },
            "curve_dynamics": {
              "vertical_shift_pct": -1.21,
              "rotation_index": -9.52,
              "dominant_shift": "aerobic_rotation"
            },
            "system_status": {
              "anaerobic": "decline",
              "vo2": "decline",
              "threshold": "moderate_gain",
              "aerobic_durability": "strong_gain"
            },
            "system_status_timeline": {
              "anaerobic": "detraining",
              "vo2": "detraining",
              "threshold": "building",
              "aerobic_durability": "building"
            },
            "derived_metrics": {
              "glycolytic_bias_ratio": {
                "name": "glycolytic_bias_ratio",
                "value": 1.52,
                "framework": "Energy System Balance Model",
                "interpretation": "Ratio of short-duration power to threshold power indicating glycolytic dominance.",
                "coaching_implication": "High values suggest anaerobic bias relative to aerobic capacity.",
                "related_metrics": {},
                "context_window": "85d_vs_85d"
              },
              "aerobic_durability_ratio": {
                "name": "aerobic_durability_ratio",
                "value": 0.86,
                "framework": "Durability / Endurance Model",
                "interpretation": "Ratio of 60-minute power to 5-minute power reflecting endurance durability across prolonged efforts.",
                "coaching_implication": "Lower ratios suggest fatigue-driven endurance drop-off.",
                "related_metrics": {},
                "context_window": "85d_vs_85d"
              },
              "durability_gradient": {
                "name": "durability_gradient",
                "value": 0.94,
                "framework": "Durability Gradient Model",
                "interpretation": "Ratio of 60-minute power to 20-minute power reflecting fatigue resistance across prolonged efforts.",
                "coaching_implication": "Lower gradients indicate durability decline during long efforts.",
                "related_metrics": {},
                "context_window": "85d_vs_85d"
              },
              "system_balance_score": {
                "name": "system_balance_score",
                "value": 0.84,
                "framework": "Energy System Balance Composite",
                "interpretation": "Composite indicator describing balance of energy system development.",
                "coaching_implication": "Values closer to 1 indicate balanced development across systems.",
                "related_metrics": {},
                "context_window": "85d_vs_85d"
              },
              "pdr_5m": {
                "name": "pdr_5m",
                "value": 39,
                "framework": "Power Duration Reserve",
                "interpretation": "Difference between 5-minute power and Critical Power representing VO\u2082 reserve capacity.",
                "coaching_implication": "Higher reserve suggests strong VO\u2082 capacity above threshold.",
                "related_metrics": {},
                "context_window": "85d_vs_85d"
              },
              "vo2_reserve_ratio": {
                "name": "vo2_reserve_ratio",
                "value": 1.133,
                "framework": "Critical Power / VO\u2082 Reserve Model",
                "interpretation": "Ratio of 5-minute power to Critical Power reflecting VO\u2082 headroom above threshold.",
                "coaching_implication": "Lower ratios indicate fatigue or VO\u2082 limitation.",
                "related_metrics": {},
                "context_window": "85d_vs_85d"
              }
            },
            "curve_regression": {
              "model": "power_duration_log_regression",
              "slope": -0.5515565406556674,
              "r2": 0.8945937596093888
            },
            "curve_quality": "excellent",
            "power_model": {
              "source": "FFT_CURVES",
              "model_quality": "excellent",
              "cp": 294,
              "w_prime": 15360,
              "pmax": 835,
              "ftp": 300
            },
            "plateau_detected": false,
            "adaptation_bias": "threshold_dominant",
            "adaptation_state": "aerobic_consolidation",
            "curve_profile": "all_rounder",
            "system_guidance": "Aerobic development progressing while VO\u2082 capacity drifts \u2014 reintroduce VO\u2082 stimulus within the next microcycle."
          }
        }
      },
      "current_ISO_weekly_microcycle": {
        "week_iso": "2026-W12",
        "weekly_target_tss": 544.0,
        "completed_tss": 0.0,
        "planned_remaining_tss": 544.0,
        "projected_total_tss": 544.0,
        "delta_to_target": 0.0,
        "basis": "The microcycle is based on the current ISO week (Monday to Sunday) and includes planned and completed with compliance,",
        "completed_hours": 0.0,
        "projected_hours": 0.0,
        "is_projected": true
      },
      "phases": [
        {
          "week": "2025-W51",
          "start": "2025-12-15",
          "end": "2025-12-21",
          "distance_km": 163.4,
          "hours": 8.4,
          "tss": 344.0,
          "ctl": 74.54,
          "atl": 61.87,
          "tsb": 12.66,
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
          "classification": "Neutral"
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
          "classification": "Neutral"
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
          "classification": "Neutral"
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
          "classification": "Neutral"
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
          "classification": "Neutral"
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
          "classification": "Productive_fatigue"
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
          "classification": "Neutral"
        },
        {
          "week": "2026-W9",
          "start": "2026-02-23",
          "end": "2026-03-01",
          "distance_km": 327.6,
          "hours": 13.4,
          "tss": 691.0,
          "ctl": 78.91,
          "atl": 91.19,
          "tsb": -12.28,
          "classification": "Productive_fatigue"
        },
        {
          "week": "2026-W10",
          "start": "2026-03-02",
          "end": "2026-03-08",
          "distance_km": 375.6,
          "hours": 13.4,
          "tss": 714.0,
          "ctl": 82.15,
          "atl": 98.61,
          "tsb": -16.46,
          "classification": "Productive_fatigue"
        },
        {
          "week": "2026-W11",
          "start": "2026-03-09",
          "end": "2026-03-15",
          "distance_km": 385.7,
          "hours": 14.4,
          "tss": 759.0,
          "ctl": 86.05,
          "atl": 105.84,
          "tsb": -19.79,
          "classification": "Productive_fatigue"
        }
      ],
      "insights": {
        "fat_oxidation_index": {
          "value": 61.9,
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
        "load_trend": {
          "value": 21.9,
          "window": "7d vs 28d",
          "basis": "Training load change relative to baseline",
          "interpretation": "Recent load rising rapidly",
          "coaching_implication": "Monitor fatigue accumulation if sustained."
        },
        "fitness_trend": {
          "value": 0.71,
          "window": "CTL slope",
          "basis": "Change in chronic training load",
          "interpretation": "Fitness building steadily",
          "coaching_implication": "Continue progressive overload."
        },
        "fatigue_trend": {
          "value": 2.72,
          "window": "ATL slope",
          "basis": "Change in short-term training stress",
          "interpretation": "Stable fatigue load",
          "coaching_implication": "Load appears manageable."
        },
        "energy_system_progression": {
          "Ride": {
            "window": "85d_vs_85d",
            "basis": "Power-duration curve progression",
            "system_status": {
              "anaerobic": "decline",
              "vo2": "decline",
              "threshold": "moderate_gain",
              "aerobic_durability": "strong_gain"
            },
            "adaptation_state": "aerobic_consolidation",
            "adaptation_bias": "threshold_dominant"
          }
        }
      },
      "insight_view": {
        "critical": [],
        "watch": [],
        "positive": [
          {
            "name": "fat_oxidation_index",
            "classification": "green",
            "interpretation": "FatOx index %; higher values mean more efficient aerobic base.",
            "coaching_implication": "If FOxI is increasing, continue to prioritize low-intensity work to enhance fat metabolism. If it decreases, consider increasing your Zone 2 training duration."
          },
          {
            "name": "LoadVariabilityIndex",
            "classification": "green",
            "interpretation": "Inverse Monotony model (Foster 2001): 1 - (Monotony / 5). Represents weekly load variability. Higher values indicate healthier variation in daily training load.",
            "coaching_implication": "Low values indicate load is exceeding current physiological tolerance; moderate values suggest manageable stress; high values reflect positive load variability with adequate systemic capacity."
          }
        ]
      },
      "renderer_instructions": "You are a deterministic URF renderer.\n\n    You must render a **Weekly Training Report** using the embedded system context.\n    This report follows the **Unified Reporting Framework (URF v5.1)**.\n\n    **Scope:** Detailed analysis of the last 7 days of training activity\n    **Data Sources:** 7-day full activities, 42-day wellness, 90 day light activities\n    **Intended Use:** Day-to-day coaching decisions, intensity balance, short-term fatigue and recovery management\n    DATA RESOLUTION MODEL:\n\n        This report uses the following semantic resolution rules.\n\n        - CTL: authoritative\n- ATL: authoritative\n- TSB: authoritative\n- zones: authoritative\n- derived_metrics: full\n- performance_intelligence: acute_full_7d\n- energy_system_progression: full\n- insights: tactical\n\n        These rules determine which metrics are authoritative,\n        which signals may appear, and the time horizon used\n        for interpretation.\n\n        Resolution rules MUST NOT be printed in the report output.\n    HARD RULES:\n    - Render exactly ONE report.\n- All sections MUST appear under their corresponding stack layer header.\n- Stack layer headers MUST be rendered using the provided stack labels in uppercase.\n- Do NOT add numeric prefixes to section headers.\n- Use emoji-based section headers only.\n- Preserve section order exactly as defined by the contract.\n- Metric context MUST be derived exclusively from each metric\u2019s `context_window` and `confidence_model` fields.\n- When both wellness signals and performance_intelligence metrics are present, interpret recovery state as the physiological response to recent training stress. Insights should reconcile these layers rather than repeating them independently.\n\n    STACK STRUCTURE RULE:\n\n        The report MUST be organised into the following conceptual intelligence layers:\n\n        Meta Context:\n- meta\n\nTraining Load:\n- training_volume\n- metrics\n- daily_load\n- events\n\nPhysiology Response:\n- wellness\n- insight_view\n\nPerformance Intelligence:\n- performance_intelligence\n- wbal_summary\n\nAdaptation:\n- energy_system_progression\n- physiology\n- zones\n\nAdaptive Decisions:\n- actions\n- planned_events\n- planned_summary_by_date\n- current_ISO_weekly_microcycle\n- planned_summary_by_iso_week\n- future_forecast\n- future_actions\n\n\n        These layers are PRESENTATIONAL GROUPINGS ONLY.\n\n        They must NOT:\n        - change section order\n        - override section_handling rules\n        - modify interpretation_rules\n        - alter table rendering rules\n\n        Sections must appear in the exact URF contract order.\n        Stack layers only determine which layer header a section appears under.\n\n        Each section must appear under its corresponding stack layer while still following the URF section order.\n        A stack layer header MUST be rendered once when the first section belonging to that layer appears.\n        Subsequent sections mapped to the same stack layer MUST remain under that header and MUST NOT repeat the header.\n\n    STACK SECTION MAP:\n        meta \u2192 \ud83d\udcca REPORT CONTEXT\ntraining_volume \u2192 \ud83e\udded TRAINING LOAD\nmetrics \u2192 \ud83e\udded TRAINING LOAD\ndaily_load \u2192 \ud83e\udded TRAINING LOAD\nevents \u2192 \ud83e\udded TRAINING LOAD\nwellness \u2192 \ud83e\udec0 PHYSIOLOGY RESPONSE\ninsight_view \u2192 \ud83e\udec0 PHYSIOLOGY RESPONSE\nperformance_intelligence \u2192 \u2699\ufe0f PERFORMANCE INTELLIGENCE\nwbal_summary \u2192 \u2699\ufe0f PERFORMANCE INTELLIGENCE\nenergy_system_progression \u2192 \ud83d\udcc8 ADAPTATION\nphysiology \u2192 \ud83d\udcc8 ADAPTATION\nzones \u2192 \ud83d\udcc8 ADAPTATION\nactions \u2192 \ud83c\udfaf ADAPTIVE DECISIONS\nplanned_events \u2192 \ud83c\udfaf ADAPTIVE DECISIONS\nplanned_summary_by_date \u2192 \ud83c\udfaf ADAPTIVE DECISIONS\ncurrent_ISO_weekly_microcycle \u2192 \ud83c\udfaf ADAPTIVE DECISIONS\nplanned_summary_by_iso_week \u2192 \ud83c\udfaf ADAPTIVE DECISIONS\nfuture_forecast \u2192 \ud83c\udfaf ADAPTIVE DECISIONS\nfuture_actions \u2192 \ud83c\udfaf ADAPTIVE DECISIONS\n\n    INTERPRETATION RULES:\n    - Interpretations may be descriptive or conditional, not predictive.\n- If semantic.training_volume exists, render it under the header 'Training Volume' with three stacked metrics: Hours, Training Load (TSS), Distance.\n- If semantic.wbal_summary.temporal_pattern exists, render a one-line anaerobic load timeline using block symbols (\u2582 \u2583 \u2587) mapped to none/low/moderate/high.\n- If semantic.daily_load exists, render it as a compact monoblock map timeline with weekday labels, relative load blocks, and numeric TSS values aligned underneath. Do NOT render daily_load as a list or table.\n- If semantic.daily_load exists AND semantic.wellness.CTL and semantic.wellness.ATL are present, a second symbolic fatigue-pressure row MAY be rendered using \u2191 \u2193 \u2014 symbols based ONLY on the sign of (ATL \u2212 CTL). No magnitude, thresholds, or new calculations are permitted.\n- All rows in the daily load timeline MUST use a fixed-width column per day to ensure vertical alignment across labels, blocks, symbols, and numeric values.\n- If session-level signal icons are rendered in the EVENTS table, a single legend line MUST be rendered once per report directly below the EVENTS section header.\n- If zone distribution data exists (e.g. zone_dist_power, zone_dist_hr, zone_dist_fused), render zone distribution as fixed-width ASCII proportional bars (one bar per zone), with the exact percentage shown. Bars are presentational only and do not constitute derived metrics.\n- If semantic.zones.lactate_calibration exists and lactate.available is true, render a Lactate Calibration subsection summarising mean mmol/L, latest mmol/L, sample count, and inferred LT1 power. This is descriptive only and must not derive new values.\n- If performance_intelligence exists, render three subsections: Anaerobic Repeatability (WDRM), Durability (ISDM), Neural Density (NDLI). Use provided values only. Do NOT recompute or merge with other metrics.\n- If high_dep_sessions > 0 and high_drift_sessions > 0 in the same week, describe this as high neuromuscular + metabolic strain overlap.\n- Interpretation may combine signals across sections when they describe the same physiological process (e.g. fatigue, adaptation, durability).\n- When energy_system_progression exists, generate at least one sentence summarising the current adaptation direction using system_status and adaptation_state.\n- Insights SHOULD prioritise adaptation signals (ESPE) before repeating metric definitions.\n- When activity_link exists inside energy_system_progression.power_curve_anchors.values, the corresponding power value MUST be rendered as a Markdown link using the format: [<power> W](activity_link).\n- If activity_link is missing, the power value MUST be rendered normally without a link.\n- Ensure current_ISO_weekly_microcycle is totled as 'Current ISO Week ## (Mon-Sun)'\n\n    COACHING INTERPRETATION RULES:\n- You are an Endurance Coach\n- You MAY include up to 5 short coaching sentence(s) per section.\n- Coaching sentences MUST be directly anchored to values, states, or interpretation fields in that section.\n- Coaching sentences MUST be descriptive or conditional, not predictive.\n- Coaching sentences MUST appear immediately after the section\u2019s data and before the next divider.\n- Coaching sentences MUST NOT introduce new metrics.\n\n    ALLOWED ENRICHMENT:\n        - Restate semantic interpretation fields.\n- Explain what a value indicates within its known threshold or state.\n- derive_stepwise_forecast\n\n\n\n\n\n    STATE PRESENTATION:\n- Present a concise, single-sentence state banner at the top of the report.\n- Use ONLY semantic states already present in the data.\n- Do NOT derive, compute, or infer new states.\n- Style: single_sentence_banner\n\n    EMPHASIS GUIDANCE:\n        The following sections should receive proportional narrative and visual emphasis.\n        This does NOT change section order, inclusion, or data fidelity.\n        - metrics: high\n- actions: high\n- events: medium\n- wellness: medium\n- adaptation: high\n\n    FRAMING INTENT:\n- Interpret and summarise this report through the following intent:\n  tactical_weekly_control\n- This intent guides prioritisation and narrative focus only.\n\n    SECTION HANDLING RULES:\n        - meta: full\n- training_volume: full\n- events: full\n- current_ISO_weekly_microcycle: full\n- daily_load: full\n- metrics: summary\n- performance_intelligence: full\n- energy_system_progression: full\n- zones: forbid\n- physiology: full\n- wellness: summary\n- phases: forbid\n- planned_events: full\n- planned_summary_by_date: forbid\n- planned_summary_by_iso_week: full\n- actions: full\n- future_actions: full\n- insights: forbid\n- insight_view: summary\n\n        Handling meanings:\n\n        - full:\n            Render the entire section exactly as provided.\n            Tables remain tables, lists remain lists.\n            Do not remove rows or fields.\n\n        - summary:\n            Render a compact representation using ONLY existing semantic aggregates\n            already present in the section. Do NOT derive new metrics.\n\n        Summary rules:\n            Prefer a short table if aggregate values exist.\n            If aggregates do not exist, show the top-level fields only.\n            Do NOT iterate full arrays or lists.\n            Do NOT narrate each element of a list.\n            Maximum 3\u20135 rows or key metrics.\n\n        - table_summary:\n            Render a condensed table using aggregate fields only.\n            Do NOT render the full underlying dataset.\n\n        - headline:\n            Render only the primary indicators of the section.\n            Maximum 3\u20134 metrics.\n            No tables longer than one row.\n            No subsections.\n            No detailed narrative.\n\n        Rules:\n        \u2022 Maximum 5 rows.\n        \u2022 Prefer totals, means, or trend indicators already provided.\n        \u2022 Do NOT derive calculations.\n\n        - forbid:\n        This section MUST NOT be rendered in the report output.\n        It may still be used internally for reasoning.\n\n    EVENTS (WEEKLY \u2014 NON-NEGOTIABLE):\n        - The events section MUST be rendered as a Markdown table.\n- EVERY event in the semantic JSON MUST appear as exactly one row.\n- The events section MUST NOT be summarised, renamed, grouped, or rewritten.\n- Bullet points, highlights, or narrative descriptions of events are FORBIDDEN.\n- Coaching sentences for events, if enabled, MUST appear AFTER the table.\n- The EVENTS table MUST use the defined column order.\n- In the EVENTS table, session-level signal icons MAY be rendered within the Activity column as a prefix using the canonical mapping derived ONLY from existing semantic fields.\n- Icons represent independent session signals and MAY appear together for a single event.\n- Add rpe_emoji and feel_emoji to the right of TSS value tightly coupled.\n- When multiple icons apply, they MUST be rendered together in the defined fixed order.\n- Icons are visual aliases only and must not replace numeric values, suppress other applicable icons, or reduce table rows.\n- When `activity_link` exists, the Activity column MUST render the activity name as a Markdown link: [name](activity_link).\n- Icons MUST appear before the link inside the same Activity cell.\n- Show icon legends underneath the table tightly coupled.\n\n        - The EVENTS table MUST use the following column order:\n        Date | Activity | Duration (min) | Distance | TSS | IF | NP | HRR60\n\n        - The semantic field `duration_seconds` MUST be converted to minutes at render time.\n- This conversion applies ONLY to duration.\n- Display as integer minutes by default.\n- Use one decimal only if duration < 30 minutes and precision is useful.\n- Label column as Duration (min). Show HRR60 column when values exist.\n\n        - When multiple icons apply, they MUST be rendered together in the following fixed order (left \u2192 right):\n        1) \u26a1 Efficient (optimal efficiency factor)\n2) \ud83d\udfe2 Aerobic (low IF with stable decoupling)\n3) \ud83d\udca5 Anaerobic (heavy W\u2032 engagement)\n4) \ud83d\udd01 Repeated (repeated W\u2032 depletion pattern)\n5) \ud83d\udcc8 Progressive (progressive W\u2032 engagement)\n6) \ud83e\uddd8 Recovery (very low intensity recovery session)\n7) \u2764\ufe0f Heart_rate_recovery_60s (Heart Rate Recovery within 60s)\n\n    PLANNED EVENTS (WEEKLY \u2014 NON-NEGOTIABLE):\n        - The planned_events section MUST be rendered as a Markdown table.\n- EVERY planned event in the semantic JSON MUST appear as exactly one row.\n- The planned_events section MUST NOT be summarised, renamed, grouped, or rewritten.\n- Narrative descriptions of planned events are FORBIDDEN.\n- Coaching sentences for planned_events, if enabled, MUST appear AFTER the table.\n\n    LIST RENDERING RULES (NON-NEGOTIABLE):\n    - If a section value is a JSON array (list), render it as a Markdown table.\n- Render EVERY element in the array.\n- Preserve one row per array element.\n- Do NOT summarise the list unless explicitly allowed by section handling.\n- Do NOT replace lists with prose unless explicitly allowed.\n- Do NOT omit rows for brevity.\n\n    TONE AND STYLE:\n    - Keep tone factual, supportive, neutral, and coach-like.\n\n    SECTION ORDER (INSTRUCTIONAL \u2014 DO NOT NUMBER HEADERS):\n    1. meta\n2. training_volume\n3. metrics\n4. daily_load\n5. events\n6. wellness\n7. insight_view\n8. performance_intelligence\n9. wbal_summary\n10. energy_system_progression\n11. physiology\n12. zones\n13. actions\n14. planned_events\n15. planned_summary_by_date\n16. current_ISO_weekly_microcycle\n17. planned_summary_by_iso_week\n18. future_forecast\n19. future_actions\n20. phases\n21. insights\n\n    CLOSING NOTE REQUIREMENTS:\n- The closing note MUST begin with one of the following classifications:\nProductive, High Strain, Overreached.\n- State clearly whether last week\u2019s training load was handled appropriately.\n- The closing note MUST remain within the conceptual focus: tactical_alignment.\n- Assess whether acute load and recovery state align with immediate training intent.\n- It MUST anchor strictly to: ACWR, FatigueTrend, NDLI, Durability, performance_intelligence.training_state, energy_system_progression, actions.\n- It MUST NOT introduce new metrics or reinterpret semantic data.\n- Maximum 4 sentences.\n\n    CLOSING REFLECTION RULE:\n        After the full report is produced, generate exactly ONE short reflective coaching question.\n\n        The question MUST be based on the dominant signal in the report.\n\n        Allowed reflection themes:\n        - adaptation\n- fatigue\n- perceived exertion (RPE / feel)\n- training load\n\n        The closing question must be grounded in the signals present in the report\n        and must not introduce new metrics or predictions.\n\n        Format exactly as:\n        ---\n        Closing Reflection\n        <question>"

}
