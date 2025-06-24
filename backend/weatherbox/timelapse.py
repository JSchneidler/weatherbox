import logging

from weatherbox.camera.arducam import capture_and_save_image
from weatherbox.db import get_session, utc_timestamp
from weatherbox.models import TimelapseImage

IMAGE_DIR = "/home/jordan/code/weatherbox/backend/images"


def capture() -> str:
    session = get_session()
    now = utc_timestamp()
    name = f"{now}.jpg"
    capture_and_save_image(f"{IMAGE_DIR}/{name}")
    image = TimelapseImage(timestamp=now, file_name=name)
    session.add(image)
    session.commit()

    logging.info("Captured timelapse image")

    return name
