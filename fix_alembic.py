# fix_alembic.py
# from sqlalchemy import create_engine, text

# DATABASE_URL = "postgresql://postgres:secret@localhost:5432/fastapi_db"

# engine = create_engine(DATABASE_URL)
# with engine.connect() as conn:
#     conn.execute(text("DROP TABLE IF EXISTS alembic_version;"))
#     conn.commit()
#     print("✅ Готово!")