import datetime
import jdatetime
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


class Verify(APIView):
    def post(self, request):
        try:
            serializer = serializers.TokenVerifySerializer(data=request.data)
            if serializer.is_valid():
                user = User.objects.get(id=AccessToken(request.data.get('token'))['user_id'])
                account = Account.objects.get(user=user)

                if account.name:
                    userInfo = [{
                            'name': account.name,
                            'position': account.position,
                            'isAuthenticated': account.isAuthenticated,
                        }]
                else:
                    userInfo = [{
                        'position': account.position,
                        'phone_number': account.phone_number,
                        'isAuthenticated': account.isAuthenticated,
                    }]

                return Response({'userInfo': userInfo}, status=status.HTTP_200_OK)
            else:
                return Response({'status': 'Token is Invalid'}, status=status.HTTP_401_UNAUTHORIZED)

        except TokenError:
            return Response({'status': 'Token is invalid or expired'}, status=status.HTTP_401_UNAUTHORIZED)

        except:
            return Response({'status': 'ارور سرور، مشکلی پیش آمده لطفا مجددا امتحان کنید یا به پشتیانی گزارش دهید.'},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ShowBars(APIView):
    def post(self, request):
        try:
            serializer = serializers.TokenVerifySerializer(data=request.data)
            if serializer.is_valid():
                bars = []
                Bars = Bar.objects.all().order_by('date').order_by('-isTopShow')
                fleetType = request.data.get('fleetType')
                destination = request.data.get('destination')
                date = request.data.get('date')
                isFiltered = False
                filteredBars = []

                if fleetType:
                    isFiltered = True
                    for f in fleetType:
                        filterItem = Bars.filter(fleet_type=f)
                        if filterItem[0] not in filteredBars:
                            filteredBars += filterItem

                if destination:
                    isFiltered = True
                    for d in destination:
                        filterItem = Bars.filter(destination=d)
                        if filterItem[0] not in filteredBars:
                            filteredBars += filterItem

                if date:
                    print(date)
                    isFiltered = True
                    for i in date:
                        filterItem = Bars.filter(date=i)
                        if filterItem[0] not in filteredBars:
                            filteredBars += filterItem

                if isFiltered:
                    f = filteredBars
                else:
                    f = Bars

                for bar in f:

                    if not bar.driver:
                        bars.append({
                            'beginning': bar.beginning,
                            'destination': bar.destination,
                            'price': bar.price,
                            'fleet_type': bar.fleet_type,
                            'description': bar.description if len(bar.description) < 126 else bar.description[:126] + '...',
                            'barId': bar.id,
                            'isSpecial': bar.isSpecial,
                        })

                return Response({'data': bars}, status=status.HTTP_200_OK)
            else:
                return Response({'status': 'Token is Invalid'}, status=status.HTTP_401_UNAUTHORIZED)

        except TokenError:
            return Response({'status': 'Token is invalid or expired'}, status=status.HTTP_401_UNAUTHORIZED)

        # except:
        #     return Response({'status': 'ارور سرور، مشکلی پیش آمده لطفا مجددا امتحان کنید یا به پشتیانی گزارش دهید.'},
        #                     status=status.HTTP_500_INTERNAL_SERVER_ERROR)


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
                        'date': str(bar[0].date),
                        'weight': bar[0].weight,
                        'product_type': bar[0].product_type,
                        'fleet_type': bar[0].fleet_type,
                        'description': bar[0].description,
                        'owner_bar': bar[0].owner_bar.name,
                        'phone_number': bar[0].phone_number,
                        'barId': bar[0].id,
                        'isSpecial': bar[0].isSpecial,
                    })
                    return Response({'data': barAllInfo}, status=status.HTTP_200_OK)

                else:
                    return Response({'status': 'Bar Not Found'}, status=status.HTTP_404_NOT_FOUND)

            else:
                return Response({'token': 'This field is required.'}, status=status.HTTP_400_BAD_REQUEST)

        except TokenError:
            return Response({'status': 'Token is invalid or expired'}, status=status.HTTP_401_UNAUTHORIZED)

        except:
            return Response({'status': 'ارور سرور، مشکلی پیش آمده لطفا مجددا امتحان کنید یا به پشتیانی گزارش دهید.'},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)


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

        except:
            return Response({'status': 'ارور سرور، مشکلی پیش آمده لطفا مجددا امتحان کنید یا به پشتیانی گزارش دهید.'},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class AddBar(APIView):
    def post(self, request):

        try:
            TokenSerializer = serializers.TokenVerifySerializer(data=request.data)
            serializer = Serializers.AddBarSerializer(data=request.data)
            if TokenSerializer.is_valid():

                if serializer.is_valid():
                    user = User.objects.get(id=AccessToken(request.data.get('token'))['user_id'])
                    account = Account.objects.get(user=user)

                    if account.position != 'manager':
                        return Response({'status': '.شما نمیتوانید بار جدید ثبت کنید \n\n فقط شرکت های مورد تایید و متصدیان آنها میتوانند بار ثبت کنند', 'position': account.position}, status=status.HTTP_403_FORBIDDEN)

                    if not account.isAuthenticated:
                        return Response({'status': 'شما احراز هویت نکردید، از صفحه پروفایل احراز هویت کنید تا بتوانید بار ثبت کنید.'}, status=status.HTTP_403_FORBIDDEN)

                    beginning = request.data.get('beginning')
                    destination = request.data.get('destination')
                    price = request.data.get('price')
                    date = request.data.get('date')
                    weight = request.data.get('weight')
                    product_type = request.data.get('product_type')
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
                    account = Account.objects.filter(user=user[0])[0]
                    return Response({
                        'refresh': str(refresh),
                        'access': str(refresh.access_token),
                        'isAuthenticated': account.isAuthenticated,
                        'position': account.position,
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
                        'first_time': True
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
                    BarId = request.data.get('barId')
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
                    bar.fleet_type = fleet_type
                    bar.owner_bar = owner_bar
                    bar.description = description
                    bar.phone_number = owner_bar.phone_number
                    bar.save()
                    return Response({'status': 'ok'}, status=status.HTTP_200_OK)
                else:
                    return Response({'status': 'فیلدهای ضروری را به درستی پر کنید'}, status=status.HTTP_400_BAD_REQUEST)

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
                            'date': str(bar.date),
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

                    if barForAccept.driver:
                        return Response({'status': 'این بار قبلا توسط راننده ای قبول شده'}, status=status.HTTP_400_BAD_REQUEST)

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


class SubmitPosition(APIView):
    def post(self, request):

        try:
            TokenSerializer = serializers.TokenVerifySerializer(data=request.data)
            serializer = Serializers.SubmitPositionSerializer(data=request.data)

            if TokenSerializer.is_valid():
                user = User.objects.get(id=AccessToken(request.data.get('token'))['user_id'])
                account = Account.objects.get(user=user)

                if account.position:
                    return Response({'status': 'شما قبلا موقعیت شغلی خودرا انتخاب کردید. اگر میخواهید آنرا تغییر دهید با پشتیبانی تماس بگیرید.'}, status=status.HTTP_400_BAD_REQUEST)

                if serializer.is_valid():
                    position = request.data.get('position')
                    account.position = position
                    account.save()
                    return Response({'status': 'ok'}, status=status.HTTP_200_OK)

                else:
                    return Response({'status': 'لطفا موقعیت شغلی خودرا انتخاب کنید.'}, status=status.HTTP_400_BAD_REQUEST)

            else:
                return Response({'token': 'This field is required.'}, status=status.HTTP_400_BAD_REQUEST)

        except TokenError:
            return Response({'status': 'Token is invalid or expired'}, status=status.HTTP_401_UNAUTHORIZED)
        except:
            return Response({'status': 'ارور سرور، مشکلی پیش آمده لطفا مجددا امتحان کنید یا به پشتیانی گزارش دهید.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class GetDate(APIView):
    def get(self, request):

        today = jdatetime.date.today()
        afterTomorrow = today + jdatetime.timedelta(2)
        twoAfterTomorrow = today + jdatetime.timedelta(3)
        threeAfterTomorrow = today + jdatetime.timedelta(4)

        dayData = [{
            'afterTomorrow': jdatetime.date.j_weekdays_fa[afterTomorrow.weekday()] + ' ' + str(afterTomorrow.day) + ' ' + jdatetime.date.j_months_fa[afterTomorrow.month - 1],
            'twoAfterTomorrow': jdatetime.date.j_weekdays_fa[twoAfterTomorrow.weekday()] + ' ' + str(twoAfterTomorrow.day) + ' ' + jdatetime.date.j_months_fa[twoAfterTomorrow.month - 1],
            'threeAfterTomorrow': jdatetime.date.j_weekdays_fa[threeAfterTomorrow.weekday()] + ' ' + str(threeAfterTomorrow.day) + ' ' + jdatetime.date.j_months_fa[threeAfterTomorrow.month - 1],
            'today': str(today),
            'tomorrow': str(today + jdatetime.timedelta(1)),
            'tomorrow1': str(afterTomorrow),
            'tomorrow2': str(twoAfterTomorrow),
            'tomorrow3': str(threeAfterTomorrow),
        }]
        return Response(dayData)
