import rtb.models as m

from django.core.management import BaseCommand
from rtb.cron import dayly_task, get_current_time
import datetime


class Command(BaseCommand):
    help = """
Loads Site Domain Performance Report for specifed adversiter and period.
Call without params - load all data for last 48 days
"""
    def handle(self, *args, **options):
        self.stdout.write('loadreportdata called')
        current_day = get_current_time().replace(hour=0, minute=0, second=0)
        one_day = datetime.timedelta(days=1)
        current_day-=one_day*31
        is_first = True
        p_line = '-'*79+'\n'
        with open('rtb/logs/loadreportdata,log', 'w') as f:
            for i in xrange(0,20):
                f.write(p_line)
                f.write('Save data for %s \n'%current_day.strftime('%Y-%m-%d'))
                f.write(p_line)
                dayly_task(current_day, is_first, f)
                is_first = False
                current_day += one_day