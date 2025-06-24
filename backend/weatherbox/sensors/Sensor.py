from abc import ABC, abstractmethod
from enum import Enum
from typing import Optional


class SensorStatus(Enum):
    DISABLED = "disabled"
    OFF = "off"
    INITIALIZING = "initializing"
    WARMING_UP = "warming_up"
    READY = "ready"
    ERROR = "error"


class Sensor(ABC):
    """
    Base class for all sensors in the WeatherBox system.
    """

    name: str
    status: SensorStatus
    error: Optional[str]

    def __init__(self, name: str):
        self.name = name
        self.status = SensorStatus.OFF
        self.error = None

    async def initialize(self) -> bool:
        """
        Initialize the sensor.
        This method should be overridden and then called by subclasses to perform generic and specific initialization tasks.
        Returns True if initialization is successful, False otherwise.
        """
        self.status = SensorStatus.READY
        return True

    async def deinitialize(self) -> bool:
        """
        Deinitialize the sensor.
        This method should be overridden and then called by subclasses to perform generic and specific deinitialization tasks.
        Returns True if deinitialization is successful, False otherwise.
        """
        self.status = SensorStatus.OFF
        return True

    def is_ready(self) -> bool:
        """
        Check if the sensor is ready for operation.
        Returns True if the sensor status is READY, False otherwise.
        """
        return self.status == SensorStatus.READY

    def get_settings(self) -> dict:
        """
        Get the settings of the sensor.
        This method should be overridden and then called by subclasses to return generic and specific sensor settings.
        Returns a dictionary containing sensor settings.
        """
        return {
            "disabled": self.status == SensorStatus.DISABLED,
        }

    @abstractmethod
    async def read(self) -> object:
        """
        Read data from the sensor.
        This method should be overridden by subclasses to perform specific read operations.
        Returns the sensor data in a format defined by the subclass.
        """
        pass

    @abstractmethod
    async def read_and_store(self):
        """
        Read data from the sensor and store it in the database.
        This method should be overridden by subclasses to perform specific read and store operations.
        """
        pass


class I2CSensor(Sensor):
    """
    Base class for I2C sensors.
    Inherits from Sensor and provides additional functionality for I2C communication.
    """

    def __init__(self, name: str, i2c_bus: int, i2c_address: int):
        super().__init__(name)
        self.i2c_bus = i2c_bus
        self.i2c_address = i2c_address

    def get_settings(self) -> dict:
        """
        Get the settings of the sensor.
        This method should be overridden and then called by subclasses to return generic and specific sensor settings.
        Returns a dictionary containing sensor settings.
        """
        return {
            **super().get_settings(),
            "i2c_bus": self.i2c_bus,
            "i2c_address": self.i2c_address,
        }
