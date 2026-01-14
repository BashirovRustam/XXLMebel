from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker



DATABASE_URL = "sqlite+aiosqlite:///./test.db"
# 1️⃣ Base для всех моделей
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
