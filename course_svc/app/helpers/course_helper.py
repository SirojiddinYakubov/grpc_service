import logging
from google.protobuf.wrappers_pb2 import BoolValue

class CourseHelper:
    @classmethod
    def check_course(cls, request, context):
        try:
            print(request, context)
            if request.course_id == "b1f3b6e2-a1d5-4932-98d4-616ac8fcb24b":
                return BoolValue(value=True)
            return BoolValue(value=False)
        except Exception as e:
            logging.error(e)
            return



course = CourseHelper()
