# create_tables.py
from sqlalchemy import create_engine
from database.database import Base
from models.models import Client, Order, Product, Transaction

# Синхронний URL (без +asyncpg)
SYNC_DATABASE_URL = "postgresql://postgres:secret@localhost:5432/fastapi_db"

# Створюємо синхронний двигун
engine = create_engine(SYNC_DATABASE_URL, echo=True)

# Створюємо всі таблиці
print("Створюю таблиці...")
Base.metadata.create_all(engine)
print("✅ Таблиці створено!")

# Перевіряємо які таблиці створились
from sqlalchemy import inspect
inspector = inspect(engine)
tables = inspector.get_table_names()
print(f"Таблиці в базі: {tables}")