from django.shortcuts import render
from rest_framework.decorators import api_view, parser_classes, permission_classes, authentication_classes
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from system.models import *
from .serializers import *
from rest_framework.response import Response
from rest_framework import status
import requests
import json
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from datetime import datetime as dt
import datetime
from datetime import timedelta
import pytz


def get_dial_code(country):
    try:
        url = "https://countriesnow.space/api/v0.1/countries/codes"
        payload = json.dumps({
            "country": Country.objects.get(id=country).name
        })
        headers = {
            'Content-Type': 'application/json'
        }
        response = requests.request("GET", url, headers=headers, data=payload)
        response = json.loads(response.text)
        if not response['error']:
            return response['data']['dial_code']
    except Exception:
        return ''


@api_view(['POST'])
def sellerRegistration(request):
    try:
        seller_registration_serializer = SellerRegistrationSerializer(data=request.data)
        if seller_registration_serializer.is_valid():
            if User.objects.filter(email=seller_registration_serializer.validated_data.get('email')).exists():
                return Response({
                    'code': status.HTTP_400_BAD_REQUEST,
                    'message': 'Seller already exists with the provided email.'
                })
            else:
                password = seller_registration_serializer.validated_data.pop('password')
                seller_instance = seller_registration_serializer.save()
                try:
                    user_instance = User.objects.create_user(
                        username=seller_instance.email,
                        email=seller_instance.email,
                        first_name=seller_instance.name,
                        password=password
                    )
                    seller_instance.user = user_instance
                    seller_instance.save()
                except Exception:
                    seller_instance.delete()
                return Response({
                    'code': status.HTTP_200_OK,
                    'message': 'Seller registration completed successfully.',
                    'data': SellerDataSerializer(seller_instance, context={"request": request}).data
                })
        else:
            return Response(seller_registration_serializer.errors)
    except Exception as e:
        return Response({
            'code': status.HTTP_400_BAD_REQUEST,
            'message': str(e)
        })


@api_view(['GET'])
def getCountryList(request):
    try:
        return Response({
            'code': status.HTTP_200_OK,
            'message': 'Country list retrieved successfully.',
            'data': CountrySerializer(Country.objects.filter(status=True), many=True).data
        })
    except Exception as e:
        return Response({
            'code': status.HTTP_400_BAD_REQUEST,
            'message': str(e)
        })


@api_view(['POST'])
def getCityList(request):
    try:
        country = request.data.get('country')
        if Country.objects.filter(id=country, status=True).exists():
            return Response({
                'code': status.HTTP_200_OK,
                'message': 'City list retrieved successfully.',
                'data': {
                    'country': CountrySerializer(Country.objects.filter(id=country, status=True), many=True).data,
                    'cities': CitySerializer(City.objects.filter(country_id=country, status=True), many=True).data
                }})
        return Response({
            'code': status.HTTP_400_BAD_REQUEST,
            'message': 'Invalid country id'
        })
    except Exception as e:
        return Response({
            'code': status.HTTP_400_BAD_REQUEST,
            'message': str(e)
        })


@api_view(['GET'])
def getCategoryList(request):
    try:
        category_list = []
        parent_category_list = Category.objects.filter(status=True, parent_category=0).order_by('order_sequence')
        for parent in parent_category_list:
            parent_data = CategorySerializer(parent, context={"request": request}).data
            sub_category = Category.objects.filter(parent_category=parent.id, status=True).order_by('name')
            sub_data = []
            for sub in sub_category:
                sub_data.append(SubCategorySerializer(sub, context={"request": request}).data)
            category_list.append({
                'parent': parent_data,
                'sub': sub_data
            })
        return Response({
            'code': status.HTTP_200_OK,
            'message': 'Category list retrieved successfully.',
            'data': category_list
        })
    except Exception as e:
        return Response({
            'code': status.HTTP_400_BAD_REQUEST,
            'message': str(e)
        })


@api_view(['POST'])
def userRegistration(request):
    try:
        user_registration_serializer = UserRegistrationSerializer(data=request.data)
        if user_registration_serializer.is_valid():
            if User.objects.filter(email=user_registration_serializer.validated_data.get('email')).exists():
                return Response({
                    'code': status.HTTP_400_BAD_REQUEST,
                    'message': 'User already exists with the provided email.'
                })
            else:
                password = user_registration_serializer.validated_data.pop('password')
                user_instance = user_registration_serializer.save()
                try:
                    user_acc_instance = User.objects.create_user(
                        username=user_instance.email,
                        email=user_instance.email,
                        first_name=user_instance.name,
                        password=password
                    )
                    user_instance.user = user_acc_instance
                    user_instance.save()
                except Exception:
                    user_instance.delete()
                return Response({
                    'code': status.HTTP_200_OK,
                    'message': 'User registration completed successfully.',
                    'data': UserDataSerializer(user_instance, context={"request": request}).data
                })
        else:
            return Response(user_registration_serializer.errors)
    except Exception as e:
        return Response({
            'code': status.HTTP_400_BAD_REQUEST,
            'message': str(e)
        })


