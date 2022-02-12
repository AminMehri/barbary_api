from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from .models import *
from . import serializer as Serializers
from rest_framework_simplejwt import serializers
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import TokenError
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework_simplejwt.tokens import RefreshToken


class Login(APIView):
    def post(self, request):
        # serializer = Serializers.LoginSerializer(data=request.data)
        serializer = serializers.TokenVerifySerializer(data=request.data)
        if serializer.is_valid():
            return Response({'status': 'ok'}, status=status.HTTP_200_OK)
        else:
            return Response({'status': 'nooooooo'}, status=status.HTTP_401_UNAUTHORIZED)


class ShowBars(APIView):
    def post(self, request):
        serializer = serializers.TokenVerifySerializer(data=request.data)
        if serializer.is_valid():
            bars = []
            for bar in Bar.objects.all():
                bars.append({
                    'beginning': bar.beginning,
                    'destination': bar.destination,
                    'price': bar.price,
                    'fleet_type': bar.fleet_type,
                    'description': bar.description if len(bar.description) < 126 else bar.description[:126] + '...',
                    'barId': bar.id,
                })
            return Response({'data': bars}, status=status.HTTP_200_OK)
        else:
            print(request.data.get('token'))
            return Response({'status': 'Token is Invalid'}, status=status.HTTP_401_UNAUTHORIZED)


class ShowBarInfo(APIView):
    def post(self, request):
        try:
            serializer = serializers.TokenVerifySerializer(data=request.data)
            barId = request.data.get('barId')
            barAllInfo = []
            if serializer.is_valid():

                bar = Bar.objects.filter(id=barId)

                if bar:
                    barAllInfo.append({
                        'beginning': bar[0].beginning,
                        'destination': bar[0].destination,
                        'price': bar[0].price,
                        'date': bar[0].date,
                        'weight': bar[0].weight,
                        'product_type': bar[0].product_type,
                        'product_packaging': bar[0].product_packaging,
                        'fleet_type': bar[0].fleet_type,
                        'description': bar[0].description,
                        'owner_bar': bar[0].owner_bar.name,
                        'phone_number': bar[0].phone_number,
                        'barId': bar[0].id,
                    })
                    return Response({'data': barAllInfo}, status=status.HTTP_200_OK)

                else:
                    return Response({'status': 'Bar Not Found'}, status=status.HTTP_404_NOT_FOUND)

            else:
                return Response({'token': 'This field is required.'}, status=status.HTTP_400_BAD_REQUEST)

        except TokenError:
            return Response({'status': 'Token is invalid or expired'}, status=status.HTTP_401_UNAUTHORIZED)


class UpdateUserInfo(APIView):
    def get(self, request):
        try:
            serializer = serializers.TokenVerifySerializer(data=request.data)

            if serializer.is_valid():
                token = request.data.get('token')
                access_token = AccessToken(token)
                user = User.objects.get(id=access_token['user_id'])
                account = Account.objects.get(user=user)
                account.address = 'testAddress'
                account.save()
                return Response(status=status.HTTP_200_OK)

            else:
                return Response({'token': 'This field is required.'}, status=status.HTTP_400_BAD_REQUEST)

        except TokenError:
            return Response({'status': 'Token is invalid or expired'}, status=status.HTTP_401_UNAUTHORIZED)


