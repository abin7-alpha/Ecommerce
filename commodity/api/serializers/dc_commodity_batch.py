from commodity.models import DcCommodityBatch
from rest_framework import serializers

class DcCommodityBatchSerializer(serializers.ModelSerializer):
    class Meta:
        model = DcCommodityBatch
        fields = ('id', 'dc_commodity', 'price', 'batch_id',
                  'minimum_order_quantity', 'expiry_date', 'available_quantity', 'mrp')
        depth = 2
        