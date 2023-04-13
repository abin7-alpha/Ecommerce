from commodity.models import DcCommodity
from rest_framework import serializers
from commodity.api.serializers.dc_commodity_batch import DcCommodityBatchSerializer

class DcCommodityForBatchSerializer(serializers.ModelSerializer):
    commodity_batches = DcCommodityBatchSerializer(many=True)
    class Meta:
        model = DcCommodity
        fields = '__all__'
        depth = 2

class DcCommoditySerializer(serializers.ModelSerializer):
    class Meta:
        model = DcCommodity
        fields = '__all__'
        depth = 1
