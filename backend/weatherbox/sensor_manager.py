import logging
import os
from typing import Dict, List

from weatherbox.sensors.Sensor import Sensor, SensorStatus

from weatherbox.sensors import AS7341, BME688, ENS160, LTR390, SPS30

I2C_BUS_0 = 0
I2C_BUS_1 = 1


class SensorManager:
    def __init__(self):
        self.sensors: List[Sensor] = [
            AS7341(I2C_BUS_0),
            BME688(I2C_BUS_1),
            ENS160(I2C_BUS_1),
            LTR390(I2C_BUS_0),
            SPS30(I2C_BUS_1),
        ]

    async def initialize_all_sensors(self):
        """
        Initialize all sensors with proper warm-up and configuration.
        Returns True if all sensors are ready, False otherwise.
        """
        for sensor in self.sensors:
            if os.getenv(f"{sensor.name.upper()}_DISABLED", "false").lower() == "true":
                sensor.status = SensorStatus.DISABLED
                logging.info(f"{sensor.name} is disabled, skipping.")
                continue

            try:
                await sensor.initialize()
            except Exception as e:
                logging.error(f"Failed to initialize {sensor.name}: {e}")
                sensor.status = SensorStatus.ERROR
                sensor.error = str(e)
                continue

    def get_sensor_status(self) -> Dict[str, str]:
        """Get the status of all sensors."""
        return {
            sensor.name: (
                str(sensor.error)
                if sensor.status == SensorStatus.ERROR
                else sensor.status.value
            )
            for sensor in self.sensors
        }

    def is_initialization_complete(self) -> bool:
        """Check if all sensors have been initialized successfully."""
        return not any(
            sensor.status == SensorStatus.INITIALIZING
            or sensor.status == SensorStatus.WARMING_UP
            for sensor in self.sensors
        )

    async def shutdown(self):
        """Shutdown all sensors gracefully."""
        logging.info("Shutting down sensors...")

        for sensor in self.sensors:
            await sensor.deinitialize()


# Global sensor manager instance
sensor_manager = SensorManager()
