from apscheduler.schedulers.asyncio import AsyncIOScheduler

from weatherbox.sensors.as7341 import read as sample_as7341

# from weatherbox.sensors.as3935 import read_and_store as read_and_store_as3935
from weatherbox.sensors.bme688 import read as sample_bme688
from weatherbox.sensors.ens160 import read as sample_ens160
from weatherbox.sensors.ltr390 import read as sample_ltr390
from weatherbox.sensors.sps30 import read as sample_sps30

# from .timelapse import capture

scheduler = AsyncIOScheduler(job_defaults={"max_instances": 1})


def pr(readFn):
    async def wrapper():
        data = await readFn()
        print(data)

    return wrapper


# TODO: Set intervals based on environment variables
# scheduler.add_job(capture, "interval", seconds=30)
scheduler.add_job(pr(sample_as7341), "interval", seconds=5)
scheduler.add_job(pr(sample_bme688), "interval", seconds=5)
scheduler.add_job(pr(sample_ens160), "interval", seconds=5)
scheduler.add_job(pr(sample_ltr390), "interval", seconds=5)
scheduler.add_job(pr(sample_sps30), "interval", seconds=60)
