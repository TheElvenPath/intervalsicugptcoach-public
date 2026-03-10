#!/usr/bin/env python3
"""
Unified URF v5.1 Report Runner
==============================

Generates and fetches audit reports for:
  • weekly
  • season
  • wellness
  • summary

Supports both:
  🔹 Local (direct) Railway-backed generation
  🔹 Remote (prefetched) Worker-based generation
  🔹 Optional GPT-rendered Markdown (via Cloudflare Worker + OpenAI)

───────────────────────────────────────────────
📡 ENDPOINTS
───────────────────────────────────────────────
• Railway Production:
    https://intervalsicugptcoach-public-production.up.railway.app

• Railway Staging:
    https://intervalsicugptcoach-public-staging.up.railway.app

• Cloudflare Worker (Unified API Gateway):
    https://intervalsicugptcoach.clive-a5a.workers.dev

───────────────────────────────────────────────
🚀 AVAILABLE ROUTES (Worker)
───────────────────────────────────────────────
• /run_weekly
• /run_season
• /run_wellness
• /run_summary
• /run_data_quality

Query parameters:
  ?staging=1          → Staging determined by Worker hostname
  ?render=gpt         → enables GPT-rendered Markdown output
                         (includes both Markdown + semantic JSON)
  ?test=strava        → simulate STRAVA-only account
                        (removes usable activities and returns friendly error)

───────────────────────────────────────────────
🏗️  MODES
───────────────────────────────────────────────
LOCAL MODE
-----------
  • Runs report generation entirely in Python via audit_core.run_report()
  • Writes either:
        - report_<range>_prod_semantic.json  (default)
        - report_<range>_prod_markdown.md    (if --format markdown)

PREFETCH MODE (REMOTE)
----------------------
  • Fetches data from Cloudflare Worker which proxies Railway.
  • Automatically handles both production and staging targets.
  • Writes semantic JSON by default:
        - report_<range>_prefetch_prod_semantic.json
  • If GPT flag is enabled:
        - report_<range>_prefetch_prod_gpt_markdown.md
        - report_<range>_prefetch_prod_gpt_semantic.json
    (Markdown is ChatGPT-rendered, JSON is original semantic graph)

───────────────────────────────────────────────
⚙️  CLI USAGE EXAMPLES
───────────────────────────────────────────────
  python report.py --range weekly (LOCAL JSON) 
  python report.py --range weekly --format semantic (LOCAL JSON)
  python report.py --range weekly --prefetch (RAILWAY JSON) - This would get sent to GPT
  python report.py --range weekly --prefetch --staging (RAILWAY STAGING JSON) - this would get sent to GPT
  python report.py --range season --prefetch --gpt (RAILWAY JSON AND GPT MD)
  python report.py --range summary --start 2025-01-01 --end 2025-12-31 (LOCAL JSON)
  python report.py --range weekly --prefetch --staging --strava-test
    → simulates STRAVA-only account and returns friendly data-source error

| CLI flag             | Worker param   | Test scenario                              | Expected result                                                            |
| -------------------- | -------------- | ------------------------------------------ | -------------------------------------------------------------------------- |
| `--strava-test stub` | `test=strava`  | All activities are STRAVA API stub rows    | Hard stop: `STRAVA_API_RESTRICTED` (422) with friendly data-source message |
| `--strava-test 1`    | `test=strava1` | Only light activities present (no full)    | Soft halt: insufficient detailed data (`FULL_DATASET_EMPTY` or similar)    |
| `--strava-test 2`    | `test=strava2` | Full dataset empty after filtering         | Soft halt: no usable activities in range                                   |
| `--strava-test 3`    | `test=strava3` | Activities present but missing key metrics | Degraded data quality state, report continues with warnings                |
| `--strava-test 4`    | `test=strava4` | Partial wellness or athlete metadata       | Degraded data quality score, report still generated                        |
| `--strava-test 5`    | `test=strava5` | Mixed valid + stub activities              | Report runs, data quality flagged with `strava_stub_detected`              |
| `--strava-test demo`    | `test=demo` | Demo report                                | Demo Report runs`              |


  DATA QUALITY REPORT
  python report.py --range data_quality --prefetch
   -> this gets data quality report

───────────────────────────────────────────────
🧠 NOTES
───────────────────────────────────────────────
• The GPT-rendered version returns a single JSON payload:
    {
        "markdown": "<AI-formatted Markdown>",
        "semantic_graph": { ... },
        "logs": "...",
        "status": "ok"
    }

• Local runs with --format semantic never use GPT (direct JSON only).

• Prefetch + GPT writes both Markdown and JSON files directly to ./reports
  — no duplication or mirror files will be created.
"""


import io
import os
import sys
import json
import argparse
import requests
from datetime import datetime
from contextlib import redirect_stdout
from pathlib import Path

# Import project modules
sys.path.append(os.path.abspath(os.path.dirname(__file__)))
sys.path.append(os.path.abspath(os.path.dirname(os.path.dirname(__file__))))
from audit_core.report_controller import run_report
from audit_core.utils import debug

sys.stdout.reconfigure(encoding="utf-8")

#---------------------------------------------
#  Resolve correct Cloudflare Worker base URL.
#----------------------------------------------
def get_worker_base(staging=False):

    if staging:
        return "https://intervalsicugptcoach-staging.clive-a5a.workers.dev"
    return "https://intervalsicugptcoach.clive-a5a.workers.dev"

