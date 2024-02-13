from rest_framework import serializers
from payment.models import Cards, Payment, PaymentCards
from django.conf import settings
import stripe


class PaymentSerializer(serializers.Serializer):
    token = serializers.CharField(min_length=8, max_length=100, write_only=True)
    total_price = serializers.CharField(max_length=100, write_only=True)

    class Meta:
        model = Payment
        fields = ['id', 'card', 'token', 'user', 'total_price']

    def create(self, validated_data):
        token = validated_data.pop('token')
        total_price = validated_data.get('total_price')
        order = Payment.objects.create(**validated_data)
        order.user = self.context.get('user_id')
        order.save()
        try:
            stripe.api_key = settings.STRIPE_PUBLIC_KEY
            intent = stripe.Charge.create(
                amount=int(total_price),
                currency='usd',
                source=token,
                description='Example charge'
        )
            return order
        except stripe.error.CardError as e:
            raise serializers.ValidationError({"error":e.user_message})


class CardsSerializer(serializers.ModelSerializer):
    card_token = serializers.CharField(max_length=100, write_only=True)
    email = serializers.CharField(max_length=100, write_only=True)

    class Meta:
        model = Cards
        fields = ['id', 'user', 'card_id', 'card_number', 'cvv', 'card_date', 'zip_code', 'custumer', 'email', 'description', 'card_token']

    def create(self, validated_data):
        card_token = validated_data.pop('card_token')
        email = validated_data.pop('email')
        user_id = self.context.get('user_id')
        card = Cards.objects.create(**validated_data, user_id=user_id)
        stripe.api_key = settings.STRIPE_SECRET_KEY
        customer = stripe.Customer.create(email=email)
        stripe_card = stripe.Customer.create_source(customer.id, source=card_token)
        card.card_id = stripe_card.id
        card.custumer = customer.id
        card.save()
        return card


class PaymentCardSerializers(serializers.ModelSerializer):

    class Meta:
        model = PaymentCards
        fields = ['id', 'user', 'amount', 'currency', 'customer', 'source', 'description']
    
    def create(self, validated_data):
        custumer = self.context.get('custumer')
        card_id = self.context.get('card_id')
        payment = PaymentCards.objects.create(**validated_data)
        payment.user = self.context.get('user_id')
        payment.customer = custumer
        payment.source = card_id
        payment.save()
        stripe.api_key = settings.STRIPE_PUBLIC_KEY
        charge = stripe.Charge.create(
            amount=int(validated_data.get('amount')),
            currency=validated_data.get('currency'),
            customer=custumer,
            source=card_id,
            description=validated_data.get('description')
        )
        return payment