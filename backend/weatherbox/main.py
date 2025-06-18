from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import select
from fastapi.responses import StreamingResponse
import uvicorn

from weatherbox.scheduler import scheduler
from weatherbox.sensors.as3935 import setup_trigger

from weatherbox.camera.stream import generate_frames
from weatherbox.db import get_session

from weatherbox.models import AS7341, BME688, ENS160, LTR390, SPS30


@asynccontextmanager
async def lifespan(_: FastAPI):
    # scheduler.start()
    setup_trigger()
    yield
    # scheduler.shutdown()


app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)


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


@app.get("/data")
def get_data():
    session = get_session()
    data = {
        "ltr390": session.exec(select(LTR390).limit(1000)).all(),
        "as7341": session.exec(select(AS7341).limit(1000)).all(),
        "bme688": session.exec(select(BME688).limit(1000)).all(),
        "ens160": session.exec(select(ENS160).limit(1000)).all(),
        "sps30": session.exec(select(SPS30).limit(1000)).all(),
    }
    return data


def start_server():
    """Entry point for the poetry start command"""
    uvicorn.run("weatherbox.main:app", host="0.0.0.0", port=8000)


if __name__ == "__main__":
    start_server()
