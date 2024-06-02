#!/bin/python3

import os
import glob
from time import sleep

import paho.mqtt.client as mqtt
import RPi.GPIO as GPIO
import spidev

from config import * 

class MoistureSensor:
    def __init__(self, spi_bus=None, spi_device=None, max_speed_hz=None):
        spi_bus = spi_bus if not spi_bus is None else DEFAULT_SPI_BUS
        spi_device = spi_device if not spi_device is None else DEFAULT_SPI_DEVICE
        max_speed_hz = max_speed_hz if not max_speed_hz is None else DEFAULT_SPI_FREQ
        self.spi = spidev.SpiDev()
        self.spi.open(spi_bus, spi_device)
        self.spi.max_speed_hz = max_speed_hz

    def read(self, channel):
        value = self.spi.xfer2([1, (8 + channel) << 4, 0])
        data = ((value[1] & 3) << 8) + value[2]
        return data

class RGBLed:
    def __init__(self, red_pin=None, green_pin=None, blue_pin=None):
        self.red_pin = red_pin if not red_pin is None else DEFAULT_PIN_RED
        self.green_pin = green_pin if not green_pin is None else DEFAULT_PIN_GREEN
        self.blue_pin = blue_pin if not blue_pin is None else DEFAULT_PIN_BLUE

        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)

        GPIO.setup(self.red_pin, GPIO.OUT)
        GPIO.setup(self.green_pin, GPIO.OUT)
        GPIO.setup(self.blue_pin, GPIO.OUT)

    def set_color(self, value):
        if value < THRESHOLD_RED:
            self._set_pins(GPIO.LOW, GPIO.HIGH, GPIO.HIGH)
        elif value < THRESHOLD_YELLOW:
            self._set_pins(GPIO.LOW, GPIO.LOW, GPIO.HIGH)
        elif value < THRESHOLD_GREEN:
            self._set_pins(GPIO.HIGH, GPIO.LOW, GPIO.HIGH)
        else:
            self._set_pins(GPIO.HIGH, GPIO.HIGH, GPIO.LOW)

    def _set_pins(self, red, green, blue):
        GPIO.output(self.red_pin, red)
        GPIO.output(self.green_pin, green)
        GPIO.output(self.blue_pin, blue)

class PumpController:
    def __init__(self, pump_pin=None, return_signal_pin=None):
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        pump_pin = pump_pin if not pump_pin is None else DEFAULT_PIN_PUMP
        return_signal_pin = return_signal_pin if not return_signal_pin is None else DEFAULT_PIN_PUMP_OBSERVE
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
    def __init__(self, broker=None, port=None, topic=None):
        broker = broker if not broker is None else DEFAULT_BROKER
        port = port if not port is None else DEFAULT_PORT
        topic = topic if not topic is None else DEFAULT_TOPIC
        self.client = mqtt.Client()
        self.broker = broker
        self.port = port
        self.topic = topic

        self.client.on_publish = self.on_publish
        self.client.connect(self.broker, self.port)

    def on_publish(self, client, userdata, msg_count):
        if DEBUG_PRINT: print(f"Data published from humidity sensor: {userdata}")
        if userdata is None: 
            print(f"{FMT_RED}FEHLER{FMT_NONE}: Leere MQTT-Nachricht für Feuchtigkeitssensor")

    def publish(self, message):
        self.client.publish(self.topic, message)
        self.client.loop(1)

class MoistureMonitoringSystem:
    def __init__(
            self, 
            has_led = None,
            mqtt_host = None, 
            mqtt_port = None, 
            mqtt_topic = None, 
            spi_bus = None, 
            spi_device = None, 
            spi_max_hz = None, 
            pump_pin = None, 
            pump_observe_pin = None
        ):
        GPIO.setwarnings(False)
        self.has_led = has_led if not has_led is None else False 
        self.sensor = MoistureSensor(spi_bus, spi_device, spi_max_hz)
        if has_led:
            self.led = RGBLed()
        self.pump = PumpController(pump_pin, pump_observe_pin)
        self.mqtt_client = MQTTClient(mqtt_host, mqtt_port, mqtt_topic)

    def run(self, channel=None):
        channel = channel if not channel is None else 2 
        while True:
            moisture_level = self.sensor.read(channel)
            if self.has_led:
                self.led.set_color(moisture_level)
            self.pump.control(moisture_level)
            self.mqtt_client.publish(moisture_level)
            sleep(1)

if __name__ == "__main__":
    system = MoistureMonitoringSystem()
    system.run()
