from django.db import models
import common

class NetworkAnalyticsReport_ByPlacement_test(models.Model): #, common.PostLoadMix):
    hour = models.DateTimeField(null=True, blank=True, db_index=True)
    publisher = models.ForeignKey("Publisher", null=True, blank=True, db_constraint=False, related_name="+", on_delete=models.DO_NOTHING)
    publisher_name = models.TextField(null=True, blank=True)
    placement = models.ForeignKey("Placement", null=True, blank=True, db_constraint=False, related_name="+", on_delete=models.DO_NOTHING)
    placement_name = models.TextField(null=True, blank=True)
    campaign = models.ForeignKey("Campaign", null=True, blank=True, db_constraint=False, related_name="+", on_delete=models.DO_NOTHING)
    campaign_name = models.TextField(null=True, blank=True)
    seller_member = models.ForeignKey("PlatformMember", null=True, blank=True, db_constraint=False,
                                      related_name="+", on_delete=models.DO_NOTHING)
    seller_member_name = models.TextField(null=True, blank=True)
    creative = models.ForeignKey("Creative", null=True, blank=True, db_constraint=False, related_name="+", on_delete=models.DO_NOTHING)
    creative_name = models.TextField(null=True, blank=True)
    size = models.TextField(null=True, blank=True)
    imps = models.IntegerField(null=True, blank=True)
    clicks = models.IntegerField(null=True, blank=True)
    cost = models.DecimalField(null=True, blank=True, max_digits=35, decimal_places=10)
    total_convs = models.IntegerField(null=True, blank=True)
    imps_viewed = models.IntegerField(null=True, blank=True)
    view_measured_imps = models.IntegerField(null=True, blank=True)
    view_rate = models.FloatField(null=True, blank=True)
    view_measurement_rate = models.FloatField(null=True, blank=True)
    site = models.ForeignKey("Site", null=True, blank=True, db_constraint=False, related_name="+", on_delete=models.DO_NOTHING)
    site_name = models.TextField(null=True, blank=True)
    geo_country = models.ForeignKey("Country", null=True, blank=True, db_constraint=False, related_name="+", on_delete=models.DO_NOTHING)
    geo_country_name = models.TextField(null=True, blank=True)
    bid_type = models.TextField(null=True, blank=True)
    imp_type_id = models.IntegerField(null=True, blank=True)

    api_report_name = "network_analytics"
    direct_csv = True

    class Meta:
        app_label = 'rtb'
        db_table = "network_analytics_report_by_placement_test"
        index_together = ["campaign", "hour"]

class NetworkCarrierReport_Simple_test(models.Model): #, common.PostLoadMix):
    day = models.DateTimeField(null=True, blank=True, db_index=True)
    carrier = models.ForeignKey("Carrier", null=True, blank=True, db_constraint=False, related_name="+", on_delete = models.DO_NOTHING)
    carrier_name = models.TextField(null=True, blank=True)
    device_type = models.TextField(null=True, blank=True)
    connection_type = models.TextField(null=True, blank=True)
    seller_member = models.ForeignKey("PlatformMember", null=True, blank=True, db_constraint=False, related_name="+", on_delete = models.DO_NOTHING)
    seller_member_name = models.TextField(null=True, blank=True)
    seller_type = models.TextField(null=True, blank=True)
    campaign = models.ForeignKey("Campaign", null=True, blank=True, db_constraint=False, related_name="+", on_delete = models.DO_NOTHING)
    campaign_name = models.TextField(null=True, blank=True)
    media_type = models.ForeignKey("MediaType", null=True, blank=True, db_constraint=False, related_name="+", on_delete = models.DO_NOTHING)
    media_type_name = models.TextField(null=True, blank=True,db_column= 'media_type') # Need special loading
    size = models.TextField(null=True, blank=True)
    geo_country = models.ForeignKey("Country", null=True, blank=True, db_constraint=False, related_name="+", on_delete = models.DO_NOTHING)
    geo_country_name = models.TextField(null=True, blank=True)
    publisher = models.ForeignKey("Publisher", null=True, blank=True, db_constraint=False, related_name="+", on_delete = models.DO_NOTHING)
    publisher_name = models.TextField(null=True, blank=True)
    imps = models.IntegerField(null=True, blank=True)
    clicks = models.IntegerField(null=True, blank=True)
    total_convs = models.IntegerField(null=True, blank=True)
    cost = models.DecimalField(null=True, blank=True, max_digits=35, decimal_places=10)

    api_report_name='network_carrier_analytics'
    add_api_columns = ('media_type',)
    direct_csv = True

    class Meta:
        db_table = "network_carrier_report_simple_test"
        app_label = 'rtb'

