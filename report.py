#!/usr/bin/env python3
"""
Unified URF v5.1 Report Runner
==============================

Command-line tool for generating and retrieving Montis URF v5.1 training reports.

The runner can operate in two modes:

• Local generation (direct Python execution via audit_core)
• Remote generation (prefetched dataset via Cloudflare Worker → Railway)

It supports optional GPT rendering, debug execution traces, synthetic dataset
testing, and custom reporting windows.


───────────────────────────────────────────────
SYSTEM ARCHITECTURE
───────────────────────────────────────────────

Local mode
    CLI → audit_core.run_report()

Remote mode
    CLI → Cloudflare Worker → Railway /run → audit_core pipeline

The Worker acts as a unified API gateway.


───────────────────────────────────────────────
ENDPOINTS
───────────────────────────────────────────────

Railway Production
https://intervalsicugptcoach-public-production.up.railway.app

Railway Staging
https://intervalsicugptcoach-public-staging.up.railway.app

Cloudflare Worker (API Gateway)
https://intervalsicugptcoach.clive-a5a.workers.dev

Cloudflare Worker (Staging)
https://intervalsicugptcoach-staging.clive-a5a.workers.dev


───────────────────────────────────────────────
WORKER ROUTES
───────────────────────────────────────────────

/run_weekly
    7-day training load and fatigue analysis.

/run_season
    Long-term performance progression and adaptation trends.

/run_wellness
    Physiological recovery indicators (HRV, RHR, fatigue, sleep).

/run_summary
    High-level overview of athlete state and key metrics.

/run_data_quality
    Dataset integrity audit without building a full report.


───────────────────────────────────────────────
QUERY PARAMETERS (Worker)
───────────────────────────────────────────────

render=gpt
    Enables GPT Markdown rendering.

    Response:
    {
        "markdown": "...",
        "semantic_graph": {...},
        "logs": "...",
        "status": "ok"
    }

debug=true
    Executes the debug pipeline and returns full execution logs.

    Response:
    {
        "status": "ok",
        "report_type": "...",
        "semantic_graph": {...},
        "compliance": {...},
        "logs": "..."
    }

start=YYYY-MM-DD
end=YYYY-MM-DD
    Overrides the reporting window.

    Supported reports:
        weekly
        summary

    Weekly reports automatically expand the window to 7 days.

test=strava*
    Injects synthetic STRAVA-only dataset scenarios for pipeline testing.


───────────────────────────────────────────────
CLI MODES
───────────────────────────────────────────────

LOCAL MODE
    Runs the full pipeline directly in Python.

    Output files:
        report_<range>_prod_semantic.json
        report_<range>_prod_markdown.md


PREFETCH MODE (REMOTE)
    Fetches a prefetched dataset through the Worker.

    Output files:
        report_<range>_prefetch_prod_semantic.json

    With GPT rendering:
        report_<range>_prefetch_prod_gpt.md
        report_<range>_prefetch_prod_semantic.json


DEBUG MODE
    Fetches the debug execution trace from the Worker.

    Output files:
        report_<range>_<env>_debug.json
        report_<range>_<env>_debug.log


───────────────────────────────────────────────
CLI USAGE EXAMPLES
───────────────────────────────────────────────

Local semantic report
python report.py --range weekly


Local markdown report
python report.py --range weekly --format markdown


Remote report (Worker → Railway)
python report.py --range weekly --prefetch


Remote staging report
python report.py --range weekly --prefetch --staging


Remote GPT-rendered report
python report.py --range season --prefetch --gpt


Custom window (summary)
python report.py --range summary --start 2025-01-01 --end 2025-12-31


Weekly window override
python report.py --range weekly --start 2026-03-01


Debug execution trace
python report.py --range weekly --debug --staging


Data quality audit
python report.py --range data_quality --prefetch


───────────────────────────────────────────────
TEST SCENARIOS
───────────────────────────────────────────────

Synthetic STRAVA-only datasets can be simulated using the CLI flag
`--strava-test`.

| CLI flag             | Worker param   | Scenario                                  | Expected behaviour |
|----------------------|---------------|--------------------------------------------|-------------------|
| --strava-test stub   | test=strava   | All activities are STRAVA API stub rows    | Hard stop: STRAVA_API_RESTRICTED |
| --strava-test 1      | test=strava1  | Only light activities present              | Soft halt: insufficient detailed data |
| --strava-test 2      | test=strava2  | Full dataset empty after filtering         | Soft halt: no usable activities |
| --strava-test 3      | test=strava3  | Activities missing key metrics             | Report runs with degraded metrics |
| --strava-test 4      | test=strava4  | Partial wellness or athlete metadata       | Report runs with degraded data quality |
| --strava-test 5      | test=strava5  | Mixed valid and stub activities            | Report runs with warnings |
| --strava-test demo   | test=demo     | Demo dataset                               | Demo report generated |


───────────────────────────────────────────────
OUTPUT LOCATION
───────────────────────────────────────────────

All reports are written to:

./reports/

Debug runs generate two files:

    semantic report
    execution log


───────────────────────────────────────────────
NOTES
───────────────────────────────────────────────

• Local semantic reports never use GPT.

• Prefetch + GPT writes both Markdown and semantic JSON.

• Debug mode captures full pipeline execution logs (Tier-0 → Tier-3).

• The CLI runner doubles as an integration harness for Worker
  and Railway pipelines.
"""


