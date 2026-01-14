from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from app.db.base import get_session
from app.schemas.order import OrderCreate, OrderOut, OrderItemOut
from app.crud.order_crud import OrderCRUD

router = APIRouter(
    prefix="/orders",
    tags=["Заказ"]
)


@router.post("/", response_model=OrderOut)
async def create_order(
    order_in: OrderCreate,
    session: AsyncSession = Depends(get_session)
):
    crud = OrderCRUD(session)
    try:
        order_out = await crud.create(order_in)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    return order_out


@router.get("/", response_model=List[OrderOut])
async def get_orders(
        email: str = Query(...),
        session: AsyncSession = Depends(get_session)
):
    crud = OrderCRUD(session)
    orders = await crud.get_by_email(email)

    return [
        OrderOut(
            id=order.id,
            email=order.email,
            total_price=order.total_price,
            created_at=order.created_at,
            items=[
                OrderItemOut(
                    id=item.id,
                    furniture_id=item.furniture_id,
                    name=item.furniture.name,
                    category=item.furniture.category,
                    price=item.furniture.price
                )
                for item in order.items
            ]
        )
        for order in orders
    ]