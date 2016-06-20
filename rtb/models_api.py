from django.db import models
from models import Advertiser
from models import SUPPLY_TYPE, FOLD_POSITION_CHOISE, AGE_BUCKET_CHOISE, GENDER


class API_Campaign(models.Model):
    #https://wiki.appnexus.com/display/api/Campaign+Service
    fetch_date = models.DateTimeField(null=True, blank=True, db_index=True)    
    id = models.IntegerField(null=True, primary_key=True, db_index=True)
    code = models.IntegerField(null=True, blank=True, db_index=True)
    advertiser_id = models.ForeignKey('Advertiser', null=True, blank=True, db_index=True)
    #advertiser_id = models.IntegerField(null=True, blank=True, db_index=True)
    pixel_id = models.IntegerField(null=True, blank=True, db_index=True)
    optimization_version = models.TextField(null=True, blank=True, db_index=True)
    profile_id = models.IntegerField(null=True, blank=True, db_index=True)
    lifetime_budget_imps = models.FloatField(null=True, blank=True, db_index=True)
    inventory_type = models.IntegerField(null=True, blank=True, db_index=True)
    lifetime_budget = models.IntegerField(null=True, blank=True, db_index=True)
    click_url = models.IntegerField(null=True, blank=True, db_index=True)
    bid_modifier_model = models.IntegerField(null=True, blank=True, db_index=True)
    enable_pacing = models.IntegerField(null=True, blank=True, db_index=True)
    allow_safety_pacing = models.IntegerField(null=True, blank=True, db_index=True)
    timezone = models.IntegerField(null=True, blank=True, db_index=True)
    cpc_goal = models.IntegerField(null=True, blank=True, db_index=True)
    optimization_lookback = models.IntegerField(null=True, blank=True, db_index=True)
    line_item_id = models.IntegerField(null=True, blank=True, db_index=True)
    bid_model = models.IntegerField(null=True, blank=True, db_index=True)
    lifetime_pacing_pct = models.IntegerField(null=True, blank=True, db_index=True)
    campaign_type = models.IntegerField(null=True, blank=True, db_index=True)
    defer_to_li_prediction = models.IntegerField(null=True, blank=True, db_index=True)
    impression_limit = models.IntegerField(null=True, blank=True, db_index=True)
    short_name = models.IntegerField(null=True, blank=True, db_index=True)
    cadence_modifier_enabled = models.IntegerField(null=True, blank=True, db_index=True)
    creative_id = models.IntegerField(null=True, blank=True, db_index=True)
    min_bid = models.IntegerField(null=True, blank=True, db_index=True)
    roadblock_type = models.IntegerField(null=True, blank=True, db_index=True)
    comments = models.IntegerField(null=True, blank=True, db_index=True)
    priority = models.IntegerField(null=True, blank=True, db_index=True)
    roadblock_creatives = models.IntegerField(null=True, blank=True, db_index=True)
    state = models.IntegerField(null=True, blank=True, db_index=True)
    max_learn_bid = models.IntegerField(null=True, blank=True, db_index=True)
    allow_unverified_ecp = models.IntegerField(null=True, blank=True, db_index=True)
    require_cookie_for_tracking = models.IntegerField(null=True, blank=True, db_index=True)
    supply_type = models.IntegerField(null=True, blank=True, db_index=True)
    start_date = models.IntegerField(null=True, blank=True, db_index=True)
    bid_multiplier = models.IntegerField(null=True, blank=True, db_index=True)
    daily_budget_imps = models.IntegerField(null=True, blank=True, db_index=True)
    labels = models.IntegerField(null=True, blank=True, db_index=True)
    base_cpm_bid_value = models.IntegerField(null=True, blank=True, db_index=True)
    end_date = models.IntegerField(null=True, blank=True, db_index=True)
    learn_override_type = models.IntegerField(null=True, blank=True, db_index=True)
    valuation = models.IntegerField(null=True, blank=True, db_index=True)
    cpm_bid_type = models.IntegerField(null=True, blank=True, db_index=True)
    ecp_learn_divisor = models.IntegerField(null=True, blank=True, db_index=True)
    creatives = models.IntegerField(null=True, blank=True, db_index=True)
    last_modified = models.IntegerField(null=True, blank=True, db_index=True)
    campaign_modifiers = models.IntegerField(null=True, blank=True, db_index=True)
    creative_distribution_type = models.IntegerField(null=True, blank=True, db_index=True)
    broker_fees = models.IntegerField(null=True, blank=True, db_index=True)
    lifetime_pacing = models.IntegerField(null=True, blank=True, db_index=True)
    remaining_days = models.IntegerField(null=True, blank=True, db_index=True)
    pixels = models.IntegerField(null=True, blank=True, db_index=True)
    supply_type_action = models.IntegerField(null=True, blank=True, db_index=True)
    name = models.IntegerField(null=True, blank=True, db_index=True)
    daily_budget = models.IntegerField(null=True, blank=True, db_index=True)
    learn_threshold = models.IntegerField(null=True, blank=True, db_index=True)
    base_bid = models.IntegerField(null=True, blank=True, db_index=True)
    bid_margin = models.IntegerField(null=True, blank=True, db_index=True)
    max_bid = models.IntegerField(null=True, blank=True, db_index=True)
    cadence_type = models.IntegerField(null=True, blank=True, db_index=True)
    projected_learn_events = models.IntegerField(null=True, blank=True, db_index=True)
    total_days = models.IntegerField(null=True, blank=True, db_index=True)
    lifetime_pacing_span = models.IntegerField(null=True, blank=True, db_index=True)
    cpc_payout = models.IntegerField(null=True, blank=True, db_index=True)
    class Meta:
        db_table = "api_campaign"
    #This function transform data
    def TransformFields(self, metadata={}):
        if not metadata: return
        if type(self.advertiser_id)==type(int):
            advertiser = metatada.get("advertiser_id")
            if not advertiser: advertiser = Advertiser.objects.get(self.advertiser_id)
            self.advertiser_id = advertiser


