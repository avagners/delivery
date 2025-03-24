from abc import ABC
import uuid
from dataclasses import dataclass


@dataclass
class Aggregate(ABC):
    """Базовый класс для Aggregate Root"""

    id: uuid.UUID

    def __eq__(self, other):
        if not isinstance(other, Aggregate):
            return False
        return self.id == other.id

    def __hash__(self):
        return hash(self.id)
