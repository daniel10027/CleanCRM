from rest_framework import serializers
from contacts.infrastructure.models import Contact

class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = ["id","directory","first_name","last_name","email","phone","extra","created_at"]
        read_only_fields = ["id","created_at"]