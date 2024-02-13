from django.urls import path
from payment.views import PaymentView, CardViews, PaymentCardView


urlpatterns = [
    path('payment', PaymentView.as_view()),
    path('cards', CardViews.as_view()),
    path('paytment/card', PaymentCardView.as_view())

]