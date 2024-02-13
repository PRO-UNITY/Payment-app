from django.urls import path
from payment.views import PaymentView, CardViews, PaymentCardView, CardDelete, WebHooks


urlpatterns = [
    path('payment', PaymentView.as_view()),
    path('cards', CardViews.as_view()),
    path('paytment/card', PaymentCardView.as_view()),
    path('card/delete/<int:pk>', CardDelete.as_view()),
    path('web_hooks', WebHooks.as_view()),
]