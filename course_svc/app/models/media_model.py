import sqlalchemy as db
from sqlalchemy.orm import relationship

from .base_model import Base


# class MediaBase(Base):
#     __abstract__ = True
#
#     title = db.Column(db.String, nullable=False)
#     description = db.Column(db.String, nullable=True)
#     path = db.Column(db.String, nullable=True)


class Media(Base):
    title = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=True)
    path = db.Column(db.String, nullable=True)


class ImageMedia(Base):
    file_format = db.Column(db.String, nullable=False)
    width = db.Column(db.Integer, nullable=True)
    height = db.Column(db.Integer, nullable=True)
    media_id = db.Column(db.Integer, db.ForeignKey(Media.id))
    # media = relationship('Media', foreign_keys='ImageMedia.media_id')


class FileMedia(Base):
    file_format = db.Column(db.String, nullable=False)
    size = db.Column(db.Integer, nullable=True)
    media_id = db.Column(db.Integer, db.ForeignKey(Media.id))
    # media = relationship('Media', foreign_keys='ImageMedia.media_id')
