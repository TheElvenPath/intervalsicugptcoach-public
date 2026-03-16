import json
import os

DEMO_WEEKLY = {}

path = "demo_weekly.json"

if os.path.exists(path):
    with open(path, "r", encoding="utf-8") as f:
        DEMO_WEEKLY = json.load(f)