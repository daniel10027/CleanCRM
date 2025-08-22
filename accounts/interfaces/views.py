from rest_framework import status, views, permissions, response
from rest_framework_simplejwt.views import TokenRefreshView
from accounts.application.use_cases import (
    RegisterUseCase, LoginUseCase, PasswordResetRequestUseCase, PasswordResetConfirmUseCase
)
from accounts.application.dto import RegisterDTO, LoginDTO, PasswordResetRequestDTO, PasswordResetConfirmDTO
from accounts.infrastructure.repositories_impl import DjangoUserRepository, DjangoOTPRepository
from .serializers import (
    RegisterSerializer, LoginSerializer, PasswordResetRequestSerializer, PasswordResetConfirmSerializer
)
from django.contrib.auth import get_user_model

class RegisterView(views.APIView):
    permission_classes = [permissions.AllowAny]
    def post(self, request):
        ser = RegisterSerializer(data=request.data)
        ser.is_valid(raise_exception=True)
        uc = RegisterUseCase(users=DjangoUserRepository())
        user = uc.execute(RegisterDTO(**ser.validated_data))
        return response.Response({"id": user.id, "email": user.email, "username": user.username}, status=status.HTTP_201_CREATED)

class LoginView(views.APIView):
    permission_classes = [permissions.AllowAny]
    def post(self, request):
        ser = LoginSerializer(data=request.data)
        ser.is_valid(raise_exception=True)
        tokens = LoginUseCase().execute(LoginDTO(**ser.validated_data))
        return response.Response(tokens)

class PasswordResetRequestView(views.APIView):
    permission_classes = [permissions.AllowAny]
    def post(self, request):
        ser = PasswordResetRequestSerializer(data=request.data)
        ser.is_valid(raise_exception=True)
        PasswordResetRequestUseCase(DjangoUserRepository(), DjangoOTPRepository()).execute(
            PasswordResetRequestDTO(**ser.validated_data)
        )
        return response.Response({"detail": "Si l'email existe, un OTP a été généré."})

class PasswordResetConfirmView(views.APIView):
    permission_classes = [permissions.AllowAny]
    def post(self, request):
        ser = PasswordResetConfirmSerializer(data=request.data)
        ser.is_valid(raise_exception=True)
        data = ser.validated_data
        def changer():
            User = get_user_model()
            u = User.objects.get(id=data["user_id"])
            u.set_password(data["new_password"])
            u.save(update_fields=["password"])
        PasswordResetConfirmUseCase(DjangoUserRepository(), DjangoOTPRepository()).execute(
            PasswordResetConfirmDTO(user_id=data["user_id"], code=data["code"], change_password=changer)
        )
        return response.Response({"detail": "Mot de passe changé."})