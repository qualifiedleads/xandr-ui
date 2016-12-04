from rest_framework.decorators import api_view, parser_classes
from rest_framework.response import Response
from django.utils import timezone
import datetime
from pytz import utc
from rtb.models.technical_works import AttentionMessage, TechnicalWork


@api_view(['GET', 'POST'])
# @check_user_advertiser_permissions(campaign_id_num=0)
def handler(request):
    """
GET all list works

## Url format: /api/v1/technicalwork



POST Add new work

## Url format: /api/v1/technicalwork

+ Parameters

    + value(Number) - value on/off

    """
    if request.method == "GET":
        k = getAll(request)
        return Response(k)
    if request.method == "POST":
        k = addNewStatus(request)
        return Response(k)


def getAll(request):
    try:
        lists = list(TechnicalWork.objects.filter().values('id', 'status', 'date'))
        for item in lists:
            item['date'] = item['date'].strftime("%Y-%m-%d %H:%M:%S")
        return lists
    except Exception, e:
        print 'Error: ' + str(e)

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


@api_view(['GET', 'POST', 'PUT'])
# @check_user_advertiser_permissions(campaign_id_num=0)
def banner(request):
    """
GET
Get last banner
## Url format: /api/v1/baner

POST
Add banner
## Url format: /api/v1/baner

PUT
change status banner
## Url format: /api/v1/baner
    """
    if request.method == "GET":
        k = getBanner()
        return Response(k)
    if request.method == "POST":
        k = addBanner(request)
        return Response(k)
    if request.method == "PUT":
        k = statusBanner()
        return Response(k)


def getBanner():
    try:
        print "Get message"
        if not AttentionMessage.objects.all():
            return {'text': '', 'status': False}
        else:
            message = AttentionMessage.objects.latest('id')
            return {'text': str(message.message), 'status': message.status}
    except Exception, e:
        print 'Error: ' + str(e)


def addBanner(request):
    try:
        if not AttentionMessage.objects.all():
            AttentionMessage(message=str(request.data.get("text")), status=request.data.get("status")).save()
            return {'text': str(request.data.get("text")), 'status': request.data.get("status")}
        else:
            message = AttentionMessage.objects.latest('id')
            message.message = request.data.get("text")
            message.status = request.data.get("status")
            message.save()
            print "Added new banner - " + str(request.data.get("text"))
            return {'text': str(message.message), 'status': message.status}
    except Exception, e:
        print 'Error: ' + str(e)


def statusBanner():
    try:
        if not AttentionMessage.objects.all():
            AttentionMessage(message='', status=False).save()
            print "Change status - OFF"
            return {'text': '', 'status': False}
        else:
            message = AttentionMessage.objects.latest('id')
            message.status = False
            message.save()
            print "Change status - OFF"
            return {'text': str(message.message), 'status': message.status}
    except Exception, e:
        print 'Error: ' + str(e)

