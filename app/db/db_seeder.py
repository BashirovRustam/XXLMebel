import asyncio
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os

from app.models.base import Base
from app.models.furniture import Furniture

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")


async def seed():
    engine = create_async_engine(DATABASE_URL, echo=True, future=True)
    async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

    async with async_session() as session:
        # Пример тестовых данных
        items = [
            Furniture(name="Диван", category="sofa", price=500),
            Furniture(name="Стул", category="chair", price=200),
            Furniture(name="Кресло", category="armchair", price=300),
        ]
        session.add_all(items)
        await session.commit()
        print("✅ DB seeded successfully!")

    await engine.dispose()


if __name__ == "__main__":
    asyncio.run(seed())
