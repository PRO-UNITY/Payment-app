from django.urls import path
from payment.views import PaymentView, CardViews, PaymentCardView, CardDelete, WebHooks, stripe_config, create_checkout_session, stripe_webhook


urlpatterns = [
    path('payment', PaymentView.as_view()),
    path('cards', CardViews.as_view()),
    path('paytment/card', PaymentCardView.as_view()),
    path('card/delete/<int:pk>', CardDelete.as_view()),
    path('web_hooks', WebHooks.as_view()),

    path('stripe_config', stripe_config),
    path('create_checkout_session', create_checkout_session),
    path('stripe_webhook', stripe_webhook),
]