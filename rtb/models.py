import datetime, re


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
    id = models.IntegerField(primary_key=True) #This prevent making automatic AutoIncrement field
    fetch_date = models.DateTimeField(null=True, blank=True, db_index=True)
    code = models.TextField(null=True, blank=True, db_index=True)
    name = models.TextField(null=True, blank=True, db_index=True)
    state = models.TextField(
        choices=STATE_CHOICES,
        null=True, blank=True)
    remarketing_segment_id = models.IntegerField(null=True, blank=True, db_index=True)
    lifetime_budget = models.FloatField(null=True, blank=True)
    lifetime_budget_imps = models.IntegerField(null=True, blank=True)
    daily_budget = models.FloatField(null=True, blank=True)
    daily_budget_imps = models.IntegerField(null=True, blank=True)
    #competitive_brands #see model AdvertiserBrands below
    #competitive_categories	#see model AdvertiserCategories below
    enable_pacing = models.NullBooleanField(null=True, blank=True)
    allow_safety_pacing = models.NullBooleanField(null=True, blank=True)
    # profile = models.ForeignKey("Profile", null=True, blank=True) Temporary changed
    profile_id = models.IntegerField(null=True, blank=True, db_index=True)
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
    #default_brand = models.ForeignKey("Brand", null=True, blank=True) #default_brand in origin API response
    default_brand_id = models.IntegerField(null=True, blank=True, db_index=True) # Temporary
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
    advertiser = models.ForeignKey("Advertiser", null=True, blank=True)
    insertion_order = models.ForeignKey("InsertionOrder", null=True, blank=True)
    line_item = models.ForeignKey("LineItem", null=True, blank=True)
    campaign = models.ForeignKey("Campaign", null=True, blank=True)
    publisher = models.ForeignKey("Publisher", null=True, blank=True)
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
    pitbull_segment_id = models.IntegerField(null=True, blank=True, db_index=True) #TODO FK is needed in future
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


CREATIVE_TYPE_CHOICES = (
    ('standard', 'standard'),
    ('html', 'html'),
    ('video', 'video')
)


CLICK_TEST_RESULT_COICES = (
    ('not_tested', 'not_tested'),
    ('passed', 'passed'),
    ('failed', 'failed')
)


SSL_STATUS_CHOICES = (
    ('disabled', 'disabled'),
    ('pending', 'pending'),
    ('approved', 'approved'),
    ('failed', 'failed')
)


GOOGLE_AUDIT_STATUS_CHOICES = (
    ('approved', 'approved'),
    ('rejected', 'rejected'),
    ('pending', 'pending')
)


MSFT_AUDIT_STATUS_CHOICES = (
    ('approved', 'approved'),
    ('rejected', 'rejected'),
    ('pending', 'pending')
)


FACEBOOK_AUDIT_STATUS_CHOICES = (
    ('pending_pre_audit', 'pending_pre_audit'),
    ('rejected_by_pre_audit', 'rejected_by_pre_audit'),
    ('approved', 'approved'),
    ('rejected', 'rejected'),
    ('pending', 'pending')
)


CREATIVE_UPLOAD_STATUS_CHOICES = (
    ('pending', 'pending'),
    ('processing', 'processing'),
    ('completed', 'completed'),
    ('failed', 'failed')
)


CREATIVE_BACKUP_UPLOAD_STATUS_CHOICES = (
    ('pending', 'pending'),
    ('processing', 'processing'),
    ('completed', 'completed'),
    ('failed', 'failed')
)


CLICK_ACTION_CHOICES = (
    ('click-to-web', 'click-to-web'),
    ('click-to-web', 'click-to-web')
)


class Creative(models.Model):
    #https://wiki.appnexus.com/display/api/Creative+Service
    id = models.IntegerField(primary_key=True)  # No AutoIncrement
    code = models.TextField(null=True, blank=True, db_index=True)
    code2 = models.TextField(null=True, blank=True, db_index=True)
    name = models.TextField(null=True, blank=True, db_index=True)
    type = models.TextField(
        choices=CREATIVE_TYPE_CHOICES,
        null=True, blank=True)
    advertiser_id = models.ForeignKey("Advertiser", null=True, blank=True)
    publisher_id = models.ForeignKey("Publisher", null=True, blank=True)
    brand_id = models.ForeignKey("Brand", null=True, blank=True)
    state = models.TextField(
        choices=STATE_CHOICES,
        null=True, blank=True)
    click_track_result = models.TextField(
        choices=CLICK_TEST_RESULT_COICES,
        null=True, blank=True)
    #campaigns = array - see model CampaignCreative
    template = models.ForeignKey("CteativeTemplate", null=True, blank=True)
    thirdparty_page = object
    custom_macros = models.TextField(
        choices=CLICK_TEST_RESULT_COICES,
        null=True, blank=True)
    width = models.IntegerField(null=True, blank=True)
    height = models.IntegerField(null=True, blank=True)
    media_url = models.TextField(null=True, blank=True)
    media_url_secure = models.TextField(null=True, blank=True)
    click_url = models.TextField(null=True, blank=True)
    file_name = models.TextField(null=True, blank=True)
    flash_click_variable = models.TextField(null=True, blank=True)
    content = models.TextField(null=True, blank=True)
    content_secure = models.TextField(null=True, blank=True)
    original_content = models.TextField(null=True, blank=True)
    original_content_secure = models.TextField(null=True, blank=True)
    macros = models.TextField(null=True, blank=True)
    audit_status = models.TextField(null=True, blank=True) #array of object in origin. Later we can create separate model for it if needed
    audit_feedback = models.TextField(null=True, blank=True)
    allow_audit = models.NullBooleanField(null=True, blank=True)
    ssl_status = models.TextField(
        choices=SSL_STATUS_CHOICES,
        null=True, blank=True)
    allow_ssl_audit = models.NullBooleanField(null=True, blank=True)
    google_audit_status = models.TextField(
        choices=GOOGLE_AUDIT_STATUS_CHOICES,
        null=True, blank=True)
    google_audit_feedback = models.TextField(null=True, blank=True)
    msft_audit_status = models.TextField(
        choices=MSFT_AUDIT_STATUS_CHOICES,
        null=True, blank=True)
    msft_audit_feedback = models.TextField(null=True, blank=True)
    facebook_audit_status = models.TextField(
        choices=FACEBOOK_AUDIT_STATUS_CHOICES,
        null=True, blank=True)
    facebook_audit_feedback = models.TextField(null=True, blank=True)
    is_self_audited = models.NullBooleanField(null=True, blank=True)
    is_expired = models.NullBooleanField(null=True, blank=True)
    is_prohibited = models.NullBooleanField(null=True, blank=True)
    is_hosted = models.NullBooleanField(null=True, blank=True)
    lifetime_budget = models.FloatField(null=True, blank=True)
    lifetime_budget_imps = models.IntegerField(null=True, blank=True)
    daily_budget = models.FloatField(null=True, blank=True)
    daily_budget_imps = models.IntegerField(null=True, blank=True)
    enable_pacing = models.NullBooleanField(null=True, blank=True)
    allow_safety_pacing = models.NullBooleanField(null=True, blank=True)
    profile_id = models.ForeignKey("Profile", null=True, blank=True)
    folder = models.ForeignKey("CreativeFolder", null=True, blank=True)
    #line_items = array - see model LineItemCreatives
    #pixels = array - see model CreativePixel below
    track_clicks = models.NullBooleanField(null=True, blank=True)
    flash_backup_content = models.TextField(null=True, blank=True)
    flash_backup_file_name = models.TextField(null=True, blank=True)
    flash_backup_url = models.TextField(null=True, blank=True)
    is_control = models.NullBooleanField(null=True, blank=True)
    #segments = array - see model CreativeSegment below
    created_on = models.DateTimeField()
    last_modified = models.DateTimeField()
    creative_upload_status = models.TextField(
        choices=CREATIVE_UPLOAD_STATUS_CHOICES,
        null=True, blank=True)
    backup_upload_status = models.TextField(
        choices=CREATIVE_BACKUP_UPLOAD_STATUS_CHOICES,
        null=True, blank=True)
    use_dynamic_click_url = models.NullBooleanField(null=True, blank=True)
    size_in_bytes = models.IntegerField(null=True, blank=True)
    text_title = models.TextField(null=True, blank=True)
    text_description = models.TextField(null=True, blank=True)
    text_display_url = models.TextField(null=True, blank=True)
    click_action = models.TextField(
        choices=CLICK_ACTION_CHOICES,
        null=True, blank=True)
    click_target = models.TextField(null=True, blank=True)
    #categories = array - see model CreativeCategory below
    #adservers = array - see model CreativeAdserver below
