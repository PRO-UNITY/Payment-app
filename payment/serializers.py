from rest_framework import serializers
from payment.models import Cards, Payment, PaymentCards
from django.contrib.auth.models import User
from django.conf import settings
import stripe


class PaymentSerializer(serializers.Serializer):
    token = serializers.CharField(min_length=8, max_length=100, write_only=True)
    total_price = serializers.IntegerField()

    class Meta:
        model = Payment
        fields = ['id', 'card', 'token', 'user']

    def create(self, validated_data):
        token = validated_data.pop('token')
        order = Payment.objects.create(**validated_data)
        order.user = self.context.get('user_id')
        total_price = validated_data.get('total_price')
        order.save()
        try:
            stripe.api_key = settings.STRIPE_PUBLIC_KEY
            intent = stripe.Charge.create(
                amount=total_price,
                currency='usd',
                source=token,
                description='Example charge'
        )
        except stripe.error.CardError as e:
            raise serializers.ValidationError({"error":e.user_message})
        return order


class CardsSerializer(serializers.Serializer):
    card_token = serializers.CharField(max_length=100, write_only=True)
    email = serializers.CharField(max_length=100, write_only=True)

    class Meta:
        model = Cards
        fields = ['id', 'user', 'card_number', 'cvv', 'card_date', 'zip_code', 'custumer', 'email', 'description', 'card_token']

    def create(self, validated_data):
        card_token = validated_data.pop('card_token')
        order = Cards.objects.create(**validated_data)
        order.user = self.context.get('user_id')
        order.save()
        stripe.api_key = settings.STRIPE_PUBLIC_KEY
        customer = stripe.Customer.create(email=validated_data.get('email'))
        order.custumer = customer.id
        order.save()
        stripe.Customer.create_source(customer.id, source=card_token)
        return order


class PaymentCardSerializers(serializers.ModelSerializer):
    card_token = serializers.CharField(max_length=100, write_only=True)

    class Meta:
        model = PaymentCards
        fields = ['id', 'user', 'amount', 'currency', 'customer', 'source', 'description', 'card_token']
    
    def create(self, validated_data):
        custumer = self.context.get('custumer')
        card_token = validated_data.pop('card_token')
        payment = PaymentCards.objects.create(**validated_data)
        payment.user = self.context.get('user_id')
        payment.save()
        stripe.api_key = settings.STRIPE_PUBLIC_KEY
        charge = stripe.Charge.create(
            amount=int(validated_data.get('amount')),  # Amount in cents
            currency=validated_data.get('currency'),
            customer="cus_PY8hmuRWHRdNnP",
            source=card_token,  # ID of the saved card
            description=validated_data.get('description')
        )
        return payment