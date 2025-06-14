from apscheduler.schedulers.asyncio import AsyncIOScheduler

# from weatherbox.sensors.as7341.as7341 import read_and_store as read_and_store_as7341
# from weatherbox.sensors.bme688.bme688 import read_and_store as read_and_store_bme688
# from weatherbox.sensors.ens160.ens160 import read_and_store as read_and_store_ens160
# from weatherbox.sensors.ltr390.ltr390 import read_and_store as read_and_store_ltr390
# from weatherbox.sensors.sps30.sps30 import read_and_store as read_and_store_sps30

from .timelapse import capture

scheduler = AsyncIOScheduler(job_defaults={"max_instances": 1})

# scheduler.add_job(capture, "interval", seconds=30)
# scheduler.add_job(read_and_store_as7341, "interval", seconds=30)
# scheduler.add_job(read_and_store_bme688, "interval", seconds=60)
# scheduler.add_job(read_and_store_ens160, "interval", seconds=60)
# scheduler.add_job(read_and_store_ltr390, "interval", seconds=30)
# scheduler.add_job(read_and_store_sps30, "interval", seconds=60)
