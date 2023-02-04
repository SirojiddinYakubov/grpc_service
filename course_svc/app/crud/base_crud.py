import logging
from typing import Optional, Type, TypeVar, Union, List
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from db.session import async_session

ModelType = TypeVar("ModelType")


class CRUDBase:
    def __init__(self, model: Type[ModelType]):
        self.model = model

    async def get(
            self, *, id: Union[UUID, str, int], db_session: Optional[AsyncSession] = None
    ) -> Optional[ModelType]:
        try:
            async with async_session() as db:
                query = select(self.model).where(self.model.id == id)
                response = await db.execute(query)
                obj = response.scalar_one_or_none()
                if obj:
                    return 200, obj
                else:
                    return 404, f"{self.model.__table__} object not found!"
        except Exception as e:
            logging.error(e)
            return 500, "Internal server error"

    async def get_multi(
            self,
            *,
            skip: int = 0,
            limit: int = 100,
            # query: Optional[Union[T, Select[T]]] = None,
    ):
        try:
            async with async_session() as db:
                # db_session = db_session or db.session
                # if query is None:
                query = select(self.model).offset(skip).limit(limit).order_by(self.model.id)
                response = await db.execute(query)
                return 200, response.scalars().all()
        except Exception as e:
            logging.error(e)
            return 500, "Internal server error"
