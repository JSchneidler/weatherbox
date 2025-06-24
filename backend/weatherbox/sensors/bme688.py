import logging
from typing import NamedTuple

import adafruit_bme680

from weatherbox.db import get_session, utc_timestamp
from weatherbox.models import BME688
from weatherbox.sensors.i2c_manager import get_i2c_bus, i2c_manager

I2C_ADDRESS = 0x77
I2C_BUS = 1

bme680 = adafruit_bme680.Adafruit_BME680_I2C(get_i2c_bus(I2C_BUS), I2C_ADDRESS)

# For Denver, CO
bme680.sea_level_pressure = 833.32


class BME688Data(NamedTuple):
    temperature: float
    humidity: float
    pressure: float
    gas: int
    altitude: float


async def read() -> BME688Data:
    async with i2c_manager.acquire_bus(I2C_BUS):
        return BME688Data(
            temperature=bme680.temperature,
            humidity=bme680.relative_humidity,
            pressure=bme680.pressure,
            gas=bme680.gas,
            altitude=bme680.altitude,
        )


async def read_and_store():
    data = await read()

    bme688_data = BME688(
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


# async def read() -> BME688Data:
#     return BME688Data(
#         temperature=round(bme680.temperature, 2),
#         humidity=round(bme680.relative_humidity, 2),
#         pressure=round(bme680.pressure, 2),
#         gas=bme680.gas,
#     )


# async def read_and_store():
#     async with i2c_manager.acquire_bus(I2C_BUS):
#         pass
