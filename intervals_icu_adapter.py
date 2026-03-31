"""
intervals_icu_adapter.py
========================
Replaces all Cloudflare Worker calls in the original audit_core pipeline
with direct intervals.icu API calls using Basic Auth.

Must be imported BEFORE any audit_core modules. Call apply() before running reports.

What it patches:
  1. audit_core.tier0_pre_audit.fetch_with_retry  — Basic Auth + URL rewrites
  2. audit_core.tier0_pre_audit.INTERVALS_API     — Cloudflare URL → intervals.icu
  3. audit_core.tier0_pre_audit.ICU_TOKEN         — placeholder (check bypass)
  4. audit_core.tier3_future_forecast.fetch_calendar_fallback — direct /events call
  5. audit_core.calendar.manager.WORKER_BASE      — same Cloudflare replacement

URL rewrites handled:
  /athlete/0/...          → /athlete/{ICU_ATHLETE_ID}/...
  /activities_t0light     → /activities  (strips &fields=… param)
  /power-curves-ext       → /power-curves (strips &curves=… &pmType=…)
  CLOUDFLARE/calendar/read → intervals.icu /events
"""

import base64
import json
import os
import re
from datetime import date, timedelta

import requests as _req
from dotenv import load_dotenv

# ── Load .env ─────────────────────────────────────────────────────────────────
load_dotenv()

ICU_API_KEY    = os.environ["ICU_API_KEY"]
ICU_ATHLETE_ID = os.environ["ICU_ATHLETE_ID"]
ICU_BASE       = "https://intervals.icu/api/v1"

# ── Set env vars BEFORE tier0 imports read them at module level ───────────────
os.environ["INTERVALS_API"] = ICU_BASE
# ICU_OAUTH must be non-empty to pass the RuntimeError check in run_tier0_pre_audit.
# Our patched fetch_with_retry ignores this value and uses Basic Auth instead.
os.environ["ICU_OAUTH"] = "placeholder_basic_auth_mode"


# ═══════════════════════════════════════════════════════════════════════════
# AUTH + URL HELPERS
# ═══════════════════════════════════════════════════════════════════════════

def _auth_header() -> str:
    """Build Basic Auth header for intervals.icu (API_KEY as username)."""
    creds = base64.b64encode(f"API_KEY:{ICU_API_KEY}".encode()).decode()
    return f"Basic {creds}"


def _rewrite_url(url: str) -> str:
    """Translate Cloudflare Worker URL patterns to standard intervals.icu API."""

    # 1. /athlete/0/ → /athlete/{real_id}/
    url = url.replace("/athlete/0/", f"/athlete/{ICU_ATHLETE_ID}/")
    url = url.replace("/athlete/0",  f"/athlete/{ICU_ATHLETE_ID}")

    # 2. /activities_t0light → /activities  (strip custom &fields= param)
    if "activities_t0light" in url:
        url = url.replace("activities_t0light", "activities")
        url = re.sub(r"[&?]fields=[^&]*", "", url)
        url = re.sub(r"\?&", "?", url)
        url = url.rstrip("?").rstrip("&")

    # 3. /power-curves-ext → /power-curves  (strip &curves= and &pmType= params)
    if "power-curves-ext" in url:
        url = url.replace("power-curves-ext", "power-curves")
        url = re.sub(r"[&?](curves|pmType)=[^&]*", "", url)
        url = re.sub(r"\?&", "?", url)
        url = url.rstrip("?").rstrip("&")

    # 4. Ensure base stays correct (shouldn't change after rewrites above)
    if url.startswith("https://intervalsicugptcoach") or "workers.dev" in url:
        # Fallback safety net — shouldn't reach here if patterns above are correct
        import re as _re
        url = _re.sub(r"https://[^/]+\.workers\.dev", ICU_BASE, url)

    return url


# ═══════════════════════════════════════════════════════════════════════════
# POWER CURVE RESPONSE NORMALISER
# ═══════════════════════════════════════════════════════════════════════════

