import pytest

from grpc_generated_files import course_pb2


@pytest.fixture
def course_data(request):
    data = {
        'valid':
            ("b1f3b6e2-a1d5-4932-98d4-616ac8fcb24b", True),
        'invalid':
            ("b1f3b6e2-a1d5-4932-98d4-616ac8fcb242", False),
    }
    return data[request.param]


@pytest.mark.asyncio
@pytest.mark.parametrize('course_data', ['valid', 'invalid'], indirect=True)
async def test_check_course(course_data, mock_context, course_servicer):
    course_id, excepted = course_data
    grpc_request = course_pb2.CheckCourseRequest(course_id=course_id)
    response = await course_servicer.check_course(grpc_request, mock_context)
    assert excepted == response.value
