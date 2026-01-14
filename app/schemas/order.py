from typing import List
from pydantic import BaseModel, EmailStr
from datetime import datetime

class OrderItemOut(BaseModel):
    id: int
    furniture_id: int
    name: str
    category: str
    price: int

    model_config = {
        "from_attributes": True
    }

class OrderCreate(BaseModel):
    email: EmailStr
    furniture_ids: list[int]

class OrderOut(BaseModel):
    id: int
    email: str
    total_price: int
    created_at: datetime
    items: List[OrderItemOut]

    model_config = {
        "from_attributes": True
    }
