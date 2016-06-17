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
    ('active', 'Active'),
    ('inactive', 'Inactive'),
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
    last_updated = models.DateTimeField()

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
    last_modified = models.DateTimeField()

    class Meta:
        db_table = "media_type"


class MediaSubType(models.Model):
    #https: // wiki.appnexus.com / display / api / Media + Subtype + Service
    name = models.TextField(null=True, blank=True, db_index=True)
    media_type = models.ForeignKey("MediaType", null=True, blank=True)
    #permitted_sizes - see model MediaSubTypePermittedSizes below
    #native_assets - see model MediaSubTypeNativeAssets below
    last_modified = models.DateTimeField()

    class Meta:
        db_table = "media_sub_type"


class MediaSubTypePermittedSizes(models.Model):
    media_sub_type = models.ForeignKey("MediaSubType", null=True, blank=True)
    platform_width = models.IntegerField(null=True, blank=True)
    platform_height = models.IntegerField(null=True, blank=True)
    validate_image_size = models.NullBooleanField(null=True, blank=True)
    scaling_permitted = models.NullBooleanField(null=True, blank=True)
    aspect_ratio_tolerance = models.FloatField(null=True, blank=True)
    min_image_width = models.IntegerField(null=True, blank=True)
    max_image_width = models.IntegerField(null=True, blank=True)
    min_image_height = models.IntegerField(null=True, blank=True)
    max_image_height = models.IntegerField(null=True, blank=True)

    class Meta:
        db_table = "media_sub_type_permitted_sizes"


NATIVE_ASSETS_NAME = (
    ('title', 'title'),
    ('content', 'content'),
    ('description', 'description'),
    ('full_text', 'full_text'),
    ('context', 'context'),
    ('icon_img_url', 'icon_img_url'),
    ('main_media', 'main_media'),
    ('cta', 'cta'),
    ('rating', 'rating'),
    ('click_fallback_url', 'click_fallback_url')
)


MEDIA_REQUIRENMENT = (
    ('required', 'required'),
    ('recommended', 'recommended'),
    ('optional', 'optional')
)


class MediaSubTypeNativeAssets(models.Model):
    media_sub_type = models.ForeignKey("MediaSubType", null=True, blank=True)
    native_asset_name = models.TextField(
        choices=NATIVE_ASSETS_NAME,
        null=True, blank=True)
    min_text_length = models.IntegerField(null=True, blank=True)
    max_text_length = models.IntegerField(null=True, blank=True)
    requirement = models.TextField(
        choices=MEDIA_REQUIRENMENT,
        null=True, blank=True)

    class Meta:
        db_table = "media_sub_type_native_assets"


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
    reselling_exposed_on = models.DateTimeField()
    reselling_name = models.TextField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    is_rtb = models.NullBooleanField(null=True, blank=True)
    timezone = models.TextField(null=True, blank=True) #originally it is enum
    last_modified = models.DateTimeField()
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
    ym_profile_id = models.IntegerField(null=True, blank=True, db_index=True) #TODO FK is needed in future
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


CONTENT_CATEGORY_TYPE = (
    ('standard', 'standard'),
    ('standard', 'standard')
)


class ContentCategory(models.Model):
    name = models.TextField(null=True, blank=True, db_index=True)
    description = models.TextField(null=True, blank=True)
    is_system = models.NullBooleanField(null=True, blank=True)
    parent_category = models.ForeignKey("ContentCategory", null=True, blank=True)
    type = models.TextField(
        choices=CONTENT_CATEGORY_TYPE,
        null=True, blank=True)
    last_modified = models.DateTimeField()

    class Meta:
        db_table = "content_category"


PLACEMENT_POSITION = (
    ('above', 'above the fold'),
    ('below', 'below the fold'),
    ('unknown', 'unknown')
)


PIXEL_TYPE = (
    ('javascript', 'javascript'),
    ('image', 'image')
)


AUDIT_LEVEL = (
    ('site', 'site'),
    ('placement', 'placement')
)


