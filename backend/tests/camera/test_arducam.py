def test_arducam_capture_image():
    from weatherbox.camera.arducam import capture_image

    image = capture_image()
    assert image is not None
    assert image.shape == (480, 640, 4)

def test_arducam_capture_and_save_image():
    from weatherbox.camera.arducam import capture_and_save_image

    capture_and_save_image("test.jpg")
    assert True