"""
HTTP client for the intervals.icu REST API.
Authentication: Basic Auth with username="API_KEY" and password=<your_api_key>
"""

import os
from datetime import date, timedelta
from typing import Any

import requests
from dotenv import load_dotenv

load_dotenv()

BASE_URL = "https://intervals.icu/api/v1"


class IntervalsClient:
    def __init__(self, api_key: str | None = None, athlete_id: str | None = None):
        self.api_key = api_key or os.environ["ICU_API_KEY"]
        self.athlete_id = athlete_id or os.environ["ICU_ATHLETE_ID"]
        self.session = requests.Session()
        # intervals.icu Basic Auth: username="API_KEY", password=api_key
        self.session.auth = ("API_KEY", self.api_key)
        self.session.headers.update({"Accept": "application/json"})

    def _get(self, path: str, params: dict | None = None) -> Any:
        url = f"{BASE_URL}{path}"
        r = self.session.get(url, params=params)
        r.raise_for_status()
        return r.json()

    def _post(self, path: str, data: Any) -> Any:
        url = f"{BASE_URL}{path}"
        r = self.session.post(url, json=data)
        r.raise_for_status()
        return r.json()

    def _put(self, path: str, data: Any) -> Any:
        url = f"{BASE_URL}{path}"
        r = self.session.put(url, json=data)
        r.raise_for_status()
        return r.json()

    def _delete(self, path: str) -> None:
        url = f"{BASE_URL}{path}"
        r = self.session.delete(url)
        r.raise_for_status()

    # ── Athlete ──────────────────────────────────────────────────────────────

    def get_athlete(self) -> dict:
        """Return athlete settings: FTP, LTHR, zones, sport config."""
        return self._get(f"/athlete/{self.athlete_id}")

    # ── Activities ────────────────────────────────────────────────────────────

    def list_activities(
        self,
        oldest: str | None = None,
        newest: str | None = None,
    ) -> list[dict]:
        """Return activity list (light) for the given date range.

        Dates as ISO strings (YYYY-MM-DD). Defaults to last 28 days.
        """
        if not oldest:
            oldest = (date.today() - timedelta(days=28)).isoformat()
        if not newest:
            newest = date.today().isoformat()
        return self._get(
            f"/athlete/{self.athlete_id}/activities",
            params={"oldest": oldest, "newest": newest},
        )

    def get_activity(self, activity_id: int) -> dict:
        """Return full details for a single activity."""
        return self._get(f"/athlete/{self.athlete_id}/activities/{activity_id}")

    # ── Wellness ──────────────────────────────────────────────────────────────

    def list_wellness(
        self,
        oldest: str | None = None,
        newest: str | None = None,
    ) -> list[dict]:
        """Return wellness records (HRV, sleep, fatigue, form…) for the date range."""
        if not oldest:
            oldest = (date.today() - timedelta(days=14)).isoformat()
        if not newest:
            newest = date.today().isoformat()
        return self._get(
            f"/athlete/{self.athlete_id}/wellness",
            params={"oldest": oldest, "newest": newest},
        )

    # ── Power curves ─────────────────────────────────────────────────────────

    def get_power_curves(self, sport_type: str = "Ride") -> dict:
        """Return power curves for the given sport type."""
        return self._get(
            f"/athlete/{self.athlete_id}/power-curves",
            params={"type": sport_type},
        )

    # ── Calendar / Events ────────────────────────────────────────────────────

    def list_events(
        self,
        oldest: str | None = None,
        newest: str | None = None,
    ) -> list[dict]:
        """Return planned workouts / calendar events."""
        if not oldest:
            oldest = date.today().isoformat()
        if not newest:
            newest = (date.today() + timedelta(days=14)).isoformat()
        return self._get(
            f"/athlete/{self.athlete_id}/events",
            params={"oldest": oldest, "newest": newest},
        )

    def create_event(self, event: dict) -> dict:
        """Create a calendar event (planned workout).

        Minimal required fields:
            start_date_local: "YYYY-MM-DD"
            name: str
            type: "Ride" | "Run" | ...
            category: "WORKOUT" | "NOTE" | "RACE" | ...
        Optional:
            description: str  (workout instructions)
            load_target: int  (target TSS)
            duration_target: int  (seconds)
        """
        return self._post(f"/athlete/{self.athlete_id}/events", event)

    def delete_event(self, event_id: int) -> None:
        """Delete a calendar event by ID."""
        self._delete(f"/athlete/{self.athlete_id}/events/{event_id}")
