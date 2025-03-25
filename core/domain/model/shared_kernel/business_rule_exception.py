from abc import ABC, abstractmethod


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
