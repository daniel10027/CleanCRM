from django.db import models
from directory.infrastructure.models import Directory

class Contact(models.Model):
    directory = models.ForeignKey(Directory, on_delete=models.CASCADE, related_name="contacts")
    first_name = models.CharField(max_length=120, blank=True, null=True)
    last_name = models.CharField(max_length=120, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    phone = models.CharField(max_length=40, blank=True, null=True)
    extra = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email or self.phone or f"Contact#{self.id}"