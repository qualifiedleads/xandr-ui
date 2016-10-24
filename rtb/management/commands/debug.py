from django.core.management import BaseCommand
from rtb.placement_state import PlacementState


class Command(BaseCommand):

    def handle(self, **options):
        state = PlacementState(14574547, [])     #   , 7043341
        result = state.change_state_placement()
        print result


