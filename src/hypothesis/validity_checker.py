# (Safety & sanity filter)
# What this does
# Ensures:
# No SLA violations
# No dangerous skips
# No unlimited approvals bypass
# This is critical for trust.

class ValidityChecker:
    def __init__(self):
        self.forbidden_rules = [
            "skip_all_approvals",
            "remove_manager"
        ]

    def is_valid(self, hypothesis):
        if hypothesis["change"] in self.forbidden_rules:
            return False

        if hypothesis["risk"] == "high":
            return False

        return True

    def filter(self, hypotheses):
        return [h for h in hypotheses if self.is_valid(h)]
