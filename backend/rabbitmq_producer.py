# backend/rabbitmq_producer.py

import asyncio
import json
from aio_pika import connect_robust, Message

RABBITMQ_URL = "amqp://guest:guest@rabbitmq:5672/"  # default RabbitMQ URL

async def publish_notification(payload: dict):
    connection = await connect_robust(RABBITMQ_URL)
    async with connection:
        channel = await connection.channel()
        queue = await channel.declare_queue("notification_queue", durable=True)

        message_body = json.dumps(payload).encode()
        message = Message(message_body)

        await channel.default_exchange.publish(message, routing_key=queue.name)
