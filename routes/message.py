# app/routes/message.py
from fastapi import APIRouter, HTTPException
from models.message import Message
from pydantic import BaseModel
from uuid import UUID
from datetime import datetime

router = APIRouter()

class MessageCreate(BaseModel):
    sender_id: UUID
    receiver_id: UUID
    content: str


@router.post("/send")
async def send_message(message: MessageCreate):
    new_message = Message(
        sender_id=message.sender_id,
        receiver_id=message.receiver_id,
        content=message.content,
        timestamp=datetime.utcnow(),
        is_read=False
    )
    await new_message.insert()
    return {"message": "Message sent successfully", "message_id": new_message.id}


@router.get("/received/{user_id}")
async def get_received_messages(user_id: UUID):
    messages = await Message.find(Message.receiver_id == user_id).to_list()
    return messages


@router.get("/sent/{user_id}")
async def get_sent_messages(user_id: UUID):
    messages = await Message.find(Message.sender_id == user_id).to_list()
    return messages


@router.put("/{message_id}/read")
async def mark_message_as_read(message_id: UUID):
    message = await Message.get(message_id)
    if not message:
        raise HTTPException(status_code=404, detail="Message not found")
    
    await message.set({"is_read": True})
    return {"message": "Message marked as read"}
