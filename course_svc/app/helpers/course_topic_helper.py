import logging

import grpc
from app.crud.course_topics import CourseTopicsCRUD
from app.grpc_generated_files.courses_types_pb2 import (
    CourseTopicShort,
    CourseTopic,
    ListCourseTopicsResponse
)

from google.protobuf.empty_pb2 import (
    Empty
)
from app.grpc_generated_files.locales_types_pb2 import (
    Locale
)

from crud.locales import LocalesCRUD
from .base_helper import BaseHelper


class CourseTopicsHelper(BaseHelper):

    @classmethod
    async def get_parent_or_none(cls, context, obj):
        if not hasattr(obj, 'parent_id') or not getattr(obj, 'parent_id'):
            return None
        parent = await CourseTopicsCRUD.get(context, obj_id=getattr(obj, 'parent_id'))
        return CourseTopicShort(id=parent.id, name=parent.name)

    @classmethod
    async def get_locale_or_none(cls, context, obj):
        if not hasattr(obj, 'locale_id') or not getattr(obj, 'locale_id'):
            return None
        locale_obj = await LocalesCRUD.get(context, obj_id=getattr(obj, 'locale_id'))
        return Locale(id=locale_obj.id, name=locale_obj.name, code=locale_obj.code, is_main=locale_obj.is_main)

    @classmethod
    async def list_course_topics(cls, context, page_number, page_size, order_by, desc):
        try:
            course_topics, pagination = await CourseTopicsCRUD.get_paginated_list(context, page_number=page_number,
                                                                                  page_size=page_size,
                                                                                  order_by=order_by, desc=desc)
            course_topics_resp = [await cls.get_course_topic(context, course_topic.id) for course_topic in
                                  course_topics]
            return ListCourseTopicsResponse(page_number=pagination.page_number, page_size=pagination.page_size,
                                            num_pages=pagination.num_pages, total_results=pagination.total_results,
                                            results=course_topics_resp)
        except Exception as e:
            logging.error(e)
            await context.abort(grpc.StatusCode.INTERNAL, "Internal server error")

    @classmethod
    async def get_course_topic(cls, context, obj_id):
        try:
            course_topic = await CourseTopicsCRUD.get(context, obj_id=int(obj_id))

            locale_resp = await cls.get_locale_or_none(context, obj=course_topic)
            parent_resp = await cls.get_parent_or_none(context, obj=course_topic)

            course_topic_resp = CourseTopic(id=course_topic.id, name=course_topic.name,
                                            description=course_topic.description, parent=parent_resp,
                                            locale=locale_resp, is_active=course_topic.is_active,
                                            sort=course_topic.sort,
                                            created_at=cls.get_timestamp_or_none(course_topic, 'created_at'),
                                            updated_at=cls.get_timestamp_or_none(course_topic, 'updated_at')
                                            )
            return course_topic_resp
        except Exception as e:
            logging.error(e)
            await context.abort(grpc.StatusCode.INTERNAL, "Internal server error")

    @classmethod
    async def create_course_topic(cls, context, valid_data):
        try:
            parent_resp = await cls.get_async_attr_or_none(valid_data, 'parent')
            locale_resp = await cls.get_async_attr_or_none(valid_data, 'locale')

            course_topic = await CourseTopicsCRUD.create(context, name=valid_data.name,
                                                         description=valid_data.description,
                                                         parent_id=getattr(parent_resp, 'id', None),
                                                         locale_id=getattr(locale_resp, 'id', None),
                                                         )

            course_topic_resp = CourseTopic(id=course_topic.id, name=course_topic.name,
                                            description=course_topic.description, parent=parent_resp,
                                            locale=locale_resp, sort=course_topic.sort,
                                            created_at=cls.get_timestamp_or_none(course_topic, 'created_at')
                                            )
            return course_topic_resp
        except Exception as e:
            logging.error(e)
            await context.abort(grpc.StatusCode.INTERNAL, "Internal server error")

    @classmethod
    async def update_course_topic(cls, context, obj_id, updated_obj, mask):
        try:
            original_obj = await CourseTopicsCRUD.get(context, obj_id=int(obj_id))
            mask.MergeMessage(updated_obj, original_obj)
            course_topic = await CourseTopicsCRUD.update(context, original_obj)

            parent_resp = await cls.get_parent_or_none(context, obj=course_topic)
            locale_resp = await cls.get_locale_or_none(context, obj=course_topic)

            course_topic_resp = CourseTopic(id=course_topic.id, name=course_topic.name,
                                            description=course_topic.description,
                                            parent=parent_resp, locale=locale_resp,
                                            sort=course_topic.sort, is_active=course_topic.is_active,
                                            created_at=cls.get_timestamp_or_none(course_topic, 'created_at'),
                                            updated_at=cls.get_timestamp_or_none(course_topic, 'updated_at'))
            return course_topic_resp
        except Exception as e:
            logging.error(e)
            await context.abort(grpc.StatusCode.INTERNAL, "Internal server error")

    @classmethod
    async def delete_course_topic(cls, context, obj_id):
        try:
            obj = await CourseTopicsCRUD.get(context, obj_id=int(obj_id))
            await CourseTopicsCRUD.delete(context, obj_id=obj.id)
            return Empty()
        except Exception as e:
            logging.error(e)
            await context.abort(grpc.StatusCode.INTERNAL, "Internal server error")
