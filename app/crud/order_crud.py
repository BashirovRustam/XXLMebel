from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete, update, func
from sqlalchemy.orm import joinedload
from typing import List, Optional
from datetime import datetime

from app.models.order import Order
from app.models.order_item import OrderItem
from app.models.furniture import Furniture
from app.schemas.order import OrderCreate


class OrderCRUD:
    def __init__(self, session: AsyncSession):
        self.session = session

    # ✅ Создание заказа с вычислением total_price
    async def create(self, order_data: OrderCreate) -> Order:
        # Получаем товары по ID
        result = await self.session.execute(
            select(Furniture).where(Furniture.id.in_(order_data.furniture_ids))
        )
        furniture_items = result.scalars().all()

        if len(furniture_items) != len(order_data.furniture_ids):
            raise ValueError("Some furniture items not found")

        total_price = sum(item.price for item in furniture_items)

        # Создаем заказ
        order = Order(email=order_data.email, total_price=total_price)
        self.session.add(order)
        await self.session.flush()  # получаем order.id без коммита

        # Создаем промежуточные записи order_items
        order_items = [
            OrderItem(order_id=order.id, furniture_id=furniture_id)
            for furniture_id in order_data.furniture_ids
        ]
        self.session.add_all(order_items)

        await self.session.commit()
        await self.session.refresh(order)

        # Загружаем заказ с товарами
        return await self.get_by_id(order.id)

    # ✅ Получить заказ по ID
    async def get_by_id(self, order_id: int) -> Optional[Order]:
        result = await self.session.execute(
            select(Order)
            .options(joinedload(Order.items).joinedload(OrderItem.furniture))
            .where(Order.id == order_id)
        )
        return result.unique().scalar_one_or_none()

    # ✅ Получить все заказы
    async def get_all(self) -> List[Order]:
        result = await self.session.execute(
            select(Order)
            .options(joinedload(Order.items).joinedload(OrderItem.furniture))
            .order_by(Order.created_at.desc())
        )
        return result.unique().scalars().all()

    # ✅ Получить заказы по email клиента
    async def get_by_email(self, email: str) -> List[Order]:
        result = await self.session.execute(
            select(Order)
            .options(joinedload(Order.items).joinedload(OrderItem.furniture))
            .where(Order.email == email)
            .order_by(Order.created_at.desc())
        )
        return result.unique().scalars().all()

    # ✅ Обновление email заказа
    async def update(self, order_id: int, email: Optional[str] = None) -> Optional[Order]:
        order = await self.get_by_id(order_id)
        if not order:
            return None

        if email is not None:
            await self.session.execute(
                update(Order).where(Order.id == order_id).values(email=email)
            )
            await self.session.commit()
            await self.session.refresh(order)

        return order

    # ✅ Удаление заказа
    async def delete(self, order_id: int) -> bool:
        order = await self.get_by_id(order_id)
        if not order:
            return False

        await self.session.execute(delete(Order).where(Order.id == order_id))
        await self.session.commit()
        return True

    # ✅ Получение заказов по диапазону дат
    async def get_by_date_range(self, start_date: datetime, end_date: datetime) -> List[Order]:
        result = await self.session.execute(
            select(Order)
            .options(joinedload(Order.items).joinedload(OrderItem.furniture))
            .where(Order.created_at >= start_date, Order.created_at <= end_date)
            .order_by(Order.created_at.desc())
        )
        return result.unique().scalars().all()

    # ✅ Общая выручка
    async def get_total_revenue(self) -> int:
        result = await self.session.execute(select(func.sum(Order.total_price)))
        return result.scalar() or 0

    # ✅ Количество заказов
    async def get_orders_count(self) -> int:
        result = await self.session.execute(select(func.count(Order.id)))
        return result.scalar() or 0

    # ✅ Добавление мебели в существующий заказ
    async def add_furniture_to_order(self, order_id: int, furniture_id: int) -> Optional[Order]:
        order = await self.get_by_id(order_id)
        if not order:
            return None

        # Проверяем, существует ли мебель
        furniture_result = await self.session.execute(
            select(Furniture).where(Furniture.id == furniture_id)
        )
        furniture = furniture_result.scalar_one_or_none()
        if not furniture:
            raise ValueError("Furniture item not found")

        # Проверяем, есть ли уже в заказе
        existing_item = await self.session.execute(
            select(OrderItem).where(
                OrderItem.order_id == order_id,
                OrderItem.furniture_id == furniture_id
            )
        )
        if existing_item.scalar_one_or_none():
            raise ValueError("Item already in order")

        # Добавляем в заказ
        order_item = OrderItem(order_id=order_id, furniture_id=furniture_id)
        self.session.add(order_item)

        # Обновляем total_price
        new_total = order.total_price + furniture.price
        await self.session.execute(
            update(Order).where(Order.id == order_id).values(total_price=new_total)
        )

        await self.session.commit()
        await self.session.refresh(order)
        return order
