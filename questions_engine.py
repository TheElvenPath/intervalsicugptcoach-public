# questions_engine.py

"""
Montis Coaching Question Engine
"""

from question_bank import QUESTION_BANK, SIGNAL_MAP

def select_question(report, signals):

    sig = dominant_signal(signals)

    if sig is None:
        category = "progression"
    else:
        category = SIGNAL_MAP.get(sig, "progression")

    questions = QUESTION_BANK.get(category)

    if not questions:
        return None

    period = report.get("meta", {}).get("period", "default")

    idx = hash(str(period)) % len(questions)

    return questions[idx]



# Signal detection
def detect_signals(report):

    signals = []

    pi = report.get("performance_intelligence", {})
    espe = report.get("energy_system_progression", {})
    metrics = report.get("metrics", {})

    # Durability
    dec = pi.get("durability", {}).get("mean_decoupling_7d")

    if dec is not None:
        if dec > 8:
            signals.append(("durability_decline", 3))
        elif dec > 5:
            signals.append(("durability_pressure", 2))

    # Anaerobic repeatability
    dep = pi.get("anaerobic_repeatability", {}).get("mean_depletion_pct_7d")

    if dep is not None:
        if dep > 0.60:
            signals.append(("anaerobic_depletion", 3))
        elif dep > 0.40:
            signals.append(("anaerobic_load", 2))

    # Neural density
    hi_days = pi.get("neural_density", {}).get("high_intensity_days_7d")

    if hi_days is not None:
        if hi_days >= 4:
            signals.append(("intensity_clustering", 3))
        elif hi_days == 3:
            signals.append(("high_intensity_density", 2))

    # Load / fatigue
    fatigue = metrics.get("FatigueTrend")
    stress = metrics.get("StressTolerance")

    # Extract numeric values if metrics are objects
    if isinstance(fatigue, dict):
        fatigue = fatigue.get("value")

    if isinstance(stress, dict):
        stress = stress.get("value")

    if fatigue is not None and fatigue > 10:
        signals.append(("fatigue_accumulation", 3))

    if stress is not None and stress > 1.3:
        signals.append(("load_pressure", 2))

    # ESPE adaptation signals
    systems = espe.get("systems", {})

    for system in systems.values():

        state = system.get("adaptation_state")

        if state == "decline":
            signals.append(("system_decline", 3))

        if state == "strong_gain":
            signals.append(("system_progression", 2))

    return signals


# Dominant Signals

def dominant_signal(signals):

    if not signals:
        return None

    signals_sorted = sorted(signals, key=lambda x: x[1], reverse=True)

    return signals_sorted[0][0]