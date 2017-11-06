from django.core.management import BaseCommand
from rtb.campaign_rules import checkRules
from rtb.models.placement_state import CampaignRules
from rtb.cron import dayly_task

class Command(BaseCommand):

    def handle(self, **options):
        dayly_task()

        # state = PlacementState(14574547, 7043440)
        # result = state.remove_placement_from_targets_list()
        print "ssss"

