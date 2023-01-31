import asyncio
import logging
from grpc import aio

from app.helpers import course
from core.config import settings
from grpc_generated_files import course_pb2, course_pb2_grpc


class CourseServicer(course_pb2_grpc.CourseServiceServicer):
    async def check_course(self, request, context):
        print("CourseServicer received request")
        return course.check_course(request, context)


async def serve():
    server = aio.server()
    listen_addr = f"[::]:{settings.SVC_PORT}"
    course_pb2_grpc.add_CourseServiceServicer_to_server(CourseServicer(), server)
    server.add_insecure_port(listen_addr)
    logging.info("Starting server on %s", listen_addr)

    await server.start()
    await server.wait_for_termination()


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    asyncio.run(serve())
