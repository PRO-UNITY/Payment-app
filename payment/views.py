from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.conf import settings
import stripe
from django.views.decorators.csrf import csrf_exempt
from stripe.error import InvalidRequestError
from payment.models import UserPayment
from payment.microservice import user_permission
from payment.serializers import PaymentSerializers
from payment.pagination import StandardResultsSetPagination
from payment.pagination import Pagination


class ProductPageView(APIView):
    @csrf_exempt
    def post(self, request):
        product = request.data['product']
        stripe.api_key = settings.STRIPE_SECRET_KEY
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[
                {
                    'price': f"{product}",
                    'quantity': 1,
                },
            ],
            mode='payment',
            customer_creation='always',
            success_url=settings.REDIRECT_DOMAIN + '/payment_successful?session_id={CHECKOUT_SESSION_ID}',
            cancel_url=settings.REDIRECT_DOMAIN + '/payment_cancelled',
        )
        return Response({'url': checkout_session.url}, status=status.HTTP_200_OK)


class PaymentSuccessfulView(APIView):
    def post(self, request):
        stripe.api_key = settings.STRIPE_SECRET_KEY
        checkout_session_id = request.data['session_id']

        if not checkout_session_id:
            return Response({"error": "No session_id provided"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            session = stripe.checkout.Session.retrieve(checkout_session_id)
            customer = stripe.Customer.retrieve(session.customer)
            payment = UserPayment.objects.get_or_create(session_id=checkout_session_id, customer=customer.id, email=customer.email, name=customer.name)
            return Response({"message": customer}, status=status.HTTP_200_OK)
        except InvalidRequestError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class AllPaymentViews(APIView, Pagination):
    pagination_class = StandardResultsSetPagination
    serializer_class = PaymentSerializers

    @user_permission
    def get(self, request, user_id=None):
        if user_id is None:
            return Response({"error": "Invalid user data"}, status=status.HTTP_401_UNAUTHORIZED)
        objects_list= UserPayment.objects.all().order_by('-id')
        page = self.paginate_queryset(objects_list)
        if page is not None:
            serializer = self.get_paginated_response(self.serializer_class(page, many=True).data)
        else:
            serializer = self.serializer_class(objects_list, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
