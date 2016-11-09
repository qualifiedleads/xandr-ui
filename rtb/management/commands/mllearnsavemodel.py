from django.core.management import BaseCommand
from rtb.ml_learn_kmeans import mlLearnKmeans
from rtb.ml_logistic_regression import mlLearnLogisticRegression

class Command(BaseCommand):
    help = """
    Call to learn and save kmeans centroids into ml_placements_clusters_kmeans
    Number of parametrs: 1
    test_name - name of the test for which need to learn model
    """

    def add_arguments(self, parser):
        parser.add_argument("test_type", type=str)
        parser.add_argument("test_name", type=str)

    def handle(self, *args, **options):
        self.stdout.write('mllearnsavemodel called')
        test_type = options.get("test_type")
        test_name = options.get("test_name")
        if test_type == "kmeans":
            mlLearnKmeans(test_name)
        if test_type == "log":
            mlLearnLogisticRegression(test_name)
