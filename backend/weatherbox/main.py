from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.responses import StreamingResponse
import uvicorn

from weatherbox.scheduler import scheduler
from weatherbox.sensors.as3935.as3935 import setup_trigger
from weatherbox.stream import generate_frames


@asynccontextmanager
async def lifespan(_: FastAPI):
    scheduler.start()
    setup_trigger()
    yield
    scheduler.shutdown()


app = FastAPI(lifespan=lifespan)


@app.get("/health")
def health_check():
    """
    Health check endpoint to verify that the service is running.
    """
    return {"status": "ok", "message": "WeatherBox service is running."}


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
