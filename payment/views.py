from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from drf_yasg.utils import swagger_auto_schema
from django.conf import settings
import stripe
import time
from django.shortcuts import render, redirect
from django.http import HttpResponse
from rest_framework.decorators import api_view
from payment.models import Cards
from payment.serializers import CardsSerializer, PaymentSerializer, PaymentCardSerializers
from payment.microservice import user_permission
from stripe.error import SignatureVerificationError
from django.views.decorators.csrf import csrf_exempt




@csrf_exempt
def product_page(request):
	stripe.api_key = settings.STRIPE_PUBLIC_KEY
	if request.method == 'POST':
		checkout_session = stripe.checkout.Session.create(
			payment_method_types = ['card'],
			line_items = [
				{
					'price': "price_1OjdD9LZ26NOlTGBKDD4aCuZ",
					'quantity': 1,
				},
			],
			mode = 'payment',
			customer_creation = 'always',
			success_url = settings.REDIRECT_DOMAIN + '/payment_successful?session_id={CHECKOUT_SESSION_ID}',
			cancel_url = settings.REDIRECT_DOMAIN + '/payment_cancelled',
		)
		return redirect(checkout_session.url, code=303)
	return render(request, 'product_page.html')


## use Stripe dummy card: 4242 4242 4242 4242
def payment_successful(request):
	stripe.api_key = settings.STRIPE_PUBLIC_KEY
	checkout_session_id = request.GET.get('session_id', None)
	session = stripe.checkout.Session.retrieve(checkout_session_id)
	customer = stripe.Customer.retrieve(session.customer)
	return render(request, 'payment_successful.html', {'customer': customer})


def payment_cancelled(request):
	stripe.api_key = settings.STRIPE_PUBLIC_KEY
	return render(request, 'payment_cancelled.html')


@csrf_exempt
def stripe_webhook(request):
	stripe.api_key = settings.STRIPE_PUBLIC_KEY
    
	time.sleep(10)
	payload = request.body
	signature_header = request.META['HTTP_STRIPE_SIGNATURE']
	event = None
	try:
		event = stripe.Webhook.construct_event(
			payload, signature_header, settings.STRIPE_WEBHOOK_SECRET_TEST
		)
	except ValueError as e:
		return HttpResponse(status=400)
	except stripe.error.SignatureVerificationError as e:
		return HttpResponse(status=400)
	if event['type'] == 'checkout.session.completed':
		session = event['data']['object']
		session_id = session.get('id', None)
		time.sleep(15)
	return HttpResponse(status=200)






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
        stripe.api_key = settings.STRIPE_PUBLIC_KEY
        deleted_card = stripe.Customer.retrieve_source(custumer.custumer, custumer.card_id)
        deleted_card.delete()
        custumer.delete()
        return Response({'message': 'delete success'}, status=status.HTTP_400_BAD_REQUEST)


class WebHooks(APIView):

    def post(self, request):
        
        payload = request.body
        sig_header = request.headers.get('Stripe-Signature')

        try:
            event = stripe.Webhook.construct_event(
                payload, sig_header, "we_1OjJAxLZ26NOlTGBTsM2AwDA"
            )
        except ValueError as e:
            # Invalid payload
            return Response({'error': 'Invalid payload'}, status=400)
        except stripe.error.SignatureVerificationError as e:
            # Invalid signature
            return Response({'error': 'Invalid signature'}, status=400)

        # Handle the event
        if event['type'] == 'payment_intent.succeeded':
            # Handle successful payment
            # You can retrieve the payment intent ID from event['data']['object']['id']
            pass
        elif event['type'] == 'payment_intent.payment_failed':
            # Handle failed payment
            # You can retrieve the payment intent ID from event['data']['object']['id']
            pass
        # Handle other event types as needed

        # Respond to the webhook with a success message
        return Response({'message': 'Webhook received successfully'}, status=200)




# @api_view(['GET'])
# def stripe_config(request):
#     if request.method == 'GET':
#         stripe_config = {'publicKey': settings.STRIPE_PUBLIC_KEY}
#         return Response(stripe_config)


# @api_view(['GET'])
# def create_checkout_session(request):
#     if request.method == 'GET':
#         domain_url = 'http://127.0.0.1:8000/'
#         stripe.api_key = settings.STRIPE_SECRET_KEY
#         try:
#             checkout_session = stripe.checkout.Session.create(
#                 success_url=domain_url + 'success?session_id={CHECKOUT_SESSION_ID}',
#                 cancel_url=domain_url + 'cancelled/',
#                 payment_method_types=['card'],
#                 mode='payment',
#                 line_items=[
#                     {
#                         'name': 'T-shirt',
#                         'quantity': 1,
#                         'currency': 'usd',
#                         'amount': '2000',
#                     }
#                 ]
#             )
#             return Response({'sessionId': checkout_session['id']})
#         except Exception as e:
#             return Response({'error': str(e)}, status=400)


# @api_view(['POST'])
# def stripe_webhook(request):
#     endpoint_secret = "whsec_add8cadbbd6f0f09c55a770ad800ba1d7d078ac20da21688435c24da55ad7062"
#     payload = request.body
#     sig_header = request.headers['STRIPE_SIGNATURE']
    
#     if sig_header is None:
#         # Return a 400 Bad Request response if signature header is missing
#         return Response({'error': 'Stripe signature header missing'}, status=400)

#     try:
#         event = stripe.Webhook.construct_event(
#             payload, sig_header, endpoint_secret
#         )
#     except ValueError as e:
#         # Invalid payload
#         return Response({'error': 'Invalid payload'}, status=400)
#     except SignatureVerificationError as e:
#         # Invalid signature
#         return Response({'error': 'Invalid signature'}, status=400)

#     # Handle the checkout.session.completed event
#     if event['type'] == 'checkout.session.completed':
#         print("Payment was successful.")
#         # TODO: run some custom code here

#     return Response(status=200)


    