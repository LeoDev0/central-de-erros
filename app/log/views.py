from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions
from .models import Log
from .serializers import LogSerializer
from django.shortcuts import get_object_or_404
from rest_framework import status


# Create your views here.
class ListLogsView(APIView):

    def get(self, request):
        """
        Lista todos os logs

        * É preciso estar autenticado para visualizar
        """
        queryset = Log.objects.all()
        serializer = LogSerializer(queryset, many=True)
        return Response(serializer.data)

    def post(self, request):
        """
        Criar novo log

        * É preciso estar autenticado para criar
        """
        serializer = LogSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)


class DetailLogView(APIView):

    def get(self, request, pk):
        """
        Lista detalhes do log

        * É preciso estar autenticado para visualizar
        """
        queryset = get_object_or_404(Log, pk=pk)
        serializer = LogSerializer(queryset)
        return Response(serializer.data)

    def put(self, request, pk):
        """
        Edita todos os itens do log

        * É preciso estar autenticado para editar
        """
        queryset = get_object_or_404(Log, pk=pk)
        serializer = LogSerializer(queryset, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_202_ACCEPTED)
        return Response(status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk):
        """
        Edita parcialmente o log

        * É preciso estar autenticado para editar
        """
        queryset = get_object_or_404(Log, pk=pk)
        serializer = LogSerializer(queryset, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_202_ACCEPTED)
        return Response(status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        """
        Deleta um log

        * É preciso estar autenticado para deletar
        """
        queryset = get_object_or_404(Log, pk=pk)
        queryset.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)