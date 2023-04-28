from confluent_kafka import Consumer

config = {
    'bootstrap.servers': '10.50.15.52:9092',
    'auto.offset.reset': 'latest',
    'group.id': 'the mighty avengers',

}

cons = Consumer(config)

cons.subscribe(['weather'])

while True:
    msg = cons.poll(1.0)
    if msg is None:
        continue
    if msg.error():
        break
    print(msg.value().decode('utf-8'))

cons.close()