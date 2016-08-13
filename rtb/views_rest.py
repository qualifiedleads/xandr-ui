from django.contrib.admin.templatetags.admin_list import result_headers
from rest_framework import filters
from rest_framework import serializers
from rest_framework import viewsets
from rest_framework.permissions import IsAdminUser
from rest_framework.exceptions import PermissionDenied

from .models import NetworkAnalyticsRaw, FrameworkUser, Advertiser, User
from django.contrib.auth.hashers import PBKDF2PasswordHasher, make_password, is_password_usable


class AdvertiserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Advertiser
        fields = '__all__'

#generics.ListAPIView
class AdvertiserViewSet(viewsets.ModelViewSet):
    queryset = Advertiser.objects.all()

    serializer_class = AdvertiserSerializer


    def get_queryset(self):
        """
        This view should return a list of all the purchases
        for the currently authenticated user.
        """
        user = self.request.user
        #return Advertiser.objects.filter(purchaser=user)
        return Advertiser.objects.all()


class NetworkAnalyticsRawSerializer(serializers.ModelSerializer):
    class Meta:
        model = NetworkAnalyticsRaw
        fields = '__all__'#()


class UsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = FrameworkUser
        fields = '__all__'


class AppnexusUsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class NetworkAnalyticsRawViewSet(viewsets.ModelViewSet):
    queryset = NetworkAnalyticsRaw.objects.all()

    serializer_class = NetworkAnalyticsRawSerializer
    filter_backends = (filters.DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter,)


class UsersViewSet(viewsets.ModelViewSet):
    queryset = FrameworkUser.objects.all()
    # PBKDF2PasswordHasher
    serializer_class = UsersSerializer
    permission_classes = (IsAdminUser,)

    def transform_password(self, request):
        if 'password' in request.data:
            password = request.data['password']
            if not is_password_usable(password):
                request.data['password'] = make_password(password)

    def create(self, request, *args, **kwargs):
        if not request.user.is_superuser:
            raise PermissionDenied('For create new users, current user must be a superuser');
        self.transform_password(request)
        return super(UsersViewSet, self).create(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        if not request.user.is_superuser:
            raise PermissionDenied('For update users data, current user must be a superuser');
        self.transform_password(request)
        return super(UsersViewSet, self).update(request, *args, **kwargs)

    def partial_update(self, request, *args, **kwargs):
        if not request.user.is_superuser:
            raise PermissionDenied('For update users data, current user must be a superuser');
        self.transform_password(request)
        return super(UsersViewSet, self).partial_update(request, *args, **kwargs)



class AppnexusUsersViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()

    serializer_class = AppnexusUsersSerializer
