from datetime import timedelta
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.schemas import Token
from app.db.config import ACCESS_TOKEN_EXPIRE_MINUTES
from app.db.database import get_async_session
from app.auth.crud_user.service import crud_user
from app.auth.security.crf_token import create_access_token
from app.schemas import User
from app.models import User as DBUser
from app.auth.security.auth_security import get_current_user

router = APIRouter()


@router.post("/token", response_model=Token, tags=['login'])
async def login_access_token(
        db_session: AsyncSession = Depends(get_async_session),
        form_data: OAuth2PasswordRequestForm = Depends()
):
    user = await  crud_user.authenticate(db_session=db_session,
                                         email=form_data.username, password=form_data.password)
    if not user:
        raise HTTPException(
            status_code=404, detail="Incorret password or username"
        )
    elif not await crud_user.is_active(user):
        raise HTTPException(
            status_code=400, detail="Inactive user"
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    return {
        "access_type": await create_access_token(
            data = {"user_id": user.id}, expires_delta=access_token_expires
        ),
        "token_type": "bearer"
    }


@router.post("/current_user/login", tags=["login"], response_model=User)
async def get_current_user_au(get_current_user_: DBUser = Depends(get_current_user)):

    return get_current_user_

