import datetime
from django.db import models, transaction
from pytz import utc
from ..report import nexus_get_objects_by_id
from .models import Placement, Campaign, Site, PlatformMember, Publisher, \
     DEAL_PAYMENT_TYPE_CHOICES, REVENUE_TYPE_CHOICES, BID_TYPE_CHOICES, IMPRESSION_TYPE_CHOICES, \
     DEVICE_TYPE_INREPORT_CHOICES, CONNECTION_TYPE_CHOICES, BUYER_TYPE_NetworkDeviceReport_CHOICES, \
     SELLER_TYPE_NetworkDeviceReport_CHOICES



def load_foreign_objects(cls, field_name, ObjectClass, from_date, to_date):
    filter_params = { field_name+'__name':None}
    if hasattr(cls, 'hour'):
        filter_params['hour__gte']=from_date
        filter_params['hour__lte']=to_date
    else:
        filter_params['day__gte']=from_date
        filter_params['day__lte']=to_date

    ids_missing = cls.objects.filter(**filter_params)\
        .values_list(field_name+'_id', flat=True)
    ids_missing = set(ids_missing)
    saved_ids = nexus_get_objects_by_id(None, ObjectClass, ids_missing)
    if saved_ids != ids_missing:
        print 'Some {}s not saved'.format(field_name)

class PostLoadMix(object):
    @classmethod
    def post_load(self, day):
        from_date = datetime.datetime(day.year, day.month, day.day, tzinfo=utc)
        to_date = from_date
        if hasattr(self,'hour'):
            to_date += datetime.timedelta(hours=23)
        load_foreign_objects(self, 'publisher', Publisher, from_date, to_date)


class Carrier(models.Model):
    """
    https://wiki.appnexus.com/display/api/Carrier+Service
    """
    id = models.IntegerField(primary_key=True) # The ID of the mobile carrier.
    name = models.TextField(null=True, blank=True) # The name of the mobile carrier.
    country_code = models.IntegerField(null=True, blank=True) # The ISO code for the country in which the carrier operates.
    country_name = models.TextField(null=True, blank=True) # The name of the country in which the carrier operates.
    codes = models.TextField(null=True, blank=True) # Third-party representations for the mobile carrier. See Codes below for more details.

    api_endpoint = 'carrier'

    class Meta:
        app_label = 'rtb'
        db_table = "carrier"


class NetworkAnalyticsReport_ByPlacement(models.Model):
    hour = models.DateTimeField(null=True, blank=True, db_index=True)
    publisher = models.ForeignKey("Publisher", null=True, blank=True, db_constraint=False, on_delete = models.DO_NOTHING)
    publisher_name = models.TextField(null=True, blank=True)
    placement = models.ForeignKey("Placement", null=True, blank=True, db_constraint=False, on_delete = models.DO_NOTHING)
    placement_name = models.TextField(null=True, blank=True)
    campaign = models.ForeignKey("Campaign", null=True, blank=True, db_constraint=False, on_delete = models.DO_NOTHING)
    campaign_name = models.TextField(null=True, blank=True)
    seller_member = models.ForeignKey("PlatformMember", null=True, blank=True, db_constraint=False, on_delete = models.DO_NOTHING)
    seller_member_name = models.TextField(null=True, blank=True)
    creative = models.ForeignKey("Creative", null=True, blank=True,db_constraint=False, on_delete = models.DO_NOTHING)
    creative_name = models.TextField(null=True, blank=True)
    size = models.TextField(null=True, blank=True)
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

        load_foreign_objects(self, 'publisher', Publisher, from_date, to_date)

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

    class Meta:
        app_label = 'rtb'
        db_table = "network_analytics_report_by_placement"
        index_together = ["campaign", "hour"]

class NetworkCarrierReport_Simple(models.Model, PostLoadMix):
    # https://wiki.appnexus.com/display/api/Network+Carrier+Analytics
    fetch_date = models.DateTimeField(null=True, blank=True, db_index=True)
    # month = time
    day = models.DateTimeField(null=True, blank=True, db_index=True)
    carrier_id = models.ForeignKey("Carrier", null=True, blank=True, db_constraint=False, on_delete = models.DO_NOTHING)
    carrier_name = models.TextField(null=True, blank=True)
    device_type = models.TextField(
        choices=DEVICE_TYPE_INREPORT_CHOICES,
        null=True, blank=True)
    connection_type = models.TextField(
        choices=CONNECTION_TYPE_CHOICES,
        null=True, blank=True)
    seller_member = models.ForeignKey("PlatformMember", null=True, blank=True, db_constraint=False, on_delete = models.DO_NOTHING)
    seller_member_name = models.TextField(null=True, blank=True)
    seller_type = models.TextField(
        choices=SELLER_TYPE_NetworkDeviceReport_CHOICES,
        null=True, blank=True)
    campaign = models.ForeignKey("Campaign", null=True, blank=True, db_constraint=False, on_delete = models.DO_NOTHING)
    campaign_name = models.TextField(null=True, blank=True)
    media_type = models.ForeignKey("MediaType", null=True, blank=True, db_constraint=False, on_delete = models.DO_NOTHING)
    media_type_name = models.TextField(null=True, blank=True) # Need special loading
    size = models.TextField(null=True, blank=True)
    geo_country = models.ForeignKey("Country", null=True, blank=True, db_constraint=False, on_delete = models.DO_NOTHING)
    geo_country_name = models.TextField(null=True, blank=True)
    publisher = models.ForeignKey("Publisher", null=True, blank=True, db_constraint=False, on_delete = models.DO_NOTHING)
    publisher_name = models.TextField(null=True, blank=True)
    imps = models.IntegerField(null=True, blank=True)
    clicks = models.IntegerField(null=True, blank=True)
    total_convs = models.IntegerField(null=True, blank=True)
    cost = models.DecimalField(null=True, blank=True, max_digits=35, decimal_places=10)

    api_report_name='network_carrier_analytics'

    class Meta:
        db_table = "network_carrier_report_simple"
        app_label = 'rtb'

