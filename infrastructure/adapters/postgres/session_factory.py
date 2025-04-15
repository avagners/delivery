from typing import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from contextlib import contextmanager

from config import DATABASE_URL


def create_session(connection_string: str = DATABASE_URL):
    engine = create_engine(connection_string, future=True)
    SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

    @contextmanager
    def session_scope() -> Generator[Session, None, None]:
        session = SessionLocal()
        try:
            yield session
            session.commit()
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()

    return session_scope()
