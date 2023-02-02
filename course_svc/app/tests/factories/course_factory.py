import pytest
from app.models import Locales, CourseTopics

from .base_factory import AsyncSQLAlchemyFactory


@pytest.fixture
def course_topic_factory(async_session):
    class CourseTopicFactory(AsyncSQLAlchemyFactory):
        class Meta:
            model = CourseTopics
            sqlalchemy_session = async_session
            # sqlalchemy_session_persistence = factory.alchemy.SESSION_PERSISTENCE_COMMIT

        name = "Dasturlash"
        description = "This is desc"

    return CourseTopicFactory
