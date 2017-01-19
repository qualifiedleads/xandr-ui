#!/bin/env python
from rtb.models.rtb_impression_tracker import RtbImpressionTracker, RtbImpressionTrackerPlacement, \
    RtbImpressionTrackerPlacementDomain, RtbClickTracker, RtbConversionTracker, RtbAdStartTracker, RtbDomainTracker
from datetime import date, datetime, timedelta
from rtb.models.placement_state import LastModified
from pytz import utc
import socket
import zlib
import json
import sys
import re
from django.utils import timezone
from django.db.models import Sum, Min, Max, Avg, Value, When, Case, F, Q, Func, FloatField, Count


def issetValue(s):
    if re.match(r'\$', s) or s == '':
        return None
    else:
        return s


def is_number(str):
    try:
        float(str)
        return True
    except ValueError:
        return False


def perdelta(start, end, delta):
    curr = start
    while curr < end:
        yield curr
        curr += delta


def get():
    try:
        # Verbtimedelta - it is time range
        Verbtimedelta = 10

        change_state = LastModified.objects.filter(type='get_data_from_impression_tracker')
        if len(change_state) >= 1:
            if timezone.make_aware(datetime.now(), timezone.get_default_timezone()) - change_state[0].date >= timedelta(minutes=15):
                LastModified.objects.filter(type='get_data_from_impression_tracker').delete()
            else:
                print "get_data_from_impression_tracker is busy, wait..."
                return None

        LastModified(type='get_data_from_impression_tracker', date=timezone.make_aware(datetime.now(), timezone.get_default_timezone())).save()

        # Domain Tracker
        print 'Domain start'
        start_ = RtbDomainTracker.objects.aggregate(Max("Date"))["Date__max"]
        if start_ is None:
            start = '2017-01-18 12:00:00'
        else:
            start = (start_ + timedelta(seconds=1)).strftime('%Y-%m-%d %H:%M:%S')
        try:
            start_date = datetime.strptime(start, '%Y-%m-%d %H:%M:%S')
            end_date = datetime.now()
            startStr = ''
            for result in perdelta(start_date, end_date, timedelta(minutes=Verbtimedelta)):
                endStr = result.strftime('%Y-%m-%d %H:%M:%S')+".999999999"
                if startStr == '':
                    startStr = result.strftime('%Y-%m-%d %H:%M:%S')
                    continue
                # Update time every circle
                LastModified.objects.filter(type='get_data_from_impression_tracker').update(date=timezone.make_aware(datetime.now(), timezone.get_default_timezone()))
                impTracker(startStr, endStr, 'Domain')
                startStr = (result + timedelta(seconds=1)).strftime('%Y-%m-%d %H:%M:%S')
        except Exception as e:
            print 'Domain Error: ' + str(e)
        print 'Domain completed'

        # Impression Tracker
        print 'Impression start'
        start_ = RtbImpressionTracker.objects.aggregate(Max("Date"))["Date__max"]
        if start_ is None:
            start = '2016-09-01 00:00:00'
        else:
            start = (start_ + timedelta(seconds=1)).strftime('%Y-%m-%d %H:%M:%S')
        try:
            start_date = datetime.strptime(start, '%Y-%m-%d %H:%M:%S')
            end_date = datetime.now()
            startStr = ''
            for result in perdelta(start_date, end_date, timedelta(minutes=Verbtimedelta)):
                endStr = result.strftime('%Y-%m-%d %H:%M:%S')+".999999999"
                if startStr == '':
                    startStr = result.strftime('%Y-%m-%d %H:%M:%S')
                    continue
                # Update time every circle
                LastModified.objects.filter(type='get_data_from_impression_tracker').update(date=timezone.make_aware(datetime.now(), timezone.get_default_timezone()))
                impTracker(startStr, endStr, 'Impression')
                startStr = (result + timedelta(seconds=1)).strftime('%Y-%m-%d %H:%M:%S')
        except Exception as e:
            print 'Impression Error: ' + str(e)
        print 'Impression completed'


        # Click Tracker
        print 'Click start'
        start_ = RtbClickTracker.objects.aggregate(Max("Date"))["Date__max"]
        if start_ is None:
            start = '2016-09-01 00:00:00'
        else:
            start = (start_ + timedelta(seconds=1)).strftime('%Y-%m-%d %H:%M:%S')
        try:
            start_date = datetime.strptime(start, '%Y-%m-%d %H:%M:%S')
            end_date = datetime.now()
            startStr = ''
            for result in perdelta(start_date, end_date, timedelta(minutes=Verbtimedelta)):
                endStr = result.strftime('%Y-%m-%d %H:%M:%S') + ".999999999"
                if startStr == '':
                    startStr = result.strftime('%Y-%m-%d %H:%M:%S')
                    continue
                # Update time every circle
                LastModified.objects.filter(type='get_data_from_impression_tracker').update(date=timezone.make_aware(datetime.now(), timezone.get_default_timezone()))
                impTracker(startStr, endStr, 'Click')
                startStr = (result + timedelta(seconds=1)).strftime('%Y-%m-%d %H:%M:%S')
        except Exception as e:
            print 'Click Error: ' + str(e)
        print 'Click completed'

        # Conversion Tracker
        print 'Conversion start'
        start_ = RtbConversionTracker.objects.aggregate(Max("Date"))["Date__max"]
        if start_ is None:
            start = '2016-09-01 00:00:00'
        else:
            start = (start_ + timedelta(seconds=1)).strftime('%Y-%m-%d %H:%M:%S')
        try:
            start_date = datetime.strptime(start, '%Y-%m-%d %H:%M:%S')
            end_date = datetime.now()
            startStr = ''
            for result in perdelta(start_date, end_date, timedelta(minutes=Verbtimedelta)):
                endStr = result.strftime('%Y-%m-%d %H:%M:%S') + ".999999999"
                if startStr == '':
                    startStr = result.strftime('%Y-%m-%d %H:%M:%S')
                    continue
                # Update time every circle
                LastModified.objects.filter(type='get_data_from_impression_tracker').update(date=timezone.make_aware(datetime.now(), timezone.get_default_timezone()))
                impTracker(startStr, endStr, 'Conversion')
                startStr = (result + timedelta(seconds=1)).strftime('%Y-%m-%d %H:%M:%S')
        except Exception as e:
            print ' Conversion Error: ' + str(e)

        # AdStart Tracker
        print 'Ad-start start'
        start_ = RtbAdStartTracker.objects.aggregate(Max("Date"))["Date__max"]
        if start_ is None:
            start = '2016-09-01 00:00:00'
        else:
            start = (start_ + timedelta(seconds=1)).strftime('%Y-%m-%d %H:%M:%S')
        try:
            start_date = datetime.strptime(start, '%Y-%m-%d %H:%M:%S')
            end_date = datetime.now()
            startStr = ''
            for result in perdelta(start_date, end_date, timedelta(minutes=Verbtimedelta)):
                endStr = result.strftime('%Y-%m-%d %H:%M:%S') + ".999999999"
                if startStr == '':
                    startStr = result.strftime('%Y-%m-%d %H:%M:%S')
                    continue
                # Update time every circle
                LastModified.objects.filter(type='get_data_from_impression_tracker').update(date=timezone.make_aware(datetime.now(), timezone.get_default_timezone()))
                impTracker(startStr, endStr, 'AdStart')
                startStr = (result + timedelta(seconds=1)).strftime('%Y-%m-%d %H:%M:%S')
        except Exception as e:
            print ' Ad-start Error: ' + str(e)

        LastModified.objects.filter(type='get_data_from_impression_tracker').delete()
    except ValueError, e:
        LastModified.objects.filter(type='get_data_from_impression_tracker').delete()
        print 'Error: ' + str(e)


