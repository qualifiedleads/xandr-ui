from django.core.management import BaseCommand
from rtb.models.rtb_impression_tracker import RtbImpressionTracker, RtbImpressionTrackerPlacement
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
    if re.match(r'\$', s) or s == '':
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
                message = 'start=' + start + ' 00:00&end=' + end + ' 00:01'

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
        for item in bulkITP:
            obj, created = RtbImpressionTrackerPlacement.objects.update_or_create(
                placement=int(item['placement']),
                domain=str(item['domain'])
            )
            print (obj, item, created)




