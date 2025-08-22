from rest_framework import serializers
from campaigns.infrastructure.models import Campaign, CampaignDelivery

class CampaignSerializer(serializers.ModelSerializer):
    class Meta:
        model = Campaign
        fields = ["id","name","channel","subject","body","directory","created_at"]
        read_only_fields = ["id","created_at"]

class CampaignDeliverySerializer(serializers.ModelSerializer):
    class Meta:
        model = CampaignDelivery
        fields = ["id","campaign","contact_id","destination","status","error","created_at"]
        read_only_fields = ["id","status","error","created_at"]