INTENDED_AUDIENCE = (
    ('general', 'general'),
    ('children', 'children'),
    ('young_adult', 'young_adult'),
    ('mature', 'mature'),

)


DEFAULT_CALCULATION_TYPE = (
    ('gross', 'gross'),
    ('net', 'net')
)


FLOOR_APPLICATION_TARGET = (
    ('external_only', 'external_only'),
    ('external_non_preferred', 'external_non_preferred'),
    ('all', 'all')
)


SITE_AUDIT_STATUS = (
    ('self', 'self'),
    ('unaudited', 'unaudited')
)


class Placement(models.Model):
    name = models.TextField(null=True, blank=True, db_index=True)
    code = models.TextField(null=True, blank=True, db_index=True)
    code2 = models.TextField(null=True, blank=True, db_index=True)
    code3 = models.TextField(null=True, blank=True, db_index=True)
    state = models.TextField(
        choices=STATE_CHOICES,
        null=True, blank=True)
    width = models.IntegerField(null=True, blank=True, db_index=True)
    height = models.IntegerField(null=True, blank=True, db_index=True)
    is_resizable = models.NullBooleanField(null=True, blank=True)
    default_position = models.TextField(
        choices=PLACEMENT_POSITION,
        null=True, blank=True)
    publisher_id = models.ForeignKey("Publisher", null=True, blank=True)
    site_id = models.IntegerField(null=True, blank=True, db_index=True) #TODO FK is needed in future
    inventory_source_id = models.IntegerField(null=True, blank=True, db_index=True) #TODO FK is needed in future
    ad_profile_id = models.IntegerField(null=True, blank=True, db_index=True) #TODO FK is needed in future
    #supported_media_types = array - see model PlacementMediaType below
    #supported_media_subtypes = array - see model PlacementMediaSubType below
    #pop_values = array - see model PlacementPopValues
    default_creative_id = models.IntegerField(null=True, blank=True, db_index=True) #TODO FK is needed in future
    reserve_price = models.FloatField(null=True, blank=True)
    hide_referer = models.NullBooleanField(null=True, blank=True)
    default_referrer_url = models.TextField(null=True, blank=True)
    visibility_profile_id = models.IntegerField(null=True, blank=True, db_index=True) #TODO FK is needed in future
    exclusive = models.NullBooleanField(null=True, blank=True)
    pixel_url = models.TextField(null=True, blank=True)
    pixel_type = models.TextField(
        choices=PIXEL_TYPE,
        null=True, blank=True)
    #content_categories = array -  see model PlacementContentCategory below
    #filtered_advertisers = array - see model FilteredAdvertisers below
    #filtered_line_items = array - see model FilteredLineItems below
    #filtered_campaigns = array - see model FilteredCampaigns
    #segments = array - see model AllowedSegments below
    #estimated_clear_prices = array - see model PlacementEstimatedClearPrices below
    intended_audience = models.TextField(
        choices=INTENDED_AUDIENCE,
        null=True, blank=True)
    #inventory_attributes = array - see model PlacementInventoryAttributes
    audited = models.NullBooleanField(null=True, blank=True)
    audit_level = models.TextField(
        choices=AUDIT_LEVEL,
        null=True, blank=True)
    default_calculation_type = models.TextField(
        choices=DEFAULT_CALCULATION_TYPE,
        null=True, blank=True)
    apply_floor_to_direct = models.NullBooleanField(null=True, blank=True)
    demand_filter_action = models.TextField(null=True, blank=True)
    floor_application_target = models.TextField(
        choices=FLOOR_APPLICATION_TARGET,
        null=True, blank=True)
    pixel_url_secure = models.TextField(null=True, blank=True)
    site_audit_status = models.TextField(
        choices=SITE_AUDIT_STATUS,
        null=True, blank=True)
    toolbar = object
    acb_code = models.TextField(null=True, blank=True)
    tag_data = models.TextField(null=True, blank=True)
    cost_cpm = models.FloatField(null=True, blank=True)
    is_prohibited = models.NullBooleanField(null=True, blank=True)
    last_modified = models.DateTimeField(null=True, blank=True)
    stats = object
    content_retrieval_timeout_ms = models.IntegerField(null=True, blank=True)
    enable_for_mediation = models.NullBooleanField(null=True, blank=True)
    #private_sizes = array - see model PlacementPrivateSizes below
    video = object
    ad_types = models.TextField(null=True, blank=True) #TODO it is an array in origin but there is no description of it so we need to look at the API responce
    use_detected_domain = bool

    class Meta:
        db_table = "placement"


