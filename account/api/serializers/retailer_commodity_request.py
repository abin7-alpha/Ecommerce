from account.models import RetailerCommodityRequests
from rest_framework import serializers

from commodity.api.serializers.dc_commodity import DcCommodityForBatchSerializer

class RetailerCommodityRequestSerializer(serializers.ModelSerializer):
    dcCommodity = DcCommodityForBatchSerializer()
    class Meta:
        model = RetailerCommodityRequests
        fields = ('id', 'dcCommodity', 'subscribed_on', 'created', 'updated', 'is_active', 'availabilty_last_notified')
        depth = 3