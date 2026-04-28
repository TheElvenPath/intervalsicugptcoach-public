#ADE V2.1

ADE_VERSION = "ade_v2.1"

from datetime import datetime
from audit_core.utils import debug

def _extract_target_event(ev):
    name = (ev.get("name") or "").lower()
    category = str(ev.get("category") or "").upper()

    if category == "RACE_A":
        priority = "A"
    elif category == "RACE_B":
        priority = "B"
    elif category == "RACE_C":
        priority = "C"
    else:
        return None

    if "climb" in name:
        training_bias = "durability"
    elif "tt" in name or "threshold" in name:
        training_bias = "ftp"
    elif "vo2" in name:
        training_bias = "anaerobic"
    elif "sprint" in name:
        training_bias = "neuromuscular"
    else:
        training_bias = "mixed"

    date_raw = ev.get("start_date_local") or ev.get("date")

    if not date_raw:
        return None

    try:
        dt = datetime.fromisoformat(str(date_raw)[:10])
    except:
        return None

    return {
        "priority": priority,
        "training_bias": training_bias,
        "dt": dt
    }

def run_adaptive_decision_engine(context):

    training_state = context.get("training_state", {}) or {}
    forecast = context.get("future_forecast", {}) or {}
    espe = context.get("energy_system_progression", {}) or {}

    directive = training_state.get("recommendation")
    operational_state = training_state.get("operational_state")
    
    fatigue_class = forecast.get("fatigue_class")
    load_trend = forecast.get("load_trend")

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
    # 🎯 TARGET EVENT CONTEXT (calendar ONLY)
    # --------------------------------------------------

    today_raw = context.get("athlete_today")

    if isinstance(today_raw, str):
        today = datetime.fromisoformat(today_raw).date()
    elif hasattr(today_raw, "date"):
        today = today_raw.date()
    else:
        today = today_raw

    events = context.get("calendar") or []

    next_a = None

    if today and events:

        candidates = []

        for ev in events:

            t = _extract_target_event(ev)

            if not t:
                continue

            if t["priority"] != "A":
                continue

            if t["dt"].date() < today:
                continue

            candidates.append(t)

        if candidates:
            next_a = sorted(candidates, key=lambda x: x["dt"])[0]

    days_to_event = None
    taper_state = "none"
    training_bias = "mixed"

    if next_a:
        days_to_event = (next_a["dt"].date() - today).days if today else None

        p = next_a.get("priority") if next_a else None

        if days_to_event is not None and p:

            if p == "A":
                if days_to_event <= 10:
                    taper_state = "taper"
                elif days_to_event <= 21:
                    taper_state = "pre_taper"

            elif p == "B":
                if days_to_event <= 5:
                    taper_state = "taper"
                elif days_to_event <= 10:
                    taper_state = "pre_taper"

            else:
                taper_state = "none"

        # ✅ DIRECT — no mapping
        training_bias = next_a.get("training_bias", "mixed")

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
        "target_event": {
            "exists": bool(next_a),
            "days_to_event": days_to_event,
            "taper_state": taper_state,
            "event_demand": training_bias
        },
        "version": ADE_VERSION
    }

    context["adaptive_decision"] = decision

    return {"adaptive_decision": decision}