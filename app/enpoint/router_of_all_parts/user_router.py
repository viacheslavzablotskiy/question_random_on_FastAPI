from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.crud_user.service import crud_user
from app.db.database import get_async_session
from app.models import User as DBUser, Question
from app.schemas import User, UserID, CreateUser


router = APIRouter()


@router.post('/create_user', response_model=User, tags=['users'])
async def create_user(
        obj_in: CreateUser,
        db_session: AsyncSession = Depends(get_async_session)):

    user = await crud_user.get_by_email(db_session=db_session, email=obj_in.email)
    if user:
        raise HTTPException(
            status_code=404, detail="User with this email already exists in system"
        )
    result_user = await crud_user.create_user(db_session=db_session, obj_in=obj_in)
    return result_user


@router.get('/get_all_users', response_model=List[User], tags=['users'])
async def get_all_users(skip: int = 0, limit: int = 100,
                        db_session: AsyncSession = Depends(get_async_session)):
    user_all = await crud_user.get_users(db_session=db_session, skip=skip, limit=limit)

    return user_all


