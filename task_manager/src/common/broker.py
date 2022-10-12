from time import sleep
from typing import Any, Callable, Type
from confluent_kafka import Producer, Consumer
from pydantic import BaseModel

from threading import Thread
from src.common.event import Event

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
        'auto.offset.reset': 'latest'}


consumer = Consumer(conf)

def _subscribe(topic: str, model: Type[BaseModel], callback: Callable, kwargs: dict[str, Any]):
    while True:
        print("Listening to", topic)
        msg = consumer.poll(1)

        if msg is None:
            sleep(2)
            continue

        if msg.error():
            print(msg.error())

            continue

        print(msg.value())
        args = {"event": model.parse_raw(msg.value()), **kwargs}
        print(args)
        callback(**args)
        consumer.commit()


def subscribe(topic: str, model: Type[BaseModel], callback: Callable, kwargs: dict[str, Any]):
    consumer.subscribe([topic])
    thread = Thread(target=_subscribe, args=[topic, model, callback, kwargs], daemon=True)
    thread.start()


