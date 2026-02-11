# audit_core/utils.py

import pandas as pd
from audit_core.errors import AuditHalt
import sys
import datetime
import os
# ------------------------------------------------------------
# 🌍 Auto-detect Railway environment
# ------------------------------------------------------------

# Railway sets this automatically:
#   production service  → RAILWAY_ENVIRONMENT=production
#   staging service     → RAILWAY_ENVIRONMENT=staging

RAILWAY_ENV = (
    os.getenv("RAILWAY_ENVIRONMENT")
    or os.getenv("ENVIRONMENT")
    or ""
).lower()

# Debug enabled everywhere except explicit production
IS_DEBUG_ENV = RAILWAY_ENV != "production"

# ------------------------------------------------------------
# Global state
# ------------------------------------------------------------

try:
    context
except NameError:
    context = {}

RUN_TIMESTAMP = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
GLOBAL_LOGFILE = None

# ------------------------------------------------------------
# 🔎 Debug Logger (Auto-suppressed in Production)
# ------------------------------------------------------------

def debug(*args):
    """
    Unified flush-safe logger.
    Auto-disabled in Railway production environment.
    """

    global GLOBAL_LOGFILE

    # 🔒 Suppress debug in production automatically
    if not IS_DEBUG_ENV:
        return

    try:
        if not args:
            return

        if isinstance(args[0], dict):
            context = args[0]
            msgs = args[1:]
        else:
            context = None
            msgs = args

        report_type = os.getenv("REPORT_TYPE", "unknown").lower()

        # Initialize logfile once (staging only)
        if GLOBAL_LOGFILE is None:
            reports_dir = os.path.join(os.getcwd(), "reports")
            os.makedirs(reports_dir, exist_ok=True)
            GLOBAL_LOGFILE = os.path.join(
                reports_dir,
                f"debug_{report_type}_{RUN_TIMESTAMP}.log"
            )

        ts = datetime.datetime.now().strftime("%H:%M:%S")
        msg = " ".join(str(m) for m in msgs)
        msg_out = f"[{ts}] {msg}"

        # Store trace in context
        if context is not None:
            context.setdefault("debug_trace", []).append(msg_out)

        # Print to stderr
        sys.stderr.write(msg_out + "\n")
        sys.stderr.flush()

        # Write to file
        with open(GLOBAL_LOGFILE, "a", encoding="utf-8") as f:
            f.write(msg_out + "\n")

    except Exception as e:
        sys.stderr.write(f"[debug-failure] {e}\n")
        sys.stderr.flush()


def validate_dataset_integrity(df: pd.DataFrame) -> bool:
    """Basic dataset sanity check — ensures no NaNs in critical fields."""
    required = ["moving_time", "icu_training_load"]
    if not all(col in df.columns for col in required):
        raise ValueError(f"Missing required columns in dataset: {required}")
    if df[required].isnull().values.any():
        raise ValueError("Null values detected in dataset integrity check.")
    return True


def validate_wellness_alignment(activity_df: pd.DataFrame, wellness_df: pd.DataFrame) -> bool:
    """Ensure wellness data covers the same date window as activity dataset."""

    # --- Defensive guards ---
    if activity_df is None or activity_df.empty:
        debug(context,"⚠ No activity data provided — skipping wellness alignment.")
        return True
    if wellness_df is None or (isinstance(wellness_df, pd.DataFrame) and wellness_df.empty):
        debug(context,"⚠ No wellness data provided — skipping wellness alignment.")
        return True

    df = activity_df.copy()
    if "start_date_local" not in df.columns:
        raise AuditHalt("❌ validate_wellness_alignment: start_date_local missing from activity_df")

        # --- Determine activity window ---
    start = pd.to_datetime(df["start_date_local"]).min()
    end = pd.to_datetime(df["start_date_local"]).max()
    debug(context,f"[T1] Wellness alignment window (tz-aware): {start} → {end}")

    # Convert to naive (date only) for fair comparison
    start_date = start.tz_convert(None).date() if start.tzinfo else start.date()
    end_date = end.tz_convert(None).date() if end.tzinfo else end.date()

    # --- Normalize wellness dates ---
    if isinstance(wellness_df, list):
        wellness_df = pd.DataFrame(wellness_df)

    if "date" not in wellness_df.columns:
        if "id" in wellness_df.columns:
            wellness_df["date"] = pd.to_datetime(wellness_df["id"]).dt.date
        else:
            debug(context,"⚠ Wellness data missing date/id column — cannot align.")
            return False

    w_dates = pd.to_datetime(wellness_df["date"], errors="coerce").dropna().sort_values()
    if w_dates.empty:
        debug(context,"⚠ Wellness dataset contains no valid dates.")
        return False

    # Convert wellness timestamps to naive dates
    w_start_date = w_dates.min().date()
    w_end_date = w_dates.max().date()
    debug(context,f"[T1] Wellness date range: {w_start_date} → {w_end_date}")

    # --- Compare as naive date objects ---
    if w_start_date > end_date or w_end_date < start_date:
        debug(context,f"⚠ Wellness window misaligned ({w_start_date}–{w_end_date} vs {start_date}–{end_date})")
        return False

    debug(context,"✅ Wellness alignment check passed.")
    return True

# PREFETCH RESOLUTION
def resolve_prefetched(name, context, fetch_fn=None, **kwargs):
    """
    Generic resolver for any prefetched dataset.
    Mirrors T0 resolve_dataset() pattern but works for any name.
    """
    pre = context.get("prefetched", {})

    # ✅ 1. Use prefetched data if available
    if name in pre and pre[name]:
        debug(context, f"[PREFETCH] Using prefetched '{name}' ({len(pre[name])} records)")
        return pre[name]

    # ✅ 2. Never fetch in prefetched (Railway) mode
    if "prefetched" in context:
        debug(context, f"[PREFETCH] Skipping external fetch for '{name}' (prefetched mode)")
        return []

    # ✅ 3. Fallback to fetch_fn only in local/dev
    if fetch_fn:
        debug(context, f"[PREFETCH] Fetching '{name}' via {fetch_fn.__name__}()")
        return fetch_fn(context, **kwargs)

    # 🚫 Safe default
    debug(context, f"[PREFETCH] No prefetched data or fetch function for '{name}'")
    return []

