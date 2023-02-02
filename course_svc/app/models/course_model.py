from typing import Optional
from uuid import UUID

from sqlmodel import Field

from .base_model import BaseModel


class BaseCourseModel(BaseModel):
    name: str
    description: str
    is_active: bool = Field(default=True)
    sort: Optional[int] = Field(default=1)


class Locales(BaseModel, table=True):
    name: str
    code: str = Field(unique=True)
    is_main: bool = Field(default=False)


class CourseTopics(BaseCourseModel, table=True):
    parent_id: int = Field(default=None, foreign_key="CourseTopics.id")
    locale_id: int = Field(default=None, foreign_key="Locales.id")


class CourseCategories(BaseCourseModel, table=True):
    main_course_topic_id: int = Field(default=None, foreign_key="CourseTopics.id")
    icon_id: UUID = Field(default=None, foreign_key="ImageMedia.id")
    parent_id: int = Field(default=None, foreign_key="CourseTopics.id")
    locale_id: int = Field(default=None, foreign_key="Locales.id")


class Courses(BaseCourseModel, table=True):
    parent_id: int = Field(default=None, foreign_key="CourseTopics.id")
    locale_id: int = Field(default=None, foreign_key="Locales.id")
    photo_id: Optional[UUID] = Field(default=None, foreign_key="ImageMedia.id")
    trailer_id: Optional[UUID] = Field(default=None, foreign_key="FileMedia.id")
    author_id: Optional[int]
    mentor_id: Optional[int]


class CategoriesCourses(BaseModel, table=True):
    category_id: int = Field(default=None, foreign_key="CourseCategories.id")
    course_id: int = Field(default=None, foreign_key="Courses.id")


class CoursePrices(BaseModel, table=True):
    course_id: int = Field(default=None, foreign_key="Courses.id")
    price: Optional[float]
    percent: Optional[float]
    percent_price: Optional[float]
    author_id: Optional[int]


class UserCoursePurchases(BaseModel, table=True):
    user_id: int
    course_id: int = Field(default=None, foreign_key="Courses.id")
    course_price_id: int = Field(default=None, foreign_key="CoursePrices.id")
    paid_percent: Optional[float]

# class CourseCategory(BaseCourseModel, table=True):
#     course_topic_id: UUID = Field(default=None, foreign_key="CourseTopic.id")
#     course_topic: CourseTopic = Relationship(
#         sa_relationship_kwargs={
#             "lazy": "selectin",
#             "primaryjoin": "CourseCategory.course_topic_id==CourseTopic.id",
#         }
#     )
#     logo_id: UUID = Field(default=None, foreign_key="ImageMedia.id")
#     logo: Optional[ImageMedia] = Relationship(
#         sa_relationship_kwargs={
#             "lazy": "selectin",
#             "primaryjoin": "Category.logo_id==ImageMedia.id",
#         }
#     )
#
#
# class CourseStatusEnum(int, enum.Enum):
#     public = 0
#     private = 1
#     premiere = 2
#
#
# class DifficultyLevelEnum(int, enum.Enum):
#     beginner = 0
#     intermediate = 1
#     expert = 2
#
#
# class LanguageEnum(int, enum.Enum):
#     uzbek = 0
#     russian = 1
#     english = 2
#
#
# class Course(BaseCourseModel, table=True):
#     course_category_id: UUID = Field(default=None, foreign_key="CourseCategory.id")
#     course_category: CourseCategory = Relationship(
#         sa_relationship_kwargs={
#             "lazy": "selectin",
#             "primaryjoin": "Course.course_category_id==CourseCategory.id",
#         }
#     )
#     created_by_id: UUID
#     price: float = Field(default=0)
#     is_free: bool = Field(default=False)
#     banner_image_id: UUID = Field(default=None, foreign_key="ImageMedia.id")
#     banner_image: ImageMedia = Relationship(
#         sa_relationship_kwargs={
#             "lazy": "selectin",
#             "primaryjoin": "Course.banner_image_id==ImageMedia.id"
#         }
#     )
#     organization_id: Optional[UUID]
#     status: CourseStatusEnum = Field(sa_column=Column(Enum(CourseStatusEnum)), default=CourseStatusEnum.private)
#     is_for_child: bool = Field(default=False)
#     is_verified: bool = Field(default=False)
#     level: DifficultyLevelEnum = Field(sa_column=Column(Enum(DifficultyLevelEnum)),
#                                        default=DifficultyLevelEnum.beginner)
#     language: LanguageEnum = Field(sa_column=Column(Enum(LanguageEnum)), default=LanguageEnum.uzbek)
#     # installment_payment_id
#     # discount_id
#     trailer_id: UUID = Field(default=None, foreign_key="FileMedia.id")
#     trailer: Optional[FileMedia] = Relationship(
#         sa_relationship_kwargs={
#             "lazy": "selectin",
#             "primaryjoin": "Course.trailer_id==FileMedia.id",
#         }
#     )
#
#
# class CourseModule(BaseCourseModel, table=True):
#     course_id: UUID = Field(default=None, foreign_key="Course.id")
#     course: Course = Relationship(
#         sa_relationship_kwargs={
#             "lazy": "selectin",
#             "primaryjoin": "CourseModule.course_id==Course.id",
#         }
#     )
#     content: Union[dict, str] = TranslationField()
#     is_free: bool = Field(default=False)
#     price: float = Field(default=0)
#     level: DifficultyLevelEnum = Field(
#         sa_column=Column(postgresql.ENUM(
#             DifficultyLevelEnum,
#             create_type=False,
#             checkfirst=True,
#             inherit_schema=True,
#         )),
#         default=DifficultyLevelEnum.beginner)
#     # discount_id
#
#
# class CourseLesson(BaseCourseModel, table=True):
#     course_module_id: UUID = Field(default=None, foreign_key="CourseModule.id")
#     course_module: CourseModule = Relationship(
#         sa_relationship_kwargs={
#             "lazy": "selectin",
#             "primaryjoin": "CourseLesson.course_module_id==CourseModule.id",
#         }
#     )
#     is_free: bool = Field(default=False)
#     price: float = Field(default=0)
#     video_id: UUID = Field(default=None, foreign_key="FileMedia.id")
#     video: Optional[FileMedia] = Relationship(
#         sa_relationship_kwargs={
#             "lazy": "selectin",
#             "primaryjoin": "CourseLesson.video_id==FileMedia.id",
#         }
#     )
#     content: Union[dict, str] = TranslationField()
#     is_learned: bool = Field(default=False, nullable=False)
#     # discount_id
#
#
# class CourseComment(BaseUUIDModel, table=True):
#     created_by_id: UUID
#     course_id: UUID = Field(default=None, foreign_key="Course.id")
#     course: Course = Relationship(
#         sa_relationship_kwargs={
#             "lazy": "selectin",
#             "primaryjoin": "CourseComment.course_id==Course.id",
#         }
#     )
#     text: Union[dict, str] = TranslationField()
#     replied_by_id: Optional[UUID]
