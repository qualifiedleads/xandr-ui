from django.core.management import BaseCommand
from rtb.ml_learn_kmeans import mlPredictKmeans
from rtb.ml_logistic_regression import mlPredictLogisticRegression
from rtb.ml_decision_tree import mlPredictDecisionClassifierTree

class Command(BaseCommand):
    help = """
    Call for prediction of that placement_id in Kmeans (firsly need to learn)
    Number of parametrs:3
        placement_id - placement for recognition
        test_type - type of the test(kmeans, logistic regression)
        test_name - set of features
    """

    def add_arguments(self, parser):
        parser.add_argument("placement_id", type=int)
        parser.add_argument("test_type", type=str)
        parser.add_argument("test_name", type=str)

    def handle(self, *args, **options):
        self.stdout.write("prediction called")
        placement_id = options.get("placement_id")
        test_type = options.get("test_type")
        test_name = options.get("test_name")
        if test_type == "kmeans":
            mlPredictKmeans(placement_id, test_name)
        if test_type == "log":
            mlPredictLogisticRegression(placement_id, test_name)
        if test_type == "tree":
            mlPredictDecisionClassifierTree(placement_id=placement_id, test_name=test_name)
