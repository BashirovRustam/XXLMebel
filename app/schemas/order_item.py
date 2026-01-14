from pydantic import BaseModel

class OrderItemOut(BaseModel):
    id: int
    furniture_id: int
    name: str
    category: str
    price: int

    class Config:
        orm_mode = True