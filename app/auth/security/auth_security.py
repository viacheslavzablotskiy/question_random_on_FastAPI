from typing import Annotated

from fastapi import Security, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from jwt import PyJWTError
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status
from starlette.status import HTTP_403_FORBIDDEN

from app.db.config import SECRET_KEY, ALGORITHM
from app.db.database import get_async_session
from app.auth.schemas import Token, TokenData
from app.auth.crud_user.service import crud_user
from app.models import User

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token")


async def get_current_user(
        db: AsyncSession = Depends(get_async_session), token: str = Security(oauth2_scheme)
):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        # username: str = payload.get("sub")
        # token_data = TokenData(username=username)
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        token_data = Token(**payload)
    except PyJWTError:
        raise HTTPException(
            status_code=HTTP_403_FORBIDDEN, detail="Could not validate credentials"
        )
    user = await crud_user.get(db, id=token_data.id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


async def get_current_active_user(current_user: User = Security(get_current_user)):
    if not crud_user.is_active(current_user):
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


async def get_current_active_superuser(current_user: User = Security(get_current_user)):
    if not crud_user.is_superuser(current_user):
        raise HTTPException(
            status_code=400, detail="The user doesn't have enough privileges"
        )
    return current_user
