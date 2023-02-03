import asyncio
import logging
from grpc import aio

from core.config import settings
from grpc_generated_files import courses_pb2_grpc
from helpers import CourseTopicsHelper


class CourseServicer(courses_pb2_grpc.CourseServiceServicer):
    async def CreateCourseTopics(self, request, context):
        print("CourseServicer received request")
        return await CourseTopicsHelper.create_course_topics(request, context)

    async def GetCourseTopics(self, request, context):
        print("CourseServicer received request")
        return await CourseTopicsHelper.get_course_topics(request, context)


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
