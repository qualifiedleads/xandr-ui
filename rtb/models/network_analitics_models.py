import datetime
from django.db import models, transaction
from pytz import utc
from ..report import nexus_get_objects_by_id
from .models import Placement, Campaign, Site, PlatformMember

class NetworkAnalyticsReport_ByPlacement(models.Model):
    hour = models.DateTimeField(null=True, blank=True, db_index=True)
    placement = models.ForeignKey("Placement", null=True, blank=True, db_constraint=False, on_delete = models.DO_NOTHING)
    campaign = models.ForeignKey("Campaign", null=True, blank=True, db_constraint=False, on_delete = models.DO_NOTHING)
    seller_member = models.ForeignKey("PlatformMember", null=True, blank=True, db_constraint=False, on_delete = models.DO_NOTHING)
    imps = models.IntegerField(null=True, blank=True)
    clicks = models.IntegerField(null=True, blank=True)
    cost = models.DecimalField(null=True, blank=True, max_digits=35, decimal_places=10)
    total_convs = models.IntegerField(null=True, blank=True)

    api_report_name = "network_analytics"

    @classmethod
    def post_load(self, day):
        from_date = datetime.datetime(day.year, day.month, day.day, tzinfo=utc)
        to_date = datetime.datetime(day.year, day.month, day.day, 23, tzinfo=utc)
        campaigns_mising = self.objects.filter(
            hour__gte=from_date,
            hour__lte=to_date,
            campaign__name=None
        ).values_list('campaign_id', flat=True)
        campaigns_mising = set(campaigns_mising)
        saved_ids = nexus_get_objects_by_id(None,Campaign,campaigns_mising)
        if saved_ids != campaigns_mising:
            print 'Some campaigns not saved'
        sellers_mising = self.objects.filter(
            hour__gte=from_date,
            hour__lte=to_date,
            seller_member__name=None
        ).values_list('seller_member_id', flat=True)
        sellers_mising = set(sellers_mising)
        saved_ids = nexus_get_objects_by_id(None,PlatformMember,sellers_mising)
        if saved_ids != sellers_mising:
            print 'Some sellers not saved'
        with transaction.atomic():
            placements_mising = self.objects.filter(
                hour__gte=from_date,
                hour__lte=to_date,
                placement__name=None
            ).values_list('placement_id', flat=True)
            placements_mising = set(placements_mising)
            # load all missing placements
            saved_ids = nexus_get_objects_by_id(None,Placement,placements_mising)
            if saved_ids != placements_mising:
                print 'Some placements not saved'
            sites_missing = Placement.objects.filter(
                pk__in=placements_mising,
                site__name=None
            ).values_list('site_id', flat=True)
            sites_missing = set(sites_missing)
            saved_ids = nexus_get_objects_by_id(None,Site,sites_missing)
            if saved_ids != sites_missing:
                print 'Some sites not saved'

            publishers_missing = Placement.objects.filter(
                pk__in=placements_mising,
                publisher__name=None
            ).values_list('publisher_id', flat=True)
            publishers_missing = set(publishers_missing)
            saved_ids = nexus_get_objects_by_id(None, Site, publishers_missing)
            if saved_ids != publishers_missing:
                print 'Some publishers not saved'

    class Meta:
        app_label = 'rtb'
        db_table = "network_analytics_report_by_placement"
        index_together = ["campaign", "hour"]
