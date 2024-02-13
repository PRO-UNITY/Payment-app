# views.py
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from drf_yasg.utils import swagger_auto_schema
from payment.models import Payment, Cards
from django.contrib.auth.models import User
from django.conf import settings
import stripe
from payment.serializers import CardsSerializer, PaymentSerializer, PaymentCardSerializers
from payment.renderers import UserRenderers



def get_token_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {"refresh": str(refresh), "access": str(refresh.access_token)}

class PaymentView(APIView):
    render_classes = [UserRenderers]
    perrmisson_class = [IsAuthenticated]

    @swagger_auto_schema(request_body=PaymentSerializer)
    def post(self, request):
        serializers = PaymentSerializer(data=request.data, context={"user_id": request.user})
        if serializers.is_valid(raise_exception=True):
            serializers.save()
            return Response(serializers.data, status=status.HTTP_201_CREATED)
        return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)


class CardViews(APIView):
    render_classes = [UserRenderers]
    perrmisson_class = [IsAuthenticated]

    def get(self, request):
        user = Cards.objects.filter(user=request.user.id)[0]
        stripe.api_key = settings.STRIPE_PUBLIC_KEY
        cards = stripe.Customer.list_sources(
            user.custumer,
            object='card'
        )
        list_card = []
        for  item in cards:
            list_card.append({'id': item.id, 'brand': item.brand, 'last4': item.last4, 'exp_month': item.exp_month, 'exp_yaer': item.exp_year})
        return Response(list_card, status=status.HTTP_200_OK)

    @swagger_auto_schema(request_body=CardsSerializer)
    def post(self, request):
        serializers = CardsSerializer(data=request.data, context={"user_id": request.user})
        if serializers.is_valid(raise_exception=True):
            serializers.save()
            return Response(serializers.data, status=status.HTTP_201_CREATED)
        return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)


class PaymentCardView(APIView):
    render_classes = [UserRenderers]
    perrmisson_class = [IsAuthenticated]

    @swagger_auto_schema(request_body=PaymentCardSerializers)
    def post(self, request):
        custumer = Cards.objects.filter(user=request.user.id)[0]
        serializers = PaymentCardSerializers(data=request.data, context={"user_id": request.user, 'custumer':custumer})
        if serializers.is_valid(raise_exception=True):
            serializers.save()
            return Response(serializers.data, status=status.HTTP_201_CREATED)
        return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)
