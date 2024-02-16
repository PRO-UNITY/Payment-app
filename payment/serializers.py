from rest_framework import serializers
from payment.models import UserPayment


class PaymentSerializers(serializers.ModelSerializer):
    class Meta:
        model = UserPayment
        fields = '__all__'
