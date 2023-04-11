import json

import paho.mqtt.client as mqtt

def on_connect(client, userdata, flags, rc):
    client.subscribe("/weather/#")

def mqtt_reading(client, userdata, msg):
    weather_obj = json.loads(msg.payload)
    mqtt_output(msg.topic,weather_obj)

def mqtt_output(topc:str,dictionary:dict):
    if topc.startswith("/weather"):
        city = dictionary.get("city")
        temp_current = dictionary.get("tempCurrent")
        temp_max = dictionary.get("tempMax")
        temp_min = dictionary.get("tempMin")
        comment = dictionary.get("comment")
        timestamp = dictionary.get("timeStamp")

        print(f"Weather data for {city} at {timestamp}:")
        print(f"Current temperature: {temp_current}")
        print(f"Max temperature: {temp_max}")
        print(f"Min temperature: {temp_min}")
        print(f"Comment: {comment}")
        print("-----------")


client = mqtt.Client()
client.on_connect = on_connect
client.on_message = mqtt_reading

client.connect("10.50.12.150", 1883, 60)

client.loop_forever()