# ─────────────────────────────────────────────
# DEBUG REPORTS
# ─────────────────────────────────────────────
def fetch_debug_report(report_type, staging=False):
    """
    Fetch debug report via Cloudflare Worker (prefetch + debug routing).
    Splits semantic report and debug logs into separate files.
    """

    worker_base = get_worker_base(staging)
    url = f"{worker_base}/run_{report_type}?debug=true&format=semantic"

    headers = {
        "Authorization": f"Bearer {os.getenv('ICU_OAUTH', '')}",
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
    json_name = f"report_{report_type}_{env}_debug.json"
    json_path = Path("reports") / json_name

    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(report_payload, f, indent=2)

    print(f"[DEBUG] ✅ Semantic report saved → {json_name}")

    # ------------------------------------------------
    # Save logs separately
    # ------------------------------------------------
    log_name = f"report_{report_type}_{env}_debug.log"
    log_path = Path("reports") / log_name

    with open(log_path, "w", encoding="utf-8") as f:
        f.write(logs)

    print(f"[DEBUG] 📜 Logs saved → {log_name}")

    if logs:
        print(f"[DEBUG] 📜 Logs captured: {len(logs.splitlines())} lines")

    return report_payload


# ─────────────────────────────────────────────
# PREFETCH HELPER — Cloudflare Worker Schema
# ─────────────────────────────────────────────
def fetch_remote_report(report_type, staging=False, gpt=False, start=None, end=None, strava_test=False):
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
        "User-Agent": "IntervalsGPTCoachLocal/1.0"
    }

    env = "staging" if staging else "prod"
    print(f"[REMOTE] env={env} report={report_type} gpt={gpt}")
    print(f"[REMOTE] → {url}")

    resp = requests.get(url, headers=headers, timeout=120)

    # Accept semantic error responses (422) from Worker
    try:
        data = resp.json()
    except Exception:
        resp.raise_for_status()
        raise

    # Only raise if truly unexpected
    if resp.status_code >= 500:
        resp.raise_for_status()

    Path("reports").mkdir(exist_ok=True)
    env_tag = "staging" if staging else "prod"

    content_type = resp.headers.get("content-type", "")

    # 🔥 Handle unified JSON payload (markdown + semantic)
    if "application/json" in content_type:
        data = resp.json()
        markdown = data.get("markdown")
        semantic = data.get("semantic_graph")

        if markdown:
            md_out = f"report_{report_type}_{env_tag}_gpt.md"
            Path(f"reports/{md_out}").write_text(markdown, encoding="utf-8")
            print(f"[REMOTE] ✅ Markdown saved → {md_out}")

        if semantic:
            json_out = f"report_{report_type}_{env_tag}_semantic.json"
            Path(f"reports/{json_out}").write_text(json.dumps(semantic, indent=2), encoding="utf-8")
            print(f"[REMOTE] ✅ Semantic JSON saved → {json_out}")

        return data

    # Legacy markdown-only fallback
    if "text/markdown" in content_type:
        text = resp.text
        md_out = f"report_{report_type}_{env_tag}_gpt.md"
        Path(f"reports/{md_out}").write_text(text, encoding="utf-8")
        print(f"[REMOTE] ✅ Markdown saved (legacy) → {md_out}")
        return {"markdown": text, "status": resp.status_code}

    # Default JSON flow (no GPT)
    data = resp.json()
    json_out = f"report_{report_type}_{env_tag}_semantic.json"
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
    strava_test=False
):
    """Run report and capture logs and output into one file."""
    buffer = io.StringIO()
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
                "status": "ok",
                "message": f"{report_type.title()} report (prefetched)",
                "semantic_graph": semantic,
                "logs": log_output,
            }

    # ============================================================
    # 💻 LOCAL MODE — Run directly via Railway
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

        with redirect_stdout(buffer):
            result = run_report(
                reportType=report_type,
                include_coaching_metrics=True,
                output_format=output_format,
                **context,
            )

        logs = buffer.getvalue()
        raw_logs = logs.splitlines()
        skip_terms = ["snapshot", "trace", "json", "context", "activities_full", "DataFrame"]
        log_output = "\n".join(
            [line for line in raw_logs if not any(term in line.lower() for term in skip_terms)]
        ).strip()

        if isinstance(result, tuple):
            report = result[0]
        else:
            report = result

        if isinstance(report, dict):
            if output_format == "semantic":
                semantic_output = report.get("semantic_graph", {})
                full_output = {
                    "status": "ok",
                    "message": f"{report_type.title()} report generated",
                    "semantic_graph": semantic_output,
                    "logs": log_output,
                    "date_range": {"start": start, "end": end} if start and end else None,
                }
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

    env_tag = "staging" if staging else "prod"
    prefetch_tag = "_prefetch" if prefetch else ""
    gpt_tag = "_gpt" if gpt else ""
    base_name = f"report_{report_type}{prefetch_tag}_{env_tag}{gpt_tag}_{output_format}"


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

    else:
        out_path = reports_dir / f"{base_name}.md"
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(full_output)
        print(f"[LOCAL] ✅ Saved markdown report → {out_path}")

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
    if args.debug:
        print(f"[CLI] 🧠 Debug mode enabled for '{args.range}' (staging={args.staging})")
        fetch_debug_report(args.range, staging=args.staging)
        return  # ✅ Skip normal report generation entirely

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
        strava_test=args.strava_test
    )



if __name__ == "__main__":
    main()
