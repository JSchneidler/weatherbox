from datetime import datetime
from typing import NamedTuple

import adafruit_bme680
import board
import busio

from weatherbox.db import get_session
from weatherbox.models import BME688

I2C_ADDRESS = 0x77
I2C_BUS = 1

i2c_bus0 = busio.I2C(board.D1, board.D0)
i2c_bus1 = board.I2C()

bme680 = adafruit_bme680.Adafruit_BME680_I2C(i2c_bus1, I2C_ADDRESS)

# For Denver, CO
bme680.sea_level_pressure = 833.32


class BME688Data(NamedTuple):
    temperature: float
    humidity: float
    pressure: float
    gas: int
    altitude: float


def read() -> BME688Data:
    return BME688Data(
        temperature=bme680.temperature,
        humidity=bme680.relative_humidity,
        pressure=bme680.pressure,
        gas=bme680.gas,
        altitude=bme680.altitude,
    )


def read_and_store():
    data = read()

    bme688_data = BME688(
        timestamp=datetime.now().isoformat(),
        temperature=data.temperature,
        humidity=data.humidity,
        pressure=data.pressure,
        gas=data.gas,
        altitude=data.altitude,
    )
    session = get_session()
    session.add(bme688_data)
    session.commit()


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
