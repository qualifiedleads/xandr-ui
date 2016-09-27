from django.core.management import BaseCommand
from rtb.ml_learn_kmeans import mlPredictKmeans
from rtb.views_adv import campaignDomains

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
        """some = "/api/v1/campaigns/:id/domains?from_date=1466667274&to_date=1466667274&skip=0&take=5"
        campaignDomains(some, 13831756)
        return"""

        placement_id = options.get('placement_id')
        mlPredictKmeans(placement_id)
