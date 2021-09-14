import abc
import json
import os
from typing import Any, Optional


class BaseStorage:
    """
    The implementation is borrowed from the simulator:
    https://practicum.yandex.ru/learn/middle-python/courses/af061b15-1607-45f2-8d34-f88d4b21765a/
    sprints/7099/topics/665ba0d6-6eab-41d5-84dd-bbc1997930fb/lessons/5fb40521-4548-487c-b840-f1d760b4ada9/
    """

    @abc.abstractmethod
    def save_state(self, state: dict) -> None:
        """Save state to persistent storage"""

        pass

    @abc.abstractmethod
    def retrieve_state(self) -> dict:
        """Load state locally from persistent storage"""

        pass


class JsonFileStorage(BaseStorage):
    def __init__(self, file_path: Optional[str] = None):
        self.file_path = file_path

        if not os.path.exists(self.file_path):
            with open(self.file_path, 'w') as file:
                json.dump(dict(), file)

    def save_state(self, state: dict) -> None:
        """Save state to persistent storage"""

        data = self.retrieve_state()
        data.update(state)

        with open(self.file_path, 'w') as file:
            json.dump(data, file)

    def retrieve_state(self) -> dict:
        """Load state locally from persistent storage"""

        with open(self.file_path, 'r') as file:
            return json.load(file)


class State:
    """
    A class for storing state when working with data, so as not to constantly re-read the data from the beginning.
    """

    def __init__(self, storage: BaseStorage):
        self.storage = storage

    def set_state(self, key: str, value: Any) -> None:
        """Set state for a specific key"""

        self.storage.save_state({f'{key}': value})

    def get_state(self, key: str) -> Any:
        """Get a state for a specific key"""

        data = self.storage.retrieve_state()
        if key in data.keys():
            return data.get(key)
        return
