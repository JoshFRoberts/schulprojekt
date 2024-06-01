import RPi.GPIO as GPIO

from humidity_sender import MoistureSensor

def test_sensor_data(spi_bus=0, spi_device=0, max_speed_hz=100000, channel=2):
    sensor = MoistureSensor(spi_bus, spi_device, max_speed_hz)
    data = sensor.read(channel)
    if data < 1:
        print("Sensorfehler")
        return False
    return True