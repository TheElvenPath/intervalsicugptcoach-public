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

    # ✅ Now interpret using actual data
    interpretation = interpret_training_state(context)
    context["training_state"] = interpretation

    return result


# ===========================================================
# WEEKLY (7-DAY FULL – DO NOT COMPROMISE)
# ===========================================================

def _compute_weekly(context, df_full):

    if df_full is None or df_full.empty:
        debug(context, "[T3] Weekly: No FULL data")
        return _empty_weekly()

    debug(context, f"[T3] Weekly FULL rows: {len(df_full)}")

    w_prime = pd.to_numeric(df_full.get("icu_pm_w_prime"), errors="coerce")
    depletion = pd.to_numeric(df_full.get("icu_max_wbal_depletion"), errors="coerce")
    joules = pd.to_numeric(df_full.get("icu_joules_above_ftp"), errors="coerce")
    decoupling = pd.to_numeric(df_full.get("decoupling"), errors="coerce")
    if_values = pd.to_numeric(df_full.get("IF"), errors="coerce")
    moving_time = pd.to_numeric(df_full.get("moving_time"), errors="coerce")

    depletion_pct = None
    if w_prime is not None and depletion is not None:
        depletion_pct = (depletion / w_prime.replace(0, pd.NA)).clip(upper=1.5)

    weekly_result = {
        "anaerobic_repeatability": {
            "max_depletion_pct_7d": _safe_max(depletion_pct),
            "mean_depletion_pct_7d": _safe_mean(depletion_pct),
            "high_depletion_sessions_7d": _safe_count(depletion_pct, 0.7),
            "total_joules_above_ftp_7d": _safe_sum(joules),
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

    w_prime = pd.to_numeric(df_light.get("icu_pm_w_prime"), errors="coerce")
    depletion = pd.to_numeric(df_light.get("icu_max_wbal_depletion"), errors="coerce")
    joules = pd.to_numeric(df_light.get("icu_joules_above_ftp"), errors="coerce")
    decoupling = pd.to_numeric(df_light.get("decoupling"), errors="coerce")
    if_values = pd.to_numeric(df_light.get("IF"), errors="coerce")
    training_load = pd.to_numeric(df_light.get("icu_training_load"), errors="coerce")

    depletion_pct = None
    if w_prime is not None and depletion is not None:
        depletion_pct = (depletion / w_prime.replace(0, pd.NA)).clip(upper=1.5)

    chronic = {
        "anaerobic_repeatability": {
            "mean_depletion_pct_90d": _safe_mean(depletion_pct),
            "max_depletion_pct_90d": _safe_max(depletion_pct),
            "high_depletion_sessions_90d": _safe_count(depletion_pct, 0.7),
            "total_joules_above_ftp_90d": _safe_sum(joules),
        },
        "durability": {
            "mean_decoupling_90d": _safe_mean(decoupling),
            "max_decoupling_90d": _safe_max(decoupling),
            "high_drift_sessions_90d": _safe_count(decoupling, 5.0),
        },
        "neural_density": {
            "high_intensity_sessions_90d": _safe_count(joules, 20000),
            "mean_if_90d": _safe_mean(if_values),
            "mean_training_load_90d": _safe_mean(training_load),
        }
    }

    # -------- Acute Overlay (full fidelity weekly) --------

    acute_overlay = None
    if df_full is not None and not df_full.empty:
        debug(context, "[T3] Season computing acute overlay (7d FULL)")
        acute_overlay = _compute_weekly(context, df_full)

    # -----------------------------------------------------------
    # T3 CONTRACT DEBUG — SEASON (CHRONIC 90D)
    # -----------------------------------------------------------

    wdrm_c = chronic["anaerobic_repeatability"]
    isdm_c = chronic["durability"]
    ndli_c = chronic["neural_density"]

    debug(context, "[T3][SEASON][WDRM] Chronic Anaerobic Repeatability (90d)",
        f"mean_dep_pct={wdrm_c['mean_depletion_pct_90d']}",
        f"max_dep_pct={wdrm_c['max_depletion_pct_90d']}",
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

        if acute_mean_dep and chronic_mean_dep and chronic_mean_dep != 0:
            dep_ratio = acute_mean_dep / chronic_mean_dep

        if acute_mean_dec and chronic_mean_dec and chronic_mean_dec != 0:
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
    """
    Synthesizes Tier-3 metrics into athlete-facing decisions.

    Returns:
        {
            state_label,
            readiness,
            adaptation,
            recommendation,
            next_session,
            confidence
        }
    """

    pi = context.get("performance_intelligence", {})
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
    # Decision Framing (no new math — just logic)
    # --------------------------------------------------

    # --- Am I cooked? ---
    if tsb_class == "high_risk" or (recovery_index and recovery_index < 0.8):
        readiness = "You are carrying significant fatigue."
        state_label = "Overreached"
        recommendation = "Back off"
        next_session = "Recovery ride or full rest"
    elif tsb_class in ("fresh", "transition"):
        readiness = "You are fresh and well recovered."
        state_label = "Fresh"
        recommendation = "Push"
        next_session = "High-quality intensity session"
    else:
        readiness = "You are in a productive training zone."
        state_label = "Productive"
        recommendation = "Maintain progression"
        next_session = "Planned structured session"

    # --- Am I adapting? ---
    adapting = "Adaptation signals are stable."

    if wdrm and wdrm > 0.6:
        adapting = "High anaerobic stimulus — adaptation likely but recovery critical."
    if durability and durability > 6:
        adapting = "Durability strain rising — aerobic consolidation advised."

    # --- Neural density check ---
    if neural and neural > 200000:
        next_session = "Low-intensity aerobic session to absorb load"
        recommendation = "Absorb before adding intensity"

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
    return int((series > threshold).sum())


def _empty_weekly():
    return {
        "anaerobic_repeatability": None,
        "durability": None,
        "neural_density": None
    }


def _empty_season():
    return {
        "chronic_state": None,
        "acute_overlay": None
    }
