from commodity.models import DrugManufacturer
from rest_framework import serializers

class DrugManufacturerSerializer(serializers.ModelSerializer):
    class Meta:
        model = DrugManufacturer
        fields = '__all__'
        depth = 1
