import aiosqlite

from settings.settings import BASEDIR, logger


class Database:
    def __init__(self):
        pass

    async def create_tables(self) -> str | None:
        """
        Создание таблиц
        :return: error/None
        """

        try:
            async with aiosqlite.connect(f"{BASEDIR}/database/sqlite/db.sqlite3") as connection:
                # таблица ru-en
                await connection.execute('''CREATE TABLE IF NOT EXISTS rus_vocab (
                                          id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                                          word VARCHAR(50) NOT NULL UNIQUE,
                                          translation VARCHAR(255) NOT NULL
                                   );''')
                # таблица en-ru
                await connection.execute('''CREATE TABLE IF NOT EXISTS eng_vocab (
                                          id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                                          word VARCHAR(50) NOT NULL UNIQUE,
                                          translation VARCHAR(255) NOT NULL,
                                          transcription VARCHAR(75) NOT NULL
                                   );''')
            return None
        except Exception as err:
            logger.critical(f'Unknown error: {err}')
            return "unknown error"

    async def get_from_rus_vocab(self, word: str) -> tuple[str, str | None]:
        """
        Получение перевода русского слова из таблицы rus_vocab (если есть), если нет - None
        :param word:
        :return: translation and error/None
        """
        try:
            async with aiosqlite.connect(f"{BASEDIR}/database/sqlite/db.sqlite3") as connection:
                async with connection.execute(f"SELECT * FROM rus_vocab WHERE word=\'{word}\';") as cursor:
                    row = await cursor.fetchone()
                    if not row:
                        logger.warning(f'Word {word} not found in "eng_vocab" table')
                        return "", "not found"
                    else:
                        return row[2], None
        except Exception as err:
            logger.critical(f'Unknown error: {err}')
            return "", "unknown error"

    async def get_from_eng_vocab(self, word: str) -> tuple[str, str, str | None]:
        """
        Получение перевода и транскрипции английского слова из таблицы eng_vocab (если есть), если нет - None
        :param word:
        :return: translation, transcription and error/None
        """
        try:
            async with aiosqlite.connect(f"{BASEDIR}/database/sqlite/db.sqlite3") as connection:
                async with connection.execute(f"SELECT * FROM eng_vocab WHERE word=\'{word}\';") as cursor:
                    row = await cursor.fetchone()
                    if not row:
                        logger.warning(f'Word {word} not found in "eng_vocab" table')
                        return "", "", "not found"
                    else:
                        return row[2], row[3], None
        except Exception as err:
            logger.critical(f'Unknown error: {err}')
            return "", "", "unknown error"

    async def add_to_rus_vocab(self, word: str, translation: str) -> str | None:
        """
        Добавление перевода русского слова в таблицу rus_vocab
        :param word:
        :param translation:
        :return: error/None
        """
        try:
            async with aiosqlite.connect(f"{BASEDIR}/database/sqlite/db.sqlite3") as connection:
                await connection.execute(f'''INSERT INTO rus_vocab (word, translation) VALUES (\'{word}\', \'{translation}\');''')
                # если зафиксировано одно изменение, то всё хорошо
                if connection.total_changes == 1:
                    await connection.commit()
                    logger.info(f'Added word "{word}" to "rus_vocab" table')
                    return None
                else:
                    logger.critical('Error while insert new translation to "rus_vocab" table')
                    return "insert error"
        except Exception as err:
            logger.critical(f'Unknown error: {err}')
            return "unknown error"

    async def add_to_eng_vocab(self, word: str, translation: str, transcription: str) -> str | None:
        """
        Добавление перевода и транскрипции английского слова в таблицу eng_vocab
        :param word:
        :param translation:
        :param transcription:
        :return: error/None
        """
        try:
            async with aiosqlite.connect(f"{BASEDIR}/database/sqlite/db.sqlite3") as connection:
                await connection.execute(f'''INSERT INTO eng_vocab (word, translation, transcription) VALUES (\'{word}\', \'{translation}\', \'{transcription}\');''')
                # если зафиксировано одно изменение, то всё хорошо
                if connection.total_changes == 1:
                    await connection.commit()
                    logger.info(f'Added word "{word}" to "eng_vocab" table')
                    return None
                else:
                    logger.critical('Error while insert new translation to "eng_vocab" table')
                    return "insert error"
        except Exception as err:
            logger.critical(f'Unknown error: {err}')
            return "unknown error"


# if __name__ == "__main__":
#     import asyncio
#
#     db = Database()
#     asyncio.run(db.create_tables())
#
#     a = asyncio.run(db.get_from_rus_vocab("яма"))
#     print("a:", a)