#    technical_attributes = array
#    language = object
#    brand = object
#    pop_values = array
    sla = models.IntegerField(null=True, blank=True)
    sla_eta = models.DateTimeField()
    currency = models.TextField(null=True, blank=True)
    first_run = models.DateTimeField()
    last_run = models.DateTimeField()
#    mobile = object
#    video_attribute = object
#    stats = object
    content_source = models.TextField(null=True, blank=True)
#    custom_request_template = multi - object
#    competitive_brands = array
#    competitive_categories = array
#    thirdparty_pixels = array
#    native = object
#    adx_audit = object
    flash_backup_url_secure = models.TextField(null=True, blank=True)
    member_id = models.IntegerField(null=True, blank=True, db_index=True) #TODO FK is needed in future

    class Meta:
        db_table = "creative"


PIXEL_FORMAT_CHOICES = (
    ('raw-js', 'raw-js'),
    ('url-html', 'url-html'),
    ('url-js', 'url-js'),
    ('url-image', 'url-image'),
    ('raw-url', 'raw-url')
)


CREATIVE_SEGMENT_ACTION_CHOICES = (
    ('add on view', 'add on view'),
    ('add on click', 'add on click')
)


class CreativeAdserver(models.Model):
    id = models.IntegerField(primary_key=True)  # No AutoIncrement
    creative = models.ForeignKey("Creative", null=True, blank=True)
    use_type = models.TextField(null=True, blank=True)
    name = models.TextField(null=True, blank=True)

    class Meta:
        db_table = "creative_adserver"


class CreativeCategory(models.Model):
    creative = models.ForeignKey("Creative", null=True, blank=True)
    category = models.ForeignKey("Category", null=True, blank=True)

    class Meta:
        db_table = "creative_category"


class CreativeSegment(models.Model):
    creative = models.ForeignKey("Creative", null=True, blank=True)
    segment = models.ForeignKey("Segment", null=True, blank=True)
    action = models.TextField(
        choices=CREATIVE_SEGMENT_ACTION_CHOICES,
        null=True, blank=True)

    class Meta:
        db_table = "creative_segment"


class PixelTemplate(models.Model):
    #https://wiki.appnexus.com/display/api/Pixel+Template+Service
    id = models.IntegerField(primary_key=True)  # No AutoIncrement
    name = models.TextField(null=True, blank=True, db_index=True)
    format = models.TextField(
        choices=PIXEL_FORMAT_CHOICES,
        null=True, blank=True)
    content = models.TextField(null=True, blank=True)
    secure_content = models.TextField(null=True, blank=True)
    url = models.TextField(null=True, blank=True)
    secure_url = models.TextField(null=True, blank=True)
    num_required_params = models.IntegerField(null=True, blank=True)
    require_reaudit = models.NullBooleanField(null=True, blank=True)

    class Meta:
        db_table = "pixel_template"


class CreativePixel(models.Model):
    id = models.IntegerField(primary_key=True)  # No AutoIncrement
    creative = models.ForeignKey("Creative", null=True, blank=True)
    pixel_template = models.ForeignKey("PixelTemplate", null=True, blank=True)
    param_1 = models.TextField(null=True, blank=True)
    param_2 = models.TextField(null=True, blank=True)
    param_3 = models.TextField(null=True, blank=True)
    param_4 = models.TextField(null=True, blank=True)
    param_5 = models.TextField(null=True, blank=True)
    format = models.TextField(
        choices=PIXEL_FORMAT_CHOICES,
        null=True, blank=True)
    content = models.TextField(null=True, blank=True)
    secure_content = models.TextField(null=True, blank=True)
    url = models.TextField(null=True, blank=True)
    secure_url = models.TextField(null=True, blank=True)

    class Meta:
        db_table = "creative_pixel"


class CreativeFolder(models.Model):
    #https://wiki.appnexus.com/display/api/Creative+Folder+Service
    name = models.TextField(null=True, blank=True, db_index=True)
    advertiser = models.ForeignKey("Advertiser", null=True, blank=True)
    last_modified = models.DateTimeField()

    class Meta:
        db_table = "creative_folder"


class CteativeTemplate(models.Model):
    #https://wiki.appnexus.com/display/api/Creative+Template+Service
    name = models.TextField(null=True, blank=True, db_index=True)
    description = models.TextField(null=True, blank=True)
    member_id = models.IntegerField(null=True, blank=True, db_index=True) #TODO FK is needed in future
    media_subtype = models.ForeignKey("MediaSubType", null=True, blank=True)
    format = models.ForeignKey("CteativeFormat", null=True, blank=True)
    is_default = models.NullBooleanField(null=True, blank=True)
    is_archived = models.NullBooleanField(null=True, blank=True)
    content_js = models.TextField(null=True, blank=True)
    content_html = models.TextField(null=True, blank=True)
    content_xml = models.TextField(null=True, blank=True)
    callback_content_html = models.TextField(null=True, blank=True)
    macros = models.TextField(null=True, blank=True) #array of object in origin. Later we can create separate model for it if needed
    last_modified = models.DateTimeField()

    class Meta:
        db_table = "creative_template"


