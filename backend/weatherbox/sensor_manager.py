import asyncio
import logging
from typing import Dict, List, Optional
from dataclasses import dataclass
from enum import Enum

from weatherbox.sensors.as7341 import as7341
from weatherbox.sensors.bme688 import bme680
from weatherbox.sensors.ens160 import ens160
from weatherbox.sensors.ltr390 import ltr390
from weatherbox.sensors.sps30 import SPS30
from weatherbox.sensors.as3935 import setup_trigger


class SensorStatus(Enum):
    PENDING = "pending"
    INITIALIZING = "initializing"
    WARMING_UP = "warming_up"
    READY = "ready"
    ERROR = "error"


@dataclass
class SensorInfo:
    name: str
    status: SensorStatus
    warm_up_time: float = 0.0
    error_message: Optional[str] = None


class SensorManager:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.sensors: Dict[str, SensorInfo] = {
            "as7341": SensorInfo("AS7341", SensorStatus.PENDING, warm_up_time=0.0),
            "bme688": SensorInfo("BME688", SensorStatus.PENDING, warm_up_time=0.0),
            "ens160": SensorInfo(
                "ENS160", SensorStatus.PENDING, warm_up_time=2.0
            ),  # 2s warm-up
            "ltr390": SensorInfo("LTR390", SensorStatus.PENDING, warm_up_time=0.0),
            "sps30": SensorInfo(
                "SPS30", SensorStatus.PENDING, warm_up_time=30.0
            ),  # 30s warm-up
            "as3935": SensorInfo("AS3935", SensorStatus.PENDING, warm_up_time=0.0),
        }
        self.sps30_instance: Optional[SPS30] = None
        self._initialization_complete = False

    async def initialize_all_sensors(self) -> bool:
        """
        Initialize all sensors with proper warm-up and configuration.
        Returns True if all sensors are ready, False otherwise.
        """
        self.logger.info("Starting sensor initialization...")

        # Initialize sensors that don't require warm-up first
        await self._initialize_simple_sensors()

        # Initialize sensors that require warm-up
        await self._initialize_complex_sensors()

        # Check final status
        all_ready = all(
            sensor.status == SensorStatus.READY for sensor in self.sensors.values()
        )
        self._initialization_complete = all_ready

        if all_ready:
            self.logger.info("All sensors initialized successfully!")
        else:
            failed_sensors = [
                name
                for name, sensor in self.sensors.items()
                if sensor.status == SensorStatus.ERROR
            ]
            self.logger.error(f"Sensor initialization failed for: {failed_sensors}")

        return all_ready

    async def _initialize_simple_sensors(self):
        """Initialize sensors that don't require warm-up."""
        simple_sensors = ["as7341", "bme688", "ltr390", "as3935"]

        for sensor_name in simple_sensors:
            await self._initialize_sensor(sensor_name)

    async def _initialize_complex_sensors(self):
        """Initialize sensors that require warm-up."""
        complex_sensors = ["ens160", "sps30"]

        for sensor_name in complex_sensors:
            await self._initialize_sensor(sensor_name)

    async def _initialize_sensor(self, sensor_name: str):
        """Initialize a single sensor with proper error handling."""
        sensor_info = self.sensors[sensor_name]
        sensor_info.status = SensorStatus.INITIALIZING

        try:
            self.logger.info(f"Initializing {sensor_info.name}...")

            if sensor_name == "sps30":
                await self._initialize_sps30()
            elif sensor_name == "ens160":
                await self._initialize_ens160()
            elif sensor_name == "as3935":
                await self._initialize_as3935()
            else:
                # Simple sensors just need to verify they're accessible
                await self._verify_sensor_access(sensor_name)

            # Apply warm-up time if needed
            if sensor_info.warm_up_time > 0:
                sensor_info.status = SensorStatus.WARMING_UP
                self.logger.info(
                    f"Warming up {sensor_info.name} for {sensor_info.warm_up_time}s..."
                )
                await asyncio.sleep(sensor_info.warm_up_time)

            sensor_info.status = SensorStatus.READY
            self.logger.info(f"{sensor_info.name} initialized successfully")

        except Exception as e:
            sensor_info.status = SensorStatus.ERROR
            sensor_info.error_message = str(e)
            self.logger.error(f"Failed to initialize {sensor_info.name}: {e}")

    async def _initialize_sps30(self):
        """Initialize SPS30 sensor with proper startup sequence."""
        try:
            self.sps30_instance = SPS30()

            # Verify sensor is accessible
            firmware_version = await self.sps30_instance.firmware_version()
            product_type = await self.sps30_instance.product_type()
            status = await self.sps30_instance.read_status_register()

            self.logger.info(
                f"SPS30 firmware: {firmware_version}, product: {product_type}"
            )
            self.logger.info(f"SPS30 status: {status}")

            # Start measurement mode
            await self.sps30_instance.start_measurement()

            # Wait for first data to be ready
            max_wait_time = 60  # 60 seconds max wait
            wait_time = 0
            while not await self.sps30_instance.read_data_ready_flag():
                await asyncio.sleep(1)
                wait_time += 1
                if wait_time >= max_wait_time:
                    raise TimeoutError("SPS30 data not ready within timeout period")

            self.logger.info("SPS30 measurement started successfully")

        except Exception as e:
            self.logger.error(f"SPS30 initialization failed: {e}")
            raise

    async def _initialize_ens160(self):
        """Initialize ENS160 sensor."""
        try:
            # Verify sensor is accessible by reading basic properties
            # The ENS160 library doesn't expose many initialization methods,
            # so we'll just verify it's responding
            aqi = ens160.AQI
            tvoc = ens160.TVOC
            eco2 = ens160.eCO2

            self.logger.info(
                f"ENS160 initial values - AQI: {aqi}, TVOC: {tvoc}, eCO2: {eco2}"
            )

        except Exception as e:
            self.logger.error(f"ENS160 initialization failed: {e}")
            raise

    async def _initialize_as3935(self):
        """Initialize AS3935 lightning sensor."""
        try:
            # Call the setup_trigger function
            setup_trigger()
            self.logger.info("AS3935 trigger setup completed")

        except Exception as e:
            self.logger.error(f"AS3935 initialization failed: {e}")
            raise

    async def _verify_sensor_access(self, sensor_name: str):
        """Verify that a simple sensor is accessible."""
        try:
            if sensor_name == "as7341":
                # Try to read a channel to verify sensor is working
                _ = as7341.channel_clear
            elif sensor_name == "bme688":
                # Try to read temperature to verify sensor is working
                _ = bme680.temperature
            elif sensor_name == "ltr390":
                # Try to read light to verify sensor is working
                _ = ltr390.light

            self.logger.info(f"{sensor_name} sensor verified as accessible")

        except Exception as e:
            self.logger.error(f"{sensor_name} sensor verification failed: {e}")
            raise

    def get_sensor_status(self) -> Dict[str, dict]:
        """Get the status of all sensors."""
        return {
            name: {
                "name": sensor.name,
                "status": sensor.status.value,
                "warm_up_time": sensor.warm_up_time,
                "error_message": sensor.error_message,
            }
            for name, sensor in self.sensors.items()
        }

    def is_initialization_complete(self) -> bool:
        """Check if all sensors have been initialized successfully."""
        return self._initialization_complete

    def get_sps30_instance(self) -> Optional[SPS30]:
        """Get the SPS30 instance if available."""
        return self.sps30_instance

    async def shutdown(self):
        """Shutdown all sensors gracefully."""
        self.logger.info("Shutting down sensors...")

        if self.sps30_instance:
            try:
                await self.sps30_instance.stop_measurement()
                self.logger.info("SPS30 measurement stopped")
            except Exception as e:
                self.logger.error(f"Error stopping SPS30: {e}")


# Global sensor manager instance
sensor_manager = SensorManager()
