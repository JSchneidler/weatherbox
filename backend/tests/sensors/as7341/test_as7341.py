def test_as7341_read():
    from weatherbox.sensors.as7341.as7341 import read

    data = read()
    assert data is not None
    assert isinstance(data.violet, int)
    assert isinstance(data.indigo, int)
    assert isinstance(data.blue, int)
    assert isinstance(data.cyan, int)
    assert isinstance(data.green, int)
    assert isinstance(data.yellow, int)
    assert isinstance(data.orange, int)
    assert isinstance(data.red, int)
    assert isinstance(data.clear, int)
    assert isinstance(data.nir, int)
