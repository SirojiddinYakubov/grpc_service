import pytest
from app.models import Locales

from .base_factory import AsyncSQLAlchemyFactory


@pytest.fixture
def locale_factory(async_session):
    class LocaleFactory(AsyncSQLAlchemyFactory):
        class Meta:
            model = Locales
            sqlalchemy_session = async_session
            # sqlalchemy_session_persistence = factory.alchemy.SESSION_PERSISTENCE_COMMIT

        name = "O'zbek tili"
        code = "uz"

    return LocaleFactory
