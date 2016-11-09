from django.core.management import BaseCommand
# from rtb.models.rtb_impression_tracker import RtbImpressionTracker, RtbImpressionTrackerPlacement
# import socket
# import zlib
# import json
# import sys
# import datetime
# import re
from rtb.imp_tracker_cron import impTracker

#   python manage.py imp_tracker '2016-10-19 22:00' '2016-10-19 23:00'
class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('start', nargs='?')
        parser.add_argument('end', nargs='?')

    def handle(self, **options):
        start = options.get('start')
        end = options.get('end')

        if options.get('start') is None or options.get('end') is None:
            impTracker()
        else:
            impTracker(start, end)
