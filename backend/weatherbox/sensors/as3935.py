from weatherbox.db import get_session
from weatherbox.models import AS3935

I2C_ADDRESS = 0x03
I2C_BUS = 1


def setup_trigger():
    pass


def register_strike(timestamp: str, distance: int, energy: int):
    as3935 = AS3935(timestamp=timestamp, distance=distance, energy=energy)
    session = get_session()
    session.add(as3935)
    session.commit()
