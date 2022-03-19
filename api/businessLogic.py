from .importFile import *
def updateSellerRank(country):
    sellers = Reward.objects.filter(user__business_country = country).order_by('-point')
    count=1
    for seller in sellers:
        seller.rank = count
        seller.save()
        count +=1

def updateBuyerRank(country):
    buyers = BuyerReward.objects.filter(user__country = country).order_by('-point')
    count=1
    for buyer in buyers:
        buyer.rank = count
        buyer.save()
        count +=1

def updateSeller(user , point):
    try:
        getShop = ShopInfo.objects.get(user=user)
    except:
        print('some problem ')

    try:
        reward = Reward.objects.filter(user=getShop)
    except:
        print("some issue")

    if reward.exists():
        u_point = reward[0].point + int(point)
        obj=reward[0]
        obj.point = u_point
        obj.save()
    else:
        obj = Reward(user=getShop, point=point, rank=0)
        obj.save()

def updateBuyer(user , point):
    try:
        getBuyer = BuyerInfo.objects.get(user=user)
    except:
        print('some problem ')

    try:
        reward = BuyerReward.objects.filter(user=getBuyer)
    except:
        print("some issue")

    if reward.exists():
        u_point = reward[0].point + int(point)
        obj=reward[0]
        obj.point = u_point
        obj.save()
    else:
        obj = BuyerReward(user=getBuyer, point=point, rank=0)
        obj.save()

def getPointOfCountry(country):
    try:
        point = Point.objects.get(country=country)
        return point.point
    except:
        return "point not exists"

def callRewardUpdater(user, accountType, point=0):
    if accountType == "Seller":
        updateSeller(user, point)

    else:
        updateBuyer(user, point)

#updated again
def updatePoints(user, code, country, accountType):
    try:
        code_info = InvitationCode.objects.filter(code=code)
        if code_info.exists():
            obj = code_info[0]
            if not obj.used:
                obj.used = True
                obj.save()

                point = getPointOfCountry(country)

                callRewardUpdater(user,accountType,point)
                callRewardUpdater(obj.user, "Seller",point)

            else:
                callRewardUpdater(user,accountType,0)
        else:
            code_buyer = BuyerInvitationCode.objects.filter(code=code)
            if code_buyer.exists():
                obj = code_buyer[0]
                if not obj.used:
                    obj.used = True
                    obj.save()

                    point = getPointOfCountry(country)

                    callRewardUpdater(user, accountType, point)
                    callRewardUpdater(obj.user, "Buyer", point)

                else:
                    callRewardUpdater(user, accountType, 0)
            else:
                callRewardUpdater(user, accountType, 0)

    except:
        print('some problem')


    updateSellerRank(country)
    updateBuyerRank(country)



def returnToken(payload,group):
    try:
        login_serializer = LoginSerializer(data=payload)

        if login_serializer.is_valid():
            mobile_number = login_serializer.validated_data.get('mobile_number')
            password = login_serializer.validated_data.get('password')

            try:
                user_instance = User.objects.get(username=mobile_number)
            except Exception as e:
                return {
                    'code': status.HTTP_400_BAD_REQUEST,
                    'message': "Incorrect mobile number/password combination."
                }

            if not user_instance.is_active:
                return {
                    "code": status.HTTP_401_UNAUTHORIZED,
                    "message": "Your account is inactive. Please contact customer support for details.",
                    "status_code": 401,
                    "errors": [
                        {
                            "status_code": 401,
                            "message": "Your account is inactive. Please contact customer support for details."
                        }
                    ]
                }

            if check_password(password, user_instance.password):
                try:
                    group = user_instance.groups.filter(name=group)
                except Exception as e:
                    return {
                        "code": status.HTTP_401_UNAUTHORIZED,
                        "message": "Something went wrong. Please contact customer support for details."
                    }

                refresh = RefreshToken.for_user(user_instance)

                return {
                    'code': status.HTTP_200_OK,
                    'access_token': str(refresh.access_token),
                    'refresh_token': str(refresh),
                    'token_type': str(refresh.payload['token_type']),
                    'expiry': refresh.payload['exp'],
                    'user_id': refresh.payload['user_id'],
                    'user_group': group[0].name
                }
            else:
                return {
                    "code": status.HTTP_401_UNAUTHORIZED,
                    "message": "Incorrect mobile number/password combination.",
                    "status_code": 401,
                    "errors": [
                        {
                            "status_code": 401,
                            "message": "No active account found with the given credentials"
                        }
                    ]
                }
        else:
            return login_serializer.errors
    except Exception as e:
        return {
            "code": status.HTTP_401_UNAUTHORIZED,
            "message": str(e),
            "status_code": 401,
            "errors": [
                {
                    "status_code": 401,
                    "message": str(e)
                }
            ]
        }
