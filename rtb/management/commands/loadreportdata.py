import rtb.models as m

from django.core.management import BaseCommand

class Command(BaseCommand):
    help = """
Loads Site Domain Performance Report for specifed adversiter and period.
Call without params - load all data for last 48 days
"""
    def handle(self, *args, **options):
        self.stdout.write('loadreportdata called')