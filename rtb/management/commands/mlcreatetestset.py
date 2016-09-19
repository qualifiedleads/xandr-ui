from django.core.management import BaseCommand
from rtb.ml_create_dailyfeaturesdb import mlCreatePlacementDailyFeaturesDB

class Command(BaseCommand):
    help = """
    Call to fill ml_placement_daily_features
    Number of parametrs:0
    """

    def handle(self, *args, **options):
        self.stdout.write("mlcreatetestset called")
        mlCreatePlacementDailyFeaturesDB()