class NetworkDeviceReport_Simple_test(models.Model): #, common.PostLoadMix):
    day = models.DateTimeField(null=True, blank=True, db_index=True)
    device_make = models.ForeignKey("DeviceMake", null=True, blank=True, db_constraint=False, related_name="+", on_delete = models.DO_NOTHING)
    device_make_name = models.TextField(null=True, blank=True)
    device_model = models.ForeignKey("DeviceModel", null=True, blank=True, db_constraint=False, related_name="+", on_delete = models.DO_NOTHING)
    device_model_name = models.TextField(null=True, blank=True)
    device_type = models.TextField(null=True, blank=True)
    connection_type = models.TextField(null=True, blank=True)
    operating_system = models.ForeignKey("OperatingSystemExtended", null=True, blank=True, db_constraint=False, related_name="+", on_delete = models.DO_NOTHING)
    operating_system_name = models.TextField(null=True, blank=True)
    browser = models.ForeignKey("Browser", null=True, blank=True, db_constraint=False, related_name="+", on_delete = models.DO_NOTHING)
    browser_name = models.TextField(null=True, blank=True)
    seller_member = models.ForeignKey("PlatformMember", related_name='+', null=True, blank=True, db_constraint=False, on_delete = models.DO_NOTHING)
    seller_member_name = models.TextField(null=True, blank=True)
    seller_type = models.TextField(null=True, blank=True)
    campaign = models.ForeignKey("Campaign", null=True, blank=True, db_constraint=False, related_name="+", on_delete = models.DO_NOTHING)
    campaign_name = models.TextField(null=True, blank=True)
    media_type = models.ForeignKey("MediaType", null=True, blank=True, db_constraint=False, related_name="+", on_delete = models.DO_NOTHING)
    media_type_name = models.TextField(null=True, blank=True,db_column='media_type') # Need special loading
    geo_country = models.ForeignKey("Country", null=True, blank=True, db_constraint=False, related_name="+", on_delete = models.DO_NOTHING)
    geo_country_name = models.TextField(null=True, blank=True)
    publisher = models.ForeignKey("Publisher", null=True, blank=True, db_constraint=False, related_name="+", on_delete = models.DO_NOTHING)
    publisher_name = models.TextField(null=True, blank=True)
    imps = models.IntegerField(null=True, blank=True)
    clicks = models.IntegerField(null=True, blank=True)
    total_convs = models.IntegerField(null=True, blank=True)
    cost = models.DecimalField(null=True, blank=True, max_digits=35, decimal_places=10)

    api_report_name = 'network_device_analytics'
    add_api_columns = ('media_type',)
    direct_csv = True

    class Meta:
        db_table = "network_device_report_simple_test"
        app_label = 'rtb'

