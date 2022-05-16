import copy

from rest_framework.decorators import parser_classes
from rest_framework.parsers import MultiPartParser

from .importFile import  *

@api_view(['POST'])
def checkExistingMobileNumber(request):
    try:
        payload = request.data
        request_serializer = ShopInfoSerializer(data=payload)
        if request_serializer.is_valid():
            mobile_number = request_serializer.validated_data.get('mobile_number')
            if User.objects.filter(username__icontains=mobile_number).exists() or ShopInfo.objects.filter(
                    mobile_number__icontains=mobile_number).exists():
                return Response({
                    'code': status.HTTP_200_OK,
                    'message': 'A shop with this mobile number already exists.',
                    'data': {
                        'mobile_number': mobile_number,
                        'existing_number': True
                    }
                })
            else:
                return Response({
                    'code': status.HTTP_200_OK,
                    'message': 'No shop account found with this mobile number.',
                    'data': {
                        'mobile_number': mobile_number,
                        'existing_number': False
                    }
                })
        else:
            return Response(request_serializer.errors)
    except Exception as e:
        return Response({
            "code": status.HTTP_400_BAD_REQUEST,
            "message": str(e)
        })


@api_view(['POST'])
def setPassword(request):
    try:
        payload = request.data
        request_serializer = PasswordInputValidator(data=payload,)
        if request_serializer.is_valid():
            business_country = request_serializer.validated_data.get('business_country')
            mobile_number = request_serializer.validated_data.get('mobile_number')
            pass1 = request_serializer.validated_data.get('password1')
            pass2 = request_serializer.validated_data.get('password2')

            if pass1 != pass2:
                return Response({
                    'code': status.HTTP_400_BAD_REQUEST,
                    'message': 'Your passwords did not match!'
                })

            if User.objects.filter(username__icontains=mobile_number).exists():
                if ShopInfo.objects.filter(mobile_number__icontains=mobile_number).exists():
                    return Response({
                        'code': status.HTTP_400_BAD_REQUEST,
                        'message': 'A user this mobile number already exists.',
                        'data': {
                            'mobile_number': mobile_number,
                            'existing_number': True
                        }
                    })
                else:
                    user = User.objects.get(username=mobile_number)
                    shop = ShopInfo.objects.create(
                        user=user,
                        mobile_number=mobile_number,
                        business_country=business_country  # edited
                    )
                    shop.save()

                    groups, created = Group.objects.get_or_create(name='Seller')
                    groups.user_set.add(user)

                    updatePoints(user, payload["invitation_code"], business_country,"Seller")
                    return Response({
                        'code': status.HTTP_200_OK,
                        'message': 'Your password has been set successfully.'
                    })
            else:
                user_instance = User.objects.create(
                    username=mobile_number
                )
                user_instance.set_password(pass2)
                user_instance.save()

                groups, created = Group.objects.get_or_create(name='Seller')
                groups.user_set.add(user_instance)

                shop = ShopInfo.objects.create(
                        user=user_instance,
                        mobile_number=mobile_number,
                        business_country=business_country  # edited
                    )
                shop.save

                updatePoints(user_instance, payload["invitation_code"], business_country,"Seller")

                return Response({
                    'code': status.HTTP_200_OK,
                    'message': 'Your password has been set successfully.'
                })
        else:
            return Response(request_serializer.errors)
    except Exception as e:
        return Response({
            "code": status.HTTP_400_BAD_REQUEST,
            "message": str(e)
})


@api_view(['POST'])
def createBuyerAccount(request):
    try:
        payload = request.data
        request_serializer = BuyerAccountValidator(data=payload,)
        if request_serializer.is_valid():
            business_country = request_serializer.validated_data.get('business_country')
            mobile_number = request_serializer.validated_data.get('mobile_number')
            pass1 = request_serializer.validated_data.get('password1')

            if User.objects.filter(username__icontains=mobile_number).exists():
                if BuyerInfo.objects.filter(mobile_number__icontains=mobile_number).exists():
                    return Response({
                        'code': status.HTTP_400_BAD_REQUEST,
                        'message': 'A Buyer User with this mobile number already exists.',
                        'data': {
                            'mobile_number': mobile_number,
                            'existing_number': True
                        }
                    })
                else:
                    user = User.objects.get(username=mobile_number)
                    buyer = BuyerInfo.objects.create(
                        user=user,
                        mobile_number=mobile_number,
                        country=business_country  # edited
                    )
                    groups, created = Group.objects.get_or_create(name='Buyer')
                    groups.user_set.add(user)
                    buyer.save()

                    updatePoints(user, payload["invitation_code"], business_country, "Buyer")

                    return Response({
                        'code': status.HTTP_200_OK,
                        'message': 'Your password has been set successfully.'
                    })

            else:
                user_instance = User.objects.create(
                    username=mobile_number
                )
                user_instance.set_password(pass1)
                user_instance.save()

                buyer = BuyerInfo.objects.create(
                    user=user_instance,
                    mobile_number=mobile_number,
                    country=business_country  # edited
                )
                buyer.save()

                groups, created = Group.objects.get_or_create(name='Buyer')
                groups.user_set.add(user_instance)

                updatePoints(user_instance, payload["invitation_code"], business_country,"Buyer")

                return Response({
                    'code': status.HTTP_200_OK,
                    'message': 'Your password has been set successfully.'
                })
        else:
            return Response(request_serializer.errors)
    except Exception as e:
        return Response({
            "code": status.HTTP_400_BAD_REQUEST,
            "message": str(e)
})


@api_view(['POST'])
def tokenObtainPair(request):
    payload = request.data
    response = returnToken(payload,'Seller')
    return Response(response)

@api_view(['POST'])
def tokenObtainBuyer(request):
    payload = request.data
    response = returnToken(payload, 'Buyer')
    return Response(response)


@api_view(['POST'])
def tokenRefresh(request):
    try:
        payload = request.data
        if 'refresh_token' not in payload:
            return Response({
                "code": 1000,
                "message": "Validation Failed",
                "errors": [
                    {
                        "code": 2002,
                        "field": "refresh_token",
                        "message": "This field is required."
                    }
                ]
            })
        refresh = RefreshToken(token=payload.get('refresh_token'), verify=True)

        try:
            group = Group.objects.get(user=User.objects.get(id=refresh.payload['user_id'])).name
        except Exception as e:
            return Response({
                "code": status.HTTP_401_UNAUTHORIZED,
                "message": "Something went wrong. Please contact customer support for details."
            })

        return Response({
            'code': status.HTTP_200_OK,
            'access_token': str(refresh.access_token),
            'refresh_token': str(refresh),
            'token_type': str(refresh.payload['token_type']),
            'expiry': refresh.payload['exp'],
            'user_id': refresh.payload['user_id'],
            'user_group': group
        })
    except Exception as e:
        return Response({
            "code": status.HTTP_401_UNAUTHORIZED,
            "message": str(e),
            "status_code": 401,
            "errors": [
                {
                    "status_code": 401,
                    "message": str(e)
                }
            ]
        })


@api_view(['POST'])
def tokenVerify(request):
    try:
        payload = request.data
        if 'access_token' not in payload:
            return Response({
                "code": 1000,
                "message": "Validation Failed",
                "errors": [
                    {
                        "code": 2002,
                        "field": "access_token",
                        "message": "This field is required."
                    }
                ]
            })
        verify = UntypedToken(token=payload.get('access_token'))

        return Response({
            'code': status.HTTP_200_OK,
            'access_token': str(verify.token),
            'token_type': str(verify.payload['token_type']),
            'expiry': verify.payload['exp'],
            'user_id': verify.payload['user_id'],
        })
    except Exception as e:
        return Response({
            "code": status.HTTP_401_UNAUTHORIZED,
            "message": str(e),
            "status_code": 401,
            "errors": [
                {
                    "status_code": 401,
                    "message": str(e)
                }
            ]
        })


@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
@seller_only
def getBusinessTypes(request):
    try:
        business_types = BusinessType.objects.all()
        response_serializer = BusinessTypeSerializer(business_types, many=True, context={'request': request})
        return Response({
            'code': status.HTTP_200_OK,
            'message': 'Business types received successfully.',
            'data': response_serializer.data
        })
    except Exception as e:
        return Response({
            "code": status.HTTP_400_BAD_REQUEST,
            "message": str(e)
        })


