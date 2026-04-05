"""
Intervals.icu MCP Server
========================
Exposes intervals.icu data and training-load analytics as MCP tools for
use with Claude Desktop (or any MCP-compatible client).

Setup:
  1. Copy .env.example → .env and fill in ICU_API_KEY + ICU_ATHLETE_ID
  2. pip install -r requirements.txt
  3. Add to Claude Desktop config (see claude_desktop_config.md)

Transport: stdio (standard for Claude Desktop)

Import order is critical:
  reports.py imports intervals_icu_adapter which patches audit_core BEFORE
  audit_core modules are loaded anywhere else.  Do NOT import audit_core
  directly in this file.
"""

# ── reports must be imported first — it pulls in intervals_icu_adapter ────
from reports import weekly_report  # noqa: E402

import json
import os
from datetime import date, timedelta

from dotenv import load_dotenv
from mcp.server.fastmcp import FastMCP

from intervals_client import IntervalsClient

load_dotenv()

mcp = FastMCP("intervals-icu")


def _client() -> IntervalsClient:
    return IntervalsClient()


# ── Athlete profile ───────────────────────────────────────────────────────────

@mcp.tool()
def get_athlete_profile() -> str:
    """Return the athlete's profile from intervals.icu: FTP, LTHR, weight, zones, and sport settings."""
    data = _client().get_athlete()
    # Keep only the most relevant fields to save context tokens
    keys = [
        "id", "name", "email", "sex", "dob", "weight",
        "ftp", "lthr", "threshold_pace", "threshold_power",
        "hrZones", "powerZones", "paceZones",
        "sport_settings",
    ]
    profile = {k: data.get(k) for k in keys if k in data}
    return json.dumps(profile, ensure_ascii=False, indent=2)


# ── Activities ────────────────────────────────────────────────────────────────

@mcp.tool()
def list_activities(oldest: str = "", newest: str = "") -> str:
    """List activities for the given date range (YYYY-MM-DD).

    Defaults to the last 28 days. Returns a compact list with key fields
    (date, name, type, distance, duration, TSS, IF, average power/HR).
    """
    if not oldest:
        oldest = (date.today() - timedelta(days=28)).isoformat()
    if not newest:
        newest = date.today().isoformat()

    activities = _client().list_activities(oldest=oldest, newest=newest)

    compact_keys = [
        "id", "start_date_local", "name", "type",
        "distance", "moving_time", "elapsed_time",
        "icu_training_load", "icu_intensity",
        "average_watts", "weighted_average_watts",
        "average_heartrate", "max_heartrate",
        "total_elevation_gain",
        "icu_z1", "icu_z2", "icu_z3", "icu_z4", "icu_z5", "icu_z6",
    ]
    compact = [
        {k: a.get(k) for k in compact_keys if k in a}
        for a in activities
    ]
    return json.dumps(compact, ensure_ascii=False, indent=2)


@mcp.tool()
def get_activity(activity_id: str) -> str:
    """Return full details for a single activity.

    activity_id: the activity ID as returned by list_activities, e.g. "i126379241".
    The "i" prefix is required — pass the full ID string, not just the number.
    Returns a list with one activity object containing power zones, HR zones,
    streams, laps, decoupling, efficiency factor and all computed metrics.
    """
    # Ensure i-prefix is present
    aid = activity_id if str(activity_id).startswith("i") else f"i{activity_id}"
    data = _client().get_activity(aid)
    # API returns a list — unwrap to single object if possible
    if isinstance(data, list) and len(data) == 1:
        data = data[0]
    return json.dumps(data, ensure_ascii=False, indent=2)


# ── Wellness ──────────────────────────────────────────────────────────────────

