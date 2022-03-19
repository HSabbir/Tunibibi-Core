import uuid
import os
from django.conf import settings
from datetime import datetime
from django.contrib.auth.models import Group


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def get_client_host(request):
    hostname = request.META.get('SERVER_NAME')
    return hostname
