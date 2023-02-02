from app.models.base_model import BaseUUIDModel, TranslationField
from uuid import UUID
from sqlmodel import Field, SQLModel, Relationship
from typing import Optional, Union


class MediaBase(SQLModel):
    title: Optional[Union[dict, str]] = TranslationField()
    description: Optional[Union[dict, str]] = TranslationField()
    path: Optional[str]


class Media(BaseUUIDModel, MediaBase, table=True):
    pass


class ImageMediaBase(SQLModel):
    file_format: Optional[str]
    width: Optional[int]
    height: Optional[int]


class ImageMedia(BaseUUIDModel, ImageMediaBase, table=True):
    media_id: Optional[UUID] = Field(default=None, foreign_key="Media.id")
    media: Media = Relationship(
        sa_relationship_kwargs={
            "lazy": "selectin",
            "primaryjoin": "ImageMedia.media_id==Media.id",
        }
    )


class FileMediaBase(SQLModel):
    file_format: Optional[str]
    size: Optional[int]


class FileMedia(BaseUUIDModel, FileMediaBase, table=True):
    media_id: Optional[UUID] = Field(default=None, foreign_key="Media.id")
    media: Media = Relationship(
        sa_relationship_kwargs={
            "lazy": "selectin",
            "primaryjoin": "FileMedia.media_id==Media.id",
        }
    )