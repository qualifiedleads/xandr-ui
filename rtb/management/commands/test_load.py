from django.core.management import BaseCommand
import datetime
from pytz import utc
from rtb.report import get_auth_token
from rtb.cron import load_report,load_reports_for_all_advertisers
from rtb.models.test_load import NetworkAnalyticsReport_ByPlacement_test,NetworkCarrierReport_Simple_test, \
    NetworkDeviceReport_Simple_test, GeoAnaliticsReport_test, SiteDomainPerformanceReport_test

def convert_date(s):
    return datetime.datetime.strptime(s,'%Y-%m-%d')

class Command(BaseCommand):
    help = """
Loads some test reports for specifed day. Date must provided as <Year>-<Month>-<Day>
Call without params - load data for yesterday
"""
    def add_arguments(self, parser):
        parser.add_argument('load_day', nargs='?', type=convert_date)

    def handle(self, **options):
        self.stdout.write('test_load called')
        day = options.get('load_day')
        if not day:
            day = datetime.datetime.now(utc).replace(hour=0, minute=0, second=0, microsecond=0) - datetime.timedelta(days=1)
        token = get_auth_token()
        load_report(token, day, NetworkCarrierReport_Simple_test)
        load_report(token, day, NetworkDeviceReport_Simple_test)
        load_report(token, day, NetworkAnalyticsReport_ByPlacement_test)
        load_report(token, day, GeoAnaliticsReport_test)
        load_reports_for_all_advertisers(token, day, SiteDomainPerformanceReport_test)
