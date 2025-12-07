from datetime import timedelta
from typing import Optional

from  bfastapi.app.api.deps import SessionDep
from  bfastapi.app.core import security
from  bfastapi.app.core.security import get_password_hash
from  bfastapi.app.models.user import User

from  bfastapi.app.utils import (
    generate_password_reset_token,
    verify_password_reset_token,
    generate_reset_password_email,
    send_email,
)

# NOT: get_user_repository kaldırıldı, kullanılmıyor.

class AuthService:
    """Kimlik doğrulama ve kullanıcı hesabı hizmeti sınıfı."""

    def __init__(self, repo=None):
        # repo injection yapılabilir ancak None gelirse hata vermesin diye kontrol eklenecek
        self.repo = repo

    async def authenticate(self, session: SessionDep, email: str, password: str) -> Optional[User]:
        """Kullanıcıyı kimlik doğrulama işlemi."""

        if self.repo is None:
            raise ValueError("AuthService: repo is not initialized")

        user = await self.repo.get_user_by_email(session=session, email=email)

        if not user:
            return None

        if not security.verify_password(password, user.hashed_password):
            return None

        return user

    async def create_access_token(self, user_id: int, expires_minutes: int):
        """Erişim tokeni oluşturma işlemi."""
        expires_delta = timedelta(minutes=expires_minutes)

        return security.create_access_token(
            subject=str(user_id),
            expires_delta=expires_delta
        )

    async def send_password_recovery_email(self, session: SessionDep, email: str):
        """Şifre kurtarma e-postası gönderme işlemi."""

        if self.repo is None:
            raise ValueError("AuthService: repo is not initialized")

        user = await self.repo.get_user_by_email(session=session, email=email)
        if not user:
            return False

        token = generate_password_reset_token(email=email)

        email_data = generate_reset_password_email(
            email_to=user.email,
            email=email,
            token=token,
        )

        send_email(
            email_to=user.email,
            subject=email_data.subject,
            html_content=email_data.html_content,
        )

        return True

    async def reset_password(self, session: SessionDep, token: str, new_password: str):
        """Şifre reset işlemi."""
        email = verify_password_reset_token(token)

        if not email:
            return False

        if self.repo is None:
            raise ValueError("AuthService: repo is not initialized")

        user = await self.repo.get_user_by_email(session=session, email=email)
        if not user:
            return False

        user.hashed_password = get_password_hash(new_password)

        session.add(user)
        await session.commit()

        return True

    async def generate_recovery_html(self, session: SessionDep, email: str):
        """Şifre kurtarma HTML içeriği oluşturma işlemi."""

        if self.repo is None:
            raise ValueError("AuthService: repo is not initialized")

        user = await self.repo.get_user_by_email(session=session, email=email)
        if not user:
            return None

        token = generate_password_reset_token(email=email)

        email_data = generate_reset_password_email(
            email_to=user.email,
            email=email,
            token=token,
        )

        return email_data
