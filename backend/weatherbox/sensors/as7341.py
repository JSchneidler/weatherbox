import logging
from typing import NamedTuple

import adafruit_as7341

from weatherbox.db import get_session, utc_timestamp
from weatherbox.models import AS7341 as AS7341Model
from weatherbox.sensors.i2c_manager import get_i2c_bus, i2c_manager
from weatherbox.sensors.Sensor import I2CSensor


DEFAULT_I2C_ADDRESS = 0x39


class AS7341Data(NamedTuple):
    violet: int
    indigo: int
    blue: int
    cyan: int
    green: int
    yellow: int
    orange: int
    red: int
    clear: int
    nir: int


class AS7341(I2CSensor):
    as7341: adafruit_as7341.AS7341

    def __init__(self, i2c_bus: int, i2c_address: int = DEFAULT_I2C_ADDRESS):
        super().__init__(
            name="AS7341",
            i2c_address=i2c_address,
            i2c_bus=i2c_bus,
        )

    async def initialize(self) -> bool:
        async with i2c_manager.acquire_bus(self.i2c_bus):
            self.as7341 = adafruit_as7341.AS7341(
                get_i2c_bus(self.i2c_bus), self.i2c_address
            )

        logging.info("AS7341 initialized")
        return await super().initialize()

    async def read(self) -> AS7341Data:
        async with i2c_manager.acquire_bus(self.i2c_bus):
            return AS7341Data(
                violet=self.as7341.channel_415nm,
                indigo=self.as7341.channel_445nm,
                blue=self.as7341.channel_480nm,
                cyan=self.as7341.channel_515nm,
                green=self.as7341.channel_555nm,
                yellow=self.as7341.channel_590nm,
                orange=self.as7341.channel_630nm,
                red=self.as7341.channel_680nm,
                clear=self.as7341.channel_clear,
                nir=self.as7341.channel_nir,
            )

    async def read_and_store(self):
        data = await self.read()

        as7341_data = AS7341Model(
            timestamp=utc_timestamp(),
            violet=data.violet,
            indigo=data.indigo,
            blue=data.blue,
            cyan=data.cyan,
            green=data.green,
            yellow=data.yellow,
            orange=data.orange,
            red=data.red,
            clear=data.clear,
            nir=data.nir,
        )
        session = get_session()
        session.add(as7341_data)
        session.commit()

        logging.info("Sampled AS7341")
