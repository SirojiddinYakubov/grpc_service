import asyncio
import json
import logging

import grpc
from grpc import aio
from pydantic import ValidationError

from core.config import settings
from grpc_generated_files import courses_pb2_grpc
from helpers import CourseTopicsHelper
from google.protobuf import empty_pb2, timestamp_pb2, json_format

from schemas.course_topics import RPCCreateCourseTopicSchema, RPCUpdateCourseTopicSchema, RPCGetCourseTopicSchema


class CourseServicer(courses_pb2_grpc.CourseServiceServicer):
    async def ListCourseTopics(self, request, context):
        print("CourseServicer received request")
        return await CourseTopicsHelper.list_course_topics(context, limit=request.limit, offset=request.offset)

    async def GetCourseTopic(self, request, context):
        print("CourseServicer received request")
        data = json_format.MessageToDict(request, preserving_proto_field_name=True)
        data.update(extra_ctx={'context': context})
        try:
            valid_data = RPCGetCourseTopicSchema(**data)
        except ValidationError as exc:
            raise await context.abort(grpc.StatusCode.INVALID_ARGUMENT, str(exc))
        return await CourseTopicsHelper.get_course_topic(context, valid_data.course_topic_id)

    async def CreateCourseTopic(self, request, context):
        print("CourseServicer received request")
        data = json_format.MessageToDict(request, preserving_proto_field_name=True)
        data.update(extra_ctx={'context': context})
        try:
            validated_data = RPCCreateCourseTopicSchema(**data)
        except ValidationError as exc:
            raise await context.abort(grpc.StatusCode.INVALID_ARGUMENT, str(exc))
        return await CourseTopicsHelper.create_course_topic(context, validated_data)

    async def UpdateCourseTopic(self, request, context):
        print("CourseServicer received request")
        data = json_format.MessageToDict(request, preserving_proto_field_name=True)
        try:
            RPCUpdateCourseTopicSchema(**data)
            return await CourseTopicsHelper.update_course_topic(context, request)
        except ValidationError as exc:
            raise await context.abort(grpc.StatusCode.INVALID_ARGUMENT, str(exc))



async def serve():
    server = aio.server()
    listen_addr = f"[::]:{settings.SVC_PORT}"
    courses_pb2_grpc.add_CourseServiceServicer_to_server(CourseServicer(), server)
    server.add_insecure_port(listen_addr)
    logging.info("Starting server on %s", listen_addr)

    await server.start()

    # await course.check_db()

    await server.wait_for_termination()


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    asyncio.run(serve())
