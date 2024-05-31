#!/bin/python3

import os
import glob
from time import sleep
 
import paho.mqtt.client as mqtt
import RPi.GPIO as GPIO
import spidev 
# MQTT setup

broker = "localhost"
port = 1883
topic = "humantiddi"

SPI_BUS = 0
SPI_DEVICE = 0
SPI_SENSOR_MAX_HZ = 100000
    
# Initalisiere Feuchtigkeitssensor
# (Check: https://sigmdel.ca/michel/ha/rpi/dnld/draft_spidev_doc.pdf)
spi = spidev.SpiDev()
spi.open(SPI_BUS, SPI_DEVICE)
spi.max_speed_hz = SPI_SENSOR_MAX_HZ

# RGB LED setup
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

redPin = 6
greenPin = 19
bluePin = 13
pumpResponse = 21

GPIO.setup(redPin,GPIO.OUT)
GPIO.setup(greenPin,GPIO.OUT)
GPIO.setup(bluePin,GPIO.OUT)
GPIO.setup(pumpResponse, GPIO.OUT)

def read_spi(channel):
    # Siehe https://tutorials-raspberrypi.com/measuring-soil-moisture-with-raspberry-pi/
    # Sensorspezifisches Bit-Gefrickel
    # siehe https://ww1.microchip.com/downloads/aemDocuments/documents/MSLD/ProductDocuments/DataSheets/MCP3004-MCP3008-Data-Sheet-DS20001295.pdf#G1.1036387
    value = spi.xfer2([1, (8+channel)<<4, 0])  
    data  = (value[1]&3 << 8) + value[2]

    # Data returning 1.7V == No Water

    return data

def on_publish(self, client, userdata, result, properties):
    print("data published")

def set_led_color(value):

    # Red for Dry
    if value < 50:
        GPIO.output(redPin, GPIO.LOW)
        GPIO.output(greenPin, GPIO.HIGH)
        GPIO.output(bluePin, GPIO.HIGH)

    # Yellow for low Water
    elif value < 100:
        GPIO.output(redPin, GPIO.LOW)
        GPIO.output(greenPin, GPIO.LOW)
        GPIO.output(bluePin, GPIO.HIGH)

    # Green for Good waterthreshhold
    elif value < 150:
        GPIO.output(redPin, GPIO.HIGH)
        GPIO.output(greenPin, GPIO.LOW)
        GPIO.output(bluePin, GPIO.HIGH)

    # Blue for Wet
    else:
        GPIO.output(redPin, GPIO.HIGH)
        GPIO.output(greenPin, GPIO.HIGH)
        GPIO.output(bluePin, GPIO.LOW)

client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
client.connect(broker, port)
client.on_publish = on_publish

while (True):
    moist = read_spi(1)
    set_led_color(moist)

    if moist <= 100:
        GPIO.output(pumpResponse, GPIO.HIGH)
    elif moist > 100:
        GPIO.output(pumpResponse, GPIO.LOW)

    client.publish(topic, moist)
    sleep(1)
    client.loop(1)

