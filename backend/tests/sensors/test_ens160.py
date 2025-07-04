import pytest


@pytest.mark.asyncio
async def test_ens160_read():
    from weatherbox.sensors.ens160 import read

    data = await read()
    assert data is not None
    assert isinstance(data.aqi, int)
    assert isinstance(data.tvoc, int)
    assert isinstance(data.eco2, int)
