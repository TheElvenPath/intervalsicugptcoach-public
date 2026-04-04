"""
Tier-2 Step 3.5 — Detect Phases (legacy-compatible, reinstated v16.1.1)
Infers phase segments from validated event-level load data.
Derived directly from legacy v15.4 inline logic.
"""
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
from audit_core.utils import debug
from coaching_cheat_sheet import CHEAT_SHEET
from coaching_profile import COACH_PROFILE

def metric_confidence(context, key, default="high"):
    # Primary: semantic metrics (weekly / seasonal reports)
    metrics = context.get("metrics", {})
    if isinstance(metrics.get(key), dict):
        return metrics[key].get("metric_confidence", default)

    # Fallback: legacy derived_metrics
    dm = context.get("derived_metrics", {})
    if isinstance(dm.get(key), dict):
        return dm[key].get("metric_confidence", default)

    return default

def metric_semantic_value(context, key, default=0.0):
    """
    Read metric value from semantic metrics first, then derived_metrics.
    """
    metrics = context.get("metrics", {})
    if isinstance(metrics.get(key), dict):
        val = metrics[key].get("value", default)
        try:
            return float(val)
        except (TypeError, ValueError):
            return default

    dm = context.get("derived_metrics", {})
    if isinstance(dm.get(key), dict):
        val = dm[key].get("value", default)
        try:
            return float(val)
        except (TypeError, ValueError):
            return default

    return default


# === Dynamic Heuristics from Cheat Sheet ===
def get_dynamic_heuristics():
    th = CHEAT_SHEET["thresholds"]
    return {
        "polarisation_target":
            sum(th["Polarisation"]["green"]) / 2,
        "recovery_floor":
            th["LoadVariabilityIndex"]["amber"][1],
        "fatigue_delta_green":
            th["FatigueTrend"]["green"],
        "acwr_upper":
            th["ACWR"]["green"][1],
        "fatigue_decay_const": 0.2,
        "efficiency_smoothing": 0.15,
    }

def metric_value(context, key, default=0.0):
    """Return numeric metric value, handling None, NaN, and dict forms safely."""
    val = context.get(key, default)
    if isinstance(val, dict):
        val = val.get("value", default)
    try:
        if val is None or (isinstance(val, float) and np.isnan(val)):
            return default
        return float(val)
    except (TypeError, ValueError):
        return default


