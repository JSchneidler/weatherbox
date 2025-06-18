from datetime import datetime

from .camera.arducam import capture_and_save_image
from .db import get_session, db_now
from weatherbox.models import TimelapseImage

IMAGE_DIR = "/home/jordan/code/weatherbox/images"


def capture() -> str:
    session = get_session()
    now = db_now()
    name = f"{now}.jpg"
    capture_and_save_image(f"{IMAGE_DIR}/{name}")
    image = TimelapseImage(timestamp=now, file_name=name)
    session.add(image)
    session.commit()

    return name
