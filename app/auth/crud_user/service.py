from typing import Optional

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import insert, select

from app.auth.utils import CRUDBase
from app.db.database import get_async_session
from app.schemas import User, CreateUser
from app.models import User as DBUser
from app.utils import verify_password, get_hash_password


class CRUDUser(CRUDBase[User, CreateUser]):

    async def get_by_email(self, email: str, db_session: AsyncSession):
        query = select(DBUser).where(DBUser.email == email)
        result = await db_session.execute(query)
        return result.scalars().first()

    async def get_user(self, user_id: int, db_session: AsyncSession = Depends(get_async_session)):
        query = select(DBUser).where(DBUser.id == user_id)
        result = await db_session.execute(query)
        return result.scalars().first()

    async def create_user(self, db_session: AsyncSession, obj_in: CreateUser):
        query = select(DBUser)
        result_query = await db_session.execute(query)
        count_result_query = len(result_query.scalars().all())
        user_in = CreateUser(
            id=count_result_query + 1, full_name=obj_in.full_name, email=obj_in.email,
            hashed_password=await get_hash_password(obj_in.hashed_password)
        )
        query_1 = insert(DBUser).values(**user_in.dict())
        await db_session.execute(query_1)
        await db_session.commit()

        user_now_creating = select(DBUser).where(DBUser.id == user_in.id)
        result_user_now_creating = await db_session.execute(user_now_creating)
        return result_user_now_creating.scalars().first()

    async def authenticate(self, db_session: AsyncSession, email: str, password: str) -> Optional[DBUser]:
        user = await self.get_by_email(db_session=db_session, email=email)
        if not user:
            return None
        if not await verify_password(password, user.hashed_password):
            return None
        return user

    async def is_active(self, user: User) -> bool:
        return user.is_active

    async def is_superuser(self, user: User) -> bool:
        return user.is_superuser


crud_user = CRUDUser(DBUser)
