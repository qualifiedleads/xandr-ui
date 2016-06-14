import datetime


from django.db import models
#from django.contrib.postgres.fields import ArrayField
#from django.contrib.postgres.fields import JSONField


class UserType(models.Model):
    description = models.TextField()

    class Meta:
        db_table = "user_type"


class User(models.Model):
    is_active = models.BooleanField()
    username = models.TextField(db_index=True)
    email = models.TextField(db_index=True)
    first_name = models.TextField()
    last_name = models.TextField()
    password = models.TextField()
    date_added = models.DateTimeField(default=datetime.datetime.now)
    user_type = models.ForeignKey('UserType', null=True, blank=True, db_index=True)

    class Meta:
        db_table = "user"


class Category(models.Model):
    #https://wiki.appnexus.com/display/api/Category+Service
    name = models.TextField(null=True, blank=True, db_index=True)
    is_sensitive = models.NullBooleanField(null=True, blank=True)
    requires_whitelist = models.NullBooleanField(null=True, blank=True)
    requires_whitelist_on_external = models.NullBooleanField(null=True, blank=True)
    last_modified = models.DateTimeField(null=True, blank=True)
    is_brand_eligible = models.NullBooleanField(null=True, blank=True)
    #countries_and_brands = db.Column(db.String) #array of objects !!! need to look at data returned by API ! it is a mess! See the model BrandInCountry below

    class Meta:
        db_table = "category"


class Brand(models.Model):
    #https://wiki.appnexus.com/display/api/Brand+Service
    name = models.TextField(null=True, blank=True, db_index=True)
    urls = models.TextField(null=True, blank=True, db_index=True)#ArrayField(models.TextField(null=True, blank=True), null=True, blank=True)
    is_premium = models.NullBooleanField(null=True, blank=True)
    category = models.ForeignKey("Category", null=True, blank=True)
    company_id = models.IntegerField(null=True, blank=True, db_index=True) #TODO FK is needed in future
    num_creatives = models.IntegerField(null=True, blank=True)
    last_modified = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = "brand"


class Country(models.Model):
    #https://wiki.appnexus.com/display/api/Country+Service
    name = models.TextField(null=True, blank=True, db_index=True)
    code = models.TextField(null=True, blank=True) #enum in origin

    class Meta:
        db_table = "country"


class BrandInCountry(models.Model):
    #See the model Category.countries_and_brands
    brand = models.ForeignKey("Brand", null=True, blank=True)
    category = models.ForeignKey("Category", null=True, blank=True)

    class Meta:
        db_table = "brand_in_country"


STATE_CHOICES = (
    ('ACTIVE', 'Active'),
    ('INACTIVE', 'Inactive'),
)

TIME_FORMAT_CHOICES = (
    ('12', '12-Hour'),
    ('24', '24-Hour'),
)


