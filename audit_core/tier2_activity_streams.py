"""
Tier-2 Activity Streams Analysis
=================================
Processes pre-computed stream summary statistics (DFA-alpha1, Heat Strain Index,
HRV, core temperature) for a single activity.

Called separately from the main pipeline and merged into the report output —
does NOT modify report_controller or semantic_json_builder.

Input:  streams_summary dict {stream_type: {min, max, mean, ...}}
Output: activity_streams_analysis dict ready for merge into coaching report
"""

import sys


def _err(msg: str) -> None:
    sys.stderr.write(f"[T2-STREAMS] {msg}\n")
    sys.stderr.flush()


def compute_activity_streams(streams_summary: dict) -> dict:
    """Analyse pre-computed stream stats and return enriched coaching signals.

    Args:
        streams_summary: dict produced by mcp_server.analyze_activity()
                         e.g. {"dfa_a1": {"mean": 1.046, "pct_above_lt1": 12.3}, ...}

    Returns:
        dict with keys: dfa_alpha1, heat_strain, core_temperature, hrv_intra
    """
    if not streams_summary or not isinstance(streams_summary, dict):
        return {}

    result: dict = {}

    # ── DFA-alpha1 ────────────────────────────────────────────────────────────
    dfa = streams_summary.get("dfa_a1", {})
    if dfa and dfa.get("mean") is not None:
        mean_dfa = dfa["mean"]
        pct_above_lt1 = dfa.get("pct_above_lt1", 0)
        pct_above_lt2 = dfa.get("pct_above_lt2", 0)

        if mean_dfa > 1.0:
            state = "aerobic_base"
            label = "Purely aerobic — well below LT1"
        elif mean_dfa > 0.75:
            state = "aerobic_threshold_zone"
            label = "Approaching LT1 — controlled aerobic load"
        elif mean_dfa > 0.5:
            state = "above_lt1"
            label = "Above LT1 — threshold/tempo territory"
        else:
            state = "above_lt2"
            label = "Predominantly above LT2 — high intensity"

        result["dfa_alpha1"] = {
            "mean": mean_dfa,
            "min": dfa.get("min"),
            "state": state,
            "label": label,
            "pct_above_lt1": pct_above_lt1,
            "pct_above_lt2": pct_above_lt2,
            "coaching_note": (
                f"{pct_above_lt1}% of session above aerobic threshold (LT1), "
                f"{pct_above_lt2}% above anaerobic threshold (LT2). "
                f"Mean α1={mean_dfa:.3f} → {label}."
            ),
        }
        _err(f"DFA-α1 mean={mean_dfa:.3f} state={state} "
             f"pct_above_lt1={pct_above_lt1}% pct_above_lt2={pct_above_lt2}%")

    # ── Heat Strain Index ─────────────────────────────────────────────────────
    hsi = streams_summary.get("heat_strain_index", {})
    if hsi and hsi.get("max") is not None:
        max_hsi = hsi["max"]
        mean_hsi = hsi.get("mean", 0)
        pct_high = hsi.get("pct_high_heat_strain", 0)

        if max_hsi > 2.0:
            level = "very_high"
            recommendation = (
                "Significant thermal load. Prioritise cooling, hydration boost, "
                "and reduce volume in subsequent heat sessions."
            )
        elif max_hsi > 1.0:
            level = "high"
            recommendation = (
                "Elevated heat strain. Monitor hydration and allow extended "
                "cool-down recovery before next session."
            )
        elif mean_hsi > 0.5:
            level = "moderate"
            recommendation = "Moderate heat stress — standard hydration precautions."
        else:
            level = "low"
            recommendation = "Minimal heat strain — no special action required."

        result["heat_strain"] = {
            "max_hsi": max_hsi,
            "mean_hsi": mean_hsi,
            "pct_high_strain": pct_high,
            "level": level,
            "recommendation": recommendation,
        }
        _err(f"HSI max={max_hsi:.2f} mean={mean_hsi:.2f} level={level}")

    # ── Core temperature ──────────────────────────────────────────────────────
    core = streams_summary.get("core_temperature", {})
    if core and core.get("max") is not None:
        max_core = core["max"]
        note = (
            "Peak core temp >38.5°C indicates significant thermal stress and "
            "impairs power output at threshold and above."
            if max_core > 38.5
            else "Core temperature within normal exercise range."
        )
        result["core_temperature"] = {
            "max_celsius": max_core,
            "mean_celsius": core.get("mean"),
            "note": note,
        }

    # ── Intra-activity HRV (raw R-R) ──────────────────────────────────────────
    hrv = streams_summary.get("hrv", {})
    if hrv and hrv.get("mean") is not None:
        result["hrv_intra"] = {
            "mean_rr_ms": hrv.get("mean"),
            "min_rr_ms": hrv.get("min"),
            "max_rr_ms": hrv.get("max"),
            "note": "Raw R-R intervals (ms) recorded during activity.",
        }

    return result
