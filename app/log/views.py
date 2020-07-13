from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import (
    authentication,
    permissions, 
    status, 
    filters, 
    generics,
)
from .models import Log
from .serializers import LogSerializer
from django.shortcuts import get_object_or_404
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


class SearchLogsView(generics.ListAPIView):
    """
    Pesquisa logs pelos campos 'description' e 'details'
    usando o parâmetro '?search='

    * É preciso estar autenticado para pesquisar
    """
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = LogSerializer

    search_fields = ['description', 'details']
    filter_backends = (filters.SearchFilter,)
    queryset = Log.objects.all()
    serializer_class = LogSerializer


class ListLogsView(APIView):

    permission_classes = [permissions.IsAuthenticated]
    serializer_class = LogSerializer

    @swagger_auto_schema(
        responses={200: LogSerializer(many=True),
                   401: 'Você não possui credenciais de autenticação válidas',}
    )
    def get(self, request):
        """
        Lista todos os logs

        * É preciso estar autenticado para visualizar
        """
        queryset = Log.objects.all()
        serializer = LogSerializer(queryset, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(
        responses={201: LogSerializer(),
                   401: 'Você não possui credenciais de autenticação válidas',
                   400: 'Má formatação'},
        request_body=LogSerializer   
    )
    def post(self, request):
        """
        Cria novo log

        * É preciso estar autenticado para criar
        """

        serializer = LogSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)


class SingleLogView(APIView):

    permission_classes = [permissions.IsAuthenticated]
    serializer_class = LogSerializer

    @swagger_auto_schema(
        responses={200: LogSerializer(),
                   401: 'Você não possui credenciais de autenticação válidas',
                   404: 'Não encontrado'}
    )
    def get(self, request, pk):
        """
        Lista detalhes do log

        * É preciso estar autenticado para visualizar
        """
        queryset = get_object_or_404(Log, pk=pk)
        serializer = LogSerializer(queryset)
        return Response(serializer.data)

    @swagger_auto_schema(
        responses={202: LogSerializer(),
                   400: 'Má formatação',
                   401: 'Você não possui credenciais de autenticação válidas',
                   404: 'Não encontrado'},
        request_body=LogSerializer   
    )
    def put(self, request, pk):
        """
        Edita todos os itens do log

        * É preciso estar autenticado para editar
        """
        queryset = get_object_or_404(Log, pk=pk)
        serializer = LogSerializer(queryset, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        return Response(status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        responses={202: LogSerializer(),
                   400: 'Má formatação',
                   401: 'Você não possui credenciais de autenticação válidas',
                   404: 'Não encontrado'},
        request_body=LogSerializer   
    )
    def patch(self, request, pk):
        """
        Edita parcialmente o log

        * É preciso estar autenticado para editar
        """
        queryset = get_object_or_404(Log, pk=pk)
        serializer = LogSerializer(queryset, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        return Response(status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(responses={204: 'Sem conteúdo',
                                    401: 'Você não possui credenciais de autenticação válidas',
                                    404: 'Não encontrado'})
    def delete(self, request, pk):
        """
        Deleta um log

        * É preciso estar autenticado para deletar
        """
        queryset = get_object_or_404(Log, pk=pk)
        queryset.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
