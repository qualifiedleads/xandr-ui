import rtb.models as m

from django.core.management import BaseCommand
from rtb.cron import dayly_task, get_current_time
import datetime


class tee(object):
    def __init__(self, _fd1, _fd2):
        self.fd1 =_fd1
        self.fd2 = _fd2
    def write(self, text):
        self.fd1.write(text)
        self.fd2.write(text)
    def flush(self):
        self.fd1.flush()
        self.fd2.flush()
        
def convert_date(s):
    return datetime.datetime.strptime(s,'%Y-%m-%d')

class Command(BaseCommand):
    help = """
Loads Site Domain Performance Report for specifed adversiter and period.
Call without params - load all data for last 48 days
Call with one parameter -load data for specifed day. Date must provided as <Year>-<Month>-<Day>
"""
    def add_arguments(self, parser):
        parser.add_argument('load_day', nargs='?', type=convert_date)

    def handle(self, **options):
        self.stdout.write('loadreportdata called')
        is_first = True
        p_line = '-'*79+'\n'
        current_day = options.get('load_day')
        if current_day:
            dayly_task(current_day, True, self.stdout)
            return
        current_day = get_current_time().date()
        one_day = datetime.timedelta(days=1)
        current_day-=one_day*31
        with open('rtb/logs/loadreportdata.log', 'w') as f:
            t = tee (self.stdout, f)
            for i in xrange(0,30):
                t.write(p_line)
                t.write('Save data for %s \n'%current_day.strftime('%Y-%m-%d'))
                t.write(p_line)
                dayly_task(current_day, is_first, t)
                is_first = False
                current_day += one_day
