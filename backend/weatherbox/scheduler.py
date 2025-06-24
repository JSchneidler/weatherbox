from apscheduler.schedulers.asyncio import AsyncIOScheduler
import logging
import os

from weatherbox.sensor_manager import sensor_manager
from weatherbox.timelapse import capture

INTERVALS = {
    "AS7341": 30,
    "BME688": 30,
    "ENS160": 30,
    "LTR390": 30,
    "SPS30": 30,
    "Timelapse": 60,
}

scheduler = AsyncIOScheduler(
    job_defaults={
        "max_instances": 1,
        "coalesce": True,
        "misfire_grace_time": 15,  # 15 seconds grace time for misfired jobs
    }
)


def get_interval(sensor_name: str) -> int:
    """
    Get the sampling interval for a given sensor.
    If the sensor is not found, return a default interval of 30 seconds.
    """
    return INTERVALS.get(sensor_name, 30)


async def initialize_and_start_scheduler():
    """
    Initialize all sensors and then start the scheduler with jobs.
    This ensures all sensors are ready before any sampling begins.
    """
    await sensor_manager.initialize_all_sensors()

    scheduler.start()

    for sensor in sensor_manager.sensors:
        if not sensor.is_ready():
            continue

        interval = get_interval(sensor.name)

        scheduler.add_job(
            sensor.read_and_store,
            "interval",
            seconds=interval,
            id=sensor.name,
            name=sensor.name,
        )
        logging.info(f"{sensor.name} scheduled with interval {interval} seconds.")

    if not os.getenv("TIMELAPSE_DISABLED", "false").lower() == "true":
        interval = get_interval("Timelapse")
        scheduler.add_job(
            capture,
            "interval",
            seconds=interval,
            id="Timelapse",
            name="Timelapse Capture",
        )
        logging.info(f"Timelapse capture scheduled with interval {interval} seconds.")


async def shutdown_scheduler():
    """
    Shutdown the scheduler and sensors gracefully.
    """
    logging.info("Shutting down scheduler...")
    scheduler.shutdown()
    await sensor_manager.shutdown()
    logging.info("Scheduler and sensors shutdown complete")
