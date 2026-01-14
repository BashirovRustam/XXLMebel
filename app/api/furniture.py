from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional

from app.db.base import get_session
from app.schemas.furniture import FurnitureOut
from app.models.furniture import Furniture
from app.crud.furniture_crud import FurnitureCRUD

router = APIRouter(
    prefix="/furniture",
    tags=["Мебель"]
)


# GET /furniture/ — список всей мебели
@router.get("/", response_model=List[FurnitureOut])
async def get_all_furniture(session: AsyncSession = Depends(get_session)):
    crud = FurnitureCRUD(session)
    return await crud.get_all()


# GET /furniture/{id} — информация о конкретном товаре
@router.get("/{furniture_id}", response_model=FurnitureOut)
async def get_furniture(furniture_id: int, session: AsyncSession = Depends(get_session)):
    crud = FurnitureCRUD(session)
    furniture = await crud.get_by_id(furniture_id)
    if not furniture:
        raise HTTPException(status_code=404, detail="Furniture not found")
    return furniture

#
# # GET /furniture/category/{category} — фильтр по категории
# @router.get("/category/{category}", response_model=List[FurnitureOut])
# async def get_furniture_by_category(category: str, session: AsyncSession = Depends(get_session)):
#     crud = FurnitureCRUD(session)
#     return await crud.get_by_category(category)
#
#
# # GET /furniture/price?min=&max= — фильтр по диапазону цен
# @router.get("/price", response_model=List[FurnitureOut])
# async def get_furniture_by_price_range(
#     min_price: int = Query(0, ge=0),
#     max_price: int = Query(10_000_000, ge=0),
#     session: AsyncSession = Depends(get_session)
# ):
#     crud = FurnitureCRUD(session)
#     return await crud.get_by_price_range(min_price, max_price)