class CteativeFormat(models.Model):
    #https://wiki.appnexus.com/display/api/Creative+Format+Service
    name = models.TextField(null=True, blank=True, db_index=True)
    last_modified = models.DateTimeField()

    class Meta:
        db_table = "creative_format"


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
    line_item = models.ForeignKey("LineItem", null=True, blank=True)

    class Meta:
        db_table = "filtered_line_items"


class FilteredCampaigns(models.Model):
    placement = models.ForeignKey("Placement", null=True, blank=True)
    campaign = models.ForeignKey("Campaign", null=True, blank=True)

    class Meta:
        db_table = "filtered_campaigns"


class Segment(models.Model):
    #https://wiki.appnexus.com/display/api/Segment+Service
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
    segment = models.ForeignKey("Segment", null=True, blank=True)

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
    line_item = models.ForeignKey("LineItem", null=True, blank=True)

    class Meta:
        db_table = "line_item_conversion_pixel"


class CampaignConversionPixel(models.Model):
    conversion_pixel = models.ForeignKey("ConversionPixel", null=True, blank=True)
    campaign = models.ForeignKey("Campaign", null=True, blank=True)
    roi_click_goal = models.FloatField(null=True, blank=True)
    roi_view_goal = models.FloatField(null=True, blank=True)
    click_payout = models.FloatField(null=True, blank=True)
    view_payout = models.FloatField(null=True, blank=True)

    class Meta:
        db_table = "campaign_conversion_pixel"


class ConversionPixelPiggybackPixels(models.Model):
    conversion_pixel = models.ForeignKey("ConversionPixel", null=True, blank=True)
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
    id = models.IntegerField(primary_key=True) #No AutoIncrement
    name = models.TextField(null=True, blank=True, db_index=True)
    fetch_date = models.DateTimeField(null=True, blank=True, db_index=True)
    last_modified = models.DateTimeField()

    class Meta:
        db_table = "os_family"


class OperatingSystem(models.Model):
    id = models.IntegerField(primary_key=True) #No AutoIncrement
    fetch_date = models.DateTimeField(null=True, blank=True, db_index=True)
    name = models.TextField(null=True, blank=True, db_index=True)
    platform_type = models.TextField(
        choices=PLATFORM_TYPE_CHOICE,
        null=True, blank=True)
    os_family = models.ForeignKey("OSFamily", null=True, blank=True)
    last_modified = models.DateTimeField()

    class Meta:
        db_table = "operating_system"

class OperatingSystemExtended(models.Model):
    id = models.IntegerField(primary_key=True) #No AutoIncrement
    fetch_date = models.DateTimeField(null=True, blank=True, db_index=True)
    name = models.TextField(null=True, blank=True, db_index=True)
    os_family = models.ForeignKey("OSFamily", null=True, blank=True)
    last_modified = models.DateTimeField()
    search_string = models.TextField(null=True, blank=True)
    
    def TransformFields(self, data, metadata={}):
		self.os_family_id = data["family"]["id"]

    class Meta:
        db_table = "operating_system_extended"


TARGETS_OPERATOR_CHOICE = (
    ('and', 'and'),
    ('or', 'or')
)


TARGETS_ACTION_CHOICE = (
    ('include', 'include'),
    ('exclude', 'exclude')
)


PROFILE_TRUST_LEVEL_CHOICE = (
    ('appnexus', 'appnexus'),
    ('seller', 'seller')
)


SESSION_FREQ_COUNTING_TYPE_CHOICE = (
    ('platform', 'platform'),
    ('publisher', 'publisher')
)


