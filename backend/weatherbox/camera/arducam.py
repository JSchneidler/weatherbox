import logging

from picamera2 import Picamera2


CAMERA_NUM = 0


def capture_image():
    """
    Capture an image and return the array.
    Uses preview configuration for faster capture.
    """
    camera = None
    try:
        camera = Picamera2(camera_num=CAMERA_NUM)
        preview_config = camera.create_preview_configuration()
        camera.configure(preview_config)
        camera.start()
        return camera.capture_array()
    finally:
        if camera:
            camera.stop()
            camera.close()


def capture_and_save_image(path: str):
    """
    Capture and save an image using Picamera2.
    Uses still configuration for best quality.
    """
    camera = None
    try:
        camera = Picamera2(camera_num=CAMERA_NUM)
        still_config = camera.create_still_configuration()
        camera.configure(still_config)
        camera.start()
        camera.capture_file(path)
    except Exception as e:
        logging.error(f"Failed to capture image: {e}")
        raise
    finally:
        if camera:
            camera.stop()
            camera.close()
