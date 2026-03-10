#!/usr/bin/env python3
"""
Intervals.icu GPTCoach Railway API
Final Unified Version with Prefetch Normalization
Parses prefetched data into identical Tier-0 format as local Python
Ensures parity for daily_load, zone distributions, derived metrics, etc.
"""
import re
from fastapi import FastAPI, Query, Request, HTTPException
from fastapi.responses import JSONResponse
import os, sys, io, json, math, pandas as pd, numpy as np
from datetime import datetime, timedelta, date
from contextlib import redirect_stdout
from audit_core.errors import AuditHalt
from collections import Counter
from demo_weekly import DEMO_WEEKLY
import copy, traceback

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), "audit_core"))

from audit_core.report_controller import run_report
from audit_core.utils import debug
from audit_core.tier0_pre_audit import expand_zones

import logging

logging.basicConfig(
    level=logging.INFO,
    stream=sys.stdout,   # 👈 THIS is the key fix
    format="%(levelname)s:%(name)s:%(message)s"
)

logger = logging.getLogger("app")

print("[BOOT] 🚀 Starting Montis.icu GPT Coach Railway API")
icuoauth = os.getenv("ICU_OAUTH")
if icuoauth:
    print("[BOOT-WARN] Variable ICU_OAUTH detected:", icuoauth[:10], "...")
else:
    print("[BOOT] ICU_OAUTH relying on passed ICU_OAUTH")

app = FastAPI(title="Montis.icu GPT Coach Railway API", version="2.0")

# ============================================================
# 🧹 SANITIZER
# ============================================================
def sanitize(obj, seen=None):
    import pandas as pd, numpy as np
    if isinstance(obj, (str, int, float, bool)) or obj is None:
        if isinstance(obj, float) and (math.isnan(obj) or math.isinf(obj)):
            return None
        return obj
    if isinstance(obj, (datetime, date, pd.Timestamp)):
        try:
            return obj.isoformat()
        except Exception:
            return str(obj)
    if isinstance(obj, (np.integer, np.floating)):
        return float(obj)
    if seen is None:
        seen = set()
    if isinstance(obj, (dict, list, tuple, pd.DataFrame, pd.Series)):
        oid = id(obj)
        if oid in seen:
            return obj  # allow reuse, not recursion
        seen.add(oid)
    if isinstance(obj, pd.DataFrame):
        return sanitize(obj.to_dict(orient="records"), seen)
    if isinstance(obj, pd.Series):
        return sanitize(obj.to_dict(), seen)
    if isinstance(obj, dict):
        return {sanitize(k, seen): sanitize(v, seen) for k, v in obj.items()}
    if isinstance(obj, (list, tuple)):
        return [sanitize(i, seen) for i in obj]
    return str(obj)


