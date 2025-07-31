import yaml

class WorkflowEngine:
    """
    Parses and executes workflow templates described in YAML DSL.
    Executes agent chains, branching, and success criteria.
    """

    def __init__(self, agent_registry):
        self.agent_registry = agent_registry

    def load_workflow(self, yaml_path):
        with open(yaml_path, "r") as f:
            self.workflow = yaml.safe_load(f)
        return self.workflow

    def run(self, input_data):
        # Basic linear workflow execution; can expand to branching logic
        results = {}
        for step in self.workflow.get("steps", []):
            agent_name = step["agent"]
            agent = self.agent_registry[agent_name]
            result = agent.run(input_data)
            results[agent_name] = result
            input_data.update(result)
        return results