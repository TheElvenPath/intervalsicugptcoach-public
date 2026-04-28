# tier3_trail_execution.py

"""
Tier-3 — Trail Execution Intelligence

Purpose:
- Evaluate how terrain affects execution quality
- Convert rule-based signals into a compact Tier-3 signal
- Inject into performance_intelligence (URF v5.1 compliant)
- This is NOT included at this time, NDLI etc provides nbetter coverage and TEM really needs to be based on single activity with interval dat to get better insight
- Approach therefore is to create new endpoint report specific to get onedayactivity with intervals in full - pass to this function and analyse and report a TEM analysis

Output (minimal, compliant):
    performance_intelligence["run_terrain_execution"] = {
        "efficiency_state": "...",
        "limiter": "...",
        "confidence": "..."
    }
"""

from coach_trail_rules import (
    TRAIL_EXECUTION_RULES,
    TRAIL_FLAGS,
    TRAIL_DEFAULTS,
    TRAIL_INTERPRETATION
)


def _has_meaningful_trail_runs(df):

    if "type" not in df.columns:
        return False

    runs = df[df["type"].str.contains("Run", na=False)]

    if runs.empty:
        return False

    # --- minimum volume (30 min total) ---
    if "moving_time" in runs.columns:
        if runs["moving_time"].sum() < 1800:
            return False

    # --- terrain relevance (derive grade properly) ---
    if "total_elevation_gain" in runs.columns and "distance" in runs.columns:

        gain = runs["total_elevation_gain"].sum()
        dist = runs["distance"].sum()

        if dist and dist > 0:
            grade = (gain / dist) * 100

            if grade < 3:
                return False

    return True

# --------------------------------------------------
# CONDITION MATCHER
# --------------------------------------------------

def match_conditions(conditions: dict, metrics: dict) -> bool:

    for key, value in conditions.items():

        if key.endswith("_min"):
            m = key.replace("_min", "")
            if metrics.get(m, 0) < value:
                return False

        elif key.endswith("_max"):
            m = key.replace("_max", "")
            if metrics.get(m, 0) > value:
                return False

        else:
            if metrics.get(key) != value:
                return False

    return True


# --------------------------------------------------
# RULE EVALUATION
# --------------------------------------------------

def evaluate_rules(metrics: dict):

    results = {}
    priorities = {}
    flags = []

    # --- execution rules ---
    for rule in TRAIL_EXECUTION_RULES:

        if match_conditions(rule["conditions"], metrics):

            rtype = rule["type"]
            priority = rule.get("priority", 99)

            if rtype not in priorities or priority < priorities[rtype]:
                results[rtype] = rule["result"]
                priorities[rtype] = priority

    # --- flags ---
    for rule in TRAIL_FLAGS:
        if match_conditions(rule["conditions"], metrics):
            flags.append(rule["flag"])

    return results, flags


# --------------------------------------------------
# CLASSIFIER (compression layer)
# --------------------------------------------------

def classify_execution(signals: dict, flags: list):

    efficiency = signals.get("efficiency", TRAIL_DEFAULTS["efficiency"])
    durability = signals.get("durability", TRAIL_DEFAULTS["durability"])
    environment = signals.get("environment", TRAIL_DEFAULTS["environment"])

    # --- limiter ---
    if environment != "none":
        limiter = "heat" if environment == "heat" else "environment"
    elif efficiency in ["overexerting", "pace_collapse"]:
        limiter = "terrain"
    elif durability == "drifting":
        limiter = "fatigue"
    else:
        limiter = "none"

    # --- efficiency state ---
    if "direct_climb_penalty" in flags:
        state = "inefficient"
    elif efficiency in ["overexerting", "pace_collapse"]:
        state = "inefficient"
    elif durability == "drifting":
        state = "moderate"
    elif efficiency == "efficient":
        state = "efficient"
    else:
        state = "moderate"

    # --- confidence ---
    confidence = "high" if len(flags) > 0 else "moderate"

    return {
        "efficiency_state": state,
        "limiter": limiter,
        "confidence": confidence
    }