import io
import os
import sys
import json
import argparse
import requests
import webbrowser
from datetime import datetime
from contextlib import redirect_stdout
from pathlib import Path

print("ARGV:", sys.argv)
# Import project modules
sys.path.append(os.path.abspath(os.path.dirname(__file__)))
sys.path.append(os.path.abspath(os.path.dirname(os.path.dirname(__file__))))
from audit_core.report_controller import run_report
from audit_core.utils import debug
from audit_core.utils import set_time_context

sys.stdout.reconfigure(encoding="utf-8")

#---------------------------------------------
#  Resolve correct Cloudflare Worker base URL.
#----------------------------------------------
def get_worker_base(staging=False):

    if staging:
        return "https://intervalsicugptcoach-staging.clive-a5a.workers.dev"
    return "https://intervalsicugptcoach.clive-a5a.workers.dev"

#---------------------------------------------
#  OPEN report helper
#----------------------------------------------

def open_report(path):
    if os.getenv("OPEN_REPORT", "1") == "1":
        try:
            webbrowser.open(Path(path).resolve().as_uri())
        except Exception:
            pass

# ─────────────────────────────────────────────
# DEBUG REPORTS
# ─────────────────────────────────────────────
def fetch_debug_report(report_type, staging=False, prefetch=False):
    """
    Fetch debug report via Cloudflare Worker (prefetch + debug routing).
    Splits semantic report and debug logs into separate files.
    """

    worker_base = get_worker_base(staging)
    url = f"{worker_base}/run_{report_type}?debug=true&format=semantic"

    headers = {
        "Authorization": f"Bearer {os.getenv('ICU_OAUTH', '')}",
        "X-Montis-Internal": os.getenv("MONTIS_INTERNAL_KEY"),
        "User-Agent": "IntervalsGPTCoachLocal/1.0"
    }

    env = "staging" if staging else "prod"

    print(f"[DEBUG] env={env} report={report_type}")
    print(f"[DEBUG] → {url}")

    resp = requests.get(url, headers=headers, timeout=120)
    resp.raise_for_status()

    data = resp.json()

    Path("reports").mkdir(exist_ok=True)

    # ------------------------------------------------
    # Extract components
    # ------------------------------------------------
    logs = data.get("logs", "")
    semantic = data.get("semantic_graph", {})

    report_payload = {
        "status": data.get("status"),
        "report_type": data.get("report_type"),
        "semantic_graph": semantic,
        "compliance": data.get("compliance", {})
    }

  # ------------------------------------------------
    # Save semantic report
    # ------------------------------------------------
    mode = "prefetch" if prefetch else "local"

    json_name = f"report_{report_type}_{mode}_{env}_debug.json"
    json_path = Path("reports") / json_name

    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(report_payload, f, indent=2)

    print(f"[DEBUG] ✅ Semantic report saved → {json_name}")
    open_report(json_path)

    # ------------------------------------------------
    # Save logs separately
    # ------------------------------------------------
    log_name = f"report_{report_type}_{mode}_{env}_debug.log"
    log_path = Path("reports") / log_name

    with open(log_path, "w", encoding="utf-8") as f:
        f.write(logs)

    print(f"[DEBUG] 📜 Logs saved → {log_name}")
    open_report(log_path)

    if logs:
        print(f"[DEBUG] 📜 Logs captured: {len(logs.splitlines())} lines")

    return report_payload


