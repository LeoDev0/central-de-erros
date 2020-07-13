from django.shortcuts import render
from rest_framework import generics, status, permissions
from .serializers import RegisterSerializer, UserSerializer
from rest_framework.response import Response
from .models import User
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404


class RegisterView(generics.GenericAPIView):
    """Criação de novo usuário"""
    serializer_class = RegisterSerializer

    def post(self, request):
        user = request.data
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        user_data = serializer.data

        return Response(user_data, status.HTTP_201_CREATED) 


class ListUsersView(APIView):

    permission_classes = [
        permissions.IsAuthenticated,
        permissions.IsAdminUser,
    ]

    def get(self, request):
        """
        Lista todos os usuários

        * É preciso estar autenticado como super usuário
        para visualizar (is_staff=True, is_superuser=True).
        """

        queryset = User.objects.all() 
        serializer = UserSerializer(queryset, many=True)
        return Response(serializer.data)


class SingleUserView(APIView):

    permission_classes = [
        permissions.IsAuthenticated,
        permissions.IsAdminUser,
    ]

    def get(self, request, pk):
        """
        Lista dados de um usuário

        * É preciso estar autenticado como super usuário
        para visualizar (is_staff=True, is_superuser=True).
        """
        queryset = get_object_or_404(User, pk=pk)
        serializer = UserSerializer(queryset)
        return Response(serializer.data)
