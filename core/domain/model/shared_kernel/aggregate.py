from abc import ABC
import uuid
from dataclasses import dataclass

from core.domain.model.shared_kernel.business_rule_exception import BusinessRule, BusinessRuleBrokenException


@dataclass
class Aggregate(ABC):
    """Базовый класс для Aggregate Root"""

    id: uuid.UUID

    def check_rule(self, rule: BusinessRule):
        """Проверяет, нарушено ли бизнес-правило. Если нарушено, выбрасывает исключение."""
        if rule.is_broken():
            raise BusinessRuleBrokenException(rule)

    def __eq__(self, other):
        if not isinstance(other, Aggregate):
            return False
        return self.id == other.id

    def __hash__(self):
        return hash(self.id)
