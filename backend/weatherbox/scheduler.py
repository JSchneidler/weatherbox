from apscheduler.schedulers.asyncio import AsyncIOScheduler
import logging
import os

from weatherbox.sensor_manager import sensor_manager
from weatherbox.timelapse import capture

INTERVALS = {
    "AS7341": 30,  # AS7341 sampling interval in seconds
    "BME688": 30,  # BME688 sampling interval in seconds
    "ENS160": 30,  # ENS160 sampling interval in seconds
    "LTR390": 30,  # LTR390 sampling interval in seconds
    "SPS30": 30,  # SPS30 sampling interval in seconds
    "Timelapse": 60,  # Timelapse capture interval in seconds
}

scheduler = AsyncIOScheduler(
    job_defaults={
        "max_instances": 1,
        "coalesce": True,
        "misfire_grace_time": 15,  # 15 seconds grace time for misfired jobs
    }
)


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

        scheduler.add_job(
            sensor.read_and_store,
            "interval",
            seconds=INTERVALS.get(sensor.name, 30),
            id=sensor.name,
            name=sensor.name,
        )
        logging.info(
            f"{sensor.name} scheduled with interval {INTERVALS[sensor.name]} seconds."
        )

    if not os.getenv("TIMELAPSE_DISABLED", "false").lower() == "true":
        scheduler.add_job(
            capture,
            "interval",
            seconds=INTERVALS["Timelapse"],
            id="Timelapse",
            name="Timelapse Capture",
        )
        logging.info(
            f"Timelapse capture scheduled with interval {INTERVALS['Timelapse']} seconds."
        )


async def shutdown_scheduler():
    """
    Shutdown the scheduler and sensors gracefully.
    """
    logging.info("Shutting down scheduler...")
    scheduler.shutdown()
    await sensor_manager.shutdown()
    logging.info("Scheduler and sensors shutdown complete")
