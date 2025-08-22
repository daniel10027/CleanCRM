from django.contrib import admin
from .infrastructure.models import Campaign, CampaignDelivery
admin.site.register(Campaign)
admin.site.register(CampaignDelivery)