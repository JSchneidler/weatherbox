from typing import Optional

from sqlmodel import Field, SQLModel


# https://www.adafruit.com/product/4698
class AS7341(SQLModel, table=True):
    """Timestamped AS7341 spectrometer data."""

    id: Optional[int] = Field(default=None, primary_key=True)
    timestamp: str = Field(index=True, nullable=False)
    violet: float = Field(nullable=False)
    indigo: float = Field(nullable=False)
    blue: float = Field(nullable=False)
    cyan: float = Field(nullable=False)
    green: float = Field(nullable=False)
    yellow: float = Field(nullable=False)
    orange: float = Field(nullable=False)
    red: float = Field(nullable=False)
    clear: float = Field(nullable=False)
    nir: float = Field(nullable=False)
