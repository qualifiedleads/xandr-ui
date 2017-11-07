from django.core.management import BaseCommand
from rtb.campaign_rules import checkRules
from rtb.models.placement_state import CampaignRules
from rtb.cron import dayly_task
from rtb.placement_state import PlacementState


class Command(BaseCommand):

    def handle(self, **options):
        dayly_task()
        state = PlacementState(None, None)
        result = state.get_token()
        # state = PlacementState(14574547, 7043440)
        # result = state.remove_placement_from_targets_list()
        print "ssss"

