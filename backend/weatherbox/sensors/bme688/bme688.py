from typing import NamedTuple

import adafruit_bme680
import board
import busio

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
    # iaq: int


def read() -> BME688Data:
    return BME688Data(
        temperature=round(bme680.temperature, 2),
        humidity=round(bme680.relative_humidity, 2),
        pressure=round(bme680.pressure, 2),
        gas=bme680.gas,
    )


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
