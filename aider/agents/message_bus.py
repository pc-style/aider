import redis
import json

class RedisMessageBus:
    """Redis-based pub/sub message bus for agent orchestration."""

    def __init__(self, host="localhost", port=6379, db=0):
        self.redis = redis.Redis(host=host, port=port, db=db)

    def send(self, channel, message):
        self.redis.publish(channel, json.dumps(message))

    def listen(self, channel):
        pubsub = self.redis.pubsub()
        pubsub.subscribe(channel)
        for msg in pubsub.listen():
            if msg["type"] == "message":
                yield json.loads(msg["data"])