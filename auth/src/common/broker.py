from confluent_kafka import Producer, Consumer
import socket

from src.event import Event

conf = {'bootstrap.servers': "62.84.123.200:9092"}

producer = Producer(conf)

def acked(err, msg):
    if err is not None:
        print("Failed to deliver message: %s: %s" % (str(msg), str(err)))
    else:
        print("Message produced: %s" % (str(msg)))



def publish(topic: str, event: Event):
    producer.produce(topic, key="user", value=event.json(), callback=acked)
    producer.flush()


conf = {'bootstrap.servers': "62.84.123.200:9092",
        'group.id': "foo",
        'auto.offset.reset': 'smallest'}

consumer = Consumer(conf)
