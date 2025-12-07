from datetime import timedelta
from typing import Annotated, Any

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.security import OAuth2PasswordRequestForm

# DOĞRU DEPS IMPORTU
from bfastapi.app.api.deps import (
    CurrentUser,
    SessionDep,
    get_current_active_superuser
)

# DOĞRU SECURITY & CONFIG IMPORTU
from bfastapi.app.core.security import (
    create_access_token,
    get_password_hash,
    verify_password
)
from bfastapi.app.core.config import settings

# DOĞRU SERVICES IMPORTU
from bfastapi.app.services.auth_services import AuthService
from bfastapi.app.services.user_service import UserService

# Schemas
from bfastapi.app.schemas.auth import (
    Message,
    TokenResponse,
    UserPublic,
    NewPassword,
    RegisterSchema as UserCreate,
)


# Use TokenResponse as Token to keep existing response_model names
Token = TokenResponse

# DOĞRU UTILS IMPORTU
from bfastapi.app.utils import (
    generate_password_reset_token,
    generate_reset_password_email,
    send_email,
    verify_password_reset_token,
)


# Services
user_service = UserService()
auth_service = AuthService(repo=user_service)

router = APIRouter(tags=["auth"])

@router.post("/auth/register", response_model=UserPublic)
async def register_user(session: SessionDep, user_in: UserCreate) -> Any:
    """
    Yeni kullanıcı kaydı oluşturur.
    """
    # Kayıt işlemi için veritabanı kontrolü
    user = await user_service.get_user_by_email(session=session, email=user_in.email)
    if user:
        raise HTTPException(
            status_code=400,
            detail="The user with this email already exists in the system.",
        )
    hashed_pwd=get_password_hash(user_in.password)
    
    # UserCreate şeması (email, password) ile yeni kullanıcı oluştur
    new_user = await user_service.create_user(
        session=session,
        email=user_in.email,
        hashed_password=hashed_pwd
    )
    
    return new_user


# LOGIN → Token oluşturma
@router.post("/auth/token", response_model=Token)
async def auth_access_token(
    session: SessionDep,
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()]
) -> Token:

    user = await auth_service.authenticate(
        session=session,
        email=form_data.username,
        password=form_data.password,
    )

    if not user:
        raise HTTPException(status_code=400, detail="Incorrect email or password")

    if not user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")

    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)

    token = create_access_token(
        subject=str(user.id),
        expires_delta=access_token_expires
    )

    return Token(access_token=token, token_type="bearer")


# MEVCUT TOKEN TESTİ
@router.post("/test-token")
def test_token(current_user: CurrentUser) -> Any:
    return current_user


# PASSWORD RECOVERY
@router.post("/auth/password-recovery/{email}", response_model=Message)
async def recover_password(email: str, session: SessionDep) -> Message:

    user = await user_service.get_user_by_email(session=session, email=email)

    if not user:
        raise HTTPException(
            status_code=404,
            detail="The user with this email does not exist in the system."
        )

    password_reset_token = generate_password_reset_token(email=email)

    email_data = generate_reset_password_email(
        email_to=user.email,
        email=email,
        token=password_reset_token
    )

    send_email(
        email_to=user.email,
        subject=email_data.subject,
        html_content=email_data.html_content,
    )

    return Message(message="Password recovery email sent")


# PASSWORD RESET
@router.post("/reset-password/", response_model=Message)
async def reset_password(session: SessionDep, body: NewPassword) -> Message:

    email = verify_password_reset_token(token=body.token)
    if not email:
        raise HTTPException(status_code=400, detail="Invalid Token")

    user = await user_service.get_user_by_email(session=session, email=email)

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if not user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")

    hashed_password = get_password_hash(password=body.new_password)
    user.hashed_password = hashed_password

    session.add(user)
    await session.commit()

    return Message(message="Password updated successfully.")


# HTML Reset Password Template
@router.post(
    "/password-recovery-html-content/{email}",
    dependencies=[Depends(get_current_active_superuser)],
    response_class=HTMLResponse,
)
async def recover_password_html_content(email: str, session: SessionDep) -> Any:

    user = await user_service.get_user_by_email(session=session, email=email)

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    password_reset_token = generate_password_reset_token(email=email)

    email_data = generate_reset_password_email(
        email_to=user.email,
        email=email,
        token=password_reset_token
    )

    return HTMLResponse(
        content=email_data.html_content,
        headers={"subject": email_data.subject}
    )
