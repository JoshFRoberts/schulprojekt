#!/bin/python3

import os
import glob
from time import sleep

## Requirements V
# pip3 install paho-mqtt spidev RPi-gpio
import paho.mqtt.client as mqtt
import RPi.GPIO as GPIO
import spidev

class MoistureSensor:
    def __init__(self, spi_bus=0, spi_device=0, max_speed_hz=100000):
        self.spi = spidev.SpiDev()
        self.spi.open(spi_bus, spi_device)
        self.spi.max_speed_hz = max_speed_hz

    def read(self, channel):
        value = self.spi.xfer2([1, (8 + channel) << 4, 0])
        data = ((value[1] & 3) << 8) + value[2]
        return data

class RGBLed:
    def __init__(self, red_pin=6, green_pin=19, blue_pin=13):
        self.red_pin = red_pin
        self.green_pin = green_pin
        self.blue_pin = blue_pin

        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)

        GPIO.setup(self.red_pin, GPIO.OUT)
        GPIO.setup(self.green_pin, GPIO.OUT)
        GPIO.setup(self.blue_pin, GPIO.OUT)

    def set_color(self, value):
        if value < 50:
            self._set_pins(GPIO.LOW, GPIO.HIGH, GPIO.HIGH)
        elif value < 100:
            self._set_pins(GPIO.LOW, GPIO.LOW, GPIO.HIGH)
        elif value < 150:
            self._set_pins(GPIO.HIGH, GPIO.LOW, GPIO.HIGH)
        else:
            self._set_pins(GPIO.HIGH, GPIO.HIGH, GPIO.LOW)

    def _set_pins(self, red, green, blue):
        GPIO.output(self.red_pin, red)
        GPIO.output(self.green_pin, green)
        GPIO.output(self.blue_pin, blue)

class PumpController:
    def __init__(self, pump_pin=21, return_signal_pin=20):
        self.pump_pin = pump_pin
        self.return_signal_pin = return_signal_pin
        GPIO.setup(self.pump_pin, GPIO.OUT)
        GPIO.setup(self.return_signal_pin, GPIO.IN, GPIO.PUD_DOWN)

    def control(self, moist_value):
        if moist_value <= 100:
            GPIO.output(self.pump_pin, GPIO.HIGH)
        else:
            GPIO.output(self.pump_pin, GPIO.LOW)

class MQTTClient:
    def __init__(self, broker="localhost", port=1883, topic="humantiddi"):
        self.client = mqtt.Client()
        self.broker = broker
        self.port = port
        self.topic = topic

        self.client.on_publish = self.on_publish
        self.client.connect(self.broker, self.port)

    def on_publish(self, client, userdata, result):
        print("data published")

    def publish(self, message):
        self.client.publish(self.topic, message)
        self.client.loop(1)

class MoistureMonitoringSystem:
    def __init__(self):
        self.sensor = MoistureSensor()
        self.led = RGBLed()
        self.pump = PumpController()
        self.mqtt_client = MQTTClient()

    def run(self, channel=2):
        while True:
            moisture_level = self.sensor.read(channel)
            self.led.set_color(moisture_level)
            self.pump.control(moisture_level)
            self.mqtt_client.publish(moisture_level)
            sleep(1)

if __name__ == "__main__":
    system = MoistureMonitoringSystem()
    system.run()