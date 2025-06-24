from typing import Optional, Sequence
from fastapi import APIRouter, Query
from sqlmodel import select
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


def _query_sensor_data(model_class, session, start_dt, end_dt, limit=1000):
    """Query sensor data from the database with evenly spaced sampling."""
    # First, create a base query with time filters
    base_query = select(model_class)
    if start_dt:
        base_query = base_query.where(model_class.timestamp >= start_dt)
    if end_dt:
        base_query = base_query.where(model_class.timestamp <= end_dt)

    # Get the total count to calculate sampling interval
    count_query = select(model_class.id)
    if base_query.whereclause is not None:
        count_query = count_query.where(base_query.whereclause)
    total_count = len(session.exec(count_query).all())

    if total_count <= limit:
        # If we have fewer rows than the limit, return all of them
        return session.exec(base_query).all()

    # Calculate the sampling interval
    interval = max(1, total_count // limit)

    # Use SQL window function to get evenly spaced rows
    # We need to use raw SQL for this specific operation
    where_clause = ""
    if base_query.whereclause is not None:
        where_clause = f"WHERE {base_query.whereclause.compile(compile_kwargs={'literal_binds': True})}"

    from sqlalchemy import text

    sql_query = text(
        f"""
    WITH numbered_rows AS (
        SELECT *, ROW_NUMBER() OVER (ORDER BY timestamp) as row_num
        FROM {model_class.__tablename__}
        {where_clause}
    )
    SELECT * FROM numbered_rows
    WHERE row_num % {interval} = 0
    ORDER BY timestamp
    LIMIT {limit}
    """
    )

    result = session.exec(sql_query)
    return result.all()


@router.get("/sensors", response_model=SensorData)
def get_sensor_data(
    start_date: Optional[str] = Query(
        None, description="Start date in ISO format (e.g., 2024-01-01T00:00:00Z)"
    ),
    end_date: Optional[str] = Query(
        None, description="End date in ISO format (e.g., 2024-01-01T23:59:59Z)"
    ),
    limit: int = Query(
        1000, description="Number of evenly spaced data points to return"
    ),
) -> SensorData:
    """Get evenly spaced data from all sensors with optional date filtering."""
    session = get_session()

    return SensorData(
        ltr390=_query_sensor_data(LTR390, session, start_date, end_date, limit),
        as7341=_query_sensor_data(AS7341, session, start_date, end_date, limit),
        bme688=_query_sensor_data(BME688, session, start_date, end_date, limit),
        ens160=_query_sensor_data(ENS160, session, start_date, end_date, limit),
        sps30=_query_sensor_data(SPS30, session, start_date, end_date, limit),
    )
