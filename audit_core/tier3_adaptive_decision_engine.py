#ADE V1.0

ADE_VERSION = "ade_v1"


def run_adaptive_decision_engine(context):

    training_state = context.get("training_state", {}) or {}
    forecast = context.get("future_forecast", {}) or {}
    espe = context.get("energy_system_progression", {}) or {}

    directive = training_state.get("recommendation")
    operational_state = training_state.get("operational_state")

    fatigue_class = forecast.get("fatigue_class")
    load_trend = forecast.get("load_trend")

    nutrition = context.get("nutrition_balance", {}) or {}
    nutrition_status = nutrition.get("status")

    system_state = None
    sports = espe.get("sports") or {}

    for sport, block in sports.items():
        if block.get("supported"):
            system_state = block.get("adaptation_state")
            break

    risk_flag = "normal"

    if fatigue_class == "red":
        risk_flag = "high"

    elif fatigue_class == "amber":
        risk_flag = "moderate"

    nutrition = context.get("nutrition_balance", {}) or {}
    nutrition_status = nutrition.get("status")
    nutrition_conf = nutrition.get("confidence")

    # --------------------------------------------------
    # Nutrition = supplementary signal only (graded)
    # --------------------------------------------------

    nutrition_note = None

    if nutrition_conf in ("moderate", "high"):

        if nutrition_status == "severely_underfuelled":
            nutrition_note = "Carbohydrate intake is far below demand for current load; fuelling gap likely limiting adaptation."

        elif nutrition_status == "underfuelled":
            nutrition_note = "Carbohydrate intake is below demand; consider increasing fuelling to match training load."

        elif nutrition_status == "overfuelled":
            nutrition_note = "Energy intake exceeds current demand; monitor balance relative to load."

        elif nutrition_status == "balanced":
            nutrition_note = "Energy intake aligns with current training demand."

    # DO NOT change:
    # - directive
    # - operational_state
    # - risk_flag

    decision = {
        "directive": directive,
        "operational_state": operational_state,
        "adaptation_focus": system_state,
        "risk_flag": risk_flag,
        "forecast_context": fatigue_class,
        "load_trend": load_trend,
        "nutrition_status": nutrition_status,
        "nutrition_confidence": nutrition_conf,
        "nutrition_note": nutrition_note,
        "version": ADE_VERSION
    }

    context["adaptive_decision"] = decision

    return {"adaptive_decision": decision}