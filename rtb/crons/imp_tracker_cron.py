#!/bin/env python
from rtb.models.rtb_impression_tracker import RtbImpressionTracker, RtbImpressionTrackerPlacement, RtbImpressionTrackerPlacementDomain, RtbClickTracker, RtbConversionTracker
from datetime import timedelta
from pytz import utc
import socket
import zlib
import json
import sys
import datetime
import re
from django.utils import timezone
from django.db.models import Sum, Min, Max, Avg, Value, When, Case, F, Q, Func, FloatField, Count


def issetValue(s):
    if re.match(r'\$', s) or s == '':
        return ' '
    else:
        return s


def get():
    end = ''
    # Impression Tracker
    print 'Impression start'
    start_ = RtbImpressionTracker.objects.aggregate(Max("Date"))["Date__max"]
    if start_ is None:
        start = ''
    else:
        start = (start_ + timedelta(seconds=1)).strftime('%Y-%m-%d %H:%M:%S')
    try:
        impTracker(start, end, 'Impression')
    except Exception as e:
        print 'Impression Error: ' + str(e)
    print 'Impression completed'
    # Click Tracker
    print 'Click start'
    start_ = RtbClickTracker.objects.aggregate(Max("Date"))["Date__max"]
    if start_ is None:
        start = ''
    else:
        start = (start_ + timedelta(seconds=1)).strftime('%Y-%m-%d %H:%M:%S')
    try:
        impTracker(start, end, 'Click')
    except Exception as e:
        print 'Click Error: ' + str(e)
    print 'Click completed'
    # Conversion Tracker
    print 'Conversion start'
    start_ = RtbConversionTracker.objects.aggregate(Max("Date"))["Date__max"]
    if start_ is None:
        start = ''
    else:
        start = (start_ + timedelta(seconds=1)).strftime('%Y-%m-%d %H:%M:%S')
    try:
        impTracker(start, end, 'Conversion')
    except Exception as e:
        print ' Conversion Error: ' + str(e)


#############################################
def impTracker(timeStart=None, timeFinish=None, type=None):
    # Create a TCP/IP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Connect the socket to the port where the server is listening
    server_address = ('imp.rtb.cat', 8002)
    # server_address = ('192.168.1.112', 8002)
    print >> sys.stderr, 'connecting to %s port %s' % server_address
    sock.connect(server_address)

    try:
        #   start=2016-09-29 17:04&end=2016-09-29 17:06&type=Impression or Click or Conversion

        if timeStart is None or timeFinish is None or type is None:
            message = 'empty'
        else:
            message = 'start=' + timeStart + '&end=' + timeFinish + '&type=' + type

        print >> sys.stderr, 'sending "%s"' % message
        sock.sendall(message)
        request = b""
        while True:
            data = sock.recv(2048)
            if not data:
                break
            request = request + data

        decompressed_data = json.loads(zlib.decompress(request, -15))

    finally:
        print >> sys.stderr, 'closing socket'
        sock.close()

    if type == 'Impression':
        Impression(decompressed_data)

    if type == 'Click':
        Click(decompressed_data)

    if type == 'Conversion':
        Conversion(decompressed_data)


