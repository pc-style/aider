import abc

class Agent(abc.ABC):
    """Base class for all agents in the workflow engine."""

    def __init__(self, agent_id, message_bus):
        self.agent_id = agent_id
        self.message_bus = message_bus

    @abc.abstractmethod
    def run(self, task_data):
        """Run the agent's main logic on a given task."""
        pass

    def send_message(self, channel, message):
        self.message_bus.send(channel, message)

    def receive_messages(self, channel):
        return self.message_bus.listen(channel)