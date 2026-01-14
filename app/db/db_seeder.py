import asyncio
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy import text, select
from dotenv import load_dotenv
import os

from app.db.base import Base  # ← ВАЖНО: импортируем из app.db.base
from app.models.furniture import Furniture

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")


async def wait_for_db(engine, retries=30, delay=2):
    """Ждем, пока PostgreSQL будет готов принимать подключения"""
    for i in range(retries):
        try:
            async with engine.connect() as conn:
                await conn.execute(text("SELECT 1"))
                await conn.commit()
            print("✅ Database is ready!")
            return True
        except Exception as e:
            print(f"⏳ DB not ready, retry {i + 1}/{retries}...")
            await asyncio.sleep(delay)
    raise Exception("❌ DB connection failed after retries")


async def init_and_seed():
    engine = create_async_engine(DATABASE_URL, echo=True)

    # Ждём, пока Postgres будет готов
    await wait_for_db(engine)

    print("🔨 Creating tables...")

    # 1️⃣ Создаем таблицы В ОДНОЙ ТРАНЗАКЦИИ
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    print("✅ Tables created successfully!")

    # Задержка для надежности
    await asyncio.sleep(1)

    # 2️⃣ Добавляем тестовые данные В НОВОЙ СЕССИИ
    async_session = sessionmaker(
        engine,
        class_=AsyncSession,
        expire_on_commit=False
    )

    async with async_session() as session:
        try:
            # Проверяем, есть ли уже данные
            result = await session.execute(select(Furniture))
            existing = result.scalars().all()

            if not existing:
                items = [
                    Furniture(name="Диван", category="sofa", price=500),
                    Furniture(name="Стул", category="chair", price=200),
                    Furniture(name="Кресло", category="armchair", price=300),
                ]
                session.add_all(items)
                await session.commit()
                print(f"✅ DB seeded with {len(items)} items!")
            else:
                print(f"ℹ️ DB already has {len(existing)} items, skipping seed")

        except Exception as e:
            print(f"❌ Error during seeding: {e}")
            await session.rollback()
            raise

    await engine.dispose()
    print("🎉 Database initialization complete!")


if __name__ == "__main__":
    asyncio.run(init_and_seed())