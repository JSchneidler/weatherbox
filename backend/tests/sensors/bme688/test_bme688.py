def test_bme688_read():
    from weatherbox.sensors.bme688.bme688 import read

    data = read()
    assert data is not None
    assert isinstance(data.temperature, float)
    assert isinstance(data.pressure, float)
    assert isinstance(data.humidity, float)
    assert isinstance(data.gas, int)