class Advertiser(models.Model):
    #https://wiki.appnexus.com/display/api/Advertiser+Service
    code = models.TextField(null=True, blank=True, db_index=True)
    name = models.TextField(null=True, blank=True, db_index=True)
    state = models.TextField(
        choices=STATE_CHOICES,
        default="ACTIVE",
        null=True, blank=True)
    default_brand_id = models.IntegerField(null=True, blank=True, db_index=True)
    remarketing_segment_id = models.IntegerField(null=True, blank=True, db_index=True)
    lifetime_budget = models.FloatField(null=True, blank=True)
    lifetime_budget_imps = models.IntegerField(null=True, blank=True)
    daily_budget = models.FloatField(null=True, blank=True)
    daily_budget_imps = models.IntegerField(null=True, blank=True)
    #competitive_brands #see model AdvertiserBrands below
    #competitive_categories	#see model AdvertiserCategories below
    enable_pacing = models.NullBooleanField(null=True, blank=True)
    allow_safety_pacing = models.NullBooleanField(null=True, blank=True)
    profile_id = models.IntegerField(null=True, blank=True, db_index=True) #TODO FK is needed in future
    control_pct = models.FloatField(null=True, blank=True)
    timezone = models.TextField(null=True, blank=True) #originally it is enum
    last_modified = models.DateTimeField(null=True, blank=True)
    #stats	object #should be in sepparait model if needed
    #billing_internal_user	array
    billing_name = models.TextField(null=True, blank=True)
    billing_phone = models.TextField(null=True, blank=True)
    billing_address1 = models.TextField(null=True, blank=True)
    billing_address2 = models.TextField(null=True, blank=True)
    billing_city = models.TextField(null=True, blank=True)
    billing_state = models.TextField(null=True, blank=True)
    billing_country = models.TextField(null=True, blank=True)
    billing_zip = models.TextField(null=True, blank=True)
    default_currency = models.TextField(null=True, blank=True)
    default_category = models.TextField(null=True, blank=True) #object in origin - no description! need to see real data
    #labels	array - see model AdvertiserLabels below
    use_insertion_orders = models.NullBooleanField(null=True, blank=True)
    time_format = models.TextField(
        choices=TIME_FORMAT_CHOICES,
        default="12",
        null=True, blank=True)
    default_brand_id = models.ForeignKey("Brand", null=True, blank=True) #default_brand in origin API responce
    is_mediated = models.NullBooleanField(null=True, blank=True)
    is_malicious = models.NullBooleanField(null=True, blank=True)
    #object_stats	object #should be in sepparait model if needed
    #thirdparty_pixels	array # see the model AdvertiserThirdpartyPixels below

    class Meta:
        db_table = "advertiser"

class AdvertiserBrand(models.Model):
    advertiser = models.ForeignKey("Advertiser", null=True, blank=True)
    brand = models.ForeignKey("Brand", null=True, blank=True)

    class Meta:
        db_table = "advertiser_brand"


class AdvertiserCategory(models.Model):
    advertiser = models.ForeignKey("Advertiser", null=True, blank=True)
    category = models.ForeignKey("Category", null=True, blank=True)

    class Meta:
        db_table = "advertiser_category"

LABELED_OBJECT_TYPE = (
    ('advertiser', 'Advertiser'),
    ('insertion_order', 'Insertion order'),
    ('line_item', 'Line item'),
    ('campaign', 'Campaign'),
    ('publisher', 'Publisher')
)


class Label(models.Model):
    # 1 (Salesperson), 3 (Account Manager), 12 (Advertiser Type), 2 (Salesperson), 4 (Account Manager)
    name = models.TextField(null=True, blank=True, db_index=True)
    member_id = models.IntegerField(null=True, blank=True, db_index=True) #TODO FK is needed in future
    is_user_associated = models.NullBooleanField(null=True, blank=True)
    is_reporting_enabled = models.NullBooleanField(null=True, blank=True)
    object_type = models.TextField(
        choices=LABELED_OBJECT_TYPE,
        null=True, blank=True,
        db_index=True)
    report_field = models.TextField(null=True, blank=True)
    #values # see model LabeledObject model below
    last_modified = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = "label"


class LabeledObject(models.Model):
    label = models.ForeignKey("Label", null=True, blank=True)
    advertiser_id = models.ForeignKey("Advertiser", null=True, blank=True)
    insertion_order_id = models.IntegerField(null=True, blank=True,db_index=True) #TODO FK is needed in future
    line_item_id = models.IntegerField(null=True, blank=True, db_index=True) #TODO FK is needed in future
    campaign_id = models.IntegerField(null=True, blank=True, db_index=True) #TODO FK is needed in future
    publisher_id = models.IntegerField(null=True, blank=True, db_index=True) #TODO FK is needed in future
    value = models.TextField(null=True, blank=True)

    class Meta:
        db_table = "labeled_object"


class AdvertiserLabel(models.Model):
    label = models.ForeignKey("Label", null=True, blank=True) #id in origin
    advertiser = models.ForeignKey("Advertiser", null=True, blank=True)
    #name = models.TextField(null=True, blank=True, db_index=True) #enum on origin  1 (Salesperson), 3 (Account Manager), 12 (Advertiser Type)
    value = models.TextField(null=True, blank=True)

    class Meta:
        db_table = "advertiser_label"


