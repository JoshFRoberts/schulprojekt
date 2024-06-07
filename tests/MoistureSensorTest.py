import RPi.GPIO as GPIO
from os import path as os_path 
from sys import path as sys_path
sys_path.append(os_path.abspath(os_path.join(os_path.dirname(__file__), '..')))

from humidity_sender import MoistureSensor

def test_sensor_data(spi_bus=None, spi_device=None, channel=None, max_speed_hz=100000):
    spi_bus = spi_bus if spi_bus is not None else 0
    spi_device = spi_device if spi_device is not None else 0
    channel = channel if channel is not None else 2

    sensor = MoistureSensor(spi_bus, spi_device, max_speed_hz)
    data = sensor.read(channel)
    if data < 1:
        return False
    return True
