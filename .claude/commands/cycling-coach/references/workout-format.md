# intervals.icu Workout Native Format

intervals.icu parses the `description` field into structured colored power-zone
blocks visible in the calendar and downloadable to Garmin/Wahoo.

**Free text = broken workout. Always use this exact format.**

## Rules

- Each step: `-<duration> <intensity> <cadence>`
- Duration: `10m`, `1h`, `1h30m`, `30s`, `4m30s`
- Intensity: zone (`z1`–`z7`) OR percentage range (`85-95%`) — **NO `@` prefix**
- Cadence: always include — **NO `@` prefix**
- Repeat block: `Nx` on its own line, steps indented with ` -` (space + dash)
- **Blank line REQUIRED before every `Nx` repeat block — no exceptions**

## Examples

**Z2 Endurance 2h:**
```
-10m z1 75-85rpm
-1h40m z2 85-90rpm
-10m z1 75-85rpm
```

**Threshold 3×10min:**
```
-15m z1-z2 85-90rpm

3x
 -10m 88-93% 85-90rpm
 -5m z1-z2 85-90rpm
-10m z1 80-85rpm
```

**VO2max 5×4min:**
```
-15m z1-z2 85-90rpm

5x
 -4m 106-120% 100-110rpm
 -4m z1 85-90rpm
-10m z1 80-85rpm
```

**Sweetspot 2×20min:**
```
-15m z1-z2 85-90rpm

2x
 -20m 88-93% 85-90rpm
 -10m z1-z2 85-90rpm
-10m z1 80-85rpm
```

**Neuromuscular Sprints 8×30s:**
```
-15m z1-z2 85-90rpm

8x
 -30s 130-150% 110-120rpm
 -4m30s z1 80-85rpm
-10m z1 75-80rpm
```

**Active Recovery 1h:**
```
-1h z1 70-80rpm
```

## Wrong vs Right

| WRONG | RIGHT |
|-------|-------|
| `-8m @105-110%` | `-8m 105-110% 85-90rpm` |
| `-10m z4 @88-93%` | `-10m 88-93% 85-90rpm` |
| `3x` (no blank line before) | `[blank line]\n3x` |
| `-30s z5 120rpm` | `-30s 130-150% 110-120rpm` |
