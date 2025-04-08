from sqlalchemy import create_engine
from infrastructure.adapters.postgres.models import Base

from config import DATABASE_URL


def init_db():
    engine = create_engine(DATABASE_URL)
    Base.metadata.create_all(engine)
    print("Database tables created successfully")


if __name__ == "__main__":
    init_db()
