from django.core.management import BaseCommand
from rtb.imp_tracker_cron import get
import datetime



class Command(BaseCommand):

    def handle(self, **options):
        get()

