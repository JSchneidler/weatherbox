from typing import Optional

from sqlmodel import Field, SQLModel


# https://www.adafruit.com/product/4831
class LTR390(SQLModel, table=True):
    """Timestamped LTR390 UV sensor data."""

    id: Optional[int] = Field(default=None, primary_key=True)
    timestamp: str = Field(index=True, nullable=False)
    uvs: float = Field(nullable=False)
    uvi: float = Field(nullable=False)
    light: float = Field(nullable=False)
    lux: float = Field(nullable=False)
