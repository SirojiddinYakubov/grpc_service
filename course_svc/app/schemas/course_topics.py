import asyncio
import concurrent
from concurrent import futures
from typing import Optional, Any, Union

from pydantic import BaseModel, validator, Field

import inspect

from crud.course_topics import CourseTopicsCRUD
from crud.locales import LocalesCRUD
from app.grpc_generated_files.locales_types_pb2 import (
    Locale
)
from app.grpc_generated_files.courses_types_pb2 import (
    CourseTopicShort
)
from google.protobuf.field_mask_pb2 import (
    FieldMask
)


class BaseSchema(BaseModel):
    extra_ctx: Optional[dict]

    @classmethod
    def get_context(cls, values: dict):
        extra_ctx = values.get('extra_ctx', None)
        if extra_ctx:
            return extra_ctx.get('context', None)
        return None


def optional(*fields):
    def dec(_cls):
        for field in fields:
            _cls.__fields__[field].required = False
        return _cls

    if fields and inspect.isclass(fields[0]) and issubclass(fields[0], BaseModel):
        cls = fields[0]
        fields = cls.__fields__
        return dec(cls)
    return dec


class RPCGetCourseTopicSchema(BaseSchema):
    course_topic_id: Union[str, int]


class RPCCreateCourseTopicSchema(BaseSchema):
    name: str
    description: Optional[str]
    parent: Optional[str] = Field(alias="parent_id")
    locale: int = Field(alias="locale_id")
    sort: Optional[int]

    @validator('locale')
    def check_locale(cls, v, values):
        context = cls.get_context(values)

        async def get_locale(locale_id):
            locale_obj = await LocalesCRUD.get(context, obj_id=locale_id)
            return Locale(id=locale_obj.id, name=locale_obj.name,
                          code=locale_obj.code, is_main=locale_obj.is_main)

        return get_locale(v)

    @validator('parent')
    def check_parent(cls, v, values):
        context = cls.get_context(values)

        async def get_parent(parent_id):
            parent = await CourseTopicsCRUD.get(context, obj_id=int(parent_id))
            return CourseTopicShort(id=parent.id, name=parent.name)

        return get_parent(v)


class RPCUpdateCourseTopicSchema(BaseSchema):
    course_topic_id: Union[str, int]
    course_topic: dict
    mask: str
