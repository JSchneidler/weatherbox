from typing import NamedTuple

import adafruit_ens160
import board
import busio


I2C_ADDRESS = 0x53
I2C_BUS = 1

i2c_bus0 = busio.I2C(board.D1, board.D0)
i2c_bus1 = board.I2C()

ens160 = adafruit_ens160.ENS160(i2c_bus0, I2C_ADDRESS)


class ENS160Data(NamedTuple):
    aqi: int
    tvoc: int
    eco2: int


def read() -> ENS160Data:
    return ENS160Data(
        aqi=ens160.AQI,
        tvoc=ens160.TVOC,
        eco2=ens160.eCO2,
    )
