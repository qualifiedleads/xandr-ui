from django.core.management import BaseCommand
from rtb.models.placement_state import PlacementState
import datetime
from pytz import utc
from rtb.report import get_auth_token
from django.conf import settings
import json
import requests
from rtb.cron import load_report,load_reports_for_all_advertisers

appnexus_url = settings.__dict__.get(
    'APPNEXUS_URL', 'https://api.appnexus.com/')

class Command(BaseCommand):

    def handle(self, **options):
        self.stdout.write('test_load called')
        day = options.get('load_day')
        if not day:
            day = datetime.datetime.now(utc).replace(hour=0, minute=0, second=0, microsecond=0) - datetime.timedelta(days=1)
        token = get_auth_token()
        headers = {"Authorization": token, 'Content-Type': 'application/json'}
        """ auth_url = appnexus_url + "placement?id=6939533"
         r = requests.post(
             auth_url,
             headers=headers)
         response = json.loads(r.content)['response']

        """

        print (token)



        """load_report(token, day, NetworkCarrierReport_Simple_test)
        load_report(token, day, NetworkDeviceReport_Simple_test)
        load_report(token, day, NetworkAnalyticsReport_ByPlacement_test)
        load_report(token, day, GeoAnaliticsReport_test)
        load_reports_for_all_advertisers(token, day, SiteDomainPerformanceReport_test)
        """
