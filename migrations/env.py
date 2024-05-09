import asyncio
from logging.config import fileConfig

from alembic import context
from sqlalchemy import engine_from_config
from sqlalchemy import pool
from sqlalchemy.ext.asyncio import AsyncEngine

from src.bets.infrastructure.database import Base
from src.bets.infrastructure.database import DatabaseConfiguration


config = context.config

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = Base.metadata

db_config = DatabaseConfiguration.from_env()
config.set_main_option(
    name='sqlalchemy.url',
    value=db_config.dsn,
)


def do_run_migrations(connection):
    context.configure(connection=connection,
                      target_metadata=target_metadata)

    with context.begin_transaction():
        context.run_migrations()


async def run_migrations_online():
    """
    Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    connectable = AsyncEngine(
        engine_from_config(
            config.get_section(config.config_ini_section),
            prefix='sqlalchemy.',
            poolclass=pool.NullPool,
            future=True,
        ),
    )

    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)

    await connectable.dispose()


asyncio.run(run_migrations_online())