# ============================================================
# 🧩 NORMALIZER — replicate Tier-0 Pre-Audit
# ============================================================
def normalize_prefetched_context(data):
    """Normalize prefetched payload from Cloudflare → local Python shape"""
    context = {}
    try:
        def safe_df(obj):
            if obj is None:
                return pd.DataFrame()

            # Already a dataframe
            if isinstance(obj, pd.DataFrame):
                return obj

            # Single dict → wrap into list
            if isinstance(obj, dict):
                obj = [obj]

            # Not list-like → empty
            if not isinstance(obj, (list, tuple)):
                return pd.DataFrame()

            df = pd.DataFrame(obj)

            if "start_date_local" in df.columns:
                df["start_date_local"] = pd.to_datetime(
                    df["start_date_local"], errors="coerce"
                ).dt.tz_localize(None)

            if "date" in df.columns:
                df["date"] = pd.to_datetime(
                    df["date"], errors="coerce"
                ).dt.tz_localize(None)

            num_cols = [
                c for c in df.columns
                if any(x in c.lower() for x in [
                    "distance","moving_time","tss",
                    "load","icu_training_load","if","vo2max"
                ])
            ]

            for c in num_cols:
                df[c] = pd.to_numeric(df[c], errors="coerce")

            return df

        # Light / Full / Wellness
        df_light = safe_df(data.get("activities_light"))
        df_full  = safe_df(data.get("activities_full"))
        df_well  = safe_df(data.get("wellness"))

        athlete = data.get("athlete") or {}
        calendar = data.get("calendar", {})

        #debug(context, f"[RAW FULL SAMPLE] {str(data.get('activities_full', [{}])[0])[:5000]}")

        # 🔒 CONTRACT INVARIANT — athlete must have an id
        if not isinstance(athlete, dict):
            raise AuditHalt(
                "Athlete profile missing or invalid.",
                code="ATHLETE_PROFILE_INVALID",
                severity="hard"
            )

        if "id" not in athlete:
            raise AuditHalt(
                "Your Intervals.icu account is not connected. "
                "Please authorize the app to access your training data, then try again.\n\n"
                "Setup guide:\n"
                "https://www.montis.icu/setup.html",
                code="OAUTH_NOT_CONFIGURED",
                severity="hard"
            )

        # 🔒 GUARD: Abort if ALL rows are STRAVA API stubs (exact note match)
        if not df_light.empty and "_note" in df_light.columns:

            strava_note_text = "STRAVA activities are not available via the API"

            # Drop NaN notes first
            notes = df_light["_note"].dropna()

            if (
                len(notes) == len(df_light) and  # every row has a note
                (notes == strava_note_text).all()
            ):
                debug(
                    context,
                    "[GUARD] All activities are STRAVA API stubs — aborting."
                )

                raise HTTPException(
                    status_code=422,
                    detail=(
                        "Activities exist for this period, but they originate from STRAVA "
                        "and are not accessible via the Intervals API. "
                        "No training metrics (time, distance, load) are available "
                        "to generate a report. "
                        "Connect Garmin/Wahoo/Zwift etc directly or upload FIT files. "
                        "OR see https://forum.intervals.icu/t/import-all-data-from-strava/81068"
                    ),
                )

        # 🔒 STRAVA STUB FILTER — detect and remove unusable API stub rows
        strava_stub_detected = False
        strava_note_text = "STRAVA activities are not available via the API"

        if not df_light.empty and "_note" in df_light.columns:

            # --- Detect stubs BEFORE removal ---
            if df_light["_note"].astype(str).str.contains(
                "STRAVA activities are not available", case=False
            ).any():
                strava_stub_detected = True

            # Persist flag into context
            context.setdefault("data_quality_flags", {})
            context["data_quality_flags"]["strava_stub_detected"] = strava_stub_detected

            # --- Remove stubs from LIGHT ---
            before_light = len(df_light)
            df_light = df_light[
                df_light["_note"].fillna("") != strava_note_text
            ].copy()
            removed_light = before_light - len(df_light)

            # --- Remove stubs from FULL (if column exists) ---
            if "_note" in df_full.columns:
                before_full = len(df_full)
                df_full = df_full[
                    df_full["_note"].fillna("") != strava_note_text
                ].copy()
                removed_full = before_full - len(df_full)
            else:
                removed_full = 0

            if removed_light > 0:
                debug(
                    context,
                    f"[NORM] Removed {removed_light} STRAVA stub rows (light), "
                    f"{removed_full} (full)"
                )

        # ─────────────────────────────────────────────
        # 🩺 Ensure baseline columns exist for Tier-0 stability
        # ─────────────────────────────────────────────
        for df_name, df in {"light": df_light, "full": df_full}.items():
            for col in ["start_date_local", "moving_time", "distance", "icu_training_load", "type"]:
                if col not in df.columns:
                    if col == "start_date_local":
                        df[col] = pd.NaT
                    elif col in ["moving_time", "distance", "icu_training_load"]:
                        df[col] = 0
                    else:
                        df[col] = ""
            debug({}, f"[NORM] ensured baseline columns exist for df_{df_name} ({len(df)} rows)")


        context["activities_light"] = df_light.to_dict(orient="records")
        context["activities_full"]  = df_full.to_dict(orient="records")
        context["wellness"]         = df_well.to_dict(orient="records")
        context["athlete"]          = athlete
        context["calendar"]         = calendar
        
        # -------------------------------------------------
        # 🔋 POWER CURVE NORMALIZATION (Worker → ESPE)
        # Replicates Tier-0 fetch_power_curves() behaviour
        # -------------------------------------------------
        power_curve = data.get("power_curve")

        normalized_curves = {}

        def extract_anchor(block, seconds):

            secs = block.get("secs", [])
            vals = block.get("values", [])
            acts = block.get("activity_id", [])

            if not secs:
                return None

            # closest duration match (safer than exact index)
            idx = min(range(len(secs)), key=lambda i: abs(secs[i] - seconds))

            power = vals[idx]
            activity_id = acts[idx] if idx < len(acts) else None

            if activity_id and not str(activity_id).startswith("i"):
                activity_id = f"i{activity_id}"

            return {
                "power": power,
                "activity_id": activity_id
            }
            
        if isinstance(power_curve, dict):

            for sport, payload in power_curve.items():

                if not isinstance(payload, dict):
                    debug(context, f"[NORM] Invalid curve block for {sport}")
                    continue

                curve_list = payload.get("list")

                if not curve_list or len(curve_list) < 2:
                    debug(context, f"[NORM] ⚠ power_curve payload missing windows for {sport}")
                    continue

                prev = curve_list[0]
                curr = curve_list[1]

                normalized_curves[sport] = {
                    "previous": {
                        "5s": extract_anchor(prev, 5),
                        "1m": extract_anchor(prev, 60),
                        "5m": extract_anchor(prev, 300),
                        "20m": extract_anchor(prev, 1200),
                        "60m": extract_anchor(prev, 3600),
                    },
                    "current": {
                        "5s": extract_anchor(curr, 5),
                        "1m": extract_anchor(curr, 60),
                        "5m": extract_anchor(curr, 300),
                        "20m": extract_anchor(curr, 1200),
                        "60m": extract_anchor(curr, 3600),
                    },
                    "window_days": prev.get("days"),
                    "curve_regression": {
                        "slope": curr.get("mapPlot", {}).get("poSlope"),
                        "r2": curr.get("mapPlot", {}).get("poR2"),
                    }
                }

                # --------------------------------------------
                # FFT_CURVES model extraction
                # --------------------------------------------
                fft_model = next(
                    (m for m in curr.get("powerModels", []) if m.get("type") == "FFT_CURVES"),
                    None
                )

                if fft_model:
                    normalized_curves[sport]["models"] = {
                        "source": "FFT_CURVES",
                        "cp": fft_model.get("criticalPower"),
                        "w_prime": fft_model.get("wPrime"),
                        "pmax": fft_model.get("pMax"),
                        "ftp": fft_model.get("ftp"),
                    }

                # --------------------------------------------
                # Guards
                # --------------------------------------------
                if not normalized_curves[sport]["current"]["5m"]:
                    debug(context, f"[NORM] ESPE missing 5m anchor for {sport}")

                debug(
                    context,
                    f"[NORM] ESPE anchors normalized → {sport}",
                    list(normalized_curves[sport]["current"].keys())
                )

            context["power_curve"] = normalized_curves

            debug(
                context,
                f"[NORM] ESPE power curves loaded for sports={list(normalized_curves.keys())}"
            )

        else:
            context["power_curve"] = {}

        # -------------------------------------------------------------------------------------
        # Derived Tier-0 equivalents
        context["df_light"]  = df_light
        context["df_master"] = df_full
        context["_df_scope_full"] = df_full.copy()
        context["df_wellness"] = df_well

        # Build daily summary if possible
        if (
            not df_full.empty and
            "icu_training_load" in df_full.columns and
            "start_date_local" in df_full.columns
        ):
            try:
                df_daily = (
                    df_full.groupby(df_full["start_date_local"].dt.date)["icu_training_load"]
                    .sum(min_count=1)
                    .reset_index()
                    .rename(columns={"start_date_local": "date"})
                )

                df_daily["date"] = pd.to_datetime(df_daily["date"], errors="coerce")
                df_daily = df_daily.sort_values("date")

                # --- enforce rolling 7-day window ---
                if not df_daily.empty:
                    end = df_daily["date"].max()
                    start = end - pd.Timedelta(days=6)

                    date_index = pd.date_range(start=start, end=end, freq="D")

                    df_daily = (
                        df_daily.set_index("date")
                        .reindex(date_index, fill_value=0)
                        .rename_axis("date")
                        .reset_index()
                    )

                context["df_daily"] = df_daily
                debug(context, f"[NORM] built rolling df_daily {len(df_daily)} days")

            except Exception as e:
                context["df_daily"] = pd.DataFrame(columns=["date", "icu_training_load"])
                debug(context, f"[NORM] df_daily build failed: {e}")
        else:
            context["df_daily"] = pd.DataFrame(columns=["date", "icu_training_load"])
            debug(context, "[NORM] df_daily empty — missing date or load columns")

        # Snapshot 7d totals
        if not df_full.empty:
            last7 = df_full.tail(7)
            context["tier0_snapshotTotals_7d"] = {
                "tss": float(last7["icu_training_load"].sum()) if "icu_training_load" in last7 else 0,
                "hours": float(last7["moving_time"].sum())/3600 if "moving_time" in last7 else 0,
                "distance_km": float(last7["distance"].sum())/1000 if "distance" in last7 else 0,
                "sessions": len(last7),
            }
            debug(context, f"[NORM] snapshot_7d totals computed: {context['tier0_snapshotTotals_7d']}")
        else:
            context["tier0_snapshotTotals_7d"] = {"tss":0,"hours":0,"distance_km":0,"sessions":0}

        # Timezone
        context["timezone"] = athlete.get("timezone", "UTC")
        context["athleteProfile"] = athlete
        context["athlete_raw"] = athlete
        context["prefetch_done"] = True
        context["semantic_mode"] = True

        # --- Normalize Intervals zone arrays (for HR and Power) ---
        def normalize_zone_fields(df):
            """Convert zone strings to JSON lists if needed (Intervals-prefetched data)."""
            if df.empty:
                return df
            for col in df.columns:
                if "zone_times" in col or "zones" in col:
                    # Convert JSON-encoded strings (e.g., '[{"secs":120},...]') to lists
                    if df[col].dtype == object:
                        df[col] = df[col].apply(
                            lambda x: json.loads(x) if isinstance(x, str) and x.strip().startswith("[") else x
                        )
            return df

        df_full = normalize_zone_fields(df_full)
        df_light = normalize_zone_fields(df_light)
        debug(context, "[NORM] ✅ Normalized zone fields in prefetched context")

        # --- Expand HR/Power/Pace zones to match Tier-0 local parity ---
        try:
            for field, prefix in [
                ("icu_zone_times", "power"),
                ("icu_hr_zone_times", "hr"),
                ("pace_zone_times", "pace"),
            ]:
                if field in df_full.columns and not df_full.empty:
                    expanded = expand_zones(df_full[[field]].copy(), field, prefix)
                    for col in expanded.columns:
                        if col not in df_full.columns:
                            df_full[col] = expanded[col]
                    # 💡 keep the original columns for Tier-1 fusion
            debug(context, "[NORM] ✅ Expanded HR/Power/Pace zones (non-destructive)")

            debug(context, "[NORM] ✅ Expanded HR/Power/Pace zones for Tier-0 parity")
        except Exception as e:
            debug(context, f"[NORM] ⚠️ Zone expansion skipped: {e}")

        # -------------------------------------------------
        # 🫀 Expand HRR nested dict (Tier-0 parity fix)
        # -------------------------------------------------
        if "icu_hrr" in df_full.columns:
            df_full["icu_hrr.hrr"] = df_full["icu_hrr"].apply(
                lambda x: x.get("hrr") if isinstance(x, dict) else None
            )
            df_full["icu_hrr.start_bpm"] = df_full["icu_hrr"].apply(
                lambda x: x.get("start_bpm") if isinstance(x, dict) else None
            )
            df_full["icu_hrr.end_bpm"] = df_full["icu_hrr"].apply(
                lambda x: x.get("end_bpm") if isinstance(x, dict) else None
            )

        if "icu_hrr" in df_light.columns:
            df_light["icu_hrr.hrr"] = df_light["icu_hrr"].apply(
                lambda x: x.get("hrr") if isinstance(x, dict) else None
            )
            df_light["icu_hrr.start_bpm"] = df_light["icu_hrr"].apply(
                lambda x: x.get("start_bpm") if isinstance(x, dict) else None
            )
            df_light["icu_hrr.end_bpm"] = df_light["icu_hrr"].apply(
                lambda x: x.get("end_bpm") if isinstance(x, dict) else None
            )

        debug(context, "[NORM] ✅ Expanded icu_hrr nested dict (non-destructive)")

        # --- Update context after expansion ---
        context["df_full"] = df_full
        context["activities_full"] = df_full.to_dict(orient="records")
        debug(
            context,
            f"[NORM] activities_light={len(df_light)} full={len(df_full)} wellness={len(df_well)} "
            f"athlete_keys={list(athlete.keys()) if athlete else 'none'}"
        )


        debug(context, f"[NORM] activities_light={len(df_light)} full={len(df_full)} wellness={len(df_well)} athlete_keys={list(athlete.keys()) if athlete else 'none'}")
    except HTTPException as e:
        raise e


    except Exception as e:
        debug(context, f"[NORM] ❌ Normalization failed: {e}")
        raise

    return context  

