# app/schemas/order.py
from typing import List
from pydantic import BaseModel, EmailStr
from datetime import datetime
from app.schemas.order_item import OrderItemOut

class OrderCreate(BaseModel):
    email: EmailStr
    furniture_ids: list[int]

class OrderOut(BaseModel):
    id: int
    email: str
    total_price: int
    created_at: datetime
    items: List[OrderItemOut]  # вложенные товары

    class Config:
        orm_mode = True
