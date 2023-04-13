from account.models import RetailerRecentSearch
from rest_framework import serializers

class RetailerRecentSearchSerializer(serializers.ModelSerializer):
    class Meta:
        model = RetailerRecentSearch
        fields = '__all__'
        depth = 1
