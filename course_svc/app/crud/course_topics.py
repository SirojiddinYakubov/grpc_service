import logging

from app.db.session import async_session
from app.models import CourseTopics
from crud.base_crud import CRUDBase


class CoursesCRUD(CRUDBase):
    @classmethod
    async def create_course_topic(cls, **kwargs):
        try:
            async with async_session() as db:
                course_topic = CourseTopics(**kwargs)
                db.add(course_topic)
                await db.commit()
                await db.refresh(course_topic)
                return 200, course_topic
        except Exception as e:
            logging.error(e)
            return 500, "Internal server error"


CourseTopicsCRUD = CoursesCRUD(CourseTopics)
