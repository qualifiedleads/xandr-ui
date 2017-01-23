import rtb.models as m
from django.core.management import BaseCommand
from rtb.crons.video_ad_cron import fillVideoAdDataCron

class Command(BaseCommand):
    help = """
Loads Site Domain Performance Report for specifed adversiter and period.
Call without params - load all data for last 48 days
Call with one parameter -load data for specifed day. Date must provided as <Year>-<Month>-<Day>
"""

    def handle(self, **options):
        fillVideoAdDataCron()