def _wrap_power_curves(resp: _req.Response) -> _req.Response:
    """
    intervals.icu /power-curves returns a plain list.
    tier0_pre_audit.fetch_power_curves expects {"list": [prev, curr]}.

    If the response is a list of ≥2 entries → wrap as {"list": entries}.
    If exactly 1 entry → duplicate it so prev/curr are both available
      (ESPE will show 0% delta — stable across all systems).
    If empty → leave as-is (tier0 handles it gracefully).
    """
    try:
        data = resp.json()
        if isinstance(data, list):
            if len(data) == 0:
                wrapped = {"list": []}
            elif len(data) == 1:
                wrapped = {"list": [data[0], data[0]]}  # prev == curr → stable
            else:
                wrapped = {"list": data}
            # Rebuild response with transformed body
            resp._content = json.dumps(wrapped).encode("utf-8")
    except Exception:
        pass  # leave response unchanged if JSON parsing fails
    return resp


# ═══════════════════════════════════════════════════════════════════════════
# PATCHED fetch_with_retry
# ═══════════════════════════════════════════════════════════════════════════

def _patched_fetch_with_retry(url: str, headers: dict, max_retries: int = 2):
    """
    Drop-in replacement for audit_core.tier0_pre_audit.fetch_with_retry.

    Changes from original:
      - Ignores the passed `headers` (which contain a placeholder Bearer token)
      - Always uses Basic Auth for intervals.icu
      - Rewrites Cloudflare/custom URLs to standard intervals.icu endpoints
      - Wraps power-curves response into {"list": [...]} format
    """
    rewritten = _rewrite_url(url)
    auth = {
        "Authorization": _auth_header(),
        "Accept": "application/json",
    }

    for attempt in range(max_retries + 1):
        try:
            resp = _req.get(rewritten, headers=auth, timeout=30)
            if resp.status_code == 200:
                # Transform power curves response format
                if "power-curves" in rewritten:
                    resp = _wrap_power_curves(resp)
                return resp
            if attempt < max_retries:
                continue
        except _req.exceptions.RequestException:
            if attempt == max_retries:
                raise
    return resp


# ═══════════════════════════════════════════════════════════════════════════
# PATCHED calendar fetch  (tier3_future_forecast)
# ═══════════════════════════════════════════════════════════════════════════

def _patched_calendar_fallback(context: dict, days: int = 14, owner: str = "intervals"):
    """
    Replaces fetch_calendar_fallback in tier3_future_forecast.
    Calls intervals.icu /events directly instead of Cloudflare /calendar/read.
    """
    start = date.today().isoformat()
    end   = (date.today() + timedelta(days=days)).isoformat()
    url   = f"{ICU_BASE}/athlete/{ICU_ATHLETE_ID}/events?oldest={start}&newest={end}"

    try:
        resp = _req.get(
            url,
            headers={"Authorization": _auth_header(), "Accept": "application/json"},
            timeout=15,
        )
        resp.raise_for_status()
        data = resp.json()
        if not isinstance(data, list):
            data = []
        context["calendar"] = data
        return data
    except Exception as e:
        context.setdefault("_adapter_warnings", []).append(
            f"Calendar fetch failed: {e}"
        )
        return []


# ═══════════════════════════════════════════════════════════════════════════
# APPLY ALL PATCHES
# ═══════════════════════════════════════════════════════════════════════════

def apply() -> None:
    """
    Monkey-patch all Cloudflare-dependent functions in audit_core.
    Call once at startup, before any report is run.
    """
    # ── tier0_pre_audit ───────────────────────────────────────────────────
    import audit_core.tier0_pre_audit as t0
    t0.INTERVALS_API    = ICU_BASE
    t0.ICU_TOKEN        = os.environ["ICU_OAUTH"]   # "placeholder_basic_auth_mode"
    t0.fetch_with_retry = _patched_fetch_with_retry

    # ── tier3_future_forecast ─────────────────────────────────────────────
    import audit_core.tier3_future_forecast as t3ff
    t3ff.CLOUDFLARE_BASE         = ICU_BASE
    t3ff.ICU_TOKEN               = os.environ["ICU_OAUTH"]
    t3ff.fetch_calendar_fallback = _patched_calendar_fallback

    # ── calendar manager (if used) ────────────────────────────────────────
    try:
        import audit_core.calendar.manager as cal_mgr
        cal_mgr.WORKER_BASE = ICU_BASE
    except Exception:
        pass


# Auto-apply when the module is imported
apply()
