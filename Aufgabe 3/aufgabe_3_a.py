from confluent_kafka import Consumer, KafkaError, TopicPartition

# Set up consumer properties
bootstrap_servers = '10.50.15.52:9092'
group_id = 'the_mighty_avengers'
topic_name = 'tankerkoenig'

# Create a KafkaConsumer object
consumer = Consumer({
    'bootstrap.servers': bootstrap_servers,
    'group.id': group_id,
    'auto.offset.reset': 'earliest',
    'enable.auto.commit': False
})

# Manually assign partitions to the consumer
partition0 = TopicPartition(topic_name, 0)
partition1 = TopicPartition(topic_name, 1)
consumer.assign([partition0, partition1])

# Start consuming data
while True:

    msg = consumer.poll(1.0)
    # ignore msgs that are empty
    if msg is None or msg.error():
        continue
    # listen for data
    print(msg.value().decode('utf-8'))
consumer.close()