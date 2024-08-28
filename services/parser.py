from aiohttp import ClientSession as AioClientSession
from aiohttp.client_exceptions import ClientConnectorError

from bs4 import BeautifulSoup
from fake_useragent import UserAgent

from settings.settings import logger


SITE_URL = 'https://wooordhunt.ru/word/'


async def translate_from_ru(word: str) -> tuple[str, str | None]:
    """
    Перевод с русского
    :param word: russian word to translate
    :return: translated word in english and error/None
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
    except ClientConnectorError as err:
        logger.critical(f'Client connector error: {err}')
        return "", "client connector error"

    soup = BeautifulSoup(html, 'html.parser')
    try:
        # парсинг перевода
        translation = soup.find('p', {'class': 't_inline'}).get_text().strip()
    except AttributeError as err:
        logger.warning(f'Translation not found: {err}')
        return "", "translation not found"

    # возвращаем полученный перевод
    return translation, None


async def translate_from_en(word: str) -> tuple[str, str, str | None]:
    """
    Перевод с английского
    :param word: english word to translate
    :return: translated word in russian, english transcription and error/None
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
    except ClientConnectorError as err:
        logger.critical(f'Client connector error: {err}')
        return "", "", "connector error"

    soup = BeautifulSoup(html, 'html.parser')
    try:
        # парсинг перевода и транскрипции
        translation = soup.find('div', {'class': 't_inline_en'}).get_text().strip()
        transcription = soup.find('div', {'id': 'uk_tr_sound'}).find('span', {'class': 'transcription'}).get_text().strip()
    except AttributeError as err:
        logger.warning(f'Translation not found: {err}')
        return "", "", "translation not found"

    # возвращаем полученный перевод и транскрипцию
    return translation, transcription, None


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
