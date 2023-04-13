from order.models import Order
from rest_framework import serializers
from order.api.serializers.order_payment import OrderPaymentSerializer

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'
        depth = 4

class OrderSerializerForDetails(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ('id', 'order_no', 'order_items', 'amount', 'pending_amount', 'retailer',
                  'inv_url', 'long_url', 'updated', 'created', 'delivery_incharge', 'dispatch_dc',
                  'delivery_time', 'status', 'manager_comments', 'staff_comments', 
                  'retailer_comments', 'staff_rating', 'retailer_rating', 'is_staff_feed_back_provided', 
                  'is_retailer_feed_back_provided', 'image_url', 'is_post_confirmation_required',
                  'shipped_time', 'get_total_products', 'is_admin_verified', 'address', 'converted_delivery_time',
                  'converted_pack_start', 'converted_pack_end',)
        depth = 4
    
class OrderSerializerForRecentOrder(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'

class OrderSerializerForOrderPayment(serializers.ModelSerializer):
    order_payments = OrderPaymentSerializer(many=True)
    class Meta:
        model = Order
        fields = ('order_payments', 'amount', 'pending_amount', 'order_no', 'id')
        depth = 3
