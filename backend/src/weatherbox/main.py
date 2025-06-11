from contextlib import asynccontextmanager

from fastapi import FastAPI
import uvicorn

from weatherbox.sensors.as3935.as3935 import setup_trigger

from .scheduler import scheduler


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


def start_server():
    """Entry point for the poetry start command"""
    uvicorn.run("src.weatherbox.main:app", host="0.0.0.0", port=8000, reload=True)


if __name__ == "__main__":
    start_server()
