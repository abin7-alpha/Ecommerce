from commodity.models import Commodity
from rest_framework import serializers

class CommoditySerializer(serializers.ModelSerializer):
    class Meta:
        model = Commodity
        fields = '__all__'
        depth = 1