@mcp.tool()
def get_wellness(oldest: str = "", newest: str = "") -> str:
    """Return wellness records for the given date range (YYYY-MM-DD).

    Defaults to the last 14 days. Includes HRV, sleep, fatigue, form (TSB),
    CTL, ATL, and subjective wellness scores.
    """
    if not oldest:
        oldest = (date.today() - timedelta(days=14)).isoformat()
    if not newest:
        newest = date.today().isoformat()

    wellness = _client().list_wellness(oldest=oldest, newest=newest)
    return json.dumps(wellness, ensure_ascii=False, indent=2)


# ── Power curves ──────────────────────────────────────────────────────────────

@mcp.tool()
def get_power_curves(sport_type: str = "Ride") -> str:
    """Return mean-maximal power curves for the given sport type.

    sport_type: 'Ride' | 'Run' | 'Swim' | 'VirtualRide' etc.
    Returns MMP values at standard durations: 1s, 5s, 10s, 30s, 1min, 2min,
    5min, 10min, 20min, 60min (in watts).
    """
    data = _client().get_power_curves(sport_type=sport_type)
    return json.dumps(data, ensure_ascii=False, indent=2)


# ── Calendar ──────────────────────────────────────────────────────────────────

@mcp.tool()
def get_calendar(oldest: str = "", newest: str = "") -> str:
    """Return planned workouts / calendar events for the given date range.

    Defaults to today → +14 days.
    """
    if not oldest:
        oldest = date.today().isoformat()
    if not newest:
        newest = (date.today() + timedelta(days=14)).isoformat()

    events = _client().list_events(oldest=oldest, newest=newest)
    return json.dumps(events, ensure_ascii=False, indent=2)


@mcp.tool()
def create_workout(
    start_date: str,
    name: str,
    description: str = "",
    sport_type: str = "Ride",
    duration_seconds: int = 0,
    target_tss: int = 0,
) -> str:
    """Create a planned workout in the intervals.icu calendar.

    Args:
        start_date: Date in YYYY-MM-DD format.
        name: Workout name (e.g. "Z2 Endurance 2h").
        description: Workout steps in intervals.icu NATIVE FORMAT (see below).
            intervals.icu automatically parses this into a structured workout
            with colored power-zone blocks visible in the calendar and
            downloadable to Garmin/Wahoo.

            NATIVE FORMAT RULES:
            - Each step starts with a dash: -<duration> <zone>
            - Duration: 10m, 1h, 1h30m, 30s
            - Zones: z1 z2 z3 z4 z5 z6 z7  or range  z1-z2
            - Repeat block: blank line, then Nx on its own line, then steps indented with " -"
            - CRITICAL: there MUST be a blank line (empty line) before any Nx repeat block
            - Intensity: zone (z1-z7) OR percentage range (85-95%) — NO "@" prefix, just digits
            - WRONG: -8m @105-110%   RIGHT: -8m 105-110% 85-90rpm
            - WRONG: -10m z4 @88-93%  RIGHT: -10m 88-93% 85-90rpm
            - Cadence: always include, e.g. 85-90rpm or 100-110rpm — NO "@" prefix

            EXAMPLES:
            Z2 endurance (always include cadence):
                -10m z1 75-85rpm
                -1h40m z2 85-90rpm
                -10m z1 75-85rpm

            Threshold intervals (blank line before 3x, cadence on every step):
                -15m z1-z2 85-90rpm

                3x
                 -10m 88-93% 85-90rpm
                 -5m z1-z2 85-90rpm
                -10m z1 80-85rpm

            VO2max (blank line before 5x, high cadence cue):
                -15m z1-z2 85-90rpm

                5x
                 -4m 106-120% 100-110rpm
                 -4m z1 85-90rpm
                -10m z1 80-85rpm

            Neuromuscular sprints:
                -15m z1-z2 85-90rpm

                8x
                 -30s 130-150% 110-120rpm
                 -4m30s z1 80-85rpm
                -10m z1 75-80rpm

            DO NOT use free text like "Warm-up 15 min easy".
            ALWAYS use the dash-zone format above.
            ALWAYS put a blank line before any Nx repeat block.
            ALWAYS include cadence on every step.

        sport_type: "Ride" | "Run" | "Swim" | "VirtualRide" | "WeightTraining" | ...
        duration_seconds: Target duration in seconds (0 = not set).
        target_tss: Target TSS/training load (0 = not set).

    Returns the created event as JSON.
    """
    # intervals.icu requires full ISO datetime — append T00:00:00 if only date given
    if len(start_date) == 10:
        start_date = f"{start_date}T00:00:00"

    event: dict = {
        "start_date_local": start_date,
        "name": name,
        "type": sport_type,
        "category": "WORKOUT",
    }
    if description:
        event["description"] = description
    if duration_seconds > 0:
        event["moving_time"] = duration_seconds
    if target_tss > 0:
        event["load_target"] = target_tss

    result = _client().create_event(event)
    return json.dumps(result, ensure_ascii=False, indent=2)


