from django.db import transaction
from django.http import JsonResponse, Http404
from rest_framework import status
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.generics import ListCreateAPIView, GenericAPIView
from advertiserTokenPermission import AdvertiserTokenPermission
from rest_framework.response import Response

from domain_api.appnexusDomainListApi import DomainListApi
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
            return Response(data=e.message, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request, *args, **kwargs):
        try:
            advertiser = self.getAdvertiserIdByHeader(request)[0]
            domainApi = DomainListApi(None)
            oldName = request.data['name']
            request.data['name'] = '{0}_{1}'.format(advertiser.id, oldName)
            result = domainApi.addNewDomainList(request.data)
            if isinstance(result, basestring):
                raise Exception(result)
            DomainList.objects.create(pk=result['id'], name=oldName, advertiser=advertiser)
            return Response(data={"id": result['id']}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(data=e.message, status=status.HTTP_400_BAD_REQUEST)

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
            domainApi = DomainListApi(pk)
            result = domainApi.getDomainListById()
            if isinstance(result, basestring):
                raise Exception(result)
            return Response(
                data={"id": domainList.id, "name": domainList.name, "domains": result['domains']},
                status=status.HTTP_200_OK
            )
        except Exception as e:
            return Response(data=e.message, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        try:
            data = request.data
            domainList = self.get_object(pk)
            domainApi = DomainListApi(pk)
            result = domainApi.getDomainListById()
            if isinstance(result, basestring):
                raise Exception(result)
            newObjectDomainList = {
                "domains": result['domains']
            }
            if data['action'] == 'append':
                if isinstance(newObjectDomainList['domains'], list):
                    newObjectDomainList['domains'].extend(request.data['domains'])
                else:
                    newObjectDomainList['domains'] = request.data['domains']

            if data['action'] == 'remove':
                if not isinstance(newObjectDomainList['domains'], list):
                    newObjectDomainList['domains'] = []
                newArrayDomainList = [domain for domain in newObjectDomainList['domains'] if domain not in request.data['domains']]
                newObjectDomainList['domains'] = newArrayDomainList

            if data['action'] == 'replace':
                newObjectDomainList['domains'] = request.data['domains']

            updatedDomainList = domainApi.updateDomainListById(newObjectDomainList)
            if isinstance(updatedDomainList, basestring):
                raise Exception(updatedDomainList)
            return Response(data={
                "name": domainList.name,
                "id": updatedDomainList['id'],
                "domains": updatedDomainList['domains']
            }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(data=e.message, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        try:
            domainList = self.get_object(pk)
            domainApi = DomainListApi(pk)
            result = domainApi.removeDomainListById()
            if isinstance(result, basestring):
                raise Exception(result)
            if result['status'] == 'OK':
                domainList.delete()
            return Response(status=status.HTTP_200_OK)
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
        domainApi = DomainListApi(pk)
        result = domainApi.applyDomainListById(campaign_id, advertiser_id, action)
        if isinstance(result, basestring):
            raise Exception(result)
        return Response(status=status.HTTP_200_OK)
    except Exception as error:
        return Response(error.message, status=status.HTTP_400_BAD_REQUEST)

