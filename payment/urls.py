from django.urls import path
from payment.views import *


urlpatterns = [
    path('payment', PaymentView.as_view()),
    path('cards', CardViews.as_view()),
    path('paytment/card', PaymentCardView.as_view()),
    path('card/delete/<int:pk>', CardDelete.as_view()),
    path('web_hooks', WebHooks.as_view()),

    # path('stripe_config', stripe_config),
    # path('create_checkout_session', create_checkout_session),
    # path('stripe_webhook', stripe_webhook),


    path('product_page', product_page, name='product_page'),
	path('payment_successful', payment_successful, name='payment_successful'),
	path('payment_cancelled', payment_cancelled, name='payment_cancelled'),
	path('stripe_webhook', stripe_webhook, name='stripe_webhook'),
]