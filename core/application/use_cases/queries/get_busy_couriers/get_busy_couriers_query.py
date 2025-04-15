from dataclasses import dataclass


@dataclass(frozen=True)
class GetBusyCouriersQuery:
    pass  # Параметров нет, просто получить всех "занятых" курьеров.
