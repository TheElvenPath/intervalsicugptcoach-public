# tier3_performance_intelligence.py
"""
Tier 3 — Performance Intelligence

Contracts:
    WDRM → Anaerobic Repeatability (W′ depletion behavior)
    ISDM → Durability (decoupling & session drift)
    NDLI → Neural Density (high-intensity clustering)

Weekly → 7d FULL dataset (high resolution)
Season → 90d LIGHT chronic aggregation + 7d acute overlay
"""


from audit_core.utils import debug
import pandas as pd

PI_VERSION = "PI_v1.2"
# ===========================================================
# Public Entry
# ===========================================================

def compute_performance_intelligence(context, contract_type="weekly"):
    """
    Tier-3 Performance Intelligence

    Weekly:
        High-resolution model using 7-day FULL.

    Season:
        Chronic aggregation using 90-day LIGHT
        + Acute overlay using 7-day FULL.
    """

    df_full = context.get("_df_scope_full")
    df_light = context.get("_df_light_90d")

    debug(context, f"[T3] Performance Intelligence start ({contract_type})")

    if contract_type == "season":
        result = _compute_season(context, df_light, df_full)
    else:
        result = _compute_weekly(context, df_full)

    # ✅ Make result visible to interpreter
    context["performance_intelligence"] = result
    context["PI_VERSION"] = PI_VERSION

    # ✅ Now interpret using actual data
    interpretation = interpret_training_state(context)
    context["training_state"] = interpretation
    debug(context, f"[T3 OUTPUT KEYS] {list(result.keys())}")

    return result


# ===========================================================
# WEEKLY (7-DAY FULL – DO NOT COMPROMISE)
# ===========================================================

