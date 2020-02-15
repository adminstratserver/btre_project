from rest_framework import serializers
from .models import Order
from django.contrib.auth.models import User


class OrderSerializer(serializers.ModelSerializer):  # create class to serializer model
    creator = serializers.ReadOnlyField(source='creator.username')

    class Meta:
        model = Order
        fields = ('tradeorder', 'datetime', 'sequencenumber', 'creator')


class UserSerializer(serializers.ModelSerializer):  # create class to serializer usermodel
    orders = serializers.PrimaryKeyRelatedField(many=True, queryset=Order.objects.all())

    class Meta:
        model = User
        fields = ('id', 'username', 'orders')