#############################################
def impTracker(timeStart=None, timeFinish=None, type=None):
    # Create a TCP/IP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Connect the socket to the port where the server is listening
    # server_address = ('imp.rtb.cat', 8002)
    server_address = ('192.168.1.112', 8002)
    print >> sys.stderr, 'connecting to %s port %s' % server_address
    sock.connect(server_address)

    try:
        # start=2016-09-29 17:04&end=2016-09-29 17:06&type=Impression or Click or Conversion

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

    if type == 'Domain':
        Domain(decompressed_data)

    if type == 'Click':
        Click(decompressed_data)

    if type == 'Conversion':
        Conversion(decompressed_data)

    if type == 'AdStart':
        AdStart(decompressed_data)


def Impression(decompressed_data):
    try:
        if decompressed_data is None:
            return
        bulkITAll = []
        for item in decompressed_data:
            tempJson = {}
            tempJson['UserCountry'] = issetValue(item['Data']['UserCountry'])
            tempJson['SessionFreq'] = issetValue(item['Data']['SessionFreq'])
            tempJson['PricePaid'] = item['Data']['PricePaid'] if is_number(item['Data']['PricePaid']) else None
            tempJson['AdvFreq'] = issetValue(item['Data']['AdvFreq'])
            tempJson['UserState'] = issetValue(item['Data']['UserState'])
            tempJson['CpgId'] = item['Data']['CpgId'] if is_number(item['Data']['CpgId']) else None
            tempJson['CustomModelLastModified'] = issetValue(item['Data']['CustomModelLastModified'])
            tempJson['UserId'] = item['Data']['UserId'] if is_number(item['Data']['UserId']) else None
            tempJson['XRealIp'] = issetValue(item['Data']['XRealIp'])
            tempJson['BidPrice'] = item['Data']['BidPrice'] if is_number(item['Data']['BidPrice']) else None
            tempJson['SegIds'] = issetValue(item['Data']['SegIds'])
            tempJson['UserAgent'] = issetValue(item['Data']['UserAgent'])
            tempJson['AuctionId'] = item['Data']['AuctionId'] if is_number(item['Data']['AuctionId']) else None
            tempJson['RemUser'] = item['Data']['RemUser'] if is_number(item['Data']['RemUser']) else None
            tempJson['CpId'] = item['Data']['CpId'] if is_number(item['Data']['CpId']) else None
            tempJson['UserCity'] = issetValue(item['Data']['UserCity'])
            tempJson['Age'] = item['Data']['Age'] if is_number(item['Data']['Age']) else None
            tempJson['ReservePrice'] = item['Data']['ReservePrice'] if is_number(item['Data']['ReservePrice']) else None
            tempJson['CacheBuster'] = item['Data']['CacheBuster'] if is_number(item['Data']['CacheBuster']) else None
            tempJson['Ecp'] = item['Data']['Ecp'] if is_number(item['Data']['Ecp']) else None
            tempJson['CustomModelId'] = item['Data']['CustomModelId'] if is_number(item['Data']['CustomModelId']) else None
            tempJson['PlacementId'] = item['Data']['PlacementId'] if is_number(item['Data']['PlacementId']) else None
            tempJson['SeqCodes'] = issetValue(item['Data']['SeqCodes'])
            tempJson['CustomModelLeafName'] = issetValue(item['Data']['CustomModelLeafName'])
            tempJson['XForwardedFor'] = issetValue(item['Data']['XForwardedFor'])
            tempJson['AdvId'] = item['Data']['AdvId'] if is_number(item['Data']['AdvId']) else None
            tempJson['CreativeId'] = item['Data']['CreativeId'] if is_number(item['Data']['CreativeId']) else None
            tempJson['Date'] = item['Time']

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
                Date=timezone.make_aware(datetime.strptime(re.sub('\..*', '', item['Time']), "%Y-%m-%d %H:%M:%S"), timezone.get_default_timezone())
            ))

        try:
            RtbImpressionTracker.objects.bulk_create(bulkITAll)
        except ValueError, e:
            print "Can't save domain. Error: " + str(e)
    except Exception, e:
        print "Impression tracker. Error: " + str(e)


