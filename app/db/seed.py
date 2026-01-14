import asyncio
from app.db.base import Base, engine
# Импортируем модели, чтобы Base их увидел
from app.models.furniture import Furniture
from app.models.order import Order
from app.models.order_item import OrderItem
from app.crud.furniture_crud import FurnitureCRUD
from app.db.base import async_session

# Тестовые товары
FURNITURE_ITEMS = [
    {"name": "Стол", "category": "table", "price": 49900},
    {"name": "Стул", "category": "chair", "price": 29900},
    {"name": "Диван", "category": "sofa", "price": 99900},
]

async def init_db():
    async with engine.begin() as conn:
        # создаёт все таблицы из Base
        await conn.run_sync(Base.metadata.create_all)
    print("Все таблицы созданы!")

async def seed_furniture():
    async with async_session() as session:
        crud = FurnitureCRUD(session)
        for item in FURNITURE_ITEMS:
            existing = await crud.get_by_name(item["name"])
            if not existing:
                await crud.create(
                    name=item["name"],
                    category=item["category"],
                    price=item["price"]
                )
                print(f"Создан товар: {item['name']}")
            else:
                print(f"Товар уже существует: {item['name']}")
    print("Furniture заполнена!")

async def main():
    await init_db()
    await seed_furniture()
    print("База готова!")

if __name__ == "__main__":
    asyncio.run(main())
