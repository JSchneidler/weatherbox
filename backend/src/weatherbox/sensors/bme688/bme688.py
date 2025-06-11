# import bme280
# from smbus2 import SMBus

from typing import NamedTuple

from weatherbox.i2c_manager import i2c_manager


class BME688Data(NamedTuple):
    temperature: float
    humidity: float
    pressure: float
    iaq: int


# bus = SMBus(1)


I2C_ADDRESS = 0x76
I2C_BUS = 0

# calibration_params = bme280.load_calibration_params(bus, I2C_ADDRESS)


# def read():
#     data = bme280.sample(bus, I2C_ADDRESS, calibration_params)
#     return BME280Data(
#         temperature=round(data.temperature, 2),
#         humidity=round(data.humidity, 2),
#         pressure=round(data.pressure, 2),
#     )


async def read() -> BME688Data:
    async with i2c_manager.acquire_bus(I2C_BUS):
        pass


async def read_and_store():
    async with i2c_manager.acquire_bus(I2C_BUS):
        pass
