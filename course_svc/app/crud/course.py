import logging

from app.db.session import async_session
from sqlalchemy import select

from app.models import CourseTopics


class CourseCRUD:
    @classmethod
    async def get_course_topic_by_id(cls, course_topic_id: int):
        try:
            async with async_session() as db:
                query = select(CourseTopics).where(CourseTopics.id == course_topic_id)
                db_course_topics = await db.execute(query)
                result = db_course_topics.first()
                if not result:
                    return 404, "CourseTopic not found!"
                return 200, result[0]
        except Exception as e:
            logging.error(e)
            return 500, "Internal server error"

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
