# questions_engine.py

"""
Montis Coaching Question Engine
"""

from question_bank import QUESTION_BANK, SIGNAL_MAP

def select_question(report, signals):

    if not signals:
        return None

    # Sort signals by severity
    signals_sorted = sorted(signals, key=lambda x: x[1], reverse=True)

    primary_sig, severity = signals_sorted[0]

    secondary_sig = None
    if len(signals_sorted) > 1:
        secondary_sig = signals_sorted[1][0]

    # Map primary signal → category
    category = SIGNAL_MAP.get(primary_sig)

    if not category:
        return None

    questions = QUESTION_BANK.get(category)

    if not questions:
        return None

    # Filter questions aligned with primary signal
    aligned = [q for q in questions if primary_sig in q["signals"]]

    if not aligned:
        return None

    # Sort by priority
    aligned = sorted(aligned, key=lambda q: q["priority"])

    idx = min(severity - 1, len(aligned) - 1)

    question = aligned[idx]["question"]

    # Blend secondary signal context if useful
    if secondary_sig and secondary_sig in SIGNAL_LABELS:

        label = SIGNAL_LABELS[secondary_sig]

        if "given the current" not in question:
            question = f"{question} given the current {label}"

    return question


def detect_signals(report):

    signals = []

    pi = report.get("performance_intelligence", {})
    espe = report.get("energy_system_progression", {})
    metrics = report.get("metrics", {})

    # -----------------------------
    # Durability
    # -----------------------------
    dec = pi.get("durability", {}).get("mean_decoupling_7d")

    if dec is not None:
        if dec >= 8:
            signals.append(("durability_decline", 3))
        elif dec >= 5:
            signals.append(("durability_pressure", 2))


    # -----------------------------
    # Anaerobic Repeatability
    # -----------------------------
    dep = pi.get("anaerobic_repeatability", {}).get("mean_depletion_pct_7d")

    if dep is not None:
        if dep >= 0.60:
            signals.append(("anaerobic_depletion", 3))
        elif dep >= 0.40:
            signals.append(("anaerobic_load", 2))


    # -----------------------------
    # Neural Density
    # -----------------------------
    hi_days = pi.get("neural_density", {}).get("high_intensity_days_7d")

    if hi_days is not None:
        if hi_days >= 4:
            signals.append(("intensity_clustering", 3))
        elif hi_days == 3:
            signals.append(("high_intensity_density", 2))


    # -----------------------------
    # Load / Fatigue
    # -----------------------------
    fatigue = metrics.get("FatigueTrend")
    stress = metrics.get("StressTolerance")

    if isinstance(fatigue, dict):
        fatigue = fatigue.get("value")

    if isinstance(stress, dict):
        stress = stress.get("value")

    if fatigue is not None:
        if fatigue >= 15:
            signals.append(("fatigue_accumulation", 3))
        elif fatigue >= 10:
            signals.append(("fatigue_accumulation", 2))

    if stress is not None:
        if stress >= 1.5:
            signals.append(("load_pressure", 3))
        elif stress >= 1.3:
            signals.append(("load_pressure", 2))


    # -----------------------------
    # ESPE Adaptation Signals
    # -----------------------------
    systems = espe.get("systems", {})

    for system in systems.values():

        state = system.get("adaptation_state")

        if state == "decline":
            signals.append(("system_decline", 3))

        elif state == "strong_gain":
            signals.append(("system_progression", 2))

        elif state == "fragile":
            signals.append(("adaptation_fragile", 2))

        elif state == "unstable":
            signals.append(("adaptation_unstable", 3))

        elif state == "stable":
            signals.append(("adaptation_stable", 1))


    return signals


# Dominant Signals

def dominant_signal(signals):

    if not signals:
        return None

    signals_sorted = sorted(signals, key=lambda x: x[1], reverse=True)

    return signals_sorted[0][0]