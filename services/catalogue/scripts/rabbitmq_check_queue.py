import pika
from utils.config import settings

RABBITMQ_HOST = settings.RABBITMQ_HOST
connection = pika.BlockingConnection(pika.ConnectionParameters(RABBITMQ_HOST))
channel = connection.channel()

queue = channel.queue_declare(queue="temp_queue", passive=True)

print(f"Messages in queue: {queue.method.message_count}")
connection.close()
