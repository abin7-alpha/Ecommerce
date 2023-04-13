from rest_framework import serializers

class LedgerSerilizer(serializers.Serializer):
    payment_mode = serializers.CharField(max_length=200)
    created = serializers.DateTimeField()
    is_online_payment = serializers.BooleanField()
    txn_id = serializers.CharField()
    amount = serializers.FloatField()
    is_verified_by_admin = serializers.BooleanField()
    orders = serializers.ListField()
