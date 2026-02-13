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


sys.path.append(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), "audit_core"))

from audit_core.report_controller import run_report
from audit_core.utils import debug
from semantic_json_builder import build_semantic_json
from audit_core.tier0_pre_audit import expand_zones


print("[BOOT] 🚀 Starting IntervalsICU GPTCoach Railway API")
icuoauth = os.getenv("ICU_OAUTH")
if icuoauth:
    print("[BOOT] ICU_OAUTH detected:", icuoauth[:10], "...")
else:
    print("[BOOT-WARN] ICU_OAUTH missing — Intervals.icu calls may fail")

app = FastAPI(title="IntervalsICU GPTCoach Railway API", version="2.0")


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
            return "<circular>"
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

        # 🔒 CONTRACT INVARIANT — athlete must have an id
        if not isinstance(athlete, dict):
            raise AuditHalt(
                "Athlete profile missing or invalid.",
                code="ATHLETE_PROFILE_INVALID",
                severity="hard"
            )

        if "id" not in athlete:
            raise AuditHalt(
                "Athlete profile missing ID.",
                code="ATHLETE_ID_MISSING",
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

        # Derived Tier-0 equivalents
        context["df_light"]  = df_light
        context["df_master"] = df_full
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
                context["df_daily"] = df_daily
                debug(context, f"[NORM] built df_daily {len(df_daily)} days")
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
    semantic_graph = build_semantic_json(context)
    return report, compliance, logs, context, semantic_graph, markdown


# ============================================================
# 🛰️ ENDPOINTS
# ============================================================
@app.get("/")
def root():
    return {"message": "IntervalsICU GPTCoach Railway API 🧠 Running"}


@app.get("/run")
def run_audit(range: str = Query("weekly"), format: str = Query("markdown")):
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
async def run_audit_with_data(request: Request):
    buffer = io.StringIO()
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

        # normalize prefetched JSON into pandas-friendly context
        try:
            prefetch_context = normalize_prefetched_context(data)
        except HTTPException as e:
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

        # ✅ NEW — inject start/end into context for Tier-0 summary to work
        if start and end:
            prefetch_context["start"] = start
            prefetch_context["end"] = end
            print(f"[STAGING] Injected start/end into prefetch_context: {start} → {end}")

        # --- EARLY HEADER INJECTION (pre-run safety) ---
        athlete_profile = prefetch_context.get("athleteProfile", {})

        resolved_start = start or prefetch_context.get("start")
        resolved_end   = end   or prefetch_context.get("end")

        prefetch_context["report_header"] = {
            "athlete": athlete_profile.get("name", "Unknown Athlete"),
            "discipline": athlete_profile.get("discipline", "cycling"),
            "report_type": report_range,
            "framework": "Unified_Reporting_Framework_v5.1",
            "timezone": athlete_profile.get("timezone", "Europe/Zurich"),
            "date_range": f"{resolved_start} → {resolved_end}" if resolved_start and resolved_end else "unknown",
        }

        sys.stderr.write(
            f"[EXEC] report_header injected (pre-run) → {prefetch_context['report_header']} "
            f"| report_type={report_range} "
            f"| athlete={prefetch_context['report_header'].get('athlete','unknown')}\n"
        )
        sys.stderr.flush()


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

        # Abort only if NO activity data at all
        if light_empty and full_empty:
            raise AuditHalt(
                "No activities found in the requested date range.",
                code="NO_ACTIVITIES_RANGE",
                severity="soft"
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
        except Exception as e:

            if isinstance(e, AuditHalt):
                sys.stderr.write("\n🛑 AUDIT HALTED (safe intercept)\n")
                sys.stderr.write(str(e) + "\n")
                sys.stderr.flush()

                halt_payload = e.to_dict()

                return JSONResponse({
                    **halt_payload,
                    "report_type": report_range,
                    "report_header": prefetch_context.get("report_header") if 'prefetch_context' in locals() else None,
                    "semantic_graph": {},
                    "compliance": {},
                    "logs": buffer.getvalue()[-20000:]
                })

            raise  # re-raise unexpected errors


        logs = buffer.getvalue()
        if fmt in ("json","semantic"):
            context = report.get("context",{}) if isinstance(report,dict) else {}
            return JSONResponse({
                "status": "ok",
                "report_type": report_range,
                "report_header": prefetch_context.get("report_header") if 'prefetch_context' in locals() else None,
                "output_format": "semantic_json",
                "semantic_graph": sanitize(build_semantic_json(context)),
                "compliance": compliance,
                "logs": logs[-20000:],
            })

        return JSONResponse({
            "status": "ok",
            "report_type": report_range,
            "report_header": prefetch_context.get("report_header") if 'prefetch_context' in locals() else None,
            "output_format": "markdown",
            "markdown": report.get("markdown",""),
            "logs": logs[-20000:],
        })

    except Exception as e:

        import traceback

        if isinstance(e, AuditHalt):
            sys.stderr.write("\n🛑 AUDIT HALTED (outer intercept)\n")
            sys.stderr.write(str(e) + "\n")
            sys.stderr.flush()

            halt_payload = e.to_dict()

            return JSONResponse({
                **halt_payload,
                "report_type": report_range,
                "report_header": prefetch_context.get("report_header") if 'prefetch_context' in locals() else None,
                "semantic_graph": {},
                "compliance": {},
                "logs": buffer.getvalue()[-20000:]
            })

        sys.stderr.write("\n🔥 UNHANDLED EXCEPTION IN /run\n")
        sys.stderr.write(traceback.format_exc())
        sys.stderr.flush()

        return error_response(e, buffer)



def error_response(e: Exception, buffer=None, status_code:int=500):
    import traceback

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


@app.get("/semantic")
def get_semantic(range: str = Query("weekly")):
    _, compliance, logs, _, sg, _ = _run_full_audit(range=range)
    return JSONResponse({"status":"ok","report_type":range,"output_format":"semantic_json","semantic_graph":sanitize(sg),"compliance":compliance,"logs":logs[:20000]})


@app.get("/metrics")
def get_metrics(range: str = Query("weekly")):
    _, compliance, logs, _, sg, _ = _run_full_audit(range=range)
    return JSONResponse({"status":"ok","report_type":range,
        "metrics":sanitize(sg.get("metrics",{})),
        "extended_metrics":sanitize(sg.get("extended_metrics",{})),
        "trend_metrics":sanitize(sg.get("trend_metrics",{})),
        "adaptation_metrics":sanitize(sg.get("adaptation_metrics",{})),
        "correlation_metrics":sanitize(sg.get("correlation_metrics",{})),
        "compliance":compliance,"logs":logs[:20000]})


@app.get("/phases")
def get_phases(range: str = Query("weekly")):
    _, compliance, logs, _, sg, _ = _run_full_audit(range=range)
    return JSONResponse({"status":"ok","report_type":range,
        "phases":sanitize(sg.get("phases",[])),"actions":sanitize(sg.get("actions",[])),
        "compliance":compliance,"logs":logs[:20000]})


@app.get("/compare")
def compare_periods(range: str = Query("weekly")):
    _, compliance, logs, _, sg, _ = _run_full_audit(range=range)
    return JSONResponse({"status":"ok","report_type":range,
        "trend_metrics":sanitize(sg.get("trend_metrics",{})),"core_metrics":sanitize(sg.get("metrics",{})),
        "compliance":compliance,"logs":logs[:20000]})


@app.get("/insights")
def get_insights(range: str = Query("weekly")):
    _, compliance, logs, _, sg, _ = _run_full_audit(range=range)
    return JSONResponse({"status":"ok","report_type":range,"insights":sanitize(sg.get("insight_view",{})),
        "compliance":compliance,"logs":logs[:20000]})

# ============================================================
# 🧠 DEBUG ENDPOINT — Semantic JSON + Logs Only
# ============================================================
@app.get("/debug")
def get_debug(
    range: str = Query("weekly", description="Report type: weekly, season, wellness, summary"),
    format: str = Query("semantic", description="Output format: semantic (ignored for now)")
):
    """
    Debug endpoint for any report type.
    Returns semantic JSON + captured logs.
    Compatible with both local and staging use.
    """
    try:
        report, compliance, logs, context, sg, markdown = _run_full_audit(
            range=range,
            output_format="semantic"
        )

        return JSONResponse({
            "status": "ok",
            "report_type": range,
            "output_format": "semantic_json",
            "semantic_graph": sanitize(sg),
            "logs": logs[-20000:],
        })

    except Exception as e:
        return error_response(e)

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
