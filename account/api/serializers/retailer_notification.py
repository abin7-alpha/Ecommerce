from account.models import RetailerNotification
from rest_framework import serializers

class RetailerNotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = RetailerNotification
        fields = '__all__'
        depth=1