def Click(decompressed_data):
    if decompressed_data is None:
        return
    try:
        bulkITAll = []
        for item in decompressed_data:
            if is_number(item['Data']['AuctionId']) == False:
                continue
            tempJson = {}
            tempJson['CpId'] = item['Data']['CpId'] if is_number(item['Data']['CpId']) else None
            tempJson['AdvId'] = item['Data']['AdvId'] if is_number(item['Data']['AdvId']) else None
            tempJson['CreativeId'] = item['Data']['CreativeId'] if is_number(item['Data']['CreativeId']) else None
            tempJson['AuctionId'] = item['Data']['AuctionId'] if is_number(item['Data']['AuctionId']) else None
            tempJson['Date'] = item['Time']

            bulkITAll.append(RtbClickTracker(
                CpId=tempJson['CpId'],
                AdvId=tempJson['AdvId'],
                CreativeId=tempJson['CreativeId'],
                AuctionId=tempJson['AuctionId'],
                Date=timezone.make_aware(datetime.strptime(re.sub('\..*', '', item['Time']), "%Y-%m-%d %H:%M:%S"),
                                         timezone.get_default_timezone())
            ))

        RtbClickTracker.objects.bulk_create(bulkITAll)
    except Exception, e:
        print "Can't save Clicks. Error: " + str(e)