class Profile(models.Model):
    #https://wiki.appnexus.com/display/api/Profile+Service
    id = models.IntegerField(primary_key=True) #No AutoIncrement
    fetch_date = models.DateTimeField(null=True, blank=True, db_index=True)
    advertiser = models.ForeignKey("Advertiser", null=True, blank=True)
    code = models.TextField(null=True, blank=True)
    description = models.TextField(null=True, blank=True, db_index=True)
    is_template = models.NullBooleanField(null=True, blank=True)
    last_modified = models.DateTimeField()
    max_lifetime_imps = models.IntegerField(null=True, blank=True)
    min_session_imps = models.IntegerField(null=True, blank=True)
    max_session_imps = models.IntegerField(null=True, blank=True)
    max_day_imps = models.IntegerField(null=True, blank=True)
    min_minutes_per_imp = models.IntegerField(null=True, blank=True)
    max_page_imps = models.IntegerField(null=True, blank=True)

    daypart_timezone = models.TextField(null=True, blank=True)
    daypart_targets = models.TextField(null=True, blank=True) #array of objects in origin TODO it is needed to be concidered if we need a sepparait model here
    segment_targets = models.TextField(null=True, blank=True) #array of objects in origin TODO it is needed to be concidered if we need a sepparait model here
    segment_group_targets = models.TextField(null=True, blank=True) #array of objects in origin TODO it is needed to be concidered if we need a sepparait model here
    segment_boolean_operator = models.TextField(
        choices=TARGETS_OPERATOR_CHOICE,
        null=True, blank=True)
    age_targets = models.TextField(null=True, blank=True) #array of objects in origin TODO it is needed to be concidered if we need a sepparait model here
    gender_targets = models.TextField(null=True, blank=True) #array of objects in origin TODO it is needed to be concidered if we need a sepparait model here
    country_targets = models.TextField(null=True, blank=True) #array of objects in origin TODO it is needed to be concidered if we need a sepparait model here
    country_action = models.TextField(
        choices=TARGETS_ACTION_CHOICE,
        null=True, blank=True)
    region_targets = models.TextField(null=True, blank=True) #array of objects in origin TODO it is needed to be concidered if we need a sepparait model here
    region_action = models.TextField(
        choices=TARGETS_ACTION_CHOICE,
        null=True, blank=True)
    dma_targets = models.TextField(null=True, blank=True) #array of objects in origin TODO it is needed to be concidered if we need a sepparait model here
    dma_action = models.TextField(
        choices=TARGETS_ACTION_CHOICE,
        null=True, blank=True)
    city_targets = models.TextField(null=True, blank=True) #array of objects in origin TODO it is needed to be concidered if we need a sepparait model here
    city_action = models.TextField(
        choices=TARGETS_ACTION_CHOICE,
        null=True, blank=True)
    domain_targets = models.TextField(null=True, blank=True) #array of objects in origin TODO it is needed to be concidered if we need a sepparait model here
    domain_action = models.TextField(
        choices=TARGETS_ACTION_CHOICE,
        null=True, blank=True)
    domain_list_targets = models.TextField(null=True, blank=True) #array of objects in origin TODO it is needed to be concidered if we need a sepparait model here
    domain_list_action = models.TextField(
        choices=TARGETS_ACTION_CHOICE,
        null=True, blank=True)
    platform_placement_targets = models.TextField(null=True, blank=True) #array of objects in origin TODO it is needed to be concidered if we need a sepparait model here
    size_targets = models.TextField(null=True, blank=True) #array of objects in origin TODO it is needed to be concidered if we need a sepparait model here
    seller_member_group_targets = models.TextField(null=True, blank=True) #array of objects in origin TODO it is needed to be concidered if we need a sepparait model here
    member_targets = models.TextField(null=True, blank=True) #array of objects in origin TODO it is needed to be concidered if we need a sepparait model here
    member_default_action = models.TextField(
        choices=TARGETS_ACTION_CHOICE,
        null=True, blank=True)
    video_targets = models.TextField(null=True, blank=True) #array of objects in origin TODO it is needed to be concidered if we need a sepparait model here
    engagement_rate_targets = models.TextField(null=True, blank=True) #array of objects in origin TODO it is needed to be concidered if we need a sepparait model here
    publisher_targets = models.TextField(null=True, blank=True) #array of objects in origin TODO it is needed to be concidered if we need a sepparait model here
    site_targets = models.TextField(null=True, blank=True) #array of objects in origin TODO it is needed to be concidered if we need a sepparait model here
    placement_targets = models.TextField(null=True, blank=True) #array of objects in origin TODO it is needed to be concidered if we need a sepparait model here
    inventory_action = models.TextField(
        choices=TARGETS_ACTION_CHOICE,
        null=True, blank=True)
    content_category_targets = models.TextField(null=True, blank=True) #array of objects in origin TODO it is needed to be concidered if we need a sepparait model here
    deal_targets = models.TextField(null=True, blank=True) #array of objects in origin TODO it is needed to be concidered if we need a sepparait model here
    platform_publisher_targets = models.TextField(null=True, blank=True) #array of objects in origin TODO it is needed to be concidered if we need a sepparait model here
    platform_content_category_targets = models.TextField(null=True, blank=True) #array of objects in origin TODO it is needed to be concidered if we need a sepparait model here
    use_inventory_attribute_targets = models.TextField(null=True, blank=True) #array of objects in origin TODO it is needed to be concidered if we need a sepparait model here
    trust = models.TextField(
        choices=PROFILE_TRUST_LEVEL_CHOICE,
        null=True, blank=True)
    certified_supply = models.NullBooleanField(null=True, blank=True)
    allow_unaudited = models.NullBooleanField(null=True, blank=True)
    session_freq_type = models.TextField(
        choices=SESSION_FREQ_COUNTING_TYPE_CHOICE,
        null=True, blank=True)
    inventory_attribute_targets = models.TextField(null=True, blank=True) #array of objects in origin TODO it is needed to be concidered if we need a sepparait model here
    intended_audience_targets = models.TextField(null=True, blank=True) #array of objects in origin TODO it is needed to be concidered if we need a sepparait model here
    language_targets = models.TextField(null=True, blank=True) #array of objects in origin TODO it is needed to be concidered if we need a sepparait model here
    language_action = models.TextField(
        choices=TARGETS_ACTION_CHOICE,
        null=True, blank=True)
    querystring_targets = models.TextField(null=True, blank=True) #array of objects in origin TODO it is needed to be concidered if we need a sepparait model here
    querystring_action = models.TextField(
        choices=TARGETS_ACTION_CHOICE,
        null=True, blank=True)
    querystring_boolean_operator = models.TextField(
        choices=TARGETS_OPERATOR_CHOICE,
        null=True, blank=True)
    postal_code_targets = models.TextField(null=True, blank=True) #array of objects in origin TODO it is needed to be concidered if we need a sepparait model here
    zip_targets = models.TextField(null=True, blank=True) #array of objects in origin TODO it is needed to be concidered if we need a sepparait model here
    supply_type_targets = models.TextField(null=True, blank=True) #array of objects in origin TODO it is needed to be concidered if we need a sepparait model here
    supply_type_action = models.TextField(
        choices=TARGETS_ACTION_CHOICE,
        null=True, blank=True)
    user_group_targets = models.TextField(null=True, blank=True) #array of objects in origin TODO it is needed to be concidered if we need a sepparait model here
    position_targets = models.TextField(null=True, blank=True) #array of objects in origin TODO it is needed to be concidered if we need a sepparait model here
    browser_targets = models.TextField(null=True, blank=True) #array of objects in origin TODO it is needed to be concidered if we need a sepparait model here
    browser_action = models.TextField(
        choices=TARGETS_ACTION_CHOICE,
        null=True, blank=True)
    location_target_latitude = models.IntegerField(null=True, blank=True)
    location_target_longitude = models.IntegerField(null=True, blank=True)
    location_target_radius = models.IntegerField(null=True, blank=True)
    device_model_targets = models.TextField(null=True, blank=True) #array of objects in origin TODO it is needed to be concidered if we need a sepparait model here
    device_model_action = models.TextField(
        choices=TARGETS_ACTION_CHOICE,
        null=True, blank=True)
    device_type_targets = models.TextField(null=True, blank=True) #array of objects in origin TODO it is needed to be concidered if we need a sepparait model here
    device_type_action = models.TextField(
        choices=TARGETS_ACTION_CHOICE,
        null=True, blank=True)
    carrier_targets = models.TextField(null=True, blank=True) #array of objects in origin TODO it is needed to be concidered if we need a sepparait model here
    carrier_action = models.TextField(
        choices=TARGETS_ACTION_CHOICE,
        null=True, blank=True)
    operating_system_family_targets = models.TextField(null=True, blank=True) #array of objects in origin TODO it is needed to be concidered if we need a sepparait model here
    operating_system_family_action = models.TextField(
        choices=TARGETS_ACTION_CHOICE,
        null=True, blank=True)
    use_operating_system_extended_targeting = models.NullBooleanField(null=True, blank=True)
    operating_system_extended_targets = models.TextField(null=True, blank=True) #array of objects in origin TODO it is needed to be concidered if we need a sepparait model here
    operating_system_action = models.TextField(
        choices=TARGETS_ACTION_CHOICE,
        null=True, blank=True)
    operating_system_targets = models.TextField(null=True, blank=True) #array of objects in origin TODO it is needed to be concidered if we need a sepparait model here
    require_cookie_for_freq_cap = models.NullBooleanField(null=True, blank=True)
    mobile_app_instance_targets = models.TextField(null=True, blank=True) #array of objects in origin TODO it is needed to be concidered if we need a sepparait model here
    mobile_app_instance_action_include = models.NullBooleanField(null=True, blank=True)
    mobile_app_instance_list_targets = models.TextField(null=True, blank=True) #array of objects in origin TODO it is needed to be concidered if we need a sepparait model here
    mobile_app_instance_list_action_include = models.NullBooleanField(null=True, blank=True)
    ip_range_list_targets = models.TextField(null=True, blank=True) #array of objects in origin TODO it is needed to be concidered if we need a sepparait model here
    optimization_zone_action = models.TextField(
        choices=TARGETS_ACTION_CHOICE,
        null=True, blank=True)
    optimization_zone_targets = models.TextField(null=True, blank=True) #array of objects in origin TODO it is needed to be concidered if we need a sepparait model here
    created_on = models.DateTimeField()
    is_expired = models.NullBooleanField(null=True, blank=True)

    class Meta:
        db_table = "profile"


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


