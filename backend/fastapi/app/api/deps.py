
from typing import Annotated,AsyncGenerator

import jwt
from fastapi import Depends, HTTPException,status
from fastapi.security import OAuth2PasswordBearer
from jwt.exceptions import InvalidTokenError
from pydantic import ValidationError
from sqlalchemy.ext.asyncio import AsyncSession

from app.core import config,security
from app.database import SessionLocal
from app.schemas import auth as auth_schema
from app.models import user as user_model



reusable_oauth2=OAuth2PasswordBearer(
    tokenUrl=f"{settings.API_V1_STR}/auth/login"
)

def get_db()->AsyncGenerator[AsyncSession, None]:
    with AsyncSession(SessionLocal()) as session:
        async with SessionLocal() as session:
            yield session

SessionDep=Annotated[AsyncSession,Depends(get_db)]
TokenDep=Annotated[str,Depends(reusable_oauth2)]

async def get_current_user(session:SessionDep,token:TokenDep)->user_model.User:
    try:
        payload=jwt.decode(
            token,settings.SECRET_KEY,algorithms=[security.ALGORITHM]
        )
        token_data=user_model(**payload)
    except (InvalidTokenError,ValidationError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
        )
    result=await session.execute(
        select(user_model.User).where(user_model.User.id==token_data.sub)
    )
    user=result.scalars().first()

    if not user:
        raise HTTPException(status_code=404,detail="User not found")
    return user

CurrentUser=Annotated[user_model.User,Depends(get_current_user)]

async def get_current_active_user(
        current_user:CurrentUser
)->user_model.User:
    if not current_user.is_active:
        raise HTTPException(status_code=400,detail="Inactive user")
    return current_user







