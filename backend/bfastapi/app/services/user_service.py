from typing import Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from bfastapi.app.models.user import User


class UserService:
    """
    Kullanıcı işlemleri servisi (repository mantığı).
    AuthService bu sınıfı kullanarak kullanıcı yönetimi yapar.
    """

    # ----------------------------------------------------------------------
    async def get_user_by_email(
        self,
        session: AsyncSession,
        email: str
    ) -> Optional[User]:
        """Email ile kullanıcıyı getir."""
        stmt = select(User).where(User.email == email)
        result = await session.execute(stmt)
        return result.scalars().first()

    # ----------------------------------------------------------------------
    async def get_user_by_id(
        self,
        session: AsyncSession,
        user_id: int
    ) -> Optional[User]:
        """ID ile kullanıcıyı getir."""
        stmt = select(User).where(User.id == user_id)
        result = await session.execute(stmt)
        return result.scalars().first()

    # ----------------------------------------------------------------------
    async def create_user(
        self,
        session: AsyncSession,
        email: str,
        hashed_password: str,
        is_active: bool = True,
        is_superuser: bool = False,
    ) -> User:
        """Yeni kullanıcı oluştur."""
        new_user = User(
            email=email,
            hashed_password=hashed_password,
            is_active=is_active,
            is_superuser=is_superuser,
        )

        session.add(new_user)
        await session.commit()
        await session.refresh(new_user)

        return new_user

    # ----------------------------------------------------------------------
    async def update_password(
        self,
        session: AsyncSession,
        user: User,
        new_hashed_password: str
    ) -> User:
        """Kullanıcının şifresini güncelle."""
        user.hashed_password = new_hashed_password
        session.add(user)
        await session.commit()
        await session.refresh(user)
        return user