# ============================================================
# 🧠 CORE RUN FUNCTION
# ============================================================
def _run_full_audit(range: str, output_format="markdown", prefetch_context=None):
    os.environ["REPORT_TYPE"] = range.lower()
    buffer = io.StringIO()
    with redirect_stdout(buffer):
        if prefetch_context:
            report, compliance = run_report(reportType=range, output_format=output_format, include_coaching_metrics=True, **prefetch_context)
        else:
            report, compliance = run_report(reportType=range, output_format=output_format, include_coaching_metrics=True)
    logs = buffer.getvalue()

    if isinstance(report, dict):
        context = report.get("context", {}) or {}
        markdown = report.get("markdown", "")
    else:
        context, markdown = {}, str(report)

    context["render_options"] = {"verbose_events": True, "include_all_events": True, "return_format": "markdown"}
    semantic_graph = report.get("semantic_graph", {})
    return report, compliance, logs, context, semantic_graph, markdown


# ============================================================
# 🛰️ ENDPOINTS
# ============================================================
@app.get("/")
def root():
    return {"message": "IntervalsICU GPTCoach Railway API 🧠 Running"}


@app.get("/run")
def run_audit(
    range: str = Query("weekly"),
    format: str = Query("markdown"),
    demo: bool = Query(False)
):
    if demo:
        return load_demo_response(range, reason="MANUAL_DEMO")
    try:
        report, compliance, logs, context, sg, markdown = _run_full_audit(range=range, output_format=format)
        if format in ("json", "semantic"):
            return JSONResponse({"status":"ok","report_type":range,"output_format":"semantic_json",
                "semantic_graph":sanitize(sg),"compliance":compliance,"logs":logs[:20000]})
        return JSONResponse({"status":"ok","report_type":range,"output_format":"markdown","markdown":markdown,"logs":logs[:20000]})
    except HTTPException as e:
        return JSONResponse(
            status_code=e.status_code,
            content={"status": "error", "message": e.detail}
        )

    except Exception as e:
        return error_response(e)