class PlacementContentCategory(models.Model):
    placement = models.ForeignKey("Placement", null=True, blank=True)
    content_category = models.ForeignKey("ContentCategory", null=True, blank=True)

    class Meta:
        db_table = "placement_content_category"


class PlacementPrivateSizes(models.Model):
    placement = models.ForeignKey("Placement", null=True, blank=True)
    width = models.IntegerField(null=True, blank=True)
    height = models.IntegerField(null=True, blank=True)

    class Meta:
        db_table = "placement_private_sizes"


class FilteredAdvertisers(models.Model):
    placement = models.ForeignKey("Placement", null=True, blank=True)
    advertiser = models.ForeignKey("Advertiser", null=True, blank=True)

    class Meta:
        db_table = "filtered_advertisers"


class FilteredLineItems(models.Model):
    placement = models.ForeignKey("Placement", null=True, blank=True)
    line_item = models.IntegerField(null=True, blank=True, db_index=True) #TODO FK is needed in future

    class Meta:
        db_table = "filtered_line_items"


class FilteredCampaigns(models.Model):
    placement = models.ForeignKey("Placement", null=True, blank=True)
    campaign = models.IntegerField(null=True, blank=True, db_index=True) #TODO FK is needed in future

    class Meta:
        db_table = "filtered_campaigns"


class Segment(models.Model):
    code = models.TextField(null=True, blank=True, db_index=True)
    state = models.TextField(
        choices=STATE_CHOICES,
        null=True, blank=True)
    short_name = models.TextField(null=True, blank=True, db_index=True)
    description = models.TextField(null=True, blank=True)
    member_id = models.IntegerField(null=True, blank=True, db_index=True) #TODO FK is needed in future
    price = models.FloatField(null=True, blank=True)
    expire_minutes = models.IntegerField(null=True, blank=True)
    enable_rm_piggyback = models.NullBooleanField(null=True, blank=True)
    max_usersync_pixels = models.IntegerField(null=True, blank=True)
    last_modified = models.DateTimeField()
    provider = models.TextField(null=True, blank=True)
    advertiser_id = models.ForeignKey("Advertiser", null=True, blank=True)
    #piggyback_pixels - see model PiggybackPixels below
    parent_segment_id = models.ForeignKey("Segment", null=True, blank=True)
    querystring_mapping = models.TextField(null=True, blank=True) #TODO JSON
    querystring_mapping_key_value = models.TextField(null=True, blank=True) #TODO JSON

    class Meta:
        db_table = "segment"


PYGGYBACK_PIXEL_TYPE = (
    ('js', 'js'),
    ('img', 'img')
)


class SegmentPiggybackPixels(models.Model):
    segment = models.ForeignKey("Segment", null=True, blank=True)
    url = models.TextField(null=True, blank=True)
    pixel_type = models.TextField(
        choices=PYGGYBACK_PIXEL_TYPE,
        null=True, blank=True)

    class Meta:
        db_table = "segment_piggyback_pixels"


class AllowedSegments(models.Model):
    placement = models.ForeignKey("Placement", null=True, blank=True)
    segment = models.IntegerField(null=True, blank=True, db_index=True) #TODO FK is needed in future

    class Meta:
        db_table = "allowed_segments"


