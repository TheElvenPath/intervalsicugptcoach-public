class AuditHalt(Exception):
    """
    Raised when audit chain must halt due to integrity or data issues.

    Supports:
    - hard  → real error
    - soft  → demo fallback
    - info  → graceful early return (no demo)
    """

    def __init__(self, message, code="DATA_INTEGRITY", severity="soft"):
        super().__init__(message)
        self.message = message
        self.code = code
        self.severity = severity

    def to_dict(self):
        return {
            "status": "halted",
            "error_type": self.code,
            "severity": self.severity,
            "message": self._friendly_message()
        }

    def to_ok_dict(self, report_type=None):
        """ used for graceful early exits (no demo, no error)"""
        return {
            "status": "ok",
            "message": self._friendly_message(),
            "report_type": report_type,
            "output_format": "semantic_json",
            "semantic_graph": {
                "meta": {
                    "note": "insufficient_data"
                }
            },
            "compliance": {},
            "logs": ""
        }

    def _friendly_message(self):
        if "snapshot source empty" in self.message.lower():
            return "No training data available for the selected period."
        if "missing 'type' column" in self.message.lower():
            return "Training data schema incomplete. Please re-sync activities."
        return self.message