CPM_BID_TYPE_COICES = (
    ('base', 'base'),
    ('average', 'average'),
    ('clearing', 'clearing'),
    ('predicted', 'predicted'),
    ('margin', 'margin'),
    ('custom_model', 'custom_model'),
    ('none', 'none')
)


CADENCE_TYPE_COICES = (
    ('advertiser', 'advertiser'),
    ('creative', 'creative')
)


LEARN_OVERRIDE_TYPE_COICES = (
    ('base_cpm_bid', 'base_cpm_bid'),
    ('venue_avg_cpm_bid', 'venue_avg_cpm_bid')
)


class Campaign(models.Model):
    #https://wiki.appnexus.com/display/api/Campaign+Service
    id = models.IntegerField(primary_key=True) # No AutoIncrement
    fetch_date = models.DateTimeField(null=True, blank=True, db_index=True)    
    state = models.TextField(
        choices=STATE_CHOICES,
        null=True, blank=True)
    parent_inactive = models.NullBooleanField(null=True, blank=True)
    code = models.TextField(null=True, blank=True, db_index=True)
    name = models.TextField(null=True, blank=True, db_index=True)
    short_name = models.TextField(null=True, blank=True, db_index=True)
    advertiser = models.ForeignKey("Advertiser", null=True, blank=True)
    profile = models.ForeignKey("Profile", null=True, blank=True)
    line_item = models.ForeignKey("LineItem", null=True, blank=True)
    start_date = models.DateTimeField(db_index=True)
    end_date = models.DateTimeField(db_index=True, null=True, blank=True)
    #creatives - see model CampaignCreative below
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
    valuation_min_margin_rtb_pct = models.DecimalField(max_digits=35, decimal_places=10, null = True)
    remaining_days_eap_multiplier = models.DecimalField(max_digits=35, decimal_places=10, null = True)
    first_run = models.DateTimeField(null=True, blank=True)
    last_run = models.DateTimeField(null=True, blank=True)
    alerts = models.TextField(null=True, blank=True)
    creative_distribution_type = models.TextField(
        choices=CREATIVE_DISTRIBUTUIN_TYPE_COICES,
        null=True, blank=True)
    weight = models.IntegerField(null=True, blank=True)
    lifetime_budget = models.FloatField(null=True, blank=True)
    lifetime_budget_imps = models.IntegerField(null=True, blank=True)
    daily_budget = models.FloatField(null=True, blank=True)
    daily_budget_imps = models.IntegerField(null=True, blank=True)
    learn_budget = models.FloatField(null=True, blank=True)
    learn_budget_imps = models.IntegerField(null=True, blank=True)
    learn_budget_daily_cap = models.FloatField(null=True, blank=True)
    learn_budget_daily_imps = models.IntegerField(null=True, blank=True)
    enable_pacing = models.NullBooleanField(null=True, blank=True)
    lifetime_pacing = models.NullBooleanField(null=True, blank=True)
    lifetime_pacing_span = models.IntegerField(null=True, blank=True)
    priority = models.IntegerField(null=True, blank=True)
    cadence_modifier_enabled = models.NullBooleanField(null=True, blank=True)
    expected_pacing = models.FloatField(null=True, blank=True)
    total_pacing = models.FloatField(null=True, blank=True)
    has_pacing_dollars = models.IntegerField(null=True, blank=True) #enum in origin
    has_pacing_imps = models.IntegerField(null=True, blank=True) #enum in origin
    imps_pacing_percent = models.IntegerField(null=True, blank=True)
    media_cost_pacing_percent = models.IntegerField(null=True, blank=True)

    cpm_bid_type = models.TextField(
        choices=CPM_BID_TYPE_COICES,
        null=True, blank=True)
    base_bid = models.FloatField(null=True, blank=True)
    min_bid = models.FloatField(null=True, blank=True)
    max_bid = models.FloatField(null=True, blank=True)
    bid_margin = models.FloatField(null=True, blank=True)
    cpc_goal = models.FloatField(null=True, blank=True)
    max_learn_bid = models.FloatField(null=True, blank=True)
    #pixels = array  - see model CampaignConversionPixel
    bid_model = models.IntegerField(null=True, blank=True, db_index=True) #TODO FK is needed in future

    learn_threshold = models.IntegerField(null=True, blank=True)
    max_learn_bid = models.FloatField(null=True, blank=True)
    cadence_type = models.TextField(
        choices=CADENCE_TYPE_COICES,
        null=True, blank=True)
    defer_to_li_prediction = models.NullBooleanField(null=True, blank=True)
    optimization_lookback = models.TextField(null=True, blank=True) #TODO JSON
    optimization_version = models.TextField(null=True, blank=True)
    learn_override_type = models.TextField(
        choices=LEARN_OVERRIDE_TYPE_COICES,
        null=True, blank=True)
    base_cpm_bid_value = models.FloatField(null=True, blank=True)
    bid_multiplier = models.FloatField(null=True, blank=True)
    impression_limit = models.IntegerField(null=True, blank=True)
    campaign_modifiers = models.TextField(null=True, blank=True) #TODO JSON
    bid_modifier_model = models.TextField(null=True, blank=True) #TODO JSON

    class Meta:
        db_table = "campaign"


REVENUE_TYPE_CHOICES = (
    ('none', 'none'),
    ('cpm', 'cpm'),
    ('cpc', 'cpc'),
    ('cpa', 'cpa'),
    ('cost_plus_cpm', 'cost_plus_cpm'),
    ('cost_plus_margin', 'cost_plus_margin'),
    ('flat_fee', 'flat_fee')
)


GOAL_TYPE_CHOICES = (
    ('none', 'none'),
    ('cpc', 'cpc'),
    ('cpa', 'cpa'),
    ('ctr', 'ctr')
)


FLAT_FEE_STATUS_CHOICES = (
    ('pending', 'pending'),
    ('processing', 'processing'),
    ('allocated', 'allocated'),
    ('error', 'error')
)