def _compute_weekly(context, df_full):

    if df_full is None or df_full.empty:
        debug(context, "[T3] Weekly: No FULL data")
        return _empty_weekly()

    debug(context, f"[T3] Weekly FULL rows: {len(df_full)}")

    w_prime = pd.to_numeric(df_full.get("icu_w_prime"), errors="coerce")
    depletion = pd.to_numeric(df_full.get("icu_max_wbal_depletion"), errors="coerce")
    joules = pd.to_numeric(df_full.get("icu_joules_above_ftp"), errors="coerce")
    decoupling_raw = pd.to_numeric(df_full.get("decoupling"), errors="coerce")
    efficiency = pd.to_numeric(df_full.get("icu_efficiency_factor"), errors="coerce")
    variability = pd.to_numeric(df_full.get("icu_variability_index"), errors="coerce")
    polarisation = pd.to_numeric(df_full.get("polarization_index"), errors="coerce")
    decoupling = decoupling_raw.abs()
    if_values = pd.to_numeric(df_full.get("icu_intensity"), errors="coerce")
    # normalize legacy intensity values (sometimes stored as %)
    if if_values is not None and if_values.dropna().size > 0 and if_values.max() > 2:
        if_values = if_values / 100
    moving_time = pd.to_numeric(df_full.get("moving_time"), errors="coerce")

    depletion_pct = None
    if w_prime is not None and depletion is not None:
        depletion_pct = (depletion / w_prime.replace(0, pd.NA)).clip(upper=1.5)

    # ---------------------------------------------
    # W′ utilization divergence (physiological)
    # ---------------------------------------------

    divergence = None

    if depletion_pct is not None and not depletion_pct.dropna().empty:

        mean_dep = depletion_pct.dropna().mean()

        # expected endurance baseline
        expected = 0.30

        divergence = float(mean_dep - expected)

        debug(
            context,
            "[T3][W′] Utilization divergence",
            f"{divergence:.3f}",
            f"(mean_dep={mean_dep:.3f}, baseline={expected})"
        )

    weekly_result = {
        "anaerobic_repeatability": {
            "max_depletion_pct_7d": _safe_max(depletion_pct),
            "mean_depletion_pct_7d": _safe_mean(depletion_pct),
            "moderate_depletion_sessions_7d": _safe_count(depletion_pct, 0.5),
            "high_depletion_sessions_7d": _safe_count(depletion_pct, 0.6),
            "total_joules_above_ftp_7d": _safe_sum(joules),
        },
        "model_diagnostics": {
            "w_prime_divergence_7d": divergence,
        },
        "durability": {
            "mean_decoupling_7d": _safe_mean(decoupling),
            "max_decoupling_7d": _safe_max(decoupling),
            "high_drift_sessions_7d": _safe_count(decoupling, 5.0),
            "long_sessions_7d": _safe_count(moving_time, 7200),
        },
        "neural_density": {
            "rolling_joules_above_ftp_7d": _safe_sum(joules),
            "high_intensity_days_7d": _safe_count(joules, 20000),
            "mean_if_7d": _safe_mean(if_values),

            # new Tier-3 signals
            "mean_efficiency_factor_7d": _safe_mean(efficiency),
            "mean_variability_index_7d": _safe_mean(variability),
        }
    }

    # -----------------------------------------------------------
    # T3 CONTRACT DEBUG — WEEKLY
    # -----------------------------------------------------------

    wdrm = weekly_result["anaerobic_repeatability"]
    isdm = weekly_result["durability"]
    ndli = weekly_result["neural_density"]

    debug(context, "[T3][WDRM] Anaerobic Repeatability (7d)",
        f"max_dep_pct={wdrm['max_depletion_pct_7d']}",
        f"mean_dep_pct={wdrm['mean_depletion_pct_7d']}",
        f"high_dep_sessions={wdrm['high_depletion_sessions_7d']}",
        f"joules_above_ftp={wdrm['total_joules_above_ftp_7d']}")

    debug(context, "[T3][ISDM] Durability (7d)",
        f"mean_decoupling={isdm['mean_decoupling_7d']}",
        f"max_decoupling={isdm['max_decoupling_7d']}",
        f"high_drift_sessions={isdm['high_drift_sessions_7d']}",
        f"long_sessions={isdm['long_sessions_7d']}")

    debug(context, "[T3][NDLI] Neural Density (7d)",
        f"rolling_joules={ndli['rolling_joules_above_ftp_7d']}",
        f"high_intensity_days={ndli['high_intensity_days_7d']}",
        f"mean_if={ndli['mean_if_7d']}")

    return weekly_result


# ===========================================================
# SEASON (90-DAY LIGHT + WEEKLY OVERLAY)
# ===========================================================

