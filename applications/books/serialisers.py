from rest_framework import serializers
from django.db.models import Min

from . import models
from applications.rent.models import Rent



class BookSeriliser(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = models.Book

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        if representation['quantity'] == 0:
            representation['Ближайший возврат:'] = Rent.objects.aggregate(nearest_date=Min('expiration_date'))['nearest_date']
        return representation