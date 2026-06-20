# Add the queue without durable and persistent message
import pika
import sys
from utils.config import settings
RABBITMQ_HOST = settings.RABBITMQ_HOST
# connect to rabbit mq
connection = pika.BlockingConnection(pika.ConnectionParameters(RABBITMQ_HOST))
# start the channel
channel = connection.channel()
channel.exchange_declare(
    exchange="temp_dlx", exchange_type="direct", durable=True)
channel.queue_declare(queue="temp_dlq", durable=True)
channel.queue_bind(queue="temp_dlq", exchange="temp_dlx",
                   routing_key="failed_temp")
channel.queue_declare(queue="temp_queue", durable=True, arguments={
    "x-dead-letter-exchange": "temp_dlx",
    "x-dead-letter-routing-key": "failed_temp"})
channel.confirm_delivery()
for i in range(100):
    channel.basic_publish(
        exchange="", routing_key="temp_queue", body=f"message-{i}", properties=pika.BasicProperties(delivery_mode=2))
print(sys.argv[1:])
print("Published 100 messages")
connection.close()
