from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
import psutil
import uvicorn

from weatherbox.scheduler import initialize_and_start_scheduler, shutdown_scheduler
from weatherbox.sensor_manager import sensor_manager

from weatherbox.camera.stream import generate_frames
from weatherbox.routes import router as data_router


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
app.include_router(data_router, prefix="/data", tags=["sensor data"])


@app.get("/health")
def health_check():
    """
    Health check endpoint to verify that the service is running.
    """
    return {"status": "ok", "message": "WeatherBox service is running."}


@app.get("/sensors/status")
def get_sensor_status():
    """
    Get the status of all sensors including initialization state.
    """
    return {
        "initialization_complete": sensor_manager.is_initialization_complete(),
        "sensors": sensor_manager.get_sensor_status(),
    }


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


@app.get("/mjpeg")
async def mjpeg():
    return StreamingResponse(
        generate_frames(), media_type="multipart/x-mixed-replace; boundary=frame"
    )


def start_server():
    """Entry point for the poetry start command"""
    uvicorn.run("weatherbox.main:app", host="0.0.0.0", port=8000)


if __name__ == "__main__":
    start_server()
