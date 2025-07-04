from datetime import datetime, timezone
from os import getenv

from sqlmodel import Session, SQLModel, create_engine

from weatherbox.models import *

engine = create_engine(f"sqlite:///weatherbox-{getenv('ENV', 'dev')}.db")

SQLModel.metadata.create_all(engine)


def get_session():
    """Get a session."""
    return Session(engine)


def utc_timestamp():
    return datetime.now(timezone.utc).isoformat()
