from dataclasses import dataclass


@dataclass(frozen=True)
class MoveCouriersCommand:
    pass  # Нет полей, всё логика внутри Handler
