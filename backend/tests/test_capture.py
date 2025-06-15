import os

from sqlmodel import select
from weatherbox.db import get_session
from weatherbox.timelapse import capture
from weatherbox.models.TimelapseImage import TimelapseImage

IMAGE_DIR = "/home/jordan/code/weatherbox/images"


def test_capture():
    session = get_session()

    name = capture()

    images = session.exec(
        select(TimelapseImage).where(TimelapseImage.file_name == name)
    ).all()
    assert len(images) == 1

    os.remove(f"{IMAGE_DIR}/{name}")

    session.delete(images[0])
    session.commit()
