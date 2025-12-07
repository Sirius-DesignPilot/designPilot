from pydantic import BaseModel, EmailStr
from typing import Optional


# Temel kullanıcı şeması (model ile uyumlu)
class UserBase(BaseModel):
    email: EmailStr


# Kullanıcı oluşturma (register) şeması
class UserCreate(UserBase):
    password: str   # plain password buraya gelir


# Kullanıcı güncelleme şeması
class UserUpdate(BaseModel):
    password: Optional[str] = None
    # İleride full_name eklersen buraya eklenebilir


# User objesi response olarak dönerken kullanılacak şema
class UserResponse(UserBase):
    id: int
    is_active: bool
    is_superuser: bool

    class Config:
        from_attributes = True
