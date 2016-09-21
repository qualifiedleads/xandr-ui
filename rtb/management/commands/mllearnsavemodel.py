__author__ = 'USER'

from django.core.management import BaseCommand
from rtb.ml_learn_kmeans import mlLearnKmeans

class Command(BaseCommand):
    help = """
    Call to learn and save kmeans centroids into ml_placements_clusters_kmeans
    Number of parametrs:1
        predict : bool
          true - predict and save results of training set prediction;
          false - just find and save centroids
    """

    def add_arguments(self, parser):
        parser.add_argument('predict', type=bool)

    def handle(self, *args, **options):
        self.stdout.write('mllearnsavemodel called')
        predict = options.get('predict')
        mlLearnKmeans(predict)
