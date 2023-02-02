import logging

from app.crud.course import CourseCRUD
from app.db.session import async_session
from app.grpc_generated_files import course_pb2


# from app.models import Roles, Permissions, RolePermissions, Users, UserRoles


class CourseHelper:
    @classmethod
    async def CreateCourseTopic(cls, request, context):
        try:
            create_data = {
                "name": request.name,
                "description": request.description,
            }
            if request.locale_id != 0:
                create_data.update(locale_id=request.locale_id)

            if request.parent_id != 0:
                status_code, result_or_error = await CourseCRUD.get_course_topic_by_id(request.parent_id)
                if not status_code == 200:
                    raise Exception(status_code, result_or_error)
                parent_course_topic = result_or_error
                create_data.update(parent_id=parent_course_topic.id)

            status_code, result_or_error = await CourseCRUD.create_course_topic(**create_data)
            if not status_code == 200:
                raise Exception(status_code, result_or_error)
            course_topic = result_or_error
            course_topic_resp = course_pb2.CourseTopic(
                name=course_topic.name,
                description=course_topic.description,
                parent_id=course_topic.parent_id,
                locale_id=course_topic.locale_id,
                created_at=int(course_topic.created_at.strftime("%s")),
                is_active=course_topic.is_active
            )

            create_course_topic_resp = course_pb2.CreateCourseTopicResponse(
                success_payload=course_topic_resp,
                status_code=status_code
            )
            return create_course_topic_resp
        except Exception as e:
            logging.error(e)
            if len(e.args) == 2:
                status_code, message = e.args[0], e.args[1]
            else:
                status_code, message = 500, "Internal server error"
            response = course_pb2.CreateCourseTopicResponse(
                error_payload=message,
                status_code=status_code
            )
            return response

    @classmethod
    async def check_db(cls):
        async with async_session() as db:
            pass
            # uz = Locales(name="O'zbek tili", code="uz", is_main=True)
            # ru = Locales(name="Rus tili", code="ru")
            #
            # db.add(uz)
            # db.add(ru)
            # await db.commit()
            #
            # topic_uz = CourseTopics(name="Backend", description="desc", locale_id=uz.id)
            # topic_ru = CourseTopics(name="Бекенд", description="desc", locale_id=ru.id, parent_id=uz.id)
            #
            # db.add(topic_uz)
            # db.add(topic_ru)
            # await db.commit()

            # locale_statement = select(Locales).where(Locales.code == "uz")
            # locale_result = await db.execute(locale_statement)
            # locale = locale_result.one()[0]
            # await db.delete(locale)
            # await db.commit()
            # # query = select(CourseTopics).where(is_(CourseTopics.parent_id, None))
            # query = select(CourseTopics).where(CourseTopics.locale_id == locale_id)
            # result = await db.execute(query)
            # topic = result.all()
            # print(topic)

            # role = Roles(role_name="moderator", display_name="Moderator")
            # permission = Permissions(permission_name="edit_course", display_name="Edit Course")
            #
            # role_permission = RolePermissions(role_id=role.id, permission_id=permission.id)
            #
            # user = Users(email="yakubov9791999@gmail.com")
            #
            # user_roles = UserRoles(user_id=user.id, role_id=role.id)
            #
            # db.add(role)
            # db.add(permission)
            # db.add(role_permission)
            # db.add(user)
            # db.add(user_roles)
            # await db.commit()


course = CourseHelper()