@app.post("/run")
async def run_audit_with_data(
    request: Request,
    demo: bool = Query(False)
):
    buffer = io.StringIO()
    if demo:
        return load_demo_response("weekly", reason="MANUAL_DEMO")
    try:
        raw = await request.body()
        if not raw:
            raise ValueError("Empty request body")
        data = json.loads(raw)
        report_range = data.get("range","weekly")
        fmt = data.get("format","markdown").lower()

        # ✅ NEW — capture start/end from the worker payload
        start = data.get("start")
        end = data.get("end")
        # ---------------------------------------------------------
        # 🚫 Future Start-Date Safeguard - COMMENTED OUT FOR TESTING OF EMPTY FUL DATA
        # ---------------------------------------------------------
#        try:
#            if start:
#                dt_start = pd.to_datetime(start).date()
#                today = datetime.utcnow().date()
#
#                if dt_start > today:
#                    return JSONResponse(
#                        status_code=400,
#                        content={
#                            "status": "error",
#                            "error_type": "FUTURE_DATE_INVALID",
#                            "severity": "hard",
#                            "message": "Cannot generate a report for a future start date.",
#                            "report_type": report_range,
#                            "semantic_graph": {},
#                            "compliance": {},
#                            "logs": ""
#                        }
#                    )
#        except Exception:
#            pass

        # normalize prefetched JSON into pandas-friendly context
        try:
            prefetch_context = normalize_prefetched_context(data)

        except AuditHalt as e:
            context = locals().get("prefetch_context")
            return handle_audit_halt(
                e,
                report_range,
                buffer=None,
                header=None,
                context=context
            )

        except HTTPException as e:

            sys.stderr.write("\n🚫 HTTPException triggered\n")
            sys.stderr.write(f"Status: {e.status_code}\n")
            sys.stderr.write(f"Detail: {e.detail}\n")
            sys.stderr.flush()

            return JSONResponse(
                status_code=e.status_code,
                content={
                    "status": "error",
                    "error_type": "STRAVA_API_RESTRICTED",
                    "severity": "hard",
                    "message": e.detail,
                    "report_type": report_range,
                    "semantic_graph": {},
                    "compliance": {},
                    "logs": ""
                }
            )

        # ============================================================
        # 🧪 DATA QUALITY EARLY EXIT (no full report build)
        # ============================================================
        if report_range == "data_quality":
            audit = data_quality_audit(prefetch_context)

            return JSONResponse({
                "status": "ok",
                "report_type": "data_quality",
                "output_format": "semantic_json",
                "semantic_graph": {
                    "meta": {
                        "report_type": "data_quality"
                    },
                    "data_quality": audit
                },
                "compliance": {},
                "logs": ""
            })

        # ---------------------------------------------------------
        # 🗓️ WINDOW RESOLUTION
        # ---------------------------------------------------------

        if report_range == "weekly":

            # If start provided → enforce 7 consecutive days
            if start:
                try:
                    dt_start = pd.to_datetime(start)
                    dt_end = dt_start + pd.Timedelta(days=6)
                    start = dt_start.strftime("%Y-%m-%d")
                    end   = dt_end.strftime("%Y-%m-%d")
                except Exception:
                    pass

            # If no start provided → derive most recent 7-day block from data
            else:
                df_daily = prefetch_context.get("df_daily")
                if df_daily is not None and not df_daily.empty:
                    dt_end = pd.to_datetime(df_daily["date"].max())
                    dt_start = dt_end - pd.Timedelta(days=6)
                    start = dt_start.strftime("%Y-%m-%d")
                    end   = dt_end.strftime("%Y-%m-%d")


        # ---------------------------------------------------------
        # 📦 Persist canonical period
        # ---------------------------------------------------------
        if start and end:
            prefetch_context["period"] = {
                "start": start,
                "end": end
            }

        # ✅ ALSO pass start/end in the legacy top-level keys (run_report consumes these)
        if start:
            prefetch_context["start"] = start
        if end:
            prefetch_context["end"] = end

        # ---------------------------------------------------------
        # 🧾 Header date range
        # ---------------------------------------------------------
        period = prefetch_context.get("period", {})
        resolved_start = period.get("start")
        resolved_end   = period.get("end")

        date_range = (
            f"{resolved_start} → {resolved_end}"
            if resolved_start and resolved_end
            else "not_passed"
        )

        light = prefetch_context.get("activities_light")
        full  = prefetch_context.get("activities_full")

        light_empty = (
            light is None or
            (isinstance(light, list) and len(light) == 0) or
            (isinstance(light, pd.DataFrame) and light.empty)
        )

        full_empty = (
            full is None or
            (isinstance(full, list) and len(full) == 0) or
            (isinstance(full, pd.DataFrame) and full.empty)
        )

        # ---------------------------------------------------------
        # LIGHT exists but FULL missing (only critical for weekly/season)
        # ---------------------------------------------------------
        if report_range in ("weekly", "season") and not light_empty and full_empty:

            last_date = None

            try:
                dates = [
                    pd.to_datetime(a.get("start_date_local"))
                    for a in light
                    if a.get("start_date_local")
                ]
                if dates:
                    last_date = max(dates)
            except Exception:
                pass

            if last_date is not None:
                last_date_str = last_date.strftime("%Y-%m-%d")
                suggested_start = (last_date - pd.Timedelta(days=7)).strftime("%Y-%m-%d")

                msg = (
                    f"No weekly period activities detected, detailed data could not be retrieved. "
                    f"Last activity I see is {last_date_str}. "
                    f"Create a weekly report for {suggested_start}."
                )
            else:
                msg = "Detailed activity data could not be retrieved."

            raise AuditHalt(
                msg,
                code="FULL_DATA_UNAVAILABLE",
                severity="soft"
            )

        # Abort only if NO activity data at all
        if light_empty and full_empty:
            if demo:
                return load_demo_response(
                    report_range,
                    reason="MANUAL_DEMO"
                )
            return load_demo_response(
                report_range,
                reason="NO_ACTIVITIES_RANGE"
            )

        # now run the unified audit (SAFE WRAPPED)
        try:
            with redirect_stdout(buffer):
                report, compliance = run_report(
                    reportType=report_range,
                    output_format=fmt,
                    include_coaching_metrics=True,
                    **prefetch_context
                )

        except AuditHalt as e:
            return handle_audit_halt(
                e,
                report_range,
                buffer=buffer,
                header=prefetch_context.get("report_header"),
                context=prefetch_context
            )

        except Exception:
            raise

        context = report.get("context", {}) if isinstance(report, dict) else {}

        period = context.get("period", {})

        resolved_start = period.get("start")
        resolved_end   = period.get("end")

        date_range = (
            f"{resolved_start} → {resolved_end}"
            if resolved_start and resolved_end
            else "not_passed"
        )

        report_header = {
            "athlete": context.get("athleteProfile", {}).get("name", "Unknown Athlete"),
            "report_type": report_range,
            "timezone": context.get("timezone", "Europe/Zurich"),
            "date_range": date_range,
        }

        logger.info(
            "[EXEC] report_header injected (post-run) → %s | report_type=%s | athlete=%s",
            report_header,
            report_range,
            report_header.get("athlete", "unknown")
        )

        logs = buffer.getvalue()

        if fmt in ("json","semantic"):

            semantic_graph = report.get("semantic_graph", {}) if isinstance(report, dict) else {}

            return JSONResponse({
                "status": "ok",
                "report_type": report_range,
                "report_header": report_header,
                "output_format": "semantic_json",
                "semantic_graph": sanitize(semantic_graph),
                "compliance": compliance,
                "logs": logs[-20000:],
            })

        return JSONResponse({
            "status": "ok",
            "report_type": report_range,
            "report_header": report_header,
            "output_format": "markdown",
            "markdown": report.get("markdown",""),
            "logs": logs[-20000:],
        })

    except AuditHalt as e:
        return handle_audit_halt(
            e,
            report_range,
            buffer=buffer,
            header=prefetch_context.get("report_header") if 'prefetch_context' in locals() else None,
            context=prefetch_context if 'prefetch_context' in locals() else None
        )

    except Exception as e:

        sys.stderr.write("\n🔥 UNHANDLED EXCEPTION IN /run\n")
        sys.stderr.write(traceback.format_exc())
        sys.stderr.flush()

        return error_response(e, buffer)



