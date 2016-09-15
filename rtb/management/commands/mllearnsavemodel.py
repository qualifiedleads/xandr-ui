__author__ = 'USER'

from django.core.management import BaseCommand
from rtb.ml_learn_kmeans import mlLearnKmeans

class Command(BaseCommand):
    help = """
    Call to learn and save predict model
    Number of parametrs:1
        placement_id - placement for recognition
    """

    def add_arguments(self, parser):
        #parser.add_argument('file_name', type=str)
        parser.add_argument('placement_id', type=int)

    def handle(self, *args, **options):
        self.stdout.write('mllearnsavemode called')
        #file_name = options.get('file_name')
        placement_id = options.get('placement_id')
        #learn(file_name)
        #learn()
        mlLearnKmeans(placement_id)
