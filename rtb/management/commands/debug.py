from django.core.management import BaseCommand
from rtb.campaign_rules import checkRules
from rtb.models.placement_state import CampaignRules

class Command(BaseCommand):

    def handle(self, **options):
        rule = CampaignRules.objects.get(pk=2)
        state = checkRules(rule.campaign_id, rule.rules)
        print state

        # state = PlacementState(14574547, 7043440)
        # result = state.remove_placement_from_targets_list()
        # print result