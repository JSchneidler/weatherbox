def test_ltr390_read():
    from weatherbox.sensors.ltr390.ltr390 import read

    data = read()
    assert data is not None
    assert isinstance(data.light, int)
    assert isinstance(data.uvs, int)
