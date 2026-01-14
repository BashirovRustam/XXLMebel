from pydantic import BaseModel
from typing import Literal


class FurnitureOut(BaseModel):
    id: int
    name: str
    category: str
    price: int

    model_config = {
        "from_attributes": True
    }