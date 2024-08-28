from pydantic import BaseModel


class RussianWord(BaseModel):
    word: str

