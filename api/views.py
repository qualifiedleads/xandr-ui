from django.http import Http404
from rest_framework import status
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework.views import APIView
from django.core.paginator import Paginator

from .models import TestModel
from .serializers import TestModelSerializer


class TestList(APIView):
    """
    List all trucks, or create a new truck.
    """

    def get(self, request, format=None):
        
        result = TestModel.objects.all()

        serializer = TestModelSerializer(result, many=True)

        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = TestModelSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TestDetail(APIView):
    """
    Retrieve, update or delete a truck instance.
    """

    def get_object(self, pk):
        try:
            return TestModel.objects.get(pk=pk)
        except TestModel.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        result = self.get_object(pk)
        serializer = TruckSerializer(result)

        return Response(serializer.data)

    def put(self, request, pk, format=None):
        snippet = self.get_object(pk)
        serializer = TestModelSerializer(snippet, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        result = self.get_object(pk)
        result.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
