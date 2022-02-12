from rest_framework import serializers
from django.core.validators import RegexValidator

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


class UpdateBarSerializer(serializers.Serializer):
    BarId = serializers.IntegerField()
    beginning = serializers.CharField(max_length=256)
    destination = serializers.CharField(max_length=256)
    price = serializers.CharField(max_length=256)
    date = serializers.DateField()
    weight = serializers.FloatField()
    product_type = serializers.CharField(max_length=256)
    product_packaging = serializers.CharField(max_length=256)
    fleet_type = serializers.CharField(max_length=256)
    description = serializers.CharField(max_length=512, allow_blank=True, allow_null=True)


class RegisterSerializer(serializers.Serializer):
    phone_number = serializers.CharField(max_length=11, min_length=11, allow_null=False, allow_blank=False,
                                         validators=[RegexValidator(r'^[1,2,3,4,5,6,7,8,9,0]{11}$')])


class BarIdSerializer(serializers.Serializer):
    barId = serializers.IntegerField()