class GeoAnaliticsReport_test(models.Model):
    day = models.DateField(null=True, blank=True, db_index=True)  # Yes	The year, month, and day in which the auction took place.
    member = models.ForeignKey("Member", null=True, blank=True, db_constraint=False, related_name="+", on_delete = models.DO_NOTHING) # Yes	The ID of the member.
    advertiser_currency = models.TextField(null=True, blank=True)  # Yes	The type of currency used by the advertiser.
    insertion_order = models.ForeignKey("InsertionOrder", null=True, blank=True, db_constraint=False, related_name="+", on_delete = models.DO_NOTHING)  # Yes	The insertion order ID.
    campaign = models.ForeignKey("Campaign", null=True, blank=True, db_constraint=False, related_name="+", on_delete = models.DO_NOTHING)  # Yes	The campaign ID.
    advertiser = models.ForeignKey("Advertiser", null=True, blank=True, db_constraint=False, related_name="+", on_delete = models.DO_NOTHING)  # Yes	The advertiser ID. If the value is 0, either the impression was purchased by an external buyer, or a default or PSA was shown. For more information on defaults and PSAs, see Network Reporting.
    line_item = models.ForeignKey("LineItem", null=True, blank=True, db_constraint=False, related_name="+", on_delete = models.DO_NOTHING)  # Yes	The line item ID.
    geo_country = models.ForeignKey("Country", null=True, blank=True, db_constraint=False, related_name="+", on_delete = models.DO_NOTHING)  # Yes	The country ID of the user's location as defined by the Country Service. 250 is shown in cases where we don't know the country or if the country doesn't map correctly to a location in our database.
    geo_region = models.ForeignKey("Region", null=True, blank=True, db_constraint=False, related_name="+", on_delete = models.DO_NOTHING)  # Yes	The region ID of the user's location as defined by the Region Service. 4291 is shown in cases where we don't know the region or if the region doesn't map correctly to a location in our database.
    geo_country_name = models.TextField(null=True, blank=True)  # No	The name of the user's country, as defined by the Country Service.
    geo_region_name = models.TextField(null=True, blank=True)  # No	The name of the region of the user's location as defined by the Region Service.
    geo_dma = models.ForeignKey("DemographicArea", null=True, blank=True, db_constraint=False, related_name="+", on_delete = models.DO_NOTHING) # No	The name and ID of the demographic area where the user is located, in the format "New York NY (501)". The string "unknown values (-1)" can appear in cases where we don't know the demographic area or if the demographic area doesn't map correctly to a location in our database.
    pixel = models.ForeignKey("ConversionPixel", null=True, blank=True, db_constraint=False, related_name="+", on_delete = models.DO_NOTHING)  # Yes The unique identification number of the conversion pixel.
    imps = models.IntegerField(null=True, blank=True)  # imps	The total number of impressions (served and resold).
    clicks = models.IntegerField(null=True, blank=True)  # clicks	The total number of clicks across all impressions.
    cost = models.DecimalField(max_digits=16, decimal_places=2, null=True, blank=True)  # cost	The total cost of the inventory purchased.
    booked_revenue = models.DecimalField(max_digits=16, decimal_places=2, null=True, blank=True)  # booked_revenue	The total revenue booked through direct advertisers (line item).
    cpm = models.DecimalField(max_digits=16, decimal_places=2, null=True, blank=True)  # cpm	The cost per one thousand impressions.
    total_convs = models.IntegerField(null=True, blank=True)  # total_convs	The total number of post-view and post-click conversions.
    convs_rate = models.FloatField(null=True, blank=True)  # total_convs / imps	The ratio of conversions to impressions.
    post_view_convs = models.IntegerField(null=True, blank=True)  # post_view_convs	The total number of recorded post-view conversions.
    post_click_convs = models.IntegerField(null=True, blank=True)  # post_click_convs	The total number of recorded post-click conversions.
    profit = models.DecimalField(max_digits=16, decimal_places=2, null=True, blank=True)  # booked_revenue - media_cost	The total revenue minus the cost.
    click_thru_pct = models.FloatField(null=True, blank=True)  # (clicks / imps) x 100	The rate of clicks to impressions, expressed as a percentage.
    external_imps = models.IntegerField(null=True, blank=True)  # external_imps	The number of external (non-network) impressions.
    external_clicks = models.IntegerField(null=True, blank=True)  # external_clicks	The number of external (non-network) clicks.
    booked_revenue_adv_curr = models.DecimalField(max_digits=16, decimal_places=2, null=True, blank=True)  # booked_revenue_adv_curr	The total revenue booked through a direct advertiser, expressed in the currency of that advertiser.

    api_report_name = "geo_analytics"
    direct_csv = True

    class Meta:
        db_table = "geo_analytics_report_test"
        app_label = 'rtb'


