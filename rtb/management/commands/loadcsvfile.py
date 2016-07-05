from django.core.management import BaseCommand
from rtb.cron import analize_csv
from rtb import models
import django.db.models as m
import os

all_classes = [models.__dict__[k]
               for k in models.__dict__
               if isinstance(models.__dict__[k], m.base.ModelBase)]

all_report_types = {getattr(c, 'api_report_name'): c for c in all_classes if hasattr(c, 'api_report_name')}

class Command(BaseCommand):
    help = """
Load data from early downloaded csv
Need two params :
    file_name - name of early loadded report
    report_type - name of report type,  from Nexus API description
"""

    def add_arguments(self, parser):
        parser.add_argument('file_name', type=str)
        parser.add_argument('report_type', type=str)

    def handle(self, **options):
        self.stdout.write('loadcsvfile called')
        file_name = options.get('file_name')
        report_type = options.get('report_type')
        if report_type not in all_report_types:
            self.stdout.write('Unknown report type. Exit')
            return
        if os.path.isfile(file_name):
            metadata = {'counter': 0}
            analize_csv(file_name, all_report_types[report_type], metadata)
        else:
            self.stdout.write('File not found. Exit')
            return
