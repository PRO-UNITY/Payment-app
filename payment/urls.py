from django.urls import path
from payment.views import *


urlpatterns = [
    path('payment', ProductPageView.as_view()),
    path('payment_successful', PaymentSuccessfulView.as_view()),
    path('payments', AllPaymentViews.as_view()),
]