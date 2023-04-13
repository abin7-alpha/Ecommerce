from commodity.models import CommodityCategory

from rest_framework import serializers

class CommodityCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = CommodityCategory
        fields = '__all__'
        