from aiohttp import ClientSession as AioClientSession
from aiohttp.client_exceptions import ClientConnectorError

from bs4 import BeautifulSoup
from fake_useragent import UserAgent


SITE_URL = 'https://wooordhunt.ru/word/'


async def translate_from_ru(word: str) -> str:
    """
    Перевод с русского
    :param word: russian word to translate
    :return: translated word in english
    """

    # применение user_agent
    user_agent = UserAgent()
    headers = {
        'User-Agent': user_agent.random
    }

    try:
        async with AioClientSession() as session:
            async with session.get(SITE_URL + word, headers=headers, timeout=3) as response:
                # берём html из запроса
                html = await response.text()
    except ClientConnectorError:
        # TODO: добавить логирование ошибки
        print("ошибка соединения")
        return ""

    soup = BeautifulSoup(html, 'html.parser')
    try:
        # парсинг перевода
        translation = soup.find('p', {'class': 't_inline'}).get_text().strip()
    except AttributeError:
        # TODO: добавить логирование ошибки
        print("слово не найдено")
        return ""

    # возвращаем полученный перевод
    return translation


async def translate_from_en(word: str) -> (str, str):
    """
    Перевод с английского
    :param word: english word to translate
    :return: translated word in russian and english transcription
    """

    # применение user_agent
    user_agent = UserAgent()
    headers = {
        'User-Agent': user_agent.random
    }

    try:
        async with AioClientSession() as session:
            async with session.get(SITE_URL + word, headers=headers, timeout=3) as response:
                # берём html из запроса
                html = await response.text()
    except ClientConnectorError:
        # TODO: добавить логирование ошибки
        print("ошибка соединения")
        return "", ""

    soup = BeautifulSoup(html, 'html.parser')
    try:
        # парсинг перевода и транскрипции
        translation = soup.find('div', {'class': 't_inline_en'}).get_text().strip()
        transcription = soup.find('div', {'id': 'uk_tr_sound'}).find('span', {'class': 'transcription'}).get_text().strip()
    except AttributeError:
        # TODO: добавить логирование ошибки
        print("слово не найдено")
        return "", ""

    # возвращаем полученный перевод и транскрипцию
    return translation, transcription


# if __name__ == '__main__':
#     import asyncio
#
#     print("Перевод слова ru-en:", asyncio.run(
#         translate_from_ru("рука")
#     ))
#
#     print("Перевод слова en-ru:", asyncio.run(
#         translate_from_en("garden")
#     ))
