from commodity.models import CommodityGroup

from rest_framework import serializers

class CommodityGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommodityGroup
        fields = '__all__'
        