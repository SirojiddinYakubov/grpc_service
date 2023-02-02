from sqlalchemy.orm import relationship

from .media_model import ImageMedia, FileMedia
from .base_model import Base
import sqlalchemy as db


class BaseCourseModel(Base):
    __abstract__ = True

    name = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=True)
    is_active = db.Column(db.Boolean, default=True)
    sort = db.Column(db.Integer, default=1)


class CourseTopics(BaseCourseModel):
    parent_id = db.Column(db.Integer, db.ForeignKey("course_topics.id"))
    # parent = relationship('CourseTopics', remote_side=[id])

    locale_id = db.Column(db.Integer, db.ForeignKey("locales.id"))
    # locale = relationship('Locales', foreign_keys='course_topics.locale_id')


class CourseCategories(BaseCourseModel):
    main_course_topic_id = db.Column(db.Integer, db.ForeignKey("course_topics.id"))
    icon_id = db.Column(db.Integer, db.ForeignKey(ImageMedia.id))

    parent_id = db.Column(db.Integer, db.ForeignKey("course_categories.id"))
    # parent = relationship('CourseCategories', remote_side=[id])

    locale_id = db.Column(db.Integer, db.ForeignKey("locales.id"))
    # locale = relationship('Locales', foreign_keys='course_categories.locale_id')


class Courses(BaseCourseModel):
    parent_id = db.Column(db.Integer, db.ForeignKey("courses.id"))
    locale_id = db.Column(db.Integer, db.ForeignKey("locales.id"))
    photo_id = db.Column(db.Integer, db.ForeignKey(ImageMedia.id))
    trailer_id = db.Column(db.Integer, db.ForeignKey(FileMedia.id))
    author_id = db.Column(db.Integer)
    mentor_id = db.Column(db.Integer)


class CategoriesCourses(Base):
    category_id = db.Column(db.Integer, db.ForeignKey("course_categories.id"))
    course_id = db.Column(db.Integer, db.ForeignKey("courses.id"))


class CoursePrices(Base):
    course_id = db.Column(db.Integer, db.ForeignKey("courses.id"))
    price = db.Column(db.Float, nullable=True)
    percent = db.Column(db.Float, nullable=True)
    percent_price = db.Column(db.Float, nullable=True)
    author_id = db.Column(db.Integer)


class UserCoursePurchases(Base):
    user_id = db.Column(db.Integer)
    course_id = db.Column(db.Integer, db.ForeignKey("courses.id"))
    course_price_id = db.Column(db.Integer, db.ForeignKey("course_prices.id"))
    paid_percent = db.Column(db.Float, nullable=True)
