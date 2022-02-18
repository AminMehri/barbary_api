import datetime
import random
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
from kavenegar import *


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
                if not account.isSeeLastNotif:
                    notif = Notification.objects.latest('date')
                    if not notif.immortal:
                        account.isSeeLastNotif = True
                        account.save()

                    notification = [{
                        'title': notif.title,
                        'description': notif.description,
                        'color': notif.color
                    }]
                    return Response({'userInfo': userInfo, 'notification': notification}, status=status.HTTP_200_OK)

                else:
                    return Response({'userInfo': userInfo}, status=status.HTTP_200_OK)

            else:
                return Response({'status': 'Token is Invalid'}, status=status.HTTP_401_UNAUTHORIZED)

        except TokenError:
            return Response({'status': 'Token is invalid or expired'}, status=status.HTTP_401_UNAUTHORIZED)

        # except:
        #     return Response({'status': 'ارور سرور، مشکلی پیش آمده لطفا مجددا امتحان کنید یا به پشتیانی گزارش دهید.'},
        #                     status=status.HTTP_500_INTERNAL_SERVER_ERROR)


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
                        if filterItem not in filteredBars:
                            filteredBars += filterItem

                if destination:
                    isFiltered = True
                    for d in destination:
                        filterItem = Bars.filter(destination=d)
                        if filterItem not in filteredBars:
                            filteredBars += filterItem

                if date:
                    isFiltered = True
                    for i in date:
                        filterItem = Bars.filter(date=i)
                        if filterItem not in filteredBars:
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
                            'description': bar.description if len(bar.description) < 126 else bar.description[
                                                                                              :126] + '...',
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
                        return Response({'status':
                                             '.شما نمیتوانید بار جدید ثبت کنید \n\n فقط شرکت های مورد تایید و متصدیان آنها میتوانند بار ثبت کنند',
                                         'position': account.position}, status=status.HTTP_403_FORBIDDEN)

                    if not account.isAuthenticated:
                        return Response({
                                            'status': 'شما احراز هویت نکردید، از صفحه پروفایل احراز هویت کنید تا بتوانید بار ثبت کنید.'},
                                        status=status.HTTP_403_FORBIDDEN)

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
                    return Response({'status': 'لطفا تمام فیلد هارا به درستی پر کنید.'},
                                    status=status.HTTP_400_BAD_REQUEST)

            else:
                return Response({'token': 'This field is required.'}, status=status.HTTP_400_BAD_REQUEST)

        except TokenError:
            return Response({'status': 'Token is invalid or expired'}, status=status.HTTP_401_UNAUTHORIZED)
        except:
            return Response({'status': 'ارور سرور، مشکلی پیش آمده لطفا مجددا امتحان کنید یا به پشتیانی گزارش دهید.'},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)


def sendMessage(phone_number, message):
    if phone_number and message:
        try:
            api = KavenegarAPI(
                '654E61314E39766367794F746E49723372704E6D38677A64744F7959514F5154426E5876664D6E344D6C6B3D')
            params = {'receptor': '09014743868', 'message': message}
            response = api.sms_send(params)
            return True
        except:
            return Response(
                {'status': 'مشکلی در ارسال پیامک تایید بوجود آمده، لطفا مجددا تلاش کنید'},
                status.HTTP_500_INTERNAL_SERVER_ERROR)


