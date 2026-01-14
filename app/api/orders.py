from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from app.db.base import get_session
from app.schemas.order import OrderCreate, OrderOut
from app.crud.order_crud import OrderCRUD

router = APIRouter(
    prefix="/orders",
    tags=["Заказ"]
)


# POST /orders/ — создание заказа
@router.post("/", response_model=OrderOut)
async def create_order(
    order_in: OrderCreate,
    session: AsyncSession = Depends(get_session)
):
    crud = OrderCRUD(session)
    try:
        order = await crud.create(order_in)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    return order


# GET /orders/?email= — список заказов по email
@router.get("/", response_model=List[OrderOut])
async def get_orders(
    email: str = Query(...),
    session: AsyncSession = Depends(get_session)
):
    crud = OrderCRUD(session)
    orders = await crud.get_by_email(email)
    return orders
