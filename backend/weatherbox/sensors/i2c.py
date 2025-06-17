# https://github.com/dvsu/sps30/blob/b732f2af929ab7a824b3c95f84c2b499a08bac7d/i2c/i2c.py
import io
from fcntl import ioctl

from weatherbox.sensors.i2c_manager import i2c_manager

I2C_SLAVE = 0x0703


class I2C:

    def __init__(self, bus: int, address: int):
        self.bus = bus

        self.fr = io.open("/dev/i2c-" + str(bus), "rb", buffering=0)
        self.fw = io.open("/dev/i2c-" + str(bus), "wb", buffering=0)

        # set device address
        ioctl(self.fr, I2C_SLAVE, address)
        ioctl(self.fw, I2C_SLAVE, address)

    async def write(self, data: list):
        async with i2c_manager.acquire_bus(self.bus):
            self.fw.write(bytearray(data))

    async def read(self, nbytes: int) -> list:
        async with i2c_manager.acquire_bus(self.bus):
            return list(self.fr.read(nbytes))

    def close(self):
        self.fw.close()
        self.fr.close()
