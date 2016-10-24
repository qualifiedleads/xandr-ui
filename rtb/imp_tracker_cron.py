#!/bin/env python
from rtb.models.rtb_impression_tracker import RtbImpressionTracker, RtbImpressionTrackerPlacement
from datetime import timedelta
from pytz import utc
import socket
import zlib
import json
import sys
import datetime
import re


def convert_date(s):
    return datetime.datetime.strptime(s, '%Y-%m-%d')


def issetValue(s):
    if re.match(r'\$', s) or s == '':
        return ' '
    else:
        return s


def get():
    # Create a TCP/IP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Connect the socket to the port where the server is listening
    server_address = ('imp.rtb.cat', 8002)
    #server_address = ('192.168.1.121', 8002)
    print >> sys.stderr, 'connecting to %s port %s' % server_address
    sock.connect(server_address)

    try:
        #   message = 'empty'
        #   start=2016-09-29 17:04&end=2016-09-29 17:06
        start = (datetime.datetime.now(utc) - timedelta(hours=4)).strftime('%Y-%m-%d %H:%M')
        end = datetime.datetime.now(utc).strftime('%Y-%m-%d %H:%M')

        if start is None or end is None:
            message = 'empty'
        else:
            message = 'start=' + start + '&end=' + end

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
        if item['Data']['PlacementId'] == '':
            print item['Data']['PlacementId']

        tempJson['PlacementId'] = issetValue(item['Data']['PlacementId'])
        tempJson['SeqCodes'] = issetValue(item['Data']['SeqCodes'])
        tempJson['CustomModelLeafName'] = issetValue(item['Data']['CustomModelLeafName'])
        tempJson['XForwardedFor'] = issetValue(item['Data']['XForwardedFor'])
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
            AuctionId=tempJson['AuctionId'],
            RemUser=tempJson['RemUser'],
            CpId=tempJson['CpId'],
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
            Date=datetime.datetime.strptime(re.sub('\..*', '', item['Time']), "%Y-%m-%d %H:%M:%S")
        ))

    try:
        RtbImpressionTracker.objects.bulk_create(bulkITAll)
    except ValueError:
        print ValueError

    for item in bulkITP:
        if len(item['placement']) > 1:
            try:
                obj, created = RtbImpressionTrackerPlacement.objects.update_or_create(
                    placement=int(item['placement']),
                    domain=str(item['domain'])
                )
                print (obj, item, created)
            except ValueError:
                print ValueError

    print 'Happy End'