def error_response(e: Exception, buffer=None, status_code:int=500):

    trace = traceback.format_exc()

    # 🔥 FORCE log into Railway
    sys.stderr.write("\n===== 🚨 UNHANDLED EXCEPTION =====\n")
    sys.stderr.write(trace + "\n")
    sys.stderr.flush()

    return JSONResponse(
        status_code=status_code,
        content={
            "status": "error",
            "message": str(e),
            "exception_type": type(e).__name__,
            "trace": trace,
            "logs": buffer.getvalue()[-20000:] if buffer else None
        }
    )


# ============================================================
# 🧠 DEBUG ENDPOINT — Semantic JSON + Logs Only
# ============================================================
@app.post("/debug")
async def get_debug(request: Request):

    buffer = io.StringIO()

    try:

        raw = await request.body()

        if not raw:
            raise ValueError("Empty request body")

        data = json.loads(raw)

        report_range = data.get("range", "weekly")

        # Normalize prefetched dataset
        prefetch_context = normalize_prefetched_context(data)

        report, compliance, logs, context, sg, markdown = _run_full_audit(
            range=report_range,
            output_format="semantic",
            prefetch_context=prefetch_context
        )

        MAX_LOG = 250000
        log_tail = logs[-MAX_LOG:]

        return JSONResponse({
            "status": "ok",
            "report_type": report_range,
            "output_format": "semantic_json",
            "semantic_graph": sanitize(sg),
            "compliance": compliance,
            "logs": log_tail
        })

    except AuditHalt as e:
        return handle_audit_halt(
            e,
            report_range,
            buffer=buffer,
            header=None,
            context=prefetch_context if 'prefetch_context' in locals() else None
        )

    except Exception as e:
        return error_response(e, buffer)