class PlacementEstimatedClearPrices(models.Model):
    placement = models.ForeignKey("Placement", null=True, blank=True)
    clear_price = models.IntegerField(null=True, blank=True)
    average_price = models.IntegerField(null=True, blank=True)
    width = models.FloatField(null=True, blank=True)
    height = models.IntegerField(null=True, blank=True)
    verified = models.NullBooleanField(null=True, blank=True)

    class Meta:
        db_table = "placement_estimated_clear_prices"


class InventoryAttribute(models.Model):
    name = models.TextField(null=True, blank=True)
    last_activity = models.DateTimeField()

    class Meta:
        db_table = "inventory_attribute"


class PlacementInventoryAttributes(models.Model):
    placement = models.ForeignKey("Placement", null=True, blank=True)
    inventory_attribute = models.ForeignKey("InventoryAttribute", null=True, blank=True)

    class Meta:
        db_table = "placement_inventory_attributes"


class PlacementMediaType(models.Model):
    placement = models.ForeignKey("Placement", null=True, blank=True)
    media_type = models.ForeignKey("MediaType", null=True, blank=True)
    last_modified = models.DateTimeField()

    class Meta:
        db_table = "placement_media_type"


class PlacementPopValues(models.Model):
    placement = models.ForeignKey("Placement", null=True, blank=True)
    pop_freq_times = models.IntegerField(null=True, blank=True)
    pop_freq_duration = models.IntegerField(null=True, blank=True)
    pop_is_prepop = models.NullBooleanField(null=True, blank=True)
    pop_max_width = models.IntegerField(null=True, blank=True)
    pop_max_height = models.IntegerField(null=True, blank=True)

    class Meta:
        db_table = "placement_pop_values"


class PlacementMediaSubType(models.Model):
    placement = models.ForeignKey("Placement", null=True, blank=True)
    media_sub_type = models.ForeignKey("MediaSubType", null=True, blank=True)
    is_private = models.NullBooleanField(null=True, blank=True)
    last_modified = models.DateTimeField()

    class Meta:
        db_table = "placement_media_sub_type"


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
    media_type = models.ForeignKey("MediaType", null=True, blank=True)

    class Meta:
        db_table = "network_analytics_report"
        index_together = ["advertiser_id", "hour"]
        index_together = ["publisher_id", "hour"]
        index_together = ["campaign_id", "hour"]


SUPPLY_TYPE = (
    ('web', 'web'),
    ('mobile_app', 'mobile_app'),
    ('mobile_web', 'mobile_web')
)


GENDER = (
    ('m', 'm'),
    ('f', 'f'),
    ('u', 'u')
)


TRIGGER_TYPE_CHOICES = (
    ('view', 'view'),
    ('click', 'click'),
    ('hybrid', 'hybrid')
)


class ConversionPixel(models.Model):
    code = models.TextField(null=True, blank=True, db_index=True)
    name = models.TextField(null=True, blank=True, db_index=True)
    state = models.TextField(
        choices=STATE_CHOICES,
        null=True, blank=True)
    #campaigns - see model CampaignConversionPixel below
    #line_items - see model LineItemConversionPixel below
    trigger_type = models.TextField(
        choices=TRIGGER_TYPE_CHOICES,
        null=True, blank=True)
    min_minutes_per_conv = models.IntegerField(null=True, blank=True)
    post_view_expire_mins = models.IntegerField(null=True, blank=True)
    post_click_expire_mins = models.IntegerField(null=True, blank=True)
    post_click_value = models.FloatField(null=True, blank=True)
    post_view_value = models.FloatField(null=True, blank=True)
    #piggyback_pixels - see model ConversionPixelPiggybackPixels below
    created_on = models.DateTimeField()
    last_modified = models.DateTimeField()
    advertiser = models.ForeignKey("Advertiser", null=True, blank=True)

    class Meta:
        db_table = "conversion_pixel"


class LineItemConversionPixel(models.Model):
    conversion_pixel = models.ForeignKey("ConversionPixel", null=True, blank=True)
    line_item = models.IntegerField(null=True, blank=True, db_index=True) #TODO FK is needed in future

    class Meta:
        db_table = "line_item_conversion_pixel"


