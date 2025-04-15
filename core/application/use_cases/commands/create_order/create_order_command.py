import uuid
from dataclasses import dataclass


@dataclass(frozen=True)
class CreateOrderCommand:
    basket_id: uuid.UUID
    street: str
