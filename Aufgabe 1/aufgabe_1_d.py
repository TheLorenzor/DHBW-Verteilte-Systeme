import json
import threading
import uuid
import time


import paho.mqtt.client as mqtt

# post to serverstate client id
def on_connect(client, userdata, flags, rc):
    publish_message("/aichat/clientstate",{"clientId":ID_CLIENT,"sender": None, "text": ID_CLIENT+" has connected"})
    client.subscribe("/aichat/default")
    client.will_set("/aichat/clientstate", {"clientId":ID_CLIENT,"sender": None, "text": ID_CLIENT+" has disconnected"}, 0, False)

def mqtt_reading(client, userdata, msg):
    msg_obj = json.loads(msg.payload.decode())
    print_msg_obj(msg.topic, msg_obj)

# printing the object output
def print_msg_obj(topic: str, msg_obj: dict):
    threadLock.acquire()
    sender = msg_obj['sender']
    channel = topic
    msg = msg_obj['text']
    print()
    print('\033[1m' + f'{sender} ({channel}): \033[0m')
    print(msg)
    threadLock.release()

def publish_message(topc: str, text: dict):
    client.publish(topc, json.dumps(text))


def output_thread():
    while True:
        # Wait for user input
        time.sleep(0.5)
        threadLock.acquire()
        threadLock.release()
        message = input("Enter your message: ")
        # Publish the message to the chat topic
        publish_message("/aichat/default", {"clientId":ID_CLIENT,"sender": SENDER, "text": message})

# Start the output thread

threadLock = threading.Lock()
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = mqtt_reading
ID_CLIENT = str(uuid.uuid4())
SENDER = input("Bitte den Namen eingeben:")
client.connect("10.50.12.150", 1883, 60)

thread = threading.Thread(target=output_thread)
thread.start()

client.loop_forever()
