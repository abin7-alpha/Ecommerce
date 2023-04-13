from rest_framework import serializers
from order.models import OrderPayment

class OrderPaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderPayment
        fields = ('id','amount', 'created', 'updated', 'is_verified_by_admin', 'collected_by', 'status')
        depth = 1
