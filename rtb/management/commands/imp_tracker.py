from django.core.management import BaseCommand
from rtb.models.rtb_impression_tracker import RtbImpressionTracker
from django.conf import settings
import socket
import zlib
import json
import sys
import datetime
import re

def convert_date(s):
    return datetime.datetime.strptime(s,'%Y-%m-%d')

def issetValue (s):
    if re.match(r'\$', s) or s == ' ':
        return ' '
    else:
        return s

class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('start', nargs='?')
        parser.add_argument('end', nargs='?')

    def handle(self, **options):

        start = options.get('start')
        end = options.get('end')
        print (start, end)
        # Create a TCP/IP socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Connect the socket to the port where the server is listening
        server_address = ('imp.rtb.cat', 8002)
        print >> sys.stderr, 'connecting to %s port %s' % server_address
        sock.connect(server_address)

        try:
            #   message = 'empty'
            #   start=2016-09-29 17:04&end=2016-09-29 17:06
            if start is None or end is None:
                message = 'empty'
            else:
                message = 'start=' + start + '&end=' + end

            print >> sys.stderr, 'sending "%s"' % message
            sock.sendall(message)
            request = b""
            while True:
                data = sock.recv(1024)
                if not data:
                    break
                request = request + data

            decompressed_data = json.loads(zlib.decompress(request, -15))

        finally:
            print >> sys.stderr, 'closing socket'
            sock.close()

        print decompressed_data
"""
        bulkITAll = []
        bulkITP = []
        for item in decompressed_data:
            tempJson = {}
            tempITP = {}
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
            tempJson['Date'] = item['Time']
            bulkITP.append({'placement': tempJson['PlacementId'], 'domain': tempJson['LocationsOrigins']})
            bulkITAll.append(RtbImpressionTracker(
                LocationsOrigins = str(issetValue(item['Data']['LocationsOrigins'][0])),
                UserCountry = issetValue(item['Data']['UserCountry']),
                SessionFreq = issetValue(item['Data']['SessionFreq']),
                PricePaid = issetValue(item['Data']['PricePaid']),
                AdvFreq = issetValue(item['Data']['AdvFreq']),
                UserState = issetValue(item['Data']['UserState']),
                CpgId = issetValue(item['Data']['CpgId']),
                CustomModelLastModified = issetValue(item['Data']['CustomModelLastModified']),
                UserId = issetValue(item['Data']['UserId']),
                XRealIp = issetValue(item['Data']['XRealIp']),
                BidPrice = issetValue(item['Data']['BidPrice']),
                SegIds = issetValue(item['Data']['SegIds']),
                UserAgent = issetValue(item['Data']['UserAgent']),
                AuctionId = issetValue(issetValue(item['Data']['AuctionId'])),
                RemUser = issetValue(item['Data']['RemUser']),
                CpId = issetValue(item['Data']['CpId']),
                UserCity = issetValue(item['Data']['UserCity']),
                Age = issetValue(item['Data']['Age']),
                ReservePrice = issetValue(item['Data']['ReservePrice']),
                CacheBuster = issetValue(item['Data']['CacheBuster']),
                Ecp = issetValue(item['Data']['Ecp']),
                CustomModelId = issetValue(item['Data']['CustomModelId']),
                PlacementId = issetValue(item['Data']['PlacementId']),
                SeqCodes = issetValue(item['Data']['SeqCodes']),
                CustomModelLeafName = issetValue(item['Data']['CustomModelLeafName']),
                XForwardedFor = issetValue(item['Data']['XForwardedFor']),
                Date = datetime.datetime.strptime(re.sub('\..*', '',item['Time']), "%Y-%m-%d %H:%M:%S")
            ))
        print bulkITAll
        print '-----'
        print bulkITP

        RtbImpressionTracker.objects.bulk_create(bulkITAll)
        #tet = []
        #tet.append(RtbImpressionTracker())





a = [{"Time": "2016-10-19 22:18:11.058450594 +0000 UTC",
      "Data": {
          "LocationsOrigins": ["http://240.mhoy.user.nym2.adnexus.net:4000", "http://240.mhoy.user.nym2.adnexus.net:4000"],
          "UserAgent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36",
          "XForwardedFor": "207.237.150.246",
          "XRealIp": "207.237.150.246",
          "PlacementId": "${TAG_ID}",
          "UserId": "${USER_ID}",
          "UserCity": "${USER_CITY}",
          "UserCountry": "${USER_COUNTRY}",
          "UserState": "${USER_STATE}",
          "SessionFreq": "${SESSION_FREQ}",
          "RemUser": "${REM_USER}",
          "SegIds": "${SEG_IDS}",
          "SeqCodes": "${SEG_CODES}",
          "PricePaid": "${PRICE_PAID}",
          "ReservePrice": "${RESERVE_PRICE}",
          "Ecp": "${ECP}",
          "CustomModelId": "${CUSTOM_MODEL_ID}",
          "CustomModelLastModified": "${CUSTOM_MODEL_LAST_MODIFIED}",
          "CustomModelLeafName": "${CUSTOM_MODEL_LEAF_NAME}",
          "CpId": "${CP_ID}",
          "CpgId": "${CPG_ID}",
          "CacheBuster": "${CACHEBUSTER}",
          "BidPrice": "${BID_PRICE}",
          "AuctionId": "${AUCTION_ID}",
          "Age": "${AGE}",
          "AdvFreq": "${ADV_FREQ}"}
      }
     ]
"""
