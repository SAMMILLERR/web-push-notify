# backend/main.py
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import asyncio

from rabbitmq_producer import publish_notification

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-memory token storage
FCM_TOKENS = []

class FCMTokenRequest(BaseModel):
    fcm_token: str

class NotificationPayload(BaseModel):
    title: str
    body: str
    image_url: str = None
    action_url: str = None
    data: dict = {}

@app.get("/")
def read_root():
    return {"message": "Welcome to the Notification Service"}

@app.post("/devices/register")
def register_device(payload: FCMTokenRequest):
    if payload.fcm_token not in FCM_TOKENS:
        FCM_TOKENS.append(payload.fcm_token)
    return {"message": "Token registered", "total_tokens": len(FCM_TOKENS)}

@app.post("/notifications/publish")
async def publish_notification_endpoint(payload: NotificationPayload):
    if not FCM_TOKENS:
        raise HTTPException(status_code=400, detail="No devices registered")
    
    # Add FCM tokens to payload
    payload_dict = payload.dict()
    payload_dict["fcm_tokens"] = FCM_TOKENS

    # Send to RabbitMQ
    await publish_notification(payload_dict)

    return {"message": "Notification queued for delivery"}
