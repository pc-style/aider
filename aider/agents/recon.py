from .base import Agent

class ReconAgent(Agent):
    """Performs reconnaissance tasks."""

    def run(self, task_data):
        # Implement reconnaissance logic here
        result = {"status": "success", "details": "Recon complete", "findings": []}
        # Send results to bus for downstream agents
        self.send_message("recon_results", result)
        return result