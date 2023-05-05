from concurrent.futures import ThreadPoolExecutor

import graphyte
from confluent_kafka import Consumer, KafkaError, TopicPartition
import time
import json
from datetime import datetime

# Set up consumer properties
bootstrap_servers = '10.50.15.52:9092'
group_id = 'the_mighty_avengers'
topic_name = 'tankerkoenig'

# Get the number of partitions for the topic
consumer = Consumer({
    'bootstrap.servers': bootstrap_servers,
    'group.id': group_id,
    'auto.offset.reset': 'earliest',
    'enable.auto.commit': False
})
metadata = consumer.list_topics(topic=topic_name)
num_partitions = len(metadata.topics[topic_name].partitions)
graphyte.init('10.50.15.52', prefix='system.sync')

# Define a dictionary to store the aggregated data
aggregated_data = {}


# Define a function to consume messages from a single partition
def consume_partition(partitionIndex):
    consumer = Consumer({
        'bootstrap.servers': bootstrap_servers,
        'group.id': group_id,
        'auto.offset.reset': 'earliest',
        'enable.auto.commit': False
    })
    partition = TopicPartition(topic_name, partitionIndex)
    consumer.assign([partition])
    while True:
        message = consumer.poll(timeout=1.0)
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
                    graphyte.send('INF20.group_ttm.tankerkoenig' + key + '.e5_price',
                                  aggregated_data[key]['timestamp'], float(aggregated_data[key]['pE5']))
                    graphyte.send('INF20.group_ttm.tankerkoenig' + key + '.e10_price',
                                  aggregated_data[key]['timestamp'], float(aggregated_data[key]['pE10']))
                    graphyte.send('INF20.group_ttm.tankerkoenig' + key + '.pDie_price',
                                  aggregated_data[key]['timestamp'], float(aggregated_data[key]['pDie']))
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
    consumer.close()

# Use a thread pool to consume messages from all partitions in parallel
with ThreadPoolExecutor(max_workers=num_partitions) as executor:
    for partition in range(num_partitions):
        executor.submit(consume_partition, partition)
