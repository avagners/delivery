from dataclasses import dataclass
from typing import List


@dataclass(frozen=True)
class Location:
    x: int
    y: int


@dataclass(frozen=True)
class CourierDTO:
    id: int
    name: str
    location: Location


@dataclass(frozen=True)
class GetBusyCouriersResponse:
    couriers: List[CourierDTO]
