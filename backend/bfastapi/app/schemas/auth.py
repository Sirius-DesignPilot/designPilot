from pydantic import BaseModel, EmailStr



class RegisterSchema(BaseModel):
    email: EmailStr
    password: str
    # full_name: str  # User modelde olmadığı için şimdilik kaldırıldı



class LoginSchema(BaseModel):
    email: EmailStr
    password: str



class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"



class NewPassword(BaseModel):
    token: str
    new_password: str



class Message(BaseModel):
    message: str



class UserPublic(BaseModel):
    id: int
    email: EmailStr
    is_active: bool
    is_superuser: bool

    class Config:
        from_attributes = True
