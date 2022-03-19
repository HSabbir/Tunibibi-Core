from seller.models import *
from rest_framework import serializers


class RewardSerializer(serializers.Serializer):
    mobile_number = serializers.CharField(max_length=20)
    point = serializers.IntegerField()
    rank = serializers.IntegerField()
