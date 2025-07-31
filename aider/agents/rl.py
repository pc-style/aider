class RLFeedback:
    """Simple RL reward/penalty system for agent optimization."""

    REWARD_TABLE = {
        "high_severity_vuln": 10,
        "tool_crash": -5,
        "duplicate_finding": -3,
    }

    def __init__(self):
        self.agent_scores = {}

    def reward(self, agent_id, event):
        score = self.REWARD_TABLE.get(event, 0)
        self.agent_scores[agent_id] = self.agent_scores.get(agent_id, 0) + score
        return self.agent_scores[agent_id]

    def get_score(self, agent_id):
        return self.agent_scores.get(agent_id, 0)