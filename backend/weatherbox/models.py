from typing import Optional

from sqlmodel import Field, SQLModel


# https://www.sparkfun.com/sparkfun-lightning-detector-as3935.html
class AS3935(SQLModel, table=True):
    """Timestamped AS3935 lightning detector data."""

    id: Optional[int] = Field(default=None, primary_key=True)
    timestamp: str = Field(index=True, nullable=False)
    distance: int = Field(nullable=False)
    energy: int = Field(nullable=False)


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


# https://www.adafruit.com/product/5046
class BME688(SQLModel, table=True):
    """Timestamped BME688 data with temperature, humidity, pressure, gas, and altitude."""

    id: Optional[int] = Field(default=None, primary_key=True)
    timestamp: str = Field(index=True, nullable=False)
    temperature: float = Field(nullable=False)
    humidity: float = Field(nullable=False)
    pressure: float = Field(nullable=False)
    gas: int = Field(nullable=False)
    altitude: float = Field(nullable=False)


# https://www.adafruit.com/product/5606
class ENS160(SQLModel, table=True):
    """Timestamped ENS160 MOX gas sensor data."""

    id: Optional[int] = Field(default=None, primary_key=True)
    timestamp: str = Field(index=True, nullable=False)
    aqi: float = Field(nullable=False)
    tvoc: float = Field(nullable=False)
    eco2: float = Field(nullable=False)


# https://www.adafruit.com/product/4831
class LTR390(SQLModel, table=True):
    """Timestamped LTR390 UV sensor data."""

    id: Optional[int] = Field(default=None, primary_key=True)
    timestamp: str = Field(index=True, nullable=False)
    uvs: float = Field(nullable=False)
    # uvi: float = Field(nullable=False)
    light: float = Field(nullable=False)
    # lux: float = Field(nullable=False)


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


class TimelapseImage(SQLModel, table=True):
    """An image from a timelapse."""

    id: Optional[int] = Field(default=None, primary_key=True)
    timestamp: str = Field(index=True, nullable=False)
    file_name: str = Field(max_length=255, nullable=False)
