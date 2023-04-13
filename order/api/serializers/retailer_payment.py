from rest_framework import serializers
from order.models import RetailerPayment

class RetailerPaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = RetailerPayment
        fields = ('payment_mode', 'created', 'is_online_payment', 'txn_id', 'amount',
                  'is_verified_by_admin', 'created')
        depth = 1


class AllRetailerPaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = RetailerPayment
        fields = ('id', 'payment_mode', 'created', 'is_online_payment', 'txn_id', 'amount',
                  'is_verified_by_admin', 'created', 'retailer', 'status')
        depth = 2
