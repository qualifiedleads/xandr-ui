from django.core.management import BaseCommand
from rtb.ml_learn_kmeans import mlPredictKmeans

class Command(BaseCommand):
    help = """
    Call for prediction of that placement_id in Kmeans (firsly need to learn)
    Number of parametrs:1
        placement_id - placement for recognition
    """

    def add_arguments(self, parser):
        parser.add_argument('placement_id', type=int)

    def handle(self, *args, **options):
        self.stdout.write('mlpredictkmeans called')
        placement_id = options.get('placement_id')
        mlPredictKmeans(placement_id)
