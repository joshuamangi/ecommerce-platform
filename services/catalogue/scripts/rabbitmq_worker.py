import sys
import time

import pika
import redis
from utils.config import settings

REDIS_HOST = settings.REDIS_HOST
REDIS_PORT = settings.REDIS_PORT

redis_client = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=0)

RABBITMQ_HOST = settings.RABBITMQ_HOST
connection = pika.BlockingConnection(pika.ConnectionParameters(RABBITMQ_HOST))
channel = connection.channel()

channel.exchange_declare(
    exchange="temp_dlx", exchange_type="direct", durable=True)
channel.queue_declare(queue="temp_dlq", durable=True)
channel.queue_bind(queue="temp_dlq", exchange="temp_dlx",
                   routing_key="failed_temp")
channel.queue_declare(queue="temp_queue", durable=True, arguments={
    "x-dead-letter-exchange": "temp_dlx",
    "x-dead-letter-routing-key": "failed_temp"})


def process_message(ch, method, properties, body):
    print(f"Received: {body.decode()}")
    lock_key = f"processed_order: {body.decode()}"
    # nx means not exists
    # ex means expiry ttl, for this case 24 hours
    is_new = redis_client.set(lock_key, "locked", nx=True, ex=86400)

    if not is_new:
        print(f"Skipping processing")
        return

    try:
        print(f"Doing work...")
        time.sleep(5)

        # Uncomment to simulate crash
        # print(f"Simulating crash")
        # sys.exit(1)
        if body.decode() == "message-10" or body.decode() == "message-12":
            ch.basic_reject(delivery_tag=method.delivery_tag, requeue=False)
            return
        ch.basic_ack(delivery_tag=method.delivery_tag)
    except Exception as e:
        redis_client.delete(lock_key)
        raise e


channel.basic_qos(prefetch_count=1)
channel.basic_consume(queue="temp_queue", auto_ack=False,
                      on_message_callback=process_message)
print(f"Waiting for messages")
channel.start_consuming()
