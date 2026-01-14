from fastapi import FastAPI
from app.api.furniture import router as furniture_router  # импортируем router
from app.api.orders import router as orders_router  # импортируем router

app = FastAPI(title="Furniture API")

# Подключаем router
app.include_router(furniture_router)
app.include_router(orders_router)

@app.get("/health")
async def health_check():
    return {"status": "ok"}