def _compute_season(context, df_light, df_full):

    if df_light is None or df_light.empty:
        debug(context, "[T3] Season: No LIGHT data")
        return _empty_season()

    debug(context, f"[T3] Season LIGHT rows: {len(df_light)}")

    # -------- Chronic 90d State --------

    # rolling CP model vs athlete profile W′
    rolling_w_prime = pd.to_numeric(df_light.get("icu_rolling_w_prime"), errors="coerce")
    athlete_w_prime = pd.to_numeric(df_light.get("icu_w_prime"), errors="coerce")

    # ensure Series
    if not isinstance(rolling_w_prime, pd.Series):
        rolling_w_prime = pd.Series([rolling_w_prime] * len(df_light))

    if not isinstance(athlete_w_prime, pd.Series):
        athlete_w_prime = pd.Series([athlete_w_prime] * len(df_light))

    depletion = pd.to_numeric(df_light.get("icu_max_wbal_depletion"), errors="coerce")

    if not isinstance(depletion, pd.Series):
        depletion = pd.Series([depletion] * len(df_light))

    joules = pd.to_numeric(df_light.get("icu_joules_above_ftp"), errors="coerce")
    decoupling = pd.to_numeric(df_light.get("decoupling"), errors="coerce")

    if_values = pd.to_numeric(
        df_light.get("icu_intensity", df_light.get("IF")),
        errors="coerce"
    )

    # normalize legacy IF values
    if if_values is not None and if_values.max() > 2:
        if_values = if_values / 100

    training_load = pd.to_numeric(df_light.get("icu_training_load"), errors="coerce")
    efficiency = pd.to_numeric(df_light.get("icu_efficiency_factor"), errors="coerce")
    variability = pd.to_numeric(df_light.get("icu_variability_index"), errors="coerce")
    polarisation = pd.to_numeric(df_light.get("polarization_index"), errors="coerce")

    # -----------------------------
    # W′ depletion %
    # -----------------------------

    depletion_pct = None
    if rolling_w_prime is not None and depletion is not None:
        depletion_pct = (depletion / rolling_w_prime.replace(0, pd.NA)).clip(upper=1.5)

    # -----------------------------
    # W′ model divergence (90d)
    # -----------------------------

    divergence_90d = None

    if rolling_w_prime is not None and athlete_w_prime is not None:

        rolling_clean = rolling_w_prime.replace(0, pd.NA)
        athlete_clean = athlete_w_prime.replace(0, pd.NA)

        valid_mask = rolling_clean.notna() & athlete_clean.notna()

        if valid_mask.any():

            mean_rolling = rolling_clean[valid_mask].mean()
            mean_athlete = athlete_clean[valid_mask].mean()

            if pd.notna(mean_athlete) and mean_athlete != 0:

                divergence_90d = float((mean_rolling - mean_athlete) / mean_athlete)

                # clamp extreme outliers
                divergence_90d = max(min(divergence_90d, 1.0), -1.0)

                debug(
                    context,
                    "[T3][W′] Model divergence (90d)",
                    f"{divergence_90d:.3f}",
                    f"(rolling={mean_rolling:.0f}, athlete={mean_athlete:.0f})"
                )

    model_diag = {}

    if divergence_90d is not None:
        model_diag["w_prime_divergence_90d"] = divergence_90d

    chronic = {
        "anaerobic_repeatability": {
            "mean_depletion_pct_90d": _safe_mean(depletion_pct),
            "max_depletion_pct_90d": _safe_max(depletion_pct),
            "moderate_depletion_sessions_90d": _safe_count(depletion_pct, 0.5),
            "high_depletion_sessions_90d": _safe_count(depletion_pct, 0.6),
            "total_joules_above_ftp_90d": _safe_sum(joules),
        },

        "model_diagnostics": model_diag,

        "durability": {
            "mean_decoupling_90d": _safe_mean(decoupling),
            "max_decoupling_90d": _safe_max(decoupling),
            "high_drift_sessions_90d": _safe_count(decoupling, 5.0),
        },

        "neural_density": {
            "high_intensity_sessions_90d": _safe_count(joules, 20000),
            "mean_if_90d": _safe_mean(if_values),
            "mean_training_load_90d": _safe_mean(training_load),

            # new Tier-3 signals
            "mean_efficiency_factor_90d": _safe_mean(efficiency),
            "mean_variability_index_90d": _safe_mean(variability),
        }
    }

    # -------- Acute Overlay (full fidelity weekly) --------

    if df_full is not None and not df_full.empty:
        acute_overlay = _compute_weekly(context, df_full)
    else:
        acute_overlay = _empty_weekly()

    # -----------------------------------------------------------
    # T3 CONTRACT DEBUG — SEASON (CHRONIC 90D)
    # -----------------------------------------------------------

    wdrm_c = chronic["anaerobic_repeatability"]
    isdm_c = chronic["durability"]
    ndli_c = chronic["neural_density"]

    debug(context, "[T3][SEASON][WDRM] Chronic Anaerobic Repeatability (90d)",
        f"mean_dep_pct={wdrm_c['mean_depletion_pct_90d']}",
        f"max_dep_pct={wdrm_c['max_depletion_pct_90d']}",
        f"moderate_dep_sessions={wdrm_c['moderate_depletion_sessions_90d']}",
        f"high_dep_sessions={wdrm_c['high_depletion_sessions_90d']}",
        f"total_joules_above_ftp={wdrm_c['total_joules_above_ftp_90d']}")

    debug(context, "[T3][SEASON][ISDM] Chronic Durability (90d)",
        f"mean_decoupling={isdm_c['mean_decoupling_90d']}",
        f"max_decoupling={isdm_c['max_decoupling_90d']}",
        f"high_drift_sessions={isdm_c['high_drift_sessions_90d']}")

    debug(context, "[T3][SEASON][NDLI] Chronic Neural Density (90d)",
        f"high_intensity_sessions={ndli_c['high_intensity_sessions_90d']}",
        f"mean_if={ndli_c['mean_if_90d']}",
        f"mean_training_load={ndli_c['mean_training_load_90d']}")

    # -----------------------------------------------------------
    # Acute vs Chronic Delta Debug
    # -----------------------------------------------------------

    if acute_overlay:

        wdrm_a = acute_overlay["anaerobic_repeatability"]
        isdm_a = acute_overlay["durability"]

        acute_mean_dep = wdrm_a.get("mean_depletion_pct_7d")
        chronic_mean_dep = wdrm_c.get("mean_depletion_pct_90d")

        acute_mean_dec = isdm_a.get("mean_decoupling_7d")
        chronic_mean_dec = isdm_c.get("mean_decoupling_90d")

        dep_ratio = None
        drift_ratio = None

        if acute_mean_dep is not None and chronic_mean_dep not in (None, 0):
            dep_ratio = acute_mean_dep / chronic_mean_dep

        if acute_mean_dec is not None and chronic_mean_dec not in (None, 0):
            drift_ratio = acute_mean_dec / chronic_mean_dec

        debug(
            context,
            "[T3][SEASON][DELTA] Acute vs Chronic",
            f"dep_ratio={dep_ratio}",
            f"drift_ratio={drift_ratio}",
        )

    return {
        "chronic_state": chronic,
        "acute_overlay": acute_overlay
    }


