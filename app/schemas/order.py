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
    items: List[OrderItemOut]

    class Config:
        orm_mode = True

    @classmethod
    def from_orm_order(cls, order):
        return cls(
            id=order.id,
            email=order.email,
            total_price=order.total_price,
            created_at=order.created_at,
            items=[OrderItemOut.from_orm_item(item) for item in order.items]
        )