def detect_phases(context, events):
    """
    Tier-2 Phase Detection (v17.9 — Science-Aligned, Traceable)
    ------------------------------------------------------------
    Classifies macrocycle phases (Base, Build, Peak, Taper, Recovery,
    Deload, Continuous Load) using week-to-week training load trends,
    CTL/ATL smoothing (Banister model), and fatigue–freshness (TSB)
    evaluation aligned with Intervals.icu and TrainingPeaks metrics.

    🧠 Scientific Foundations:
        • Banister et al. (1975–1991) – Impulse-Response Model (CTL/ATL/TSB)
        • Seiler (2010, 2020) – Endurance intensity distribution & durability
        • Mujika & Padilla (2003, 2010) – Tapering & performance maintenance
        • Issurin (2008) – Block Periodisation: accumulation → realisation
        • Friel (2009) – Practical macrocycle mapping (Base → Build → Peak)
        • Gabbett (2016) – Acute:Chronic Workload Ratio (ACWR safety)
        • Foster (1998) – Training monotony and load variability

    📚 Adds: calc_method + calc_context per phase for full traceability.
    """

    debug(context, "[PHASES] ---- Phase detection start (v17.9) ----")

    # --- Validate input ----------------------------------------------------
    if not events or not isinstance(events, (list, tuple)):
        debug(context, "[PHASES] ❌ No valid event list")
        context["phases"] = [{"phase": "No Data", "start": None, "end": None, "delta": 0.0}]
        return context

    df = pd.DataFrame(events)
    if df.empty or "icu_training_load" not in df.columns:
        debug(context, "[PHASES] ❌ Missing icu_training_load")
        context["phases"] = [{"phase": "No Data", "start": None, "end": None, "delta": 0.0}]
        return context

    # --- Normalize timestamps ---------------------------------------------
    date_col = "start_date_local" if "start_date_local" in df.columns else "start_date"
    df["date"] = pd.to_datetime(df[date_col], errors="coerce")
    df = df.dropna(subset=["date"]).sort_values("date")

    # --- Weekly aggregation ------------------------------------------------
    df["week_start"] = df["date"].dt.to_period("W").apply(lambda r: r.start_time)
    df_week = (
        df.groupby("week_start")
          .agg({"icu_training_load": "sum"})
          .reset_index()
          .rename(columns={"icu_training_load": "tss"})
    )
    if df_week.empty:
        debug(context, "[PHASES] ⚠️ No weekly load data after aggregation")
        context["phases"] = [{"phase": "No Data", "start": None, "end": None, "delta": 0.0}]
        return context

    # --- Compute Banister model metrics -----------------------------------
    df_week["ctl"] = df_week["tss"].ewm(span=6, adjust=False).mean()
    df_week["atl"] = df_week["tss"].ewm(span=2, adjust=False).mean()
    df_week["tsb"] = df_week["ctl"] - df_week["atl"]
    df_week["delta_raw"] = df_week["tss"].pct_change().clip(-1, 2).fillna(0)
    df_week["delta"] = df_week["delta_raw"].ewm(span=3, adjust=False).mean().round(3)

    # --- Compute dynamic ACWR & Foster LVI -----------------------------
    df_week["acwr"] = (df_week["atl"] / df_week["ctl"]).replace([np.inf, -np.inf], np.nan).fillna(1.0).clip(0, 2)
    rolling_mean = df_week["tss"].rolling(3).mean()
    rolling_std  = df_week["tss"].rolling(3).std(ddof=0)

    weekly_monotony = (rolling_mean / (rolling_std + 1e-6)).fillna(1.0)
    df_week["lvi"] = (1 - (weekly_monotony / 5)).clip(0, 1)

    # --- Precompute safe slopes -------------------------------------------
    df_week["ctl_slope"] = df_week["ctl"].diff().fillna(0)
    df_week["atl_slope"] = df_week["atl"].diff().fillna(0)

    # --- Load thresholds ---------------------------------------------------
    phase_thresholds = CHEAT_SHEET["thresholds"]["PhaseBoundaries"]
    phase_advice     = CHEAT_SHEET["advice"]["PhaseAdvice"]

    # --- Phase classification (per-week) ----------------------------------
    labels, methods, traces = [], [], []
    for i in range(len(df_week)):
        d, tss, ctl, atl, tsb = (
            df_week.iloc[i]["delta"],
            df_week.iloc[i]["tss"],
            df_week.iloc[i]["ctl"],
            df_week.iloc[i]["atl"],
            df_week.iloc[i]["tsb"]
        )
        ctl_slope = float(df_week.iloc[i]["ctl_slope"])
        atl_slope = float(df_week.iloc[i]["atl_slope"])
        acwr = float(df_week.iloc[i]["acwr"])
        lvi = float(df_week.iloc[i]["lvi"])

        label = "Base"
        method_source = "steady_load_fallback"
        method_trace = {
            "delta": round(d, 3),
            "tsb": round(tsb, 2),
            "ctl_slope": round(ctl_slope, 2),
            "atl_slope": round(atl_slope, 2),
            "acwr": round(acwr, 2),
            "lvi": round(lvi, 2)
        }

        # --- Primary thresholds
        d = 0.0 if (d is None or (isinstance(d, float) and np.isnan(d))) else float(d)

        for phase, bounds in phase_thresholds.items():
            if bounds["trend_min"] <= d <= bounds["trend_max"]:
                if acwr <= bounds.get("acwr_max", 9) and lvi >= bounds.get("lvi_min", 0):
                    label = phase
                    method_source = f"PhaseBoundaries({phase})"
                    break

        # --- Banister-informed multi-model phase detection system
        '''
        Hybrid endurance periodisation model combining:
        - Banister load-response (CTL/ATL/TSB)
        - ΔTSS trend analysis
        - ACWR load safety
        - Block periodisation mapping
        - Macrocycle
            └── Mesocycle (Season block)
                └── Phase (Base / Build / etc.)
                    └── Microcycle (Week)
                            └── Sessions
        '''
        if tsb < -30:
            # True overreach = strong spike + deep fatigue
            if (
                d > 0.20
                and tsb < -50
                and acwr >= 1.15
                and atl_slope > ctl_slope * 1.3
            ):
                label, method_source = "Overreached", "TSB<-50 + overload spike"
            else:
                label, method_source = "Build", "TSB<-30 (acute overload)"

        elif tsb > 10:
            # distinguish taper vs recovery by magnitude of drop
            if d < -0.15:
                label, method_source = "Taper", "TSB>10 + strong unload"
            elif d < -0.05:
                label, method_source = "Deload", "TSB>10 + moderate unload"
            else:
                label, method_source = "Recovery", "TSB>10 + low load"

        elif -5 <= tsb <= 5 and abs(d) < 0.05:
            label, method_source = "Base", "|ΔTSS|<5% & TSB≈0"

        elif -30 <= tsb < -5 and d > 0.10:
            label, method_source = "Build", "TSB=-30–-5 & ΔTSS>0.1"

        labels.append(label)
        methods.append(method_source)
        traces.append(method_trace)

    df_week["phase_raw"] = labels
    df_week["calc_method"] = methods
    df_week["calc_context"] = traces

    # --- Merge contiguous same-phase blocks -------------------------------
    merged = []
    current_phase, current_method, start_date, tss_acc = None, None, None, 0

    for i, row in df_week.iterrows():
        ph = row["phase_raw"]

        force_split = False

        if ph != current_phase or force_split:
            if current_phase is not None:
                merged.append({
                    "phase": current_phase,
                    "start": start_date.strftime("%Y-%m-%d"),
                    "end": prev.strftime("%Y-%m-%d"),
                    "duration_days": (prev - start_date).days,
                    "duration_weeks": round((prev - start_date).days / 7, 1),
                    "tss_total": round(tss_acc, 1),
                    "ctl": round(prev_ctl, 2),
                    "tsb": round(prev_tsb, 2),
                    "calc_method": current_method,
                    "calc_context": prev_trace,
                    "descriptor": phase_advice.get(current_phase, f"{current_phase} phase detected.")
                })
            current_phase = ph
            current_method = row["calc_method"]
            start_date = row["week_start"]
            tss_acc = row["tss"]
        else:
            tss_acc += row["tss"]
        prev = row["week_start"]
        prev_ctl, prev_tsb = row["ctl"], row["tsb"]
        prev_trace = row["calc_context"]

    # Close final phase
    if current_phase:
        merged.append({
            "phase": current_phase,
            "start": start_date.strftime("%Y-%m-%d"),
            "end": prev.strftime("%Y-%m-%d"),
            "duration_days": (prev - start_date).days,
            "duration_weeks": round((prev - start_date).days / 7, 1),
            "tss_total": round(tss_acc, 1),
            "ctl": round(prev_ctl, 2),
            "tsb": round(prev_tsb, 2),
            "calc_method": current_method,
            "calc_context": prev_trace,
            "descriptor": phase_advice.get(current_phase, f"{current_phase} phase detected.")
        })


    # --- Phase smoothing (prevent flip-flopping) ------------------
    '''
    Banister model → fatigue/adaptation lag (not instant)
    Issurin block periodisation → blocks ≥ 2–4 weeks
    Mujika tapering → taper ≠ 1-week noise flip
    Real coaching practice → phases persist
    '''
    min_block_weeks = 2
    smoothed = []

    for i in range(len(df_week)):
        current = df_week.iloc[i]["phase_raw"]

        if i == 0:
            smoothed.append(current)
            continue

        prev = smoothed[-1]

        # if phase changes too quickly → ignore change
        if current != prev:
            # look ahead to confirm change is real
            future = df_week.iloc[i:i+min_block_weeks]["phase_raw"].tolist()

            if len(future) < min_block_weeks or any(p != current for p in future):
                smoothed.append(prev)   # reject flip
            else:
                smoothed.append(current)
        else:
            smoothed.append(current)

    df_week["phase_raw"] = smoothed

    # -------------------------------------------------
    # 🔁 Post-process: fix misclassified Load Spikes
    # -------------------------------------------------

    for i in range(len(merged)):

        phase = merged[i]["phase"]
        duration = merged[i]["duration_days"]
        ctx = merged[i].get("calc_context", {}) or {}

        delta = ctx.get("delta", 0)
        acwr = ctx.get("acwr", 1.0)
        ctl_slope = ctx.get("ctl_slope", 0)

    # --- Finalization -----------------------------------------------------
    context["phases"] = merged
    debug(context, f"[PHASES] ✅ Completed detection ({len(merged)} merged phases)")
    for p in merged:
        debug(context, f"[PHASES] → {p['phase']} ({p['start']} → {p['end']}) | TSB={p['tsb']}, CTL={p['ctl']} [{p['calc_method']}]")

    debug(context, "[PHASES] ---- Phase detection end ----")
    return context






