from confluent_kafka import Consumer
# bootstrap server is the server the kafka server is on
# the offset is the latest
# group id is  for the commiting andgetting the latest group
config = {
    'bootstrap.servers': '10.50.15.52:9092',
    'auto.offset.reset': 'latest',
    'group.id': 'the_mighty_avengers',

}
# instantiate the consumer with config and subscribe to the weather channel
cons = Consumer(config)

cons.subscribe(['weather'])
# listen and just continuously copy it
while True:
    msg = cons.poll(1.0)
    # ignore msgs that are empty
    if msg is None:
        continue
    if msg.error():
        break
    # print the value and decode it to utf8 to prevent errors
    print(msg.value().decode('utf-8'))
# close connection
cons.close()