class CampaignConversionPixel(models.Model):
    conversion_pixel = models.ForeignKey("ConversionPixel", null=True, blank=True)
    campaign = models.IntegerField(null=True, blank=True, db_index=True) #TODO FK is needed in future

    class Meta:
        db_table = "campaign_conversion_pixel"


class ConversionPixelPiggybackPixels(models.Model):
    segment = models.ForeignKey("ConversionPixel", null=True, blank=True)
    url = models.TextField(null=True, blank=True)
    pixel_type = models.TextField(
        choices=PYGGYBACK_PIXEL_TYPE,
        null=True, blank=True)

    class Meta:
        db_table = "conversion_pixel_piggyback_pixels"


AGE_BUCKET_CHOISE = (
    ('0', 'unknown'),
    ('1', '13-17'),
    ('2', '18-24'),
    ('3', '25-34'),
    ('4', '35-44'),
    ('5', '45-54'),
    ('6', '55-64'),
    ('7', '65+')
)


FOLD_POSITION_CHOISE = (
    ('0', 'unknown'),
    ('1', 'above'),
    ('2', 'below'),
    ('11', 'Top FB Ad Slot'),
    ('12', '2nd FB Ad Slot'),
    ('13', '3nd FB Ad Slot'),
    ('14', '4nd FB Ad Slot'),
    ('15', '5nd FB Ad Slot'),
    ('16', '6nd FB Ad Slot'),
    ('17', '7nd FB Ad Slot'),
    ('18', '8nd FB Ad Slot'),
    ('19', '9nd FB Ad Slot'),
    ('20', '10nd FB Ad Slot')
)


PLATFORM_TYPE_CHOICE = (
    ('web', 'web'),
    ('mobile', 'mobile'),
    ('both', 'both')
)


class OSFamily(models.Model):
    name = models.TextField(null=True, blank=True, db_index=True)
    last_modified = models.DateTimeField()

    class Meta:
        db_table = "os_family"


class OperatingSystem(models.Model):
    name = models.TextField(null=True, blank=True, db_index=True)
    platform_type = models.TextField(
        choices=PLATFORM_TYPE_CHOICE,
        null=True, blank=True)
    os_family = models.ForeignKey("OSFamily", null=True, blank=True)
    last_modified = models.DateTimeField()

    class Meta:
        db_table = "operating_system"


INVENTORY_TYPE_COICES = (
    ('real_time', 'real_time'),
    ('direct', 'direct'),
    ('both', 'both')
)


READLOCK_TYPE_COICES = (
    ('normal_roadblock', 'normal_roadblock'),
    ('partial_roadblock', 'partial_roadblock'),
    ('exact_roadblock', 'exact_roadblock')
)


CREATIVE_DISTRIBUTUIN_TYPE_COICES = (
    ('even', 'even'),
    ('weighted', 'weighted'),
    ('ctr-optimized', 'ctr-optimized')
)


