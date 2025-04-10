import uuid

from sqlalchemy import Column, Integer, String, Enum as SQLEnum, ForeignKey, MetaData
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import declarative_base

from core.domain.model.courier_aggregate.courier_status import CourierStatusValue
from core.domain.model.order_aggregate.order_status import OrderStatusValue

metadata = MetaData()
Base = declarative_base(metadata=metadata)


class CourierModel(Base):
    """Модель SQLAlchemy для курьера"""
    __tablename__ = 'couriers'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)
    transport_name = Column(String, nullable=False)
    transport_speed = Column(Integer, nullable=False)
    location_x = Column(Integer, nullable=False)
    location_y = Column(Integer, nullable=False)
    status = Column(SQLEnum(CourierStatusValue), nullable=False)


class OrderModel(Base):
    """Модель SQLAlchemy для заказа"""
    __tablename__ = 'orders'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    location_x = Column(Integer, nullable=False)
    location_y = Column(Integer, nullable=False)
    status = Column(SQLEnum(OrderStatusValue), nullable=False)
    courier_id = Column(UUID(as_uuid=True), ForeignKey('couriers.id'), nullable=True)
