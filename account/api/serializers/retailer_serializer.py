from account.models import Retailer
from rest_framework import serializers

from order.api.serializers.order import OrderSerializer

class RetailerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Retailer
        fields = (
            'id', 'user', 'address', 'shops', 'dc', 'selected_city', 'position', 'position',
            'gst_no', 'created', 'is_admin_verified', 'is_payment_check_required', 'pending_amount_limit',
            'total_amount_outstanding', 'updated', 'document_pic', 'city', 'prefered_lang', 'prefered_lang_code',
            'last_active_login', 'last_notification_view'
        )
        depth = 2
    
class RetailerOrderSerializer(serializers.ModelSerializer):
    orders = OrderSerializer(many=True)
    class Meta:
        model = Retailer
        fields = '__all__'
        depth = 1
