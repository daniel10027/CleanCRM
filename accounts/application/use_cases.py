from dataclasses import dataclass
from typing import Optional
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from .dto import RegisterDTO, LoginDTO, PasswordResetRequestDTO, PasswordResetConfirmDTO
from accounts.domain.repositories import UserRepository, OTPRepository

@dataclass
class RegisterUseCase:
    users: UserRepository
    def execute(self, dto: RegisterDTO):
        user = self.users.create_user(dto.email, dto.username, dto.password)
        return user

@dataclass
class LoginUseCase:
    def execute(self, dto: LoginDTO):
        user = authenticate(username=dto.username, password=dto.password)
        if not user:
            raise ValueError("Identifiants invalides")
        refresh = RefreshToken.for_user(user)
        return {"access": str(refresh.access_token), "refresh": str(refresh)}

@dataclass
class PasswordResetRequestUseCase:
    users: UserRepository
    otps: OTPRepository
    def execute(self, dto: PasswordResetRequestDTO):
        user = self.users.get_by_email(dto.email)
        if not user:
            return
        self.otps.create_code(user.id, purpose="password_reset")

@dataclass
class PasswordResetConfirmUseCase:
    users: UserRepository
    otps: OTPRepository
    def execute(self, dto: PasswordResetConfirmDTO):
        ok = self.otps.verify_code(dto.user_id, "password_reset", dto.code)
        if not ok:
            raise ValueError("OTP invalide")
        # Le changement de mot de passe est effectué côté repo impl (infrastructure)
        dto.change_password()
        return True