import json

import paho.mqtt.client as mqtt

def on_connect(client, userdata, flags, rc):
    client.subscribe("/weather/#")

def mqtt_reading(client, userdata, msg):
    weather_obj = json.loads(msg.payload)
    mqtt_output(msg.topic,weather_obj)

def mqtt_output(topc:str,dictionary:dict):
    pass


client = mqtt.Client()
client.on_connect = on_connect
client.on_message = mqtt_reading

client.connect("10.50.12.150", 1883, 60)

client.loop_forever()