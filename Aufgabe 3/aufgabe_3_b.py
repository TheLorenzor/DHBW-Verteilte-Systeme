from concurrent.futures import ThreadPoolExecutor
import socket
from confluent_kafka import Consumer, KafkaError, TopicPartition
import time
import json
from datetime import datetime
import graphyte

# Set up consumer properties
bootstrap_servers = '10.50.15.52:9092'
group_id = 'the_mighty_avengers'
topic_name = 'tankerkoenig'


num_partitions = 10
graphyte.init('10.50.15.52', prefix='system.sync')
# Define a dictionary to store the aggregated data
aggregated_data = {}


def convertTime(dt):
    print(dt)
    timestamp_s = (int)(dt.timestamp() // 1000)
    # format timestamp as string in Graphite format
    return timestamp_s


def sendMessage(sock,group, fuel, price, timestamp):

    path = 'INF20.group_ttm.tankerkoenig.'+group+"."+fuel
    message = f'{path} {price} {timestamp.timestamp()}\n'
    print(message)
    sock.send(bytearray(message, encoding='utf-8'))

# Define a function to consume messages from a single partition
def consume_partition(partitionIndex):
    consumers = Consumer({
        'bootstrap.servers': bootstrap_servers,
        'group.id': group_id,
        'auto.offset.reset': 'earliest',
    })
    partitions = TopicPartition(topic_name, partitionIndex)
    consumers.assign([partitions])
    while True:
        sock = socket.create_connection(('10.50.15.52', 2003), timeout=1)
        message = consumers.poll(timeout=1.0)
        if message is None:
            print("is none")
            continue

        if message.error():
            print(f"Error while consuming message: {message.error()}")
        else:
            print("no error")
            # Parse the message as a JSON object
            message_data = json.loads(message.value().decode('utf-8'))
            # Extract the PLZ and timestamp from the message
            plz = message_data['plz']
            timestamp = datetime.fromisoformat(message_data['dat'])
            # Truncate the timestamp to the nearest hour
            timestamp = timestamp.replace(minute=0, second=0, microsecond=0)
            # Create a dictionary key for the PLZ and hour
            key = f"{partitionIndex}"
            if key not in aggregated_data:
                aggregated_data[key] = {'timestamp': 0, 'pE5': 0.0, 'pE10': 0.0, 'pDie': 0.0, 'count': 0}
            if key in aggregated_data:
                if aggregated_data[key]['timestamp'] != timestamp and aggregated_data[key]['timestamp'] != 0:
                    # send to graphite
                    print("send")
                    try:
                        sendMessage(sock, key, 'pE5', aggregated_data[key]['pE5'], aggregated_data[key]['timestamp'])
                        sendMessage(sock, key, 'pE10', aggregated_data[key]['pE10'], aggregated_data[key]['timestamp'])
                        sendMessage(sock, key, 'pDie', aggregated_data[key]['pDie'], aggregated_data[key]['timestamp'])
                    finally:
                        sock.close()
                    # reset values
                    aggregated_data[key] = {'timestamp': 0, 'pE5': 0.0, 'pE10': 0.0, 'pDie': 0.0, 'count': 0}
            # Add the message's pE5 and pE10 values to the aggregated data

            aggregated_data[key]['timestamp'] = timestamp
            aggregated_data[key]['count'] += 1
            if message_data['pE5'] is not None:
                aggregated_data[key]['pE5'] = (aggregated_data[key]['pE5'] * (aggregated_data[key]['count'] - 1) +
                                               message_data['pE5']) / aggregated_data[key]['count']
            if message_data['pE10'] is not None:
                aggregated_data[key]['pE10'] = (aggregated_data[key]['pE10'] * (aggregated_data[key]['count'] - 1) +
                                                message_data['pE10']) / aggregated_data[key]['count']
            if message_data['pDie'] is not None:
                aggregated_data[key]['pDie'] = (aggregated_data[key]['pDie'] * (aggregated_data[key]['count'] - 1) +
                                                message_data['pDie']) / aggregated_data[key]['count']

            # Output the current aggregated data for the PLZ and hour
            # print(f"{key}: {aggregated_data[key]}from partition: {message.partition()}")
    sock.close()


# Use a thread pool to consume messages from all partitions in parallel
with ThreadPoolExecutor(max_workers=num_partitions) as executor:
    for partition in range(num_partitions):
        executor.submit(consume_partition, partition)
