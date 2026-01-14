from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import List
from app.schemas.furniture import FurnitureOut


class OrderCreate(BaseModel):
    email: EmailStr
    furniture_ids: List[int]


class OrderOut(BaseModel):
    id: int
    email: EmailStr
    total_price: int
    created_at: datetime
    items: List[FurnitureOut]

    model_config = {
        "from_attributes": True
    }
