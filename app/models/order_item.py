from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base


class OrderItem(Base):
    __tablename__ = "order_items"

    id: Mapped[int] = mapped_column(primary_key=True)
    order_id: Mapped[int] = mapped_column(ForeignKey("orders.id"))
    furniture_id: Mapped[int] = mapped_column(ForeignKey("furniture.id"))

    order = relationship("Order", back_populates="items")
    furniture = relationship("Furniture")
