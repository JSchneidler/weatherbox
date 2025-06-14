import io
import logging
from threading import Condition

from picamera2 import Picamera2
from picamera2.encoders import MJPEGEncoder, Quality
from picamera2.outputs import FileOutput


def generate_frames():
    while True:
        try:
            frame = output.read()
            if frame is not None:
                yield (
                    b"--frame\r\n" b"Content-Type: image/jpeg\r\n\r\n" + frame + b"\r\n"
                )
        except Exception as e:
            logging.error(f"Error in generate_frames: {str(e)}")
            break

    print("done")


class StreamingOutput(io.BufferedIOBase):
    def __init__(self):
        self.frame = None
        self.condition = Condition()

    def write(self, buf):
        with self.condition:
            self.frame = buf
            self.condition.notify_all()

    def read(self):
        with self.condition:
            self.condition.wait()
            return self.frame


picam2 = Picamera2(camera_num=1)
video_config = picam2.create_video_configuration(main={"size": (1920, 1080)})
picam2.configure(video_config)
output = StreamingOutput()
picam2.start_recording(MJPEGEncoder(), FileOutput(output), Quality.VERY_HIGH)


def stop():
    print("Stopping recording")
    picam2.stop_recording()
    picam2.close()


class StreamManager:
    def __init__(self):
        self.camera = Picamera2(camera_num=1)
        self.video_config = self.camera.create_video_configuration(
            main={"size": (1920, 1080)}
        )
        self.camera.configure(self.video_config)
        self.output = StreamingOutput()
        self.camera.start_recording(
            MJPEGEncoder(), FileOutput(self.output), Quality.VERY_HIGH
        )

    def stop(self):
        self.camera.stop()
        self.camera.close()

    def get_frame(self):
        return self.output.read()
