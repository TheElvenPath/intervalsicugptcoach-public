## Montis TOOL FUNCTIONS and parameters

Weekly Report → runWeeklyReportV2 → params: test?, lite?, start?, athleteID? → weekly performance review 
Season Report → runSeasonReportV2 → params: lite?, athleteID? → training block progression
Wellness Report → runWellnessReportV2 → params: athleteID? → recovery and fatigue status
Summary Report → runSummaryReportV2 → params: start?, end?, athleteID? → long-term trends

Read Calendar → readCalendarV1 → params: start*, end*, lite?, athleteID? → planned workouts and events
Write Calendar → writeCalendarV1 → body: planned_workouts[]* → create or update workouts
Delete Calendar → deleteCalendarV1 → body: id* | date* | dates* → remove workouts or events

List Activities (Light) → listActivitiesLight → params: oldest?, newest?, fields?, athleteID?
One Day Full Activity → getOneDayFullActivityV1 → params: date? | activity_id?, athleteID? → full activity breakdown or activities for a given day
One Day Wellness → getOneDayWellnessV1 → params: date*, athleteID? → HRV, fatigue, recovery

Power Curves → getPowerCurvesExtV1 → params: type*, curves?, pmType?, athleteID? → power curve modelling
Pace Curves → getPaceCurvesExtV1 → params: type*, curves?, athleteID? → pace profiling
HR Curves → getHRCurvesV1 → params: curves?, type?, athleteID? → hr curve modelling
Power-HR Curve → getPowerHRCurveV1 → params: start*, end*, athleteID? → power vs heart rate relationship
MMP Model → getMMPModelV1 → params: type?, athleteID?  → The MMP model describes the best power you can sustain across all durations
Athlete Profile → getAthleteProfileV1 → params: athleteID? → athlete profile
Sport Settings → getSportSettingsV1 → params: athleteID?  → athlete sport settings
Training Plan → getAthleteTrainingPlanV1 → params: athleteID? → structured training plan (if setup in intervals.icu)
Coached Athletes → getCoachedAthletesV1 → params: none  → list coached athletes if available (needs special setup, contact Montis owner)
Send Message → sendChatMessageV1 → body: content*, (chat_id | to_athlete_id | to_activity_id)* → send message to chat/athlete/activity
Data Quality Report → runDataQualityReportV1 → params: athleteID? → check your intervals data

---

Fields for listActivitiesLight

     // --- Field alias map (handles ChatGPT and API variances) ---
    const fieldAliases = {
    // ───── Core training metrics ─────
    "tss": "icu_training_load",
    "load": "icu_training_load",
    "training_load": "icu_training_load",
    "stress": "icu_training_load",
    "atl": "icu_atl",
    "ctl": "icu_ctl",
    "subtype": "sub_type",

    // ───── Duration variants ─────
    "duration": "moving_time",
    "duration_moving": "moving_time",
    "time": "moving_time",
    "elapsed": "moving_time",
    "moving_time": "moving_time",
    "duration_seconds": "moving_time",
    "duration_minutes": "moving_time",  // convert /60 in code

    // ───── Heart-rate variants ─────
    "hr": "average_heartrate",
    "heartrate": "average_heartrate",
    "avg_hr": "average_heartrate",
    "average_hr": "average_heartrate",
    "hr_avg": "average_heartrate",
    "heart_rate": "average_heartrate",
    "max_heartrate": "max_heartrate",
    "hr_max": "max_heartrate",
    "max_hr": "max_heartrate",
    "hrr": "icu_hrr",

    // ───── Power / Watts ─────
    "watts": "icu_average_watts",
    "power": "icu_average_watts",
    "avg_power": "icu_average_watts",
    "average_power": "icu_average_watts",
    "power_avg": "icu_average_watts",
    "average_watts": "icu_average_watts",
    "weighted_power": "icu_weighted_avg_watts",
    "ftp": "icu_ftp",

    // ───── Extended Power Metrics ─────
    "np": "icu_weighted_avg_watts",              // Normalized Power (NP)
    "normalized_power": "icu_weighted_avg_watts",
    "normalized_watts": "icu_weighted_avg_watts",
    "normalised_watts": "icu_weighted_avg_watts",
    "icu_normalized_power": "icu_weighted_avg_watts",
    "max_power": "icu_pm_p_max",              // Max instantaneous power
    "power_max": "icu_pm_p_max",              // Max instantaneous power
    "peak_power": "icu_pm_p_max",
    "activity_ftp": "icu_pm_ftp",          
    "power_balance": "avg_lr_balance",      // L/R balance if available
    "power_variability_index": "icu_variability_index",       // Variability Index
    "vi": "icu_variability_index",
    "work": "icu_joules",                 // total work (J)
    "work_joules": "icu_joules",
    "kjoules": "icu_joules",
    "wbal_depletion": "icu_max_wbal_depletion",// W′bal depletion
    "wbal": "icu_max_wbal_depletion",
    "anaerobic_capacity": "icu_w_prime",       // alias of w′
    "icu_variability_index": "icu_variability_index",
    "icu_weighted_avg_watts": "icu_weighted_avg_watts",
    "kj": "icu_joules",
    "avg_pace": "pace",

    // ───── Cadence ─────
    "cadence": "average_cadence",
    "cad": "average_cadence",
    "avg_cadence": "average_cadence",
    "cadence_avg": "average_cadence",

    // ───── Distance ─────
    "distance": "distance",
    "distance_m": "distance",
    "distance_km": "distance",   // divide by 1000
    "dist": "distance",

    // ───── Elevation / Climb ─────
    "elevation": "total_elevation_gain",
    "elevation_gain": "total_elevation_gain",
    "elev_gain": "total_elevation_gain",
    "climb": "total_elevation_gain",

    // ───── Intensity / Efficiency ─────
    "if": "icu_intensity",
    "intensity_factor": "icu_intensity",
    "intensity": "icu_intensity",
    "intensity_percent": "icu_intensity",
    "decoupling": "decoupling",

    // ───── Metadata ─────
    "title": "name",
    "name": "name",
    "activity": "name",
    "activity_id": "id",
    "date": "start_date_local",
    "start": "start_date_local",
    "sport": "type",
    "type": "type",
    "sport_type": "type",
    "source": "source",
    "platform": "source",
    "device": "device_name",

    // ───── Energy / Calories ─────
    "calories": "calories",
    "kcal": "calories",
    "energy": "calories",

    // ───── TRIMP / Strain / HR Load ─────
    "trimp": "trimp",
    "strain": "strain_score",
    "strain_score": "strain_score",
    "hr_load": "hr_load",

    // ───── VO₂-related ─────
    "vo2max": "VO2MaxGarmin",
    "vo2_max": "VO2MaxGarmin",
    "vo2maxgarmin": "VO2MaxGarmin",
    "vo2max_garmin": "VO2MaxGarmin",
    "vo2max_garmin_connect": "VO2MaxGarmin",

    // ───── W′ (anaerobic work capacity) ─────
    "wprime": "icu_w_prime",
    "w_prime": "icu_w_prime",

    // ───── W′ (LACTATE) ─────
    "lt1_mmol": "HrtLndLt1",
    "lt1_power": "HrtLndLt1p",
    "hrtlndlt1": "HrtLndLt1",
    "hrtlndlt1p": "HrtLndLt1p",

    // ───── Optional Tier-1 / extended ─────
    "notes": "description",              // full dataset only
    "comment": "description",
    "description": "description"
    };