@api_view(['POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
@seller_only
def createShop(request):
    try:
        payload = request.data
        request_serializer = ShopCreateSerializer(data=payload)
        if request_serializer.is_valid():
            shop_instance = ShopInfo.objects.get(user=request.user)
            request_serializer.update(shop_instance, request_serializer.validated_data)
            business_slug = slugify(request_serializer.validated_data.get('business_name'))
            shop_instance.business_slug = "%s-%s" % (business_slug, str(shop_instance.mobile_number[-4:]))
            shop_instance.save()

            if not ShopOnlineStatus.objects.filter(user=request.user).exists():
                ShopOnlineStatus.objects.create(
                    user=request.user
                )

            return Response({
                'code': status.HTTP_200_OK,
                'message': 'Shop updated successfully.'
            })
        else:
            return Response(request_serializer.errors)
    except Exception as e:
        return Response({
            "code": status.HTTP_400_BAD_REQUEST,
            "message": str(e)
        })


@api_view(['POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
@seller_only
def updateShopAddress(request):
    try:
        payload = request.data
        request_serializer = ShopAddressUpdateSerializer(data=payload)
        if request_serializer.is_valid():
            shop_instance = ShopInfo.objects.get(user=request.user)
            request_serializer.update(shop_instance, request_serializer.validated_data)
            return Response({
                'code': status.HTTP_200_OK,
                'message': 'Shop address updated successfully.'
            })
        else:
            return Response(request_serializer.errors)
    except Exception as e:
        return Response({
            "code": status.HTTP_400_BAD_REQUEST,
            "message": str(e)
        })


@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
@seller_only
def getShopInfo(request):
    try:
        shop_info = ShopInfo.objects.get(user=request.user)
        return Response({
            'code': status.HTTP_200_OK,
            'message': 'Shop info received successfully.',
            'data': ShopInfoReadSerializer(shop_info, context={'request': request}).data
        })
    except Exception as e:
        return Response({
            "code": status.HTTP_400_BAD_REQUEST,
            "message": str(e)
        })


@api_view(['POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
@seller_only
def updateShopInfo(request):
    try:
        shop_info = ShopInfo.objects.get(user=request.user)
        payload = request.data
        if 'business_logo' in payload and payload['business_logo'] is not None and payload['business_logo'] != "":
            fmt, img_str = str(payload['business_logo']).split(';base64,')
            ext = fmt.split('/')[-1]
            img_file = ContentFile(base64.b64decode(img_str), name='%s.%s' % (shop_info.business_slug, ext))
            payload['business_logo'] = img_file
        request_serializer = ShopInfoUpdateSerializer(data=payload)
        if request_serializer.is_valid():
            request_serializer.update(instance=shop_info, validated_data=request_serializer.validated_data)
            if 'email' in payload and payload['email'] is not None and payload['email'] != "":
                shop_info.user.email = payload['email']
                shop_info.user.save()
            return Response({
                'code': status.HTTP_200_OK,
                'message': 'Shop info updated successfully.',
                'data': ShopInfoReadSerializer(shop_info, context={'request': request}).data
            })
        else:
            return Response(request_serializer.errors)
    except Exception as e:
        return Response({
            "code": status.HTTP_400_BAD_REQUEST,
            "message": str(e)
        })


@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
@seller_only
def getShopOnlineStatus(request):
    try:
        online_instance = ShopOnlineStatus.objects.get(user=request.user)
        return Response({
            'code': status.HTTP_200_OK,
            'message': 'Shop online status received successfully.',
            'data': ShopOnlineStatusSerializer(online_instance).data
        })
    except Exception as e:
        return Response({
            "code": status.HTTP_400_BAD_REQUEST,
            "message": str(e)
        })


@api_view(['POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
@seller_only
def goShopOnline(request):
    try:
        online_instance = ShopOnlineStatus.objects.get(user=request.user)
        online_instance.online_status = True
        online_instance.save()
        return Response({
            'code': status.HTTP_200_OK,
            'message': 'Shop status set to Online.',
        })
    except Exception as e:
        return Response({
            "code": status.HTTP_400_BAD_REQUEST,
            "message": str(e)
        })


@api_view(['POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
@seller_only
def goShopOffline(request):
    try:
        payload = request.data
        request_serializer = ShopOfflineUpdateSerializer(data=payload)
        if request_serializer.is_valid():
            online_instance = ShopOnlineStatus.objects.get(user=request.user)
            request_serializer.update(online_instance, request_serializer.validated_data)
            online_instance.online_status = False
            online_instance.save()
            return Response({
                'code': status.HTTP_200_OK,
                'message': 'Shop status set to Offline.',
            })
        else:
            return Response(request_serializer.errors)
    except Exception as e:
        return Response({
            "code": status.HTTP_400_BAD_REQUEST,
            "message": str(e)
        })


@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
@seller_only
def getPromoBanners(request):
    try:
        promo_banners = HomePromoBanner.objects.all()
        return Response({
            'code': status.HTTP_200_OK,
            'message': 'Promo banners received successfully.',
            'data': HomeBannerSerializer(promo_banners, many=True, context={'request': request}).data
        })
    except Exception as e:
        return Response({
            "code": status.HTTP_400_BAD_REQUEST,
            "message": str(e)
        })


@api_view(['POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
@seller_only
def getHomeOverview(request):
    try:
        payload = request.data
        request_serializer = HomeOverviewFilterSerializer(data=payload)
        if request_serializer.is_valid():
            return Response({
                'code': status.HTTP_200_OK,
                'message': 'Home overview received successfully.',
                'data': {
                    'orders': 0,
                    'total_sales': 0,
                    'store_view': 0,
                    'product_view': 0
                }
            })
        else:
            return Response(request_serializer.errors)
    except Exception as e:
        return Response({
            "code": status.HTTP_400_BAD_REQUEST,
            "message": str(e)
        })


@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
@seller_only
def getWeightUnits(request):
    try:
        return Response({
            'code': status.HTTP_200_OK,
            'message': 'Weight unit received successfully.',
            'data': WeightUnitSerializer(ProductWeightUnit.objects.all(), many=True).data
        })
    except Exception as e:
        return Response({
            "code": status.HTTP_400_BAD_REQUEST,
            "message": str(e)
        })


@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
@seller_only
def getCategoryList(request):
    try:
        return Response({
            'code': status.HTTP_200_OK,
            'message': 'Product category received successfully.',
            'data': ProductCategorySerializer(ProductCategory.objects.all(), many=True,
                                              context={'request': request}).data
        })
    except Exception as e:
        return Response({
            "code": status.HTTP_400_BAD_REQUEST,
            "message": str(e)
        })


@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
@seller_only
def getCategoryTree(request):
    try:
        return Response({
            'code': status.HTTP_200_OK,
            'message': 'Product category tree received successfully.',
            'data': ProductCategoryTreeSerializer(ProductCategory.objects.all(), many=True,
                                                  context={'request': request}).data
        })
    except Exception as e:
        return Response({
            "code": status.HTTP_400_BAD_REQUEST,
            "message": str(e)
        })


@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
@seller_only
def getSubcategoryList(request):
    try:
        parent_category = int(request.GET['category'])
        return Response({
            'code': status.HTTP_200_OK,
            'message': 'Product subcategory received successfully.',
            'data': ProductSubcategorySerializer(ProductSubcategory.objects.filter(parent_category_id=parent_category),
                                                 many=True, context={'request': request}).data
        })
    except Exception as e:
        return Response({
            "code": status.HTTP_400_BAD_REQUEST,
            "message": str(e)
        })


@api_view(['POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
@seller_only
def addProductVariant(request):
    try:
        payload = request.data
        if 'color' not in payload:
            return Response({
                "code": 1000,
                "message": "Validation Failed",
                "errors": [{
                    "code": 2002,
                    "field": "color",
                    "message": "This field is required."
                }]
            })
        fmt, img_str = str(payload['color']).split(';base64,')
        ext = fmt.split('/')[-1]
        img_file = ContentFile(base64.b64decode(img_str), name='temp.' + ext)
        payload['color'] = img_file
        payload['user'] = request.user.id
        request_serializer = ProductAddVariantSerializer(data=payload)
        if request_serializer.is_valid():
            save_serializer = ProductAddVariantSaveSerializer(data=payload)
            if save_serializer.is_valid():
                instance_id = save_serializer.save().id
                try:
                    for ss in payload['size_stock']:
                        ProductSizeStock.objects.create(
                            variant_id=instance_id,
                            size=ss['size'],
                            stock=ss['stock']
                        )
                except Exception as e:
                    ProductVariant.objects.get(id=instance_id).delete()
                    return Response({
                        "code": status.HTTP_400_BAD_REQUEST,
                        "message": str(e)
                    })
                return Response({
                    'code': status.HTTP_200_OK,
                    'message': 'Product variant created successfully.',
                    'data': ProductVariantReadSerializer(ProductVariant.objects.get(id=instance_id),
                                                         context={'request': request}).data
                })
            else:
                return Response(save_serializer.errors)
        else:
            return Response(request_serializer.errors)
    except Exception as e:
        return Response({
            "code": status.HTTP_400_BAD_REQUEST,
            "message": str(e)
        })


@api_view(['PUT'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
@seller_only
def editProductVariant(request):
    try:
        payload = request.data
        if 'color' in payload and payload['color'] is not None and payload['color'] != "null":
            fmt, img_str = str(payload['color']).split(';base64,')
            ext = fmt.split('/')[-1]
            img_file = ContentFile(base64.b64decode(img_str), name='temp.' + ext)
            payload['color'] = img_file
        else:
            payload.pop('color', None)
        payload['user'] = request.user.id
        request_serializer = ProductEditVariantSerializer(data=payload)
        if request_serializer.is_valid():
            save_serializer = ProductEditVariantSaveSerializer(data=payload)
            if save_serializer.is_valid():
                variant_id = request_serializer.validated_data.get('variant_id')
                variant_instance = ProductVariant.objects.get(user=request.user, id=variant_id)
                save_serializer.update(variant_instance, save_serializer.validated_data)
                existing_size_stock = list(ProductSizeStock.objects.filter(variant_id=variant_id).values('pk'))
                existing_stock_array = []
                for sizes in existing_size_stock:
                    existing_stock_array.append(sizes['pk'])
                try:
                    for ss in payload['size_stock']:
                        ProductSizeStock.objects.create(
                            variant_id=variant_id,
                            size=ss['size'],
                            stock=ss['stock']
                        )
                except Exception as e:
                    return Response({
                        "code": status.HTTP_400_BAD_REQUEST,
                        "message": str(e)
                    })
                ProductSizeStock.objects.filter(id__in=existing_stock_array).delete()
                return Response({
                    'code': status.HTTP_200_OK,
                    'message': 'Product variant updated successfully.',
                    'data': ProductVariantReadSerializer(ProductVariant.objects.get(id=variant_id),
                                                         context={'request': request}).data
                })
            else:
                return Response(save_serializer.errors)
        else:
            return Response(request_serializer.errors)
    except Exception as e:
        return Response({
            "code": status.HTTP_400_BAD_REQUEST,
            "message": str(e)
        })


@api_view(['DELETE'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
@seller_only
def deleteProductVariant(request):
    try:
        variant_instance = ProductVariant.objects.get(user=request.user, id=request.GET['id'])
        # color_img_path = os.path.join(settings.BASE_DIR, variant_instance.color.path)
        # if os.path.exists(color_img_path):
        #     os.remove(color_img_path)
        variant_instance.delete()
        return Response({
            'code': status.HTTP_200_OK,
            'message': 'Product variant deleted successfully.'
        })
    except Exception as e:
        return Response({
            "code": status.HTTP_400_BAD_REQUEST,
            "message": str(e)
        })


@api_view(['POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
@seller_only
def addProduct(request):
    try:
        payload = request.data
        payload['user'] = request.user.id
        request_serializer = AddProductSerializer(data=payload)
        if request_serializer.is_valid():
            save_serializer = AddProductSaveSerializer(data=payload)
            if save_serializer.is_valid():
                product_id = save_serializer.save().id
                try:
                    variant_list = str(payload['variant_id']).split(',')
                    for variant in variant_list:
                        variant_instance = ProductVariant.objects.get(id=variant)
                        variant_instance.product_id = product_id
                        variant_instance.save()
                except Exception as e:
                    ShopProduct.objects.get(id=product_id).delete()
                    return Response({
                        "code": status.HTTP_400_BAD_REQUEST,
                        "message": str(e)
                    })
                time_prefix = str(datetime.now().timestamp()).split('.')[1]
                product_instance = ShopProduct.objects.get(id=product_id)
                product_instance.slug = "%s-%s" % (time_prefix, slugify(product_instance.name))

                if 'wholesale_price' in payload:
                    product_instance.basic_price = payload['wholesale_price'][0]['amount']

                product_instance.save()
                return Response({
                    'code': status.HTTP_200_OK,
                    'message': 'Product created successfully.',
                    'data': {
                        'product_id': product_id,
                        'product_name': payload['name']
                    }
                })
            else:
                return Response(save_serializer.errors)
        else:
            return Response(request_serializer.errors)
    except Exception as e:
        return Response({
            "code": status.HTTP_400_BAD_REQUEST,
            "message": str(e)
        })


@api_view(['POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
@seller_only
def addProductImage(request):
    try:
        payload = request.data
        request_serializer = AddProductImageSerializer(data=payload)
        if request_serializer.is_valid():
            product_id = request_serializer.validated_data.get('product')
            ShopProduct.objects.get(id=product_id, user=request.user)
            img_ids = []
            for img in request_serializer.validated_data.get('images'):
                fmt, img_str = str(img).split(';base64,')
                ext = fmt.split('/')[-1]
                img_file = ContentFile(base64.b64decode(img_str), name='temp.' + ext)
                save_payload = {
                    'user': request.user.id,
                    'product': product_id,
                    'product_image': img_file
                }
                img_save_serializer = AddProductImageSaveSerializer(data=save_payload)
                if img_save_serializer.is_valid():
                    img_ids.append(img_save_serializer.save().id)
                else:
                    return Response(img_save_serializer.errors)
            image_list = ProductImages.objects.filter(id__in=img_ids)
            return Response({
                'code': status.HTTP_200_OK,
                'message': 'Product images uploaded successfully.',
                'data': ProductImagesReadSerializer(image_list, many=True, context={'request': request}).data
            })
        else:
            return Response(request_serializer.errors)
    except Exception as e:
        return Response({
            "code": status.HTTP_400_BAD_REQUEST,
            "message": str(e)
        })


@api_view(['DELETE'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
@seller_only
def deleteProductImage(request):
    try:
        payload = request.GET
        request_serializer = DeleteProductImageSerializer(data=payload)
        if request_serializer.is_valid():
            image_id = request_serializer.validated_data.get('image_id')
            img_instance = ProductImages.objects.get(id=image_id, user=request.user)
            # img_path = os.path.join(settings.BASE_DIR, img_instance.product_image.path)
            # if os.path.exists(img_path):
            #     os.remove(img_path)
            img_instance.delete()
            return Response({
                'code': status.HTTP_200_OK,
                'message': 'Product image deleted successfully.'
            })
        else:
            return Response(request_serializer.errors)
    except Exception as e:
        return Response({
            "code": status.HTTP_400_BAD_REQUEST,
            "message": str(e)
        })

from django.db import connection

@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
@seller_only
def getShopProducts(request):
    try:
        shop_products = ShopProduct.objects.filter(user=request.user)
        print(connection.queries)
        response_serializer = ShopProductsReadSerializer(shop_products, many=True, context={'request': request})
        return Response({
            'code': status.HTTP_200_OK,
            'message': 'Products received successfully.',
            'data': response_serializer.data
        })
    except Exception as e:
        return Response({
            "code": status.HTTP_400_BAD_REQUEST,
            "message": str(e)
        })

@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def getSellerRecomendedProducts(request,pk):
    try:
        shop_products = ShopProduct.objects.filter(user=pk).order_by('-created_at')
        if len(shop_products) > 5:
            shop_products = shop_products[5]
        response_serializer = ShopProductsReadSerializer(shop_products, many=True, context={'request': request})
        return Response({
            'code': status.HTTP_200_OK,
            'message': 'Products received successfully.',
            'data': response_serializer.data
        })
    except Exception as e:
        return Response({
            "code": status.HTTP_400_BAD_REQUEST,
            "message": str(e)
        })


@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def getSeller_all_item(request,pk):
    try:
        shop_products = ShopProduct.objects.filter(user=pk)
        response_serializer = ShopProductsReadSerializer(shop_products, many=True, context={'request': request})
        return Response({
            'code': status.HTTP_200_OK,
            'message': 'Products received successfully.',
            'data': response_serializer.data
        })
    except Exception as e:
        return Response({
            "code": status.HTTP_400_BAD_REQUEST,
            "message": str(e)
        })


@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
@seller_only
def getShopProductDetails(request):
    try:
        payload = request.GET
        if 'product_id' not in payload:
            return Response({
                "code": 1000,
                "message": "Validation Failed",
                "errors": [{
                    "code": 2002,
                    "field": "product_id",
                    "message": "This field is required."
                }]
            })
        shop_products = ShopProduct.objects.get(id=payload['product_id'], user=request.user)
        response_serializer = ShopProductsReadSerializer(shop_products, context={'request': request})
        return Response({
            'code': status.HTTP_200_OK,
            'message': 'Product details received successfully.',
            'data': response_serializer.data
        })
    except Exception as e:
        return Response({
            "code": status.HTTP_400_BAD_REQUEST,
            "message": str(e)
        })


@api_view(['PUT'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
@seller_only
def updateProductStatus(request):
    try:
        payload = request.data
        request_serializer = ProductStatusUpdateSerializer(data=payload)
        if request_serializer.is_valid():
            product_instance = ShopProduct.objects.get(user=request.user,
                                                       id=request_serializer.validated_data.get('product_id'))
            request_save = ProductStatusUpdateSaveSerializer(data=payload)
            if request_save.is_valid():
                request_save.update(product_instance, request_save.validated_data)
                return Response({
                    'code': status.HTTP_200_OK,
                    'message': 'Product details received successfully.'
                })
            else:
                return Response(request_save.errors)
        else:
            return Response(request_serializer.errors)
    except Exception as e:
        return Response({
            "code": status.HTTP_400_BAD_REQUEST,
            "message": str(e)
        })


@api_view(['DELETE'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
@seller_only
def deleteProduct(request):
    try:
        payload = request.GET
        request_serializer = ProductDeleteSerializer(data=payload)
        if request_serializer.is_valid():
            product_instance = ShopProduct.objects.get(id=request_serializer.validated_data.get('product_id'),
                                                       user=request.user)
            # variants = product_instance.product_variant.all()
            # images = product_instance.product_image.all()
            # for variant in variants:
            #     if variant.color != '' and variant.color is not None:
            #         img_path = os.path.join(settings.BASE_DIR, variant.color.path)
            #         if os.path.exists(img_path):
            #             os.remove(img_path)
            # for img in images:
            #     if img.product_image != '' and img.product_image is not None:
            #         img_path = os.path.join(settings.BASE_DIR, img.product_image.path)
            #         if os.path.exists(img_path):
            #             os.remove(img_path)
            product_instance.delete()
            return Response({
                "code": status.HTTP_200_OK,
                "message": 'Product deleted successfully.'
            })
        else:
            return Response(request_serializer.errors)
    except Exception as e:
        return Response({
            "code": status.HTTP_400_BAD_REQUEST,
            "message": str(e)
        })


@api_view(['PUT'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
@seller_only
def editProduct(request):
    try:
        payload = request.data
        request_serializer = EditProductSerializer(data=payload)
        if request_serializer.is_valid():
            save_serializer = EditProductSaveSerializer(data=payload)
            if save_serializer.is_valid():
                product_instance = ShopProduct.objects.get(id=request_serializer.validated_data.get('product_id'),
                                                           user=request.user)
                try:
                    variant_list = str(payload['variant_id']).split(',')
                    for variant in variant_list:
                        variant_instance = ProductVariant.objects.get(id=variant)
                        variant_instance.product_id = product_instance.id
                        variant_instance.save()
                except Exception as e:
                    return Response({
                        "code": status.HTTP_400_BAD_REQUEST,
                        "message": str(e)
                    })
                save_serializer.update(product_instance, save_serializer.validated_data)
                return Response({
                    'code': status.HTTP_200_OK,
                    'message': 'Product updated successfully.'
                })
            else:
                return Response(save_serializer.errors)
        else:
            return Response(request_serializer.errors)
    except Exception as e:
        return Response({
            "code": status.HTTP_400_BAD_REQUEST,
            "message": str(e)
        })


@api_view(['POST'])
def createCustomer(request):
    try:
        payload = request.data
        request_serializer = CreateCustomerSerializer(data=payload)

        if request_serializer.is_valid():
            mobile_number = request_serializer.validated_data.get('mobile_number')
            pass1 = request_serializer.validated_data.get('password1')
            pass2 = request_serializer.validated_data.get('password2')

            if pass1 != pass2:
                return Response({
                    'code': status.HTTP_400_BAD_REQUEST,
                    'message': 'Your passwords did not match!'
                })

            if User.objects.filter(username__icontains=mobile_number).exists() or CustomerInfo.objects.filter(
                    mobile_number__icontains=mobile_number).exists():
                return Response({
                    'code': status.HTTP_400_BAD_REQUEST,
                    'message': 'Mobile number already exists.',
                    'data': {
                        'mobile_number': mobile_number,
                        'existing_number': True
                    }
                })

            user_instance = User.objects.create(
                username=mobile_number
            )
            user_instance.set_password(pass2)
            user_instance.save()

            groups, created = Group.objects.get_or_create(name='Customer')
            groups.user_set.add(user_instance)

            info_instance = CustomerInfo.objects.create(
                user=user_instance,
                mobile_number=mobile_number,
                reg_ip=api.helper.get_client_ip(request)
            )
            customer_info_serializer = CustomerInfoSaveSerializer(data=payload)
            if customer_info_serializer.is_valid():
                customer_info_serializer.update(instance=info_instance,
                                                validated_data=customer_info_serializer.validated_data)
            return Response({
                'code': status.HTTP_200_OK,
                'message': 'Your account has been created successfully.'
            })
        else:
            return Response(request_serializer.errors)
    except Exception as e:
        return Response({
            "code": status.HTTP_400_BAD_REQUEST,
            "message": str(e)
        })


@api_view(['POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
@buyer_or_customer
def placeOrder(request):
    try:
        payload = request.data
        data = copy.deepcopy(payload)
        buy_together_obj = None
        place_order_serializer = PlaceOrderSerializer(data=payload)
        if place_order_serializer.is_valid():
            for product in payload['products']:
                if 'buy_together' in product:
                    del product['buy_together']
                    del product['item_need']
                    del product['buy_together_price']

                elif 'buy_together_id' in product:
                    del product['buy_together_id']
                product_serializer = OrderItemSerializer(data=product)
                if not product_serializer.is_valid():
                    return Response(product_serializer.errors)

            seller_instance = ShopProduct.objects.get(id=payload['products'][0]['product_id']).user
            customer_instance = request.user

            order_instance = Orders.objects.create(
                seller=seller_instance,
                customer=customer_instance,
                item_count=len(payload['products']),
                delivery_fee=payload['delivery_fee'],
                coupon_code=payload['coupon_code'],
                coupon_discount=payload['coupon_discount'],
                token_discount= payload['token_discount'],
                payment_method=payload['payment_method']
            )

            date_today = datetime.now().astimezone()
            order_id = "%s%s%s%s" % (date_today.year, date_today.month, date_today.day, order_instance.id)
            order_instance.order_id = order_id
            order_instance.save()

            grand_total = order_instance.delivery_fee - order_instance.coupon_discount
            item_total = 0
            print(data)
            for product in data['products']:
                product_instance = ShopProduct.objects.get(id=product['product_id'])
                product_instance.total_sale += product["quantity"]

                product['order'] = order_instance.id
                if 'buy_together' in product:
                    buy_together_obj = BuyTogether.objects.create(item_need=product['item_need']-product['quantity'],
                                                     buy_together_price=product['buy_together_price'])
                    if buy_together_obj.item_need <0:
                        buy_together_obj.item_need = 0
                    buy_together_obj.save()
                    del product['buy_together']
                    del product['item_need']
                    del product['buy_together_price']

                    product['buy_together'] = buy_together_obj.id
                elif 'buy_together_id' in product:
                    buy_together_obj = BuyTogether.objects.filter(id=product['buy_together_id']).first()
                    buy_together_obj.item_need = buy_together_obj.item_need - product['quantity']

                    if buy_together_obj.item_need <0:
                        buy_together_obj.item_need = 0
                    buy_together_obj.save()

                    del product['buy_together_id']

                    product['buy_together'] = buy_together_obj.id

                product['item_name'] = product_instance.name
                product['subtotal'] = round(float(product['quantity']) * float(product['unit_price']), 2)
                item_total += round(float(product['quantity']) * float(product['unit_price']), 2)
                save_serializer = OrderItemSaveSerializer(data=product)
                if save_serializer.is_valid():
                    save_serializer.save()
                else:
                    return Response(save_serializer.errors)

            product_instance.save()


            grand_total += item_total
            order_instance.item_total = item_total
            grand_total = grand_total - order_instance.token_discount
            order_instance.grand_total = grand_total
            order_instance.save()



            if 'transection_id' in payload:
                try:
                    payment_method = PaymentMethods.objects.filter(method_name=payload['payment_method']).first()
                    obj = PaymentTransection.objects.create(
                        order=order_instance,
                        payment_method = payment_method,
                        transection_id = payload['transection_id']
                        )
                    obj.save()
                except:
                    return Response({
                        "code": status.HTTP_200_OK,
                        "message": "Your order has been saved but error in payment method",
                        "data": {
                            "order_id": order_id
                        }
                    })

            return Response({
                "code": status.HTTP_200_OK,
                "message": "Your order has been placed successfully.",
                "data": {
                    "order_id": order_id
                }
            })
        else:
            return Response(place_order_serializer.errors)
    except Exception as e:
        return Response({
            "code": status.HTTP_400_BAD_REQUEST,
            "message": str(e)
        })


@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
@seller_only
def getOrders(request):
    try:
        order_list = Orders.objects.filter(seller=request.user, order_date__gte=request.GET['filter_from'],
                                           order_date__lte=request.GET['filter_to'])
        order_status = request.GET['order_status']
        if order_status != 'All':
            order_list = order_list.filter(order_status=order_status)
        order_info = OrderInfoSerializer(order_list, many=True, context={'request': request})
        return Response({
            'code': status.HTTP_200_OK,
            'message': 'Order list received successfully.',
            'data': order_info.data
        })
    except Exception as e:
        return Response({
            "code": status.HTTP_400_BAD_REQUEST,
            "message": str(e)
        })


@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
@seller_only
def getOrderDetails(request):
    try:
        order_id = request.GET['order_id']
        order_summary = Orders.objects.get(order_id=order_id, seller=request.user)
        order_products = OrderItems.objects.filter(order__order_id=order_id)
        customer_info = CustomerInfo.objects.get(user=order_summary.customer)
        return Response({
            'code': status.HTTP_200_OK,
            'message': 'Order details received successfully.',
            'data': {
                'summary': AllOrderInfoSerializer(order_summary, many=False, context={'request': request}).data,
                'products': AllOrderProductSerializer(order_products, many=True, context={'request': request}).data,
                'customer': DetailsCustomerInfoSerializer(customer_info, many=False, context={'request': request}).data
            }
        })
    except Exception as e:
        return Response({
            "code": status.HTTP_400_BAD_REQUEST,
            "message": str(e)
        })


@api_view(['POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
@seller_only
def acceptOrder(request):
    try:
        payload = request.data
        request_serializer = AcceptOrderSerializer(data=payload)
        if request_serializer.is_valid():
            order_instance = Orders.objects.get(order_id=request_serializer.validated_data.get('order_id'),
                                                seller=request.user)
            order_instance.delivery_time = request_serializer.validated_data.get('delivery_time')
            order_instance.order_status = "Processing"
            order_instance.save()
            return Response({
                'code': status.HTTP_200_OK,
                'message': 'Order has been accepted successfully.'
            })
        else:
            return Response(request_serializer.errors)
    except Exception as e:
        return Response({
            "code": status.HTTP_400_BAD_REQUEST,
            "message": str(e)
        })


@api_view(['POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
@seller_only
def cancelOrder(request):
    try:
        payload = request.data
        request_serializer = OrderIDSerializer(data=payload)
        if request_serializer.is_valid():
            order_instance = Orders.objects.get(order_id=request_serializer.validated_data.get('order_id'),
                                                seller=request.user)
            order_instance.order_status = "Cancelled"
            order_instance.save()
            return Response({
                'code': status.HTTP_200_OK,
                'message': 'Order has been cancelled.'
            })
        else:
            return Response(request_serializer.errors)
    except Exception as e:
        return Response({
            "code": status.HTTP_400_BAD_REQUEST,
            "message": str(e)
        })


@api_view(['POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
@seller_only
def shipOrder(request):
    try:
        payload = request.data
        request_serializer = OrderIDSerializer(data=payload)
        if request_serializer.is_valid():
            order_instance = Orders.objects.get(order_id=request_serializer.validated_data.get('order_id'),
                                                seller=request.user)
            order_instance.order_status = "Shipped"
            order_instance.shipping_status = "Shipped"
            order_instance.save()
            return Response({
                'code': status.HTTP_200_OK,
                'message': 'Order has been shipped.'
            })
        else:
            return Response(request_serializer.errors)
    except Exception as e:
        return Response({
            "code": status.HTTP_400_BAD_REQUEST,
            "message": str(e)
        })


@api_view(['POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
@seller_only
def completeOrder(request):
    try:
        payload = request.data
        request_serializer = OrderIDSerializer(data=payload)
        if request_serializer.is_valid():
            order_instance = Orders.objects.get(order_id=request_serializer.validated_data.get('order_id'),
                                                seller=request.user)
            order_instance.shipping_status = "Completed"
            order_instance.order_status = "Completed"
            order_instance.save()
            return Response({
                'code': status.HTTP_200_OK,
                'message': 'Order has been completed.'
            })
        else:
            return Response(request_serializer.errors)
    except Exception as e:
        return Response({
            "code": status.HTTP_400_BAD_REQUEST,
            "message": str(e)
        })


@api_view(['POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
@seller_only
def failedOrder(request):
    try:
        payload = request.data
        request_serializer = OrderIDSerializer(data=payload)
        if request_serializer.is_valid():
            order_instance = Orders.objects.get(order_id=request_serializer.validated_data.get('order_id'),
                                                seller=request.user)
            order_instance.shipping_status = "Failed"
            order_instance.order_status = "Cancelled"
            order_instance.save()
            return Response({
                'code': status.HTTP_200_OK,
                'message': 'Order has been failed.'
            })
        else:
            return Response(request_serializer.errors)
    except Exception as e:
        return Response({
            "code": status.HTTP_400_BAD_REQUEST,
            "message": str(e)
        })


@api_view(['POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
@seller_only
def createCoupon(request):
    try:
        payload = request.data
        payload['seller'] = request.user.id
        request_serializer = CouponSerializer(data=payload)
        if request_serializer.is_valid():
            instance = request_serializer.save()
            return Response({
                'code': status.HTTP_200_OK,
                'message': 'Coupon created successfully',
                'data': CouponReadSerializer(instance).data
            })
        else:
            return Response(request_serializer.errors)
    except Exception as e:
        return Response({
            "code": status.HTTP_400_BAD_REQUEST,
            "message": str(e)
        })


@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
@seller_only
def getCoupons(request):
    try:
        coupon_list = Coupon.objects.filter(seller=request.user).order_by('-created_at')
        return Response({
            'code': status.HTTP_200_OK,
            'message': 'Coupon received successfully',
            'data': CouponReadSerializer(coupon_list, many=True).data
        })
    except Exception as e:
        return Response({
            "code": status.HTTP_400_BAD_REQUEST,
            "message": str(e)
        })


@api_view(['POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
@seller_only
def createCourier(request):
    try:
        payload = request.data
        for courier in payload['courier']:
            courier['seller'] = request.user.id
            request_serializer = CourierMethodSerializer(data=courier)
            if not request_serializer.is_valid():
                return Response(request_serializer.errors)
        for courier in payload['courier']:
            courier['seller'] = request.user.id
            request_serializer = CourierMethodSerializer(data=courier)
            if request_serializer.is_valid():
                request_serializer.save()
        return Response({
            'code': status.HTTP_200_OK,
            'message': 'Courier method created successfully'
        })
    except Exception as e:
        return Response({
            "code": status.HTTP_400_BAD_REQUEST,
            "message": str(e)
        })


@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
@seller_only
def getCourier(request):
    try:
        courier_list = CourierMethod.objects.filter(seller=request.user).order_by('courier_name')
        return Response({
            'code': status.HTTP_200_OK,
            'message': 'Courier method received successfully',
            'data': CourierMethodReadSerializer(courier_list, many=True).data
        })
    except Exception as e:
        return Response({
            "code": status.HTTP_400_BAD_REQUEST,
            "message": str(e)
        })


@api_view(['POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
@seller_only
def changePassword(request):
    try:
        payload = request.data
        if 'current_pass' in payload and payload['current_pass'] is not None and payload['current_pass'] != "":
            current_pass = payload['current_pass']
            if check_password(current_pass, request.user.password):
                new_pass1 = payload['new_pass1']
                new_pass2 = payload['new_pass2']
                if new_pass1 == new_pass2:
                    request.user.set_password(new_pass2)
                    request.user.save()
                    return Response({
                        'code': status.HTTP_200_OK,
                        'message': 'Password updated successfully.',
                    })
                else:
                    return Response({
                        'code': status.HTTP_400_BAD_REQUEST,
                        'message': 'Your passwords did not match.',
                    })
            else:
                return Response({
                    'code': status.HTTP_400_BAD_REQUEST,
                    'message': 'Incorrect password.',
                })
        else:
            return Response({
                'code': status.HTTP_400_BAD_REQUEST,
                'message': 'Invalid request.',
            })
    except Exception as e:
        return Response({
            "code": status.HTTP_400_BAD_REQUEST,
            "message": str(e)
        })


@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
@seller_only
def getPaymentMethod(request):
    try:
        if not PaymentMethods.objects.filter(method_name='UPI ID', seller_id=request.user.id).exists():
            PaymentMethods.objects.create(
                seller_id=request.user.id,
                method_name='UPI ID'
            )
            PaymentMethods.objects.create(
                seller_id=request.user.id,
                method_name='Bank Transfer'
            )
            PaymentMethods.objects.create(
                seller_id=request.user.id,
                method_name='UPI ID'
            )
        method_list = PaymentMethods.objects.filter(seller=request.user)
        return Response({
            'code': status.HTTP_200_OK,
            'message': 'Payment methods received successfully.',
            'data': PaymentMethodReadSerializer(method_list, many=True).data
        })
    except Exception as e:
        return Response({
            "code": status.HTTP_400_BAD_REQUEST,
            "message": str(e)
        })


@api_view(['POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
@seller_only
def updatePaymentMethod(request):
    try:
        payload = request.data
        request_serializer = PaymentMethodUpdateSerializer(data=payload)
        if request_serializer.is_valid():
            instance = PaymentMethods.objects.get(id=payload['id'], seller=request.user)
            request_serializer.update(instance, request_serializer.validated_data)
            return Response({
                'code': status.HTTP_200_OK,
                'message': 'Payment methods received successfully.',
                'data': PaymentMethodReadSerializer(instance).data
            })
        else:
            return Response(request_serializer.errors)
    except Exception as e:
        return Response({
            "code": status.HTTP_400_BAD_REQUEST,
            "message": str(e)
        })


@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
@seller_only
def myPayments(request):
    try:
        return Response({
            'code': status.HTTP_200_OK,
            'message': 'My payments received successfully.',
            'data': {
                'balance': 20000,
                'transactions': [{
                    'id': 2,
                    'order_id': '12313',
                    'payment_id': '231313',
                    'status': 'Pending',
                    'amount': 500,
                    'pay_time': 'Feb 11, 01:50 PM'
                }, {
                    'id': 3,
                    'order_id': '12313',
                    'payment_id': '231313',
                    'status': 'Pending',
                    'amount': 500,
                    'pay_time': 'Feb 11, 01:50 PM'
                }, {
                    'id': 4,
                    'order_id': '12313',
                    'payment_id': '231313',
                    'status': 'Pending',
                    'amount': 500,
                    'pay_time': 'Feb 11, 01:50 PM'
                }, {
                    'id': 5,
                    'order_id': '12313',
                    'payment_id': '231313',
                    'status': 'Pending',
                    'amount': 500,
                    'pay_time': 'Feb 11, 01:50 PM'
                }]
            }
        })
    except Exception as e:
        return Response({
            "code": status.HTTP_400_BAD_REQUEST,
            "message": str(e)
        })


@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
@seller_only
def getExtraCharge(request):
    try:
        if not ExtraCharge.objects.filter(seller=request.user).exists():
            ExtraCharge.objects.create(seller=request.user)
        extra_charge = ExtraCharge.objects.get(seller=request.user)
        return Response({
            'code': status.HTTP_200_OK,
            'message': 'Extra charge received successfully.',
            'data': ExtraChargeSerializer(extra_charge).data
        })
    except Exception as e:
        return Response({
            "code": status.HTTP_400_BAD_REQUEST,
            "message": str(e)
        })


@api_view(['POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
@seller_only
def updateExtraCharge(request):
    try:
        payload = request.data
        request_serializer = ExtraChargeSerializer(data=payload)
        if request_serializer.is_valid():
            ec_instance = ExtraCharge.objects.get(seller=request.user)
            request_serializer.update(ec_instance, request_serializer.validated_data)
            return Response({
                'code': status.HTTP_200_OK,
                'message': 'Extra charge updated successfully.',
                'data': ExtraChargeSerializer(ec_instance).data
            })
        else:
            return Response(request_serializer.errors)
    except Exception as e:
        return Response({
            "code": status.HTTP_400_BAD_REQUEST,
            "message": str(e)
        })


@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
@seller_only
def myQR(request):
    try:
        shop_info = ShopInfo.objects.get(user=request.user)
        return Response({
            'code': status.HTTP_200_OK,
            'message': 'QR Info received successfully.',
            'data': {
                'shop_info': ShopInfoReadSerializer(shop_info).data,
                'qr_code': 'https://cdn.ttgtmedia.com/rms/misc/qr_code_barcode.jpg'
            }
        })
    except Exception as e:
        return Response({
            "code": status.HTTP_400_BAD_REQUEST,
            "message": str(e)
        })

@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def getReview(request,pk=None):
    try:
        reviews = Review.objects.filter(product__id=pk)

        total_review = len(reviews)
        sum_ratings = 0
        for q in reviews:
            sum_ratings += q.ratings
        try:
            avg_rating=(sum_ratings/total_review)
        except:
            avg_rating = 0

        serializer = ReviewSerializer(reviews, many=True)

        return Response({
            'code': status.HTTP_200_OK,
            'msg': 'Ok',
            'total_review':total_review,
            'avg_rating':avg_rating,
            'serializers': serializer.data
        })
    except Exception as e:
        return Response({
            "code": status.HTTP_400_BAD_REQUEST,
            "message": str(e)
        })

@api_view(['POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def createReview(request):
    try:
        payload = request.data
        request_serializer = ReviewSerializer(data=payload)
        if request_serializer.is_valid():
            request_serializer.save()
            return Response(request_serializer.data)

    except Exception as e:
        return Response({
            "code": status.HTTP_400_BAD_REQUEST,
            "message": str(e)
        })


def generate_promo_code(type):
    while True:
        s = 6
        global promo_code
        promo_code = ''.join(random.choices(
            string.ascii_uppercase + string.digits, k=s))
        promo_code = "#Tuni" + str(promo_code)
        check_exists = False
        if type== "Seller":
            try:
                check_exists = InvitationCode.objects.filter(code=promo_code).exists()
            except:
                print('some exception')
        else:
            try:
                check_exists = BuyerInvitationCode.objects.filter(code=promo_code).exists()
            except:
                print('some exception')

        if not check_exists:
            return promo_code

@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
@seller_only
def invitation(request):
    code = generate_promo_code('Seller')
    code_ins = InvitationCode(user=request.user, code=code)
    code_ins.save()

    return Response({
        'code': status.HTTP_200_OK,
        'invitation': code,
        'msg': 'Promo code generated successfully!'
    })

@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
@buyer_only
def buyerinvitation(request):
    code = generate_promo_code('Buyer')
    code_ins = BuyerInvitationCode(user=request.user, code=code)
    code_ins.save()

    return Response({
        'code': status.HTTP_200_OK,
        'invitation': code,
        'msg': 'Promo code generated successfully!'
    })


@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
@seller_only
def getLeaderboard(request):
    try:
        current_user = ShopInfo.objects.get(user=request.user)
        country = current_user.business_country
        users = Reward.objects.filter(user__business_country=country)

        serializer = LeaderBoardSerializer(users, many=True)

        return Response({
            'code': status.HTTP_200_OK,
            'msg': 'Ok',
            'serializers': serializer.data
        })

    except Exception as e:
        return Response({
            "code": status.HTTP_400_BAD_REQUEST,
            "message": str(e)
        })

@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
@buyer_only
def getBuyerLeaderboard(request):
    try:
        current_user = BuyerInfo.objects.get(user=request.user)
        country = current_user.country
        users = BuyerReward.objects.filter(user__country=country)

        serializer = BuyerLeaderBoardSerializer(users, many=True)

        return Response({
            'code': status.HTTP_200_OK,
            'msg': 'Ok',
            'serializers': serializer.data
        })

    except Exception as e:
        return Response({
            "code": status.HTTP_400_BAD_REQUEST,
            "message": str(e)
        })


@api_view(['POST'])
def RewardForPoint(request):
    try:
        payload = request.data
        data_serializer = RewardForPointSerializer(data=payload)
        if data_serializer.is_valid():
            data_serializer.save()
            return Response({
                'code': status.HTTP_200_OK,
                'msg': 'Reward point Saved',
                'serializers': data_serializer.data
            })


    except Exception as e:
        return Response({
            "code": status.HTTP_400_BAD_REQUEST,
            "message": str(e)
        })




@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
@seller_only
def getrewardbycountry(request, country):
    try:
        reward = RewardForPoint.objects.filter(country=country)
        data_serializer = RewardForPointSerializer(reward, many=True)
        print(reward)

        return Response({
            'code': status.HTTP_200_OK,
            'message': 'Reward For Country received successfully.',
            'data': data_serializer.data
        })
    except Exception as e:
        return Response({
            "code": status.HTTP_400_BAD_REQUEST,
            "message": str(e)
        })


@api_view(['POST'])
def createoperator(request):
    try:
        payload = request.data
        request_serializer = OperatorSerializer(data=payload)
        if request_serializer.is_valid():
            request_serializer.save()
            return Response(request_serializer.data)

    except Exception as e:
        return Response({
            "code": status.HTTP_400_BAD_REQUEST,
            "message": str(e)
        })


@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
@seller_only
def getoperator(request):
    try:
        current_user = ShopInfo.objects.get(user=request.user)
        country = current_user.business_country
        operators = Operator.objects.filter(country=country)

        serializer = OperatorSerializer(operators, many=True)

        return Response({
            'code': status.HTTP_200_OK,
            'msg': 'Ok',
            'serializers': serializer.data
        })

    except Exception as e:
        return Response({
            "code": status.HTTP_400_BAD_REQUEST,
            "message": str(e)
        })


@api_view(['POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
@seller_only
def claimrecharge(request):
    try:
        payload = request.data
        deduct_point = payload["point"]
        user = ShopInfo.objects.get(user=request.user)
        request_serializer = ClaimRechargeSerializer(data=payload)
        if request_serializer.is_valid():
            request_serializer.save()

            obj = Reward.objects.get(user=user)
            obj.point = obj.point - deduct_point

            obj.save()

            updateSellerRank(user.business_country)

            return Response(request_serializer.data)

    except Exception as e:
        return Response({
            "code": status.HTTP_400_BAD_REQUEST,
            "message": str(e)
        })


@api_view(['POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
@buyer_only
def buyerclaimrecharge(request):
    try:
        payload = request.data
        deduct_point = payload["point"]
        user = BuyerInfo.objects.get(user=request.user)
        request_serializer = BuyerClaimRechargeSerializer(data=payload)
        if request_serializer.is_valid():
            request_serializer.save()

            obj = BuyerReward.objects.get(user=user)
            obj.point = obj.point - deduct_point

            obj.save()

            updateBuyerRank(user.country)

            return Response(request_serializer.data)

    except Exception as e:
        return Response({
            "code": status.HTTP_400_BAD_REQUEST,
            "message": str(e)
        })

@api_view(['POST'])
def how_it_works(request):
    try:
        payload = request.data
        serializers = Seller_textSerializer(data=payload)
        if serializers.is_valid():
            serializers.save()
            return Response({
                'code': status.HTTP_200_OK,
                'message': 'How it Works Generate Successfully!',
                'serializers': serializers.data
            })

    except Exception as e:
        return Response({
            "code": status.HTTP_400_BAD_REQUEST,
            "message": str(e)
        })


@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
@seller_only
def current_status(request):
    try:
        user = ShopInfo.objects.get(user=request.user)
        obj = Reward.objects.get(user=user)
        serializers = LeaderBoardSerializer(obj)
        return Response({
            'code': status.HTTP_200_OK,
            'msg': 'Your Status is',
            'serializers': serializers.data
        })
    except Exception as e:
        return Response({
            "code": status.HTTP_400_BAD_REQUEST,
            "message": str(e)
        })


@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
@buyer_only
def current_buyer_status(request):
    try:
        user = BuyerInfo.objects.get(user=request.user)
        obj = BuyerReward.objects.get(user=user)
        serializers = BuyerLeaderBoardSerializer(obj)
        return Response({
            'code': status.HTTP_200_OK,
            'msg': 'Your Status is',
            'serializers': serializers.data
        })
    except Exception as e:
        return Response({
            "code": status.HTTP_400_BAD_REQUEST,
            "message": str(e)
        })

@api_view(['POST'])
def reward_post(request):
    try:
        payload = request.data
        data_serializer = RewardForPointSerializer(data=payload)
        if data_serializer.is_valid():
            data_serializer.save()

            return Response({
                'code': status.HTTP_200_OK,
                'msg': 'Your Status is',
                'serializers': data_serializer.data
            })


    except Exception as e:
        return Response({
            "code": status.HTTP_400_BAD_REQUEST,
            "message": str(e)
        })


@api_view(['POST'])
def post_referal_point(request):
    try:
        payload = request.data
        data_serializer = PointSerializer(data=payload)
        if data_serializer.is_valid():
            data_serializer.save()

            return Response({
                'code': status.HTTP_200_OK,
                'msg': 'Point Saved!',
                'serializers': data_serializer.data
            })


    except Exception as e:
        return Response({
            "code": status.HTTP_400_BAD_REQUEST,
            "message": str(e)
        })


@api_view(['PATCH'])
def follow(request):
    try:
        payload = request.data
        data_serializer = FollowerSerializer(data=payload)
        shop = ShopInfo.objects.filter(id=payload['id']).first()
        buyer = BuyerInfo.objects.filter(id=payload['followers']).first()

        if shop.user != buyer.user:
            shop.followers.add(buyer)
            shop.save()

            return Response({
                'code': status.HTTP_200_OK,
                'msg': 'Follower Added!'
            })

        return Response({
            'code': status.HTTP_200_OK,
            'msg': 'Buyer And Seller is same user!'
        })
    except Exception as e:
        return Response({
            "code": status.HTTP_400_BAD_REQUEST,
            "message": str(e)
        })

# @api_view(['PATCH'])
# @authentication_classes([JWTAuthentication])
# @permission_classes([IsAuthenticated])
# @buyer_only
# def updateProfile(request):
#     try:
#         data = request.data
#         data_serializer = BuyerInfoUpdateSerialiser(data=data)
#
#         if data_serializer.is_valid:
#             obj = BuyerInfo.objects.filter(id=data['id']).first()
#
#             obj.name = data.get("name", obj.name)
#             obj.country = data.get("country", obj.country)
#             obj.mobile_number = data.get("mobile_number", obj.mobile_number)
#             obj.address = data.get("address", obj.address)
#             obj.photo = data.get("photo", obj.photo)
#             obj.city = data.get("city", obj.city)
#             obj.postcode = data.get("postcode", obj.postcode)
#
#             obj.save()
#
#             return Response({
#                 'code': status.HTTP_200_OK,
#                 'msg': 'Updated Info'
#             })
#     except Exception as e:
#         return Response({
#             "code": status.HTTP_400_BAD_REQUEST,
#             "message": str(e)
#         })


@api_view(['PATCH'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
@buyer_only
def add_product_existing_folder(request,pk):
    try:
        buyer = request.user
        data = request.data
        folder = BuyerFolderToSaveProduct.objects.filter(buyer=buyer).filter(id=pk).first()
        print(folder)

        if 'products' in data:
            product = ShopProduct.objects.filter(id=data["products"]).first()
            folder.products.add(product)

            folder.save()

            return Response({
                'code': status.HTTP_200_OK,
                'msg': 'Added to folder'
            })
    except Exception as e:
        return Response({
            "code": status.HTTP_400_BAD_REQUEST,
            "message": str(e)
        })


@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
@buyer_only
def get_cart(request):
    try:
        cart = CartShop.objects.filter(cart__user=request.user)
        serializers = GetCartItem(cart, many=True)
        return Response({
            'code': status.HTTP_200_OK,
            'msg': 'Your Status is',
            'serializers': serializers.data
        })
    except Exception as e:
        return Response({
            "code": status.HTTP_400_BAD_REQUEST,
            "message": str(e)
        })

@api_view(['POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
@buyer_only
def add_to_cart(request):
    data = request.data
    user = request.user
    try:
        cart = Cart.objects.filter(user=user).first()
        print(cart)
        try:
            product = ShopProduct.objects.get(id=data["product"])
            cart_shop = CartShop.objects.filter(shop__user=product.user).first()
            cart_item = CartItem.objects.create(cart_shop=cart_shop,product=product,quantity=data["quantity"],
                                                size=data["size"],color=data["color"])
            cart_item.save()
            return Response({
                'code': status.HTTP_200_OK,
                'msg': 'added item to cart',
            })
        except:
            product = ShopProduct.objects.get(id=data["product"])
            shop = ShopInfo.objects.get(user=product.user)
            cart_shop = CartShop.objects.create(cart=cart,shop=shop)
            cart_item = CartItem.objects.create(cart_shop=cart_shop, product=product, quantity=data["quantity"],
                                                size=data["size"],color=data["color"])
            cart_item.save()
            return Response({
                'code': status.HTTP_200_OK,
                'msg': 'added item to cart',
            })
    except:
        cart = Cart.objects.create(user=user)
        product = ShopProduct.objects.get(id=data["product"])
        shop = ShopInfo.objects.get(user=product.user)
        cart_shop = CartShop.objects.create(cart=cart, shop=shop)
        cart_item = CartItem.objects.create(cart_shop=cart_shop, product=product, quantity=data["quantity"],
                                            size=data["size"],color=data["color"])
        cart_item.save()
        return Response({
            'code': status.HTTP_200_OK,
            'msg': 'added item to cart',
        })


@api_view(['POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
@buyer_only
def update_cart(request):
    data = request.data
    user = request.user
    try:
        cart_item = CartItem.objects.filter(cart_shop__cart__user=user).filter(product__id=data["product"]).first()
        cart_item.quantity = data["quantity"]
        cart_item.save()
        return Response({
            'code': status.HTTP_200_OK,
            'msg': 'updated cart',
        })
    except Exception as e:
        return Response({
            "code": status.HTTP_400_BAD_REQUEST,
            "message": str(e)
        })

@api_view(['DELETE'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
@buyer_only
def remove_cart_item(request):
    data = request.data
    user = request.user
    try:
        cart_item = CartItem.objects.filter(cart_shop__cart__user=user).filter(product__id=data["product"]).first()
        shop = cart_item.cart_shop
        cart_item.delete()
        count_shop_item = CartItem.objects.filter(cart_shop=shop).count()
        if count_shop_item < 1 :
            shop.delete()
        return Response({
            'code': status.HTTP_200_OK,
            'msg': 'deleted cart item',
        })
    except Exception as e:
        return Response({
            "code": status.HTTP_400_BAD_REQUEST,
            "message": str(e)
        })

@api_view(['DELETE'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
@buyer_only
def remove_cart_item_by_store(request):
    data = request.data
    user = request.user
    try:
        shop = CartShop.objects.filter(cart__user=user).filter(shop__user__id=data["shop_id"])
        shop.delete()
        return Response({
            'code': status.HTTP_200_OK,
            'msg': 'deleted all cart item from shop',
        })
    except Exception as e:
        return Response({
            "code": status.HTTP_400_BAD_REQUEST,
            "message": str(e)
        })

@api_view(['DELETE'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
@buyer_only
def remove_all_item(request):
    data = request.data
    user = request.user
    try:
        cart = Cart.objects.filter(user=user).first()
        cart.delete()
        return Response({
            'code': status.HTTP_200_OK,
            'msg': 'deleted all cart item',
        })
    except Exception as e:
        return Response({
            "code": status.HTTP_400_BAD_REQUEST,
            "message": str(e)
        })

@api_view(['POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
@buyer_only
def update_cart(request):
    data = request.data
    user = request.user
    try:
        cart_item = CartItem.objects.filter(cart_shop__cart__user=user).filter(product__id=data["product"]).first()
        cart_item.quantity = data["quantity"]
        cart_item.save()
        return Response({
            'code': status.HTTP_200_OK,
            'msg': 'updated cart',
        })
    except Exception as e:
        return Response({
            "code": status.HTTP_400_BAD_REQUEST,
            "message": str(e)
        })

@api_view(['POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
@parser_classes([ MultiPartParser])
@buyer_only
def upload_bank_reciept(request):
    data = request.data
    print(data)
    user = request.user
    try:
        transection_id = ''.join(random.choices(
            string.ascii_uppercase + string.digits, k=12))
        transection_id = "#TBANK" + str(transection_id)
        data["transection_id"] = transection_id
        data["user"] = user.id
        serializer = UploadBankReciept(data=data, context={'request':request})
        if serializer.is_valid():
            serializer.save()
        return Response({
            'code': status.HTTP_200_OK,
            'msg': 'uploaded reciept',
            'transection_id':transection_id
        })
    except Exception as e:
        return Response({
            "code": status.HTTP_400_BAD_REQUEST,
            "message": str(e)
        })


@api_view(['POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
@buyer_only
def add_shipping_address(request):
    try:
        buyer = request.user
        data = request.data
        serializer = BuyerShippingAddress(data=data)
        if serializer.is_valid():
            try:
                obj = BuyerSgippingAddress.objects.filter(buyer=buyer).filter(default=True).first()
                print(obj)
                obj.default = False
                obj.save()
            except:
                print('Y')
            serializer.save()
            return Response({
                "code": 200,
                "message": "Added Shipping Address",
                "data":serializer.data
            })

    except Exception as e:
        return Response({
            "code": status.HTTP_400_BAD_REQUEST,
            "message": str(e)
        })

@api_view(['PUT'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
@buyer_only
def update_shipping_address(request,pk):

    try:
        data = request.data
        data_serializer = BuyerShippingAddressUpdate(data=data)

        if data_serializer.is_valid():
            obj = BuyerSgippingAddress.objects.filter(id=pk).first()

            obj.name = data.get("name", obj.name)
            obj.country = data.get("country", obj.country)
            obj.mobile_number = data.get("mobile_number", obj.mobile_number)
            obj.street_address = data.get("street_address", obj.street_address)
            obj.apt_suite_unit = data.get("apt_suite_unit", obj.apt_suite_unit)
            obj.city = data.get("city", obj.city)
            obj.zip_code = data.get("zip_code", obj.zip_code)

            if data["default"] == True :
                try:
                    previous_default = BuyerSgippingAddress.objects.filter(buyer=request.user).filter(default=True).first()
                    previous_default.default = False
                    previous_default.save()
                except:
                    pass
                obj.default = data.get("default", obj.default)
                obj.save()

                return Response({
                    'code': status.HTTP_200_OK,
                    'msg': 'Updated Info',
                    'data':data_serializer.data
                })

    except Exception as e:
        return Response({
            "code": status.HTTP_400_BAD_REQUEST,
            "message": str(e)
        })

@api_view(['PATCH'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
@buyer_only
def change_default_shipping_address(request,pk):
    try:
        buyer = request.user
        current_default = BuyerSgippingAddress.objects.filter(buyer=buyer,default=True).first()
        current_default.default = False
        current_default.save()

        update_obj = BuyerSgippingAddress.objects.get(id=pk)
        update_obj.default = True
        update_obj.save()

        return Response({
            "code": 200,
            "message": "Updated default address"
        })
    except Exception as e:
        return Response({
            "code": status.HTTP_400_BAD_REQUEST,
            "message": str(e)
        })
