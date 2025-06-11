from typing import Optional

from sqlmodel import Field, SQLModel


# https://www.adafruit.com/product/5606
class ENS160(SQLModel, table=True):
    """Timestamped ENS160 MOX gas sensor data."""

    id: Optional[int] = Field(default=None, primary_key=True)
    timestamp: str = Field(index=True, nullable=False)
    aqi: float = Field(nullable=False)
    tvoc: float = Field(nullable=False)
    eco2: float = Field(nullable=False)
