from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional

from app.db.base import get_session
from app.schemas.furniture import FurnitureOut, FurnitureCreate
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

# POST /furniture/ — создать мебель
@router.post("/", response_model=FurnitureOut)
async def create_furniture(
    furniture_in: FurnitureCreate,
    session: AsyncSession = Depends(get_session)
):
    crud = FurnitureCRUD(session)
    return await crud.create(
        name=furniture_in.name,
        category=furniture_in.category,
        price=furniture_in.price
    )