"""Engine and session factory for the THEA Postgres database."""

from collections.abc import Iterator
from contextlib import contextmanager

from sqlalchemy import Engine, create_engine
from sqlalchemy.orm import Session, sessionmaker


def make_engine(database_url: str, *, echo: bool = False) -> Engine:
    # psycopg3 driver; callers pass the plain postgresql:// URL from settings.
    url = database_url.replace("postgresql://", "postgresql+psycopg://", 1)
    return create_engine(url, echo=echo, pool_pre_ping=True)


def make_session_factory(engine: Engine) -> sessionmaker[Session]:
    return sessionmaker(engine, expire_on_commit=False)


@contextmanager
def transaction(factory: sessionmaker[Session]) -> Iterator[Session]:
    """One unit of work: commits on success, rolls back on any error."""
    with factory.begin() as session:
        yield session
