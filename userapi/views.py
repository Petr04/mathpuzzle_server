from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.generics import RetrieveUpdateDestroyAPIView
from rest_framework.views import APIView

from .models import User
from .serializers import LoginSerializer, RegistrationSerializer, \
    UserDataSerializer


class RegistrationAPIView(APIView):
    permission_classes = [AllowAny]
    serializer_class = RegistrationSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response({
            'token': serializer.data.get('token', None)
        }, status=status.HTTP_201_CREATED)


class LoginAPIView(APIView):
    permission_classes = [AllowAny]
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


class UserDataAPIView(RetrieveUpdateDestroyAPIView):
    permission_classes = [AllowAny]
    serializer_class = UserDataSerializer
    queryset = User.objects.all()
    lookup_field = 'username'


class IsRegistered(APIView): # is username registered
    permission_classes = [AllowAny]
    def get(self, request):
        data = dict([list(request.GET.items())[0]])
        users = User.objects.filter(**data)
        return Response({
            "is_registered": users.count() > 0
        })
