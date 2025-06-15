from typing import NamedTuple

import adafruit_ltr390
import board
import busio

I2C_ADDRESS = 0x53
I2C_BUS = 1

i2c_bus0 = busio.I2C(board.D1, board.D0)
i2c_bus1 = board.I2C()

ltr390 = adafruit_ltr390.LTR390(i2c_bus1, I2C_ADDRESS)


class LTR390Data(NamedTuple):
    light: int
    uvs: int


def read():
    return LTR390Data(light=ltr390.light, uvs=ltr390.uvs)


# async def read_and_store():
#     async with i2c_manager.acquire_bus(I2C_BUS):
#         pass