class NetworkDeviceReport_Simple(models.Model, PostLoadMix):
    # https://wiki.appnexus.com/display/api/Network+Device+Analytics
    fetch_date = models.DateTimeField(null=True, blank=True, db_index=True)
    # month = time
    day = models.DateTimeField(null=True, blank=True, db_index=True)
    device_make = models.ForeignKey("DeviceMake", null=True, blank=True, db_constraint=False, on_delete = models.DO_NOTHING)
    device_make_name = models.TextField(null=True, blank=True)
    device_model = models.ForeignKey("DeviceModel", null=True, blank=True, db_constraint=False, on_delete = models.DO_NOTHING)
    device_model_name = models.TextField(null=True, blank=True)
    device_type = models.TextField(
        choices=DEVICE_TYPE_INREPORT_CHOICES,
        null=True, blank=True)
    connection_type = models.TextField(
        choices=CONNECTION_TYPE_CHOICES,
        null=True, blank=True)
    operating_system = models.ForeignKey("OperatingSystemExtended", null=True, blank=True, db_constraint=False, on_delete = models.DO_NOTHING)
    operating_system_name = models.TextField(null=True, blank=True)
    browser = models.ForeignKey("Browser", null=True, blank=True, db_constraint=False, on_delete = models.DO_NOTHING)
    browser_name = models.TextField(null=True, blank=True)
    seller_member = models.ForeignKey("PlatformMember", related_name='+', null=True, blank=True, db_constraint=False, on_delete = models.DO_NOTHING)
    seller_member_name = models.TextField(null=True, blank=True)
    seller_type = models.TextField(
        choices=SELLER_TYPE_NetworkDeviceReport_CHOICES,
        null=True, blank=True)
    campaign = models.ForeignKey("Campaign", null=True, blank=True, db_constraint=False, on_delete = models.DO_NOTHING)
    campaign_name = models.TextField(null=True, blank=True)
    media_type = models.ForeignKey("MediaType", null=True, blank=True, db_constraint=False, on_delete = models.DO_NOTHING)
    media_type_name = models.TextField(null=True, blank=True) # Need special loading
    geo_country = models.ForeignKey("Country", null=True, blank=True, db_constraint=False, on_delete = models.DO_NOTHING)
    geo_country_name = models.TextField(null=True, blank=True)
    publisher = models.ForeignKey("Publisher", null=True, blank=True, db_constraint=False, on_delete = models.DO_NOTHING)
    publisher_name = models.TextField(null=True, blank=True)
    imps = models.IntegerField(null=True, blank=True)
    clicks = models.IntegerField(null=True, blank=True)
    total_convs = models.IntegerField(null=True, blank=True)
    cost = models.DecimalField(null=True, blank=True, max_digits=35, decimal_places=10)

    api_report_name = 'network_device_analytics'

    class Meta:
        db_table = "network_device_report_simple"
        app_label = 'rtb'

docs="""
<input ng-click="campdetails.selectInfoBtn($event, campdetails.ctrlBbtns.placement.header)" name="Placement"
value="Placement" class="nav-btn nav-btn-active" type="button"> <input ng-click="campdetails.selectInfoBtn($event, campdetails.ctrlBbtns.creativeId.header)" name="creative_id"
value="creative_id" class="nav-btn" type="button"> <input ng-click="campdetails.selectInfoBtn($event, campdetails.ctrlBbtns.creativeSize.header)" name="creative_size"
value="creative_size" class="nav-btn" type="button"> <input ng-click="campdetails.selectInfoBtn($event, campdetails.ctrlBbtns.viewability.header)" name="viewability"
value="viewability" class="nav-btn" type="button"> <input ng-click="campdetails.selectInfoBtn($event, campdetails.ctrlBbtns.os.header)" name="OS"
SiteDomainPerformanceReport value="OS" class="nav-btn" type="button"> <input ng-click="campdetails.selectInfoBtn($event, campdetails.ctrlBbtns.carrier.header)" name="carrier"
NetworkCarrierReport value="carrier" class="nav-btn" type="button"> <input ng-click="campdetails.selectInfoBtn($event, campdetails.ctrlBbtns.networkSeller.header)" name="network(seller)"
value="network(seller)" class="nav-btn" type="button"> <input ng-click="campdetails.selectInfoBtn($event, campdetails.ctrlBbtns.connectionType.header)" name="connection_type"
NetworkDeviceReport value="connection_type" class="nav-btn" type="button"> <input ng-click="campdetails.selectInfoBtn($event, campdetails.ctrlBbtns.device.header)" name="device"
NetworkDeviceReport value="device" class="nav-btn" type="button">
"""
