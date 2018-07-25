from django.contrib.auth import authenticate, login, logout
from django.utils import timezone
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

from .serializers import (
    UserSerializer, CreateUserSerializer, LoginUserSerializer
)


class UserView(GenericAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = UserSerializer

    def get(self, request, *args, **kwargs):
        return Response(self.get_serializer(request.user).data,
                        status=status.HTTP_200_OK)


class CreateUserView(GenericAPIView):
    permission_classes = (AllowAny,)
    serializer_class = CreateUserSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            if user:
                data = UserSerializer(user,
                                      context=self.get_serializer_context()).data
                return Response(data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)


class LoginUserView(GenericAPIView):
    permission_classes = (AllowAny,)
    serializer_class = LoginUserSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            password = serializer.validated_data['password']
            company = serializer.validated_data['auth_company']

            user = authenticate(
                email=email,
                password=password
            )
            if user:
                request.session['company'] = company
                login(request, user)

                token, created = Token.objects.get_or_create(user=user)

                if not created:
                    token.created = timezone.now()
                    token.save()

                data = {'key': token.key}
                return Response(data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)


class LogoutUserView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        request.user.auth_token.delete()
        logout(request)
        return Response(status=status.HTTP_200_OK)
