from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete, update
from sqlalchemy.orm import selectinload
from typing import List, Optional

from app.models.furniture import Furniture
from app.schemas.furniture import FurnitureOut


class FurnitureCRUD:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, name: str, category: str, price: int) -> Furniture:
        furniture = Furniture(name=name, category=category, price=price)
        self.session.add(furniture)
        await self.session.commit()
        await self.session.refresh(furniture)
        return furniture

    async def get_by_id(self, furniture_id: int) -> Optional[Furniture]:
        result = await self.session.execute(
            select(Furniture).where(Furniture.id == furniture_id)
        )
        return result.scalar_one_or_none()

    async def get_all(self, category: Optional[str] = None) -> List[Furniture]:
        query = select(Furniture)
        if category:
            query = query.where(Furniture.category == category)
        result = await self.session.execute(query)
        return result.scalars().all()

    async def get_by_category(self, category: str) -> List[Furniture]:
        result = await self.session.execute(
            select(Furniture).where(Furniture.category == category)
        )
        return result.scalars().all()

    async def update(
        self, 
        furniture_id: int, 
        name: Optional[str] = None, 
        category: Optional[str] = None, 
        price: Optional[int] = None
    ) -> Optional[Furniture]:
        furniture = await self.get_by_id(furniture_id)
        if not furniture:
            return None

        update_data = {}
        if name is not None:
            update_data["name"] = name
        if category is not None:
            update_data["category"] = category
        if price is not None:
            update_data["price"] = price

        if update_data:
            await self.session.execute(
                update(Furniture)
                .where(Furniture.id == furniture_id)
                .values(**update_data)
            )
            await self.session.commit()
            await self.session.refresh(furniture)

        return furniture

    async def delete(self, furniture_id: int) -> bool:
        furniture = await self.get_by_id(furniture_id)
        if not furniture:
            return False

        await self.session.execute(
            delete(Furniture).where(Furniture.id == furniture_id)
        )
        await self.session.commit()
        return True

    async def get_by_name(self, name: str) -> Optional[Furniture]:
        result = await self.session.execute(
            select(Furniture).where(Furniture.name == name)
        )
        return result.scalar_one_or_none()

    async def get_by_price_range(self, min_price: int, max_price: int) -> List[Furniture]:
        result = await self.session.execute(
            select(Furniture).where(
                Furniture.price >= min_price,
                Furniture.price <= max_price
            )
        )
        return result.scalars().all()
