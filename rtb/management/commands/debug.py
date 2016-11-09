from django.core.management import BaseCommand
from rtb.placement_state import PlacementState


class Command(BaseCommand):

    def handle(self, **options):

        # state = PlacementState(None, None)

        # state.suspend_state_middleware()
        # state
        state = PlacementState(None, None)
        result = state.placement_targets_list()
        print result

        # state = PlacementState(14574547, 7043440)
        # result = state.remove_placement_from_targets_list()
        # print result