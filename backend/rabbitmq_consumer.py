# backend/rabbitmq_consumer.py

import asyncio
import json
from aio_pika import connect_robust, IncomingMessage
import firebase_admin
from firebase_admin import credentials, messaging

# Firebase Init
cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred)

RABBITMQ_URL = "amqp://guest:guest@localhost:5672/"

async def send_push_notification(payload: dict):
    fcm_tokens = payload.get("fcm_tokens", [])

    if not fcm_tokens:
        print(" No FCM tokens provided in payload. Skipping.")
        return

    notification = messaging.Notification(
        title=payload.get("title", "No Title"),
        body=payload.get("body", ""),
        image=payload.get("image_url")
    )

    data = payload.get("data", {})
    webpush = messaging.WebpushConfig(
        fcm_options=messaging.WebpushFCMOptions(
            link=payload.get("action_url", "https://example.com")
        )
    )

    try:
        if len(fcm_tokens) == 1:
            # Single recipient
            message = messaging.Message(
                notification=notification,
                token=fcm_tokens[0],
                data={k: str(v) for k, v in data.items()},
                webpush=webpush
            )
            response = messaging.send(message)
            print(f" Sent to 1 device")
        else:
            # Multiple recipients
            message = messaging.MulticastMessage(
                notification=notification,
                tokens=fcm_tokens,
                data={k: str(v) for k, v in data.items()},
                webpush=webpush
            )
            response = messaging.send_multicast(message)
            print(f" Sent to {response.success_count}/{len(fcm_tokens)} devices")

    except Exception as e:
        print(" Firebase send error:", e)
        print(" Payload was:", json.dumps(payload, indent=2))


async def handle_message(message: IncomingMessage):
    async with message.process():
        try:
            payload = json.loads(message.body)
            print(" Message received:", payload)
            await send_push_notification(payload)
        except Exception as e:
            print(" Error handling message:", e)
            print(" Raw message body:", message.body.decode())

async def main():
    connection = await connect_robust(RABBITMQ_URL)
    channel = await connection.channel()
    queue = await channel.declare_queue("notification_queue", durable=True)
    print(" Listening for notifications...")
    await queue.consume(handle_message)

if __name__ == "__main__":
    asyncio.run(main())
