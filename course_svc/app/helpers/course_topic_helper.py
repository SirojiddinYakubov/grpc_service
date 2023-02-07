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
    async def get_course_topic(cls, context, course_topic_id):
        try:
            course_topic = await CourseTopicsCRUD.get(context, obj_id=course_topic_id)

            if course_topic.parent_id:
                parent = await CourseTopicsCRUD.get(context, obj_id=course_topic.parent_id)
                parent_resp = CourseTopicShort(id=parent.id, name=parent.name)
            else:
                parent_resp = None

            if course_topic.locale_id:
                locale_obj = await LocalesCRUD.get(context, obj_id=course_topic.locale_id)
                locale_resp = Locale(id=locale_obj.id, name=locale_obj.name,
                                     code=locale_obj.code, is_main=locale_obj.is_main)
            else:
                locale_resp = None

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
    async def create_course_topic(cls, context, validated_data):
        try:
            if validated_data.parent_id:
                parent = await CourseTopicsCRUD.get(context, obj_id=validated_data.parent_id)
                parent_resp = CourseTopicShort(id=parent.id, name=parent.name)
            else:
                parent_resp = None

            if validated_data.locale_id:
                locale_obj = await LocalesCRUD.get(context, obj_id=validated_data.locale_id)
                locale_resp = Locale(id=locale_obj.id, name=locale_obj.name,
                                     code=locale_obj.code, is_main=locale_obj.is_main)
            else:
                locale_resp = None

            course_topic = await CourseTopicsCRUD.create(
                context,
                name=validated_data.name,
                description=validated_data.description,
                parent_id=validated_data.parent_id if validated_data.parent_id else None,
                locale_id=validated_data.locale_id if validated_data.locale_id else None,
            )

            course_topic_resp = CourseTopic(
                id=course_topic.id, name=course_topic.name, description=course_topic.description,
                parent=parent_resp, locale=locale_resp,
                sort=course_topic.sort, created_at=Timestamp(seconds=int(course_topic.created_at.timestamp()))
            )
            return course_topic_resp
        except Exception as e:
            logging.error(e)
            raise await context.abort(grpc.StatusCode.INTERNAL, "Internal server error")

    @classmethod
    async def update_course_topic(cls, request, context):
        try:

            obj_data = {
                "name": request.name if request.name else None,
                "description": request.description if request.description else None,
                "sort": request.sort if request.sort else None,
            }
            if hasattr(request, "is_active"):
                obj_data.update(is_active=request.is_active)

            if request.locale_id:
                obj_data.update(locale_id=request.locale_id)

            if request.parent_id:
                obj_data.update(parent_id=request.parent_id)

            status_code, course_topic_or_error = await CourseTopicsCRUD.update(obj_id=request.id, **obj_data)
            if not status_code == 200:
                raise Exception(status_code, course_topic_or_error)

            if request.locale_id:
                status_code, locale_or_error = await LocalesCRUD.get(obj_id=request.locale_id)
                if not status_code == 200:
                    raise Exception(status_code, locale_or_error)

                locales_resp = await cls.make_response(Locales, locale_or_error,
                                                       ['id', 'name', 'code', 'is_main'])
            else:
                locales_resp = None

            if request.parent_id:
                status_code, course_topic_parent_or_error = await CourseTopicsCRUD.get(obj_id=request.parent_id)
                if not status_code == 200:
                    raise Exception(status_code, "parent_id not found!")

                course_topic_short_resp = cls.make_response(CourseTopicsShort, course_topic_parent_or_error,
                                                            ['id', 'name'])
            else:
                course_topic_short_resp = None

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
