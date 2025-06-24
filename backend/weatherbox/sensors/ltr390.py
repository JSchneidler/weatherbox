import logging
from typing import NamedTuple

import adafruit_ltr390

from weatherbox.db import get_session, utc_timestamp
from weatherbox.models import LTR390 as LTR390Model
from weatherbox.sensors.i2c_manager import get_i2c_bus, i2c_manager
from weatherbox.sensors.Sensor import I2CSensor


DEFAULT_I2C_ADDRESS = 0x53


class LTR390Data(NamedTuple):
    light: int
    uvs: int


class LTR390(I2CSensor):
    ltr390: adafruit_ltr390.LTR390

    def __init__(self, i2c_bus: int, i2c_address: int = DEFAULT_I2C_ADDRESS):
        super().__init__(
            name="LTR390",
            i2c_address=i2c_address,
            i2c_bus=i2c_bus,
        )

    async def initialize(self) -> bool:
        async with i2c_manager.acquire_bus(self.i2c_bus):
            self.ltr390 = adafruit_ltr390.LTR390(
                get_i2c_bus(self.i2c_bus), self.i2c_address
            )

        logging.info("LTR390 initialized")
        return await super().initialize()

    async def read(self) -> LTR390Data:
        async with i2c_manager.acquire_bus(self.i2c_bus):
            return LTR390Data(light=self.ltr390.light, uvs=self.ltr390.uvs)

    async def read_and_store(self):
        data = await self.read()

        ltr390_data = LTR390Model(
            timestamp=utc_timestamp(),
            light=data.light,
            uvs=data.uvs,
        )
        session = get_session()
        session.add(ltr390_data)
        session.commit()

        logging.info("Sampled LTR390")
