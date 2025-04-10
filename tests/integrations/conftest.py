import pytest
from sqlalchemy import create_engine

from config import DATABASE_URL
from infrastructure.adapters.postgres.models import metadata
from infrastructure.adapters.postgres.unit_of_work import UnitOfWork


@pytest.fixture(scope="session")
def db_engine():
    engine = create_engine(DATABASE_URL)
    metadata.drop_all(engine)
    metadata.create_all(engine)
    yield engine
    engine.dispose()


@pytest.fixture
def uow(db_engine):
    return UnitOfWork(connection_string=DATABASE_URL)
