"""
Energy System Progression Engine (ESPE)
Version: v1

Stateless physiological engine comparing two rolling power-curve windows.

Consumes:
    power_curve block injected by Worker

Produces:
    energy_system_progression section
"""

from typing import Dict, Any

from coaching_cheat_sheet import CHEAT_SHEET
from audit_core.utils import debug
from coaching_profile import COACH_PROFILE

ESPE_VERSION = "espe_v1"


# ---------------------------------------------------------------------
# Entry Point
# ---------------------------------------------------------------------

def run_espe(power_curve_block: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:

    result = {
        "version": ESPE_VERSION,
        "sports": {}
    }

    if not power_curve_block:
        debug(context, "[ESPE] no power_curve block provided")
        return _unsupported("missing power curve data")

    for sport, data in power_curve_block.items():

        debug(context, f"[ESPE] processing sport={sport}")

        if not _valid_curve_block(data, context, sport):
            result["sports"][sport] = _unsupported("invalid or insufficient data")
            continue

        result["sports"][sport] = _process_sport(sport, data, context)

    return result


# ---------------------------------------------------------------------
# Core Logic
# ---------------------------------------------------------------------
def _process_sport(sport: str, data: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:

    current = data["current"]
    previous = data["previous"]

    delta = _compute_delta_percent(current, previous, context)

    glycolytic_bias = _safe_ratio(current.get("1m"), current.get("20m"))
    aerobic_durability = _safe_ratio(current.get("60m"), current.get("5m"))

    # durability gradient (long-duration sustainability)
    durability_gradient = _safe_ratio(current.get("60m"), current.get("20m"))

    system_status = _classify_system_status(sport, delta)
    system_timeline = _build_system_timeline(system_status)

    plateau = _detect_plateau(sport, delta, context)

    balance_score = _compute_balance_score(glycolytic_bias, aerobic_durability)

    # regression diagnostics
    regression = data.get("curve_regression", {})
    curve_slope = regression.get("slope") or data.get("curve_slope")
    curve_r2 = regression.get("r2") or data.get("curve_fit_r2")

    if curve_r2 is not None:
        curve_r2 = float(curve_r2)

    curve_quality = _classify_curve_quality(curve_r2)
    model_quality = curve_quality

    # FFT_CURVES model
    models = data.get("models", {})
    cp = models.get("cp")
    w_prime = models.get("w_prime")
    pmax = models.get("pmax")
    ftp = models.get("ftp")

    # ---- ESPE v1 derived power metrics ----
    p5m = current.get("5m")

    pdr_5m = None
    vo2_reserve_ratio = None

    if cp is not None and p5m is not None and cp != 0:
        pdr_5m = round(p5m - cp, 2)
        vo2_reserve_ratio = round(p5m / cp, 3)

    curve_profile = (
        _classify_curve_profile(sport, curve_slope)
        if curve_slope is not None
        else "unknown"
    )

    adaptation_bias = _derive_adaptation_bias(system_status)
    adaptation_state = classify_adaptation_state(system_status, delta)

    curve_dynamics = _compute_curve_dynamics(delta)
    # ---- curve window definition ----
    window = data.get(
        "window_days",
        CHEAT_SHEET["thresholds"]["ESPE"]["curve_windows"]["default_days"]
    )

    curve_window = {
        "current_days": window,
        "previous_days": window,
        "comparison": f"{window}d_vs_{window}d",
        "anchor": "report_end",
        "curve_source": "FFT_CURVES"
    }

    # ---- derived metrics block ----
    markers = COACH_PROFILE.get("markers", {})
    window_label = curve_window["comparison"]

    derived_metrics = {}

    def _metric(name, value):
        meta = markers.get(name, {})
        return {
            "name": name,
            "value": value,
            "framework": meta.get("framework"),
            "interpretation": meta.get("interpretation"),
            "coaching_implication": meta.get("coaching_implication"),
            "related_metrics": {},
            "context_window": window_label,
        }

    if glycolytic_bias is not None:
        derived_metrics["glycolytic_bias_ratio"] = _metric(
            "glycolytic_bias_ratio", round(glycolytic_bias, 3)
        )

    if aerobic_durability is not None:
        derived_metrics["aerobic_durability_ratio"] = _metric(
            "aerobic_durability_ratio", round(aerobic_durability, 3)
        )

    if durability_gradient is not None:
        derived_metrics["durability_gradient"] = _metric(
            "durability_gradient", round(durability_gradient, 3)
        )

    if balance_score is not None:
        derived_metrics["system_balance_score"] = _metric(
            "system_balance_score", round(balance_score, 3)
        )

    if pdr_5m is not None:
        derived_metrics["pdr_5m"] = _metric("pdr_5m", pdr_5m)

    if vo2_reserve_ratio is not None:
        derived_metrics["vo2_reserve_ratio"] = _metric(
            "vo2_reserve_ratio", vo2_reserve_ratio
        )

    debug(
        context,
        f"[ESPE] {sport} bias={adaptation_bias} balance={balance_score}"
    )

    return {
        "supported": True,

        "curve_window": curve_window,

        "delta_percent": delta,

        "curve_dynamics": curve_dynamics,

        "system_status": system_status,
        "system_status_timeline": system_timeline,

        "derived_metrics": derived_metrics,

        "curve_regression": {
            "model": "power_duration_log_regression",
            "slope": curve_slope,
            "r2": curve_r2
        },

        "curve_quality": curve_quality,

        "power_model": {
            "source": "FFT_CURVES",
            "model_quality": model_quality,
            "cp": cp,
            "w_prime": w_prime,
            "pmax": pmax,
            "ftp": ftp
        },

        "plateau_detected": plateau,

        "adaptation_bias": adaptation_bias,
        "adaptation_state": adaptation_state,

        "curve_profile": curve_profile
    }

def _compute_curve_dynamics(delta: Dict[str, float]) -> Dict[str, Any]:

    short = delta.get("1m", 0)
    vo2 = delta.get("5m", 0)
    thr = delta.get("20m", 0)
    long = delta.get("60m", 0)

    # average shift of entire curve
    vertical_shift = round((short + vo2 + thr + long) / 4, 2)

    # rotation strength (difference between short vs long systems)
    rotation_index = round(((short + vo2) / 2) - ((thr + long) / 2), 2)

    # classification
    if abs(rotation_index) < 0.75:
        dominant = "uniform_shift"
    elif rotation_index > 0:
        dominant = "anaerobic_rotation"
    else:
        dominant = "aerobic_rotation"

    return {
        "vertical_shift_pct": vertical_shift,
        "rotation_index": rotation_index,
        "dominant_shift": dominant
    }


# ---------------------------------------------------------------------
# Calculations
# ---------------------------------------------------------------------

def _compute_delta_percent(
    current: Dict[str, float],
    previous: Dict[str, float],
    context: Dict[str, Any]
) -> Dict[str, float]:

    delta = {}

    for k in current:
        if k in previous and previous[k] > 0:

            d = round(
                ((current[k] - previous[k]) / previous[k]) * 100,
                2
            )

            delta[k] = d
            debug(context, f"[ESPE] delta {k} = {d}%")

    return delta


def _safe_ratio(a: float, b: float) -> float:

    if not a or not b or b == 0:
        return 0.0

    return round(a / b, 2)


# ---------------------------------------------------------------------
# Classification
# ---------------------------------------------------------------------

def _classify_system_status(
    sport: str,
    delta: Dict[str, float]
) -> Dict[str, str]:

    thresholds = _sport_thresholds(sport)

    return {
        "anaerobic": _band(delta.get("1m", 0), thresholds["anaerobic"]),
        "vo2": _band(delta.get("5m", 0), thresholds["vo2"]),
        "threshold": _band(delta.get("20m", 0), thresholds["threshold"]),
        "aerobic_durability": _band(delta.get("60m", 0), thresholds["aerobic"])
    }


def _band(value: float, bands: Dict[str, float]) -> str:

    neutral_band = (
        CHEAT_SHEET
        .get("thresholds", {})
        .get("ESPE", {})
        .get("neutral_band", 0.75)
    )

    if abs(value) < neutral_band:
        return "stable"

    if value >= bands["strong"]:
        return "strong_gain"

    if value >= bands["moderate"]:
        return "moderate_gain"

    if value >= bands["mild"]:
        return "mild_gain"

    if value <= bands["decline"]:
        return "decline"

    return "stable"


def _sport_thresholds(sport: str) -> Dict[str, Dict[str, float]]:

    espe = (
        CHEAT_SHEET
        .get("thresholds", {})
        .get("ESPE", {})
    )

    if sport in espe:
        return espe[sport]

    return espe.get("Ride", {})


# ---------------------------------------------------------------------
# Derived Metrics
# ---------------------------------------------------------------------

def _detect_plateau(
    sport: str,
    delta: Dict[str, float],
    context: Dict[str, Any]
) -> bool:

    threshold_gain = delta.get("20m", 0)

    debug(context, f"[ESPE] plateau check {sport} threshold_delta={threshold_gain}")

    if sport == "Run":
        return threshold_gain < 0.5

    return threshold_gain < 1.0


def _compute_balance_score(
    glycolytic: float,
    aerobic: float
) -> float:

    ideal = 1.8

    if glycolytic == 0:
        return 0.0

    deviation = abs(glycolytic - ideal) / ideal
    score = max(0.0, 1 - deviation)

    return round(score, 2)


def _derive_adaptation_bias(system_status: Dict[str, str]) -> str:

    if system_status["vo2"] in ("strong_gain", "moderate_gain"):
        return "vo2_dominant"

    if system_status["threshold"] in ("strong_gain", "moderate_gain"):
        return "threshold_dominant"

    return "balanced"

def _classify_curve_profile(sport: str, slope: float) -> str:

    if slope is None:
        return "unknown"

    espe = (
        CHEAT_SHEET
        .get("thresholds", {})
        .get("ESPE", {})
    )

    # -----------------------------
    # Running classification
    # -----------------------------
    if sport == "Run":

        if slope >= espe["run_curve_slope_endurance_runner"]:
            return "endurance_runner"

        if slope >= espe["run_curve_slope_balanced_runner"]:
            return "balanced_runner"

        if slope >= espe["run_curve_slope_punchy_runner"]:
            return "punchy_runner"

        return "speed_runner"

    # -----------------------------
    # Cycling classification
    # -----------------------------

    if slope >= espe["curve_slope_time_trialist"]:
        return "time_trialist"

    if slope >= espe["curve_slope_endurance_specialist"]:
        return "endurance_specialist"

    if slope >= espe["curve_slope_all_rounder"]:
        return "all_rounder"

    if slope >= espe["curve_slope_punchy_climber"]:
        return "punchy_climber"

    if slope >= espe["curve_slope_punchy"]:
        return "punchy"

    if slope >= espe["curve_slope_anaerobic_specialist"]:
        return "anaerobic_specialist"

    return "sprinter"

def classify_adaptation_state(system_status, deltas):

    thr = deltas.get("20m", 0)
    dur = deltas.get("60m", 0)
    vo2 = deltas.get("5m", 0)
    neu = deltas.get("5s", 0)

    # aerobic development
    if thr > 1 and dur > 2:
        return "aerobic_consolidation"

    # vo2 expansion
    if vo2 > 3:
        return "vo2_expansion"

    # anaerobic build
    if neu > 5:
        return "anaerobic_build"

    # plateau
    if all(abs(v) < 1 for v in deltas.values()):
        return "plateau"

    # systemic decline
    if thr < -3 and vo2 < -3:
        return "fatigue_state"

    return "mixed_adaptation"

def _classify_curve_quality(r2: float):

    espe = (
        CHEAT_SHEET
        .get("thresholds", {})
        .get("ESPE", {})
    )

    q = espe.get("curve_quality", {})

    if r2 is None:
        return "unknown"

    if r2 >= q.get("excellent", 0.85):
        return "excellent"

    if r2 >= q.get("good", 0.75):
        return "good"

    return "low_confidence"

def _build_system_timeline(system_status: Dict[str, str]):

    mapping = (
        CHEAT_SHEET
        .get("thresholds", {})
        .get("ESPE", {})
        .get("system_timeline_map", {})
    )

    timeline = {}

    for system, state in system_status.items():
        timeline[system] = mapping.get(state, "unknown")

    return timeline

# ---------------------------------------------------------------------
# Validation
# ---------------------------------------------------------------------

def _valid_curve_block(
    data: Dict[str, Any],
    context: Dict[str, Any],
    sport: str
) -> bool:

    if "current" not in data or "previous" not in data:
        debug(context, f"[ESPE] missing curve block for {sport}")
        return False

    required = ["1m", "5m", "20m", "60m"]

    current = data.get("current", {})
    previous = data.get("previous", {})

    for k in required:
        if current.get(k, 0) <= 0 or previous.get(k, 0) <= 0:
            debug(context, f"[ESPE] missing anchor {k} for {sport}")
            return False

    return True


# ---------------------------------------------------------------------
# Unsupported
# ---------------------------------------------------------------------

def _unsupported(reason: str) -> Dict[str, Any]:

    return {
        "supported": False,
        "reason": reason
    }