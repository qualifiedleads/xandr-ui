from django.core.management import BaseCommand
from rtb.crons.ml_video_ad_camp_algo_cron import mlRefreshAlgoListCron

class Command(BaseCommand):
    help = """
    Call to save refresh video ad cpm models
    """

    def handle(self, *args, **options):
        self.stdout.write('ml_video_refresh_algo called')
        mlRefreshAlgoListCron()