def interpret_training_state(context):

    # Synthesizes Tier-3 metrics into athlete-facing decisions.

    pi = context.get("performance_intelligence", {})
    # weekly + season compatibility
    if "acute" in pi:
        pi = pi["acute"]
    elif "acute_overlay" in pi:
        pi = pi["acute_overlay"]
    future = context.get("future_forecast", {})
    wellness = context.get("wellness_summary", {})
    phase = (
        context.get("current_phase")
        or context.get("phase_detected")
        or (context.get("phases", [{}])[-1].get("phase") if context.get("phases") else None)
    )

    # --------------------------------------------------
    # Pull signals (safe extraction)
    # --------------------------------------------------

    wdrm = (pi.get("anaerobic_repeatability") or {}).get("mean_depletion_pct_7d")
    durability = (pi.get("durability") or {}).get("mean_decoupling_7d")
    neural = (pi.get("neural_density") or {}).get("rolling_joules_above_ftp_7d")

    tsb_class = future.get("fatigue_class")
    recovery_index = wellness.get("recovery_index")


    # --------------------------------------------------
    # Load vs Recovery detection
    # --------------------------------------------------

    wellness = context.get("wellness_summary", {})

    autonomic_ratio = wellness.get("hrv_ratio")

    atl = wellness.get("atl") or wellness.get("ATL")
    ctl = wellness.get("ctl") or wellness.get("CTL")

    # convert Series → scalar if needed
    try:
        if hasattr(atl, "iloc"):
            atl = float(atl.iloc[-1])
        if hasattr(ctl, "iloc"):
            ctl = float(ctl.iloc[-1])
    except Exception:
        pass

    debug(
        context,
        f"[T3-STATE] signals → autonomic={autonomic_ratio}, ATL={atl}, CTL={ctl}"
    )

    load_recovery_state = "balanced"
    if autonomic_ratio is not None and atl is not None and ctl is not None:

        load_pressure = atl - ctl

        if load_pressure <= 0:
            load_recovery_state = "balanced"

        elif autonomic_ratio < 0.90 and load_pressure > 10:
            load_recovery_state = "maladaptation_risk"

        elif autonomic_ratio < 0.95 and load_pressure > 5:
            load_recovery_state = "adaptation_pressure"

        elif autonomic_ratio >= 1.05 and load_pressure > 5:
            load_recovery_state = "productive_load"


    # --------------------------------------------------
    # Decision Framing (no new math — just logic)
    # --------------------------------------------------

    # --- readiness / fatigue interpretation ---

    if tsb_class == "overreached" or (recovery_index and recovery_index < 0.8):
        readiness = "You are carrying significant fatigue."
        state_label = "Overreached"
        recommendation = "Back off"
        next_session = "Recovery ride or full rest"

    elif tsb_class in ("fresh", "transition"):
        readiness = "You are fresh and well recovered."
        state_label = "Fresh"
        recommendation = "Push"
        next_session = "High-quality intensity session"

    elif tsb_class == "productive_fatigue":
        readiness = "You are training under productive fatigue."
        state_label = "Productive Load"
        recommendation = "Maintain progression"
        next_session = "Structured endurance or threshold session"

    else:  # neutral
        readiness = "Training load and recovery appear balanced."
        state_label = "Stable"
        recommendation = "Maintain training structure"
        next_session = "Planned structured session"

    # --- Am I adapting? ---
    adapting = "Adaptation signals are stable."

    if wdrm and wdrm > 0.6:
        adapting = "High anaerobic stimulus — adaptation likely but recovery critical."
    if durability is not None and abs(durability) > 6:
        adapting = "Durability strain rising — aerobic consolidation advised."

    # --- Neural density check ---
    if neural and neural > 200000:
        next_session = "Low-intensity aerobic session to absorb load"
        recommendation = "Absorb before adding intensity"


    # --------------------------------------------------
    # Load vs Recovery override (autonomic + load model)
    # --------------------------------------------------

    if load_recovery_state == "maladaptation_risk":
        state_label = "Maladaptation Risk"
        readiness = "Autonomic recovery suppressed relative to training load."
        recommendation = "Reduce load and prioritise recovery"
        next_session = "Recovery ride or full rest"

    elif load_recovery_state == "adaptation_pressure":
        state_label = "Adaptation Pressure"
        readiness = "Training load elevated — monitor recovery carefully."

    elif load_recovery_state == "productive_load":
        state_label = "Productive Load"
        readiness = "Load and recovery interaction suggests productive stimulus."

    # --------------------------------------------------
    # Confidence
    # --------------------------------------------------

    confidence = "moderate"

    if tsb_class and recovery_index:
        confidence = "high"

    return {
        "state_label": state_label,
        "readiness": readiness,
        "adaptation": adapting,
        "recommendation": recommendation,
        "next_session": next_session,
        "confidence": confidence,
        "phase_context": phase,
        "load_recovery_state": load_recovery_state,
    }


# ===========================================================
# Utilities
# ===========================================================

def _safe_sum(series):
    if series is None:
        return None
    return float(series.fillna(0).sum())


def _safe_mean(series):
    if series is None or series.dropna().empty:
        return None
    return float(series.mean())


def _safe_max(series):
    if series is None or series.dropna().empty:
        return None
    return float(series.max())


def _safe_count(series, threshold):
    if series is None:
        return None
    return int((series >= threshold).sum())


def _empty_weekly():
    return {
        "anaerobic_repeatability": {},
        "model_diagnostics": {},
        "durability": {},
        "neural_density": {}
    }


def _empty_season():
    return {
        "chronic_state": None,
        "acute_overlay": None
    }
