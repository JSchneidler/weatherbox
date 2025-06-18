import pytest


@pytest.mark.asyncio
async def test_bme688_read():
    from weatherbox.sensors.bme688 import read

    data = await read()
    assert data is not None
    assert isinstance(data.temperature, float)
    assert isinstance(data.pressure, float)
    assert isinstance(data.humidity, float)
    assert isinstance(data.gas, int)
    assert isinstance(data.altitude, float)