def data_quality_audit(ctx: dict) -> dict:
    score = 0
    flags = []
    datasets = {}

    athlete = ctx.get("athlete", {})
    light = ctx.get("activities_light", []) or []
    full = ctx.get("activities_full", []) or []
    wellness = ctx.get("wellness", []) or []

    dq_flags = ctx.get("data_quality_flags", {})
    strava_stub_detected = dq_flags.get("strava_stub_detected", False)

    # --------------------------------------------------
    # Basic report header
    # --------------------------------------------------
    meta = ctx.get("meta", {})
    report_type = ctx.get("report_type", "data_quality")
    period = ctx.get("period") or meta.get("period")

    report_header = {
        "report_type": report_type,
        "framework": meta.get("framework", "URF"),
        "athlete_id": athlete.get("id"),
        "athlete_name": athlete.get("name"),
        "timezone": athlete.get("timezone"),
        "period": period,
        "generated_at": datetime.utcnow().isoformat() + "Z"
    }

    # --------------------------------------------------
    # Athlete
    # --------------------------------------------------
    athlete_valid = bool(athlete.get("id")) and bool(athlete.get("timezone"))
    if athlete_valid:
        score += 30
    else:
        flags.append("athlete_invalid")

    datasets["athlete"] = {
        "present": bool(athlete),
        "valid": athlete_valid,
        "issues": [] if athlete_valid else ["missing_id_or_timezone"]
    }

    # --------------------------------------------------
    # Light activities
    # --------------------------------------------------
    light_ok = isinstance(light, list) and len(light) > 0
    if light_ok:
        score += 20
    else:
        flags.append("light_missing")

    light_issues = []
    if not light_ok:
        light_issues.append("no_light_activities")
    if strava_stub_detected:
        light_issues.append("strava_stub_detected")

    datasets["light"] = {
        "present": light_ok,
        "count": len(light),
        "issues": light_issues
    }

    # --------------------------------------------------
    # Full activities
    # --------------------------------------------------
    full_ok = isinstance(full, list) and len(full) > 0
    if full_ok:
        score += 25
    else:
        flags.append("full_missing")

    datasets["full"] = {
        "present": full_ok,
        "count": len(full),
        "issues": [] if full_ok else ["no_full_activities"]
    }

    # --------------------------------------------------
    # Wellness
    # --------------------------------------------------
    wellness_ok = isinstance(wellness, list) and len(wellness) > 0
    if wellness_ok:
        score += 25
    else:
        flags.append("wellness_missing")

    datasets["wellness"] = {
        "present": wellness_ok,
        "count": len(wellness),
        "issues": [] if wellness_ok else ["missing_wellness_timeseries"]
    }

    # --------------------------------------------------
    # Global flags
    # --------------------------------------------------
    if strava_stub_detected:
        flags.append("strava_stub_detected")

    # --------------------------------------------------
    # Coverage metrics
    # --------------------------------------------------
    expected_days = ctx.get("window_days", 7)

    def unique_days(records):
        days = set()
        for r in records:
            d = r.get("date") or r.get("start_date_local")
            if d:
                days.add(str(d)[:10])
        return len(days)

    coverage = {
        "light_activity_days": unique_days(light),
        "full_activity_days": unique_days(full),
        "wellness_days": unique_days(wellness),
        "expected_days": expected_days
    }

    # --------------------------------------------------
    # Source breakdown
    # --------------------------------------------------
    source_counter = Counter()
    for act in full:
        src = act.get("source")
        if src:
            source_counter[src] += 1

    sources = dict(source_counter)

    # --------------------------------------------------
    # Sport distribution
    # --------------------------------------------------
    sport_counter = Counter()
    for act in full:
        t = act.get("type")
        if t:
            sport_counter[t] += 1

    sport_distribution = dict(sport_counter)

    # --------------------------------------------------
    # Field integrity
    # --------------------------------------------------
    power_count = 0
    hr_count = 0
    tss_count = 0

    for act in full:
        if act.get("icu_average_watts") or act.get("average_watts"):
            power_count += 1
        if act.get("average_heartrate"):
            hr_count += 1
        if act.get("icu_training_load"):
            tss_count += 1

    field_integrity = {
        "activities_total": len(full),
        "activities_with_power": power_count,
        "activities_with_hr": hr_count,
        "activities_with_tss": tss_count,
        "missing_power_count": len(full) - power_count,
        "missing_hr_count": len(full) - hr_count
    }

    # --------------------------------------------------
    # Timeline checks
    # --------------------------------------------------
    dates = []
    for act in full:
        d = act.get("start_date_local")
        if d:
            dates.append(str(d)[:10])

    timeline_checks = {
        "first_activity": min(dates) if dates else None,
        "last_activity": max(dates) if dates else None,
        "activity_days": len(set(dates)) if dates else 0
    }

    # --------------------------------------------------
    # State classification
    # --------------------------------------------------
    if score >= 80:
        state = "ok"
        trust_level = "high"
    elif score >= 50:
        state = "degraded"
        trust_level = "moderate"
    else:
        state = "invalid"
        trust_level = "low"

    # --------------------------------------------------
    # Recommended actions
    # --------------------------------------------------
    actions = []

    if "athlete_invalid" in flags:
        actions.append("Athlete profile incomplete — check account sync.")

    if "light_missing" in flags or "full_missing" in flags:
        actions.append("No activities detected — verify device connections.")

    if "wellness_missing" in flags:
        actions.append("No wellness data — enable HRV or resting HR tracking.")

    if strava_stub_detected:
        actions.append("Connect Garmin/Wahoo/Zwift directly or upload FIT files.")

    # --------------------------------------------------
    # Return
    # --------------------------------------------------
    return {
        "report_header": report_header,
        "score": score,
        "state": state,
        "trust_level": trust_level,
        "datasets": datasets,
        "flags": flags,
        "coverage": coverage,
        "sources": sources,
        "sport_distribution": sport_distribution,
        "field_integrity": field_integrity,
        "timeline_checks": timeline_checks,
        "actions": actions,
        "strava_stub_detected": strava_stub_detected
    }

