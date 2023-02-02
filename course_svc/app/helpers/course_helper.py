import logging
from google.protobuf.wrappers_pb2 import BoolValue

from app.db.session import async_session
from app.models import Locales, CourseTopics
from sqlalchemy.sql.operators import is_
from sqlmodel import select


class CourseHelper:
    @classmethod
    async def check_course(cls, request, context):
        try:
            print(request, context)
            if request.course_id == "b1f3b6e2-a1d5-4932-98d4-616ac8fcb24b":
                return BoolValue(value=True)
            return BoolValue(value=False)
        except Exception as e:
            logging.error(e)
            return

    @classmethod
    async def check_db(cls):
        async with async_session() as db:
            # uz = Locales(name="O'zbek tili", code="uz", is_main=True)
            # ru = Locales(name="Rus tili", code="ru")
            #
            # db.add(uz)
            # db.add(ru)
            # await db.commit()
            #
            # topic_uz = CourseTopics(name="Backend", description="desc", locale_id=uz.id)
            # topic_ru = CourseTopics(name="Бекенд", description="desc", locale_id=ru.id, parent_id=uz.id)
            #
            # db.add(topic_uz)
            # db.add(topic_ru)
            # await db.commit()

            locale_statement = select(Locales.id).where(Locales.code == "uz")
            locale_result = await db.execute(locale_statement)
            locale_id = locale_result.one()[0]

            # query = select(CourseTopics).where(is_(CourseTopics.parent_id, None))
            query = select(CourseTopics).where(CourseTopics.locale_id == locale_id)
            result = await db.execute(query)
            topic = result.all()
            print(topic)


course = CourseHelper()
