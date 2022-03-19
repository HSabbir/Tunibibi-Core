import datetime
import json
import os
import random
import string

from .models import *
from django.shortcuts import render, HttpResponseRedirect, reverse
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken, UntypedToken
from rest_framework_simplejwt.authentication import JWTAuthentication

from django.db.models import Q
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from django.contrib.auth.hashers import check_password
from datetime import timedelta, datetime

from django.contrib import messages
from django.contrib.auth.models import Group

import requests
import api.helper

import api.helper
from .serializers import *
from .decorators import *

from .businessLogic import *

from django.contrib.auth.models import Permission
from django.utils.text import slugify
from django.conf import settings
from django.core.files.base import ContentFile
import base64
