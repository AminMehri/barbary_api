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


class Login(APIView):
    def post(self, request):
        # serializer = Serializers.LoginSerializer(data=request.data)
        serializer = serializers.TokenVerifySerializer(data=request.data)
        if serializer.is_valid():
            return Response({'status': 'ok'}, status=status.HTTP_200_OK)
        else:
            return Response({'status': 'nooooooo'}, status=status.HTTP_200_OK)


class ShowBars(APIView):
    def get(self, request):
        serializer = serializers.TokenVerifySerializer(data=request.data)
        if serializer.is_valid():
            bars = []
            for bar in Bar.objects.all():
                bars.append({
                    'beginning': bar.beginning
                })
            return Response({'data': bars}, status=status.HTTP_200_OK)
        else:
            return Response({'status': 'Token is Invalid'}, status=status.HTTP_200_OK)


class ShowBarInfo(APIView):
    def get(self, request):
        try:
            serializer = serializers.TokenVerifySerializer(data=request.data)
            barId = request.data.get('barId')
            barAllInfo = []
            if serializer.is_valid():

                bar = Bar.objects.filter(id=barId)

                if bar:
                    barAllInfo.append({
                        'beginning': bar[0].beginning,
                        'destination': bar[0].destination
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
                print(user)
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
                    return Response({'status': 'ok'}, status=status.HTTP_200_OK)
                else:
                    return Response({'status': 'The Field Required Is Not Accepted.'}, status=status.HTTP_400_BAD_REQUEST)

            else:
                return Response({'token': 'This field is required.'}, status=status.HTTP_400_BAD_REQUEST)

        except TokenError:
            return Response({'status': 'Token is invalid or expired'}, status=status.HTTP_401_UNAUTHORIZED)
        # except:
        #     return Response({'status': 'Internal Server Error'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)