class LineItem(models.Model):
    #https://wiki.appnexus.com/display/api/Line+Item+Service
    id = models.IntegerField(primary_key=True) # No AutoIncrement    
    fetch_date = models.DateTimeField(null=True, blank=True, db_index=True)    
    code = models.TextField(null=True, blank=True, db_index=True)
    name = models.TextField(null=True, blank=True, db_index=True)
    advertiser = models.ForeignKey("Advertiser", null=True, blank=True)
    state = models.TextField(
        choices=STATE_CHOICES,
        null=True, blank=True)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField(null=True, blank = True)
    timezone = models.TextField(null=True, blank=True)
    revenue_value = models.FloatField(null=True, blank=True)
    revenue_type = models.TextField(
        choices=REVENUE_TYPE_CHOICES,
        null=True, blank=True)
    goal_type = models.TextField(
        choices=GOAL_TYPE_CHOICES,
        null=True, blank=True)
    goal_value = models.FloatField(null=True, blank=True)
    last_modified = models.DateTimeField()
    click_url = models.TextField(null=True, blank=True)
    currency = models.TextField(null=True, blank=True)
    require_cookie_for_tracking = models.NullBooleanField(null=True, blank=True)
    profile = models.ForeignKey("Profile", null=True, blank=True)
    member_id = models.IntegerField(null=True, blank=True, db_index=True) #TODO FK is needed in future
    comments = models.TextField(null=True, blank=True)
    remaining_days = models.IntegerField(null=True, blank=True)
    total_days = models.IntegerField(null=True, blank=True)
    manage_creative = models.NullBooleanField(null=True, blank=True)
    flat_fee_status = models.TextField(
        choices=FLAT_FEE_STATUS_CHOICES,
        null=True, blank=True)
    flat_fee_allocation_date = models.DateTimeField(null=True, blank=True)
    flat_fee_adjustment_id = models.IntegerField(null=True, blank=True)
    #labels = array - see model LineItemLabel below
    #broker_fees = array - see model LineItemBroker below
    #pixels = array - see model LineItemConversionPixel
    #insertion_orders = array - see model LineItemInsertionOrder
    #goal_pixels = array - see model LineItemGoalPixel below
    #imptrackers = array - see model ImpressionTracker below
    #clicktrackers = array - see model ClickTracker below
    #campaigns = array - see model Campaign
    valuation_min_margin_pct = models.FloatField(null=True, blank=True)
    valuation_goal_threshold = models.FloatField(null=True, blank=True)
    valuation_goal_target = models.FloatField(null=True, blank=True)
    valuation_performance_offer = models.NullBooleanField(null=True, blank=True)
    valuation_performance_mkt_managed = models.NullBooleanField(null=True, blank=True)
    valuation_performance_mkt_crossnet = models.NullBooleanField(null=True, blank=True)
    #creatives = array - see model LineItemCreatives below
    budget_intervals = models.TextField(null=True, blank=True) #TODO JSON and maybe separate model later
    lifetime_budget = models.FloatField(null=True, blank=True)
    lifetime_budget_imps = models.IntegerField(null=True, blank=True)
    daily_budget = models.FloatField(null=True, blank=True)
    daily_budget_imps = models.FloatField(null=True, blank=True)
    enable_pacing = models.NullBooleanField(null=True, blank=True)
    allow_safety_pacing = models.NullBooleanField(null=True, blank=True)
    lifetime_pacing = models.NullBooleanField(null=True, blank=True)
    lifetime_pacing_span = models.IntegerField(null=True, blank=True)
    lifetime_pacing_pct = models.FloatField(null=True, blank=True)
    payout_margin = models.FloatField(null=True, blank=True)
    insertion_order = models.ForeignKey("InsertionOrder", null=True, blank=True)
    #stats = object - late we'll decide if we need a model for stats
    #all_stats = array - may be we'll need this in separate model in the future
    first_run = models.DateTimeField(null=True, blank=True)
    last_run = models.DateTimeField(null=True, blank=True)
    expected_pacing = models.FloatField(null=True, blank=True)
    total_pacing = models.FloatField(null=True, blank=True)
    has_pacing_dollars = models.IntegerField(null=True, blank=True) #enum in origin
    has_pacing_imps = models.IntegerField(null=True, blank=True) #enum in origin
    imps_pacing_percent = models.IntegerField(null=True, blank=True)
    rev_pacing_percent = models.IntegerField(null=True, blank=True)
    alerts = models.TextField(null=True, blank=True) #TODO JSON
    creative_distribution_type = models.TextField(
        choices=CREATIVE_DISTRIBUTUIN_TYPE_COICES,
        null=True, blank=True)
    weight = models.IntegerField(null=True, blank=True)
    inventory_type = models.TextField(null=True, blank=True) #no description in origin
    priority = models.TextField(null=True, blank=True) #no description in origin

    class Meta:
        db_table = "line_item"


class LineItemCreatives(models.Model):
    line_item = models.ForeignKey("LineItem", null=True, blank=True)
    creative = models.IntegerField(null=True, blank=True, db_index=True) #TODO FK is needed in future
    code = models.TextField(null=True, blank=True, db_index=True)

    class Meta:
        db_table = "line_item_creatives"


class ClickTracker(models.Model):
    #https://wiki.appnexus.com/display/api/Click+Tracker+Service
    member_id = models.IntegerField(null=True, blank=True, db_index=True) #TODO FK is needed in future
    advertiser_id = models.ForeignKey("Advertiser", null=True, blank=True)
    name = models.TextField(null=True, blank=True, db_index=True)
    code = models.TextField(null=True, blank=True, db_index=True)
    state = models.TextField(
        choices=STATE_CHOICES,
        null=True, blank=True)
    click_url = models.TextField(null=True, blank=True, db_index=True)
    publisher = models.ForeignKey("Publisher", null=True, blank=True)
    #tag = array - see model ClickTrackerPlacement below
    payment_rule_id = models.IntegerField(null=True, blank=True, db_index=True) #TODO FK is needed in future
    line_item = models.ForeignKey("LineItem", null=True, blank=True)
    last_modified = models.DateTimeField()

    class Meta:
        db_table = "click_tracker"


class ClickTrackerPlacement(models.Model):
    click_tracker = models.ForeignKey("ClickTracker", null=True, blank=True)
    placement = models.ForeignKey("Placement", null=True, blank=True)

    class Meta:
        db_table = "click_tracker_placement"


class ImpressionTracker(models.Model):
    #https://wiki.appnexus.com/display/api/Impression+Tracker+Service
    member_id = models.IntegerField(null=True, blank=True, db_index=True) #TODO FK is needed in future
    advertiser_id = models.ForeignKey("Advertiser", null=True, blank=True)
    name = models.TextField(null=True, blank=True, db_index=True)
    code = models.TextField(null=True, blank=True, db_index=True)
    state = models.TextField(
        choices=STATE_CHOICES,
        null=True, blank=True)
    publisher = models.ForeignKey("Publisher", null=True, blank=True)
    #tag = array - see model ImpressionTrackerPlacement below
    payment_rule_id = models.IntegerField(null=True, blank=True, db_index=True) #TODO FK is needed in future
    line_item = models.ForeignKey("LineItem", null=True, blank=True)
    last_modified = models.DateTimeField()

    class Meta:
        db_table = "impression_tracker"


