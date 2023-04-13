from account.models import RetailerShop
from rest_framework import serializers

class RetailerShopSerializer(serializers.ModelSerializer):
    class Meta:
        model = RetailerShop
        fields = '__all__'
        depth = 1