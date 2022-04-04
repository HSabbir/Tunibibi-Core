from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from django.contrib.auth.models import Group, User


def customer_only(view_func):
    def wrapper_func(request, *args, **kwargs):
        if User.objects.filter(username=request.user.username, groups__name='Customer').exists():
            return view_func(request, *args, **kwargs)
        else:
            return JsonResponse({
                'code': 400,
                'message': 'Request not permitted!'
            }, safe=False)

    return wrapper_func


def seller_only(view_func):
    def wrapper_func(request, *args, **kwargs):
        if User.objects.filter(username=request.user.username, groups__name='Seller').exists():
            return view_func(request, *args, **kwargs)
        else:
            return JsonResponse({
                'code': 400,
                'message': 'Request not permitted!'
            }, safe=False)

    return wrapper_func

def buyer_only(view_func):
    def wrapper_func(request, *args, **kwargs):
        if User.objects.filter(username=request.user.username, groups__name='Buyer').exists():
            return view_func(request, *args, **kwargs)
        else:
            return JsonResponse({
                'code': 400,
                'message': 'Request not permitted!'
            }, safe=False)

    return wrapper_func

def buyer_or_customer(view_func):
    def wrapper_func(request, *args, **kwargs):
        if User.objects.filter(username=request.user.username, groups__name='Customer').exists() or \
                User.objects.filter(username=request.user.username, groups__name='Buyer').exists():
            return view_func(request, *args, **kwargs)
        else:
            return JsonResponse({
                'code': 400,
                'message': 'Request not permitted!'
            }, safe=False)

    return wrapper_func