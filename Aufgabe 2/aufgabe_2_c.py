# Import the Producer class from the confluent_kafka library
from confluent_kafka import Producer

# Set the configuration for the Kafka Producer
config = {
    'bootstrap.servers': '10.50.15.52:9092',
}

# Create a Kafka Producer instance with the configuration
prod = Producer(config)

# Call poll() to make sure any queued messages are delivered before sending new ones
prod.poll(0)
# Create a message to send
data = 'diest ist ein test'
# Use the produce() method to send the message to a Kafka topic called 'vlvs_inf20_the_mighty_avengers'
prod.produce('vlvs_inf20_the_mighty_avengers',data.encode('utf-8'))
# Call flush() to make sure any remaining messages are delivered before closing the producer
prod.flush()