"""
Tier-2 Step 4 — Evaluate Coaching Actions (v16.1.1)
Applies heuristics to validated derived metrics, outputs recommendations.
Now includes automatic phase detection from event-level data.
"""


def evaluate_actions(context):
    """
    Tier-2 Step 4 — Evaluate Coaching Actions (v17 dynamic)
    Fully dynamic thresholds and phase advice integration.
    """
    heur = get_dynamic_heuristics()

    derived = context.get("derived_metrics", {})
    extended = context.get("extended_metrics", {})

    # Promote metrics
    for k in ["ACWR", "Monotony", "Strain", "Polarisation", "LoadVariabilityIndex"]:
        if k not in context or isinstance(context[k], dict):
            if k in derived and isinstance(derived[k], dict):
                val = derived[k].get("value", np.nan)
                if isinstance(val, (int, float)) and not np.isnan(val):
                    context[k] = float(val)
    for k in ["Durability", "LoadIntensityRatio", "EnduranceReserve", "IFDrift", "FatOxidation"]:
        if k in extended:
            context[k] = extended[k]

    debug(context, "[T2-ACTIONS] Derived metrics integrated")

    actions = []
    metric_signals = []
    primary_message = None

    # ---------------- Stateful DELOAD latch ----------------
    lvi = context.get("LoadVariabilityIndex", 1.0)
    acwr = context.get("ACWR", 1.0)

    phase = (
        context.get("current_phase")
        or (context.get("phases", [{}])[-1].get("phase") if context.get("phases") else "")
    )

    last_phase = context.get("phases", [{}])[-1]
    ctl_slope = (
        last_phase.get("calc_context", {}).get("ctl_slope")
        if isinstance(last_phase.get("calc_context"), dict)
        else context.get("ctl_slope")
    )

    deload = context.get("_deload_state", {
        "active": False,
        "triggered_on": None,
        "reason": None,
    })

    failed_adaptation = (
        lvi < heur["recovery_floor"]
        and ctl_slope is not None
        and ctl_slope <= 0
    )

    phase_allows = phase not in ("Base", "Early Base")

    if not deload["active"] and failed_adaptation and phase_allows:
        deload["active"] = True
        deload["triggered_on"] = context.get("period", {}).get("end")
        deload["reason"] = "Recovery suppressed with no fitness gain"

        msg_key = "build_deload"
        if acwr > heur["acwr_upper"]:
            msg_key = "overreach_deload"

        primary_message = CHEAT_SHEET.get("primary_messages", {}).get(msg_key)

    elif deload["active"]:
        actions.append("🟡 Deload in progress — allow recovery before resuming load.")

    context["_deload_state"] = deload

    # ---------------- Reset DELoad latch ----------------
    if (
        deload["active"]
        and deload.get("triggered_on") != context.get("period", {}).get("end")
    ):
        recovered = (
            lvi >= heur["recovery_floor"]
            and acwr <= heur["acwr_upper"]
        )

        if recovered:
            deload["active"] = False
            deload["reason"] = None
            actions.append("🟢 Recovery restored — deload complete, resume progression.")


    # ---------------- Fatigue Trend ----------------
    ft = context.get("FatigueTrend")
    if ft is None:
        ft = 0.0

    ft_state = (
        context.get("metrics", {})
        .get("FatigueTrend", {})
        .get("semantic_state")
    )

    if ft_state:
        if ft_state in ("recovering", "moderate_low"):
            metric_signals.append(f"⚠ FatigueTrend {ft:.2f} — recovery phase, maintain steady load.")

        elif ft_state in ("moderate_high", "accumulating", "extreme_accumulation"):
            metric_signals.append(f"⚠ FatigueTrend {ft:.2f} — accumulating fatigue, monitor intensity.")

        elif ft_state == "balanced":
            metric_signals.append(f"✅ FatigueTrend {ft:.2f} — balanced load.")
    # ---------------- Benchmark / FatMax ----------------
    if context.get("weeks_since_last_FTP", 0) >= 6:
        metric_signals.append("🔄 Retest FTP/LT1 for updated benchmarks.")
    decoup = context.get("Decoupling")
    if decoup is not None and abs(context.get("FatMaxDeviation", 1.0)) <= 0.05 and decoup <= 0.05:
        metric_signals.append("✅ FatMax calibration verified (±5 %).")

    # ---------------- UI Flag ----------------
    if lvi < 0.6:
        context["ui_flag"] = "🔴 Overreached"
    elif lvi < 0.8:
        context["ui_flag"] = "🟠 Fatigued"
    else:
        context["ui_flag"] = "🟢 Normal"

    # ---------------- Derived Metric Feedback ----------------

    th = CHEAT_SHEET["thresholds"]

    lvi = context.get("LoadVariabilityIndex", 1.0)
    fox = context.get("FatOxidation")
    decoup = context.get("Decoupling")

    # ---- Metabolic efficiency ----
    if fox is not None and decoup is not None:

        if fox >= 0.8 and decoup <= 0.05:

            metric_signals.append({
                "metric": "FatOxidation",
                "state": "efficient"
            })

        else:

            metric_signals.append({
                "metric": "FatOxidation",
                "state": "needs_improvement"
            })


    # ---- Load Variability Index ---- # not a coaching metric now = old 
#    if lvi < th["LoadVariabilityIndex"]["amber"][0]:

#        metric_signals.append({
#            "metric": "LoadVariabilityIndex",
#            "state": "poor"
#        })

#    elif lvi < th["LoadVariabilityIndex"]["green"][0]:

#        metric_signals.append({
#            "metric": "LoadVariabilityIndex",
#            "state": "moderate"
#        })

#    else:

#        metric_signals.append({
#            "metric": "LoadVariabilityIndex",
#            "state": "healthy"
#        })

    # ---------------- Append metric feedback ----------------

    final_actions = []

    if primary_message and all(k in primary_message for k in ("status", "action", "next")):
        final_actions.extend([
            "### Current status",
            primary_message["status"],
            "",
            "### Primary action",
            primary_message["action"],
            "",
            "### Once recovered",
            primary_message["next"],
            "",
            "---",
        ])

    final_actions.extend(actions)

    context["derived_metrics"] = derived
    context["actions"] = final_actions
    context["metric_signals"] = metric_signals
    return context


