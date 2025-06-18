import pytest


@pytest.mark.asyncio
async def test_ltr390_read():
    from weatherbox.sensors.ltr390 import read

    data = await read()
    assert data is not None
    assert isinstance(data.light, int)
    assert isinstance(data.uvs, int)
