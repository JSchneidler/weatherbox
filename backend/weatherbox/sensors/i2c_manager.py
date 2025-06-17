import asyncio
from contextlib import asynccontextmanager
import board
import busio


i2c_bus0 = busio.I2C(board.D1, board.D0)
i2c_bus1 = board.I2C()


def get_i2c_bus(bus_number: int):
    if bus_number == 0:
        return i2c_bus0
    elif bus_number == 1:
        return i2c_bus1
    else:
        raise ValueError(f"Invalid I2C bus number: {bus_number}")


class I2CManager:
    def __init__(self):
        self._lock_bus_0 = asyncio.Lock()
        self._lock_bus_1 = asyncio.Lock()

    @asynccontextmanager
    async def acquire_bus(self, bus_number: int):
        if bus_number == 0:
            async with self._lock_bus_0:
                yield
        elif bus_number == 1:
            async with self._lock_bus_1:
                yield
        else:
            raise ValueError(f"Invalid I2C bus number: {bus_number}")


i2c_manager = I2CManager()
