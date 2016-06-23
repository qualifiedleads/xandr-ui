from rest_framework import filters
from rest_framework import serializers
from rest_framework import viewsets
from django.http import JsonResponse

from .models import NetworkAnalyticsRaw, User

def stats(request):
    return JsonResponse({"message":"hello, world"})


class NetworkAnalyticsRawSerializer(serializers.ModelSerializer):
    class Meta:
        model = NetworkAnalyticsRaw
        fields = ()


class UsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class NetworkAnalyticsRawViewSet(viewsets.ModelViewSet):
    queryset = NetworkAnalyticsRaw.objects.all()

    serializer_class = NetworkAnalyticsRawSerializer
    filter_backends = (filters.DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter,)

class UsersViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()

    serializer_class = UsersSerializer
