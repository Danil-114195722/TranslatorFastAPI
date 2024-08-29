from re import match as re_match

from fastapi import FastAPI
from fastapi.responses import JSONResponse
from yaml import safe_load as yaml_safe_load

from database.db import Database
from services import parser
from services.post_models import RussianWord
from settings.settings import BASEDIR


app = FastAPI(redoc_url=None)
db = Database()

with open(f'{BASEDIR}/docs/swagger_docs.yml') as yaml_swagger_docs:
    # Чтение YAML-файла
    custom_openapi = yaml_safe_load(yaml_swagger_docs)
    # Заменяем стандартную OpenAPI схему на свою
    app.openapi = lambda: custom_openapi


@app.get("/")
async def index():
    return {"message": "Hello from TranslatorFastAPI!"}


@app.get("/from-en/{word}")
async def from_en(word: str, transcription: bool = True):
    """
    Получение перевода английского слова на русский \n
    :param word: слово для перевода, указывается в пути. Пример для "dog" - http://127.0.0.1:8000/from-en/dog \n
    :param transcription: получить ли транскрипцию, указывается как параметр, по умолчанию - True. Пример - http://127.0.0.1:8000/from-en/dog?transcription=false \n
    :return: JSON
    """

    # если слово не английское
    if not re_match(r'[a-zA-Z\-,._\"\']', word):
        return JSONResponse(content={"error": "given word is not english"}, status_code=400)

    # ищем перевод в БД
    translation, transcript, error = await db.get_from_eng_vocab(word=word)
    # если перевод не найден
    if error is not None:
        # парсим перевод
        translation, transcript, error = await parser.translate_from_en(word=word)
        if error is not None:
            return JSONResponse(content={"error": error}, status_code=500)

        # добавляем перевод в БД
        _ = await db.add_to_eng_vocab(word=word, translation=translation, transcription=transcript)

    if transcription:
        return {"word": word, "translation": translation, "transcription": transcript}
    else:
        return {"word": word, "translation": translation}


@app.post("/from-ru")
async def from_ru(body: RussianWord):
    """
    Получение перевода русского слова на английский \n
    :param body: слово для перевода, указывается в body. Пример для "кот" - {"word": "кот"} \n
    :return: JSON
    """

    word = body.word
    # если слово не русское
    if not re_match(r'[а-яА-ЯёЁ\-,._\"\']', word):
        return JSONResponse(content={"error": "given word is not russian"}, status_code=400)

    # ищем перевод в БД
    translation, error = await db.get_from_rus_vocab(word=word)
    # если перевод не найден
    if error is not None:
        # парсим перевод
        translation, error = await parser.translate_from_ru(word=word)
        if error is not None:
            return JSONResponse(content={"error": error}, status_code=500)

        # добавляем перевод в БД
        _ = await db.add_to_rus_vocab(word=word, translation=translation)

    return {"word": word, "translation": translation}
