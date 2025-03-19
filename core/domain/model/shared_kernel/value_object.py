from dataclasses import dataclass


@dataclass(frozen=True)
class ValueObject:
    """Базовый класс для всех Value-Object"""

    def __eq__(self, other) -> bool:
        if not isinstance(other, ValueObject):
            return False
        return self.__dict__ == other.__dict__

    def __hash__(self) -> int:
        return hash(tuple(sorted(self.__dict__.items())))
