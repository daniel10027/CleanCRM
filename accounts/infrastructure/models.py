from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
import random

class User(AbstractUser):
    # email unique pour simplicité
    email = models.EmailField(unique=True)

class OTP(models.Model):
    PURPOSES = [("login", "login"), ("password_reset", "password_reset")]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    code = models.CharField(max_length=6)
    purpose = models.CharField(max_length=32, choices=PURPOSES)
    expires_at = models.DateTimeField()
    used = models.BooleanField(default=False)

    @staticmethod
    def generate_code():
        return f"{random.randint(0, 999999):06d}"

    @classmethod
    def create_for(cls, user, purpose: str, ttl_minutes=10):
        obj = cls.objects.create(
            user=user,
            code=cls.generate_code(),
            purpose=purpose,
            expires_at=timezone.now() + timezone.timedelta(minutes=ttl_minutes),
        )
        return obj

    def verify(self, code: str) -> bool:
        if self.used:
            return False
        if timezone.now() > self.expires_at:
            return False
        if self.code != code:
            return False
        self.used = True
        self.save(update_fields=["used"])
        return True