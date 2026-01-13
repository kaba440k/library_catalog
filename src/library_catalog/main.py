# src/library_catalog/main.py
"""
Точка входа FastAPI приложения Library Catalog.
"""

from fastapi import FastAPI

from src.library_catalog.core.config import settings

# Создать приложение
app = FastAPI(
    title="Library Catalog API",
    description="REST API для управления библиотечным каталогом",
    version="1.0.0",
)


@app.get("/")
async def root():
    """Корневой эндпоинт."""
    return {"message": "Welcome to Library Catalog API"}


@app.get("/health")
async def health_check():
    """Health check эндпоинт."""
    return {"status": "healthy"}


# print("=== Debug settings ===")
# print(f"App name:     {settings.app_name}")
# print(f"Environment:  {settings.environment}")
# print(f"Debug mode:   {settings.debug}")
# print(f"DB URL:       {settings.database_url}")

# Для запуска через python -m
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)