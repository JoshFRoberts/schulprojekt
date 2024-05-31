#!/bin/python3

import os
import glob
import paho.mqtt.client as mqtt

topic = "humantiddi"
broker = "localhost"
port = 1883

def on_message(client, userdata, message):
    msg = str(message.payload.decode("utf-8"))
    print("massachusetts")
    print(msg)

def on_connect(client, userdata, flags, rc, properties):
    print("Conneticut")
    client.subscribe(topic)

client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)

client.connect(broker, port)

client.on_connect = on_connect

while (True):

    client.on_message = on_message
    client.loop(0.1)