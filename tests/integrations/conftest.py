import pytest
from sqlalchemy import create_engine

from config import DATABASE_URL
from infrastructure.adapters.postgres.models import metadata
from infrastructure.adapters.postgres.unit_of_work import UnitOfWork


@pytest.fixture(scope="session")
def db_engine():
    engine = create_engine(DATABASE_URL)
    yield engine
    engine.dispose()


@pytest.fixture(autouse=True)
def reset_database(db_engine):
    metadata.drop_all(db_engine)    # Удаляет все таблицы
    metadata.create_all(db_engine)  # Создаёт таблицы заново


@pytest.fixture
def uow(db_engine):
    return UnitOfWork(connection_string=DATABASE_URL)