class GetOTP(APIView):
    def post(self, request):
        try:
            serializer = Serializers.OTPSerializer(data=request.data)
            if serializer.is_valid():
                phone_number = request.data.get('phone_number')
                # if user, else create it and account
                user = User.objects.filter(username=phone_number)
                if user:
                    account = Account.objects.get(user=user[0])

                    # sms Validate
                    if account.lastOtpTimeSet + jdatetime.timedelta(seconds=120) > jdatetime.datetime.now():
                        now = jdatetime.datetime.now()
                        last = account.lastOtpTimeSet
                        time_remaining = jdatetime.timedelta(minutes=last.minute + 2 - now.minute, seconds=last.second - now.second)

                        return Response({'status': 'شما هر دو دقیقه یک بار قادر به درخواست کد تایید هستید، لطفا کمی صبر کنید و مجددا امتحان کنید' ,
                                         'time_remaining': time_remaining.seconds * 1000},
                                        status=status.HTTP_429_TOO_MANY_REQUESTS)

                    randomNum = random.randint(1000, 9999)
                    message = f'کد ورود شما به باربر:\n {randomNum}'
                    sendMessage(phone_number, message)
                    account.lastOTP = randomNum
                    account.lastOtpTimeSet = jdatetime.datetime.now()
                    account.save()
                    return Response({'status': 'پیامک تایید ارسال شد'}, status=status.HTTP_200_OK)

                else:
                    newUser = User.objects.create(username=phone_number)
                    randomNum = random.randint(1000, 9999)
                    message = f'کد ورود شما به باربر:\n {randomNum}'
                    acc = Account()
                    acc.user = newUser
                    acc.phone_number = phone_number
                    acc.lastOtpTimeSet = jdatetime.datetime.now()
                    acc.lastOTP = randomNum
                    acc.save()
                    sendMessage(phone_number, message)

                    return Response({'status': 'پیامک تایید ارسال شد'}, status=status.HTTP_200_OK)

            else:
                return Response({'phone_number': 'The Field Is Required.'}, status=status.HTTP_400_BAD_REQUEST)
        except TokenError:
            return Response({'status': 'ارور سرور، مشکلی پیش آمده لطفا مجددا امتحان کنید یا به پشتیانی گزارش دهید.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class Register(APIView):
    def post(self, request):
        try:
            serializer = Serializers.RegisterSerializer(data=request.data)
            if serializer.is_valid():
                phone_number = request.data.get('phone_number')
                OTP = request.data.get('OTP')
                user = User.objects.filter(username=phone_number)
                if user:
                    account = Account.objects.get(user=user[0])
                    if account.lastOtpTimeSet + jdatetime.timedelta(seconds=120) < jdatetime.datetime.now():
                        return Response({'status':
                                'اعتبار ۲ دقیقه ای کد تایید شما گذشته، لطفا مجددا تلاش فرمایید'},
                                        status=status.HTTP_408_REQUEST_TIMEOUT)

                    if account.lastOTP != OTP:
                        return Response({'status':'کد تایید اشتباه است، لطفا مجددا تلاش کنید یا درخواست کد تایید جدید نمایید' ,},
                                        status=status.HTTP_403_FORBIDDEN)

                    refresh = RefreshToken.for_user(user[0])
                    account.lastOTP = ''
                    account.save()
                    if account.first_time:
                        account.first_time = False
                        account.save()
                        return Response({
                            'access': str(refresh.access_token),
                            'refresh': str(refresh),
                            'first_time': True
                        })
                    else:
                        return Response({
                            'access': str(refresh.access_token),
                            'refresh': str(refresh),
                            'isAuthenticated': account.isAuthenticated,
                            'position': account.position,
                            'first_time': False
                        })

                else:
                    return Response({'status':
                            'این شماره تا به حال درخواست کد تایید نکرده، لطفا مجددا درخواست کد تایید کنید یا به پشتیبانی گزارش دهید'},
                                    status=status.HTTP_404_NOT_FOUND)


            else:
                return Response({'status': 'شماره یا کد تایید به درستی وارد نشدند'}, status=status.HTTP_400_BAD_REQUEST)

        except:
            return Response({'status': 'ارور سرور، مشکلی پیش آمده لطفا مجددا امتحان کنید یا به پشتیانی گزارش دهید.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


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
                    return Response({'status': 'The Field Required Is Not Accepted.'},
                                    status=status.HTTP_400_BAD_REQUEST)

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
                today = jdatetime.date.today()
                if barsHistory:
                    for bar in barsHistory:
                        data.append({
                            'beginning': bar.beginning,
                            'destination': bar.destination,
                            'price': bar.price,
                            'fleet_type': bar.fleet_type,
                            'date': str(bar.date),
                            'description': bar.description if len(bar.description) < 126 else bar.description[
                                                                                              :126] + '...',
                            'barId': bar.id,
                            'isPast': True if bar.date < today else False

                        })

                return Response({'data': data}, status=status.HTTP_200_OK)


            else:
                return Response({'token': 'This field is required.'}, status=status.HTTP_400_BAD_REQUEST)

        except TokenError:
            return Response({'status': 'Token is invalid or expired'}, status=status.HTTP_401_UNAUTHORIZED)
        except:
            return Response({'status': 'ارور سرور، مشکلی پیش آمده لطفا مجددا امتحان کنید یا به پشتیانی گزارش دهید.'},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)


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
                        return Response({'status': 'این بار قبلا توسط راننده ای قبول شده'},
                                        status=status.HTTP_400_BAD_REQUEST)

                    if barForAccept.owner_bar != account:

                        if account.isAuthenticated:

                            barForAccept.driver = account
                            barForAccept.save()
                            return Response({'status': 'ok'}, status=status.HTTP_200_OK)
                            # send sms to owner bar

                        else:

                            return Response({'status':
                                'شما احراز هویت نکردید، از صفحه پروفایل احراز هویت کنید تا بتوانید بار را قبول کنید.'},
                                            status=status.HTTP_403_FORBIDDEN)

                    else:
                        return Response({"status": "نمیتوانید بار خودتان را قبول کنید"},
                                        status=status.HTTP_400_BAD_REQUEST)

            else:
                return Response({'token': 'This field is required.'}, status=status.HTTP_400_BAD_REQUEST)

        except TokenError:
            return Response({'status': 'Token is invalid or expired'}, status=status.HTTP_401_UNAUTHORIZED)
        except:
            return Response({'status': 'ارور سرور، مشکلی پیش آمده لطفا مجددا امتحان کنید یا به پشتیانی گزارش دهید.'},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class SubmitPosition(APIView):
    def post(self, request):

        try:
            TokenSerializer = serializers.TokenVerifySerializer(data=request.data)
            serializer = Serializers.SubmitPositionSerializer(data=request.data)

            if TokenSerializer.is_valid():
                user = User.objects.get(id=AccessToken(request.data.get('token'))['user_id'])
                account = Account.objects.get(user=user)

                if account.position:
                    return Response({
                                        'status': 'شما قبلا موقعیت شغلی خودرا انتخاب کردید. اگر میخواهید آنرا تغییر دهید با پشتیبانی تماس بگیرید.'},
                                    status=status.HTTP_400_BAD_REQUEST)

                if serializer.is_valid():
                    position = request.data.get('position')
                    account.position = position
                    account.save()
                    return Response({'status': 'ok'}, status=status.HTTP_200_OK)

                else:
                    return Response({'status': 'لطفا موقعیت شغلی خودرا انتخاب کنید.'},
                                    status=status.HTTP_400_BAD_REQUEST)

            else:
                return Response({'token': 'This field is required.'}, status=status.HTTP_400_BAD_REQUEST)

        except TokenError:
            return Response({'status': 'Token is invalid or expired'}, status=status.HTTP_401_UNAUTHORIZED)
        except:
            return Response({'status': 'ارور سرور، مشکلی پیش آمده لطفا مجددا امتحان کنید یا به پشتیانی گزارش دهید.'},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class GetDate(APIView):
    def get(self, request):
        today = jdatetime.date.today()
        afterTomorrow = today + jdatetime.timedelta(2)
        twoAfterTomorrow = today + jdatetime.timedelta(3)
        threeAfterTomorrow = today + jdatetime.timedelta(4)

        dayData = [{
            'afterTomorrow': jdatetime.date.j_weekdays_fa[afterTomorrow.weekday()] + ' ' + str(
                afterTomorrow.day) + ' ' + jdatetime.date.j_months_fa[afterTomorrow.month - 1],
            'twoAfterTomorrow': jdatetime.date.j_weekdays_fa[twoAfterTomorrow.weekday()] + ' ' + str(
                twoAfterTomorrow.day) + ' ' + jdatetime.date.j_months_fa[twoAfterTomorrow.month - 1],
            'threeAfterTomorrow': jdatetime.date.j_weekdays_fa[threeAfterTomorrow.weekday()] + ' ' + str(
                threeAfterTomorrow.day) + ' ' + jdatetime.date.j_months_fa[threeAfterTomorrow.month - 1],
            'today': str(today),
            'tomorrow': str(today + jdatetime.timedelta(1)),
            'tomorrow1': str(afterTomorrow),
            'tomorrow2': str(twoAfterTomorrow),
            'tomorrow3': str(threeAfterTomorrow),
        }]
        return Response(dayData)


class SendSMS(APIView):
    def post(self, request):
        try:
            TokenSerializer = serializers.TokenVerifySerializer(data=request.data)

            if TokenSerializer.is_valid():
                user = User.objects.get(id=AccessToken(request.data.get('token'))['user_id'])
                # account = Account.objects.get(user=user)
                try:
                    api = KavenegarAPI(
                        '654E61314E39766367794F746E49723372704E6D38677A64744F7959514F5154426E5876664D6E344D6C6B3D')
                    params = {'receptor': '09014743868', 'message': '.وب سرویس پیام کوتاه کاوه نگار'}
                    response = api.sms_send(params)
                    print('response is:', response)
                except APIException as e:
                    print(e)
                    return Response(str(e), status.HTTP_500_INTERNAL_SERVER_ERROR)
                except HTTPException as e:
                    print(e)
                    return Response(str(e), status.HTTP_500_INTERNAL_SERVER_ERROR)

                return Response({'status': 'sended successfuly'}, status=status.HTTP_200_OK)

            else:
                return Response({'token': 'This field is required.'}, status=status.HTTP_400_BAD_REQUEST)

        except TokenError:
            return Response({'status': 'Token is invalid or expired'}, status=status.HTTP_401_UNAUTHORIZED)
