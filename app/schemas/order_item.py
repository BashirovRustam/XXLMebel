from pydantic import BaseModel

class OrderItemOut(BaseModel):
    id: int
    furniture_id: int
    name: str
    category: str
    price: int

    class Config:
        orm_mode = True

    @classmethod
    def from_orm_item(cls, order_item):
        """Создаёт OrderItemOut из SQLAlchemy OrderItem"""
        return cls(
            id=order_item.id,
            furniture_id=order_item.furniture_id,
            name=order_item.furniture.name,
            category=order_item.furniture.category,
            price=order_item.furniture.price
        )
