from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
import psutil
import uvicorn

from weatherbox.sensors.Sensor import Sensor
from weatherbox.sensor_manager import sensor_manager
from weatherbox.scheduler import (
    initialize_and_start_scheduler,
    shutdown_scheduler,
    get_interval,
)
from weatherbox.timelapse import TIMELAPSE_DISABLED

# from weatherbox.camera.stream import generate_frames
from weatherbox.routes.sensors import router as sensors
from weatherbox.routes.images import router as images


@asynccontextmanager
async def lifespan(_: FastAPI):
    # Initialize sensors and start scheduler
    await initialize_and_start_scheduler()
    yield
    # Shutdown scheduler and sensors
    await shutdown_scheduler()


app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include the data routes
app.include_router(sensors, prefix="/sensors", tags=["sensor data"])
app.include_router(images, prefix="/images", tags=["image data"])


@app.get("/health")
def health_check():
    """
    Health check endpoint to verify that the service is running.
    """
    return {"status": "ok", "message": "WeatherBox service is running."}


# @app.get("/mjpeg")
# async def mjpeg():
#     return StreamingResponse(
#         generate_frames(), media_type="multipart/x-mixed-replace; boundary=frame"
#     )


@app.get("/system/stats")
def get_system_stats():
    """
    Get the system stats.
    """
    return {
        "cpu_usage": psutil.cpu_percent(),
        "memory_usage": psutil.virtual_memory().percent,
        "disk_usage": psutil.disk_usage("/").percent,
        "uptime": psutil.boot_time(),
        "fan_rpm": psutil.sensors_fans()["pwmfan"][0][1],
        "cpu_temperature": psutil.sensors_temperatures()["cpu_thermal"][0][1],
    }


@app.get("/settings")
def get_sensor_settings():
    """
    Get the current settings for all sensors.
    """

    settings = {
        sensor.name: getSensorSettings(sensor) for sensor in sensor_manager.sensors
    }

    settings["timelapse"] = {
        "enabled": not TIMELAPSE_DISABLED,
        "interval": get_interval("timelapse"),
    }

    return settings


def getSensorSettings(sensor: Sensor):
    return {
        **sensor.get_settings(),
        "sample_interval": get_interval(sensor.name),
    }


def start_server():
    """Entry point for the poetry start command"""
    uvicorn.run("weatherbox.main:app", host="0.0.0.0", port=8000)


if __name__ == "__main__":
    start_server()
