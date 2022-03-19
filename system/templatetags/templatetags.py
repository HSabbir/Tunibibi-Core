from django import template
from system.models import *
import json
from django.contrib import messages
from django.core import serializers

register = template.Library()


@register.simple_tag
def get_app_name():
    return Settings.objects.all().last().app_name


@register.simple_tag
def get_app_icon():
    return Settings.objects.all().last().favicon.url


@register.simple_tag
def get_app_logo():
    return Settings.objects.all().last().logo.url


@register.simple_tag
def get_parent_category_name(category_id):
    if category_id != 0:
        return Category.objects.get(id=category_id).name
    else:
        return 'N/A'
