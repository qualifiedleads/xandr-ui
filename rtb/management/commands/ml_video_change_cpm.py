from django.core.management import BaseCommand
from rtb.crons.ml_video_ad_camp_algo_cron import mlChangeCampaignCpmCron

class Command(BaseCommand):
    help = """
    Call to change predicted cpm on appnexus
    """

    def handle(self, *args, **options):
        self.stdout.write('ml_video_change_cpm called')
        mlChangeCampaignCpmCron()