def load_demo_response(report_range: str, reason: str, detail: str | None = None):

    sys.stderr.write("\n🧪 DEMO RESPONSE GENERATED\n")
    sys.stderr.write(f"Report: {report_range}\n")
    sys.stderr.write(f"Reason code: {reason}\n")
    sys.stderr.flush()

    demo_sg = copy.deepcopy(DEMO_WEEKLY)

    if report_range != "weekly":
        demo_sg["meta"]["report_type"] = report_range

    REASON_MAP = {
        "OAUTH_NOT_CONFIGURED": "Account not connected." + " See www.montis.net/setup.html",
        "ATHLETE_PROFILE_INVALID": "Invalid athlete profile."  + " See www.montis.net/setup.html",
        "NO_ACTIVITIES_RANGE": "No activities found in requested period." + " See www.montis.net/setup.html",
        "FULL_DATA_UNAVAILABLE": "Detailed activity data unavailable."  + " See www.montis.net/setup.html",
        "FULL_FETCH_FAILED": "Failed to retrieve detailed activity data."  + " See www.montis.net/setup.html",
        "LIGHT_ONLY_CONTEXT": "Only summary activity data available."  + " See www.montis.net/setup.html",
        "STRAVA_API_RESTRICTED": "Strava API access restricted."  + " See www.montis.net/setup.html",
        "MANUAL_DEMO": "Manual demo mode enabled." + " See www.montis.net/setup.html"
    }

    readable_reason = detail or REASON_MAP.get(
        reason,
        "Demo fallback. See www.montis.net/setup.html"
    )

    # ✅ Canonical location — root of semantic_graph
    existing = demo_sg.get("renderer_instructions", "")

    demo_block = f"""

DEMO MODE NOTICE:
- This is a demonstration report.
- Triggered because: {readable_reason}.
- Real athlete data was unavailable.
- Render normally using the provided semantic data.
"""

    if "DEMO MODE NOTICE" not in existing:
        demo_sg["renderer_instructions"] = existing.rstrip() + demo_block

    # Flags stay in meta
    meta = demo_sg.setdefault("meta", {})
    meta["demo"] = True
    meta["demo_reason"] = readable_reason
    meta["demo_code"] = reason
    meta["demo_mode"] = "fallback"

    safe_payload = {
        "status": "demo",
        "report_type": report_range,
        "report_header": meta.get("report_header"),
        "output_format": "semantic_json",
        "semantic_graph": demo_sg,
        "compliance": {},
        "logs": ""
    }

    safe_json = json.loads(
        json.dumps(safe_payload, ensure_ascii=False)
        .encode("utf-8", "ignore")
        .decode("utf-8")
    )

    return JSONResponse(safe_json)

