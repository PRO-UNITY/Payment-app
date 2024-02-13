from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from drf_yasg.utils import swagger_auto_schema
from django.conf import settings
import stripe
from payment.models import Cards
from payment.serializers import CardsSerializer, PaymentSerializer, PaymentCardSerializers
from payment.microservice import user_permission


class PaymentView(APIView):
    @user_permission
    @swagger_auto_schema(request_body=PaymentSerializer)
    def post(self, request, user_id=None):
        if user_id is None:
            return Response({"error": "Invalid user data"}, status=status.HTTP_401_UNAUTHORIZED)
        serializers = PaymentSerializer(data=request.data, context={"user_id": user_id})
        if serializers.is_valid(raise_exception=True):
            instance = serializers.save()
            return Response(serializers.data, status=status.HTTP_201_CREATED)
        return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)



class CardViews(APIView):
    @user_permission
    def get(self, request, user_id=None):
        if user_id is None:
            return Response({"error": "Invalid user data"}, status=status.HTTP_401_UNAUTHORIZED)
        user = Cards.objects.filter(user=user_id)[0]
        stripe.api_key = settings.STRIPE_PUBLIC_KEY
        cards = stripe.Customer.list_sources(user.custumer, object='card')
        list_card = []
        for  item in cards:
            list_card.append({'id': item.id, 'brand': item.brand, 'last4': item.last4, 'exp_month': item.exp_month, 'exp_yaer': item.exp_year})
        return Response(list_card, status=status.HTTP_200_OK)

    @user_permission
    @swagger_auto_schema(request_body=CardsSerializer)
    def post(self, request, user_id=None):
        if user_id is None:
            return Response({"error": "Invalid user data"}, status=status.HTTP_401_UNAUTHORIZED)
        serializers = CardsSerializer(data=request.data, context={"user_id": user_id})
        if serializers.is_valid(raise_exception=True):
            serializers.save()
            return Response(serializers.data, status=status.HTTP_201_CREATED)
        return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)


class PaymentCardView(APIView):
    @user_permission
    @swagger_auto_schema(request_body=PaymentCardSerializers)
    def post(self, request, user_id=None):
        if user_id is None:
            return Response({"error": "Invalid user data"}, status=status.HTTP_401_UNAUTHORIZED)
        custumer = Cards.objects.filter(user=user_id)[0]
        serializers = PaymentCardSerializers(data=request.data, context={"user_id": user_id, 'custumer':custumer.custumer, 'card_id': custumer.card_id})
        if serializers.is_valid(raise_exception=True):
            serializers.save()
            return Response(serializers.data, status=status.HTTP_201_CREATED)
        return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)


class CardDelete(APIView):
    @user_permission
    def delete(self, request, pk, user_id=None):
        if user_id is None:
            return Response({"error": "Invalid user data"}, status=status.HTTP_401_UNAUTHORIZED)
        custumer = Cards.objects.get(id=pk)
        deleted_card = stripe.Customer.retrieve_source(custumer.custumer, custumer.card_id)
        deleted_card.delete()
        custumer.delete()
        return Response({'message': 'delete success'}, status=status.HTTP_400_BAD_REQUEST)
