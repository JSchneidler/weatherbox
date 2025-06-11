from typing import Optional

from sqlmodel import Field, SQLModel


# https://www.sparkfun.com/particulate-matter-sensor-sps30.html
class SPS30(SQLModel, table=True):
    """Timestamped SPS30 particulate matter sensor data."""

    id: Optional[int] = Field(default=None, primary_key=True)
    timestamp: str = Field(index=True, nullable=False)
    pm10: float = Field(nullable=False)
    pm25: float = Field(nullable=False)
    pm40: float = Field(nullable=False)
    pm100: float = Field(nullable=False)
    nc05: float = Field(nullable=False)
    nc10: float = Field(nullable=False)
    nc25: float = Field(nullable=False)
    nc40: float = Field(nullable=False)
    nc100: float = Field(nullable=False)
    typical_particle_size: float = Field(nullable=False)
