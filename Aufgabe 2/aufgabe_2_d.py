import json
import socket
from datetime import datetime
from confluent_kafka import Consumer
import graphyte

# bootstrap server is the server the kafka server is on
# the offset is the latest
# group id is  for the commiting andgetting the latest group
config = {
    'bootstrap.servers': '10.50.15.52:9092',
    'auto.offset.reset': 'latest',
    'group.id': 'the_mighty_avengers',

}

# instantiate the consumer with config and subscribe to the weather channel
# establish the connection to graphite
cons = Consumer(config)
graphyte.init('10.50.15.52', prefix='system.sync')
cons.subscribe(['weather'])
timestamp_ctr = [0,0,0]
# listen and continuously format the temperatur-data and send it to graphite
while True:
    msg = cons.poll(1.0)
    # ignore msgs that are empty
    if msg is None or msg.error():
        continue
    # listen for data
    data = json.loads(msg.value().decode('utf-8'))
    location = data['city'].replace(' ', '_')
    temperatur = data['tempCurrent']
    timestamp = datetime.strptime(data['timeStamp'], '%Y-%m-%dT%H:%M:%S.%f%z').timestamp()
    # send data to graphite
    if location == 'Mosbach' and timestamp != timestamp_ctr[0]:
        timestamp_ctr[0] = timestamp
    elif location == 'Stuttgart' and timestamp != timestamp_ctr[1]:
        timestamp_ctr[1] = timestamp
    elif location == 'Bad_Mergentheim' and timestamp != timestamp_ctr[2]:
        timestamp_ctr[2] = timestamp
    else:
        continue
    sock = socket.create_connection(('10.50.15.52', 2003), timeout=1)
    try:
        print(temperatur)
        message = f'INF20.group_ttm.{location}.temperature {float(temperatur)} {timestamp}\n'
        sock.send(bytearray(message,encoding='utf-8'))
    finally:
        sock.close()

# close connection
cons.close()
