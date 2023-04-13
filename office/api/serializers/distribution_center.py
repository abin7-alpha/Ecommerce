from rest_framework import serializers
from order.models import DistributionCenter

class DistributionCenterSerializer(serializers.ModelSerializer):
    class Meta:
        model = DistributionCenter
        fields = '__all__'
        depth = 1
