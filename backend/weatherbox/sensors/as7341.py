from datetime import datetime
from typing import NamedTuple

import adafruit_as7341


from weatherbox.db import get_session
from weatherbox.models import AS7341
from weatherbox.sensors.i2c_manager import get_i2c_bus, i2c_manager

I2C_ADDRESS = 0x39
I2C_BUS = 1


as7341 = adafruit_as7341.AS7341(get_i2c_bus(I2C_BUS), I2C_ADDRESS)


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


async def read() -> AS7341Data:
    async with i2c_manager.acquire_bus(I2C_BUS):
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


async def read_and_store():
    data = await read()

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