class AddBar(APIView):
    def post(self, request):

        try:
            TokenSerializer = serializers.TokenVerifySerializer(data=request.data)
            serializer = Serializers.AddBarSerializer(data=request.data)
            if TokenSerializer.is_valid():

                if serializer.is_valid():
                    user = User.objects.get(id=AccessToken(request.data.get('token'))['user_id'])
                    account = Account.objects.get(user=user)

                    if not account.isAuthenticated:
                        return Response({'status': 'شما احراز هویت نکردید، از صفحه پروفایل احراز هویت کنید تا بتوانید بار را قبول کنید.'}, status=status.HTTP_403_FORBIDDEN)

                    beginning = request.data.get('beginning')
                    destination = request.data.get('destination')
                    price = request.data.get('price')
                    date = request.data.get('date')
                    weight = request.data.get('weight')
                    product_type = request.data.get('product_type')
                    product_packaging = request.data.get('product_packaging')
                    fleet_type = request.data.get('fleet_type')
                    owner_bar = Account.objects.get(user=user)
                    description = request.data.get('description')

                    bar = Bar()
                    bar.beginning = beginning
                    bar.destination = destination
                    bar.price = price
                    bar.date = date
                    bar.weight = weight
                    bar.product_type = product_type
                    bar.product_packaging = product_packaging
                    bar.fleet_type = fleet_type
                    bar.owner_bar = owner_bar
                    bar.description = description
                    bar.phone_number = owner_bar.phone_number
                    bar.save()
                    return Response({'status': 'ok'}, status=status.HTTP_201_CREATED)
                else:
                    return Response({'status': 'لطفا تمام فیلد هارا به درستی پر کنید.'}, status=status.HTTP_400_BAD_REQUEST)

            else:
                return Response({'token': 'This field is required.'}, status=status.HTTP_400_BAD_REQUEST)

        except TokenError:
            return Response({'status': 'Token is invalid or expired'}, status=status.HTTP_401_UNAUTHORIZED)
        except:
            return Response({'status': 'ارور سرور، مشکلی پیش آمده لطفا مجددا امتحان کنید یا به پشتیانی گزارش دهید.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class Register(APIView):
    def post(self, request):
        try:
            serializer = Serializers.RegisterSerializer(data=request.data)
            if serializer.is_valid():
                phone_number = request.data.get('phone_number')
                user = User.objects.filter(username=phone_number)
                if user:
                    # sms Validate
                    refresh = RefreshToken.for_user(user[0])

                    return Response({
                        'refresh': str(refresh),
                        'access': str(refresh.access_token),
                        'isAuthenticated': Account.objects.filter(user=user[0])[0].isAuthenticated,
                    })

                else:
                    # sms Validate

                    newUser = User.objects.create(username=phone_number)
                    acc = Account()
                    acc.user = newUser
                    acc.phone_number = phone_number
                    acc.save()

                    refresh = RefreshToken.for_user(newUser)

                    return Response({
                        'refresh': str(refresh),
                        'access': str(refresh.access_token),
                    })

            else:
                return Response({'phone_number': 'The Field Is Required.'}, status=status.HTTP_400_BAD_REQUEST)

        except:
            return Response({'status': 'Internal Server Error'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class UpdateBar(APIView):
    def post(self, request):

        try:
            TokenSerializer = serializers.TokenVerifySerializer(data=request.data)
            serializer = Serializers.UpdateBarSerializer(data=request.data)
            if TokenSerializer.is_valid():

                if serializer.is_valid():
                    user = User.objects.get(id=AccessToken(request.data.get('token'))['user_id'])
                    account = Account.objects.get(user=user)
                    BarId = request.data.get('BarId')
                    try:
                        editBar = Bar.objects.get(id=BarId)
                    except:
                        return Response({'Not Found': 'Bar Not Found'}, status=status.HTTP_404_NOT_FOUND)

                    if not account.isAuthenticated or editBar.owner_bar != account:
                        return Response({'Not Access'}, status=status.HTTP_403_FORBIDDEN)

                    beginning = request.data.get('beginning')
                    destination = request.data.get('destination')
                    price = request.data.get('price')
                    date = request.data.get('date')
                    weight = request.data.get('weight')
                    product_type = request.data.get('product_type')
                    product_packaging = request.data.get('product_packaging')
                    fleet_type = request.data.get('fleet_type')
                    owner_bar = Account.objects.get(user=user)
                    description = request.data.get('description')

                    bar = editBar
                    bar.beginning = beginning
                    bar.destination = destination
                    bar.price = price
                    bar.date = date
                    bar.weight = weight
                    bar.product_type = product_type
                    bar.product_packaging = product_packaging
                    bar.fleet_type = fleet_type
                    bar.owner_bar = owner_bar
                    bar.description = description
                    bar.phone_number = owner_bar.phone_number
                    bar.save()
                    return Response({'status': 'ok'}, status=status.HTTP_200_OK)
                else:
                    return Response({'status': 'The Field Required Is Not Accepted.'}, status=status.HTTP_400_BAD_REQUEST)

            else:
                return Response({'token': 'This field is required.'}, status=status.HTTP_400_BAD_REQUEST)

        except TokenError:
            return Response({'status': 'Token is invalid or expired'}, status=status.HTTP_401_UNAUTHORIZED)
        except:
            return Response({'status': 'Internal Server Error'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class RemoveBar(APIView):
    def post(self, request):

        try:
            TokenSerializer = serializers.TokenVerifySerializer(data=request.data)
            serializer = Serializers.BarIdSerializer(data=request.data)
            if TokenSerializer.is_valid():

                if serializer.is_valid():
                    user = User.objects.get(id=AccessToken(request.data.get('token'))['user_id'])
                    account = Account.objects.get(user=user)
                    BarId = request.data.get('barId')
                    try:
                        removeBar = Bar.objects.get(id=BarId)
                    except:
                        return Response({'Not Found': 'بار مورد نظر یافت نشد'}, status=status.HTTP_404_NOT_FOUND)

                    if not account.isAuthenticated or removeBar.owner_bar != account:
                        return Response({'status': 'شما اجازه حذف این بار را ندارید'}, status=status.HTTP_403_FORBIDDEN)

                    removeBar.delete()

                    return Response({'status': 'ok'}, status=status.HTTP_200_OK)

                else:
                    return Response({'status': 'The Field Required Is Not Accepted.'}, status=status.HTTP_400_BAD_REQUEST)

            else:
                return Response({'token': 'This field is required.'}, status=status.HTTP_400_BAD_REQUEST)

        except TokenError:
            return Response({'status': 'Token is invalid or expired'}, status=status.HTTP_401_UNAUTHORIZED)
        except:
            return Response({'status': 'Internal Server Error'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ShowUserBarHistory(APIView):
    def post(self, request):

        try:
            TokenSerializer = serializers.TokenVerifySerializer(data=request.data)
            if TokenSerializer.is_valid():

                user = User.objects.get(id=AccessToken(request.data.get('token'))['user_id'])
                account = Account.objects.get(user=user)

                barsHistory = Bar.objects.filter(owner_bar=account)

                data = []

                if barsHistory:
                    for bar in barsHistory:
                        data.append({
                            'beginning': bar.beginning,
                            'destination': bar.destination,
                            'price': bar.price,
                            'fleet_type': bar.fleet_type,
                            'date': bar.date,
                            'description': bar.description if len(bar.description) < 126 else bar.description[:126] + '...',
                            'barId': bar.id,

                        })

                return Response({'data': data}, status=status.HTTP_200_OK)


            else:
                return Response({'token': 'This field is required.'}, status=status.HTTP_400_BAD_REQUEST)

        except TokenError:
            return Response({'status': 'Token is invalid or expired'}, status=status.HTTP_401_UNAUTHORIZED)
        except:
            return Response({'status': 'ارور سرور، مشکلی پیش آمده لطفا مجددا امتحان کنید یا به پشتیانی گزارش دهید.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class AcceptBar(APIView):
    def post(self, request):

        try:
            TokenSerializer = serializers.TokenVerifySerializer(data=request.data)
            serializer = Serializers.BarIdSerializer(data=request.data)

            if TokenSerializer.is_valid():

                if serializer.is_valid():
                    user = User.objects.get(id=AccessToken(request.data.get('token'))['user_id'])
                    account = Account.objects.get(user=user)
                    BarId = request.data.get('barId')

                    try:
                        barForAccept = Bar.objects.get(id=BarId)

                    except:
                        return Response({'status': 'بار مورد نظر پیدا نشد'}, status=status.HTTP_404_NOT_FOUND)

                    if barForAccept.owner_bar != account:

                        if account.isAuthenticated:

                            barForAccept.driver = account
                            barForAccept.save()
                            return Response({'status': 'ok'}, status=status.HTTP_200_OK)
                            # send sms to owner bar

                        else:

                            return Response({'status': 'شما احراز هویت نکردید، از صفحه پروفایل احراز هویت کنید تا بتوانید بار را قبول کنید.'}, status=status.HTTP_403_FORBIDDEN)

                    else:
                        return Response({"status": "نمیتوانید بار خودتان را قبول کنید!"}, status=status.HTTP_400_BAD_REQUEST)

            else:
                return Response({'token': 'This field is required.'}, status=status.HTTP_400_BAD_REQUEST)

        except TokenError:
            return Response({'status': 'Token is invalid or expired'}, status=status.HTTP_401_UNAUTHORIZED)
        except:
            return Response({'status': 'ارور سرور، مشکلی پیش آمده لطفا مجددا امتحان کنید یا به پشتیانی گزارش دهید.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


