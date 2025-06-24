import asyncio
import logging
import sys
from queue import Queue
from typing import Dict, NamedTuple

from weatherbox.db import get_session, utc_timestamp
from weatherbox.models import SPS30 as SPS30Model
from weatherbox.sensors.i2c import I2C
from weatherbox.sensors.Sensor import I2CSensor, SensorStatus

DEFAULT_I2C_ADDRESS = 0x69

# https://github.com/dvsu/sps30/blob/b732f2af929ab7a824b3c95f84c2b499a08bac7d/sps30.py
# I2C commands
CMD_START_MEASUREMENT = [0x00, 0x10]
CMD_STOP_MEASUREMENT = [0x01, 0x04]
CMD_READ_DATA_READY_FLAG = [0x02, 0x02]
CMD_READ_MEASURED_VALUES = [0x03, 0x00]
CMD_SLEEP = [0x10, 0x01]
CMD_WAKEUP = [0x11, 0x03]
CMD_START_FAN_CLEANING = [0x56, 0x07]
CMD_AUTO_CLEANING_INTERVAL = [0x80, 0x04]
CMD_PRODUCT_TYPE = [0xD0, 0x02]
CMD_SERIAL_NUMBER = [0xD0, 0x33]
CMD_FIRMWARE_VERSION = [0xD1, 0x00]
CMD_READ_STATUS_REGISTER = [0xD2, 0x06]
CMD_CLEAR_STATUS_REGISTER = [0xD2, 0x10]
CMD_RESET = [0xD3, 0x04]

# Length of response in bytes
NBYTES_READ_DATA_READY_FLAG = 3
NBYTES_MEASURED_VALUES_FLOAT = 60  # IEEE754 float
NBYTES_MEASURED_VALUES_INTEGER = 30  # unsigned 16 bit integer
NBYTES_AUTO_CLEANING_INTERVAL = 6
NBYTES_PRODUCT_TYPE = 12
NBYTES_SERIAL_NUMBER = 48
NBYTES_FIRMWARE_VERSION = 3
NBYTES_READ_STATUS_REGISTER = 6

# Packet size including checksum byte [data1, data2, checksum]
PACKET_SIZE = 3

# Size of each measurement data packet (PMx) including checksum bytes, in bytes
SIZE_FLOAT = 6  # IEEE754 float
SIZE_INTEGER = 3  # unsigned 16 bit integer


class SPS30Data(NamedTuple):
    mass_density: Dict[str, float]
    particle_count: Dict[str, float]
    particle_size: float