class ImpressionTrackerPlacement(models.Model):
    impression_tracker = models.ForeignKey("ImpressionTracker", null=True, blank=True)
    placement = models.ForeignKey("Placement", null=True, blank=True)

    class Meta:
        db_table = "impression_tracker_placement"


class GoalPixel(models.Model):
    code = models.TextField(null=True, blank=True, db_index=True)
    name = models.TextField(null=True, blank=True, db_index=True)
    state = models.TextField(
        choices=STATE_CHOICES,
        null=True, blank=True)
    trigger_type = models.TextField(
        choices=TRIGGER_TYPE_CHOICES,
        null=True, blank=True)
    post_click_goal_target = models.FloatField(null=True, blank=True)
    post_view_goal_target = models.FloatField(null=True, blank=True)
    post_click_goal_threshold = models.FloatField(null=True, blank=True)
    post_view_goal_threshold = models.FloatField(null=True, blank=True)

    class Meta:
        db_table = "goal_pixel"


class LineItemGoalPixel(models.Model):
    pixel = models.ForeignKey("GoalPixel", null=True, blank=True)
    line_item = models.ForeignKey("LineItem", null=True, blank=True)

    class Meta:
        db_table = "line_item_goal_pixel"


class InsertionOrder(models.Model):
    #https://wiki.appnexus.com/display/api/Insertion+Order+Service
    id = models.IntegerField(primary_key=True) # No AutoIncrement
    fetch_date = models.DateTimeField(null=True, blank=True, db_index=True)    
    name = models.TextField(null=True, blank=True, db_index=True)
    code = models.TextField(null=True, blank=True, db_index=True)
    state = models.TextField(
        choices=STATE_CHOICES,
        null=True, blank=True)
    advertiser = models.ForeignKey("Advertiser", null=True, blank=True)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    last_modified = models.DateTimeField()
    timezone = models.FloatField(null=True, blank=True)
    currency = models.FloatField(null=True, blank=True)
    comments = models.FloatField(null=True, blank=True)
    billing_code = models.FloatField(null=True, blank=True)
    #spend_protection_pixels = array - it is in alpha-beta phase on AppNexus
    #labels = array - see model InsertionOrderLabel below
    #broker_fees = array - see model InsertionOrderBrokerFees below
    budget_intervals = models.TextField(null=True, blank=True) #TODO JSON and maybe separate model later
    lifetime_pacing = models.NullBooleanField(null=True, blank=True)
    lifetime_budget = models.FloatField(null=True, blank=True)
    lifetime_budget_imps = models.IntegerField(null=True, blank=True)
    enable_pacing = models.NullBooleanField(null=True, blank=True)
    lifetime_pacing_span = models.IntegerField(null=True, blank=True)
    daily_budget = models.FloatField(null=True, blank=True)
    daily_budget_imps = models.FloatField(null=True, blank=True)
    lifetime_pacing_pct = models.FloatField(null=True, blank=True)
    #stats = object - late we'll decide if we need a model for stats

    class Meta:
        db_table = "insertion_order"


PAYMENT_TYPE_CHOICES = (
    ('cpm', 'cpm'),
    ('revshare', 'revshare')
)


class InsertionOrderBrokerFees(models.Model):
    insertion_order = models.ForeignKey("InsertionOrder", null=True, blank=True)
    broker_id = models.IntegerField(null=True, blank=True, db_index=True) #TODO FK is needed in future
    payment_type = models.TextField(
        choices=PAYMENT_TYPE_CHOICES,
        null=True, blank=True)
    value = models.FloatField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)

    class Meta:
        db_table = "insertion_order_brocker_fees"


class InsertionOrderLabel(models.Model):
    insertion_order = models.ForeignKey("InsertionOrder", null=True, blank=True)
    line_item = models.ForeignKey("LineItem", null=True, blank=True)

    class Meta:
        db_table = "insertion_order_label"


class LineItemInsertionOrder(models.Model):
    insertion_order = models.ForeignKey("InsertionOrder", null=True, blank=True)
    line_item = models.ForeignKey("LineItem", null=True, blank=True)

    class Meta:
        db_table = "line_item_insertion_order"


#class LineItemConversionPixel(models.Model):
#    pixel = models.ForeignKey("ConversionPixel", null=True, blank=True)
#    line_item = models.ForeignKey("LineItem", null=True, blank=True)

#    class Meta:
#        db_table = "line_item_conversion_pixel"


class LineItemLabel(models.Model):
    label = models.ForeignKey("Label", null=True, blank=True) #id in origin
    line_item = models.ForeignKey("LineItem", null=True, blank=True)

    class Meta:
        db_table = "line_item_label"


class LineItemBroker(models.Model):
    broker_id = models.IntegerField(null=True, blank=True, db_index=True) #TODO FK is needed in future
    line_item = models.ForeignKey("LineItem", null=True, blank=True)
    payment_type = models.TextField(
        choices=PAYMENT_TYPE_CHOICES,
        null=True, blank=True)
    value = models.FloatField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)

    class Meta:
        db_table = "line_item_broker"


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


class CampaignCreative(models.Model):
    campaign = models.ForeignKey("Campaign", null=True, blank=True)
    creative = models.ForeignKey("Creative", null=True, blank=True)

    class Meta:
        db_table = "campaign_creative"


class CampaignLineItems(models.Model):
    campaign = models.ForeignKey("Campaign", null=True, blank=True)
    line_item = models.ForeignKey("LineItem", null=True, blank=True)

    class Meta:
        db_table = "campaign_line_items"


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
    placement_id = models.ForeignKey("Placement", null=True, blank=True)
    insertion_order_id = models.ForeignKey("InsertionOrder", null=True, blank=True)
    line_item_id = models.ForeignKey("LineItem", null=True, blank=True)
    campaign_id = models.ForeignKey("Campaign", null=True, blank=True)
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

num_in_p = re.compile(r'\((\d+)\)$')
def get_text_in_parentheses(s):
    return  num_in_p.search(s).group(1)