def Impression(decompressed_data):
    bulkITAll = []
    bulkITP = []
    for item in decompressed_data:
        tempJson = {}
        if item['Data']['LocationsOrigins'] is None:
            tempJson['LocationsOrigins'] = ' '
        else:
            tempJson['LocationsOrigins'] = issetValue(item['Data']['LocationsOrigins'][0])
        tempJson['UserCountry'] = issetValue(item['Data']['UserCountry'])
        tempJson['SessionFreq'] = issetValue(item['Data']['SessionFreq'])
        tempJson['PricePaid'] = issetValue(item['Data']['PricePaid'])
        tempJson['AdvFreq'] = issetValue(item['Data']['AdvFreq'])
        tempJson['UserState'] = issetValue(item['Data']['UserState'])
        tempJson['CpgId'] = issetValue(item['Data']['CpgId'])
        tempJson['CustomModelLastModified'] = issetValue(item['Data']['CustomModelLastModified'])
        tempJson['UserId'] = issetValue(item['Data']['UserId'])
        tempJson['XRealIp'] = issetValue(item['Data']['XRealIp'])
        tempJson['BidPrice'] = issetValue(item['Data']['BidPrice'])
        tempJson['SegIds'] = issetValue(item['Data']['SegIds'])
        tempJson['UserAgent'] = issetValue(item['Data']['UserAgent'])
        tempJson['AuctionId'] = issetValue(issetValue(item['Data']['AuctionId']))
        tempJson['RemUser'] = issetValue(item['Data']['RemUser'])
        tempJson['CpId'] = issetValue(item['Data']['CpId'])
        tempJson['UserCity'] = issetValue(item['Data']['UserCity'])
        tempJson['Age'] = issetValue(item['Data']['Age'])
        tempJson['ReservePrice'] = issetValue(item['Data']['ReservePrice'])
        tempJson['CacheBuster'] = issetValue(item['Data']['CacheBuster'])
        tempJson['Ecp'] = issetValue(item['Data']['Ecp'])
        tempJson['CustomModelId'] = issetValue(item['Data']['CustomModelId'])
        tempJson['PlacementId'] = issetValue(item['Data']['PlacementId'])
        tempJson['SeqCodes'] = issetValue(item['Data']['SeqCodes'])
        tempJson['CustomModelLeafName'] = issetValue(item['Data']['CustomModelLeafName'])
        tempJson['XForwardedFor'] = issetValue(item['Data']['XForwardedFor'])
        tempJson['AdvId'] = issetValue(item['Data']['AdvId'])
        tempJson['CreativeId'] = issetValue(item['Data']['CreativeId'])
        tempJson['Date'] = item['Time']
        bulkITP.append({'placement': tempJson['PlacementId'], 'domain': tempJson['LocationsOrigins']})
        bulkITAll.append(RtbImpressionTracker(
            LocationsOrigins=tempJson['LocationsOrigins'],
            UserCountry=tempJson['UserCountry'],
            SessionFreq=tempJson['SessionFreq'],
            PricePaid=tempJson['PricePaid'],
            AdvFreq=tempJson['AdvFreq'],
            UserState=tempJson['UserState'],
            CpgId=tempJson['CpgId'],
            CustomModelLastModified=tempJson['CustomModelLastModified'],
            UserId=tempJson['UserId'],
            XRealIp=tempJson['XRealIp'],
            BidPrice=tempJson['BidPrice'],
            SegIds=tempJson['SegIds'],
            UserAgent=tempJson['UserAgent'],
            CpId=tempJson['CpId'],
            AuctionId=tempJson['AuctionId'],
            RemUser=tempJson['RemUser'],
            UserCity=tempJson['UserCity'],
            Age=tempJson['Age'],
            ReservePrice=tempJson['ReservePrice'],
            CacheBuster=tempJson['CacheBuster'],
            Ecp=tempJson['Ecp'],
            CustomModelId=tempJson['CustomModelId'],
            PlacementId=tempJson['PlacementId'],
            SeqCodes=tempJson['SeqCodes'],
            CustomModelLeafName=tempJson['CustomModelLeafName'],
            XForwardedFor=tempJson['XForwardedFor'],
            AdvId=tempJson['AdvId'],
            CreativeId=tempJson['CreativeId'],
            Date=timezone.make_aware(datetime.datetime.strptime(re.sub('\..*', '', item['Time']), "%Y-%m-%d %H:%M:%S"), timezone.get_default_timezone())
        ))

    try:
        RtbImpressionTracker.objects.bulk_create(bulkITAll)
    except ValueError, e:
        print "Can't save domain. Error: " + str(e)

    for item in bulkITP:
        if item["placement"].strip() != '':
            if len(item['placement']) > 1 and item['domain'].strip() != '':
                try:
                    obj, created = RtbImpressionTrackerPlacement.objects.update_or_create(
                        placement_id=int(item['placement']),
                        domain=str(item['domain'].strip())
                    )
                except ValueError, e:
                    print "Can't save domain. Error: " + str(e)
                    #CODE FOR ADDING TO RtbImpressionTrackerPlacementDomain clear domain

    for item in bulkITP:
        if item["placement"].strip() != '':
            allDomainsQuery = RtbImpressionTrackerPlacement.objects.filter(placement_id=item["placement"]).distinct()
            if not allDomainsQuery:
                continue
            if len(allDomainsQuery) == 1:
                ans = allDomainsQuery[0].domain
            else:
                position = 1
                finish = False
                while True:
                    for i in xrange(len(allDomainsQuery)):
                        for j in xrange(len(allDomainsQuery)):
                            if i == j or allDomainsQuery[i].domain == "null":
                                continue

                            if len(allDomainsQuery[i].domain) < position or len(allDomainsQuery[j].domain) < position:
                                finish = True
                                break
                            if allDomainsQuery[i].domain[-position] != allDomainsQuery[j].domain[-position]:
                                finish = True
                                break
                    if finish == True:
                        break
                    position += 1
                ans = "*"
                position -= 1
                while position != 0:
                    ans += allDomainsQuery[0].domain[-position]
                    position -= 1
            try:
                domainRecord = RtbImpressionTrackerPlacementDomain(
                    placement_id=item["placement"],
                    domain=ans
                )
                tempQuery = RtbImpressionTrackerPlacementDomain.objects.filter(placement_id=item["placement"])
                if not tempQuery:
                    domainRecord.save()
                else:
                    tempQuery.update(
                        domain=ans
                    )
            except Exception, e:
                print "Can't save domain. Error: " + str(e)