# ─────────────────────────────────────────────
# PREFETCH HELPER — Cloudflare Worker Schema
# ─────────────────────────────────────────────
def fetch_remote_report(
    report_type,
    staging=False,
    gpt=False,
    provider=None,
    model=None,
    start=None,
    end=None,
    strava_test=False
):
    """
    Fetch a URF report (semantic+markdown) from Cloudflare Worker.
    If GPT rendering is enabled (?render=gpt), the Worker now returns both
    markdown and semantic JSON in a single JSON envelope.
    """
    worker_base = get_worker_base(staging)
    base = f"{worker_base}/run_{report_type}"
    # Build query params
    params = []
    if gpt:
        params.append("render=gpt")

        if provider:
            params.append(f"provider={provider}")

        if model:
            params.append(f"model={model}")
    if start:
        params.append(f"start={start}")
    if end:
        params.append(f"end={end}")
    if strava_test:
        # Accept: stub, 1–5
        if strava_test == "stub":
            params.append("test=strava-stub")
        elif strava_test == "demo":
            params.append("test=demo")
        elif strava_test in ["1", "2", "3", "4", "5"]:
            params.append(f"test=strava{strava_test}")
        else:
            raise ValueError(
                "Invalid --strava-test value. Use: stub, demo, 1,2,3,4,5"
            )


    query = "&".join(params)
    url = f"{base}?{query}" if query else base

    headers = {
        "Authorization": f"Bearer {os.getenv('ICU_OAUTH', '')}",
        "X-Montis-Internal": os.getenv("MONTIS_INTERNAL_KEY"),
        "User-Agent": "IntervalsGPTCoachLocal/1.0"
    }

    env = "staging" if staging else "prod"
    print(f"[REMOTE] env={env} report={report_type} gpt={gpt}")
    print(f"[REMOTE] → {url}")

    resp = requests.get(url, headers=headers, timeout=120)

    print(f"[REMOTE] HTTP {resp.status_code}")

    # Only crash for true server failures
    if resp.status_code >= 500:
        resp.raise_for_status()

    content_type = resp.headers.get("content-type", "")

    # Try to parse JSON if possible
    try:
        data = resp.json()
    except Exception:
        # Surface Worker error text instead of crashing
        text = resp.text
        print("[REMOTE] Non-JSON response from Worker:")
        print(text)
        return {"status": "error", "raw": text}

    Path("reports").mkdir(exist_ok=True)
    env_tag = "staging" if staging else "prod"

    content_type = resp.headers.get("content-type", "")

    # 🔥 Handle unified JSON payload (markdown + semantic)
    if "application/json" in content_type:

        data = resp.json()
        markdown = data.get("markdown")
        semantic = data.get("semantic_graph")

        mode = "prefetch"
        env_tag = "staging" if staging else "prod"

        # ------------------------------------------------
        # Write semantic JSON (always if present)
        # ------------------------------------------------
        if semantic:

            json_out = f"report_{report_type}_{mode}_{env_tag}_semantic.json"
            json_path = Path("reports") / json_out

            json_path.write_text(
                json.dumps(semantic, indent=2),
                encoding="utf-8"
            )

            print(f"[REMOTE] ✅ Semantic JSON saved → {json_out}")
            open_report(json_path)

        # ------------------------------------------------
        # Write markdown if GPT requested
        # ------------------------------------------------
        if gpt:

            md_out = f"report_{report_type}_{mode}_{env}_gpt_{provider}_{model}.md"
            md_path = Path("reports") / md_out

            if markdown:
                md_path.write_text(markdown, encoding="utf-8")
                print(f"[REMOTE] ✅ Markdown saved → {md_out}")
            else:
                md_path.write_text(
                    "# LLM render unavailable\n\n"
                    "The worker did not return markdown.\n"
                    "Check semantic JSON for details.",
                    encoding="utf-8"
                )
                print(f"[REMOTE] ⚠️ Markdown missing — placeholder written → {md_out}")

            open_report(md_path)

        return data

    # Legacy markdown-only fallback
    if "text/markdown" in content_type:
        text = resp.text
        md_out = f"report_{report_type}_prefetch_{env_tag}_gpt.md"
        Path(f"reports/{md_out}").write_text(text, encoding="utf-8")
        print(f"[REMOTE] ✅ Markdown saved (legacy) → {md_out}")
        return {"markdown": text, "status": resp.status_code}

    # Default JSON flow (no GPT)
    data = resp.json()
    json_out = f"report_{report_type}_prefetch_{env_tag}_semantic.json"
    Path(f"reports/{json_out}").write_text(json.dumps(data, indent=2), encoding="utf-8")
    print(f"[REMOTE] ✅ Semantic JSON saved → {json_out}")
    return data



