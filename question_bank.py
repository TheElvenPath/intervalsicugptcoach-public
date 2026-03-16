# Montis Coaching Intelligence Question Bank

QUESTION_BANK = {

"durability": [
{"signals":["durability_decline"],"priority":1,"question":"Is decoupling revealing durability limits or expected fatigue?"},
{"signals":["durability_decline"],"priority":1,"question":"Am I able to maintain output late in sessions or drifting early?"},
{"signals":["durability_pressure"],"priority":1,"question":"Is pacing stability improving across longer rides?"},
{"signals":["durability_pressure"],"priority":1,"question":"Is endurance resilience improving compared with recent weeks?"},

{"signals":["durability_decline","durability_pressure"],"priority":2,"question":"Is my durability improving or am I still decoupling under sustained load?"},
{"signals":["durability_decline","durability_pressure"],"priority":2,"question":"Did aerobic stability hold across longer sessions this week?"},
{"signals":["durability_decline","durability_pressure"],"priority":2,"question":"Are endurance sessions reinforcing durability or exposing drift?"},
{"signals":["durability_decline","durability_pressure"],"priority":2,"question":"Are longer efforts showing better stability than previous blocks?"},

{"signals":["durability_decline","durability_pressure"],"priority":3,"question":"Has durability progressed or plateaued?"},
{"signals":["durability_decline","durability_pressure"],"priority":3,"question":"Is aerobic durability keeping pace with training load?"},
{"signals":["durability_decline","durability_pressure"],"priority":3,"question":"Are longer rides showing improved efficiency across time?"},
{"signals":["durability_decline","durability_pressure"],"priority":3,"question":"Is pacing stability improving under fatigue?"},
{"signals":["durability_decline","durability_pressure"],"priority":3,"question":"Am I finishing longer efforts with the same control I started with?"},
{"signals":["durability_decline","durability_pressure"],"priority":3,"question":"Is endurance resilience strengthening across the block?"}
],


"repeatability":[
{"signals":["anaerobic_depletion"],"priority":1,"question":"Is W′ depletion happening earlier than expected?"},
{"signals":["anaerobic_depletion"],"priority":1,"question":"Are repeated hard efforts maintaining quality?"},
{"signals":["anaerobic_load"],"priority":1,"question":"Are high-intensity efforts becoming more repeatable?"},
{"signals":["anaerobic_load"],"priority":1,"question":"Am I sustaining power across repeated efforts?"},

{"signals":["anaerobic_depletion","anaerobic_load"],"priority":2,"question":"Is my anaerobic repeatability improving or declining?"},
{"signals":["anaerobic_depletion","anaerobic_load"],"priority":2,"question":"Are intervals degrading across the session or remaining stable?"},
{"signals":["anaerobic_depletion","anaerobic_load"],"priority":2,"question":"Is high-intensity capacity progressing across recent weeks?"},

{"signals":["anaerobic_depletion","anaerobic_load"],"priority":3,"question":"Are repeated efforts showing improved resilience?"},
{"signals":["anaerobic_depletion","anaerobic_load"],"priority":3,"question":"Is repeatability limiting the quality of hard sessions?"}
],


"neural_density":[
{"signals":["intensity_clustering"],"priority":1,"question":"Am I stacking intensity too closely together?"},
{"signals":["intensity_clustering"],"priority":1,"question":"Is intensity clustering limiting adaptation?"},
{"signals":["high_intensity_density"],"priority":1,"question":"Are high-intensity sessions accumulating effectively?"},
{"signals":["high_intensity_density"],"priority":1,"question":"Is neural density progressing across recent weeks?"},

{"signals":["intensity_clustering","high_intensity_density"],"priority":2,"question":"Is neural load balanced across the week?"},
{"signals":["intensity_clustering","high_intensity_density"],"priority":2,"question":"Is neural stimulus consistent across sessions?"},

{"signals":["intensity_clustering","high_intensity_density"],"priority":3,"question":"Is neural load evolving as expected across the block?"}
],


"training_load":[
{"signals":["load_pressure"],"priority":1,"question":"Is my current training load sustainable?"},
{"signals":["load_pressure"],"priority":1,"question":"Am I accumulating productive stress or excessive load?"},
{"signals":["load_pressure"],"priority":1,"question":"Is training demand exceeding recovery capacity?"},

{"signals":["load_pressure"],"priority":2,"question":"Is the training load progressing smoothly?"},
{"signals":["load_pressure"],"priority":2,"question":"Is the workload building consistently across weeks?"}
],


"fatigue_balance":[
{"signals":["fatigue_accumulation"],"priority":1,"question":"Is fatigue accumulating faster than adaptation?"},
{"signals":["fatigue_accumulation"],"priority":1,"question":"Is recovery keeping pace with accumulated stress?"},
{"signals":["fatigue_accumulation"],"priority":1,"question":"Is fatigue beginning to constrain performance?"},

{"signals":["fatigue_accumulation"],"priority":2,"question":"Is fatigue plateauing or escalating?"},
{"signals":["fatigue_accumulation"],"priority":2,"question":"Is fatigue interfering with high-quality sessions?"}
],


"system_balance":[
{"signals":["system_decline"],"priority":1,"question":"Which physiological system currently limits performance most?"},
{"signals":["system_decline"],"priority":1,"question":"Is aerobic durability limiting performance?"},
{"signals":["system_decline"],"priority":1,"question":"Is anaerobic repeatability becoming a constraint?"},

{"signals":["system_decline"],"priority":2,"question":"Which physiological system needs the most development?"}
],


"progression":[
{"signals":["system_progression"],"priority":1,"question":"Is my performance trajectory improving across recent blocks?"},
{"signals":["system_progression"],"priority":1,"question":"Is adaptation progressing steadily?"},

{"signals":["system_progression"],"priority":2,"question":"Is training stimulus translating into measurable improvement?"}
],


"adaptation_stability":[
{"signals":["system_progression"],"priority":2,"question":"Is the current adaptation stable or fragile?"},
{"signals":["system_progression"],"priority":2,"question":"Are gains stabilizing across repeated sessions?"},
{"signals":["system_progression"],"priority":2,"question":"Is adaptation consolidating across weeks?"},
{"signals":["system_progression"],"priority":2,"question":"Are improvements resilient under fatigue?"},
{"signals":["system_progression"],"priority":3,"question":"Is the trajectory of development stable?"}
]

}



