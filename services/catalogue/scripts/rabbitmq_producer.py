# Add the queue without durable and persistent message
import pika
from utils.config import settings
RABBITMQ_HOST = settings.RABBITMQ_HOST
# connect to rabbit mq
connection = pika.BlockingConnection(pika.ConnectionParameters(RABBITMQ_HOST))
# start the channel
channel = connection.channel()
channel.queue_declare(queue="temp_queue", durable=True)
for i in range(100):
    channel.basic_publish(
        exchange="", routing_key="temp_queue", body=f"message-{i}", properties=pika.BasicProperties(delivery_mode=2))
print("Published 100 messages")
connection.close()
