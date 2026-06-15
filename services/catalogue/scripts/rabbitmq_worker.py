import sys
import time

import pika
from utils.config import settings

RABBITMQ_HOST = settings.RABBITMQ_HOST
connection = pika.BlockingConnection(pika.ConnectionParameters(RABBITMQ_HOST))
channel = connection.channel()

channel.queue_declare(queue="temp_queue", durable=True)


def process_message(ch, method, properties, body):
    for i in range(100):
        if i == 40:
            print(f"Received: {body.decode()}")
            print(f"Doing work...")
            time.sleep(3)

            print(f"Simulating crash")
            sys.exit(1)

            # Never gets here
            ch.basic_ack(delivery_tag=method.delivery_tag)
        else:
            print(f"Received: {body.decode()}")
            print(f"Doing work...")
            ch.basic_ack(delivery_tag=method.delivery_tag)


channel.basic_consume(queue="temp_queue", auto_ack=False,
                      on_message_callback=process_message)
print(f"Waiting for messages")
channel.start_consuming()