class Campaign(models.Model):
    state = models.TextField(
        choices=STATE_CHOICES,
        null=True, blank=True)
    parent_inactive = models.NullBooleanField(null=True, blank=True)
    code = models.TextField(null=True, blank=True, db_index=True)
    name = models.TextField(null=True, blank=True, db_index=True)
    short_name = models.TextField(null=True, blank=True, db_index=True)
    advertiser = models.ForeignKey("Advertiser", null=True, blank=True)
    profile_id = models.IntegerField(null=True, blank=True, db_index=True) #TODO FK is needed in future
    line_item_id = models.IntegerField(null=True, blank=True, db_index=True) #TODO FK is needed in future
    start_date = models.DateTimeField(db_index=True)
    end_date = models.DateTimeField(db_index=True)
    #creatives - see model CampaignCreatives below
    #creative_groups - se model CampaignLineItems below
    timezone = models.TextField(null=True, blank=True)
    last_modified = models.DateTimeField()
    supply_type = models.TextField(null=True, blank=True)
    supply_type_action = models.TextField(null=True, blank=True)
    inventory_type = models.TextField(
        choices=INVENTORY_TYPE_COICES,
        null=True, blank=True)
    roadblock_creatives = models.NullBooleanField(null=True, blank=True)
    roadblock_type = models.TextField(
        choices=READLOCK_TYPE_COICES,
        null=True, blank=True)
    #stats - will create another model in it will be needed
    #all_stats - will create another model in it will be needed
    comments = models.TextField(null=True, blank=True)
    #labels - see model CampaignLabel below
    #broker_fees - see CampaignBrokerFees below
    click_url = models.TextField(null=True, blank=True)
    valuation_min_margin_rtb_pct = models.DecimalField(max_digits=35, decimal_places=10)
    remaining_days_eap_multiplier = models.DecimalField(max_digits=35, decimal_places=10)
    first_run = models.DateTimeField()
    last_run = models.DateTimeField()
    alerts = models.TextField(null=True, blank=True)
    creative_distribution_type = models.TextField(
        choices=CREATIVE_DISTRIBUTUIN_TYPE_COICES,
        null=True, blank=True)
    weight = models.IntegerField(null=True, blank=True)


    class Meta:
        db_table = "campaign"


PAYMENT_TYPE_CHOICES = (
    ('cpm', 'cpm'),
    ('revshare', 'revshare')
)


class CampaignBrokerFees(models.Model):
    campaign = models.ForeignKey("Campaign", null=True, blank=True)
    broker_id = models.IntegerField(null=True, blank=True, db_index=True) #TODO FK is needed in future
    payment_type = models.TextField(
        choices=PAYMENT_TYPE_CHOICES,
        null=True, blank=True)
    value = models.FloatField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)

    class Meta:
        db_table = "campaign_brocker_fees"


class CampaignLabel(models.Model):
    label = models.ForeignKey("Label", null=True, blank=True) #id in origin
    campaign = models.ForeignKey("Campaign", null=True, blank=True)

    class Meta:
        db_table = "campaign_label"


class CampaignCreatives(models.Model):
    campaign = models.ForeignKey("Campaign", null=True, blank=True)
    creative = models.IntegerField(null=True, blank=True, db_index=True) #TODO FK is needed in future

    class Meta:
        db_table = "campaign_creatives"


class CampaignLineItems(models.Model):
    campaign = models.ForeignKey("Campaign", null=True, blank=True)
    line_item = models.IntegerField(null=True, blank=True, db_index=True) #TODO FK is needed in future

    class Meta:
        db_table = "campaign_line_items"


class SiteDomainPerformanceReport(models.Model):
    #https://wiki.appnexus.com/display/api/Site+Domain+Performance
    day = models.DateTimeField(null=True, blank=True, db_index=True)
    site_domain = models.TextField(null=True, blank=True, db_index=True)
    campaign = models.IntegerField(null=True, blank=True, db_index=True) #TODO FK is needed in future
    line_item_id = models.IntegerField(null=True, blank=True, db_index=True) #TODO FK is needed in future
    top_level_category = models.ForeignKey("ContentCategory", related_name='top_level_category_id', null=True, blank=True)
    second_level_category = models.ForeignKey("ContentCategory", related_name='second_level_category_id', null=True, blank=True)
    deal_id = models.IntegerField(null=True, blank=True, db_index=True) #TODO FK is needed in future
    advertiser = models.ForeignKey("Advertiser", null=True, blank=True)
    #campaign_group = campaign_group is a synonymous with line_item .
    buyer_member_id = models.IntegerField(null=True, blank=True, db_index=True) #TODO FK is needed in future
    operating_system = models.ForeignKey("OperatingSystem", null=True, blank=True)
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
    conversion_pixel = models.ForeignKey("ConversionPixel", null=True, blank=True)
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
        db_table = "site_domain_performance_report"
    #This function transform raw data, collected from csv, to value, saved into DB/
    def TransformFields(self):
        pass
