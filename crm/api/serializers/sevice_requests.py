from rest_framework import serializers
from crm.models import ServiceRequest

class ServiceRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceRequest
        depth = 2
        fields = '__all__'
