import logging

from app.crud.course_topics import CourseTopicsCRUD
from app.db.session import async_session
from app.grpc_generated_files.locales_types_pb2 import (
    Locales
)
from app.grpc_generated_files.courses_types_pb2 import (
    CourseTopicsShort,
    CourseTopics,
    CourseTopicsResponse,
    ListCourseTopicsResponse
)

from .base_helper import BaseHelper
from crud.locales import LocalesCRUD


class CourseTopicsHelper(BaseHelper):

    @classmethod
    async def list_course_topics(cls, request, context):
        try:
            status_code, course_topics_or_error = await CourseTopicsCRUD.get_multi()
            if not status_code == 200:
                raise Exception(status_code, course_topics_or_error)
            list_resp = []
            for course_topic in course_topics_or_error:
                print(course_topic)
                if course_topic.locale_id:
                    status_code, locale_or_error = await LocalesCRUD.get(id=course_topic.locale_id)
                    if not status_code == 200:
                        raise Exception(status_code, locale_or_error)

                    locales_resp = await cls.make_response(Locales, locale_or_error,
                                                           ['id', 'name', 'code', 'is_main'])
                else:
                    locales_resp = None

                if course_topic.parent_id:
                    status_code, course_topic_parent_or_error = await CourseTopicsCRUD.get(id=course_topic.parent_id)
                    if not status_code == 200:
                        raise Exception(status_code, "parent_id not found!")

                    course_topic_short_resp = cls.make_response(CourseTopicsShort, course_topic_parent_or_error,
                                                                ['id', 'name'])
                else:
                    course_topic_short_resp = None

                list_resp.append(cls.make_response(
                    CourseTopics, course_topic, ['id', 'name', 'description', 'sort', 'is_active'],
                    {
                        "parent": course_topic_short_resp, "locale": locales_resp,
                        "created_at": cls.convert_to_timestamp(course_topic.created_at)
                    }))

            list_course_topics_resp = ListCourseTopicsResponse(
                success_payload=list_resp,
                status_code=status_code
            )
            return list_course_topics_resp
        except Exception as e:
            return cls.make_error_response(CourseTopicsResponse, e)

    @classmethod
    async def get_course_topics(cls, request, context):
        try:
            status_code, course_topic_or_error = await CourseTopicsCRUD.get(id=request.course_topic_id)
            if not status_code == 200:
                raise Exception(status_code, course_topic_or_error)

            if course_topic_or_error.parent_id:
                status_code, course_topic_parent_or_error = await CourseTopicsCRUD.get(
                    id=course_topic_or_error.parent_id)
                if not status_code == 200:
                    raise Exception(status_code, course_topic_parent_or_error)

                course_topic_short_resp = cls.make_response(CourseTopicsShort, course_topic_parent_or_error,
                                                                  ['id', 'name'])
            else:
                course_topic_short_resp = None

            if course_topic_or_error.locale_id:
                status_code, result_or_error = await LocalesCRUD.get(id=course_topic_or_error.locale_id)
                if not status_code == 200:
                    raise Exception(status_code, result_or_error)

                locales_resp = cls.make_response(Locales, result_or_error,
                                                       ['id', 'name', 'code', 'is_main'])
            else:
                locales_resp = None

            course_topic_resp = cls.make_response(
                CourseTopics, course_topic_or_error, ['id', 'name', 'description', 'sort', 'is_active'],
                {
                    "parent": course_topic_short_resp, "locale": locales_resp,
                    "created_at": cls.convert_to_timestamp(course_topic_or_error.created_at)
                })

            get_course_topic_resp = CourseTopicsResponse(
                success_payload=course_topic_resp,
                status_code=status_code
            )
            return get_course_topic_resp
        except Exception as e:
            return cls.make_error_response(CourseTopicsResponse, e)

    @classmethod
    async def create_course_topics(cls, request, context):
        try:
            if request.locale_id:
                status_code, locale_or_error = await LocalesCRUD.get(id=request.locale_id)
                if not status_code == 200:
                    raise Exception(status_code, locale_or_error)

                locales_resp = await cls.make_response(Locales, locale_or_error,
                                                       ['id', 'name', 'code', 'is_main'])
            else:
                locales_resp = None

            if request.parent_id:
                status_code, course_topic_parent_or_error = await CourseTopicsCRUD.get(id=request.parent_id)
                if not status_code == 200:
                    raise Exception(status_code, "parent_id not found!")

                course_topic_short_resp = cls.make_response(CourseTopicsShort, course_topic_parent_or_error,
                                                                  ['id', 'name'])
            else:
                course_topic_short_resp = None

            status_code, course_topic_or_error = await CourseTopicsCRUD.create_course_topic(
                name=request.name,
                description=request.description,
                parent_id=request.parent_id if request.parent_id else None,
                locale_id=request.locale_id if request.locale_id else None,
            )
            if not status_code == 200:
                raise Exception(status_code, course_topic_or_error)

            course_topic_resp = cls.make_response(
                CourseTopics, course_topic_or_error, ['id', 'name', 'description', 'sort', 'is_active'],
                {
                    "parent": course_topic_short_resp, "locale": locales_resp,
                    "created_at": cls.convert_to_timestamp(course_topic_or_error.created_at)
                })

            create_course_topic_resp = CourseTopicsResponse(
                success_payload=course_topic_resp,
                status_code=status_code
            )
            return create_course_topic_resp
        except Exception as e:
            return cls.make_error_response(CourseTopicsResponse, e)

    @classmethod
    async def check_db(cls):
        async with async_session() as db:
            pass
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

            # locale_statement = select(Locales).where(Locales.code == "uz")
            # locale_result = await db.execute(locale_statement)
            # locale = locale_result.one()[0]
            # await db.delete(locale)
            # await db.commit()
            # # query = select(CourseTopics).where(is_(CourseTopics.parent_id, None))
            # query = select(CourseTopics).where(CourseTopics.locale_id == locale_id)
            # result = await db.execute(query)
            # topic = result.all()
            # print(topic)

            # role = Roles(role_name="moderator", display_name="Moderator")
            # permission = Permissions(permission_name="edit_course", display_name="Edit Course")
            #
            # role_permission = RolePermissions(role_id=role.id, permission_id=permission.id)
            #
            # user = Users(email="yakubov9791999@gmail.com")
            #
            # user_roles = UserRoles(user_id=user.id, role_id=role.id)
            #
            # db.add(role)
            # db.add(permission)
            # db.add(role_permission)
            # db.add(user)
            # db.add(user_roles)
            # await db.commit()