@mcp.tool()
def delete_workout(event_id: int) -> str:
    """Delete a planned workout from the intervals.icu calendar by its event ID."""
    _client().delete_event(event_id)
    return json.dumps({"deleted": True, "event_id": event_id})


# ── Activity deep analysis ────────────────────────────────────────────────────

@mcp.tool()
def analyze_activity(activity_id: str) -> str:
    """Fetch full activity data + time-series streams for deep single-activity analysis.

    Returns a combined JSON with:
      - activity: full metadata (power zones, HR zones, TSS, IF, decoupling, etc.)
      - streams_summary: per-stream descriptive stats computed from the raw data
      - streams_raw: raw time-series arrays (time, watts, heartrate, dfa_a1, hrv,
                     heat_strain_index, core_temperature, respiration, cadence)
      - wellness: wellness record for the activity date (HRV, sleep, resting HR)

    DFA-alpha1 interpretation (aerobic threshold detection):
      α1 > 1.0   → purely aerobic (Z1–Z2)
      α1 ≈ 0.75  → aerobic threshold (LT1) — key coaching marker
      α1 < 0.75  → above LT1, approaching threshold
      α1 < 0.5   → high intensity (approaching or above LT2)

    Heat Strain Index (HSI) from Garmin body temperature sensors:
      < 0.5  → low heat strain
      0.5–1.0 → moderate
      > 1.0  → high heat strain (reduce intensity)
      > 2.0  → very high, dangerous

    Use this tool when the user asks to analyse a specific workout, check
    aerobic threshold markers, or evaluate thermal load.
    """
    aid = activity_id if str(activity_id).startswith("i") else f"i{activity_id}"
    client = _client()

    # 1. Full activity metadata
    activity = client.get_activity(aid)
    if isinstance(activity, list) and len(activity) == 1:
        activity = activity[0]

    # 2. Time-series streams
    streams = {}
    try:
        streams = client.get_activity_streams(aid)
    except Exception as e:
        streams = {"error": str(e)}

    # 3. Compute summary stats per stream
    def _stats(values: list) -> dict:
        if not values:
            return {}
        nums = [v for v in values if v is not None]
        if not nums:
            return {}
        n = len(nums)
        mn = min(nums)
        mx = max(nums)
        avg = sum(nums) / n
        return {"count": n, "min": round(mn, 3), "max": round(mx, 3), "mean": round(avg, 3)}

    streams_summary: dict = {}
    for stream_type, data in streams.items():
        if stream_type == "error" or not isinstance(data, list):
            continue
        s = _stats(data)
        if not s:
            continue
        # DFA-alpha1 thresholds
        if stream_type == "dfa_a1":
            nums = [v for v in data if v is not None]
            total = len(nums)
            if total:
                below_075 = sum(1 for v in nums if v < 0.75)
                below_050 = sum(1 for v in nums if v < 0.50)
                s["pct_above_lt1"] = round(below_075 / total * 100, 1)   # % time above aerobic threshold
                s["pct_above_lt2"] = round(below_050 / total * 100, 1)   # % time above anaerobic threshold
                s["aerobic_threshold_estimate"] = "check dfa_a1 ≈ 0.75 crossings"
        # HSI thresholds
        if stream_type == "heat_strain_index":
            nums = [v for v in data if v is not None]
            total = len(nums)
            if total:
                high = sum(1 for v in nums if v > 1.0)
                s["pct_high_heat_strain"] = round(high / total * 100, 1)
        streams_summary[stream_type] = s

    # 4. Wellness for activity date
    wellness_day: dict = {}
    try:
        activity_date = (activity.get("start_date_local") or "")[:10]
        if activity_date:
            wellness_list = client.list_wellness(oldest=activity_date, newest=activity_date)
            if wellness_list:
                wellness_day = wellness_list[0]
    except Exception:
        pass

    result = {
        "activity": activity,
        "streams_summary": streams_summary,
        "streams_raw": streams,
        "wellness": wellness_day,
    }
    return json.dumps(result, ensure_ascii=False, indent=2)


