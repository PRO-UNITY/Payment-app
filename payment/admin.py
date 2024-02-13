from django.contrib import admin
from payment.models import Cards, Payment, PaymentCards

admin.site.register(Cards)
admin.site.register(Payment)
admin.site.register(PaymentCards)