from typing import Annotated, TYPE_CHECKING
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession

from bfastapi.app.database import get_db
from bfastapi.app.core.config import settings
from bfastapi.app.core.security import ALGORITHM
from jose import jwt, JWTError

from bfastapi.app.models.user import User

from bfastapi.app.services.user_service import UserService



SessionDep = Annotated["AsyncSession", Depends(get_db)]



oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl=f"{settings.API_V1_STR}/auth/access-token"
)



user_service = UserService()



async def get_current_user(
    session: SessionDep,
    token: Annotated[str, Depends(oauth2_scheme)]
) -> User:

    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")

        if user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication token",
                headers={"WWW-Authenticate": "Bearer"},
            )

    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    user = await user_service.get_user_by_id(session=session, user_id=int(user_id))

    if not user:
        raise HTTPException(status_code=404, detail="User not found.")

    return user



async def get_current_active_user(
    current_user: Annotated[User, Depends(get_current_user)]
) -> User:

    if not current_user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Inactive user account."
        )

    return current_user



async def get_current_active_superuser(
    current_user: Annotated[User, Depends(get_current_active_user)]
) -> User:

    if not current_user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Requires superuser privileges."
        )

    return current_user


# Type alias for easier usage in endpoints
CurrentUser = Annotated[User, Depends(get_current_active_user)]
