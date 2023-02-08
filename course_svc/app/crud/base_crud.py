import logging
from typing import Optional, Type, TypeVar, Union
from uuid import UUID

import grpc
from sqlalchemy import exc
from sqlalchemy import select

from db.session import async_session

ModelType = TypeVar("ModelType")


class CRUDBase:
    def __init__(self, model: Type[ModelType]):
        self.model = model

    async def get(self, context, obj_id: Union[UUID, str, int]) -> Optional[ModelType]:
        try:
            async with async_session() as db:
                query = select(self.model).where(self.model.id == obj_id)
                response = await db.execute(query)
                obj = response.scalar_one_or_none()
                if not obj:
                    await context.abort(grpc.StatusCode.NOT_FOUND, f"{self.model.__table__} object not found!")
                return obj
        except Exception as e:
            logging.error(e)
            await context.abort(grpc.StatusCode.INTERNAL, "Internal server error")

    async def get_multi(self, context, limit: int = 10, offset: int = 1):
        try:
            async with async_session() as db:
                query = select(self.model).offset(offset).limit(limit).order_by(self.model.id)
                response = await db.execute(query)
                return response.scalars().all()
        except Exception as e:
            logging.error(e)
            raise await context.abort(grpc.StatusCode.INTERNAL, "Internal server error")

    async def create(self, context, **obj_data):
        try:
            async with async_session() as db:
                db_obj = self.model(**obj_data)
                try:
                    db.add(db_obj)
                    await db.commit()
                except exc.IntegrityError:
                    db.rollback()
                    raise await context.abort(grpc.StatusCode.ALREADY_EXISTS,
                                              f"{self.model.__table__} object already exists!")
                await db.refresh(db_obj)
                return db_obj
        except Exception as e:
            logging.error(e)
            raise await context.abort(grpc.StatusCode.INTERNAL, "Internal server error")

    async def update(self, context, updated_obj):
        try:
            async with async_session() as db:
                db.add(updated_obj)
                await db.commit()
                await db.refresh(updated_obj)
                return updated_obj
        except Exception as e:
            logging.error(e)
            await context.abort(grpc.StatusCode.INTERNAL, "Internal server error")
