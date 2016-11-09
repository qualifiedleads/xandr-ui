from django.core.management import BaseCommand
from rtb.ml_learn_kmeans import mlmakeCsv

class Command(BaseCommand):
    help = """
    Call to save recognition results to csv-file
    Number of parametrs: 1
    test_name - name of the test, which results need to save
    """

    def add_arguments(self, parser):
        parser.add_argument("test_name", type=str)

    def handle(self, *args, **options):
        self.stdout.write('mlcreatecsvresult called')
        test_name = options.get("test_name")
        mlmakeCsv(test_name)