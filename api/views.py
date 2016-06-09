from rest_framework import filters
from rest_framework import serializers
from rest_framework import viewsets

from .models import NetworkAnalyticsRaw


class NetworkAnalyticsRawSerializer(serializers.ModelSerializer):
    class Meta:
        model = NetworkAnalyticsRaw
        fields = ()


class NetworkAnalyticsRawViewSet(viewsets.ModelViewSet):
    """
    List all trucks, or create a new truck.
    """
    queryset = NetworkAnalyticsRaw.objects.all()

    serializer_class = NetworkAnalyticsRawSerializer
    filter_backends = (filters.DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter,)
