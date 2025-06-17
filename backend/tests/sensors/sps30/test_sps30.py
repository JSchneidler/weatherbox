def test_sps30_read():
    from weatherbox.sensors.sps30 import SPS30

    sps30 = SPS30()
    assert sps30.firmware_version() == "2.3"
    assert sps30.product_type() == "00080000"
    # assert sps30.serial_number() == "0000000000000000"
    assert sps30.read_status_register() == {
        "speed_status": "ok",
        "laser_status": "ok",
        "fan_status": "ok",
    }
    assert sps30.read_data_ready_flag() is False
    assert sps30.read_auto_cleaning_interval() == 604800


def test_sps30_read_measurement():
    from time import sleep
    from weatherbox.sensors.sps30 import SPS30

    sps30 = SPS30()
    sps30.start_measurement()

    while not sps30.read_data_ready_flag():
        sleep(0.1)

    data = sps30.get_measurement()
    assert data is not None
    assert isinstance(data["sensor_data"]["mass_density"]["pm1.0"], float)
    assert isinstance(data["sensor_data"]["mass_density"]["pm2.5"], float)
    assert isinstance(data["sensor_data"]["mass_density"]["pm4.0"], float)
    assert isinstance(data["sensor_data"]["mass_density"]["pm10"], float)
    assert isinstance(data["sensor_data"]["particle_count"]["pm0.5"], float)
    assert isinstance(data["sensor_data"]["particle_count"]["pm1.0"], float)
    assert isinstance(data["sensor_data"]["particle_count"]["pm2.5"], float)
    assert isinstance(data["sensor_data"]["particle_count"]["pm4.0"], float)
    assert isinstance(data["sensor_data"]["particle_count"]["pm10"], float)
    assert isinstance(data["sensor_data"]["particle_size"], float)
    assert data["sensor_data"]["mass_density_unit"] == "ug/m3"
    assert data["sensor_data"]["particle_count_unit"] == "#/cm3"

    sps30.stop_measurement()
