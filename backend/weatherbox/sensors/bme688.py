import logging
from typing import NamedTuple

import adafruit_bme680

from weatherbox.db import get_session, utc_timestamp
from weatherbox.models import BME688 as BME688Model
from weatherbox.sensors.i2c_manager import get_i2c_bus, i2c_manager
from weatherbox.sensors.Sensor import I2CSensor

DEFAULT_I2C_ADDRESS = 0x77
SEA_LEVEL_PRESSURE = 833.32


class BME688Data(NamedTuple):
    temperature: float
    humidity: float
    pressure: float
    gas: int
    altitude: float


class BME688(I2CSensor):
    bme680: adafruit_bme680.Adafruit_BME680_I2C

    def __init__(self, i2c_bus: int, i2c_address: int = DEFAULT_I2C_ADDRESS):
        super().__init__(
            name="BME688",
            i2c_address=i2c_address,
            i2c_bus=i2c_bus,
        )

    async def initialize(self) -> bool:
        async with i2c_manager.acquire_bus(self.i2c_bus):
            self.bme680 = adafruit_bme680.Adafruit_BME680_I2C(
                get_i2c_bus(self.i2c_bus), self.i2c_address
            )
            self.bme680.sea_level_pressure = SEA_LEVEL_PRESSURE

        logging.info("BME688 initialized")
        return await super().initialize()

    def get_settings(self) -> dict:
        """
        Get the settings of the BME688 sensor.
        This method overrides the base class method to include specific settings for BME688.
        Returns a dictionary containing sensor settings.
        """
        return {
            **super().get_settings(),
            "sea_level_pressure": SEA_LEVEL_PRESSURE,
        }

    async def read(self) -> BME688Data:
        async with i2c_manager.acquire_bus(self.i2c_bus):
            return BME688Data(
                temperature=self.bme680.temperature,
                humidity=self.bme680.relative_humidity,
                pressure=self.bme680.pressure,
                gas=self.bme680.gas,
                altitude=self.bme680.altitude,
            )

    async def read_and_store(self):
        data = await self.read()

        bme688_data = BME688Model(
            timestamp=utc_timestamp(),
            temperature=data.temperature,
            humidity=data.humidity,
            pressure=data.pressure,
            gas=data.gas,
            altitude=data.altitude,
        )
        session = get_session()
        session.add(bme688_data)
        session.commit()

        logging.info("Sampled BME688")
