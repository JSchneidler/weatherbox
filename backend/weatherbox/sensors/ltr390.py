from datetime import datetime
from typing import NamedTuple

import adafruit_ltr390

from weatherbox.db import get_session
from weatherbox.models import LTR390
from weatherbox.sensors.i2c_manager import get_i2c_bus, i2c_manager

I2C_ADDRESS = 0x53
I2C_BUS = 1

ltr390 = adafruit_ltr390.LTR390(get_i2c_bus(I2C_BUS), I2C_ADDRESS)


class LTR390Data(NamedTuple):
    light: int
    uvs: int


async def read() -> LTR390Data:
    async with i2c_manager.acquire_bus(I2C_BUS):
        return LTR390Data(light=ltr390.light, uvs=ltr390.uvs)


async def read_and_store():
    data = await read()

    ltr390_data = LTR390(
        timestamp=datetime.now().isoformat(),
        light=data.light,
        uvs=data.uvs,
    )
    session = get_session()
    session.add(ltr390_data)
    session.commit()


# async def read_and_store():
#     async with i2c_manager.acquire_bus(I2C_BUS):
#         pass
