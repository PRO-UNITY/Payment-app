from django.db import models
from django.contrib.auth.models import User


class Payment(models.Model):
    user = models.IntegerField(null=True, blank=True)
    total_price = models.CharField(max_length=250, null=True, blank=True)
    card = models.CharField(max_length=250, null=True, blank=True)
    create_at = models.DateTimeField(auto_now_add=True)


class Cards(models.Model):
    user = models.IntegerField(null=True, blank=True)
    card_id = models.CharField(max_length=250, null=True, blank=True)
    card_number = models.CharField(max_length=50, null=True, blank=True)
    cvv = models.IntegerField(null=True, blank=True)
    card_date = models.CharField(max_length=100, null=True, blank=True)
    zip_code= models.IntegerField(null=True, blank=True)
    custumer = models.CharField(max_length=250, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    description = models.CharField(max_length=255, null=True, blank=True)
    create_at = models.DateTimeField(auto_now_add=True)


class PaymentCards(models.Model):
    user = models.IntegerField(null=True, blank=True)
    amount = models.CharField(max_length=250, null=True, blank=True)
    currency = models.CharField(max_length=100, null=True, blank=True)
    customer = models.CharField(max_length=250, null=True, blank=True)
    source = models.CharField(max_length=250, null=True, blank=True)
    description = models.CharField(max_length=250, null=True, blank=True)
    create_at = models.DateTimeField(auto_now_add=True)