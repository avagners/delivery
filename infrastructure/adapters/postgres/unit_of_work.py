from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session

from infrastructure.adapters.postgres.order_repository import OrderRepositoryImpl
from infrastructure.adapters.postgres.courier_repository import CourierRepositoryImpl


class UnitOfWork:
    """Unit of Work для управления транзакциями и репозиториями"""

    def __init__(self, connection_string: str):
        self.engine = create_engine(connection_string)
        self.session_factory = scoped_session(
            sessionmaker(bind=self.engine, autocommit=False, autoflush=False)
        )

    def __enter__(self):
        self.session = self.session_factory()
        self.orders = OrderRepositoryImpl(self.session)
        self.couriers = CourierRepositoryImpl(self.session)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is not None:
            self.session.rollback()
        else:
            self.session.commit()
        self.session.close()
