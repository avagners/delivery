from abc import ABC
from dataclasses import dataclass, field

from core.domain.model.shared_kernel.business_rule_exception import BusinessRule, BusinessRuleBrokenException

import uuid


@dataclass
class Entity(ABC):
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