def Click(decompressed_data):
    try:
        bulkITAll = []
        for item in decompressed_data:
            tempJson = {}
            tempJson['CpId'] = issetValue(item['Data']['CpId'])
            tempJson['AdvId'] = issetValue(item['Data']['AdvId'])
            tempJson['CreativeId'] = issetValue(item['Data']['CreativeId'])
            tempJson['AuctionId'] = issetValue(item['Data']['AuctionId'])
            tempJson['Date'] = item['Time']

            bulkITAll.append(RtbClickTracker(
                CpId=tempJson['CpId'],
                AdvId=tempJson['AdvId'],
                CreativeId=tempJson['CreativeId'],
                AuctionId=tempJson['AuctionId'],
                Date=timezone.make_aware(datetime.datetime.strptime(re.sub('\..*', '', item['Time']), "%Y-%m-%d %H:%M:%S"),
                                         timezone.get_default_timezone())
            ))

        RtbClickTracker.objects.bulk_create(bulkITAll)
    except Exception, e:
        print "Can't save Clicks. Error: " + str(e)


def Conversion(decompressed_data):
    try:
        bulkITAll = []
        for item in decompressed_data:
            tempJson = {}
            tempJson['CpId'] = issetValue(item['Data']['CpId'])
            tempJson['AdvId'] = issetValue(item['Data']['AdvId'])
            tempJson['CreativeId'] = issetValue(item['Data']['CreativeId'])
            tempJson['AuctionId'] = issetValue(item['Data']['AuctionId'])
            tempJson['Date'] = item['Time']

            bulkITAll.append(RtbConversionTracker(
                CpId=tempJson['CpId'],
                AdvId=tempJson['AdvId'],
                CreativeId=tempJson['CreativeId'],
                AuctionId=tempJson['AuctionId'],
                Date=timezone.make_aware(datetime.datetime.strptime(re.sub('\..*', '', item['Time']), "%Y-%m-%d %H:%M:%S"),
                                         timezone.get_default_timezone())
            ))

        RtbConversionTracker.objects.bulk_create(bulkITAll)
    except Exception, e:
        print "Can't save Conversions. Error: " + str(e)

