from commodity.models import DistributionStoreIndent
from rest_framework import serializers

class DistributionStoreIndentSerializer(serializers.ModelSerializer):
    class Meta:
        model = DistributionStoreIndent
        fields = '__all__'
        depth = 2
        