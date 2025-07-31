from .base import Agent

class ReportAgent(Agent):
    """Aggregates and reports findings."""

    def run(self, task_data):
        # Implement reporting logic here
        report = {"summary": "Report generated", "findings": task_data.get("findings", [])}
        self.send_message("reports", report)
        return report