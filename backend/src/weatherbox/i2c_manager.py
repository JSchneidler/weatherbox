import asyncio
from contextlib import asynccontextmanager


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
