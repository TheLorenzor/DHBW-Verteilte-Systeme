import json
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
graphyte.init('10.50.15.52',prefix='system.sync')
cons.subscribe(['weather'])

# listen and continuously format the temperatur-data and send it to graphite
while True:
    msg = cons.poll(1.0)
    # ignore msgs that are empty
    if msg is None or msg.error():
        continue
    # listen for data
    data = json.loads(msg.value().decode('utf-8'))
    location = data['city'].replace(' ','_')
    temperatur = data['tempCurrent']
    timestamp = datetime.strptime(data['timeStamp'],'%Y-%m-%dT%H:%M:%S.%f%z').timestamp()*1000
    # send data to graphite
    print(temperatur)
    graphyte.send('INF20.group_ttm.'+location+'.temperature',float(temperatur))

# close connection
cons.close()