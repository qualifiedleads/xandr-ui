from rest_framework.decorators import api_view, parser_classes
from django.http import HttpResponse
from rest_framework.response import Response
from django.core import serializers
from django.utils import timezone
import datetime
import json
from pytz import utc
from rtb.models.technical_works import AttentionMessage, TechnicalWork


@api_view(['GET', 'POST'])
# @check_user_advertiser_permissions(campaign_id_num=0)
def handler(request):
    """
Get all list works

## Url format: /api/v1/technicalwork

+ Parameters

    + id(Number) - id for getting information about company


    """
    if request.method == "GET":
        k = getAll(request)
        return Response(k)
    if request.method == "POST":
        k = addNewStatus(request)
        return Response(k)


def getAll(request):
    lists = TechnicalWork.objects.all()
    ddd = json.loads(str(lists))
    return ddd


def addNewStatus(request):
    try:
        request.data.get("value")
        TechnicalWork(status=request.data.get("value"), date=timezone.make_aware(datetime.datetime.now(), timezone.get_default_timezone())).save()
        print "Added new status for technical work - " + request.data.get("value")
        return request.data.get("value")
    except Exception, e:
        print 'Error: ' + str(e)


@api_view(['GET'])
# @check_user_advertiser_permissions(campaign_id_num=0)
def getLast(request):
    """
Get last status works

## Url format: /api/v1/technicalwork/last

+ Parameters

    + id(Number) - id for getting information about company
    """
    try:
        if not TechnicalWork.objects.all():
            return Response("off")
        else:
            k = TechnicalWork.objects.latest('id')
            print "Last status for technical work - " + k.status
            return Response(k.status)
    except Exception, e:
        print 'Error: ' + str(e)