def handle_audit_halt(e, report_range, buffer=None, header=None, context=None):

    severity = getattr(e, "severity", "hard")
    code = getattr(e, "code", None)

    athlete_name = None
    athlete_id = None
    period_str = None

    if context:
        athlete = context.get("athlete") or context.get("athleteProfile") or {}
        athlete_name = athlete.get("name")
        athlete_id = athlete.get("id")

        period = context.get("period", {})
        start = period.get("start")
        end = period.get("end")

        if start and end:
            period_str = f"{start} → {end}"

    # 🔥 Always log to Railway
    sys.stderr.write("\n🛑 AUDIT HALTED\n")
    sys.stderr.write(f"Code: {code}\n")
    sys.stderr.write(f"Severity: {severity}\n")
    sys.stderr.write(f"Report: {report_range}\n")

    if athlete_name or athlete_id:
        sys.stderr.write(f"Athlete: {athlete_name} ({athlete_id})\n")

    if period_str:
        sys.stderr.write(f"Period: {period_str}\n")

    sys.stderr.write(str(e) + "\n")
    sys.stderr.flush()
    logger.info(
        "[HALT] report_type=%s athlete=%s code=%s message=%s",
        report_range,
        athlete_name,
        code,
        str(e)
    )

    # 🟡 Soft → demo
    if severity == "soft":
        return load_demo_response(
            report_range,
            reason=code,
            detail=str(e)
        )

    # 🔴 Hard but demo-allowed (auth cases)
    if code in ["OAUTH_NOT_CONFIGURED", "ATHLETE_PROFILE_INVALID"]:
        demo = load_demo_response(report_range, reason=code)
        demo.status_code = 401
        return demo

    # 🔴 Real hard halt
    halt_payload = e.to_dict()

    return JSONResponse({
        **halt_payload,
        "report_type": report_range,
        "report_header": header,
        "semantic_graph": {},
        "compliance": {},
        "logs": buffer.getvalue()[-20000:] if buffer else ""
    })
