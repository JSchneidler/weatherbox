from datetime import datetime
from typing import Optional, Sequence, Type
from fastapi import APIRouter, Query
from sqlmodel import select, col, text
from sqlalchemy import func
from pydantic import BaseModel

from weatherbox.db import get_session
from weatherbox.models import AS7341, BME688, ENS160, LTR390, SPS30

router = APIRouter()


class SensorData(BaseModel):
    """Response model containing data from all sensors."""

    ltr390: Sequence[LTR390]
    as7341: Sequence[AS7341]
    bme688: Sequence[BME688]
    ens160: Sequence[ENS160]
    sps30: Sequence[SPS30]


def _parse_date(date_str: Optional[str]) -> Optional[datetime]:
    """Parse date string to datetime object."""
    if not date_str:
        return None
    try:
        return datetime.fromisoformat(date_str.replace("Z", "+00:00"))
    except ValueError:
        return None


def _query_sensor_data(model_class, session, start_dt, end_dt):
    """Query sensor data from the database."""
    query = select(model_class)
    if start_dt:
        query = query.where(model_class.timestamp >= start_dt)
    if end_dt:
        query = query.where(model_class.timestamp <= end_dt)

    query = query.order_by(model_class.timestamp.desc())
    query = query.limit(1000)

    return session.exec(query).all()


@router.get("/sensors", response_model=SensorData)
def get_sensor_data(
    start_date: Optional[str] = Query(
        None, description="Start date in ISO format (e.g., 2024-01-01T00:00:00)"
    ),
    end_date: Optional[str] = Query(
        None, description="End date in ISO format (e.g., 2024-01-01T23:59:59)"
    ),
    limit: int = Query(
        1000, description="Number of evenly spaced data points to return"
    ),
) -> SensorData:
    """Get evenly spaced data from all sensors with optional date filtering."""
    session = get_session()

    start_dt = _parse_date(start_date)
    end_dt = _parse_date(end_date)

    return SensorData(
        ltr390=_query_sensor_data(LTR390, session, start_dt, end_dt),
        as7341=_query_sensor_data(AS7341, session, start_dt, end_dt),
        bme688=_query_sensor_data(BME688, session, start_dt, end_dt),
        ens160=_query_sensor_data(ENS160, session, start_dt, end_dt),
        sps30=_query_sensor_data(SPS30, session, start_dt, end_dt),
    )
