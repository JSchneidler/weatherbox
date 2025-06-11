import time

from picamera2 import Picamera2

def capture_image():
    camera = Picamera2()
    camera.start()
    image = camera.capture_array()
    camera.stop()

    return image

def capture_and_save_image(path: str):
    camera = Picamera2()
    # camera.start_and_capture_file(path)

    config = camera.create_still_configuration()
    camera.start()
    time.sleep(1)
    camera.autofocus_cycle()
    camera.switch_mode_and_capture_file(config, path)

    camera.stop()