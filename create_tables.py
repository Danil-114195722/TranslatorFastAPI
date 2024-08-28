"""Создание нужных таблиц в БД"""


import asyncio
from database.db import Database
from settings.settings import logger


async def main() -> None:
    logger.info(f'Start creating SQLite tables')
    print("Creating SQLite tables...")

    db = Database()
    err = await db.create_tables()

    if err is None:
        logger.info(f'SQLite tables was created successfully')
        print("SQLite tables was created successfully!")


asyncio.run(main())