class SiteDomainPerformanceReport(models.Model):
    #https://wiki.appnexus.com/display/api/Site+Domain+Performance
    fetch_date = models.DateTimeField(null=True, blank=True, db_index=True)
    day = models.DateTimeField(null=True, blank=True, db_index=True)
    site_domain = models.TextField(null=True, blank=True, db_index=True)
    campaign = models.ForeignKey("Campaign", null=True, blank=True)
    line_item = models.ForeignKey("LineItem", null=True, blank=True)
    top_level_category = models.ForeignKey("ContentCategory", related_name='top_level_category_id', null=True, blank=True)
    second_level_category = models.ForeignKey("ContentCategory", related_name='second_level_category_id', null=True, blank=True)
    deal_id = models.IntegerField(null=True, blank=True, db_index=True) #TODO FK is needed in future
    advertiser = models.ForeignKey("Advertiser", null=True, blank=True)
    #campaign_group = campaign_group is a synonymous with line_item .
    buyer_member_id = models.IntegerField(null=True, blank=True, db_index=True) #TODO FK is needed in future
    operating_system = models.ForeignKey("OperatingSystemExtended", null=True, blank=True)
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
    #is_remarketing = models.IntegerField(null=True, blank=True)
    is_remarketing = models.NullBooleanField()
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
    def TransformFields(self, data,  metadata={}):
        if not metadata: return
        campaign_dict = metadata["campaign_dict"]
        missed_campaigns = metadata["missed_campaigns"]
        #self.campaign = None
        text_in_parentheses = get_text_in_parentheses(data["campaign"])
        self.campaign_id = int(text_in_parentheses)
        #self.campaign = campaign_dict.get(self.campaign_id) #This also change self.campaign_id
        if self.campaign_id not in campaign_dict:
            campaign_dict[self.campaign_id] = data["campaign"][:-len(text_in_parentheses)-2]
            missed_campaigns.append(self.campaign_id)
        self.advertiser = None
        self.advertiser_id = metadata.get("advertiser_id")
        #self.line_item_id = get_text_in_parentheses(data["line_item"])
        self.operating_system = None
        self.operating_system_id = get_text_in_parentheses(data["operating_system"])
        if data["top_level_category"]=="--":
            self.top_level_category = None
        if data["second_level_category"]=="--":
            self.second_level_category = None
        #if self.is_remarketing == 'no'
        self.click_thru_pct = self.click_thru_pct.replace('%','')



class API_Campaign(models.Model):
    #https://wiki.appnexus.com/display/api/Campaign+Service
    id = models.IntegerField(primary_key=True) # No AutoIncrement
    fetch_date = models.DateTimeField(null=True, blank=True, db_index=True)    
    code = models.IntegerField(null=True, blank=True)
    advertiser = models.ForeignKey('Advertiser', null=True, blank=True)
    pixel_id = models.IntegerField(null=True, blank=True, db_index=True)
    optimization_version = models.TextField(null=True, blank=True)
    profile_id = models.IntegerField(null=True, blank=True, db_index=True) #foreign field
    lifetime_budget_imps = models.IntegerField(null=True, blank=True) #or float
    inventory_type = models.TextField(null=True, blank=True)
    lifetime_budget = models.DecimalField(null=True, blank=True, max_digits=15, decimal_places=2)
    click_url = models.TextField(null=True, blank=True)
    bid_modifier_model = models.TextField(null=True, blank=True)
    enable_pacing = enable_pacing = models.NullBooleanField(null=True, blank=True)
    allow_safety_pacing = models.NullBooleanField(null=True, blank=True)
    timezone = models.TextField(null=True, blank=True)
    cpc_goal = models.FloatField(null=True, blank=True)    
    optimization_lookback = models.TextField(null=True, blank=True)
    line_item_id = models.IntegerField(null=True, blank=True)
    bid_model = models.TextField(null=True, blank=True)
    
    lifetime_pacing_pct = models.IntegerField(null=True, blank=True)
    campaign_type = models.IntegerField(null=True, blank=True)
    defer_to_li_prediction = models.IntegerField(null=True, blank=True)
    impression_limit = models.IntegerField(null=True, blank=True)
    short_name = models.IntegerField(null=True, blank=True)
    cadence_modifier_enabled = models.IntegerField(null=True, blank=True)
    creative_id = models.IntegerField(null=True, blank=True)
    min_bid = models.IntegerField(null=True, blank=True)
    roadblock_type = models.IntegerField(null=True, blank=True)
    comments = models.IntegerField(null=True, blank=True)
    priority = models.IntegerField(null=True, blank=True)
    roadblock_creatives = models.IntegerField(null=True, blank=True)
    state = models.IntegerField(null=True, blank=True)
    max_learn_bid = models.IntegerField(null=True, blank=True)
    allow_unverified_ecp = models.IntegerField(null=True, blank=True)
    require_cookie_for_tracking = models.IntegerField(null=True, blank=True)
    supply_type = models.IntegerField(null=True, blank=True)
    start_date = models.IntegerField(null=True, blank=True)
    bid_multiplier = models.IntegerField(null=True, blank=True)
    daily_budget_imps = models.IntegerField(null=True, blank=True)
    labels = models.IntegerField(null=True, blank=True)
    base_cpm_bid_value = models.IntegerField(null=True, blank=True)
    end_date = models.IntegerField(null=True, blank=True)
    learn_override_type = models.IntegerField(null=True, blank=True)
    valuation = models.IntegerField(null=True, blank=True)
    cpm_bid_type = models.IntegerField(null=True, blank=True)
    ecp_learn_divisor = models.IntegerField(null=True, blank=True)
    creatives = models.IntegerField(null=True, blank=True)
    last_modified = models.IntegerField(null=True, blank=True)
    campaign_modifiers = models.IntegerField(null=True, blank=True)
    creative_distribution_type = models.IntegerField(null=True, blank=True)
    broker_fees = models.IntegerField(null=True, blank=True)
    lifetime_pacing = models.IntegerField(null=True, blank=True)
    remaining_days = models.IntegerField(null=True, blank=True)
    pixels = models.IntegerField(null=True, blank=True)
    supply_type_action = models.IntegerField(null=True, blank=True)
    name = models.IntegerField(null=True, blank=True)
    daily_budget = models.IntegerField(null=True, blank=True)
    learn_threshold = models.IntegerField(null=True, blank=True)
    base_bid = models.IntegerField(null=True, blank=True)
    bid_margin = models.IntegerField(null=True, blank=True)
    max_bid = models.IntegerField(null=True, blank=True)
    cadence_type = models.IntegerField(null=True, blank=True)
    projected_learn_events = models.IntegerField(null=True, blank=True)
    total_days = models.IntegerField(null=True, blank=True)
    lifetime_pacing_span = models.IntegerField(null=True, blank=True)
    cpc_payout = models.IntegerField(null=True, blank=True)
    class Meta:
        db_table = "api_campaign"
    #This function transform data
    def TransformFields(self, metadata={}):
        if not metadata: return


#table for SiteDomainPerformanceReport. Data extracted from correspondent report
class API_SiteDomainPerformanceReport(models.Model):
    #https://wiki.appnexus.com/display/api/Site+Domain+Performance
    fetch_date = models.DateTimeField(null=True, blank=True, db_index=True)
    advertiser = models.ForeignKey('Advertiser', null=True, blank=True, db_index=True)
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
        #self.advertiser_id = metadata.get("advertiser_id")
