from pydantic import BaseModel
from typing import List
from datetime import date


# ---------- Top Products ----------
class TopProduct(BaseModel):
    product: str
    count: int


# ---------- Channel Activity ----------
class ChannelActivity(BaseModel):
    channel_name: str
    date: date
    message_count: int


# ---------- Message Search ----------
class MessageResult(BaseModel):
    message_id: int
    channel_name: str
    message_text: str
    views: int


# ---------- Visual Content Stats ----------
class VisualContentStat(BaseModel):
    channel_name: str
    category: str
    image_count: int
