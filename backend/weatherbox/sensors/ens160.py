import logging
from typing import NamedTuple

import adafruit_ens160

from weatherbox.db import get_session, utc_timestamp
from weatherbox.models import ENS160
from weatherbox.sensors.i2c_manager import get_i2c_bus, i2c_manager


I2C_ADDRESS = 0x53
I2C_BUS = 1

ens160 = adafruit_ens160.ENS160(get_i2c_bus(I2C_BUS), I2C_ADDRESS)


class ENS160Data(NamedTuple):
    aqi: int
    tvoc: int
    eco2: int


async def read() -> ENS160Data:
    async with i2c_manager.acquire_bus(I2C_BUS):
        return ENS160Data(
            aqi=ens160.AQI,
            tvoc=ens160.TVOC,
            eco2=ens160.eCO2,
        )


async def read_and_store():
    data = await read()

    ens160_data = ENS160(
        timestamp=utc_timestamp(),
        aqi=data.aqi,
        tvoc=data.tvoc,
        eco2=data.eco2,
    )
    session = get_session()
    session.add(ens160_data)
    session.commit()

    logging.info("Sampled ENS160")
