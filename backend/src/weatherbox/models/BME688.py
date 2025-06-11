from typing import Optional

from sqlmodel import Field, SQLModel


# https://www.adafruit.com/product/5046
class BME688(SQLModel, table=True):
    """Timestamped BME688 data with temperature, humidity, pressure, and IAQ."""

    id: Optional[int] = Field(default=None, primary_key=True)
    timestamp: str = Field(index=True, nullable=False)
    temperature: float = Field(nullable=False)
    humidity: float = Field(nullable=False)
    pressure: float = Field(nullable=False)
    iaq: float = Field(nullable=False)
