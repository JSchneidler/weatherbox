from typing import Optional

from sqlmodel import Field, SQLModel


# https://www.sparkfun.com/sparkfun-lightning-detector-as3935.html
class AS3935(SQLModel, table=True):
    """Timestamped AS3935 lightning detector data."""

    id: Optional[int] = Field(default=None, primary_key=True)
    timestamp: str = Field(index=True, nullable=False)
    distance: int = Field(nullable=False)
    energy: int = Field(nullable=False)
