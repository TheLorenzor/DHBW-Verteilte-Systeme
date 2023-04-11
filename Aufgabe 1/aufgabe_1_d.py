import json
import threading
import uuid
import time

import paho.mqtt.client as mqtt


# post to serverstate client id
def on_connect(client, userdata, flags, rc):
    # send a message to Publish and clientstate
    publish_message("/aichat/clientstate",
                    {"clientId": ID_CLIENT, "sender": None, "text": ID_CLIENT + " has connected"})
    client.subscribe("/aichat/default")
    #
    client.will_set("/aichat/clientstate",
                    {"clientId": ID_CLIENT, "sender": None, "text": ID_CLIENT + " has disconnected"}, 0, False)


def mqtt_reading(client, userdata, msg):
    msg_obj = json.loads(msg.payload.decode())
    print_msg_obj(msg.topic, msg_obj)


# printing the object output of the message --> is defined as
def print_msg_obj(topic: str, msg_obj: dict):
    """

    :param topic: the topic given by the client
    :param msg_obj:  the message object containing the text
    :return:
    """
    # locking it to prevent any inputs by the user
    threadLock.acquire()
    sender = msg_obj['sender']
    channel = topic
    msg = msg_obj['text']
    print()
    # print everything
    print('\033[1m' + f'{sender} ({channel}): \033[0m')
    print(msg)
    threadLock.release()

# publish the message to the client and dumping the json client
def publish_message(topc: str, text: dict):
    client.publish(topc, json.dumps(text))


def output_thread():
    while True:
        # Wait for user input
        # waiot half a second to overwrite the input
        time.sleep(0.5)
        threadLock.acquire()
        threadLock.release()
        message = input("Enter your message: ")
        # Publish the message to the chat topic
        publish_message("/aichat/default", {"clientId": ID_CLIENT, "sender": SENDER, "text": message})


# Start the output thread
# starting lock
threadLock = threading.Lock()
# start client and on connect
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = mqtt_reading
# create a unique id
ID_CLIENT = str(uuid.uuid4())
# give the sender a name
SENDER = input("Bitte den Namen eingeben:")
client.connect("10.50.12.150", 1883, 60)
# starting threads to make input and output parallel
thread = threading.Thread(target=output_thread)
thread.start()

client.loop_forever()
