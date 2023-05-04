

from confluent_kafka import Consumer
config = {
    'bootstrap.servers': '10.50.15.52:9092',
    'auto.offset.reset': 'latest',
    'group.id': 'the_mighty_avengers',

}

# instantiate the consumer with config and subscribe to the weather channel
# establish the connection to graphite
cons = Consumer(config)
cons.subscribe(['tankerkoenig'])


while True:
    msg = cons.poll(1.0)
    print("abc")
    # ignore msgs that are empty
    if msg is None or msg.error():
        continue
    # listen for data
    print(msg.value().decode('utf-8'))

# close connection
cons.close()