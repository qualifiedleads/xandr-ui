from django.core.management import BaseCommand
from rtb.ml_auc import mlBuildROC

class Command(BaseCommand):
    help = """
    Call to save build roc-curve for recognition models
    Number of parametrs: 2
    test_type - name of the used method
    test_name - name of the test (list of features)
    """

    def add_arguments(self, parser):
        parser.add_argument("test_type", type=str)
        parser.add_argument("test_name", type=str)

    def handle(self, *args, **options):
        self.stdout.write('mlbuildroc called')
        test_type = options.get("test_type")
        test_name = options.get("test_name")
        mlBuildROC(test_type, test_name)