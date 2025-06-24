import logging
from typing import NamedTuple

import adafruit_ens160

from weatherbox.db import get_session, utc_timestamp
from weatherbox.models import ENS160 as ENS160Model
from weatherbox.sensors.i2c_manager import get_i2c_bus, i2c_manager
from weatherbox.sensors.Sensor import I2CSensor


DEFAULT_I2C_ADDRESS = 0x53


class ENS160Data(NamedTuple):
    aqi: int
    tvoc: int
    eco2: int


class ENS160(I2CSensor):
    ens160: adafruit_ens160.ENS160

    def __init__(self, i2c_bus: int, i2c_address: int = DEFAULT_I2C_ADDRESS):
        super().__init__(
            name="ENS160",
            i2c_address=i2c_address,
            i2c_bus=i2c_bus,
        )

    async def initialize(self) -> bool:
        async with i2c_manager.acquire_bus(self.i2c_bus):
            self.ens160 = adafruit_ens160.ENS160(
                get_i2c_bus(self.i2c_bus), self.i2c_address
            )
        logging.info("ENS160 initialized")
        return await super().initialize()

    async def read(self) -> ENS160Data:
        async with i2c_manager.acquire_bus(self.i2c_bus):
            return ENS160Data(
                aqi=self.ens160.AQI,
                tvoc=self.ens160.TVOC,
                eco2=self.ens160.eCO2,
            )

    async def read_and_store(self):
        data = await self.read()

        ens160_data = ENS160Model(
            timestamp=utc_timestamp(),
            aqi=data.aqi,
            tvoc=data.tvoc,
            eco2=data.eco2,
        )
        session = get_session()
        session.add(ens160_data)
        session.commit()

        logging.info("Sampled ENS160")
