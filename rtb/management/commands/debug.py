from django.core.management import BaseCommand
from rtb.placement_state import PlacementState


class Command(BaseCommand):

    def handle(self, **options):
        state = PlacementState(None, None)     #   , 7043341
        result = state.placement_targets_list()
        print result


