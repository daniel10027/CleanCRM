from django.db import models
from directory.infrastructure.models import Directory

class Campaign(models.Model):
    CHANNELS = [("email","email"),("sms","sms"),("whatsapp","whatsapp")]
    name = models.CharField(max_length=255)
    channel = models.CharField(max_length=16, choices=CHANNELS)
    subject = models.CharField(max_length=255, blank=True, null=True)
    body = models.TextField()
    directory = models.ForeignKey(Directory, on_delete=models.CASCADE, related_name="campaigns")
    created_at = models.DateTimeField(auto_now_add=True)

class CampaignDelivery(models.Model):
    STATUS = [("pending","pending"),("sent","sent"),("failed","failed")]
    campaign = models.ForeignKey(Campaign, on_delete=models.CASCADE, related_name="deliveries")
    contact_id = models.IntegerField()
    destination = models.CharField(max_length=255)
    status = models.CharField(max_length=16, choices=STATUS, default="pending")
    error = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)