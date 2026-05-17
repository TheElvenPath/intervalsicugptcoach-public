# Report Rendering Format

When presenting data from `run_weekly_report`, use this exact structure.
Always use tables, emojis, and sections. Never dump raw JSON or bullet-point metrics.

---

## Weekly / Wellness Report Template

```
# 📊 REPORT CONTEXT
Athlete: [name]  |  Period: [oldest] → [newest]  |  Phase: [detected phase]

---

# 🫀 PHYSIOLOGY RESPONSE

## 🧠 STATE
| Component       | Value               | Signal   | Interpretation                  |
|-----------------|---------------------|----------|---------------------------------|
| HRV Ratio       | X.XX                | 🔴/🟡/🟢 | подавление/стабильно/отлично    |
| Resting HR      | XX bpm              | 🔴/🟡/🟢 | стресс/норма/отдохнул           |
| Sleep Score     | XX                  | 🔴/🟡/🟢 | плохо/хорошо/отлично            |
| CTL / ATL / TSB | XX / XX / XX        | 🔴/🟡/🟢 | перегруз/баланс/готов           |
| Recovery State  | [state]             | —        | [one-line summary]              |

## 📡 LOAD SIGNALS
| Metric              | Value  | Signal   | Mechanism                        |
|---------------------|--------|----------|----------------------------------|
| ACWR                | X.XX   | 🔴/🟡/🟢 | Gabbett injury risk model        |
| HRV Stability Index | X.XXX  | 🔴/🟡/🟢 | ANS recovery indicator           |
| Stress Tolerance    | X.XX   | 🔴/🟡/🟢 | Foster strain model              |
| Monotony            | X.XX   | 🔴/🟡/🟢 | Foster monotony                  |
| Strain              | XXX    | 🔴/🟡/🟢 | TSS × Monotony                   |
| Polarisation Index  | XX%    | 🔴/🟡/🟢 | Seiler 3-zone distribution       |

## 🧾 INTERPRETATION
- What is happening physiologically (cause → effect)
- What the combination of signals means together
- What the body needs right now

---

# ⚙️ PERFORMANCE INTELLIGENCE

## 💪 POWER PROFILE
| Duration | Watts | W/kg | Context           |
|----------|-------|------|-------------------|
| 5s       | ...   | ...  | Neuromuscular     |
| 1min     | ...   | ...  | Anaerobic capacity|
| 5min     | ...   | ...  | VO2max proxy      |
| 20min    | ...   | ...  | FTP proxy         |

## 🔋 ENERGY SYSTEM STATUS
| System          | Indicator                   | State |
|-----------------|-----------------------------|-------|
| Aerobic engine  | EF, decoupling              | ...   |
| Threshold       | W' depletion, kJ above FTP  | ...   |
| VO2max          | 5min MMP trend              | ...   |
| Neuromuscular   | P_max, sprint power         | ...   |

---

# 🧾 CLOSING NOTE
**[State Label]** — e.g. "Productive Fatigue", "Adaptation Under Pressure", "Primed to Perform"

2–3 sentences: physiological mechanism → what it means for the athlete → action needed.
Recommendation for the next 24–72 hours.

---
### 💭 Coaching Question
One open question to prompt athlete self-awareness.
```

## Signal thresholds

| Metric | 🟢 | 🟡 | 🔴 |
|--------|----|----|-----|
| HRV Ratio | >0.95 | 0.85–0.95 | <0.85 |
| TSB | >−5 | −20 to −5 | <−20 |
| ACWR | <1.1 | 1.1–1.3 | >1.3 |
| Monotony | <1.5 | 1.5–2.0 | >2.0 |
| Decoupling | <5% | 5–8% | >8% |
