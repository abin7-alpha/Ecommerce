from order.models import ShippingVendor
from rest_framework import serializers

class ShippingVendorSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShippingVendor
        fields = '__all__'
        depth = 2