import abc
import json

from redis import Redis

from postgres_to_es.config import logger
from postgres_to_es.helpers import EnhancedJSONEncoder


class BaseStorage:
    @abc.abstractmethod
    def save_state(self, state: dict) -> None:
        """Save state to persistent storage"""
        pass

    @abc.abstractmethod
    def retrieve_state(self) -> dict:
        """Load state locally from persistent storage"""
        pass


class RedisStorage(BaseStorage):
    """
    Borrowed from here:

    https://practicum.yandex.ru/learn/middle-python/courses/af061b15-1607-45f2-8d34-f88d4b21765a/sprints/
    7099/topics/665ba0d6-6eab-41d5-84dd-bbc1997930fb/lessons/97e47164-ba1c-4f72-ac23-df54564a4bcd/
    """

    def __init__(self, redis_adapter: Redis):
        self.redis_adapter = redis_adapter

    def save_state(self, state: dict) -> None:
        """Save state to persistent storage"""

        self.redis_adapter.set(
            'start_from_ts',
            json.dumps(
                state,
                cls=EnhancedJSONEncoder
            )
        )

    def retrieve_state(self) -> dict:
        """Load state locally from persistent storage"""

        raw_data = self.redis_adapter.get('start_from_ts')
        if raw_data is None:
            logger.info('Continue with the in-memory state since no state file was provided.')
            return {}
        return json.loads(raw_data)
