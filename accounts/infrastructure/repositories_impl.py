from typing import Optional
from django.contrib.auth import get_user_model
from .models import OTP
from accounts.domain.entities import UserEntity, OTPCode

User = get_user_model()

class DjangoUserRepository:
    def get_by_email(self, email: str) -> Optional[UserEntity]:
        try:
            u = User.objects.get(email=email)
            return UserEntity(id=u.id, email=u.email, username=u.username, is_active=u.is_active)
        except User.DoesNotExist:
            return None

    def create_user(self, email: str, username: str, password: str) -> UserEntity:
        u = User.objects.create_user(username=username, email=email, password=password)
        return UserEntity(id=u.id, email=u.email, username=u.username, is_active=u.is_active)

class DjangoOTPRepository:
    def create_code(self, user_id: int, purpose: str) -> OTPCode:
        from django.contrib.auth import get_user_model
        User = get_user_model()
        u = User.objects.get(id=user_id)
        otp = OTP.create_for(u, purpose)
        return OTPCode(id=otp.id, user_id=u.id, code=otp.code, purpose=otp.purpose, expires_at=otp.expires_at, used=otp.used)

    def verify_code(self, user_id: int, purpose: str, code: str) -> bool:
        try:
            otp = OTP.objects.filter(user_id=user_id, purpose=purpose, used=False).latest("id")
        except OTP.DoesNotExist:
            return False
        return otp.verify(code)