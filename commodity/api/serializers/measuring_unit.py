from commodity.models import CommodityMeasuringUnits
from rest_framework import serializers

class CommodityMeasuringUnitsSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommodityMeasuringUnits
        fields = '__all__'
        depth = 1
