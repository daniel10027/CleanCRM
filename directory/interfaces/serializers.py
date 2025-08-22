from rest_framework import serializers
from directory.infrastructure.models import Directory

class DirectorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Directory
        fields = ["id","name","owner","created_at"]
        read_only_fields = ["id","created_at","owner"]