class SPS30(I2CSensor):
    sampling_period: int
    i2c: I2C
    task: asyncio.Task
    __data: Queue
    __valid: Dict[str, bool]

    def __init__(
        self,
        i2c_bus: int,
        i2c_address: int = DEFAULT_I2C_ADDRESS,
        sampling_period: int = 1,
    ):
        super().__init__("SPS30", i2c_bus, i2c_address)
        self.sampling_period = sampling_period
        self.i2c = I2C(self.i2c_bus, self.i2c_address)
        self.__data = Queue(maxsize=20)
        self.__valid = {
            "mass_density": False,
            "particle_count": False,
            "particle_size": False,
        }

    async def initialize(self) -> bool:
        """Initialize SPS30 sensor with proper startup sequence."""
        try:
            # Verify sensor is accessible
            firmware_version = await self.firmware_version()
            product_type = await self.product_type()
            status = await self.read_status_register()

            logging.info(f"SPS30 firmware: {firmware_version}, product: {product_type}")
            logging.info(f"SPS30 status: {status}")

            # Start measurement mode
            await self.start_measurement()

            # Wait for first data to be ready
            max_wait_time = 60  # 60 seconds max wait
            wait_time = 0
            while not await self.read_data_ready_flag():
                await asyncio.sleep(1)
                wait_time += 1
                if wait_time >= max_wait_time:
                    raise TimeoutError("SPS30 data not ready within timeout period")

            logging.info("SPS30 measurement started successfully")

        except Exception as e:
            logging.error(f"SPS30 initialization failed: {e}")
            self.status = SensorStatus.ERROR
            return False

        return await super().initialize()

    async def deinitialize(self) -> bool:
        """Deinitialize SPS30 sensor."""
        try:
            await self.stop_measurement()
        except Exception as e:
            logging.error(f"SPS30 deinitialization failed: {e}")
            self.status = SensorStatus.ERROR
            return False

        return await super().deinitialize()

    async def read(self) -> SPS30Data:
        await self.start_measurement()

        while not await self.read_data_ready_flag():
            await asyncio.sleep(0.1)

        data = await self.get_measurement()
        await self.stop_measurement()

        return SPS30Data(
            mass_density=data["sensor_data"]["mass_density"],
            particle_count=data["sensor_data"]["particle_count"],
            particle_size=data["sensor_data"]["particle_size"],
        )

    async def read_and_store(self):
        if not await self.read_data_ready_flag():
            return  # No data ready, skip this reading

        data = await self.get_measurement()

        if not data:  # Empty data, skip this reading
            return

        sps30_data = SPS30Model(
            timestamp=utc_timestamp(),
            pm10=data["sensor_data"]["mass_density"]["pm1.0"],
            pm25=data["sensor_data"]["mass_density"]["pm2.5"],
            pm40=data["sensor_data"]["mass_density"]["pm4.0"],
            pm100=data["sensor_data"]["mass_density"]["pm10"],
            nc05=data["sensor_data"]["particle_count"]["pm0.5"],
            nc10=data["sensor_data"]["particle_count"]["pm1.0"],
            nc25=data["sensor_data"]["particle_count"]["pm2.5"],
            nc40=data["sensor_data"]["particle_count"]["pm4.0"],
            nc100=data["sensor_data"]["particle_count"]["pm10"],
            typical_particle_size=data["sensor_data"]["particle_size"],
        )
        session = get_session()
        session.add(sps30_data)
        session.commit()

        logging.info("Sampled SPS30")

    def crc_calc(self, data: list) -> int:
        crc = 0xFF
        for i in range(2):
            crc ^= data[i]
            for _ in range(8, 0, -1):
                if crc & 0x80:
                    crc = (crc << 1) ^ 0x31
                else:
                    crc = crc << 1

        # The checksum only contains 8-bit,
        # so the calculated value has to be masked with 0xFF
        return crc & 0x0000FF

    async def firmware_version(self) -> str:
        await self._write(CMD_FIRMWARE_VERSION)
        data = await self._read(NBYTES_FIRMWARE_VERSION)

        if self.crc_calc(data[:2]) != data[2]:
            return "CRC mismatched"

        return ".".join(map(str, data[:2]))

    async def product_type(self) -> str:
        await self._write(CMD_PRODUCT_TYPE)
        data = await self._read(NBYTES_PRODUCT_TYPE)
        result = ""

        for i in range(0, NBYTES_PRODUCT_TYPE, 3):
            if self.crc_calc(data[i : i + 2]) != data[i + 2]:
                return "CRC mismatched"

            result += "".join(map(chr, data[i : i + 2]))

        return result

    async def serial_number(self) -> str:
        await self._write(CMD_SERIAL_NUMBER)
        data = await self._read(NBYTES_SERIAL_NUMBER)
        result = ""

        for i in range(0, NBYTES_SERIAL_NUMBER, PACKET_SIZE):
            if self.crc_calc(data[i : i + 2]) != data[i + 2]:
                return "CRC mismatched"

            result += "".join(map(chr, data[i : i + 2]))

        return result

    async def read_status_register(self) -> dict:
        await self._write(CMD_READ_STATUS_REGISTER)
        data = await self._read(NBYTES_READ_STATUS_REGISTER)

        status = []
        for i in range(0, NBYTES_READ_STATUS_REGISTER, PACKET_SIZE):
            if self.crc_calc(data[i : i + 2]) != data[i + 2]:
                return "CRC mismatched"

            status.extend(data[i : i + 2])

        binary = "{:032b}".format(
            status[0] << 24 | status[1] << 16 | status[2] << 8 | status[3]
        )
        speed_status = "too high/ too low" if int(binary[10]) == 1 else "ok"
        laser_status = "out of range" if int(binary[26]) == 1 else "ok"
        fan_status = "0 rpm" if int(binary[27]) == 1 else "ok"

        return {
            "speed_status": speed_status,
            "laser_status": laser_status,
            "fan_status": fan_status,
        }

    async def clear_status_register(self) -> None:
        await self.i2c.write(CMD_CLEAR_STATUS_REGISTER)

    async def read_data_ready_flag(self) -> bool:
        await self._write(CMD_READ_DATA_READY_FLAG)
        data = await self._read(NBYTES_READ_DATA_READY_FLAG)

        if self.crc_calc(data[:2]) != data[2]:
            logging.warning(
                "'read_data_ready_flag' CRC mismatched!"
                + f"  Data: {data[:2]}"
                + f"  Calculated CRC: {self.crc_calc(data[:2])}"
                + f"  Expected: {data[2]}"
            )

            return False

        return True if data[1] == 1 else False

    async def sleep(self) -> None:
        await self.i2c.write(CMD_SLEEP)

    async def wakeup(self) -> None:
        await self.i2c.write(CMD_WAKEUP)

    async def start_fan_cleaning(self) -> None:
        await self.i2c.write(CMD_START_FAN_CLEANING)

    async def read_auto_cleaning_interval(self) -> int:
        await self._write(CMD_AUTO_CLEANING_INTERVAL)
        data = await self._read(NBYTES_AUTO_CLEANING_INTERVAL)

        interval = []
        for i in range(0, NBYTES_AUTO_CLEANING_INTERVAL, 3):
            if self.crc_calc(data[i : i + 2]) != data[i + 2]:
                return "CRC mismatched"

            interval.extend(data[i : i + 2])

        return interval[0] << 24 | interval[1] << 16 | interval[2] << 8 | interval[3]

    async def write_auto_cleaning_interval_days(self, days: int) -> int:
        seconds = days * 86400  # 1day = 86400sec
        interval = []
        interval.append((seconds & 0xFF000000) >> 24)
        interval.append((seconds & 0x00FF0000) >> 16)
        interval.append((seconds & 0x0000FF00) >> 8)
        interval.append(seconds & 0x000000FF)
        data = CMD_AUTO_CLEANING_INTERVAL
        data.extend([interval[0], interval[1]])
        data.append(self.crc_calc(data[2:4]))
        data.extend([interval[2], interval[3]])
        data.append(self.crc_calc(data[5:7]))
        await self.i2c.write(data)
        await asyncio.sleep(0.05)
        return await self.read_auto_cleaning_interval()

    async def reset(self) -> None:
        await self.i2c.write(CMD_RESET)

    def __ieee754_number_conversion(self, data: int) -> float:
        binary = "{:032b}".format(data)

        sign = int(binary[0:1])
        exp = int(binary[1:9], 2) - 127

        divider = 0
        if exp < 0:
            divider = abs(exp)
            exp = 0

        mantissa = binary[9:]

        real = int(("1" + mantissa[:exp]), 2)
        decimal = mantissa[exp:]

        dec = 0.0
        for i in range(len(decimal)):
            dec += int(decimal[i]) / (2 ** (i + 1))

        if divider == 0:
            return round((((-1) ** (sign) * real) + dec), 3)
        else:
            return round((((-1) ** (sign) * real) + dec) / pow(2, divider), 3)

    def __mass_density_measurement(self, data: list) -> dict:
        category = ["pm1.0", "pm2.5", "pm4.0", "pm10"]

        density = {"pm1.0": 0.0, "pm2.5": 0.0, "pm4.0": 0.0, "pm10": 0.0}

        for block, (pm) in enumerate(category):
            pm_data = []
            for i in range(0, SIZE_FLOAT, PACKET_SIZE):
                offset = (block * SIZE_FLOAT) + i
                if self.crc_calc(data[offset : offset + 2]) != data[offset + 2]:
                    logging.warning(
                        "'__mass_density_measurement' CRC mismatched!"
                        + f"  Data: {data[offset:offset+2]}"
                        + f"  Calculated CRC: {self.crc_calc(data[offset:offset+2])}"
                        + f"  Expected: {data[offset+2]}"
                    )
                    self.__valid["mass_density"] = False
                    return {}

                pm_data.extend(data[offset : offset + 2])

            density[pm] = self.__ieee754_number_conversion(
                pm_data[0] << 24 | pm_data[1] << 16 | pm_data[2] << 8 | pm_data[3]
            )

        self.__valid["mass_density"] = True

        return density

    def __particle_count_measurement(self, data: list) -> dict:
        category = ["pm0.5", "pm1.0", "pm2.5", "pm4.0", "pm10"]

        count = {"pm0.5": 0.0, "pm1.0": 0.0, "pm2.5": 0.0, "pm4.0": 0.0, "pm10": 0.0}

        for block, (pm) in enumerate(category):
            pm_data = []
            for i in range(0, SIZE_FLOAT, PACKET_SIZE):
                offset = (block * SIZE_FLOAT) + i
                if self.crc_calc(data[offset : offset + 2]) != data[offset + 2]:
                    logging.warning(
                        "'__particle_count_measurement' CRC mismatched!"
                        + f"  Data: {data[offset:offset+2]}"
                        + f"  Calculated CRC: {self.crc_calc(data[offset:offset+2])}"
                        + f"  Expected: {data[offset+2]}"
                    )

                    self.__valid["particle_count"] = False
                    return {}

                pm_data.extend(data[offset : offset + 2])

            count[pm] = self.__ieee754_number_conversion(
                pm_data[0] << 24 | pm_data[1] << 16 | pm_data[2] << 8 | pm_data[3]
            )

        self.__valid["particle_count"] = True

        return count

    def __particle_size_measurement(self, data: list) -> float:
        size = []
        for i in range(0, SIZE_FLOAT, PACKET_SIZE):
            if self.crc_calc(data[i : i + 2]) != data[i + 2]:
                logging.warning(
                    "'__particle_size_measurement' CRC mismatched!"
                    + f"  Data: {data[i:i+2]}"
                    + f"  Calculated CRC: {self.crc_calc(data[i:i+2])}"
                    + f"  Expected: {data[i+2]}"
                )

                self.__valid["particle_size"] = False
                return 0.0

            size.extend(data[i : i + 2])

        self.__valid["particle_size"] = True

        return self.__ieee754_number_conversion(
            size[0] << 24 | size[1] << 16 | size[2] << 8 | size[3]
        )

    async def __read_measured_value(self) -> None:
        while True:
            try:
                if not await self.read_data_ready_flag():
                    continue

                await self._write(CMD_READ_MEASURED_VALUES)
                data = await self._read(NBYTES_MEASURED_VALUES_FLOAT)

                if self.__data.full():
                    self.__data.get()

                result = {
                    "sensor_data": {
                        "mass_density": self.__mass_density_measurement(data[:24]),
                        "particle_count": self.__particle_count_measurement(
                            data[24:54]
                        ),
                        "particle_size": self.__particle_size_measurement(data[54:]),
                        "mass_density_unit": "ug/m3",
                        "particle_count_unit": "#/cm3",
                        "particle_size_unit": "um",
                    },
                    "timestamp": utc_timestamp(),
                }

                self.__data.put(result if all(self.__valid.values()) else {})

            except KeyboardInterrupt:
                logging.warning("Stopping measurement...")

                await self.stop_measurement()
                sys.exit()

            except Exception as e:
                logging.warning(f"{type(e).__name__}: {e}")

            finally:
                await asyncio.sleep(self.sampling_period)

    async def start_measurement(self) -> None:
        data_format = {"IEEE754_float": 0x03, "unsigned_16_bit_integer": 0x05}

        data = CMD_START_MEASUREMENT
        data.extend([data_format["IEEE754_float"], 0x00])
        data.append(self.crc_calc(data[2:4]))
        await self.i2c.write(data)
        await asyncio.sleep(0.05)
        self.__run()

    async def _read(self, nbytes: int) -> list:
        return await self.i2c.read(nbytes)

    async def _write(self, data: list) -> None:
        await self.i2c.write(data)

    async def get_measurement(self) -> dict:
        if not await self.read_data_ready_flag():
            return {}

        await self._write(CMD_READ_MEASURED_VALUES)
        data = await self._read(NBYTES_MEASURED_VALUES_FLOAT)

        result = {
            "sensor_data": {
                "mass_density": self.__mass_density_measurement(data[:24]),
                "particle_count": self.__particle_count_measurement(data[24:54]),
                "particle_size": self.__particle_size_measurement(data[54:]),
                "mass_density_unit": "ug/m3",
                "particle_count_unit": "#/cm3",
                "particle_size_unit": "um",
            },
            "timestamp": utc_timestamp(),
        }

        return result if all(self.__valid.values()) else {}

    async def stop_measurement(self) -> None:
        await self.i2c.write(CMD_STOP_MEASUREMENT)
        self.task.cancel()
        # self.i2c.close()

    def __run(self) -> None:
        self.task = asyncio.create_task(self.__read_measured_value())