class AdvertiserThirdpartyPixel(models.Model):
    advertiser = models.ForeignKey("Advertiser", null=True, blank=True)
    thirdparty_pixel = models.ForeignKey("ThirdPartyPixel", null=True, blank=True)

    class Meta:
        db_table = "advertiser_thirdparty_pixel"


class ThirdPartyPixel(models.Model):
    is_active = models.NullBooleanField(null=True, blank=True)
    name = models.TextField(null=True, blank=True, db_index=True)

    class Meta:
        db_table = "thirdparty_pixel"


class NetworkAnalyticsRaw(models.Model):
    json = models.TextField(null=True, blank=True)#JSONField(null=True, blank=True)
    csv = models.TextField(null=True, blank=True)
    report_type = models.TextField(null=True, blank=True)
    report_id = models.TextField(null=True, blank=True) #TODO FK is needed in future
    last_updated = models.DateTimeField(default=datetime.datetime.now)

    class Meta:
        db_table = "network_analytics_raw"

    def __unicode__(self):
        return self.id

MEDIA_TYPE_SIZES = (
    ('always', 'Width and height are required when adding creatives (Banner, Expandable, and Facebook)'),
    ('sometimes', 'Width and height are sometimes required when adding creatives (Pop and Text)'),
    ('never', 'Width and height are not required when adding creatives (Interstitial, Video, and Skin)')
)

class MediaType(models.Model):
    #https://wiki.appnexus.com/display/api/Media+Type+Service
    name = models.TextField(null=True, blank=True, db_index=True)
    media_type_group_id = models.IntegerField(null=True, blank=True, db_index=True) #TODO FK is needed in future. It is not clear what is Group yet...
    uses_sizes = models.TextField(
        choices=MEDIA_TYPE_SIZES,
        null=True, blank=True)
    last_modified = models.DateTimeField(default=datetime.datetime.now)

    class Meta:
        db_table = "media_type"


RESELLING_EXPOSURE_CHOICES = (
    ('public', 'public'),
    ('private', 'private')
)

INVENTORY_RELATIONSHIP = (
    ('unknown', 'unknown'),
    ('owned_operated', 'owned_operated'),
    ('direct', 'direct'),
    ('indirect_single_publisher', 'indirect_single_publisher'),
    ('indirect_multiple_publishers', 'indirect_multiple_publishers')
)

INVENTORY_SOURCE = (
    ('other', 'other'),
    ('rubicon', 'rubicon'),
    ('openx', 'openx'),
    ('pubmatic', 'pubmatic'),
    ('aol', 'aol')
)

DISCLOSURE_STATUS = (
    ('undisclosed', 'undisclosed'),
    ('disclosed_pending', 'disclosed_pending'),
    ('disclosed_approved', 'disclosed_approved'),
    ('disclosed_rejected', 'disclosed_rejected')
)

