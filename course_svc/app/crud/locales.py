import logging

from app.db.session import async_session
from sqlalchemy import select

from app.models import Locales
from .base_crud import CRUDBase


class LocalesCRUD(CRUDBase):
    pass


LocalesCRUD = LocalesCRUD(Locales)
