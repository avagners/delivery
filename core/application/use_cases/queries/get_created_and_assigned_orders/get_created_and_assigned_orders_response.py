from dataclasses import dataclass
from typing import List
from uuid import UUID


@dataclass
class Location:
    x: int
    y: int


@dataclass
class OrderDTO:
    id: UUID
    location: Location


@dataclass
class GetCreatedAndAssignedOrdersResponse:
    orders: List[OrderDTO]