def Conversion(decompressed_data):
    try:
        if decompressed_data is None:
            return
        bulkITAll = []
        for item in decompressed_data:
            if is_number(item['Data']['AuctionId']) == False:
                continue
            tempJson = {}
            tempJson['CpId'] = item['Data']['CpId'] if is_number(item['Data']['CpId']) else None
            tempJson['AdvId'] = item['Data']['AdvId'] if is_number(item['Data']['AdvId']) else None
            tempJson['CreativeId'] = item['Data']['CreativeId'] if is_number(item['Data']['CreativeId']) else None
            tempJson['AuctionId'] = item['Data']['AuctionId'] if is_number(item['Data']['AuctionId']) else None
            tempJson['Date'] = item['Time']

            bulkITAll.append(RtbConversionTracker(
                CpId=tempJson['CpId'],
                AdvId=tempJson['AdvId'],
                CreativeId=tempJson['CreativeId'],
                AuctionId=tempJson['AuctionId'],
                Date=timezone.make_aware(datetime.strptime(re.sub('\..*', '', item['Time']), "%Y-%m-%d %H:%M:%S"),
                                         timezone.get_default_timezone())
            ))

        RtbConversionTracker.objects.bulk_create(bulkITAll)
    except Exception, e:
        print "Can't save Conversions. Error: " + str(e)


def AdStart(decompressed_data):
    try:
        if decompressed_data is None:
            return
        bulkITAll = []
        for item in decompressed_data:
            if is_number(item['Data']['AuctionId']) == False:
                continue

            tempJson = {}
            tempJson['CpId'] = item['Data']['CpId'] if is_number(item['Data']['CpId']) else None
            tempJson['AdvId'] = item['Data']['AdvId'] if is_number(item['Data']['AdvId']) else None
            tempJson['CreativeId'] = item['Data']['CreativeId'] if is_number(item['Data']['CreativeId']) else None
            tempJson['AuctionId'] = item['Data']['AuctionId'] if is_number(item['Data']['AuctionId']) else None
            tempJson['cpvm'] = item['Data']['CPVM'] if is_number(item['Data']['CPVM']) else None
            tempJson['Date'] = item['Time']

            bulkITAll.append(RtbAdStartTracker(
                CpId=tempJson['CpId'],
                AdvId=tempJson['AdvId'],
                CreativeId=tempJson['CreativeId'],
                AuctionId=tempJson['AuctionId'],
                cpvm=tempJson['cpvm'],
                Date=timezone.make_aware(datetime.strptime(re.sub('\..*', '', item['Time']), "%Y-%m-%d %H:%M:%S"),
                                         timezone.get_default_timezone())
            ))

        RtbAdStartTracker.objects.bulk_create(bulkITAll)
    except Exception, e:
        print "Can't save ad-start. Error: " + str(e)


def Domain(decompressed_data):
    try:
        if decompressed_data is None:
            return
        bulkITAll = []
        bulkITP = []
        for item in decompressed_data:
            if is_number(item['Data']['AuctionId']) == False:
                continue

            tempJson = {}
            if item['Data']['LocationsOrigins'] is None:
                tempJson['LocationsOrigins'] = None
            else:
                tempJson['LocationsOrigins'] = issetValue(item['Data']['LocationsOrigins'][0])
            tempJson['AuctionId'] = item['Data']['AuctionId'] if is_number(item['Data']['AuctionId']) else None
            tempJson['PlacementId'] = item['Data']['PlacementId'] if is_number(item['Data']['PlacementId']) else None
            tempJson['UserId'] = item['Data']['UserId'] if is_number(item['Data']['UserId']) else None
            tempJson['AdvId'] = item['Data']['AdvId'] if is_number(item['Data']['AdvId']) else None
            tempJson['Date'] = item['Time']

            bulkITP.append({'placement': tempJson['PlacementId'], 'domain': tempJson['LocationsOrigins']})
            bulkITAll.append(RtbDomainTracker(
                placement_id=tempJson['PlacementId'],
                domain=tempJson['LocationsOrigins'],
                advid=tempJson['AdvId'],
                auctionid=tempJson['AuctionId'],
                userid=tempJson['UserId'],
                Date=timezone.make_aware(datetime.strptime(re.sub('\..*', '', item['Time']), "%Y-%m-%d %H:%M:%S"),
                                         timezone.get_default_timezone())
            ))

        RtbDomainTracker.objects.bulk_create(bulkITAll)
        for item in bulkITP:
            try:
                if item["placement"].strip() != '':
                    if len(item['placement']) > 1 and item['domain'].strip() != '':
                        try:
                            obj, created = RtbImpressionTrackerPlacement.objects.update_or_create(
                                placement_id=int(item['placement']),
                                domain=str(item['domain'].strip())
                            )
                        except ValueError, e:
                            print "Can't save domain. Error: " + str(e)
            except Exception, e:
                print "Can't save domain. Error: " + str(e)

        for item in bulkITP:
            try:
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
            except Exception, e:
                print "Can't save domain to rtb_impression_tracker_placement_domain. Error: " + str(e)
    except Exception, e:
        print "Can't save Domain. Error: " + str(e)