SIGNAL_MAP = {

"durability_decline": "durability",
"durability_pressure": "durability",
"durability_trend_decline": "durability",
"durability_trend_improving": "durability",

"anaerobic_depletion": "repeatability",
"anaerobic_load": "repeatability",

"intensity_clustering": "neural_density",
"high_intensity_density": "neural_density",

"fatigue_accumulation": "fatigue_balance",
"load_pressure": "training_load",

"system_decline": "system_balance",
"system_progression": "progression",

"adaptation_fragile": "adaptation_stability",
"adaptation_unstable": "adaptation_stability",
"adaptation_stable": "adaptation_stability"
}

QUESTION_TEMPLATES = {

# ------------------------------------------------
# FATIGUE
# ------------------------------------------------

"fatigue_accumulation": {

"signals": ["fatigue_accumulation"],

"question_variants": [

"Is fatigue beginning to constrain performance?",
"Is accumulated fatigue starting to affect session quality?",
"Is fatigue rising faster than adaptation?"

]

},

"fatigue_accumulation+load_pressure": {

"signals": ["fatigue_accumulation","load_pressure"],

"question_variants": [

"Is fatigue beginning to constrain performance given the current {secondary}?",
"Is accumulated fatigue affecting performance under the present {secondary}?",
"Is fatigue rising faster than the body can adapt to the current {secondary}?"

]

},

# ------------------------------------------------
# LOAD
# ------------------------------------------------

"load_pressure": {

"signals": ["load_pressure"],

"question_variants": [

"Is the current training load sustainable?",
"Is the present load level producing productive stress or excessive strain?",
"Is the load trajectory aligned with adaptation?"

]

},

# ------------------------------------------------
# DURABILITY
# ------------------------------------------------

"durability_decline": {

"signals": ["durability_decline"],

"question_variants": [

"Is durability beginning to break down late in sustained efforts?",
"Is aerobic stability drifting under prolonged load?",
"Is fatigue revealing limits in endurance durability?"

]

},

"durability_pressure": {

"signals": ["durability_pressure"],

"question_variants": [

"Is durability responding positively to recent training load?",
"Is aerobic stability holding under the current endurance demand?",
"Is durability progressing as training volume increases?"

]

},

"durability_decline+fatigue_accumulation": {

"signals": ["durability_decline","fatigue_accumulation"],

"question_variants": [

"Is fatigue contributing to durability drift late in sustained efforts?",
"Is aerobic stability breaking down under accumulated fatigue?",
"Is fatigue revealing limits in durability?"

]

},

"durability_trend_decline": {
"signals": ["durability_trend_decline"],
"question_variants": [
"Is long-term durability trending downward across recent blocks?",
"Is endurance resilience declining across longer training windows?",
"Is sustained durability slipping compared with earlier phases?"
]
},

"durability_trend_improving": {
"signals": ["durability_trend_improving"],
"question_variants": [
"Is long-term durability steadily improving?",
"Are endurance adaptations consolidating across blocks?",
"Is durability strengthening across recent training cycles?"
]
},

# ------------------------------------------------
# ANAEROBIC
# ------------------------------------------------

"anaerobic_depletion": {

"signals": ["anaerobic_depletion"],

"question_variants": [

"Is anaerobic repeatability declining across high-intensity efforts?",
"Are repeated hard efforts losing quality due to W′ depletion?",
"Is anaerobic capacity being depleted faster than it recovers?"

]

},

"anaerobic_load": {

"signals": ["anaerobic_load"],

"question_variants": [

"Is anaerobic demand producing productive stimulus?",
"Are repeated high-intensity efforts becoming more sustainable?",
"Is anaerobic repeatability improving under current intensity?"

]

},

# ------------------------------------------------
# NEURAL
# ------------------------------------------------

"intensity_clustering": {

"signals": ["intensity_clustering"],

"question_variants": [

"Is intensity clustering limiting adaptation?",
"Are hard sessions stacking too closely together?",
"Is neural load concentrated too tightly in the week?"

]

},

"high_intensity_density": {

"signals": ["high_intensity_density"],

"question_variants": [

"Is the current intensity density supporting progression?",
"Are high-intensity sessions accumulating effectively?",
"Is neural demand balanced across the week?"

]

},

# ------------------------------------------------
# SYSTEM ADAPTATION
# ------------------------------------------------

"system_decline": {

"signals": ["system_decline"],

"question_variants": [

"Is a physiological system beginning to constrain performance?",
"Is one energy system declining relative to the others?",
"Is the current training stimulus misaligned with system needs?"

]

},

"system_progression": {

"signals": ["system_progression"],

"question_variants": [

"Is a specific physiological system showing clear progression?",
"Is adaptation occurring in the system currently targeted by training?",
"Is the current stimulus producing meaningful system improvement?"

]

},

"adaptation_plateau": {
"signals": ["adaptation_stable"],
"question_variants": [
"Has adaptation plateaued under the current stimulus?",
"Is training stimulus no longer driving measurable improvement?",
"Is a change in training stimulus required to progress further?"
]
},

# ------------------------------------------------
# ADAPTATION STABILITY
# ------------------------------------------------

"adaptation_fragile": {

"signals": ["adaptation_fragile"],

"question_variants": [

"Is the current adaptation fragile under training stress?",
"Are improvements stabilizing or fluctuating?",
"Is adaptation consolidating across sessions?"

]

},

"adaptation_unstable": {

"signals": ["adaptation_unstable"],

"question_variants": [

"Is adaptation becoming unstable under current stress?",
"Are improvements fluctuating instead of consolidating?",
"Is training stress exceeding adaptive capacity?"

]

},

"adaptation_stable": {

"signals": ["adaptation_stable"],

"question_variants": [

"Is adaptation consolidating successfully?",
"Are gains stabilizing across repeated sessions?",
"Is the current progression becoming durable?"

]

}

}