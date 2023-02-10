import datetime
import logging
from typing import Optional, Type, TypeVar, Union
from uuid import UUID

import grpc
from sqlalchemy import exc
from sqlalchemy import select
from sqlalchemy.sql.expression import column

from db.session import async_session
from utils.pagination import apply_pagination

ModelType = TypeVar("ModelType")


class CRUDBase:
    def __init__(self, model: Type[ModelType]):
        self.model = model

    def order_by(self, order_by='id', desc=False):
        query = select(self.model).filter(self.model.deleted_at.is_(None))
        if desc:
            query = query.order_by(getattr(self.model, order_by).desc())
        else:
            query = query.order_by(getattr(self.model, order_by).asc())
        return query

    async def get(self, context, obj_id: Union[UUID, str, int]):
        try:
            async with async_session() as db:
                query = select(self.model).where(self.model.id == obj_id).filter(self.model.deleted_at.is_(None))
                response = await db.execute(query)
                obj = response.scalar_one_or_none()
                if not obj:
                    await context.abort(grpc.StatusCode.NOT_FOUND, f"{self.model.__table__} object not found!")
                return obj
        except Exception as e:
            logging.error(e)
            await context.abort(grpc.StatusCode.INTERNAL, "Internal server error")

    async def get_list(self, context, order_by, desc):
        try:
            async with async_session() as db:
                query = self.order_by(order_by, desc)
                response = await db.execute(query)
                results = response.scalars().all()
                return results, len(results)
        except Exception as e:
            logging.error(e)
            raise await context.abort(grpc.StatusCode.INTERNAL, "Internal server error")

    async def get_paginated_list(self, context, page_number, page_size, order_by, desc):
        try:
            async with async_session() as db:
                query = self.order_by(order_by, desc)
                query, pagination = await apply_pagination(self.model, query, page_number=page_number,
                                                           page_size=page_size)
                response = await db.execute(query)
                return response.scalars().all(), pagination
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

    async def delete(self, context, obj_id: Union[UUID, str, int]):
        try:
            async with async_session() as db:
                query = select(self.model).where(self.model.id == obj_id)
                response = await db.execute(query)
                obj = response.scalar_one_or_none()
                if not obj:
                    await context.abort(grpc.StatusCode.NOT_FOUND, f"{self.model.__table__} object not found!")
                # Soft delete logic
                obj.deleted_at = datetime.datetime.now()
                db.add(obj)
                await db.commit()
                await db.refresh(obj)
                await db.commit()
        except Exception as e:
            logging.error(e)
            await context.abort(grpc.StatusCode.INTERNAL, "Internal server error")