def generate_full_report(
    report_type="weekly",
    output_path=None,
    output_format="markdown",
    prefetch=False,
    staging=False,
    start=None,
    end=None,
    gpt=False,
    provider=None,
    model=None,
    strava_test=False,
    debug_mode=False
):
    """Run report and capture logs and output into one file."""
    buffer = io.StringIO()
    logs = ""
    os.environ["REPORT_TYPE"] = report_type.lower()
    Path("reports").mkdir(parents=True, exist_ok=True)

    # ✅ Always respect custom date range flags (even if unused by remote)
    if start and end:
        print(f"[CLI] ⏱️ Custom date range override detected: {start} → {end}")
    else:
        print("[CLI] Using automatic window selection (based on report type).")

    # ============================================================
    # 🌐 PREFETCH MODE — via Cloudflare Worker
    # ============================================================
    if prefetch:
        print(f"[PREFETCH] Using Worker prehydrated report (staging={staging}, gpt={gpt})")
        data = fetch_remote_report(
            report_type,
            staging=staging,
            gpt=gpt,
            provider=provider,
            model=model,
            start=start,
            end=end,
            strava_test=strava_test
        )

        # ✅ GPT-handled — Worker already wrote markdown + semantic
        if gpt:
            print("[GPT] ✅ Worker already saved Markdown + Semantic JSON — exiting early.")
            return None  # 🚫 This now safely exits generate_full_report()

        # If Worker returned a block/error, preserve it exactly
        if data.get("status") != "ok":
            full_output = data
        else:
            log_output = data.get("logs", "")
            semantic = data.get("semantic_graph", {})
            full_output = {
                "status": data.get("status", "ok"),
                "message": data.get("message", f"{report_type.title()} report (prefetched)"),
                "error_type": data.get("error_type"),
                "severity": data.get("severity"),
                "semantic_graph": semantic,
                "logs": log_output,
            }

    # ============================================================
    # 💻 LOCAL MODE — Run local
    # ============================================================
    else:
        debug({}, f"🧭 Generating {report_type.title()} Report (local mode)")

        # 🧩 Inject optional custom date range
        context = {}
        if start and end:
            debug(context, f"[CLI] ⏱️ Custom date range provided: {start} → {end}")
            context["start"] = start
            context["end"] = end
        else:
            debug(context, "[CLI] Using default auto-window (today-365 for summary, etc.)")

        if debug_mode:
            with redirect_stdout(buffer):
                result = run_report(
                    reportType=report_type,
                    include_coaching_metrics=True,
                    output_format=output_format,
                    **context,
                )
            logs = buffer.getvalue()
        else:
            result = run_report(
                reportType=report_type,
                include_coaching_metrics=True,
                output_format=output_format,
                **context,
            )
            logs = ""
        raw_logs = logs.splitlines()
        skip_terms = ["snapshot", "trace", "json", "context", "activities_full", "DataFrame"]
        log_output = "\n".join(
            [line for line in raw_logs if not any(term in line.lower() for term in skip_terms)]
        ).strip()

        # Capture report + dataset summary
        summary = None
        if isinstance(result, tuple):
            report, summary = result
        else:
            report = result

        if isinstance(report, dict):

            if output_format == "semantic":
                semantic_output = report.get("semantic_graph", {})

                full_output = {
                    "status": "ok",
                    "message": f"{report_type.title()} report generated",
                    "semantic_graph": semantic_output,
                    "summary": summary,
                }

                log_file_output = log_output

            else:
                md_output = report.get("markdown", "")

                full_output = (
                    f"# 🧾 {report_type.title()} Audit Report\n\n"
                    f"🗓️ Date Range: {start} → {end}\n\n" if start and end else ""
                ) + (
                    "## Execution Logs\n\n"
                    "```\n" + log_output + "\n```\n\n"
                    "## Rendered Markdown Report\n\n"
                    + md_output.strip()
                )

        else:
            full_output = {"markdown": str(report), "logs": log_output}


    # ============================================================
    # 💾 FILE WRITING (Distinct Names, No Collisions)
    # ============================================================
    if prefetch and gpt:
        print("[SAFEGUARD] 🛑 Prefetch GPT detected — skipping local file writing entirely.")
        return None  # 🧱 Hard stop, prevents duplicate writes

    mode = "prefetch" if prefetch else "local"
    env_tag = "staging" if staging else "prod"
    gpt_tag = "_gpt" if gpt else ""

    base_name = f"report_{report_type}_{mode}_{env_tag}{gpt_tag}_{output_format}"


    # ============================================================
    # 💾 WRITE LOCAL OUTPUT (Semantic or Markdown)
    # ============================================================
    reports_dir = Path("reports")
    reports_dir.mkdir(parents=True, exist_ok=True)

    if output_format == "semantic":
        out_path = reports_dir / f"{base_name}.json"

        # --- Safe JSON encoder for Pandas, NumPy, and datetime objects ---
        def json_default(obj):
            import pandas as pd, datetime, numpy as np
            if isinstance(obj, (pd.Timestamp, datetime.date, datetime.datetime)):
                return obj.isoformat()
            if isinstance(obj, (np.int64, np.int32)):
                return int(obj)
            if isinstance(obj, (np.float32, np.float64)):
                return float(obj)
            return str(obj)

        with open(out_path, "w", encoding="utf-8") as f:
            json.dump(full_output, f, indent=2, default=json_default)

        print(f"[LOCAL] ✅ Saved semantic JSON → {out_path}")

        # Write debug logs (local debug mode)
        if debug_mode and logs:

            log_path = reports_dir / f"report_{report_type}_local_{env_tag}_debug.log"

            with open(log_path, "w", encoding="utf-8") as f:
                f.write(logs)

            print(f"[DEBUG] 📜 Logs saved → {log_path.name}")
            print(f"[DEBUG] 📜 Logs captured: {len(logs.splitlines())} lines")

            open_report(log_path)

        if debug and logs:
            with open(log_path, "w", encoding="utf-8") as f:
                f.write(logs)

        if os.getenv("OPEN_REPORT", "1") == "1":
            webbrowser.open(out_path.resolve().as_uri())

    else:
        out_path = reports_dir / f"{base_name}.md"
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(full_output)
        print(f"[LOCAL] ✅ Saved markdown report → {out_path}")

        if os.getenv("OPEN_REPORT", "1") == "1":
            webbrowser.open(out_path.resolve().as_uri())

    return full_output

