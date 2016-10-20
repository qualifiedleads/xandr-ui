from django.core.management import BaseCommand
from rtb.ml_learn_kmeans import mlGetPlacementQuallity

class Command(BaseCommand):
    help = """
    Call to check if placement good or bad
    Number of parametrs: 3
    placement_id - which placement to check
    test_type - name of the used method
    test_name - name of the test (list of features)
    """

    def add_arguments(self, parser):
        parser.add_argument("placement_id", type=int)
        parser.add_argument("test_type", type=str)
        parser.add_argument("test_name", type=str)

    def handle(self, *args, **options):
        self.stdout.write('mlcheckplacement called')
        placement_id = options.get("placement_id")
        test_type = options.get("test_type")
        test_name = options.get("test_name")
        mlGetPlacementQuallity(placement_id, test_type, test_name)