#table for SiteDomainPerformanceReport. Data extracted from correspondent report
class API_SiteDomainPerformanceReport(models.Model):
    #https://wiki.appnexus.com/display/api/Site+Domain+Performance
    fetch_date = models.DateTimeField(null=True, blank=True, db_index=True)
    advertiser_id = models.ForeignKey('Advertiser', null=True, blank=True, db_index=True)
    #advertiser_id = models.IntegerField(null=True, blank=True, db_index=True)
    campaign = models.ForeignKey("API_Campaign",null=True, blank=True, db_index=True)  
    day = models.DateTimeField(null=True, blank=True, db_index=True)
    site_domain = models.TextField(null=True, blank=True, db_index=True)
    line_item_id = models.IntegerField(null=True, blank=True, db_index=True)
    top_level_category_id = models.IntegerField(null=True, blank=True, db_index=True)
    second_level_category_id = models.IntegerField(null=True, blank=True, db_index=True)
    deal_id = models.IntegerField(null=True, blank=True, db_index=True)
    #campaign_group = campaign_group is a synonymous with line_item .
    buyer_member_id = models.IntegerField(null=True, blank=True, db_index=True)
    operating_system_id = models.IntegerField(null=True, blank=True, db_index=True)
    supply_type = models.TextField(
        choices=SUPPLY_TYPE,
        null=True, blank=True)
    mobile_application_id =  models.TextField(null=True, blank=True, db_index=True)
    mobile_application_name = models.TextField(null=True, blank=True, db_index=True)
    mobile_application = models.TextField(null=True, blank=True, db_index=True)
    fold_position = models.TextField(
        choices=FOLD_POSITION_CHOISE,
        null=True, blank=True)
    age_bucket = models.TextField(
        choices=AGE_BUCKET_CHOISE,
        null=True, blank=True)
    gender = models.TextField(
        choices=GENDER,
        null=True, blank=True)
    is_remarketing = models.IntegerField(null=True, blank=True)
    conversion_pixel_id = models.IntegerField(null=True, blank=True, db_index=True)
    booked_revenue = models.DecimalField(max_digits=35, decimal_places=10)
    clicks = models.IntegerField(null=True, blank=True)
    click_thru_pct = models.FloatField(null=True, blank=True)
    convs_per_mm = models.FloatField(null=True, blank=True)
    convs_rate = models.FloatField(null=True, blank=True)
    cost_ecpa = models.DecimalField(max_digits=35, decimal_places=10)
    cost_ecpc = models.DecimalField(max_digits=35, decimal_places=10)
    cpm = models.DecimalField(max_digits=35, decimal_places=10)
    ctr = models.FloatField(null=True, blank=True)
    imps = models.IntegerField(null=True, blank=True)
    media_cost = models.DecimalField(max_digits=35, decimal_places=10)
    post_click_convs = models.IntegerField(null=True, blank=True)
    post_click_convs_rate = models.FloatField(null=True, blank=True)
    post_view_convs = models.IntegerField(null=True, blank=True)
    post_view_convs_rate = models.FloatField(null=True, blank=True)
    profit = models.DecimalField(max_digits=35, decimal_places=10)
    profit_ecpm = models.DecimalField(max_digits=35, decimal_places=10)
    imps_viewed = models.IntegerField(null=True, blank=True)
    view_measured_imps = models.IntegerField(null=True, blank=True)
    view_rate = models.FloatField(null=True, blank=True)
    view_measurement_rate = models.FloatField(null=True, blank=True)

    class Meta:
        db_table = "api_site_domain_performance_report"
    #This function transform raw data, collected from csv, to value, saved into DB
    def TransformFields(self, metadata={}):
        if not metadata: return
        campaign_name_to_code = metadata["campaign_name_to_code"]
        self.campaign=campaign_name_to_code.get(self.campaign)
        self.advertiser_id = metatada.get("advertiser_id")
