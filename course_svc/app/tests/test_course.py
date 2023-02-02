import pytest

from grpc_generated_files import course_pb2

from app.models import Locales


@pytest.fixture
async def create_course_topic_data(request, locale_factory, course_topic_factory):
    locale_obj = await locale_factory.create()
    course_topic = await course_topic_factory.create(locale_id=locale_obj.id)
    data = {
        'valid':
            (200, "Dasturlash", "This is desc", course_topic.id, None),
        # 'invalid':
        #     (400, None, "This is desc", None, None),
    }
    return data[request.param]


@pytest.mark.asyncio
@pytest.mark.parametrize('create_course_topic_data', ['valid'], indirect=True)
async def test_create_course_topic(create_course_topic_data, mock_context, course_servicer):
    status_code, name, description, parent_id, locale_id = create_course_topic_data
    grpc_request = course_pb2.CreateCourseTopicRequest(
        name=name,
        description=description,
        parent_id=parent_id,
        locale_id=locale_id
    )

    response = await course_servicer.CreateCourseTopic(grpc_request, mock_context)
    assert status_code == response.status_code
