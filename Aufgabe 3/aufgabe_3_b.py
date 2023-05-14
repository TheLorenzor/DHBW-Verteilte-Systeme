from concurrent.futures import ThreadPoolExecutor
import socket
from confluent_kafka import Consumer, KafkaError, TopicPartition
import time
import json
from datetime import datetime
import graphyte

# Set up consumer properties
bootstrap_servers = '10.50.15.52:9092'
topic_name = 'tankerkoenig'

# Get the number of partitions for the topic
consumer = Consumer({
    'bootstrap.servers': bootstrap_servers,
    'group.id': 'the_mighty_avengers',
    'auto.offset.reset': 'earliest',
})
metadata = consumer.list_topics(topic=topic_name)
num_partitions = len(metadata.topics[topic_name].partitions)

# Define a dictionary to store the aggregated data
aggregated_data = {}


# Define a function to consume messages from a single partition
def consume_partition(partitionIndex):
    consumers = Consumer({
        'bootstrap.servers': bootstrap_servers,
        'group.id': group_id,
        'auto.offset.reset': 'earliest',
    })
    partitions = TopicPartition(topic_name, partitionIndex)
    consumers.assign([partitions])
    sock = socket.create_connection(('10.50.15.52', 2003), timeout=1)
    while True:
        
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
                    sendMessage(sock,'pE5',aggregated_data[key]['pE5'],aggregated_data[key]['timestamp'])
                    sendMessage(sock,'pE10',aggregated_data[key]['pE10'],aggregated_data[key]['timestamp'])
                    sendMessage(sock,'pDie',aggregated_data[key]['pDie'],aggregated_data[key]['timestamp'])
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
            #print(f"{key}: {aggregated_data[key]}from partition: {message.partition()}")
        sock.close()
# Use a thread pool to consume messages from all partitions in parallel
with ThreadPoolExecutor(max_workers=num_partitions) as executor:
    for partition in range(num_partitions):
        executor.submit(consume_partition, partition)

def convertTime(dt):
    timestamp_s = dt.timestamp() // 1000
    # format timestamp as string in Graphite format
    result = datetime.datetime.utcfromtimestamp(timestamp_s).strftime('%Y-%m-%d %H:%M:%S')
    return result

def sendMessage(sock,fuel,price,timestamp):
        message = f'INF20.group_ttm.tankerkoenig.{fuel}.{float(price)} {timestamp}\n'
        sock.send(bytearray(message,encoding='utf-8'))