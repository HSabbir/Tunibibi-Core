from django.db import models
from django.contrib.auth.models import User


class CustomerInfo(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='customer_auth', null=True, blank=True)
    name = models.CharField(max_length=200, null=True, blank=True)
    country = models.CharField(max_length=200, null=True, blank=True)
    mobile_number = models.CharField(max_length=20)
    address = models.TextField(null=True)
    city = models.TextField(null=True)
    postcode = models.TextField(null=True)
    reg_ip = models.GenericIPAddressField(null=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return str(self.user)



