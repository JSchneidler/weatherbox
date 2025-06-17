from datetime import datetime
from typing import NamedTuple

import adafruit_as7341
import board
import busio

from weatherbox.db import get_session
from weatherbox.models import AS7341

I2C_ADDRESS = 0x39
I2C_BUS = 0

i2c_bus0 = busio.I2C(board.D1, board.D0)
i2c_bus1 = board.I2C()

as7341 = adafruit_as7341.AS7341(i2c_bus1, I2C_ADDRESS)


class AS7341Data(NamedTuple):
    violet: int
    indigo: int
    blue: int
    cyan: int
    green: int
    yellow: int
    orange: int
    red: int
    clear: int
    nir: int


def read() -> AS7341Data:
    return AS7341Data(
        violet=as7341.channel_415nm,
        indigo=as7341.channel_445nm,
        blue=as7341.channel_480nm,
        cyan=as7341.channel_515nm,
        green=as7341.channel_555nm,
        yellow=as7341.channel_590nm,
        orange=as7341.channel_630nm,
        red=as7341.channel_680nm,
        clear=as7341.channel_clear,
        nir=as7341.channel_nir,
    )


def read_and_store():
    data = read()

    as7341_data = AS7341(
        timestamp=datetime.now().isoformat(),
        violet=data.violet,
        indigo=data.indigo,
        blue=data.blue,
        cyan=data.cyan,
        green=data.green,
        yellow=data.yellow,
        orange=data.orange,
        red=data.red,
        clear=data.clear,
        nir=data.nir,
    )
    session = get_session()
    session.add(as7341_data)
    session.commit()
