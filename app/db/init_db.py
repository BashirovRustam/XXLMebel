import asyncio
from sqlalchemy.ext.asyncio import create_async_engine
from app.models.base import Base
from dotenv import load_dotenv
import os

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

async def init_db():
    engine = create_async_engine(DATABASE_URL, echo=True, future=True)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    await engine.dispose()
    print("✅ Tables created successfully!")

if __name__ == "__main__":
    asyncio.run(init_db())
