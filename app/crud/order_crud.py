import os
from email.message import EmailMessage
import aiosmtplib
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete, update, func
from sqlalchemy.orm import joinedload
from typing import List, Optional
from datetime import datetime

from app.models.order import Order
from app.models.order_item import OrderItem
from app.models.furniture import Furniture
from app.schemas.order import OrderCreate, OrderOut, OrderItemOut


class OrderCRUD:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def send_order_email(self, order: OrderOut):
        """
        Асинхронная отправка email через локальный SMTP (MailHog)
        """
        message = EmailMessage()
        message["From"] = os.getenv("EMAIL_FROM", "no-reply@example.com")
        message["To"] = order.email
        message["Subject"] = f"Ваш заказ #{order.id} подтвержден"

        items_text = "\n".join(
            f"- {item.name} ({item.category}) — {item.price} тенге." for item in order.items
        )
        message.set_content(
            f"Здравствуйте!\n\nВаш заказ #{order.id} был успешно создан.\n\n"
            f"Состав заказа:\n{items_text}\n\n"
            f"Итоговая сумма: {order.total_price} тенге.\n\nСпасибо за покупку!"
        )

        smtp_host = os.getenv("SMTP_HOST", "mailhog")
        smtp_port = int(os.getenv("SMTP_PORT", 1025))

        try:
            await aiosmtplib.send(message, hostname=smtp_host, port=smtp_port)
            print(f"✅ Email sent to {order.email}")
        except Exception as e:
            print(f"❌ Failed to send email: {e}")

    async def create(self, order_data: OrderCreate) -> OrderOut:
        # 1️⃣ Получаем мебель
        result = await self.session.execute(
            select(Furniture).where(Furniture.id.in_(order_data.furniture_ids))
        )
        furniture_items = result.scalars().all()

        if len(furniture_items) != len(order_data.furniture_ids):
            raise ValueError("Some furniture items not found")

        # 2️⃣ Считаем total_price
        total_price = sum(item.price for item in furniture_items)

        # 3️⃣ Создаем заказ
        order = Order(email=order_data.email, total_price=total_price)
        self.session.add(order)
        await self.session.flush()  # чтобы получить order.id

        # 4️⃣ Создаем OrderItem
        order_items = [
            OrderItem(order_id=order.id, furniture_id=f.id) for f in furniture_items
        ]
        self.session.add_all(order_items)

        await self.session.commit()
        await self.session.refresh(order)

        # 5️⃣ Формируем OrderOut с вложенными предметами
        items_out = [
            OrderItemOut(
                id=item.id,
                furniture_id=item.furniture.id,
                name=item.furniture.name,
                category=item.furniture.category,
                price=item.furniture.price
            )
            for item in order_items
        ]

        order_out = OrderOut(
            id=order.id,
            email=order.email,
            total_price=order.total_price,
            created_at=order.created_at,
            items=items_out
        )

        # 6️⃣ Отправка email
        await self.send_order_email(order_out)

        return order_out

    async def get_by_email(self, email: str) -> List[Order]:
        result = await self.session.execute(
            select(Order)
            .options(
                joinedload(Order.items)
                .joinedload(OrderItem.furniture)
            )
            .where(Order.email == email)
            .order_by(Order.created_at.desc())
        )
        return result.unique().scalars().all()
