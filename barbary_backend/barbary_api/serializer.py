from rest_framework import serializers


class LoginSerializer(serializers.Serializer):
    pass


class AddBarSerializer(serializers.Serializer):
    beginning = serializers.CharField(max_length=256)
    destination = serializers.CharField(max_length=256)
    price = serializers.CharField(max_length=256)
    date = serializers.DateField()
    weight = serializers.FloatField()
    product_type = serializers.CharField(max_length=256)
    product_packaging = serializers.CharField(max_length=256)
    fleet_type = serializers.CharField(max_length=256)
    description = serializers.CharField(max_length=512, allow_blank=True, allow_null=True)
