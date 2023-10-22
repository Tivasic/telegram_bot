from typing import Optional

from pydantic import BaseModel


class User(BaseModel):
    id: Optional[int]
    mention: Optional[str]
    first_name: str = ''
    last_name: str = ''
    language_code: str = 'ru'
