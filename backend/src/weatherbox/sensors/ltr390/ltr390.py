from weatherbox.i2c_manager import i2c_manager


I2C_ADDRESS = 0x53
I2C_BUS = 0


async def read_and_store():
    async with i2c_manager.acquire_bus(I2C_BUS):
        pass
