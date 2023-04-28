import time
from confluent_kafka import Producer

config = {
    'bootstrap.servers': '10.50.15.52:9092',
}

prod = Producer(config)


prod.poll(0)
data = 'diest ist ein test'
prod.produce('vlvs_inf20_the_mighty_avengers',data.encode('utf-8'))
prod.flush()
