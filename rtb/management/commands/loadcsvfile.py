from django.core.management import BaseCommand
from rtb.cron import dayly_task, get_current_time


class Command(BaseCommand):
    help = """
Load data from early downloaded csv
Need two params :
    file_name - name of early loadded report
    report_type - name of report type,  from Nexus API description
"""

    def add_arguments(self, parser):
        parser.add_argument('load_day', nargs='?', type=convert_date)

    def handle(self, **options):
        self.stdout.write('loadreportdata called')
