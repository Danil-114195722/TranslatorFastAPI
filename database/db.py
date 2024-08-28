import aiosqlite

from settings.settings import BASEDIR


class Database:
    def __init__(self):
        pass

    async def create_tables(self):
        """Создание таблиц"""
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
                await connection.close()
        except Exception as err:
            # TODO: добавить логирование ошибки
            print("неизвестная ошибка:", str(err))

    async def get_from_rus_vocab(self, word: str) -> str | None:
        """
        Получение перевода русского слова из таблицы rus_vocab (если есть), если нет - None
        :param word:
        :return: translation or None
        """
        try:
            async with aiosqlite.connect(f"{BASEDIR}/database/sqlite/db.sqlite3") as connection:
                async with connection.execute(f"SELECT * FROM rus_vocab WHERE word=\'{word}\';") as cursor:
                    row = await cursor.fetchone()
                    if not row:
                        return None
                    else:
                        return row[2]
        except Exception as err:
            # TODO: добавить логирование ошибки
            print("неизвестная ошибка:", str(err))
            return None

    async def get_from_eng_vocab(self, word: str) -> tuple[str, str] | None:
        """
        Получение перевода и транскрипции английского слова из таблицы eng_vocab (если есть), если нет - None
        :param word:
        :return: translation or None
        """
        try:
            async with aiosqlite.connect(f"{BASEDIR}/database/sqlite/db.sqlite3") as connection:
                async with connection.execute(f"SELECT * FROM eng_vocab WHERE word=\'{word}\';") as cursor:
                    row = await cursor.fetchone()
                    if not row:
                        return None
                    else:
                        return row[2], row[3]
        except Exception as err:
            # TODO: добавить логирование ошибки
            print("неизвестная ошибка:", str(err))
            return None

    async def add_to_rus_vocab(self, word: str, translation: str) -> bool:
        """
        Добавление перевода русского слова в таблицу rus_vocab
        :param word:
        :param translation:
        :return: result of operation
        """
        try:
            async with aiosqlite.connect(f"{BASEDIR}/database/sqlite/db.sqlite3") as connection:
                await connection.execute(f'''INSERT INTO rus_vocab (word, translation) VALUES (\'{word}\', \'{translation}\');''')
                # если зафиксировано одно изменение, то всё хорошо
                if connection.total_changes == 1:
                    await connection.commit()
                    return True
                else:
                    return False
        except Exception as err:
            # TODO: добавить логирование ошибки
            print("неизвестная ошибка:", str(err))
            return False

    async def add_to_eng_vocab(self, word: str, translation: str, transcription: str) -> bool:
        """
        Добавление перевода и транскрипции английского слова в таблицу eng_vocab
        :param word:
        :param translation:
        :param transcription:
        :return: result of operation
        """
        try:
            async with aiosqlite.connect(f"{BASEDIR}/database/sqlite/db.sqlite3") as connection:
                await connection.execute(f'''INSERT INTO eng_vocab (word, translation, transcription) VALUES (\'{word}\', \'{translation}\', \'{transcription}\');''')
                # если зафиксировано одно изменение, то всё хорошо
                if connection.total_changes == 1:
                    await connection.commit()
                    return True
                else:
                    return False
        except Exception as err:
            # TODO: добавить логирование ошибки
            print("неизвестная ошибка:", str(err))
            return False


# if __name__ == "__main__":
#     import asyncio
#
#     db = Database()
#     asyncio.run(db.create_tables())
#
#     a = asyncio.run(db.get_from_rus_vocab("яма"))
#     print("a:", a)
