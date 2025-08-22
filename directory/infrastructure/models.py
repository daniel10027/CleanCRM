from django.db import models
from django.conf import settings

class Directory(models.Model):
    """Répertoire appartenant à un utilisateur/organisation (simple)."""
    name = models.CharField(max_length=255)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="directories")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name