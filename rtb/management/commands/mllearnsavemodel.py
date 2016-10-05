from django.core.management import BaseCommand
from rtb.ml_learn_kmeans import mlLearnKmeans

class Command(BaseCommand):
    help = """
    Call to learn and save kmeans centroids into ml_placements_clusters_kmeans
    Number of parametrs:0
    """

    def add_arguments(self, parser):
        parser.add_argument("test_name", type=str)

    def handle(self, *args, **options):
        self.stdout.write('mllearnsavemodel called')
        test_name = options.get("test_name")
        mlLearnKmeans(test_name)
