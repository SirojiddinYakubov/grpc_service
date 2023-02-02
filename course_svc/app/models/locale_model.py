from sqlmodel import Field

from .base_model import BaseModel


class Locales(BaseModel, table=True):
    name: str
    code: str = Field(unique=True)
    is_main: bool = Field(default=False)