class SiteDomainPerformanceReport_test(models.Model):
    day = models.DateTimeField(null=True, blank=True, db_index=True)
    site_domain = models.TextField(null=True, blank=True, db_index=True)
    campaign = models.ForeignKey("Campaign", null=True, blank=True, db_constraint=False, related_name="+", on_delete = models.DO_NOTHING)
    line_item = models.ForeignKey("LineItem", null=True, blank=True, db_constraint=False, related_name="+", on_delete = models.DO_NOTHING)
    top_level_category = models.ForeignKey("ContentCategory", null=True, blank=True, db_constraint=False, related_name="+", on_delete = models.DO_NOTHING)
    second_level_category = models.ForeignKey("ContentCategory", null=True, blank=True, db_constraint=False, related_name="+", on_delete = models.DO_NOTHING)
    deal = models.ForeignKey("Deal", null=True, blank=True, db_constraint=False, related_name="+", on_delete = models.DO_NOTHING)
    advertiser = models.ForeignKey("Advertiser", null=True, blank=True, db_constraint=False, related_name="+", on_delete = models.DO_NOTHING)
    buyer_member = models.ForeignKey("Member", null=True, blank=True, db_constraint=False, related_name="+", on_delete = models.DO_NOTHING)
    operating_system = models.ForeignKey("OperatingSystemExtended", null=True, blank=True, db_constraint=False, related_name="+", on_delete = models.DO_NOTHING)
    supply_type = models.TextField(null=True, blank=True)
    mobile_application_id =  models.TextField(null=True, blank=True, db_index=True)
    mobile_application_name = models.TextField(null=True, blank=True, db_index=True)
    mobile_application = models.TextField(null=True, blank=True, db_index=True)
    fold_position = models.TextField(null=True, blank=True)
    age_bucket = models.TextField(null=True, blank=True)
    gender = models.TextField(null=True, blank=True)
    is_remarketing = models.NullBooleanField()
    conversion_pixel = models.ForeignKey("ConversionPixel", null=True, blank=True, db_constraint=False, related_name="+", on_delete = models.DO_NOTHING)
    booked_revenue = models.DecimalField(null=True, blank=True, max_digits=35, decimal_places=10)
    clicks = models.IntegerField(null=True, blank=True)
    click_thru_pct = models.FloatField(null=True, blank=True)
    convs_per_mm = models.FloatField(null=True, blank=True)
    convs_rate = models.FloatField(null=True, blank=True)
    cost_ecpa = models.DecimalField(null=True, blank=True, max_digits=35, decimal_places=10)
    cost_ecpc = models.DecimalField(null=True, blank=True, max_digits=35, decimal_places=10)
    cpm = models.DecimalField(null=True, blank=True, max_digits=35, decimal_places=10)
    ctr = models.FloatField(null=True, blank=True)
    imps = models.IntegerField(null=True, blank=True)
    media_cost = models.DecimalField(null=True, blank=True, max_digits=35, decimal_places=10)
    post_click_convs = models.IntegerField(null=True, blank=True)
    post_click_convs_rate = models.FloatField(null=True, blank=True)
    post_view_convs = models.IntegerField(null=True, blank=True)
    post_view_convs_rate = models.FloatField(null=True, blank=True)
    profit = models.DecimalField(null=True, blank=True, max_digits=35, decimal_places=10)
    profit_ecpm = models.DecimalField(null=True, blank=True, max_digits=35, decimal_places=10)
    imps_viewed = models.IntegerField(null=True, blank=True)
    view_measured_imps = models.IntegerField(null=True, blank=True)
    view_rate = models.FloatField(null=True, blank=True)
    view_measurement_rate = models.FloatField(null=True, blank=True)

    api_report_name = "site_domain_performance"
    direct_csv = True

    class Meta:
        db_table = "site_domain_performance_report_test"
        app_label = 'rtb'
        index_together = ["advertiser", "day"]
