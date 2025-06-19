from apscheduler.schedulers.asyncio import AsyncIOScheduler
import logging

from weatherbox.sensors.as7341 import read_and_store as sample_as7341

# from weatherbox.sensors.as3935 import read_and_store as read_and_store_as3935
from weatherbox.sensors.bme688 import read_and_store as sample_bme688
from weatherbox.sensors.ens160 import read_and_store as sample_ens160
from weatherbox.sensors.ltr390 import read_and_store as sample_ltr390
from weatherbox.sensors.sps30 import read_and_store_with_instance as sample_sps30
from weatherbox.sensor_manager import sensor_manager

# from .timelapse import capture

scheduler = AsyncIOScheduler(
    job_defaults={
        "max_instances": 1,
        "coalesce": True,
        "misfire_grace_time": 15,  # 15 seconds grace time for misfired jobs
    }
)

logger = logging.getLogger(__name__)


async def initialize_and_start_scheduler():
    """
    Initialize all sensors and then start the scheduler with jobs.
    This ensures all sensors are ready before any sampling begins.
    """
    logger.info("Starting sensor initialization...")

    # Initialize all sensors
    success = await sensor_manager.initialize_all_sensors()

    if not success:
        logger.error("Sensor initialization failed. Some sensors may not be available.")
        # You might want to continue with partial initialization or exit
        # For now, we'll continue but log the issue

    # Start the scheduler
    scheduler.start()
    logger.info("Scheduler started")

    # Add jobs only after initialization
    await add_sensor_jobs()


async def add_sensor_jobs():
    """
    Add sensor sampling jobs to the scheduler.
    This is called after sensor initialization is complete.
    """
    logger.info("Adding sensor jobs to scheduler...")

    # Get sensor status to determine which sensors are available
    sensor_status = sensor_manager.get_sensor_status()

    # Add jobs for sensors that are ready
    if sensor_status["as7341"]["status"] == "ready":
        scheduler.add_job(sample_as7341, "interval", seconds=15)
        logger.info("Added AS7341 job (15s interval)")

    if sensor_status["bme688"]["status"] == "ready":
        scheduler.add_job(sample_bme688, "interval", seconds=15)
        logger.info("Added BME688 job (15s interval)")

    if sensor_status["ens160"]["status"] == "ready":
        scheduler.add_job(sample_ens160, "interval", seconds=15)
        logger.info("Added ENS160 job (15s interval)")

    if sensor_status["ltr390"]["status"] == "ready":
        scheduler.add_job(sample_ltr390, "interval", seconds=15)
        logger.info("Added LTR390 job (15s interval)")

    if sensor_status["sps30"]["status"] == "ready":
        # Get the SPS30 instance and create a wrapper function
        sps30_instance = sensor_manager.get_sps30_instance()
        if sps30_instance:

            async def sps30_wrapper():
                await sample_sps30(sps30_instance)

            scheduler.add_job(sps30_wrapper, "interval", seconds=5)
            logger.info("Added SPS30 job (5s interval)")
        else:
            logger.error("SPS30 instance not available despite status being ready")

    # TODO: Add AS3935 job when implemented
    # if sensor_status["as3935"]["status"] == "ready":
    #     scheduler.add_job(read_and_store_as3935, "interval", seconds=15)
    #     logger.info("Added AS3935 job (15s interval)")

    # TODO: Add timelapse job when implemented
    # scheduler.add_job(capture, "interval", seconds=30)

    logger.info("All sensor jobs added to scheduler")


async def shutdown_scheduler():
    """
    Shutdown the scheduler and sensors gracefully.
    """
    logger.info("Shutting down scheduler...")
    scheduler.shutdown()
    await sensor_manager.shutdown()
    logger.info("Scheduler and sensors shutdown complete")
