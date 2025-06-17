from datetime import datetime
from typing import NamedTuple

import adafruit_ens160
import board
import busio

from weatherbox.db import get_session
from weatherbox.models import ENS160


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


def read_and_store():
    data = read()

    ens160_data = ENS160(
        timestamp=datetime.now().isoformat(),
        aqi=data.aqi,
        tvoc=data.tvoc,
        eco2=data.eco2,
    )
    session = get_session()
    session.add(ens160_data)
    session.commit()
