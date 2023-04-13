from rest_framework import serializers
from crm.models import RetailerServiceRequest

class RetailerServiceRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = RetailerServiceRequest
        depth = 2
        fields = '__all__'
