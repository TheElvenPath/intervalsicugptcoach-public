"""
reports.py — Thin wrapper over audit_core pipeline
====================================================
Delegates all analysis to the original audit_core.report_controller.
The intervals_icu_adapter patches Cloudflare Worker calls with direct
intervals.icu API calls using Basic Auth before any audit_core modules load.

Import order matters:
  1. intervals_icu_adapter  ← patches env vars + functions
  2. audit_core.*           ← loaded with patches already applied

Pre-fetched data contract (all optional):
  activities_light  list[dict]   90-day activity list (light fields)
  wellness          list[dict]   42-day wellness records
  athlete           dict         Athlete profile from intervals.icu
  calendar          list[dict]   Planned events (next 14d)
  power_curve       dict         Omit — let tier0 fetch via adapter

If no pre-fetched data is supplied, tier0 fetches everything itself
via the patched fetch_with_retry (direct intervals.icu API, Basic Auth).
"""

# ── CRITICAL: patch env vars + audit_core functions BEFORE any audit_core import
import intervals_icu_adapter  # noqa: F401 — side effects: apply() called on import

import json

from audit_core.report_controller import run_report as _run_report
from audit_core.tier2_activity_streams import compute_activity_streams


# ═══════════════════════════════════════════════════════════════════════════
# PUBLIC API
# ═══════════════════════════════════════════════════════════════════════════

def weekly_report(
    activities: list | None = None,
    wellness: list | None = None,
    power_curve_block: dict | None = None,
    calendar_events: list | None = None,
    ftp: float | None = None,
    athlete: dict | None = None,
) -> dict:
    """
    Run the full audit_core analysis pipeline (Tier-0 → Tier-3) and return
    a JSON-serialisable coaching report in URF v5.1 semantic format.

    Parameters
    ----------
    activities : list[dict] | None
        Pre-fetched activity list (light fields).  If None, tier0 fetches
        90 days of activities via the adapter.
    wellness : list[dict] | None
        Pre-fetched wellness records.  If None, tier0 fetches 42 days.
    power_curve_block : dict | None
        Ignored — tier0 always fetches power curves directly so that the
        adapter's response-format normalisation (_wrap_power_curves) runs.
    calendar_events : list[dict] | None
        Pre-fetched calendar events.  If None, the patched
        fetch_calendar_fallback fetches the next 14 days.
    ftp : float | None
        Athlete FTP (W).  Passed via athlete dict if available; otherwise
        tier0 derives it from the fetched athlete profile.
    athlete : dict | None
        Pre-fetched athlete profile.  If None, tier0 fetches it.

    Returns
    -------
    dict
        URF v5.1 semantic_graph (JSON-serialisable) on success, or an
        error dict ``{"status": "error", "message": "..."}`` on failure.
    """
    # ── Build prefetch context (only pass what we have) ───────────────────
    kwargs: dict = {}

    if isinstance(activities, list) and activities:
        kwargs["activities_light"] = activities

    if isinstance(wellness, list) and wellness:
        kwargs["wellness"] = wellness

    if isinstance(athlete, dict) and athlete:
        # Ensure timezone is present (required by the pipeline)
        if not athlete.get("timezone"):
            athlete = {**athlete, "timezone": "UTC"}
        kwargs["athlete"] = athlete

    if isinstance(calendar_events, list):
        kwargs["calendar"] = calendar_events

    # NOTE: power_curve intentionally NOT passed as prefetch.
    # tier0 calls fetch_with_retry → adapter rewrites the URL and wraps
    # the response into {"list": [prev, curr]} format that ESPE expects.
    # Passing raw intervals.icu data here would bypass that normalisation.

    # ── Run full pipeline ─────────────────────────────────────────────────
    try:
        result = _run_report(
            reportType="weekly",
            output_format="semantic",
            render_mode="full+metrics",
            include_coaching_metrics=True,
            suppressPrompts=True,
            **kwargs,
        )
    except Exception as exc:
        return {"status": "error", "message": str(exc)}

    # ── Unpack (output, compliance) tuple ─────────────────────────────────
    if isinstance(result, tuple):
        output, _ = result
    else:
        output = result

    if not isinstance(output, dict):
        return {"status": "error", "message": "Unexpected pipeline output format"}

    # ── Return semantic_graph (preferred) or sanitised output ─────────────
    semantic = output.get("semantic_graph")
    if isinstance(semantic, dict):
        return _make_serialisable(semantic)

    # Fallback: strip non-serialisable context key and return raw output
    output.pop("context", None)
    return _make_serialisable(output)


def analyze_activity_report(activity: dict, streams_summary: dict) -> dict:
    """
    Run full audit_core pipeline for a single activity enriched with stream data.

    The standard weekly pipeline runs with [activity] as the dataset.
    DFA-alpha1, Heat Strain Index, core temperature and intra-activity HRV
    are computed separately via tier2_activity_streams and merged on top —
    no changes to report_controller or semantic_json_builder required.

    Parameters
    ----------
    activity : dict
        Full activity object from intervals.icu (as returned by get_activity).
    streams_summary : dict
        Pre-computed stream stats from mcp_server.analyze_activity()
        e.g. {"dfa_a1": {"mean": 1.046, "pct_above_lt1": 12.3}, ...}

    Returns
    -------
    dict
        Merged report: URF v5.1 semantic_graph + "streams_analysis" key.
    """
    # 1. Run the standard pipeline with the single activity as the dataset
    report = weekly_report(activities=[activity])

    # 2. Compute streams analysis independently
    streams_analysis = compute_activity_streams(streams_summary)

    # 3. Merge — enrich report without touching existing keys
    if isinstance(report, dict) and streams_analysis:
        report["streams_analysis"] = _make_serialisable(streams_analysis)

    return report


# ═══════════════════════════════════════════════════════════════════════════
# HELPERS
# ═══════════════════════════════════════════════════════════════════════════

def _make_serialisable(obj):
    """
    Recursively convert any non-JSON-serialisable value (numpy types,
    pandas Timestamps, DataFrames, etc.) to a plain Python object.
    """
    try:
        # Fast path: already serialisable
        json.dumps(obj)
        return obj
    except (TypeError, ValueError):
        pass

    if isinstance(obj, dict):
        return {k: _make_serialisable(v) for k, v in obj.items()}
    if isinstance(obj, (list, tuple)):
        return [_make_serialisable(v) for v in obj]

    # numpy / pandas scalars
    try:
        import numpy as np
        if isinstance(obj, (np.integer,)):
            return int(obj)
        if isinstance(obj, (np.floating,)):
            return float(obj)
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        if hasattr(obj, "item"):          # generic numpy scalar
            return obj.item()
    except ImportError:
        pass

    try:
        import pandas as pd
        if isinstance(obj, pd.Timestamp):
            return obj.isoformat()
        if isinstance(obj, pd.DataFrame):
            return obj.to_dict(orient="records")
        if isinstance(obj, pd.Series):
            return obj.tolist()
    except ImportError:
        pass

    # datetime / date
    try:
        from datetime import datetime, date
        if isinstance(obj, (datetime, date)):
            return obj.isoformat()
    except ImportError:
        pass

    # Last resort: stringify
    return str(obj)
