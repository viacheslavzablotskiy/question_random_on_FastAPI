from typing import TypeVar, Generic, Type

from pydantic import BaseModel
from sqlalchemy import select, insert
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.database import Base

ModelType = TypeVar("ModelType", bound=Base)
CreateSchemasType = TypeVar("CreateSchemasType", bound=BaseModel)
# UpdateSchemasType = TypeVar("UpdateSchemasType", bound=BaseModel)


class CRUDBase(Generic[ModelType, CreateSchemasType]):
    def __init__(self, model: Type[ModelType]):
        self.model = model

    async def get_user(self, db_session: AsyncSession, user_id: int):
        query = select(self.model).where(self.model.id == user_id)
        result = await db_session.execute(query)
        return result.scalars().first()

    async def get_users(self, db_session: AsyncSession, *, skip: int = 0, limit: int = 100):
        query = select(self.model).limit(limit)
        result = await db_session.execute(query)
        return result.scalars().all()

    async def create_user(self, db_session: AsyncSession, obj_in: CreateSchemasType):
        data = insert(self.model).values(**obj_in.dict())

        await db_session.execute(data)
        await db_session.commit()
        return data

