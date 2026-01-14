import os
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from dotenv import load_dotenv



# DATABASE_URL = "sqlite+aiosqlite:///./test.db"

# Загружаем переменные окружения
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")


class Base(DeclarativeBase):
    pass

# 2️⃣ Engine — для async SQLite
engine = create_async_engine(
    DATABASE_URL,
    echo=True,
    future=True
)

# 3️⃣ Session — фабрика сессий
async_session = sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False
)

# 4️⃣ Зависимость для FastAPI
async def get_session() -> AsyncSession:
    async with async_session() as session:
        yield session
