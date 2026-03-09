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