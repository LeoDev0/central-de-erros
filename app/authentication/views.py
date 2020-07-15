from rest_framework import generics, status, permissions
from .serializers import RegisterSerializer, UserSerializer
from rest_framework.response import Response
from .models import User
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from drf_yasg.utils import swagger_auto_schema


class RegisterView(generics.GenericAPIView):
    """
    Cria novo usuário

    * Criação de novo usuário
    """
    serializer_class = RegisterSerializer

    @swagger_auto_schema(responses={
        201: 'Usuário criado com sucesso',
        400: 'Má formatação'
    }, request_body=RegisterSerializer)
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
    serializer_class = UserSerializer

    @swagger_auto_schema(responses={
        200: UserSerializer(many=True),
        401: 'Você não possui credenciais de autenticação válidas',
        403: 'Você não possui permissão para visualizar',
    })
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
    serializer_class = UserSerializer

    @swagger_auto_schema(responses={
        200: UserSerializer(many=True),
        401: 'Você não possui credenciais de autenticação válidas',
        403: 'Você não possui permissão para visualizar',
        404: 'Não encontrado'
    })
    def get(self, request, pk):
        """
        Lista dados de um usuário

        * É preciso estar autenticado como super usuário
        para visualizar (is_staff=True, is_superuser=True).
        """
        queryset = get_object_or_404(User, pk=pk)
        serializer = UserSerializer(queryset)
        return Response(serializer.data)