@api_view(['POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def liveStreamCreate(request):
    try:
        live_create_serializer = LiveStreamCreateSerializer(data=request.data)
        if live_create_serializer.is_valid():
            naive = dt.now()
            timezone = pytz.timezone("Asia/Dhaka")
            aware1 = naive.astimezone(timezone)
            aware2 = live_create_serializer.validated_data.get('schedule_datetime').astimezone(timezone)
            schedule_time = aware2.strftime('%Y-%m-%d %H:%M:%S%z')
            current_time = aware1.strftime('%Y-%m-%d %H:%M:%S%z')
            if schedule_time <= current_time:
                return Response({
                    'code': status.HTTP_400_BAD_REQUEST,
                    'message': 'Live stream can not be created for older date and time.'
                })
            live_instance = live_create_serializer.save()
            live_instance.user = request.user
            live_instance.end_datetime = live_instance.schedule_datetime + timedelta(minutes=live_instance.duration)
            live_instance.save()
            LiveStreamStatistics.objects.create(
                live=live_instance,
                views=0,
                reaction=0,
                comments=0
            )
            return Response({
                'code': status.HTTP_200_OK,
                'message': 'Live stream scheduled successfully.',
                'data': LiveStreamDataSerializer(live_instance, context={"request": request}).data
            })
        else:
            return Response(live_create_serializer.errors)
    except Exception as e:
        return Response({
            'code': status.HTTP_400_BAD_REQUEST,
            'message': str(e)
        })


@api_view(['POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def liveStreamFilter(request):
    try:
        naive = dt.now()
        timezone = pytz.timezone("Asia/Dhaka")
        aware1 = naive.astimezone(timezone)
        if 'category' in request.POST and request.POST['category'] != "" and 'seller_id' in request.POST and \
                request.POST['seller_id'] != "":
            live_stream_list = LiveStreaming.objects.filter(
                end_datetime__gte=aware1,
                user__seller__id=request.POST['seller_id'],
                category_id=request.POST['category']).order_by('-schedule_datetime')
        elif 'category' in request.POST and request.POST['category'] != "":
            live_stream_list = LiveStreaming.objects.filter(
                end_datetime__gte=aware1,
                category_id=request.POST['category']).order_by('-schedule_datetime')
        elif 'seller_id' in request.POST and request.POST['seller_id'] != "":
            live_stream_list = LiveStreaming.objects.filter(
                end_datetime__gte=aware1,
                user__seller__id=request.POST['seller_id']).order_by('-schedule_datetime')
        else:
            live_stream_list = []
        return Response({
            'code': status.HTTP_200_OK,
            'message': 'Live stream list retrieved successfully.',
            'data': LiveStreamDataSerializer(live_stream_list, many=True).data
        })
    except Exception as e:
        return Response({
            'code': status.HTTP_400_BAD_REQUEST,
            'message': str(e)
        })


@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def liveStreamAll(request):
    try:
        naive = dt.now()
        timezone = pytz.timezone("Asia/Dhaka")
        aware1 = naive.astimezone(timezone)
        live_stream_list = LiveStreaming.objects.filter(end_datetime__gte=aware1).order_by('-schedule_datetime')
        return Response({
            'code': status.HTTP_200_OK,
            'message': 'Live stream list retrieved successfully.',
            'data': LiveStreamDataSerializer(live_stream_list, many=True).data
        })
    except Exception as e:
        return Response({
            'code': status.HTTP_400_BAD_REQUEST,
            'message': str(e)
        })


@api_view(['POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def liveStreamStats(request):
    try:
        live_stream_stat = LiveStreamStatistics.objects.filter(live_id=request.POST['live_id'])
        return Response({
            'code': status.HTTP_200_OK,
            'message': 'Live stream stat retrieved successfully.',
            'data': LiveStreamStatReadSerializer(live_stream_stat, many=True).data
        })
    except Exception as e:
        return Response({
            'code': status.HTTP_400_BAD_REQUEST,
            'message': str(e)
        })


@api_view(['POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def liveStreamStatsUpdate(request):
    try:
        live_stream_stats = LiveStreamStatUpdateSerializer(data=request.data)
        if live_stream_stats.is_valid():
            if LiveStreamStatistics.objects.filter(live_id=live_stream_stats.validated_data.get('live')).exists():
                stat_instance = live_stream_stats.update(
                    instance=LiveStreamStatistics.objects.get(live_id=live_stream_stats.validated_data.get('live')),
                    validated_data=live_stream_stats.validated_data)
            else:
                stat_instance = live_stream_stats.save()
            return Response({
                'code': status.HTTP_200_OK,
                'message': 'Live stream stat updated successfully.',
                'data': LiveStreamStatReadSerializer(stat_instance).data
            })
        else:
            return Response(live_stream_stats.errors)
    except Exception as e:
        return Response({
            'code': status.HTTP_400_BAD_REQUEST,
            'message': str(e)
        })