class Publisher(models.Model):
    #https://wiki.appnexus.com/display/api/Publisher+Service
    code = models.TextField(null=True, blank=True, db_index=True)
    name = models.TextField(null=True, blank=True, db_index=True)
    state = models.TextField(
        choices=STATE_CHOICES,
        null=True, blank=True)
    expose_domains = models.NullBooleanField(null=True, blank=True)
    enable_cookie_tracking_default = models.NullBooleanField(null=True, blank=True)
    reselling_exposure = models.TextField(
        choices=RESELLING_EXPOSURE_CHOICES,
        null=True, blank=True)
    reselling_exposed_on = models.DateTimeField(default=datetime.datetime.now)
    reselling_name = models.TextField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    is_rtb = models.NullBooleanField(null=True, blank=True)
    timezone = models.TextField(null=True, blank=True) #originally it is enum
    last_modified = models.DateTimeField(default=datetime.datetime.now)
    # stats	object #should be in sepparait model if needed
    max_learn_pct = models.IntegerField(null=True, blank=True)
    learn_bypass_cpm = models.IntegerField(null=True, blank=True)
    ad_quality_advanced_mode_enabled = models.NullBooleanField(null=True, blank=True)
    allow_report_on_default_imps = models.NullBooleanField(null=True, blank=True)
    default_site_id =  models.IntegerField(null=True, blank=True, db_index=True) #TODO FK is needed in future
    default_ad_profile_id =  models.IntegerField(null=True, blank=True, db_index=True) #TODO FK is needed in future
    billing_dba = models.TextField(null=True, blank=True)
    billing_address1 = models.TextField(null=True, blank=True)
    billing_address2 = models.TextField(null=True, blank=True)
    billing_city = models.TextField(null=True, blank=True)
    billing_state = models.TextField(null=True, blank=True)
    billing_zip = models.TextField(null=True, blank=True)
    billing_country = models.TextField(null=True, blank=True)
    accept_supply_partner_usersync = models.NullBooleanField(null=True, blank=True)
    accept_demand_partner_usersync = models.NullBooleanField(null=True, blank=True)
    accept_data_provider_usersync = models.NullBooleanField(null=True, blank=True)
    ym_profile_id =  models.IntegerField(null=True, blank=True, db_index=True) #TODO FK is needed in future
    allow_cpm_managed = models.NullBooleanField(null=True, blank=True)
    allow_cpm_external = models.NullBooleanField(null=True, blank=True)
    allow_cpa_managed = models.NullBooleanField(null=True, blank=True)
    allow_cpa_external = models.NullBooleanField(null=True, blank=True)
    allow_cpc_managed = models.NullBooleanField(null=True, blank=True)
    allow_cpc_external = models.NullBooleanField(null=True, blank=True)
    managed_cpc_bias_pct = models.IntegerField(null=True, blank=True)
    managed_cpa_bias_pct = models.IntegerField(null=True, blank=True)
    external_cpc_bias_pct = models.IntegerField(null=True, blank=True)
    external_cpa_bias_pct = models.IntegerField(null=True, blank=True)
    is_oo = models.NullBooleanField(null=True, blank=True)
    base_payment_rule_id =  models.IntegerField(null=True, blank=True, db_index=True) #TODO FK is needed in future
    base_ad_quality_rule_id =  models.IntegerField(null=True, blank=True, db_index=True) #TODO FK is needed in future
    currency = models.TextField(null=True, blank=True)
    visibility_profile_id =  models.IntegerField(null=True, blank=True, db_index=True) #TODO FK is needed in future
    billing_internal_user = models.IntegerField(null=True, blank=True)
    # labels	array - see model PublisherLabel below
    # placements = array - see model PublisherPlacements below
    # external_inv_codes = array - see model PublisherExternalInventoryCodes below
    cpm_reselling_disabled = models.NullBooleanField(null=True, blank=True)
    cpc_reselling_disabled = models.NullBooleanField(null=True, blank=True)
    platform_ops_notes = models.TextField(null=True, blank=True)
    pitbull_segment_id =  models.IntegerField(null=True, blank=True, db_index=True) #TODO FK is needed in future
    pitbull_segment_value = models.IntegerField(null=True, blank=True)
    #publisher_brand_exceptions = array - see model PublisherBrandExceptions below
    seller_page_cap_enabled = models.NullBooleanField(null=True, blank=True)
    inventory_relationship = models.TextField(
        choices=INVENTORY_RELATIONSHIP,
        null=True, blank=True)
    inventory_source = models.TextField(
        choices=INVENTORY_SOURCE,
        null=True, blank=True)
    disclosure_status = models.TextField(
        choices=DISCLOSURE_STATUS,
        null=True, blank=True)
    inventory_source_name = models.TextField(null=True, blank=True)
    #contact = array - see model PublisherContact below

    class Meta:
        db_table = "publisher"


class PublisherContact(models.Model):
    publisher = models.ForeignKey("Publisher", null=True, blank=True)
    name = models.TextField(null=True, blank=True)
    phone = models.TextField(null=True, blank=True)
    email = models.TextField(null=True, blank=True)

    class Meta:
        db_table = "publisher_contact"


class PublisherBrandExceptions(models.Model):
    publisher = models.ForeignKey("Publisher", null=True, blank=True)
    brand = models.ForeignKey("Brand", null=True, blank=True)

    class Meta:
        db_table = "publisher_brand_exceptions"