def build_interpretation(signals: dict, flags: list, classification: dict):

    eff = signals.get("efficiency")
    dur = signals.get("durability")
    env = signals.get("environment")

    state = classification.get("efficiency_state")

    interpretation = None
    coaching = None

    # --------------------------------------------------
    # PRIORITY 1 → FLAGS (most specific)
    # --------------------------------------------------

    for f in flags:
        block = TRAIL_INTERPRETATION.get("flags", {}).get(f)
        if block:
            return block["interpretation"], block["coaching"]

    # --------------------------------------------------
    # PRIORITY 2 → EFFICIENCY
    # --------------------------------------------------

    block = TRAIL_INTERPRETATION.get("efficiency", {}).get(eff)
    if block:
        interpretation = block["interpretation"]
        coaching = block["coaching"]

    # --------------------------------------------------
    # PRIORITY 3 → DURABILITY override
    # --------------------------------------------------

    if dur == "drifting":
        block = TRAIL_INTERPRETATION.get("durability", {}).get("drifting")
        if block:
            interpretation = block["interpretation"]
            coaching = block["coaching"]

    # --------------------------------------------------
    # PRIORITY 4 → ENVIRONMENT override
    # --------------------------------------------------

    if env != "none":
        block = TRAIL_INTERPRETATION.get("environment", {}).get(env)
        if block:
            interpretation = block["interpretation"]
            coaching = block["coaching"]

    # --------------------------------------------------
    # FALLBACK (state-based)
    # --------------------------------------------------

    if not interpretation:
        block = TRAIL_INTERPRETATION.get("efficiency", {}).get(state)
        if block:
            interpretation = block["interpretation"]
            coaching = block["coaching"]

    return interpretation, coaching

# --------------------------------------------------
# MAIN ENTRY
# --------------------------------------------------

def run_trail_execution(context: dict):

    df = context.get("_df_scope_full")

    if df is None or df.empty:
        return

    # --- RUN + TERRAIN GATE ---
    if not _has_meaningful_trail_runs(df):
        return

    # --------------------------------------------------
    # METRIC EXTRACTION (aligned to Intervals data)
    # --------------------------------------------------

    metrics = {}

    # -----------------------------
    # GRADE (% from elevation)
    # -----------------------------
    if "total_elevation_gain" in df.columns and "distance" in df.columns:
        gain = df["total_elevation_gain"].sum()
        dist = df["distance"].sum()

        if dist and dist > 0:
            metrics["grade"] = (gain / dist) * 100


    # -----------------------------
    # CADENCE
    # -----------------------------
    if "average_cadence" in df.columns:
        metrics["cadence"] = float(df["average_cadence"].mean())
        metrics["cadence_var"] = float(df["average_cadence"].std())


    # -----------------------------
    # HR ratio (vs LTHR)
    # -----------------------------
    if "average_heartrate" in df.columns:
        hr = float(df["average_heartrate"].mean())
        lthr = context.get("athlete", {}).get("lthr", 160)

        if lthr:
            metrics["hr_ratio"] = hr / lthr


    # -----------------------------
    # DECOUPLING
    # -----------------------------
    if "decoupling" in df.columns:
        metrics["decoupling"] = float(df["decoupling"].mean())


    # -----------------------------
    # SPEED DROP (proxy)
    # -----------------------------
    if "average_speed" in df.columns and "max_speed" in df.columns:
        avg = df["average_speed"].mean()
        maxs = df["max_speed"].max()

        if maxs and maxs > 0:
            metrics["speed_drop"] = (maxs - avg) / maxs


    # -----------------------------
    # TEMPERATURE
    # -----------------------------
    if "average_weather_temp" in df.columns:
        metrics["temp"] = float(df["average_weather_temp"].mean())

    # --------------------------------------------------
    # APPLY RULES
    # --------------------------------------------------

    signals, flags = evaluate_rules(metrics)

    # apply defaults
    for k, v in TRAIL_DEFAULTS.items():
        signals.setdefault(k, v)

    # --------------------------------------------------
    # CLASSIFY
    # --------------------------------------------------

    classification = classify_execution(signals, flags)

    interpretation, coaching = build_interpretation(
        signals,
        flags,
        classification
    )

    terrain_execution = {
        **classification,
        "interpretation": interpretation,
        "coaching_implication": coaching,
        "flags": flags   # keep for downstream use/debug
    }

    # --------------------------------------------------
    # INJECT INTO TIER-3
    # --------------------------------------------------

    pi = context.get("performance_intelligence", {})

    pi["run_terrain_execution"] = terrain_execution

    context["performance_intelligence"] = pi

    return