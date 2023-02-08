import logging

import grpc
from google.protobuf import empty_pb2, timestamp_pb2, json_format
from app.crud.course_topics import CourseTopicsCRUD
from app.grpc_generated_files.courses_types_pb2 import (
    CourseTopicShort,
    CourseTopic,
    ListCourseTopicsResponse
)
from google.protobuf.timestamp_pb2 import (
    Timestamp
)
from app.grpc_generated_files.locales_types_pb2 import (
    Locale
)

from crud.locales import LocalesCRUD
from .base_helper import BaseHelper


class CourseTopicsHelper(BaseHelper):

    @classmethod
    async def get_parent_by_id(cls, context, parent_id):
        parent = await CourseTopicsCRUD.get(context, obj_id=parent_id)
        return CourseTopicShort(id=parent.id, name=parent.name)

    @classmethod
    async def get_locale_by_id(cls, context, locale_id):
        locale_obj = await LocalesCRUD.get(context, obj_id=locale_id)
        return Locale(id=locale_obj.id, name=locale_obj.name, code=locale_obj.code, is_main=locale_obj.is_main)

    @classmethod
    async def list_course_topics(cls, context, limit, offset):
        try:
            course_topics = await CourseTopicsCRUD.get_multi(context, limit=limit, offset=offset)
            course_topics_resp = [await cls.get_course_topic(context, course_topic.id) for course_topic in
                                  course_topics]
            return ListCourseTopicsResponse(course_topics=course_topics_resp)
        except Exception as e:
            logging.error(e)
            await context.abort(grpc.StatusCode.INTERNAL, "Internal server error")

    @classmethod
    async def get_course_topic(cls, context, obj_id):
        try:
            course_topic = await CourseTopicsCRUD.get(context, obj_id=int(obj_id))

            parent_resp = await cls.get_parent_by_id(context, parent_id=getattr(course_topic, 'parent_id')) if getattr(
                course_topic, 'parent_id') else None

            locale_resp = await cls.get_locale_by_id(context, locale_id=getattr(course_topic, 'locale_id')) if getattr(
                course_topic, 'locale_id') else None

            course_topic_resp = CourseTopic(
                id=course_topic.id, name=course_topic.name, description=course_topic.description,
                parent=parent_resp, locale=locale_resp,
                sort=course_topic.sort, created_at=Timestamp(seconds=int(course_topic.created_at.timestamp()))
            )
            return course_topic_resp
        except Exception as e:
            logging.error(e)
            await context.abort(grpc.StatusCode.INTERNAL, "Internal server error")

    @classmethod
    async def create_course_topic(cls, context, valid_data):
        try:
            parent_resp = await getattr(valid_data, 'parent') if getattr(valid_data, 'parent') else None
            locale_resp = await getattr(valid_data, 'locale') if getattr(valid_data, 'locale') else None

            course_topic = await CourseTopicsCRUD.create(
                context,
                name=valid_data.name, description=valid_data.description,
                parent_id=getattr(parent_resp, 'id', None), locale_id=getattr(locale_resp, 'id', None),
            )

            course_topic_resp = CourseTopic(
                id=course_topic.id, name=course_topic.name, description=course_topic.description,
                parent=parent_resp, locale=locale_resp, sort=course_topic.sort,
                created_at=Timestamp(seconds=int(course_topic.created_at.timestamp()))
            )
            return course_topic_resp
        except Exception as e:
            logging.error(e)
            await context.abort(grpc.StatusCode.INTERNAL, "Internal server error")

    @classmethod
    async def update_course_topic(cls, context, request):
        try:
            obj_id = request.course_topic_id
            mask = request.mask
            updated_obj = request.course_topic
            original_obj = await CourseTopicsCRUD.get(context, obj_id=int(obj_id))
            mask.MergeMessage(updated_obj, original_obj)
            course_topic = await CourseTopicsCRUD.update(context, original_obj)

            parent_resp = await cls.get_parent_by_id(context, parent_id=getattr(course_topic, 'parent_id')) if getattr(
                course_topic, 'parent_id') else None

            locale_resp = await cls.get_locale_by_id(context, locale_id=getattr(course_topic, 'locale_id')) if getattr(
                course_topic, 'locale_id') else None

            course_topic_resp = CourseTopic(
                id=course_topic.id, name=course_topic.name, description=course_topic.description,
                parent=parent_resp, locale=locale_resp,
                sort=course_topic.sort,
                created_at=Timestamp(seconds=int(course_topic.created_at.timestamp()))
            )
            return course_topic_resp
        except Exception as e:
            logging.error(e)
            await context.abort(grpc.StatusCode.INTERNAL, "Internal server error")
