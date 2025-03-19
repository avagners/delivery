from abc import ABC, abstractmethod
from dataclasses import dataclass, field

import uuid


class BusinessRule(ABC):
    """Абстрактный класс для бизнес-правил"""

    @abstractmethod
    def is_broken(self) -> bool:
        """Проверяет, нарушено ли правило"""
        raise NotImplementedError


class BusinessRuleBrokenException(Exception):
    """Исключение, которое выбрасывается при нарушении бизнес-правила"""

    def __init__(self, rule: BusinessRule):
        self.rule = rule
        super().__init__(f"Business rule {rule.__class__.__name__} is broken: {rule}")


@dataclass
class Entity:
    """Базовый класс для всех Entities"""
    id: uuid.UUID = field(default_factory=lambda: globals()['Entity'].next_id(), kw_only=True)

    @classmethod
    def next_id(cls) -> uuid.UUID:
        """Генерирует новый UUID"""
        return uuid.uuid4()

    def check_rule(self, rule: BusinessRule):
        """Проверяет, нарушено ли бизнес-правило. Если нарушено, выбрасывает исключение."""
        if rule.is_broken():
            raise BusinessRuleBrokenException(rule)

    def __eq__(self, other) -> bool:
        """Сравнивает две Entity по их идентификатору"""
        if not isinstance(other, Entity):
            return False
        return self.id == other.id

    def __hash__(self) -> int:
        """Возвращает хэш Entity на основе её идентификатора"""
        return hash(self.id)