from django.core.management import BaseCommand
from rtb.imp_tracker_cron import get
from rtb.placement_state import PlacementState


class Command(BaseCommand):

    def handle(self, **options):
        state = PlacementState(14574547, [7043440, 7043341])     #   , 7043341
        state.change_state_placement()
        print state


