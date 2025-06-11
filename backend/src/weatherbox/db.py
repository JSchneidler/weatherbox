from datetime import datetime
from os import getenv

from sqlmodel import Session, create_engine

engine = create_engine(f"sqlite:///weatherbox-{getenv('ENV', 'dev')}.db")


def get_session():
    """Get a session."""
    return Session(engine)


def db_now():
    return datetime.now().isoformat()
