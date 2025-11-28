from datetime import timedelta#token süresi belirlerken dakika eklemek için
from typing import Optional#bir değer dönebilirde dönmeyebilirde
from app.api.deps import SessionDep#veri bağlantısı için
from app.core import security#güvenlik işlemleri için
from app.core.security import get_password_hash#şifreyi hashlemek için
from app.models.user import User#kullanıcı modeli

# şifre sıfırlama işlemleri için gerekli yardımcı fonksiyonlar
from app.utils import (
    generate_password_reset_token,
    verify_password_reset_token,
    generate_reset_password_email,
    send_email,
)

from app.api.deps import get_user_repository #kullanıcı deposu için

class AuthService:
    """Kimlik doğrulama ve kullanıcı hesabı hizmeti sınıfı."""
    def __init__(self,repo=None):
        self.repo=repo
        #servis hangi repo ile çalışacağını burada alıyor .
        #Repo:veritabanındaki kullanıcılarla etkileşim kurmak için kullanılır.

    async def authenticate(self,session:SessionDep,email: str, password: str) -> Optional[User]:
        """Kullanıcıyı kimlik doğrulama işlemi."""
        user = await self.repo.get_user_by_email(session=session,email=email)#email ile kullanıcıyı veritabanından alır
        if not user:
            return None
        if not security.verify_password(password, user.hashed_password):#şifre doğrulama işlemi
            return None
        return user
    async def create_access_token(self,user_id:int,expires_minutes: int):
        #Erişim tokeni oluşturma işlemi.
        expires_delta = timedelta(minutes=expires_minutes)#token süresi belirlerken dakika eklemek için
        return security.create_access_token(user_id,expires_delta)#token oluşturma fonksiyonu
    
    #Şifre reset maili gönderme işlemi
    async def send_password_recovery_email(self,session:SessionDep,email: str):#şifre kurtarma e-postası gönderme işlemi.
        user=await self.repo.get_user_by_email(session=session,email=email)#email ile kullanıcıyı veritabanından alır
        if not user:
            return False
        token=generate_password_reset_token(email=email)

        email.data =generate_password_reset_token(email=email)

        email_data = generate_reset_password_email(#e-posta içeriği oluşturma işlemi
            email_to=user.email,
            email=email,
            token=token,
        )
        

        send_email(#e-posta gönderme işlemi
            email_to=user.email,
            subject=email_data.subject,#e-posta konusu
            html_content=email_data.html_content,#e-posta içeriği

        )
        return True
    
    #ŞİFRE RESET İŞLEMİ
    async def reset_password(self, session: SessionDep, token: str, new_password: str):
        email = verify_password_reset_token(token)#token doğrulama işlemi
        if not email:
            return False

        user = await self.repo.get_user_by_email(session=session, email=email)
        if not user:
            return False

        user.hashed_password = get_password_hash(new_password)

        session.add(user)
        await session.commit()

        return True
    
    #Şifre kurtarma HTML içeriği oluşturma işlemi
    async def generate_recovery_html(self, session: SessionDep, email: str):
        user = await self.repo.get_user_by_email(session=session, email=email)
        if not user:
            return None

        token = generate_password_reset_token(email=email)#token oluşturma işlemi

        email_data = generate_reset_password_email(
            email_to=user.email,
            email=email,
            token=token
        )

        return email_data


    