# ── Weekly report ─────────────────────────────────────────────────────────────

@mcp.tool()
def run_weekly_report() -> str:
    """Run a full training-load analysis covering all analytical tiers.

    Tier-2 Derived:
      ACWR (EWMA 7d/28d), Monotony, Strain (Foster method), FatigueTrend,
      ZQI (Zone Quality Index), Polarisation (Seiler 3-zone + Treff PI),
      FatOxEfficiency, FOxI, MES, StressTolerance, lactate (if available).

    Tier-2 Extended:
      CTL/ATL/TSB from wellness, fitness/fatigue trend slopes,
      Recovery Index, personalized Z2 calibration via lactate.

    Wellness (full):
      HRV 42d mean, deviation %, 14d stability index, resting HR delta,
      sleep score 14d rolling avg, coverage stats.

    Tier-3 Performance Intelligence:
      Anaerobic Repeatability (W' depletion %), Durability (cardiac decoupling),
      Neural Density (joules above FTP, mean IF, efficiency factor).
      Training state interpretation → operational coaching directive.

    Tier-3 ESPE:
      Power curve analysis across energy systems: anaerobic (1m), VO2 (5m),
      threshold (20m), aerobic durability (60m). Adaptation state, curve profile.

    Tier-3 Future Forecast:
      CTL/ATL/TSB projections from planned calendar events (14d).

    Use this as the primary data-gathering step before any coaching recommendation.
    """
    client = _client()

    # 90-day activities with all light fields needed for Tier-2 + Tier-3
    activities = client.list_activities(
        oldest=(date.today() - timedelta(days=90)).isoformat(),
        newest=date.today().isoformat(),
    )

    # 42-day wellness for full HRV baseline
    wellness = client.list_wellness(
        oldest=(date.today() - timedelta(days=42)).isoformat(),
        newest=date.today().isoformat(),
    )

    # Calendar events for future forecast
    try:
        calendar_events = client.list_events(
            oldest=date.today().isoformat(),
            newest=(date.today() + timedelta(days=14)).isoformat(),
        )
    except Exception:
        calendar_events = []

    # Athlete profile — supplies FTP + timezone to the pipeline
    athlete: dict | None = None
    ftp: float | None = None
    try:
        athlete = client.get_athlete()
        ftp = athlete.get("ftp") or athlete.get("threshold_power")
    except Exception:
        pass

    report = weekly_report(
        activities=activities,
        wellness=wellness,
        # power_curve_block intentionally omitted — tier0 fetches power curves
        # directly via the patched fetch_with_retry so the response-format
        # normalisation (_wrap_power_curves) runs correctly.
        calendar_events=calendar_events,
        ftp=ftp,
        athlete=athlete,
    )
    return json.dumps(report, ensure_ascii=False, indent=2)


# ── Entry point ───────────────────────────────────────────────────────────────

if __name__ == "__main__":
    mcp.run(transport="stdio")
