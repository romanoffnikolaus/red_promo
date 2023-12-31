from rest_framework import serializers

from .models import Rent


class RentSerialiser(serializers.ModelSerializer):
    class Meta:
        model = Rent
        fields = '__all__'