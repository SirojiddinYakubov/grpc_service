import json
from typing import Optional, Any

from sqlalchemy import types
from sqlalchemy.dialects.postgresql import JSONB

from app.utils.uuid6 import uuid7, UUID
from sqlmodel import SQLModel as _SQLModel, Field, Column
from sqlalchemy.orm import declared_attr
from datetime import datetime

# id: implements proposal uuid7 draft4


from app.core.config import settings


class SQLModel(_SQLModel):
    @declared_attr  # type: ignore
    def __tablename__(cls) -> str:
        return cls.__name__


class BaseUUIDModel(SQLModel):
    id: UUID = Field(
        default_factory=uuid7,
        primary_key=True,
        index=True,
        nullable=False,
    )
    updated_at: Optional[datetime] = Field(
        default_factory=datetime.utcnow, sa_column_kwargs={"onupdate": datetime.utcnow}
    )
    created_at: Optional[datetime] = Field(default_factory=datetime.utcnow)


class BaseModel(SQLModel):
    id: int = Field(
        primary_key=True,
        index=True,
        nullable=False,
    )
    updated_at: Optional[datetime] = Field(
        default_factory=datetime.utcnow, sa_column_kwargs={"onupdate": datetime.utcnow}
    )
    created_at: Optional[datetime] = Field(default_factory=datetime.utcnow)
    deleted_at: Optional[datetime]


class SaTranslationFieldComparator(JSONB.Comparator):
    def __eq__(self, other: Any) -> bool:
        print(36, other)
        return self.contains({"uz": other})


class SaTranslationField(types.TypeDecorator):
    impl: JSONB = JSONB()
    cache_ok = True
    comparator_factory = SaTranslationFieldComparator

    def coerce_compared_value(self, op: Any, value: Any) -> types.TypeEngine[Any]:
        print(45, op, value)
        return self.impl.coerce_compared_value(op, value)

    def process_bind_param(self, value: Any, dialect: Any) -> Optional[dict]:  # type: ignore
        if isinstance(value, dict):
            if not all(map(lambda k: k in settings.ALLOWED_LANGUAGES, value.keys())):
                raise ValueError("This language cannot be added to the database")
            return value
        elif isinstance(value, str):
            return dict(uz=value)
        return dict()

    def process_result_value(self, value: Any, dialect: Any) -> Optional[Any]:
        # translated = value.get("uz")
        return value


def TranslationField(**kwargs: Any) -> Any:
    return Field(sa_column=Column(SaTranslationField), nullable=False, default=dict(), **kwargs)

# q = select(Region).filter(
#            Region.title['uz'].astext.cast(String) == "Toshkent"
#        )
