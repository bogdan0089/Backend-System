from logging.config import fileConfig
from sqlalchemy import engine_from_config, create_engine
from sqlalchemy import pool
from alembic import context
import sys
from pathlib import Path 
from database.database import Base



sys.path.append(str(Path(__file__).parent.parent))



print("="*50)
print("ДІАГНОСТИКА:")
print(f"Base.metadata.tables.keys(): {list(Base.metadata.tables.keys())}")
print(f"Кількість таблиць: {len(Base.metadata.tables)}")
print("="*50)

target_metadata = Base.metadata

config = context.config

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

def run_migrations_offline() -> None:

    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
        
        url = config.get_main_option("sqlalchemy.url")
        if url and "+asyncpg" in url:
            url = url.replace("+asyncpg", "")
        connectable = create_engine(url, poolclass=pool.NullPool)




    

        with connectable.connect() as connection:
            context.configure(
                connection=connection, target_metadata=target_metadata, compare_type=True, include_schemas=True
            )

            with context.begin_transaction():
                context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