class PublisherExternalInventoryCode(models.Model):
    #https://wiki.appnexus.com/display/api/External+Inventory+Code+Service
    publisher = models.ForeignKey("Publisher", null=True, blank=True)
    name = models.TextField(null=True, blank=True, db_index=True)
    code = models.TextField(null=True, blank=True, db_index=True)

    class Meta:
        db_table = "publisher_external_inventory_code"


class PublisherLabel(models.Model):
    label = models.ForeignKey("Label", null=True, blank=True) #id in origin
    publisher = models.ForeignKey("Publisher", null=True, blank=True)
    #name = models.TextField(null=True, blank=True, db_index=True) #enum in origin 2 (Salesperson), 4 (Account Manager)
    value = models.TextField(null=True, blank=True)

    class Meta:
        db_table = "publisher_label"


class Placement(models.Model):
    name = models.TextField(null=True, blank=True, db_index=True)
    #TODO to be continued

    class Meta:
        db_table = "placement"


class PublisherPlacement(models.Model):
    placement = models.ForeignKey("Placement", null=True, blank=True) #id in origin
    publisher = models.ForeignKey("Publisher", null=True, blank=True)
    code = models.TextField(null=True, blank=True)

    class Meta:
        db_table = "publisher_placement"


class NetworkAnalyticsReport(models.Model):
    hour = models.DateTimeField(null=True, blank=True, db_index=True)
    entity_member_id = models.IntegerField(null=True, blank=True, db_index=True) #TODO FK is needed in future
    buyer_member_id = models.IntegerField(null=True, blank=True, db_index=True) #TODO FK is needed in future
    seller_member_id = models.IntegerField(null=True, blank=True, db_index=True) #TODO FK is needed in future
    advertiser_id = models.ForeignKey("Advertiser", null=True, blank=True)
    adjustment_id = models.IntegerField(null=True, blank=True, db_index=True) #TODO FK is needed in future
    publisher_id = models.ForeignKey("Publisher", null=True, blank=True)
    pub_rule_id = models.IntegerField(null=True, blank=True, db_index=True) #TODO FK is needed in future
    site_id = models.IntegerField(null=True, blank=True, db_index=True) #TODO FK is needed in future
    pixel_id = models.IntegerField(null=True, blank=True, db_index=True) #TODO FK is needed in future
    placement_id = models.IntegerField(null=True, blank=True, db_index=True) #TODO FK is needed in future
    insertion_order_id = models.IntegerField(null=True, blank=True, db_index=True) #TODO FK is needed in future
    line_item_id = models.IntegerField(null=True, blank=True, db_index=True) #TODO FK is needed in future
    campaign_id = models.IntegerField(null=True, blank=True, db_index=True) #TODO FK is needed in future
    creative_id = models.IntegerField(null=True, blank=True, db_index=True) #TODO FK is needed in future
    size = models.TextField(null=True, blank=True)
    brand_id = models.ForeignKey("Brand", null=True, blank=True)
    billing_period_start_date = models.DateTimeField(null=True, blank=True, db_index=True)
    billing_period_end_date = models.DateTimeField(null=True, blank=True, db_index=True)
    geo_country = models.TextField(null=True, blank=True)
    inventory_class = models.TextField(null=True, blank=True)
    bid_type = models.TextField(null=True, blank=True)
    imp_type_id = models.IntegerField(null=True, blank=True, db_index=True) #TODO FK is needed in future
    buyer_type = models.TextField(null=True, blank=True)
    seller_type = models.TextField(null=True, blank=True)
    revenue_type_id = models.IntegerField(null=True, blank=True, db_index=True) #TODO FK is needed in future

    supply_type = models.TextField(null=True, blank=True)
    payment_type = models.TextField(null=True, blank=True)
    deal_id = models.IntegerField(null=True, blank=True, db_index=True) #TODO FK is needed in future
    media_type_id = models.ForeignKey("MediaType", null=True, blank=True) #TODO FK is needed in future

    class Meta:
        db_table = "network_analytics_report"
        index_together = ["advertiser_id", "hour"]
        index_together = ["publisher_id", "hour"]
        index_together = ["campaign_id", "hour"]
