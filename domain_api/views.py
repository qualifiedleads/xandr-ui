from django.db import transaction
from django.http import JsonResponse, Http404
from rest_framework import status
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.generics import ListCreateAPIView, GenericAPIView
from advertiserTokenPermission import AdvertiserTokenPermission
from rest_framework.response import Response
from models import DomainList
from rtb.models import Advertiser


class DomainListView(ListCreateAPIView):
    permission_classes = (AdvertiserTokenPermission, )
    authentication_classes = ([])

    def get(self, request, *args, **kwargs):
        try:
            advertiser = self.getAdvertiserIdByHeader(request)[0]
            domainList = list(DomainList.objects.filter(advertiser=advertiser.id))
            return JsonResponse({"domainList": domainList})
        except Exception as e:
            Response(data=e.message, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request, *args, **kwargs):
        try:
            data = request.data
            data['user'] = request.user.id
            return Response(status=status.HTTP_200_OK)
        except Exception as e:
            Response(data=e.message, status=status.HTTP_400_BAD_REQUEST)

    def getAdvertiserIdByHeader(self, request):
        token = request.META['HTTP_AUTHORIZATION'].split(' ')[1]
        return list(Advertiser.objects.filter(token=token))


class DetailDomainListView(GenericAPIView):
    permission_classes = (AdvertiserTokenPermission, )
    authentication_classes = ([])

    def get_object(self, pk):
        try:
            return DomainList.objects.get(pk=pk)
        except DomainList.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        try:
            domainList = self.get_object(pk)
            return Response(data={"name": domainList.name, "domains": []}, status=status.HTTP_200_OK)
        except Exception as e:
            Response(data=e.message, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        try:
            domainList = self.get_object(pk)
            return Response(data=request.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(data=e.message, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        try:
            domainList = self.get_object(pk)
            return Response(data=request.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(data=e.message, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([AdvertiserTokenPermission])
@authentication_classes([])
def applyDomainList(request, pk):
    try:
        action = request.query_params['action']
        advertiser_id = request.query_params['advertiser_id']
        campaign_id = request.query_params['campaign_id']
        return Response(status=status.HTTP_200_OK)
    except Exception as error:
        return Response(error.message, status=status.HTTP_400_BAD_REQUEST)