# ─────────────────────────────────────────────
# CLI ENTRY POINT
# ─────────────────────────────────────────────
def main():
    parser = argparse.ArgumentParser(description="Generate audit reports for different data ranges.")
    parser.add_argument("--range", type=str.lower,
                        choices=["weekly", "season", "wellness", "summary", "data_quality"],
                        default="weekly")
    parser.add_argument("--output", type=str, default=None)
    parser.add_argument("--format", type=str.lower,
                        choices=["markdown", "semantic"],
                        default="semantic",
                        help="Output format (default: semantic)")
    parser.add_argument("--prefetch", action="store_true",
                        help="Use prehydrated dataset from Railway proxy (via Worker)")
    parser.add_argument("--staging", action="store_true",
                        help="Request staging environment (Worker will decide access)")
    parser.add_argument("--start", type=str, help="Custom start date (YYYY-MM-DD)")
    parser.add_argument("--end", type=str, help="Custom end date (YYYY-MM-DD)")
    parser.add_argument("--gpt", action="store_true",
                        help="Request GPT-rendered report from Cloudflare Worker (adds ?render=gpt)")
    parser.add_argument("--provider", type=str,
                        choices=["openai","anthropic","google"],
                        help="LLM provider")
    parser.add_argument("--model", type=str,
                        help="LLM model")    
    parser.add_argument("--debug", action="store_true",
                        help="Run any report type in debug mode (via Railway /debug endpoint if available)")
    parser.add_argument(
        "--strava-test",
        type=str,
        choices=["stub", "demo", "1", "2", "3", "4", "5"],
        help=(
            "Simulate Strava-only scenarios:\n"
            "  stub → all activities are STRAVA API stubs (hard stop)\n"
            "  1    → light-only dataset, no full activities\n"
            "  2    → full dataset empty after filtering\n"
            "  3    → activities present but missing key metrics\n"
            "  4    → partial wellness or athlete metadata\n"
            "  5    → mixed valid + stub activities (degraded state)"
            "  demo → demo"
        )
    )

    args = parser.parse_args()
    # 🧠 Debug mode shortcut — directly fetch from /debug and exit
    if args.debug and args.prefetch:

        os.environ["PREFETCH_MODE"] = "1"

        print(f"[CLI] 🧠 Prefetch debug mode for '{args.range}' (staging={args.staging})")

        fetch_debug_report(args.range, staging=args.staging, prefetch=args.prefetch)

        return

    # 🧩 Otherwise, run the normal flow
    generate_full_report(
        report_type=args.range,
        output_path=args.output,
        output_format=args.format,
        prefetch=args.prefetch,
        staging=args.staging,
        start=args.start,
        end=args.end,
        gpt=args.gpt,
        provider=args.provider,
        model=args.model,
        strava_test=args.strava_test,
        debug_mode=args.debug
    )



if __name__ == "__main__":
    main()
