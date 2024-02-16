from django.db import models


class UserPayment(models.Model):
	session_id = models.CharField(max_length=500, null=True, blank=True, unique = True)
	customer = models.CharField(max_length=250, null=True, blank=True)
	email = models.CharField(max_length=250, null=True, blank=True)
	name = models.CharField(max_length=250, null=True, blank=True)
	create_at = models.DateTimeField(auto_now_add=True)
