import datetime, re
from pytz import utc
from django.db import models, IntegrityError
from django.utils.timezone import now as now_tz
#from django.contrib.postgres.fields import ArrayField
#from django.contrib.postgres.fields import JSONField
from django.contrib.auth.models import User as DjangoUser

STATE_CHOICES = (
    ('active', 'Active'),
    ('inactive', 'Inactive'),
)


USER_TYPES_CHOICES = (
    ('member', 'member'),
    ('bidder', 'bidder'),
    ('publisher', 'publisher'),
    ('advertiser', 'advertiser'),
    ('member_advertiser', 'member_advertiser'),
    ('member_advertiser', 'member_advertiser'),
    ('member_publisher', 'member_publisher')
)


REPORTING_DECIMAL_TYPE = (
    ('comma', 'comma'),
    ('decimal', 'decimal')
)


DECIMAL_MARK = (
    ('comma', 'comma'),
    ('period', 'period')
)


THOUSAND_SEPARATOR = (
    ('comma', 'comma'),
    ('space', 'space'),
    ('period', 'period')
)


class User(models.Model):
    #https://wiki.appnexus.com/display/api/User+Service
    id = models.BigIntegerField(primary_key=True)  # This prevent making automatic AutoIncrement field
    fetch_date = models.DateTimeField(null=True, blank=True, db_index=True)
    state = models.TextField(
        choices=STATE_CHOICES,
        null=True, blank=True)
    username = models.TextField(null=True, blank=True, db_index=True)
    password = models.TextField(null=True, blank=True)
    email = models.TextField(null=True, blank=True, db_index=True)
    first_name = models.TextField(null=True, blank=True)
    last_name = models.TextField(null=True, blank=True)
    custom_data = models.TextField(null=True, blank=True)
    phone = models.TextField(null=True, blank=True)
    user_type = models.TextField(
        choices=USER_TYPES_CHOICES,
        null=True, blank=True)
    read_only = models.NullBooleanField(null=True, blank=True)
    api_login = models.NullBooleanField(null=True, blank=True)
    entity = models.ForeignKey("Member", null=True, blank=True)
    publisher = models.ForeignKey("Publisher", null=True, blank=True)
    advertiser = models.ForeignKey("Advertiser", null=True, blank=True)
    #advertiser_access = array - see model UserAdvertiserAccess below
    #publisher_access = array - see model UserPubliserAccess below
    reporting_decimal_type = models.TextField(
        choices=REPORTING_DECIMAL_TYPE,
        null=True, blank=True)
    decimal_mark = models.TextField(
        choices=DECIMAL_MARK,
        null=True, blank=True)
    thousand_separator = models.TextField(
        choices=THOUSAND_SEPARATOR,
        null=True, blank=True)
    send_safety_budget_notifications = models.NullBooleanField(null=True, blank=True)
    is_developer = models.NullBooleanField(null=True, blank=True)
    last_modified = models.DateTimeField(default=now_tz)
    def __unicode__(self):
        return "%s (%s %s)"%(self.username, self.first_name, self.last_name)

    api_endpoint = 'user'
    class Meta:
        db_table = "user"

class MembershipUserToAdvertiser(models.Model):
    advertiser = models.ForeignKey('Advertiser', on_delete=models.CASCADE)
    frameworkuser = models.ForeignKey('FrameworkUser', on_delete=models.CASCADE)
    can_write = models.BooleanField(default=False)
    class Meta:
        #auto_created = True #dirty trick
        db_table = "rtb_membershipusertoadvertiser"
        unique_together = (
            ('advertiser', 'frameworkuser')
        )

def get_permissions_for_user(user_id):
    membership_info = MembershipUserToAdvertiser.objects.filter(frameworkuser_id=user_id)
    return [{"name": x.advertiser.name, "can_read": True, "can_write": x.can_write}
            for x in membership_info]


# class FrameworkUser(models.Model):
class FrameworkUser(DjangoUser):
    # user = models.OneToOneField(DjangoUser, on_delete=models.CASCADE, primary_key=True)
    apnexus_user = models.ForeignKey("User", null=True, blank=True)
    advertisers = models.ManyToManyField("Advertiser", through= "MembershipUserToAdvertiser")
    # advertisers = models.ManyToManyField("Advertiser")

    @property
    def name(self):
        if hasattr(self, 'username'):
            return self.username
        return self.user and self.user.username

    @property
    def apnexusname(self):
        return self.apnexus_user and self.apnexus_user.name

    @property
    def permission(self):
        return get_permissions_for_user(self.pk)

    def __unicode__(self):
        return self.name
    class Meta:
        db_table = "framework_user"

class UserPubliserAccess(models.Model):
    publisher = models.ForeignKey("Publisher", null=True, blank=True)
    user = models.ForeignKey("User", null=True, blank=True)

    class Meta:
        db_table = "user_publisher_access"


class UserAdvertiserAccess(models.Model):
    advertiser = models.ForeignKey("Advertiser", null=True, blank=True)
    user = models.ForeignKey("User", null=True, blank=True)

    class Meta:
        db_table = "user_advertiser_access"


class Category(models.Model):
    #https://wiki.appnexus.com/display/api/Category+Service
    id = models.IntegerField(primary_key=True)  # No AutoIncrement
    fetch_date = models.DateTimeField(null=True, blank=True, db_index=True)
    name = models.TextField(null=True, blank=True, db_index=True)
    is_sensitive = models.NullBooleanField(null=True, blank=True)
    requires_whitelist = models.NullBooleanField(null=True, blank=True)
    requires_whitelist_on_external = models.NullBooleanField(null=True, blank=True)
    last_modified = models.DateTimeField(default=now_tz) 
    is_brand_eligible = models.NullBooleanField(null=True, blank=True)
    #countries_and_brands = db.Column(db.String) #array of objects !!! need to look at data returned by API ! it is a mess! See the model BrandInCountry below

    api_endpoint = 'category'
    class Meta:
        db_table = "category"


class Company(models.Model):
    #https://wiki.appnexus.com/display/api/Brand+Company+Service
    id = models.IntegerField(primary_key=True)  # No AutoIncrement
    fetch_date = models.DateTimeField(null=True, blank=True, db_index=True)
    models.IntegerField(primary_key=True)  # No AutoIncrement
    name = models.TextField(null=True, blank=True, db_index=True)
    last_modified = models.DateTimeField(default=now_tz)

    api_endpoint = 'brand-company'
    class Meta:
        db_table = "company"


class Brand(models.Model):
    #https://wiki.appnexus.com/display/api/Brand+Service
    id = models.IntegerField(primary_key=True)  # No AutoIncrement
    fetch_date = models.DateTimeField(null=True, blank=True, db_index=True)
    name = models.TextField(null=True, blank=True, db_index=True)
    urls = models.TextField(null=True, blank=True)#ArrayField(models.TextField(null=True, blank=True), null=True, blank=True)
    is_premium = models.NullBooleanField(null=True, blank=True)
    category = models.ForeignKey("Category", null=True, blank=True)
    company = models.ForeignKey("Company", null=True, blank=True)
    num_creatives = models.IntegerField(null=True, blank=True)
    last_modified = models.DateTimeField(default=now_tz)

    api_endpoint = 'brand'
    class Meta:
        db_table = "brand"


class DemographicArea(models.Model):
    #https://wiki.appnexus.com/display/api/Demographic+Area+Service
    id = models.IntegerField(primary_key=True) # No AutoIncrement
    fetch_date = models.DateTimeField(null=True, blank=True, db_index=True)
    name = models.TextField(null=True, blank=True, db_index=True)

    api_endpoint = 'dma'
    class Meta:
        db_table = "demographic_area"


class Country(models.Model):
    #https://wiki.appnexus.com/display/api/Country+Service
    id = models.IntegerField(primary_key=True) # No AutoIncrement
    fetch_date = models.DateTimeField(null=True, blank=True, db_index=True)
    name = models.TextField(null=True, blank=True, db_index=True)
    code = models.TextField(null=True, blank=True) #enum in origin

    api_endpoint = 'country'
    class Meta:
        db_table = "country"


class Region(models.Model):
    #https://wiki.appnexus.com/display/api/Region+Service
    id = models.IntegerField(primary_key=True) # No AutoIncrement
    fetch_date = models.DateTimeField(null=True, blank=True, db_index=True)
    name = models.TextField(null=True, blank=True, db_index=True)
    code = models.TextField(null=True, blank=True) #enum in origin
    country = models.ForeignKey("Country", null=True, blank=True)

    api_endpoint = 'region'
    class Meta:
        db_table = "region"


class BrandInCountry(models.Model):  # TODO:ManyToManyField
    #See the model Category.countries_and_brands
    brand = models.ForeignKey("Brand", null=True, blank=True)
    #brand_id = models.IntegerField(null=True, blank=True)
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
    profile = models.ForeignKey("Profile", null=True, blank=True, related_name='profile_id')
    control_pct = models.FloatField(null=True, blank=True)
    timezone = models.TextField(null=True, blank=True) #originally it is enum
    last_modified = models.DateTimeField(default=now_tz) 
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
    def __unicode__(self):
        return self.name
    api_endpoint = 'advertiser'
    class Meta:
        db_table = "advertiser"


class AdvertiserBrand(models.Model):
    advertiser = models.ForeignKey("Advertiser", null=True, blank=True)
    brand = models.ForeignKey("Brand", null=True, blank=True)
    #brand_id = models.IntegerField(null=True, blank=True)

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
    member = models.ForeignKey("Member", null=True, blank=True)
    is_user_associated = models.NullBooleanField(null=True, blank=True)
    is_reporting_enabled = models.NullBooleanField(null=True, blank=True)
    object_type = models.TextField(
        choices=LABELED_OBJECT_TYPE,
        null=True, blank=True,
        db_index=True)
    report_field = models.TextField(null=True, blank=True)
    #values # see model LabeledObject model below
    last_modified = models.DateTimeField(default=now_tz) 

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
    id = models.IntegerField(primary_key=True)  # No AutoIncrement
    fetch_date = models.DateTimeField(null=True, blank=True, db_index=True)
    name = models.TextField(null=True, blank=True, db_index=True)
    media_type_group_id = models.IntegerField(null=True, blank=True, db_index=True) #TODO FK is needed in future. It is not clear what is Group yet...
    uses_sizes = models.TextField(
        choices=MEDIA_TYPE_SIZES,
        null=True, blank=True)
    last_modified = models.DateTimeField(default=now_tz)

    api_endpoint = 'media-type'
    class Meta:
        db_table = "media_type"


class MediaSubType(models.Model):
    #https: // wiki.appnexus.com / display / api / Media + Subtype + Service
    id = models.IntegerField(primary_key=True)  # No AutoIncrement
    fetch_date = models.DateTimeField(null=True, blank=True, db_index=True)
    name = models.TextField(null=True, blank=True, db_index=True)
    media_type = models.ForeignKey("MediaType", null=True, blank=True)
    #permitted_sizes - see model MediaSubTypePermittedSizes below
    #native_assets - see model MediaSubTypeNativeAssets below
    last_modified = models.DateTimeField(default=now_tz)

    api_endpoint = 'media-subtype'
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


DEFAILT_MEMBER_STATUS_CHOICES = (
    ('case-by-case', 'case-by-case'),
    ('trusted', 'trusted'),
    ('banned', 'banned')
)


DEFAILT_BRAND_STATUS_CHOICES = (
    ('trusted', 'trusted'),
    ('banned', 'banned')
)


DEFAILT_LANGUAGE_STATUS_CHOICES = (
    ('trusted', 'trusted'),
    ('banned', 'banned')
)


DEFAILT_AD_SERVER_STATUS_CHOICES = (
    ('trusted', 'trusted'),
    ('banned', 'banned')
)


DEFAILT_CATEGORY_STATUS_CHOICES = (
    ('trusted', 'trusted'),
    ('banned', 'banned')
)


DEFAILT_TECHNICAL_ATTRIBUTE_STATUS_CHOICES = (
    ('trusted', 'trusted'),
    ('banned', 'banned')
)


DEFAILT_AUDIT_TYPE_CHOICES = (
    ('platform', 'platform'),
    ('platform_or_self', 'platform_or_self')
)


class AdProfile(models.Model):
    #https://wiki.appnexus.com/display/api/Ad+Profile+Service
    id = models.IntegerField(primary_key=True)
    fetch_date = models.DateTimeField(null=True, blank=True, db_index=True)
    state = models.TextField(
        choices=STATE_CHOICES,
        null=True, blank=True)
    member = models.ForeignKey("Member", null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    default_member_status = models.TextField(
        choices=DEFAILT_MEMBER_STATUS_CHOICES,
        null=True, blank=True)
    default_brand_status = models.TextField(
        choices=DEFAILT_BRAND_STATUS_CHOICES,
        null=True, blank=True)
    default_language_status = models.TextField(
        choices=DEFAILT_LANGUAGE_STATUS_CHOICES,
        null=True, blank=True)
    default_ad_server_status = models.TextField(
        choices=DEFAILT_AD_SERVER_STATUS_CHOICES,
        null=True, blank=True)
    default_category_status = models.TextField(
        choices=DEFAILT_CATEGORY_STATUS_CHOICES,
        null=True, blank=True)
    default_technical_attribute_status = models.TextField(
        choices=DEFAILT_TECHNICAL_ATTRIBUTE_STATUS_CHOICES,
        null=True, blank=True)
    default_audit_type = models.TextField(
        choices=DEFAILT_AUDIT_TYPE_CHOICES,
        null=True, blank=True)
    #members = array - see model AdProfileMember below
    #brands = array - see model AdProfileBrand below
    #creatives = array - see model AdProfileCreative below
    #languages = array - see model AdProfileLanguage below
    #ad_servers = array - see model AdProfileAdServer below
    #categories = array - see model AdProfileCategory below
    #technical_attributes = array - see model AdProfileTechnicalAttribute below
    #frequency_caps = array - see model AdProfileFrequencyCaps below
    total_creative_count = models.IntegerField(null=True, blank=True)
    approved_creative_count = models.IntegerField(null=True, blank=True)
    banned_creative_count = models.IntegerField(null=True, blank=True)
    creatives_approved_percent = models.FloatField(null=True, blank=True)
    creatives_unreviewed = models.IntegerField(null=True, blank=True)
    brands_unreviewed = models.IntegerField(null=True, blank=True)
    exclude_unaudited = models.NullBooleanField(null=True, blank=True)
    exclude_unaudited_direct = models.NullBooleanField(null=True, blank=True)
    audit_type_direct = models.TextField(null=True, blank=True)
    check_attributes_direct = models.NullBooleanField(null=True, blank=True)
    excluded_landing_page_urls = models.TextField(null=True, blank=True) # it is array in origine but it is marked as Not available.
    notes = models.TextField(null=True, blank=True)
    publisher = models.ForeignKey("Publisher", null=True, blank=True)
    last_modified = models.DateTimeField(default=now_tz)

    api_endpoint = 'ad-profile'
    class Meta:
        db_table = "ad_profile"


class AdProfileFrequencyCaps(models.Model):
    ad_profile = models.ForeignKey("AdProfile", null=True, blank=True)
    member = models.ForeignKey("Member", null=True, blank=True)
    max_session_imps = models.IntegerField(null=True, blank=True)
    max_day_imps = models.IntegerField(null=True, blank=True)
    min_minutes_per_imp = models.IntegerField(null=True, blank=True)
    cap_user_without_cookie = models.NullBooleanField(null=True, blank=True)
    #technical_attributes = array - see model AdProfileFrequencyCapsTechnicalAttribute below
    #categories = array - see model AdProfileFrequencyCapsCategory below

    class Meta:
        db_table = "ad_profile_frequency_caps"


class AdProfileMember(models.Model):
    ad_profile = models.ForeignKey("AdProfile", null=True, blank=True)
    member = models.ForeignKey("Member", null=True, blank=True)
    status = models.TextField(
        choices=DEFAILT_MEMBER_STATUS_CHOICES,
        null=True, blank=True)
    audit_type = models.TextField(
        choices=DEFAILT_AUDIT_TYPE_CHOICES,
        null=True, blank=True)
    exclude_unaudited = models.NullBooleanField(null=True, blank=True)

    class Meta:
        db_table = "ad_profile_member"


class AdProfileBrand(models.Model):
    ad_profile = models.ForeignKey("AdProfile", null=True, blank=True)
    brand = models.ForeignKey("Brand", null=True, blank=True)
    #brand_id = models.IntegerField(null=True, blank=True)
    status = models.TextField(
        choices=DEFAILT_BRAND_STATUS_CHOICES,
        null=True, blank=True)

    class Meta:
        db_table = "ad_profile_brand"


class AdProfileCreative(models.Model):
    ad_profile = models.ForeignKey("AdProfile", null=True, blank=True)
    creative = models.ForeignKey("Creative", null=True, blank=True)
    approved = models.NullBooleanField(null=True, blank=True)

    class Meta:
        db_table = "ad_profile_creative"


class AdProfileLanguage(models.Model):
    ad_profile = models.ForeignKey("AdProfile", null=True, blank=True)
    language = models.ForeignKey("Language", null=True, blank=True)
    status = models.TextField(
        choices=DEFAILT_LANGUAGE_STATUS_CHOICES,
        null=True, blank=True)

    class Meta:
        db_table = "ad_profile_language"


class AdServer(models.Model):
    #https://wiki.appnexus.com/display/api/Ad+Server+Service
    id = models.IntegerField(primary_key=True)
    name = models.TextField(null=True, blank=True, db_index=True)
    description = models.TextField(null=True, blank=True)
    declare_to_adx = models.NullBooleanField(null=True, blank=True)
    last_modified = models.DateTimeField(default=now_tz) 
    #hostnames = array - see model AdServerHostname below

    class Meta:
        db_table = "ad_server"


class AdServerHostname(models.Model):
    ad_server = models.ForeignKey("AdServer", null=True, blank=True)
    hostname = models.TextField(null=True, blank=True, db_index=True)

    class Meta:
        db_table = "ad_server_hostname"


class AdProfileAdServer(models.Model):
    ad_profile = models.ForeignKey("AdProfile", null=True, blank=True)
    ad_server = models.ForeignKey("AdServer", null=True, blank=True)
    status = models.TextField(
        choices=DEFAILT_AD_SERVER_STATUS_CHOICES,
        null=True, blank=True)

    class Meta:
        db_table = "ad_profile_ad_server"


class AdProfileCategory(models.Model):
    ad_profile = models.ForeignKey("AdProfile", null=True, blank=True)
    category = models.ForeignKey("Category", null=True, blank=True)
    status = models.TextField(
        choices=DEFAILT_CATEGORY_STATUS_CHOICES,
        null=True, blank=True)

    class Meta:
        db_table = "ad_profile_category"


class TechnicalAttribute(models.Model):
    #https://wiki.appnexus.com/display/api/Technical+Attribute+Service
    id = models.IntegerField(primary_key=True)
    name = models.TextField(null=True, blank=True, db_index=True)
    last_activity = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = "technical_attribute"


class AdProfileTechnicalAttribute(models.Model):
    ad_profile = models.ForeignKey("AdProfile", null=True, blank=True)
    technical_attribute = models.ForeignKey("TechnicalAttribute", null=True, blank=True)
    status = models.TextField(
        choices=DEFAILT_CATEGORY_STATUS_CHOICES,
        null=True, blank=True)

    class Meta:
        db_table = "ad_profile_technical_attribute"


class AdProfileFrequencyCapsTechnicalAttribute(models.Model):
    frequency_caps = models.ForeignKey("AdProfileFrequencyCaps", null=True, blank=True)
    technical_attribute = models.ForeignKey("TechnicalAttribute", null=True, blank=True)

    class Meta:
        db_table = "ad_profile_frequency_caps_technical_attribute"


class AdProfileFrequencyCapsCategory(models.Model):
    frequency_caps = models.ForeignKey("AdProfileFrequencyCaps", null=True, blank=True)
    category = models.ForeignKey("Category", null=True, blank=True)

    class Meta:
        db_table = "ad_profile_frequency_caps_category"


TYPE_OF_INVENTORY_CHOICES = (
    ('managed', 'managed'),
    ('rtb', 'rtb')
)


class OptimizationZone(models.Model):
    #https://wiki.appnexus.com/display/api/Optimization+Zone+Service
    id = models.IntegerField(primary_key=True)
    fetch_date = models.DateTimeField(null=True, blank=True, db_index=True)
    name = models.TextField(null=True, blank=True, db_index=True)
    external_name = models.TextField(null=True, blank=True, db_index=True)
    last_modified = models.DateTimeField(default=now_tz) 
    type = models.TextField(
        choices=TYPE_OF_INVENTORY_CHOICES,
        null=True, blank=True)
    search = models.TextField(null=True, blank=True)
    #sites = array - see model Site below
    #manual_offer_rankings = array - see model ManualOfferRanking below

    api_endpoint = 'optimization-zone'
    class Meta:
        db_table = "optimization_zone"


class ManualOfferRanking(models.Model):
    #https://wiki.appnexus.com/display/api/Manual+Offer+Ranking+Service
    id = models.IntegerField(primary_key=True)
    managed_optimization_zone = models.ForeignKey("OptimizationZone", null=True, blank=True)
    line_item = models.ForeignKey("LineItem", null=True, blank=True)
    country_code = models.TextField(null=True, blank=True, db_index=True)
    creative_height = models.IntegerField(null=True, blank=True)
    creative_width = models.IntegerField(null=True, blank=True)

    class Meta:
        db_table = "manual_offer_ranking"


class MobileAppInstance(models.Model):
    #https://wiki.appnexus.com/display/api/Mobile+App+Instance+Service
    id = models.IntegerField(primary_key=True)
    fetch_date = models.DateTimeField(null=True, blank=True, db_index=True)
    #instance - bundle - see model MobileAppInstanceBundle below
    mobile_app_store = models.ForeignKey("MobileAppStore", null=True, blank=True)
    store_name = models.TextField(null=True, blank=True)
    store_url = models.TextField(null=True, blank=True)
    mobile_app_store = models.TextField(null=True, blank=True)
    last_modified = models.DateTimeField(default=now_tz) 
    created_on = models.DateTimeField(null=True, blank=True)

    api_endpoint = 'mobile-app-instance'
    class Meta:
        db_table = "mobile_app_instance"


class MobileAppInstanceBundle(models.Model):
    bundle_id = models.IntegerField(primary_key=True)
    os_family = models.ForeignKey("OSFamily", null=True, blank=True)
    last_modified = models.DateTimeField(default=now_tz) 
    created_on = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = "mobile_app_instance_bundle"


class MobileAppStore(models.Model):
    #https://wiki.appnexus.com/display/api/Mobile+App+Store+Service
    id = models.IntegerField(primary_key=True)
    name = models.TextField(null=True, blank=True, db_index=True)
    url = models.TextField(null=True, blank=True)
    os_family = models.ForeignKey("OSFamily", null=True, blank=True)
    last_modified = models.DateTimeField(default=now_tz) 

    class Meta:
        db_table = "mobile_app_store"


INTENDED_AUDIENCE = (
    ('general', 'general'),
    ('children', 'children'),
    ('young_adult', 'young_adult'),
    ('mature', 'mature'),

)


SUPPLY_TYPE = (
    ('web', 'web'),
    ('mobile_app', 'mobile_app'),
    ('mobile_web', 'mobile_web'),
    ('facebook_sidebar', 'facebook_sidebar')
)


class Site(models.Model):
    #https://wiki.appnexus.com/display/api/Site+Service
    id = models.IntegerField(primary_key=True)
    fetch_date = models.DateTimeField(null=True, blank=True, db_index=True)
    code = models.TextField(null=True, blank=True, db_index=True)
    name = models.TextField(null=True, blank=True, db_index=True)
    state = models.TextField(
        choices=STATE_CHOICES,
        null=True, blank=True)
    url = models.TextField(null=True, blank=True)
    publisherd = models.ForeignKey("Publisher", null=True, blank=True)
    primary_content_category = models.ForeignKey("ContentCategory", null=True, blank=True)
    last_modified = models.DateTimeField(default=now_tz) 
    #placements = array - see model Placement below
    #content_categories = array - see model SiteContentCategory below
    intended_audience = models.TextField(
        choices=INTENDED_AUDIENCE,
        null=True, blank=True)
    managed_optimization_zone = models.ForeignKey("OptimizationZone", null=True, blank=True,
                                                  related_name='managed_optimization_zone_id')
    rtb_optimization_zone = models.ForeignKey("OptimizationZone", null=True, blank=True,
                                              related_name='rtb_optimization_zone_id')
    #inventory_attributes = array - see model SiteInventoryAttributes below
    audited = models.NullBooleanField(null=True, blank=True)
    publisher_join = models.TextField(null=True, blank=True) # it is an array in origin but there is no description
    supply_type = models.TextField(
        choices=SUPPLY_TYPE,
        null=True, blank=True)
    creative_format_action = models.NullBooleanField(null=True, blank=True)
    creative_formats = models.TextField(null=True, blank=True) # array in origine - we need use Postgresql Array of string
    allowed_click_actions = models.TextField(null=True, blank=True) #array in origine - we need use Postgresql Array of string
    marketplace_map = models.TextField(null=True, blank=True) # it is an array in origin but there is no description
    mobile_app_instance = models.ForeignKey("MobileAppInstance", null=True, blank=True)

    api_endpoint = 'site'
    class Meta:
        db_table = "site"


class SiteInventoryAttributes(models.Model):
    site = models.ForeignKey("Site", null=True, blank=True)
    inventory_attribute = models.ForeignKey("InventoryAttribute", null=True, blank=True)

    class Meta:
        db_table = "site_inventory_attributes"


class SiteContentCategory(models.Model):
    site = models.ForeignKey("Site", null=True, blank=True)
    content_category = models.ForeignKey("ContentCategory", null=True, blank=True)

    class Meta:
        db_table = "site_content_category"


class YieldManagementProfile(models.Model):
    #https://wiki.appnexus.com/display/api/Yield+Management+Profile+Service
    id = models.IntegerField(primary_key=True)
    fetch_date = models.DateTimeField(null=True, blank=True, db_index=True)
    code = models.TextField(null=True, blank=True, db_index=True)
    name = models.TextField(null=True, blank=True, db_index=True)
    description = models.TextField(null=True, blank=True)
    base_ym_bias_id = models.IntegerField(null=True, blank=True, db_index=True) #TODO FK is needed in future
    base_ym_floor_id = models.IntegerField(null=True, blank=True, db_index=True) #TODO FK is needed in future
    publisher = models.ForeignKey("Publisher", null=True, blank=True)
    #modifiers = array - see model YieldManagementProfileModifiers below
    biases = models.TextField(null=True, blank=True) #TODO JSON - may be in future we need modell here
    floors = models.TextField(null=True, blank=True) #TODO JSON - may be in future we need modell here
    last_modified = models.DateTimeField(default=now_tz)

    api_endpoint = 'ym-profile'
    class Meta:
        db_table = "yield_management_profile"


YIELD_MANAGEMENT_PROFILE_MODIFIERS_CHOICES = (
    ('bias-pct', 'bias-pct'),
    ('bias-cpm', 'bias-cpm'),
    ('floor-pct', 'floor-pct'),
    ('floor-cpm', 'floor-cpm')
)


class YieldManagementProfileModifiers(models.Model):
    yield_management_profile = models.ForeignKey("YieldManagementProfile", null=True, blank=True)
    technical_attribute = models.ForeignKey("TechnicalAttribute", null=True, blank=True)
    type = models.TextField(
        choices=YIELD_MANAGEMENT_PROFILE_MODIFIERS_CHOICES,
        null=True, blank=True)
    amount_pct = models.FloatField(null=True, blank=True)
    amount_cpm = models.FloatField(null=True, blank=True)

    class Meta:
        db_table = "yield_management_profile_modifiers"


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
    id = models.IntegerField(primary_key=True)  # No AutoIncrement
    fetch_date = models.DateTimeField(null=True, blank=True, db_index=True)
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
    reselling_exposed_on = models.DateTimeField(null=True, blank=True)
    reselling_name = models.TextField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    is_rtb = models.NullBooleanField(null=True, blank=True)
    timezone = models.TextField(null=True, blank=True) #originally it is enum
    last_modified = models.DateTimeField(default=now_tz) 
    # stats	object #should be in sepparait model if needed
    max_learn_pct = models.IntegerField(null=True, blank=True)
    learn_bypass_cpm = models.IntegerField(null=True, blank=True)
    ad_quality_advanced_mode_enabled = models.NullBooleanField(null=True, blank=True)
    allow_report_on_default_imps = models.NullBooleanField(null=True, blank=True)
    default_site = models.ForeignKey("Site", null=True, blank=True)
    default_ad_profile = models.ForeignKey("AdProfile", null=True, blank=True, related_name='publisher_ad_profile_id')
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
    ym_profile = models.ForeignKey("YieldManagementProfile", null=True, blank=True, related_name='ym_profile_id')
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
    base_payment_rule = models.ForeignKey("PaymentRule", null=True, blank=True)
    base_ad_quality_rule_id = models.IntegerField(null=True, blank=True, db_index=True) #TODO FK is needed in future
    currency = models.TextField(null=True, blank=True)
    visibility_profile_id = models.IntegerField(null=True, blank=True, db_index=True) #TODO FK is needed in future
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

    api_endpoint = 'publisher'
    class Meta:
        db_table = "publisher"


class PublisherContact(models.Model):
    publisher = models.ForeignKey("Publisher", null=True, blank=True)
    name = models.TextField(null=True, blank=True)
    phone = models.TextField(null=True, blank=True)
    email = models.TextField(null=True, blank=True)

    class Meta:
        db_table = "publisher_contact"


class PublisherBrandExceptions(models.Model): # TODO: ManyToMany field
    publisher = models.ForeignKey("Publisher", null=True, blank=True)
    brand = models.ForeignKey("Brand", null=True, blank=True)
    #brand_id = models.IntegerField(null=True, blank=True)
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
)

# https://wiki.appnexus.com/display/api/Content+Category+Service
class ContentCategory(models.Model):
    id = models.IntegerField(primary_key=True)  # No AutoIncrement
    fetch_date = models.DateTimeField(null=True, blank=True, db_index=True)
    name = models.TextField(null=True, blank=True, db_index=True)
    description = models.TextField(null=True, blank=True)
    is_system = models.NullBooleanField(null=True, blank=True)
    parent_category = models.ForeignKey("ContentCategory", null=True, blank=True)
    type = models.TextField(
        choices=CONTENT_CATEGORY_TYPE,
        null=True, blank=True)
    last_modified = models.DateTimeField(default=now_tz)

    api_endpoint = 'content-category'
    class Meta:
        db_table = "content_category"

    def TransformFields(self, data):
        if data['parent_category']:
            self.parent_category_id = int(data['parent_category']['id'])


class Language(models.Model):
    id = models.IntegerField(primary_key=True)  # No AutoIncrement
    fetch_date = models.DateTimeField(null=True, blank=True, db_index=True)
    name = models.TextField(null=True, blank=True, db_index=True)

    api_endpoint = 'language'
    class Meta:
        db_table = "language"


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
    fetch_date = models.DateTimeField(null=True, blank=True, db_index=True)
    code = models.TextField(null=True, blank=True, db_index=True)
    code2 = models.TextField(null=True, blank=True, db_index=True)
    name = models.TextField(null=True, blank=True, db_index=True)
    type = models.TextField(
        choices=CREATIVE_TYPE_CHOICES,
        null=True, blank=True)
    advertiser = models.ForeignKey("Advertiser", null=True, blank=True)
    publisher = models.ForeignKey("Publisher", null=True, blank=True)
    brand = models.ForeignKey("Brand", null=True, blank=True)
    #brand_id = models.IntegerField(null=True, blank=True)
    state = models.TextField(
        choices=STATE_CHOICES,
        null=True, blank=True)
    click_track_result = models.TextField(
        choices=CLICK_TEST_RESULT_COICES,
        null=True, blank=True)
    #campaigns = array - see model CampaignCreative
    template = models.ForeignKey("CreativeTemplate", null=True, blank=True)
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
    profile = models.ForeignKey("Profile", null=True, blank=True)
    folder = models.ForeignKey("CreativeFolder", null=True, blank=True)
    #line_items = array - see model LineItemCreatives
    #pixels = array - see model CreativePixel below
    track_clicks = models.NullBooleanField(null=True, blank=True)
    flash_backup_content = models.TextField(null=True, blank=True)
    flash_backup_file_name = models.TextField(null=True, blank=True)
    flash_backup_url = models.TextField(null=True, blank=True)
    is_control = models.NullBooleanField(null=True, blank=True)
    #segments = array - see model CreativeSegment below
    created_on = models.DateTimeField(default=now_tz)
    last_modified = models.DateTimeField(default=now_tz) 
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
    #technical_attributes - see model CreativeTechnicalAttribute
    language = models.ForeignKey("Language", null=True, blank=True)
    pop_values = models.TextField(null=True, blank=True) #TODO JSON
    sla = models.IntegerField(null=True, blank=True)
    sla_eta = models.DateTimeField(null=True, blank=True)
    currency = models.TextField(null=True, blank=True)
    first_run = models.DateTimeField(default=now_tz)
    last_run = models.DateTimeField(null=True, blank=True)
    mobile = models.TextField(null=True, blank=True) #TODO JSON
    video_attribute = models.TextField(null=True, blank=True) #TODO JSON
    #stats = object # - will create another model in it will be needed
    content_source = models.TextField(null=True, blank=True)
    custom_request_template = models.TextField(null=True, blank=True) #TODO JSON
    #competitive_brands = array - see model CreativeCompetitiveBrand below
    #competitive_categories = array - see model CreativeCompetitiveCategory below
    #thirdparty_pixels = array - see model CreativeThirdpartyPixel
    #native = models.TextField(null=True, blank=True) #TODO JSON
    #adx_audit = models.TextField(null=True, blank=True) #TODO JSON
    flash_backup_url_secure = models.TextField(null=True, blank=True)
    member = models.ForeignKey("Member", null=True, blank=True)

    api_endpoint = 'creative'
    class Meta:
        db_table = "creative"


class CreativeTechnicalAttribute(models.Model):
    technical_attribute = models.ForeignKey("TechnicalAttribute", null=True, blank=True)
    creative = models.ForeignKey("Creative", null=True, blank=True)

    class Meta:
        db_table = "creative_technical_attribute"


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


class CreativeThirdpartyPixel(models.Model):
    thirdparty_pixel = models.ForeignKey("ThirdPartyPixel", null=True, blank=True)
    creative = models.ForeignKey("Creative", null=True, blank=True)

    class Meta:
        db_table = "creative_thirdparty_pixel"


class CreativeCompetitiveBrand(models.Model):
    creative = models.ForeignKey("Creative", null=True, blank=True)
    brand = models.ForeignKey("Brand", null=True, blank=True)
    #brand_id = models.IntegerField(null=True, blank=True)
    class Meta:
        db_table = "creative_competitive_brand"


class CreativeCompetitiveCategory(models.Model):
    creative = models.ForeignKey("Creative", null=True, blank=True)
    category = models.ForeignKey("Category", null=True, blank=True)

    class Meta:
        db_table = "creative_competitive_category"


class CreativeAdserver(models.Model):
    id = models.IntegerField(primary_key=True)  # No AutoIncrement
    creative = models.ForeignKey("Creative", null=True, blank=True)
    ad_server = models.ForeignKey("AdServer", null=True, blank=True)
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
    id = models.IntegerField(primary_key=True)  # No AutoIncrement
    fetch_date = models.DateTimeField(null=True, blank=True, db_index=True)
    name = models.TextField(null=True, blank=True, db_index=True)
    advertiser = models.ForeignKey("Advertiser", null=True, blank=True)
    last_modified = models.DateTimeField(default=now_tz)

    api_endpoint = 'creative-folder'
    class Meta:
        db_table = "creative_folder"


class CreativeTemplate(models.Model):
    #https://wiki.appnexus.com/display/api/Creative+Template+Service
    id = models.IntegerField(primary_key=True)  # No AutoIncrement
    fetch_date = models.DateTimeField(null=True, blank=True, db_index=True)
    name = models.TextField(null=True, blank=True, db_index=True)
    description = models.TextField(null=True, blank=True)
    member = models.ForeignKey("Member", null=True, blank=True)
    media_subtype = models.ForeignKey("MediaSubType", null=True, blank=True)
    format = models.ForeignKey("CreativeFormat", null=True, blank=True)
    is_default = models.NullBooleanField(null=True, blank=True)
    is_archived = models.NullBooleanField(null=True, blank=True)
    content_js = models.TextField(null=True, blank=True)
    content_html = models.TextField(null=True, blank=True)
    content_xml = models.TextField(null=True, blank=True)
    callback_content_html = models.TextField(null=True, blank=True)
    macros = models.TextField(null=True, blank=True) #array of object in origin. Later we can create separate model for it if needed
    last_modified = models.DateTimeField(default=now_tz)

    api_endpoint = 'template'
    class Meta:
        db_table = "creative_template"


class CreativeFormat(models.Model):
    #https://wiki.appnexus.com/display/api/Creative+Format+Service
    id = models.IntegerField(primary_key=True)  # No AutoIncrement
    fetch_date = models.DateTimeField(null=True, blank=True, db_index=True)
    name = models.TextField(null=True, blank=True, db_index=True)
    last_modified = models.DateTimeField(default=now_tz)

    api_endpoint = 'creative-format'
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


DEMAND_FILTER_ACTION_CHOICES = (
    ('include', 'include'),
    ('exclude', 'exclude'),
    ('default', 'default')
)


class Placement(models.Model):
    #https://wiki.appnexus.com/display/api/Placement+Service
    id = models.IntegerField(primary_key=True)  # No AutoIncrement
    fetch_date = models.DateTimeField(null=True, blank=True, db_index=True)
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
    publisher = models.ForeignKey("Publisher", null=True, blank=True)
    site = models.ForeignKey("Site", null=True, blank=True)
    inventory_source_id = models.IntegerField(null=True, blank=True, db_index=True) #TODO FK is needed in future
    ad_profile = models.ForeignKey("AdProfile", null=True, blank=True)
    #supported_media_types = array - see model PlacementMediaType below
    #supported_media_subtypes = array - see model PlacementMediaSubType below
    #pop_values = array - see model PlacementPopValues
    default_creative = models.ForeignKey("Creative", null=True, blank=True)
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
    demand_filter_action = models.TextField(
        choices=DEMAND_FILTER_ACTION_CHOICES,
        null=True, blank=True)
    floor_application_target = models.TextField(
        choices=FLOOR_APPLICATION_TARGET,
        null=True, blank=True)
    pixel_url_secure = models.TextField(null=True, blank=True)
    site_audit_status = models.TextField(
        choices=SITE_AUDIT_STATUS,
        null=True, blank=True)
    toolbar = models.TextField(null=True, blank=True) #TODO JSON
    cost_cpm = models.FloatField(null=True, blank=True)
    is_prohibited = models.NullBooleanField(null=True, blank=True)
    last_modified = models.DateTimeField(default=now_tz) 
    #stats - will create another model in it will be needed
    content_retrieval_timeout_ms = models.IntegerField(null=True, blank=True)
    enable_for_mediation = models.NullBooleanField(null=True, blank=True)
    #private_sizes = array - see model PlacementPrivateSizes below
    video = models.TextField(null=True, blank=True) #TODO JSON
    ad_types = models.TextField(null=True, blank=True) #TODO it is an array in origin but there is no description of it so we need to look at the API responce
    use_detected_domain = models.NullBooleanField(null=True, blank=True)

    api_endpoint = 'placement'
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
    member = models.ForeignKey("Member", null=True, blank=True)
    price = models.FloatField(null=True, blank=True)
    expire_minutes = models.IntegerField(null=True, blank=True)
    enable_rm_piggyback = models.NullBooleanField(null=True, blank=True)
    max_usersync_pixels = models.IntegerField(null=True, blank=True)
    last_modified = models.DateTimeField(default=now_tz) 
    provider = models.TextField(null=True, blank=True)
    advertiser = models.ForeignKey("Advertiser", null=True, blank=True)
    #piggyback_pixels - see model PiggybackPixels below
    parent_segment = models.ForeignKey("Segment", null=True, blank=True)
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
    last_activity = models.DateTimeField(default=now_tz)

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
    last_modified = models.DateTimeField(default=now_tz) 

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
    last_modified = models.DateTimeField(default=now_tz) 

    class Meta:
        db_table = "placement_media_sub_type"


class PublisherPlacement(models.Model):
    placement = models.ForeignKey("Placement", null=True, blank=True) #id in origin
    publisher = models.ForeignKey("Publisher", null=True, blank=True)
    code = models.TextField(null=True, blank=True)

    class Meta:
        db_table = "publisher_placement"


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
    "https://wiki.appnexus.com/display/api/Conversion+Pixel+Service"
    id = models.IntegerField(primary_key=True) # No AutoIncrement
    fetch_date = models.DateTimeField(null=True, blank=True, db_index=True)
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
    created_on = models.DateTimeField(default=now_tz)
    last_modified = models.DateTimeField(default=now_tz) 
    advertiser = models.ForeignKey("Advertiser", null=True, blank=True)

    api_endpoint = 'pixel'
    class Meta:
        db_table = "conversion_pixel"


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
    last_modified = models.DateTimeField(default=now_tz)

    api_endpoint = 'operating-system-family'
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
    last_modified = models.DateTimeField(default=now_tz) 

    class Meta:
        db_table = "operating_system"


class OperatingSystemExtended(models.Model):
    id = models.IntegerField(primary_key=True) #No AutoIncrement
    fetch_date = models.DateTimeField(null=True, blank=True, db_index=True)
    name = models.TextField(null=True, blank=True, db_index=True)
    os_family = models.ForeignKey("OSFamily", null=True, blank=True)
    last_modified = models.DateTimeField(default=now_tz) 
    search_string = models.TextField(null=True, blank=True)
    
    def TransformFields(self, data, metadata={}):
        self.os_family_id = data["family"]["id"]

    api_endpoint = 'operating-system-extended'
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
    advertiser = models.ForeignKey("Advertiser", null=True, blank=True, related_name='advertiser_id')
    code = models.TextField(null=True, blank=True)
    description = models.TextField(null=True, blank=True, db_index=True)
    is_template = models.NullBooleanField(null=True, blank=True)
    last_modified = models.DateTimeField(default=now_tz) 
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
    created_on = models.DateTimeField(default=now_tz)
    is_expired = models.NullBooleanField(null=True, blank=True)

    api_endpoint = 'profile'
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


MODEL_OUTPUT_CHOICES = (
    ('bid', 'bid'),
    ('bid_modifier', 'bid_modifier')
)


CUSTOM_MODEL_STRUCTURE_CHOICES = (
    ('decision_tree', 'decision_tree'),
    ('decision_tree', 'decision_tree')
)


class CustomModel(models.Model):
    #https://wiki.appnexus.com/display/api/Custom+Model+Service
    id = models.IntegerField(primary_key=True) #No AutoIncrement
    fetch_date = models.DateTimeField(null=True, blank=True, db_index=True)
    name = models.TextField(null=True, blank=True, db_index=True)
    member = models.ForeignKey("Member", null=True, blank=True)
    advertiser = models.ForeignKey("Advertiser", null=True, blank=True)
    custom_model_structure = models.TextField(
        choices=CUSTOM_MODEL_STRUCTURE_CHOICES,
        null=True, blank=True)
    model_output = models.TextField(
        choices=MODEL_OUTPUT_CHOICES,
        null=True, blank=True)
    model_text = models.TextField(null=True, blank=True)
    original_text = models.TextField(null=True, blank=True)
    active = models.NullBooleanField(null=True, blank=True)
    last_modified = models.DateTimeField(default=now_tz) 

    class Meta:
        db_table = "custom_model"


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
    start_date = models.DateTimeField(db_index=True, null=True, default=now_tz)
    end_date = models.DateTimeField(db_index=True, null=True, blank=True)
    #creatives - see model CampaignCreative below
    #creative_groups - se model CampaignLineItems below
    timezone = models.TextField(null=True, blank=True)
    last_modified = models.DateTimeField(default=now_tz) 
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
    bid_model = models.ForeignKey("CustomModel", null=True, blank=True)
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

    api_endpoint = 'campaign'
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
    start_date = models.DateTimeField(null=True, blank=True)
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
    last_modified = models.DateTimeField(default=now_tz) 
    click_url = models.TextField(null=True, blank=True)
    currency = models.TextField(null=True, blank=True)
    require_cookie_for_tracking = models.NullBooleanField(null=True, blank=True)
    profile = models.ForeignKey("Profile", null=True, blank=True)
    member = models.ForeignKey("Member", null=True, blank=True)
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

    api_endpoint = 'line-item'
    class Meta:
        db_table = "line_item"


class LineItemCreatives(models.Model):
    line_item = models.ForeignKey("LineItem", null=True, blank=True)
    creative = models.ForeignKey("Creative", null=True, blank=True)
    code = models.TextField(null=True, blank=True, db_index=True)

    class Meta:
        db_table = "line_item_creatives"


PRICING_TYPE_CHOICES = (
    ('cpm', 'cpm'),
    ('revshare', 'revshare'),
    ('dynamic', 'dynamic')
)


BUYER_TYPE_CHOICES = (
    ('direct', 'direct'),
    ('rtb', 'rtb'),
    ('both', 'both')
)


class PaymentRule(models.Model):
    #https://wiki.appnexus.com/display/api/Payment+Rule+Service
    id = models.IntegerField(primary_key=True) # No AutoIncrement
    fetch_date = models.DateTimeField(null=True, blank=True, db_index=True)
    name = models.TextField(null=True, blank=True, db_index=True)
    code = models.TextField(null=True, blank=True, db_index=True)
    state = models.TextField(
        choices=STATE_CHOICES,
        null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    start_date = models.DateTimeField(null=True, blank=True)
    end_date = models.DateTimeField(null=True, blank=True)
    pricing_type = models.TextField(
        choices=PRICING_TYPE_CHOICES,
        null=True, blank=True)
    cost_cpm = models.FloatField(null=True, blank=True)
    revshare = models.FloatField(null=True, blank=True)
    profile = models.ForeignKey("Profile", null=True, blank=True)
    priority = models.IntegerField(null=True, blank=True)
    timezone = models.TextField(null=True, blank=True)
    last_modified = models.DateTimeField(default=now_tz) 
    #filtered_advertisers = array - see model FilteredPaymentRuleAdvertisers below
    #filtered_line_items = array - see model FilteredPaymentRuleAdvertisers below
    #filtered_campaigns = array - see model FilteredPaymentRuleAdvertisers below
    buyer_type = models.TextField(
        choices=BUYER_TYPE_CHOICES,
        null=True, blank=True)
    max_revshare = models.FloatField(null=True, blank=True)
    apply_cost_on_default = models.NullBooleanField(null=True, blank=True)
    demand_filter_action = models.TextField(
        choices=DEMAND_FILTER_ACTION_CHOICES,
        null=True, blank=True)

    api_endpoint = 'payment-rule'
    class Meta:
        db_table = "payment_rule"


class FilteredPaymentRuleAdvertisers(models.Model):
    payment_rule = models.ForeignKey("PaymentRule", null=True, blank=True)
    advertiser = models.ForeignKey("Advertiser", null=True, blank=True)

    class Meta:
        db_table = "filtered_payment_rule_advertisers"


class FilteredPaymentRuleLineItems(models.Model):
    payment_rule = models.ForeignKey("PaymentRule", null=True, blank=True)
    line_item = models.ForeignKey("LineItem", null=True, blank=True)

    class Meta:
        db_table = "filtered_payment_rule_line_items"


class FilteredPaymentRuleCampaigns(models.Model):
    payment_rule = models.ForeignKey("PaymentRule", null=True, blank=True)
    campaign = models.ForeignKey("Campaign", null=True, blank=True)

    class Meta:
        db_table = "filtered_payment_rule_campaigns"


class ClickTracker(models.Model):
    #https://wiki.appnexus.com/display/api/Click+Tracker+Service
    id = models.IntegerField(primary_key=True) # No AutoIncrement
    fetch_date = models.DateTimeField(null=True, blank=True, db_index=True)
    member = models.ForeignKey("Member", null=True, blank=True)
    advertiser = models.ForeignKey("Advertiser", null=True, blank=True)
    name = models.TextField(null=True, blank=True, db_index=True)
    code = models.TextField(null=True, blank=True, db_index=True)
    state = models.TextField(
        choices=STATE_CHOICES,
        null=True, blank=True)
    click_url = models.TextField(null=True, blank=True, db_index=True)
    publisher = models.ForeignKey("Publisher", null=True, blank=True)
    #tag = array - see model ClickTrackerPlacement below
    payment_rule = models.ForeignKey("PaymentRule", null=True, blank=True)
    line_item = models.ForeignKey("LineItem", null=True, blank=True)
    last_modified = models.DateTimeField(default=now_tz) 

    class Meta:
        db_table = "click_tracker"


class ClickTrackerPlacement(models.Model):
    id = models.IntegerField(primary_key=True) # No AutoIncrement
    fetch_date = models.DateTimeField(null=True, blank=True, db_index=True)
    click_tracker = models.ForeignKey("ClickTracker", null=True, blank=True)
    placement = models.ForeignKey("Placement", null=True, blank=True)

    class Meta:
        db_table = "click_tracker_placement"


class ImpressionTracker(models.Model):
    #https://wiki.appnexus.com/display/api/Impression+Tracker+Service
    member = models.ForeignKey("Member", null=True, blank=True)
    advertiser = models.ForeignKey("Advertiser", null=True, blank=True)
    name = models.TextField(null=True, blank=True, db_index=True)
    code = models.TextField(null=True, blank=True, db_index=True)
    state = models.TextField(
        choices=STATE_CHOICES,
        null=True, blank=True)
    publisher = models.ForeignKey("Publisher", null=True, blank=True)
    #tag = array - see model ImpressionTrackerPlacement below
    payment_rule = models.ForeignKey("PaymentRule", null=True, blank=True)
    line_item = models.ForeignKey("LineItem", null=True, blank=True)
    last_modified = models.DateTimeField(default=now_tz) 

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
    start_date = models.DateTimeField(null=True, blank=True)
    end_date = models.DateTimeField(null=True, blank=True)
    last_modified = models.DateTimeField(default=now_tz) 
    timezone = models.TextField(null=True, blank=True)  # enum
    currency = models.TextField(null=True, blank=True)
    comments = models.TextField(null=True, blank=True)
    billing_code = models.IntegerField(null=True, blank=True)
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

    api_endpoint = 'insertion-order'
    class Meta:
        db_table = "insertion_order"


PAYMENT_TYPE_CHOICES = (
    ('cpm', 'cpm'),
    ('revshare', 'revshare')
)


class Broker(models.Model):
    #https://wiki.appnexus.com/display/api/Broker+Service
    id = models.IntegerField(primary_key=True)  # No AutoIncrement
    name = models.TextField(null=True, blank=True, db_index=True)
    state = models.TextField(
        choices=STATE_CHOICES,
        null=True, blank=True)
    member = models.ForeignKey("Member", null=True, blank=True)
    last_modified = models.DateTimeField(default=now_tz) 

    class Meta:
        db_table = "broker"


class InsertionOrderBrokerFees(models.Model):
    insertion_order = models.ForeignKey("InsertionOrder", null=True, blank=True)
    broker = models.ForeignKey("Broker", null=True, blank=True)
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


class LineItemConversionPixel(models.Model):
    pixel = models.ForeignKey("ConversionPixel", null=True, blank=True)
    line_item = models.ForeignKey("LineItem", null=True, blank=True)

    class Meta:
        db_table = "line_item_conversion_pixel"


class LineItemLabel(models.Model):
    label = models.ForeignKey("Label", null=True, blank=True) #id in origin
    line_item = models.ForeignKey("LineItem", null=True, blank=True)

    class Meta:
        db_table = "line_item_label"


class LineItemBroker(models.Model):
    broker = models.ForeignKey("Broker", null=True, blank=True)
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
    broker = models.ForeignKey("Broker", null=True, blank=True)
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
    last_updated = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = "network_analytics_raw"

    def __unicode__(self):
        return self.id


class BuyerGroup(models.Model):
    #https://wiki.appnexus.com/display/api/Buyer+Group+Service
    id = models.IntegerField(primary_key=True)  # No AutoIncrement
    fetch_date = models.DateTimeField(null=True, blank=True, db_index=True)
    code = models.TextField(null=True, blank=True, db_index=True)
    name = models.TextField(null=True, blank=True, db_index=True)
    description = models.TextField(null=True, blank=True)
    last_modified = models.DateTimeField(default=now_tz)

    api_endpoint = 'buyer-group'
    class Meta:
        db_table = "buyer_group"


MEMBER_ENTITY_TYPE = (
    ('reseller', 'reseller'),
    ('direct', 'direct')
)


MEMBER_RESELLING_EXPOSURE = (
    ('public', 'public'),
    ('private', 'private')
)


MEMBER_PLATFORM_EXPOSURE = (
    ('public', 'public'),
    ('private', 'private'),
    ('hidden', 'hidden')
)


MEMBER_DEFAULT_CAMPAIGN_TRUST = (
    ('seller', 'seller'),
    ('appnexus', 'appnexus')
)


class Developer(models.Model):
    """Description at https://wiki.appnexus.com/display/api/Developer+Service"""
    id = models.IntegerField(primary_key=True) # No AutoIncrement
    fetch_date = models.DateTimeField(null=True, blank=True, db_index=True)
    name = models.TextField(null=True, blank=True, db_index=True)
    entity_id = models.IntegerField(null=True, blank=True)
    phone = models.TextField(null=True, blank=True)
    email = models.TextField(null=True, blank=True)
    billing_address_1 = models.TextField(null=True, blank=True)
    billing_address_2 = models.TextField(null=True, blank=True)
    billing_city = models.TextField(null=True, blank=True)
    billing_region = models.TextField(null=True, blank=True)
    billing_postal_code = models.TextField(null=True, blank=True)
    billing_country = models.TextField(null=True, blank=True)
    last_modified = models.DateTimeField(default=now_tz)

    api_endpoint = 'developer'
    class Meta:
        db_table = "developer"


class Member(models.Model):
    #https://wiki.appnexus.com/display/api/Member+Service
    id = models.IntegerField(primary_key=True) # No AutoIncrement
    fetch_date = models.DateTimeField(null=True, blank=True, db_index=True)
    name = models.TextField(null=True, blank=True, db_index=True)
    reselling_description = models.TextField(null=True, blank=True)
    state = models.TextField(
        choices=STATE_CHOICES,
        null=True, blank=True)
    no_reselling_priority = models.IntegerField(null=True, blank=True)
    entity_type = models.TextField(
        choices=MEMBER_ENTITY_TYPE,
        null=True, blank=True)
    buyer_clearing_fee_pct = models.FloatField(null=True, blank=True)
    app_contract_accepted = models.NullBooleanField(null=True, blank=True)
    default_buyer_group = models.ForeignKey("BuyerGroup", null=True, blank=True)
    interface_domain = models.TextField(null=True, blank=True)
    interface_domain_beta = models.TextField(null=True, blank=True)
    creative_size_minimum_bytes = models.IntegerField(null=True, blank=True)
    creative_size_fee_per_gb = models.FloatField(null=True, blank=True)
    default_ad_profile = models.ForeignKey("AdProfile", null=True, blank=True, related_name='member_ad_profile_id')
    email_code = models.TextField(null=True, blank=True)
    serving_domain = object
    reselling_exposure = models.TextField(
        choices=MEMBER_RESELLING_EXPOSURE,
        null=True, blank=True)
    reselling_exposed_on = models.TextField(null=True, blank=True)
    last_modified = models.DateTimeField(default=now_tz) 
    standard_sizes = models.TextField(null=True, blank=True) #TODO JSON
    buyer_credit_limit = models.FloatField(null=True, blank=True)
    timezone = models.TextField(null=True, blank=True)  # enum
    seller_revshare_pct = models.IntegerField(null=True, blank=True)
    #default_country = array - see model MemberCountry below
    dongle = models.TextField(null=True, blank=True)
    platform_exposure = models.TextField(
        choices=MEMBER_PLATFORM_EXPOSURE,
        null=True, blank=True)
    audit_notify_email = models.TextField(null=True, blank=True)
    sherlock_notify_email = models.TextField(null=True, blank=True)
    domain_blacklist_email = models.TextField(null=True, blank=True)
    contact_email = models.TextField(null=True, blank=True)
    allow_ad_profile_override = models.NullBooleanField(null=True, blank=True)
    default_currency = models.TextField(null=True, blank=True)
    use_insertion_orders = models.NullBooleanField(null=True, blank=True)
    expose_optimization_levers = models.NullBooleanField(null=True, blank=True)
    pops_enabled_UI = models.NullBooleanField(null=True, blank=True)
    default_accept_supply_partner_usersync = models.NullBooleanField(null=True, blank=True)
    default_accept_data_provider_usersync = models.NullBooleanField(null=True, blank=True)
    default_accept_demand_partner_usersync = models.NullBooleanField(null=True, blank=True)
    short_name = models.TextField(null=True, blank=True, db_index=True)
    expose_eap_ecp_placement_settings = models.NullBooleanField(null=True, blank=True)
    daily_imps_verified = models.IntegerField(null=True, blank=True)
    daily_imps_self_audited = models.IntegerField(null=True, blank=True)
    daily_imps_unaudited = models.IntegerField(null=True, blank=True)
    is_iash_compliant = models.NullBooleanField(null=True, blank=True)
    deal_types = models.TextField(null=True, blank=True) #TODO JSON or Model - no description in source
    allow_non_cpm_payment = models.NullBooleanField(null=True, blank=True)
    default_allow_cpc = models.NullBooleanField(null=True, blank=True)
    default_allow_cpa = models.NullBooleanField(null=True, blank=True)
    visibility_profile_id = models.IntegerField(null=True, blank=True, db_index=True) #TODO FK is needed in future
    default_campaign_trust = models.TextField(
        choices=MEMBER_DEFAULT_CAMPAIGN_TRUST,
        null=True, blank=True)
    default_campaign_allow_unaudited = models.NullBooleanField(null=True, blank=True)
    website_url = models.TextField(null=True, blank=True)
    contract_allows_unaudited = models.NullBooleanField(null=True, blank=True)
    reporting_decimal_type = models.TextField(
        choices=REPORTING_DECIMAL_TYPE,
        null=True, blank=True)
    plugins_enabled = models.NullBooleanField(null=True, blank=True)
    #plugins = array - see model MemberPlugin below
    enable_click_and_imp_trackers = models.NullBooleanField(null=True, blank=True)
    max_hosted_video_size = models.IntegerField(null=True, blank=True)
    require_facebook_preaudit = models.NullBooleanField(null=True, blank=True)
    developer = models.ForeignKey("Developer", null=True, blank=True)
    pitbull_segment_id = models.IntegerField(null=True, blank=True, db_index=True) #TODO FK is needed in future
    pitbull_segment_value = models.IntegerField(null=True, blank=True)
    #content_categories = array - see model MemberContentCategory below
    #inventory_trust = array - see model MemberInventoryTrust below
    #seller_member_groups = array - see model SellerMemberGroup below
    default_content_retrieval_timeout_ms = models.IntegerField(null=True, blank=True)
    default_enable_for_mediation = models.NullBooleanField(null=True, blank=True)
    prioritize_margin = models.NullBooleanField(null=True, blank=True)
    #member_brand_exceptions = array - see model MemberBrandException below
    #thirdparty_pixels = array - see model MemberThirdpartyPixel below
    #floor_optimization = array - see model MemberFloorOptimisation below
    mediation_auto_bid_adjustment_enabled = models.NullBooleanField(null=True, blank=True)
    reporting_sync_enabled = models.NullBooleanField(null=True, blank=True)
    native_custom_keys = models.TextField(null=True, blank=True) #TODO JSON or Model - array in source
    daily_budget = models.DecimalField(null=True, blank=True, max_digits=35, decimal_places=10)
    daily_budget_imps = models.IntegerField(null=True, blank=True)

    api_endpoint = 'member'
    class Meta:
        db_table = "member"


PRIMARY_PLATFORM_MEMBER_TYPE_CHOICES = (
    ('network', 'network'),
    ('buyer', 'buyer'),
    ('seller', 'seller'),
    ('data_provider', 'data_provider')
)


SELLER_TYPE_CHOICES = (
    ('platform', 'platform'),
    ('partner', 'partner')
)


class MemberProfile(models.Model):
    #https://wiki.appnexus.com/display/api/Member+Profile+Service
    id = models.IntegerField(primary_key=True) # No AutoIncrement
    domain_list_action = models.TextField(
        choices=TARGETS_ACTION_CHOICE,
        null=True, blank=True)
    domain_list_targets = models.TextField(null=True, blank=True) #array of objects in origin TODO it is needed to be concidered if we need a sepparait model here
    #country_targets - see model MemberProfileCountry below
    last_modified = models.DateTimeField(default=now_tz) 

    class Meta:
        db_table = "member_profile"


class MemberProfileCountry(models.Model):
    member_profile = models.ForeignKey("MemberProfile", null=True, blank=True)
    country = models.ForeignKey("Country", null=True, blank=True)

    class Meta:
        db_table = "member_profilecountry"


class PlatformMember(models.Model):
    #https://wiki.appnexus.com/display/api/Platform+Member+Service
    id = models.IntegerField(primary_key=True) # No AutoIncrement
    fetch_date = models.DateTimeField(null=True, blank=True, db_index=True)
    name = models.TextField(null=True, blank=True, db_index=True)
    primary_type = models.TextField(
        choices=PRIMARY_PLATFORM_MEMBER_TYPE_CHOICES,
        null=True, blank=True)
    platform_exposure = models.TextField(
        choices=MEMBER_RESELLING_EXPOSURE,
        null=True, blank=True)
    email = models.TextField(null=True, blank=True)
    daily_imps_any_audit_status = models.BigIntegerField(null=True, blank=True)
    daily_imps_appnexus_reviewed = models.BigIntegerField(null=True, blank=True)
    daily_imps_appnexus_seller_reviewed = models.BigIntegerField(null=True, blank=True)
    is_iash_compliant = models.NullBooleanField(null=True, blank=True)
    has_resold = models.NullBooleanField(null=True, blank=True)
    visibility_rules = models.TextField(null=True, blank=True) #TODO JSON
    bidder = models.ForeignKey('User', null=True, blank=True, db_index=True)
    seller_type = models.TextField(
        choices=SELLER_TYPE_CHOICES,
        null=True, blank=True)
    contact_info = models.TextField(null=True, blank=True) #TODO JSON
    active = models.NullBooleanField(null=True, blank=True)
    last_modified = models.DateTimeField(default=now_tz) 
    default_discrepancy_pct = models.FloatField(null=True, blank=True)

    api_endpoint = 'platform-member'
    class Meta:
        db_table = "platform_member"


class MemberFloorOptimisation(models.Model):
    member = models.ForeignKey("Member", null=True, blank=True)
    active = models.NullBooleanField(null=True, blank=True)
    bidder = models.ForeignKey('User', null=True, blank=True, db_index=True)

    class Meta:
        db_table = "member_floor_optimization"


class MemberThirdpartyPixel(models.Model):
    member = models.ForeignKey("Member", null=True, blank=True)
    thirdparty_pixel = models.ForeignKey("ThirdPartyPixel", null=True, blank=True)

    class Meta:
        db_table = "member_thirdparty_pixel"


class MemberBrandException(models.Model):
    member = models.ForeignKey("Member", null=True, blank=True)
    brand = models.ForeignKey("Brand", null=True, blank=True)
    #brand_id = models.IntegerField(null=True, blank=True)
    class Meta:
        db_table = "member_brand_exception"


class MemberCountry(models.Model):
    member = models.ForeignKey("Member", null=True, blank=True)
    country = models.ForeignKey("Country", null=True, blank=True)

    class Meta:
        db_table = "member_country"


class MemberContentCategory(models.Model):
    member = models.ForeignKey("Member", null=True, blank=True)
    content_category = models.ForeignKey("ContentCategory", null=True, blank=True)

    class Meta:
        db_table = "member_content_category"


class SellerMemberGroup(models.Model):
    id = models.IntegerField(primary_key=True)  # No AutoIncrement
    member = models.ForeignKey("Member", null=True, blank=True)
    display_order = models.IntegerField(null=True, blank=True)
    name = models.TextField(null=True, blank=True, db_index=True)
    description = models.TextField(null=True, blank=True)
    last_modified = models.DateTimeField(default=now_tz) 
    created_on = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = "seller_member_group"


DEFAULT_TRUST_CHOICES = (
    ('appnexus', 'appnexus'),
    ('seller', 'seller')
)


class MemberInventoryTrust(models.Model):
    member = models.ForeignKey("Member", null=True, blank=True)
    members = models.TextField(null=True, blank=True) #TODO JSON
    default_is_banned = models.NullBooleanField(null=True, blank=True)
    default_trust = models.TextField(
        choices=DEFAULT_TRUST_CHOICES,
        null=True, blank=True)
    default_allow_unaudited = models.NullBooleanField(null=True, blank=True)

    class Meta:
        db_table = "member_inventory_trust"


class Plugin(models.Model):
    #https://wiki.appnexus.com/display/api/Plugin+Service
    id = models.IntegerField(primary_key=True)  # No AutoIncrement
    name = models.TextField(null=True, blank=True, db_index=True)
    description = models.TextField(null=True, blank=True)
    public_key = models.TextField(null=True, blank=True)
    moreinfo_url = models.TextField(null=True, blank=True)
    log_level_data_fee = models.IntegerField(null=True, blank=True)
    plugin_category = models.ForeignKey("Category", null=True, blank=True)
    is_available = models.NullBooleanField(null=True, blank=True)
    summary = models.TextField(null=True, blank=True)
    contact_name = models.TextField(null=True, blank=True)
    contact_phone = models.TextField(null=True, blank=True)
    contact_email = models.TextField(null=True, blank=True)
    contact_text = models.TextField(null=True, blank=True)
    author_display_name = models.TextField(null=True, blank=True)
    recommended = models.NullBooleanField(null=True, blank=True)
    featured = models.NullBooleanField(null=True, blank=True)
    has_payment_access = models.NullBooleanField(null=True, blank=True)
    allowed_asset_count = models.IntegerField(null=True, blank=True)
    addendum = models.TextField(null=True, blank=True)
    click_to_install = models.NullBooleanField(null=True, blank=True)
    video_url = models.TextField(null=True, blank=True)
    developer = models.ForeignKey("Developer", null=True, blank=True)
    #domains = array - see model PluginDomain below
    permissions = models.TextField(null=True, blank=True) #TODO JSON or Model - array in source
    #plugin_instances = array -  see model PluginInstance below
    member_availabilities = models.TextField(null=True, blank=True) #TODO JSON or Model - array in source

    class Meta:
        db_table = "plugin"


PLUGIN_STATE = (
    ('available', 'available'),
    ('installed', 'installedinstalled'),
    ('accept_permissions', 'accept_permissions')
)


class PluginDomain(models.Model):
    #https://wiki.appnexus.com/display/api/Plugin+Instance+Service
    plugin = models.ForeignKey("Plugin", null=True, blank=True)
    name = models.TextField(null=True, blank=True, db_index=True)

    class Meta:
        db_table = "plugin_domain"


PLUGIN_INSTANCE_FLAVOUR_CHOICES = (
    ('standalone', 'standalone'),
    ('creative_action', 'creative_action'),
    ('advertiser_menu', 'advertiser_menu'),
    ('publisher_menu', 'publisher_menu'),
    ('conversion_pixel', 'conversion_pixel')
)


class PluginInstance(models.Model):
    id = models.IntegerField(primary_key=True)  # No AutoIncrement
    plugin = models.ForeignKey("Plugin", null=True, blank=True)
    name = models.TextField(null=True, blank=True, db_index=True)
    flavor = models.TextField(
        choices=PLUGIN_INSTANCE_FLAVOUR_CHOICES,
        null=True, blank=True)
    iframe_url = models.TextField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    icon_url = models.TextField(null=True, blank=True)
    proxy_url = models.TextField(null=True, blank=True)

    class Meta:
        db_table = "plugin_instance"


class MemberPlugin(models.Model):
    member = models.ForeignKey("Member", null=True, blank=True)
    plugin = models.ForeignKey("Plugin", null=True, blank=True)
    state = models.TextField(
        choices=PLUGIN_STATE,
        null=True, blank=True)

    class Meta:
        db_table = "member_plugin"


DEAL_PAYMENT_TYPE_CHOICES = (
    ('default', 'default'),
    ('cpvm', 'cpvm')
)


DEAL_TYPE_CHOICES = (
    ('1', 'Open Auction'),
    ('2', 'Private Auction')
)

class Deal(models.Model):
    #https://wiki.appnexus.com/display/api/Deal+Service
    id = models.IntegerField(primary_key=True)  # No AutoIncrement
    fetch_date = models.DateTimeField(null=True, blank=True, db_index=True)
    code = models.TextField(null=True, blank=True, db_index=True)
    name = models.TextField(null=True, blank=True, db_index=True)
    description = models.TextField(null=True, blank=True)
    active = models.NullBooleanField(null=True, blank=True)
    start_date = models.DateTimeField(null=True, blank=True)
    end_date = models.DateTimeField(null=True, blank=True)
    profile = models.ForeignKey("Profile", null=True, blank=True)
    package_id = models.IntegerField(null=True, blank=True, db_index=True) #TODO FK is needed in future
    floor_price = models.FloatField(null=True, blank=True)
    currency = models.TextField(null=True, blank=True)
    use_deal_floor = models.NullBooleanField(null=True, blank=True)
    last_modified = models.DateTimeField(default=now_tz) 
    data_protected = models.NullBooleanField(null=True, blank=True)
    allow_creative_add_on_view = models.NullBooleanField(null=True, blank=True)
    allow_creative_add_on_click = models.NullBooleanField(null=True, blank=True)
    visibility_profile_id = models.IntegerField(null=True, blank=True, db_index=True) #TODO FK is needed in future
    size_preference = models.TextField(null=True, blank=True)
    audit_status_option = models.TextField(null=True, blank=True)
    brand_restrict = models.NullBooleanField(null=True, blank=True)
    category_restrict = models.NullBooleanField(null=True, blank=True)
    language_restrict = models.NullBooleanField(null=True, blank=True)
    technical_attribute_restrict = models.NullBooleanField(null=True, blank=True)
    created_by = models.TextField(null=True, blank=True)
    seller = models.ForeignKey("PlatformMember", related_name='seller_id', null=True, blank=True)
    buyer = models.ForeignKey("PlatformMember", related_name='buyer_id', null=True, blank=True)
    type = models.TextField(
        choices=DEAL_TYPE_CHOICES,
        null=True, blank=True)
    #brands = array - see model DealBrand below
    #categories = array - see model DealCategory below
    #languages = array - see model DealLanguage below
    #technical_attributes = array - see model DealTechnicalAtribute below
    #creatives = array - see model DealCreative below
    ask_price = models.FloatField(null=True, blank=True)
    priority = models.IntegerField(null=True, blank=True)
    payment_type = models.TextField(
        choices=DEAL_PAYMENT_TYPE_CHOICES,
        null=True, blank=True)
    #allowed_media_types = array - see model DealAllowedMediaType below
    #allowed_media_subtypes = array - see model DealAllowedMediaSubType below
    media_preference = models.TextField(null=True, blank=True)

    api_endpoint = 'deal'
    class Meta:
        db_table = "deal"


class DealAllowedMediaSubType(models.Model):
    deal = models.ForeignKey("Deal", null=True, blank=True)
    media_sub_type = models.ForeignKey("MediaSubType", null=True, blank=True)
    last_modified = models.DateTimeField(default=now_tz) 

    class Meta:
        db_table = "deal_allowed_media_sub_type"


class DealAllowedMediaType(models.Model):
    deal = models.ForeignKey("Deal", null=True, blank=True)
    media_type = models.ForeignKey("MediaType", null=True, blank=True)
    last_modified = models.DateTimeField(default=now_tz) 

    class Meta:
        db_table = "deal_allowed_media_type"


CREATIVE_STATUS_CHOICES = (
    ('banned', 'banned'),
    ('approved', 'approved')
)


class DealCreative(models.Model):
    deal = models.ForeignKey("Deal", null=True, blank=True)
    creative = models.ForeignKey("Creative", null=True, blank=True)
    status = models.TextField(
        choices=CREATIVE_STATUS_CHOICES,
        null=True, blank=True)

    class Meta:
        db_table = "deal_creative"


class DealBrand(models.Model):
    deal = models.ForeignKey("Deal", null=True, blank=True)
    brand = models.ForeignKey("Brand", null=True, blank=True)
    #brand_id = models.IntegerField(null=True, blank=True)
    override = models.NullBooleanField(null=True, blank=True)

    class Meta:
        db_table = "deal_brand"


class DealCategory(models.Model):
    deal = models.ForeignKey("Deal", null=True, blank=True)
    category = models.ForeignKey("Category", null=True, blank=True)
    override = models.NullBooleanField(null=True, blank=True)

    class Meta:
        db_table = "deal_category"


class DealTechnicalAtribute(models.Model):
    deal = models.ForeignKey("Deal", null=True, blank=True)
    technical_attribute = models.ForeignKey("TechnicalAttribute", null=True, blank=True)
    override = models.NullBooleanField(null=True, blank=True)

    class Meta:
        db_table = "deal_technical_attribute"


class DealLanguage(models.Model):
    deal = models.ForeignKey("Deal", null=True, blank=True)
    language = models.ForeignKey("Language", null=True, blank=True)
    override = models.NullBooleanField(null=True, blank=True)

    class Meta:
        db_table = "deal_language"


BID_TYPE_CHOICES = (
    ('Manual', 'Manual'),
    ('Learn', 'Learn'),
    ('Optimized', 'Optimized'),
    ('Unknown', 'Unknown'),
    ('Optimized give up', 'Optimized give up'),
    ('Learn give up', 'Learn give up'),
    ('Manual give up', 'Manual give up')
)


IMPRESSION_TYPE_CHOICES = (
    ('1', 'Blank'),
    ('2', 'PSA'),
    ('3', 'Default Error'),
    ('4', 'Default'),
    ('5', 'Kept'),
    ('6', 'Resold'),
    ('7', 'RTB'),
    ('8', 'PSA Error'),
    ('9', 'External Impression'),
    ('10', 'External Click'),
    ('11', 'Insertion')
)


REVENUE_TYPE_CHOICES = (
    ('-1', 'No Payment'),
    ('0', 'Flat CPM'),
    ('1', 'Cost Plus CPM'),
    ('2', 'Cost Plus Margin'),
    ('3', 'CPC'),
    ('4', 'CPA'),
    ('5', 'Revshare'),
    ('6', 'Flat Fee'),
    ('9', 'CPVM')
)


class AdQualityRule(models.Model):
    # https://wiki.appnexus.com/display/api/Ad+Quality+Rule+Service
    id = models.IntegerField(primary_key=True)  # No AutoIncrement
    fetch_date = models.DateTimeField(null=True, blank=True, db_index=True)
    code = models.TextField(null=True, blank=True, db_index=True)
    name = models.TextField(null=True, blank=True, db_index=True)
    description = models.TextField(null=True, blank=True)
    ad_profile = models.ForeignKey("AdProfile", null=True, blank=True)
    publisher = models.ForeignKey("Publisher", null=True, blank=True)
    member = models.ForeignKey("Member", null=True, blank=True)
    profile = models.ForeignKey("Profile", null=True, blank=True)
    priority = models.IntegerField(null=True, blank=True)
    last_modified = models.DateTimeField(default=now_tz)

    api_endpoint = 'ad-quality-rule'
    class Meta:
        db_table = "ad_quality_rule"


class NetworkAnalyticsReport(models.Model):
    #https://wiki.appnexus.com/display/api/Network+Analytics
    hour = models.DateTimeField(null=True, blank=True, db_index=True)
    entity_member = models.IntegerField(null=True, blank=True,
                                        db_index=True)  #target model depends on imp_type buyer_member or seller_member
    buyer_member = models.ForeignKey("PlatformMember", related_name='buyer_member_id', null=True, blank=True)
    seller_member = models.ForeignKey("PlatformMember", related_name='seller_member_id', null=True, blank=True)
    advertiser = models.ForeignKey("Advertiser", null=True, blank=True)
    adjustment_id = models.IntegerField(null=True, blank=True,
                                        db_index=True)  # TODO FK is needed in future - there is no description in documentation
    adjustment_hour = models.DateTimeField(null=True, blank=True)
    publisher = models.ForeignKey("Publisher", null=True, blank=True)
    pub_rule = models.ForeignKey("AdQualityRule", null=True, blank=True)
    site = models.ForeignKey("Site", null=True, blank=True)
    pixel = models.ForeignKey("ConversionPixel", null=True, blank=True)
    placement = models.ForeignKey("Placement", null=True, blank=True)
    insertion_order = models.ForeignKey("InsertionOrder", null=True, blank=True)
    line_item = models.ForeignKey("LineItem", null=True, blank=True)
    campaign = models.ForeignKey("Campaign", null=True, blank=True)
    creative = models.ForeignKey("Creative", null=True, blank=True)
    size = models.TextField(null=True, blank=True)
    brand = models.ForeignKey("Brand", null=True, blank=True)
    #brand_id = models.IntegerField(null=True, blank=True)
    billing_period_start_date = models.DateTimeField(null=True, blank=True, db_index=True)
    billing_period_end_date = models.DateTimeField(null=True, blank=True, db_index=True)
    geo_country = models.ForeignKey("Country", null=True, blank=True)
    inventory_class = models.TextField(null=True, blank=True)
    bid_type = models.TextField(
        choices=BID_TYPE_CHOICES,
        null=True, blank=True)
    imp_type_id = models.IntegerField(
        choices=IMPRESSION_TYPE_CHOICES,
        null=True, blank=True)
    buyer_type = models.TextField(
        choices=BUYER_TYPE_CHOICES,
        null=True, blank=True)
    seller_type = models.TextField(
        choices=SELLER_TYPE_CHOICES,
        null=True, blank=True)
    revenue_type_id = models.IntegerField(
        choices=REVENUE_TYPE_CHOICES,
        null=True, blank=True)
    supply_type = models.TextField(null=True, blank=True)
    payment_type = models.TextField(
        choices=DEAL_PAYMENT_TYPE_CHOICES,
        null=True, blank=True)
    deal = models.ForeignKey("Deal", null=True, blank=True)
    media_type = models.ForeignKey("MediaType", null=True, blank=True)
    salesperson_for_advertiser = models.TextField(null=True, blank=True)
    salesperson_for_publisher = models.TextField(null=True, blank=True)
    trafficker_for_line_item = models.TextField(null=True, blank=True)
    salesrep_for_line_item = models.TextField(null=True, blank=True)
    buying_currency = models.TextField(null=True, blank=True)
    selling_currency = models.TextField(null=True, blank=True)
    imps = models.IntegerField(null=True, blank=True)
    imps_blank = models.IntegerField(null=True, blank=True)
    imps_psa = models.IntegerField(null=True, blank=True)
    imps_psa_error = models.IntegerField(null=True, blank=True)
    imps_default_error = models.IntegerField(null=True, blank=True)
    imps_default_bidder = models.IntegerField(null=True, blank=True)
    imps_kept = models.IntegerField(null=True, blank=True)
    imps_resold = models.IntegerField(null=True, blank=True)
    imps_rtb = models.IntegerField(null=True, blank=True)
    external_impression = models.IntegerField(null=True, blank=True)
    clicks = models.IntegerField(null=True, blank=True)
    click_thru_pct = models.FloatField(null=True, blank=True)
    external_click = models.IntegerField(null=True, blank=True)
    cost = models.DecimalField(null=True, blank=True, max_digits=35, decimal_places=10)
    cost_including_fees = models.DecimalField(null=True, blank=True, max_digits=35, decimal_places=10)
    revenue = models.DecimalField(null=True, blank=True, max_digits=35, decimal_places=10)
    revenue_including_fees = models.DecimalField(null=True, blank=True, max_digits=35, decimal_places=10)
    booked_revenue = models.DecimalField(null=True, blank=True, max_digits=35, decimal_places=10)
    booked_revenue_adv_curr = models.DecimalField(null=True, blank=True, max_digits=35, decimal_places=10)
    reseller_revenue = models.DecimalField(null=True, blank=True, max_digits=35, decimal_places=10)
    profit = models.DecimalField(null=True, blank=True, max_digits=35, decimal_places=10)
    profit_including_fees = models.DecimalField(null=True, blank=True, max_digits=35, decimal_places=10)
    commissions = models.DecimalField(null=True, blank=True, max_digits=35, decimal_places=10)
    cpm = models.DecimalField(null=True, blank=True, max_digits=35, decimal_places=10)
    cpm_including_fees = models.DecimalField(null=True, blank=True, max_digits=35, decimal_places=10)
    post_click_convs = models.IntegerField(null=True, blank=True)
    post_click_revenue = models.DecimalField(null=True, blank=True, max_digits=35, decimal_places=10)
    post_view_convs = models.IntegerField(null=True, blank=True)
    post_view_revenue = models.DecimalField(null=True, blank=True, max_digits=35, decimal_places=10)
    total_convs = models.IntegerField(null=True, blank=True)
    convs_per_mm = models.FloatField(null=True, blank=True)
    convs_rate = models.FloatField(null=True, blank=True)
    ctr = models.FloatField(null=True, blank=True)
    rpm = models.DecimalField(null=True, blank=True, max_digits=35, decimal_places=10)
    rpm_including_fees = models.DecimalField(null=True, blank=True, max_digits=35, decimal_places=10)
    total_network_rpm = models.DecimalField(null=True, blank=True, max_digits=35, decimal_places=10)
    total_publisher_rpm = models.DecimalField(null=True, blank=True, max_digits=35, decimal_places=10)
    sold_network_rpm = models.FloatField(null=True, blank=True)
    sold_publisher_rpm = models.FloatField(null=True, blank=True)
    media_cost_pub_curr = models.DecimalField(null=True, blank=True, max_digits=35, decimal_places=10)
    ppm = models.DecimalField(null=True, blank=True, max_digits=35, decimal_places=10)
    ppm_including_fees = models.DecimalField(null=True, blank=True, max_digits=35, decimal_places=10)
    serving_fees = models.DecimalField(null=True, blank=True, max_digits=35, decimal_places=10)
    imps_viewed = models.IntegerField(null=True, blank=True)
    view_measured_imps = models.IntegerField(null=True, blank=True)
    view_rate = models.FloatField(null=True, blank=True)
    view_measurement_rate = models.FloatField(null=True, blank=True)
    cpvm = models.DecimalField(null=True, blank=True, max_digits=35, decimal_places=10)
    data_costs = models.DecimalField(null=True, blank=True, max_digits=35, decimal_places=10)
    revenue_buying_currency = models.DecimalField(null=True, blank=True, max_digits=35, decimal_places=10)
    revenue_selling_currency = models.DecimalField(null=True, blank=True, max_digits=35, decimal_places=10)
    booked_revenue_buying_currency = models.DecimalField(null=True, blank=True, max_digits=35, decimal_places=10)
    booked_revenue_selling_currency = models.DecimalField(null=True, blank=True, max_digits=35, decimal_places=10)
    reseller_revenue_buying_currency = models.DecimalField(null=True, blank=True, max_digits=35, decimal_places=10)
    reseller_revenue_selling_currency = models.DecimalField(null=True, blank=True, max_digits=35, decimal_places=10)
    cost_buying_currency = models.DecimalField(null=True, blank=True, max_digits=35, decimal_places=10)
    cost_selling_currency = models.DecimalField(null=True, blank=True, max_digits=35, decimal_places=10)
    profit_buying_currency = models.DecimalField(null=True, blank=True, max_digits=35, decimal_places=10)
    profit_selling_currency = models.DecimalField(null=True, blank=True, max_digits=35, decimal_places=10)
    total_network_rpm_buying_currency = models.DecimalField(null=True, blank=True, max_digits=35, decimal_places=10)
    total_network_rpm_selling_currency = models.DecimalField(null=True, blank=True, max_digits=35, decimal_places=10)
    cpm_buying_currency = models.DecimalField(null=True, blank=True, max_digits=35, decimal_places=10)
    cpm_selling_currency = models.DecimalField(null=True, blank=True, max_digits=35, decimal_places=10)
    rpm_buying_currency = models.DecimalField(null=True, blank=True, max_digits=35, decimal_places=10)
    rpm_selling_currency = models.DecimalField(null=True, blank=True, max_digits=35, decimal_places=10)
    ppm_buying_currency = models.DecimalField(null=True, blank=True, max_digits=35, decimal_places=10)
    ppm_selling_currency = models.DecimalField(null=True, blank=True, max_digits=35, decimal_places=10)
    sold_network_rpm_buying_currency = models.DecimalField(null=True, blank=True, max_digits=35, decimal_places=10)
    sold_network_rpm_selling_currency = models.DecimalField(null=True, blank=True, max_digits=35, decimal_places=10)
    commissions_buying_currency = models.DecimalField(null=True, blank=True, max_digits=35, decimal_places=10)
    commissions_selling_currency = models.DecimalField(null=True, blank=True, max_digits=35, decimal_places=10)
    serving_fees_buying_currency = models.DecimalField(null=True, blank=True, max_digits=35, decimal_places=10)
    serving_fees_selling_currency = models.DecimalField(null=True, blank=True, max_digits=35, decimal_places=10)
    data_costs_buying_currency = models.DecimalField(null=True, blank=True, max_digits=35, decimal_places=10)
    data_costs_selling_currency = models.DecimalField(null=True, blank=True, max_digits=35, decimal_places=10)

    api_report_name = "network_analytics"
    api_columns = [
        "hour",
        "advertiser_id",
        "advertiser_name",
        "campaign_id",
        "campaign_name",
        "creative_id",
        "creative_name",
        "geo_country",
        "insertion_order_id",
        "insertion_order_name",
        "line_item_id",
        "line_item_name",
        "site_id",
        "site_name",
        "placement_id",
        "placement_name",
        "publisher_id",
        "publisher_name",
        "imps",
        "clicks",
        "total_convs",
        "cost",
        "commissions",
        "serving_fees"
    ]


    class Meta:
        db_table = "network_analytics_report"
        index_together = ["advertiser", "hour"]
        index_together = ["publisher", "hour"]
        index_together = ["campaign", "hour"]


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
    deal = models.ForeignKey("Deal", null=True, blank=True)
    advertiser = models.ForeignKey("Advertiser", null=True, blank=True)
    #campaign_group = campaign_group is a synonymous with line_item .
    buyer_member = models.ForeignKey("Member", null=True, blank=True)
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
    class Meta:
        db_table = "site_domain_performance_report"
        index_together = [
            ("advertiser", "day"),
        ]
    #This function transform raw data, collected from csv, to value, saved into DB/
    def TransformFields1(self, data,  metadata={}):
        if not metadata: return
        campaign_dict = metadata["campaign_dict"]
        all_line_items = metadata["all_line_items"]
        #missed_campaigns = metadata["missed_campaigns"]
        #self.campaign = None
        text_in_parentheses = get_text_in_parentheses(data["campaign"])
        self.campaign_id = int(text_in_parentheses)
        #self.campaign = campaign_dict.get(self.campaign_id) #This also change self.campaign_id
        if self.campaign_id not in campaign_dict:
            #campaign_dict[self.campaign_id] = data["campaign"][:-len(text_in_parentheses)-2]
            campaign_dict[self.campaign_id] = data["campaign_name"]
            self.create_campaign(data["campaign_name"], metadata['advertiser_id'])
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
        if self.line_item_id not in all_line_items:
            self.line_item = None

    def TransformFields(self, data,  metadata={}):
        if not metadata: return
        campaign_dict = metadata["campaign_dict"]
        advertiser_id = metadata.get('advertiser_id', data.get('advertiser_id'))
        if self.campaign_id not in campaign_dict:
            campaign_dict[self.campaign_id] = data["campaign_name"]
            self.create_campaign(data["campaign_name"], advertiser_id)

    def create_campaign(self, campaign_name, advertiser_id):
        camp = Campaign()
        camp.id = self.campaign_id
        camp.fetch_date = self.fetch_date
        camp.state = "Inactive"
        camp.name = campaign_name
        camp.advertiser_id = advertiser_id
        camp.comments = "created automatically"
        camp.start_date = datetime.datetime(1970, 1, 1, tzinfo=utc)
        camp.last_modified = self.fetch_date
        try:
            camp.save()
        except IntegrityError as e:
            # Ignore 'duplicate key value' errors
            # Object created in other thread
            if e.message.find('duplicate key value') < 0: raise



class GeoAnaliticsReport(models.Model):
    # month = date  # Yes	The year and month in which the auction took place.
    fetch_date = models.DateTimeField(null=True, blank=True, db_index=True)
    day = models.DateField(null=True, blank=True, db_index=True)  # Yes	The year, month, and day in which the auction took place.
    member = models.ForeignKey("Member", null=True, blank=True) # Yes	The ID of the member.
    advertiser_currency = models.TextField(null=True, blank=True)  # Yes	The type of currency used by the advertiser.
    insertion_order = models.ForeignKey("InsertionOrder", null=True, blank=True)  # Yes	The insertion order ID.
    campaign = models.ForeignKey("Campaign", null=True, blank=True)  # Yes	The campaign ID.
    advertiser = models.ForeignKey("Advertiser", null=True, blank=True)  # Yes	The advertiser ID. If the value is 0, either the impression was purchased by an external buyer, or a default or PSA was shown. For more information on defaults and PSAs, see Network Reporting.
    line_item = models.ForeignKey("LineItem", null=True, blank=True)  # Yes	The line item ID.
    geo_country = models.ForeignKey("Country", null=True, blank=True)  # Yes	The country ID of the user's location as defined by the Country Service. 250 is shown in cases where we don't know the country or if the country doesn't map correctly to a location in our database.
    geo_region = models.ForeignKey("Region", null=True, blank=True)  # Yes	The region ID of the user's location as defined by the Region Service. 4291 is shown in cases where we don't know the region or if the region doesn't map correctly to a location in our database.
    geo_country_name = models.TextField(null=True, blank=True)  # No	The name of the user's country, as defined by the Country Service.
    geo_region_name = models.TextField(null=True, blank=True)  # No	The name of the region of the user's location as defined by the Region Service.
    geo_country = models.TextField(null=True, blank=True)  # No	The country name and code where the user is located, in the format "France (FR)". The string "250" can appear in cases where we don't know the country or if the country doesn't map correctly to a location in our database.
    geo_region = models.TextField(null=True, blank=True)  # No	The region name and country code of the users location, in the format "Bremen (DE)". The string "4192" can appear in cases where we don't know the region/state or if the region/state doesn't map correctly to a location in our database.
    geo_dma = models.ForeignKey("DemographicArea", null=True, blank=True) # No	The name and ID of the demographic area where the user is located, in the format "New York NY (501)". The string "unknown values (-1)" can appear in cases where we don't know the demographic area or if the demographic area doesn't map correctly to a location in our database.
    pixel = models.ForeignKey("ConversionPixel", null=True, blank=True)  # Yes The unique identification number of the conversion pixel.
    # pixel = models.ForeignKey("ConversionPixel",null=True, blank=True)
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

    class Meta:
        db_table = "geo_analytics_report"


class DeviceMake(models.Model):
    # https://wiki.appnexus.com/display/api/Device+Make+Service
    id = models.IntegerField(primary_key=True)  # No AutoIncrement
    name = models.TextField(null=True, blank=True, db_index=True)

    # codes = array - see model DeviceMakeCodes below

    class Meta:
        db_table = "device_make"


class DeviceMakeCodes(models.Model):
    # https://wiki.appnexus.com/display/api/Device+Make+Service
    id = models.IntegerField(primary_key=True)  # No AutoIncrement
    code = models.TextField(null=True, blank=True, db_index=True)
    notes = models.TextField(null=True, blank=True)
    device_make = models.ForeignKey("DeviceMake", null=True, blank=True)

    class Meta:
        db_table = "device_make_codes"


DEVICE_TYPE_CHOICES = (
    ('Phone', 'Phone'),
    ('Tablet', 'Tablet'),
    ('Other Devices', 'Other Devices')
)


class DeviceModel(models.Model):
    # https://wiki.appnexus.com/display/api/Device+Model+Service
    id = models.IntegerField(primary_key=True)  # No AutoIncrement
    name = models.TextField(null=True, blank=True, db_index=True)
    device_make = models.ForeignKey("DeviceMake", null=True, blank=True)
    device_type = models.TextField(
        choices=DEVICE_TYPE_CHOICES,
        null=True, blank=True)
    screen_width = models.IntegerField(null=True, blank=True)
    screen_height = models.IntegerField(null=True, blank=True)
    supports_js = models.IntegerField(null=True, blank=True)
    supports_cookies = models.IntegerField(null=True, blank=True)
    supports_flash = models.IntegerField(null=True, blank=True)
    supports_geo = models.IntegerField(null=True, blank=True)
    supports_html_video = models.IntegerField(null=True, blank=True)
    supports_html_audio = models.IntegerField(null=True, blank=True)

    # codes = array - see model DeviceMakeCodes below

    class Meta:
        db_table = "device_model"


class DeviceModelCodes(models.Model):
    # https://wiki.appnexus.com/display/api/Device+Model+Service
    id = models.IntegerField(primary_key=True)  # No AutoIncrement
    code = models.TextField(null=True, blank=True, db_index=True)
    notes = models.TextField(null=True, blank=True)
    device_model = models.ForeignKey("DeviceModel", null=True, blank=True)

    class Meta:
        db_table = "device_model_codes"


class Browser(models.Model):
    # https://wiki.appnexus.com/display/api/Browser+Service
    id = models.IntegerField(primary_key=True)  # No AutoIncrement
    name = models.TextField(null=True, blank=True, db_index=True)
    last_modified = models.DateTimeField(default=now_tz) 

    class Meta:
        db_table = "browser"


DEVICE_TYPE_INREPORT_CHOICES = (
    ('pc', 'pc'),
    ('phone', 'phone'),
    ('tablet', 'tablet')
)

BUYER_TYPE_NetworkDeviceReport_CHOICES = (
    ('Real Time', 'Real Time'),
    ('Direct', 'Direct')
)

SELLER_TYPE_NetworkDeviceReport_CHOICES = (
    ('Real Time', 'Real Time'),
    ('Direct', 'Direct')
)

CONNECTION_TYPE_CHOICES = (
    ('Carrier-based', 'Carrier-based'),
    ('Wifi or Static', 'Wifi or Static')
)


class NetworkDeviceReport(models.Model):
    # https://wiki.appnexus.com/display/api/Network+Device+Analytics
    fetch_date = models.DateTimeField(null=True, blank=True, db_index=True)
    # month = time
    day = models.DateTimeField(null=True, blank=True, db_index=True)
    device_make = models.ForeignKey("DeviceMake", null=True, blank=True)
    device_model = models.ForeignKey("DeviceModel", null=True, blank=True)
    device_type = models.TextField(
        choices=DEVICE_TYPE_INREPORT_CHOICES,
        null=True, blank=True)
    connection_type = models.TextField(
        choices=CONNECTION_TYPE_CHOICES,
        null=True, blank=True)
    operating_system = models.ForeignKey("OperatingSystem", null=True, blank=True)
    browser = models.ForeignKey("Browser", null=True, blank=True)
    entity_member = models.IntegerField(null=True, blank=True,
                                        db_index=True)  # target model depends on imp_type buyer_member or seller_member
    buyer_member = models.ForeignKey("PlatformMember", related_name='+', null=True, blank=True)
    seller_member = models.ForeignKey("PlatformMember", related_name='+', null=True, blank=True)
    buyer_type = models.TextField(
        choices=BUYER_TYPE_NetworkDeviceReport_CHOICES,
        null=True, blank=True)
    seller_type = models.TextField(
        choices=SELLER_TYPE_NetworkDeviceReport_CHOICES,
        null=True, blank=True)
    advertiser = models.ForeignKey("Advertiser", null=True, blank=True)
    insertion_order = models.ForeignKey("InsertionOrder", null=True, blank=True)
    line_item = models.ForeignKey("LineItem", null=True, blank=True)
    campaign = models.ForeignKey("Campaign", null=True, blank=True)
    pixel = models.ForeignKey("ConversionPixel", null=True, blank=True)
    media_type = models.ForeignKey("MediaType", null=True, blank=True)
    size = models.TextField(null=True, blank=True)
    geo_country = models.ForeignKey("Country", null=True, blank=True)
    payment_type = models.TextField(
        choices=DEAL_PAYMENT_TYPE_CHOICES,
        null=True, blank=True)
    revenue_type_id = models.IntegerField(
        choices=REVENUE_TYPE_CHOICES,
        null=True, blank=True)
    publisher = models.ForeignKey("Publisher", null=True, blank=True)
    pub_rule = models.ForeignKey("AdQualityRule", null=True, blank=True)
    bid_type = models.TextField(
        choices=BID_TYPE_CHOICES,
        null=True, blank=True)
    imp_type_id = models.IntegerField(
        choices=IMPRESSION_TYPE_CHOICES,
        null=True, blank=True)
    venue = models.TextField(null=True, blank=True, db_index=True)
    imps = models.IntegerField(null=True, blank=True)
    imps_blank = models.IntegerField(null=True, blank=True)
    imps_psa = models.IntegerField(null=True, blank=True)
    imps_default_error = models.IntegerField(null=True, blank=True)
    imps_default_bidder = models.IntegerField(null=True, blank=True)
    imps_kept = models.IntegerField(null=True, blank=True)
    imps_resold = models.IntegerField(null=True, blank=True)
    imps_rtb = models.IntegerField(null=True, blank=True)
    clicks = models.IntegerField(null=True, blank=True)
    click_thru_pct = models.FloatField(null=True, blank=True)
    ctr = models.FloatField(null=True, blank=True)
    total_convs = models.IntegerField(null=True, blank=True)
    post_view_convs = models.IntegerField(null=True, blank=True)
    post_click_convs = models.IntegerField(null=True, blank=True)
    convs_per_mm = models.FloatField(null=True, blank=True)
    convs_rate = models.FloatField(null=True, blank=True)
    cost = models.DecimalField(null=True, blank=True, max_digits=35, decimal_places=10)
    cpm = models.DecimalField(null=True, blank=True, max_digits=35, decimal_places=10)
    revenue = models.DecimalField(null=True, blank=True, max_digits=35, decimal_places=10)
    booked_revenue = models.DecimalField(null=True, blank=True, max_digits=35, decimal_places=10)
    reseller_revenue = models.DecimalField(null=True, blank=True, max_digits=35, decimal_places=10)
    rpm = models.DecimalField(null=True, blank=True, max_digits=35, decimal_places=10)
    profit = models.DecimalField(null=True, blank=True, max_digits=35, decimal_places=10)
    ppm = models.DecimalField(null=True, blank=True, max_digits=35, decimal_places=10)
    total_publisher_rpm = models.DecimalField(null=True, blank=True, max_digits=35, decimal_places=10)
    sold_publisher_rpm = models.FloatField(null=True, blank=True)
    sold_network_rpm = models.FloatField(null=True, blank=True)

    class Meta:
        db_table = "network_device_report"


class NetworkCarrierReport(models.Model):
    # https://wiki.appnexus.com/display/api/Network+Carrier+Analytics
    fetch_date = models.DateTimeField(null=True, blank=True, db_index=True)
    # month = time
    day = models.DateTimeField(null=True, blank=True, db_index=True)
    carrier_id = int
    device_type = models.TextField(
        choices=DEVICE_TYPE_INREPORT_CHOICES,
        null=True, blank=True)
    connection_type = models.TextField(
        choices=CONNECTION_TYPE_CHOICES,
        null=True, blank=True)
    entity_member = models.IntegerField(null=True, blank=True,
                                        db_index=True)  # target model depends on imp_type buyer_member or seller_member
    buyer_member = models.ForeignKey("PlatformMember", related_name='+', null=True, blank=True)
    seller_member = models.ForeignKey("PlatformMember", related_name='+', null=True, blank=True)
    buyer_type = models.TextField(
        choices=BUYER_TYPE_NetworkDeviceReport_CHOICES,
        null=True, blank=True)
    seller_type = models.TextField(
        choices=SELLER_TYPE_NetworkDeviceReport_CHOICES,
        null=True, blank=True)
    advertiser = models.ForeignKey("Advertiser", null=True, blank=True)
    insertion_order = models.ForeignKey("InsertionOrder", null=True, blank=True)
    line_item = models.ForeignKey("LineItem", null=True, blank=True)
    campaign = models.ForeignKey("Campaign", null=True, blank=True)
    pixel = models.ForeignKey("ConversionPixel", null=True, blank=True)
    media_type = models.ForeignKey("MediaType", null=True, blank=True)
    size = models.TextField(null=True, blank=True)
    geo_country = models.ForeignKey("Country", null=True, blank=True)
    payment_type = models.TextField(
        choices=DEAL_PAYMENT_TYPE_CHOICES,
        null=True, blank=True)
    revenue_type_id = models.IntegerField(
        choices=REVENUE_TYPE_CHOICES,
        null=True, blank=True)
    publisher = models.ForeignKey("Publisher", null=True, blank=True)
    pub_rule = models.ForeignKey("AdQualityRule", null=True, blank=True)
    bid_type = models.TextField(
        choices=BID_TYPE_CHOICES,
        null=True, blank=True)
    imp_type_id = models.IntegerField(
        choices=IMPRESSION_TYPE_CHOICES,
        null=True, blank=True)
    venue = models.TextField(null=True, blank=True, db_index=True)
    imps = models.IntegerField(null=True, blank=True)
    imps_blank = models.IntegerField(null=True, blank=True)
    imps_psa = models.IntegerField(null=True, blank=True)
    imps_default_error = models.IntegerField(null=True, blank=True)
    imps_default_bidder = models.IntegerField(null=True, blank=True)
    imps_kept = models.IntegerField(null=True, blank=True)
    imps_resold = models.IntegerField(null=True, blank=True)
    imps_rtb = models.IntegerField(null=True, blank=True)
    clicks = models.IntegerField(null=True, blank=True)
    click_thru_pct = models.FloatField(null=True, blank=True)
    ctr = models.FloatField(null=True, blank=True)
    total_convs = models.IntegerField(null=True, blank=True)
    post_view_convs = models.IntegerField(null=True, blank=True)
    post_click_convs = models.IntegerField(null=True, blank=True)
    convs_per_mm = models.FloatField(null=True, blank=True)
    convs_rate = models.FloatField(null=True, blank=True)
    cost = models.DecimalField(null=True, blank=True, max_digits=35, decimal_places=10)
    cpm = models.DecimalField(null=True, blank=True, max_digits=35, decimal_places=10)
    revenue = models.DecimalField(null=True, blank=True, max_digits=35, decimal_places=10)
    booked_revenue = models.DecimalField(null=True, blank=True, max_digits=35, decimal_places=10)
    reseller_revenue = models.DecimalField(null=True, blank=True, max_digits=35, decimal_places=10)
    rpm = models.DecimalField(null=True, blank=True, max_digits=35, decimal_places=10)
    profit = models.DecimalField(null=True, blank=True, max_digits=35, decimal_places=10)
    ppm = models.DecimalField(null=True, blank=True, max_digits=35, decimal_places=10)
    total_publisher_rpm = models.DecimalField(null=True, blank=True, max_digits=35, decimal_places=10)
    sold_publisher_rpm = models.FloatField(null=True, blank=True)
    sold_network_rpm = models.FloatField(null=True, blank=True)

    class Meta:
        db_table = "network_carrier_report"


OPTIMISATION_PHASE_CHOICES = (
    ('-2', 'No predict phase'),
    ('-1', 'Base predict phase'),
    ('0', 'Learn giveup'),
    ('1', 'Learn'),
    ('2', 'Throttled'),
    ('3', 'Optimized'),
    ('4', 'Biased'),
    ('5', 'Optimized 1'),
    ('8', 'Optimized giveup'),
    ('9', 'Base bid below giveup')
)


class NetworkAdvertiserAnalyticsReport(models.Model):
    # https://wiki.appnexus.com/display/api/Network+Advertiser+Analytics
    fetch_date = models.DateTimeField(null=True, blank=True, db_index=True)
    hour = models.DateTimeField(null=True, blank=True, db_index=True)
    #day = date
    #month = date
    buyer_member = models.ForeignKey("PlatformMember", related_name='+', null=True, blank=True)
    seller_member = models.ForeignKey("PlatformMember", related_name='+', null=True, blank=True)
    advertiser = models.ForeignKey("Advertiser", null=True, blank=True)
    campaign = models.ForeignKey("Campaign", null=True, blank=True)
    creative = models.ForeignKey("Creative", null=True, blank=True)
    site = models.ForeignKey("Site", null=True, blank=True)
    placement = models.ForeignKey("Placement", null=True, blank=True)
    deal = models.ForeignKey("Deal", null=True, blank=True)
    size = models.TextField(null=True, blank=True)
    geo_country = models.ForeignKey("Country", null=True, blank=True)
    insertion_order = models.ForeignKey("InsertionOrder", null=True, blank=True)
    billing_period_start_date = models.DateTimeField(null=True, blank=True, db_index=True)
    billing_period_end_date = models.DateTimeField(null=True, blank=True, db_index=True)
    payment_type = models.TextField(
        choices=DEAL_PAYMENT_TYPE_CHOICES,
        null=True, blank=True)
    line_item = models.ForeignKey("LineItem", null=True, blank=True)
    pixel = models.ForeignKey("ConversionPixel", null=True, blank=True)
    publisher = models.ForeignKey("Publisher", null=True, blank=True)
    imp_type_id = models.IntegerField(
        choices=IMPRESSION_TYPE_CHOICES,
        null=True, blank=True)
    bid_type = models.TextField(
        choices=BID_TYPE_CHOICES,
        null=True, blank=True)
    seller_type = models.TextField(
        choices=SELLER_TYPE_CHOICES,
        null=True, blank=True)
    media_type = models.ForeignKey("MediaType", null=True, blank=True)
    venue_id = models.IntegerField(null=True, blank=True)
    venue = models.TextField(null=True, blank=True)
    predict_type_rev = models.IntegerField(
        choices=OPTIMISATION_PHASE_CHOICES,
        null=True, blank=True)
    trafficker_for_line_item = models.TextField(null=True, blank=True)
    trafficker_for_insertion_order = models.TextField(null=True, blank=True)
    salesrep_for_line_item = models.TextField(null=True, blank=True)
    salesrep_for_insertion_order = models.TextField(null=True, blank=True)
    user_group_for_campaign = models.TextField(null=True, blank=True)
    adjustment_id = models.IntegerField(null=True, blank=True,
                                        db_index=True)  # TODO FK is needed in future - there is no description in documentation
    revenue_type_id = models.IntegerField(
        choices=REVENUE_TYPE_CHOICES,
        null=True, blank=True)
    imps = models.IntegerField(null=True, blank=True)
    clicks = models.IntegerField(null=True, blank=True)
    post_view_convs = models.IntegerField(null=True, blank=True)
    post_view_revenue = models.DecimalField(null=True, blank=True, max_digits=35, decimal_places=10)
    post_click_convs = models.IntegerField(null=True, blank=True)
    post_click_revenue = models.DecimalField(null=True, blank=True, max_digits=35, decimal_places=10)
    total_revenue = models.DecimalField(null=True, blank=True, max_digits=35, decimal_places=10)
    total_revenue_adv_curr = models.DecimalField(null=True, blank=True, max_digits=35, decimal_places=10)
    total_convs = models.IntegerField(null=True, blank=True)
    convs_rate = models.FloatField(null=True, blank=True)
    post_view_convs_rate = models.FloatField(null=True, blank=True)
    post_click_convs_rate = models.FloatField(null=True, blank=True)
    ctr = models.FloatField(null=True, blank=True)
    profit = models.DecimalField(null=True, blank=True, max_digits=35, decimal_places=10)
    click_convs_rate = models.FloatField(null=True, blank=True)
    advertiser_currency = models.TextField(null=True, blank=True, db_index=True)
    revenue_ecpm = models.DecimalField(null=True, blank=True, max_digits=35, decimal_places=10)
    revenue_ecpm_adv_curr = models.DecimalField(null=True, blank=True, max_digits=35, decimal_places=10)
    cost_ecpm = models.DecimalField(null=True, blank=True, max_digits=35, decimal_places=10)
    profit_ecpm = models.DecimalField(null=True, blank=True, max_digits=35, decimal_places=10)
    revenue_ecpc = models.DecimalField(null=True, blank=True, max_digits=35, decimal_places=10)
    revenue_ecpc_adv_curr = models.DecimalField(null=True, blank=True, max_digits=35, decimal_places=10)
    revenue_ecpa = models.DecimalField(null=True, blank=True, max_digits=35, decimal_places=10)
    revenue_ecpa_adv_curr = models.DecimalField(null=True, blank=True, max_digits=35, decimal_places=10)
    cost_ecpc = models.DecimalField(null=True, blank=True, max_digits=35, decimal_places=10)
    cost_ecpa = models.DecimalField(null=True, blank=True, max_digits=35, decimal_places=10)
    profit_margin = models.DecimalField(null=True, blank=True, max_digits=35, decimal_places=10)
    media_cost = models.DecimalField(null=True, blank=True, max_digits=35, decimal_places=10)
    convs_per_mm = models.FloatField(null=True, blank=True)
    click_thru_pct = models.FloatField(null=True, blank=True)
    commissions = models.DecimalField(null=True, blank=True, max_digits=35, decimal_places=10)
    serving_fees = models.DecimalField(null=True, blank=True, max_digits=35, decimal_places=10)
    profit_including_fees = models.DecimalField(null=True, blank=True, max_digits=35, decimal_places=10)
    total_revenue_including_fees = models.DecimalField(null=True, blank=True, max_digits=35, decimal_places=10)
    total_revenue_including_fees_adv_currency = models.DecimalField(null=True, blank=True, max_digits=35, decimal_places=10)
    revenue_ecpa_including_fees = models.DecimalField(null=True, blank=True, max_digits=35, decimal_places=10)
    revenue_ecpa_including_fees_adv_currency = models.DecimalField(null=True, blank=True, max_digits=35, decimal_places=10)
    revenue_ecpc_including_fees = models.DecimalField(null=True, blank=True, max_digits=35, decimal_places=10)
    revenue_ecpc_including_fees_adv_currency = models.DecimalField(null=True, blank=True, max_digits=35, decimal_places=10)
    revenue_ecpm_including_fees = models.DecimalField(null=True, blank=True, max_digits=35, decimal_places=10)
    revenue_ecpm_including_fees_adv_currency = models.DecimalField(null=True, blank=True, max_digits=35, decimal_places=10)
    cost_ecpa_including_fees = models.DecimalField(null=True, blank=True, max_digits=35, decimal_places=10)
    cost_ecpc_including_fees = models.DecimalField(null=True, blank=True, max_digits=35, decimal_places=10)
    cost_ecpm_including_fees = models.DecimalField(null=True, blank=True, max_digits=35, decimal_places=10)
    profit_net_including_fees = models.DecimalField(null=True, blank=True, max_digits=35, decimal_places=10)
    profit_ecpm_including_fees = models.DecimalField(null=True, blank=True, max_digits=35, decimal_places=10)
    profit_margin_including_fees = models.DecimalField(null=True, blank=True, max_digits=35, decimal_places=10)
    post_view_convs_pixel = models.IntegerField(null=True, blank=True)
    post_clicks_convs_pixel = models.IntegerField(null=True, blank=True)
    total_revenue_pixel = models.DecimalField(null=True, blank=True, max_digits=35, decimal_places=10)
    total_revenue_including_fees_pixel = models.DecimalField(null=True, blank=True, max_digits=35, decimal_places=10)
    imps_viewed = models.IntegerField(null=True, blank=True)
    view_measured_imps = models.IntegerField(null=True, blank=True)
    view_rate = models.FloatField(null=True, blank=True)
    view_measurement_rate = models.FloatField(null=True, blank=True)
    cost_ecpvm = models.DecimalField(null=True, blank=True, max_digits=35, decimal_places=10)

    class Meta:
        db_table = "network_advertiser_analytics_report"


class NetworkAnalyticsFeed(models.Model):
    # https://wiki.appnexus.com/display/api/Network+Analytics+Feed
    fetch_date = models.DateTimeField(null=True, blank=True, db_index=True)
    hour = models.DateTimeField(null=True, blank=True, db_index=True)
    day = models.DateTimeField(null=True, blank=True, db_index=True)
    month = models.DateTimeField(null=True, blank=True, db_index=True)
    advertiser = models.ForeignKey("Advertiser", null=True, blank=True)
    bid_type = models.TextField(
        choices=BID_TYPE_CHOICES,
        null=True, blank=True)
    buyer_member = models.ForeignKey("PlatformMember", related_name='+', null=True, blank=True)
    campaign = models.ForeignKey("Campaign", null=True, blank=True)
    creative = models.ForeignKey("Creative", null=True, blank=True)
    deal = models.ForeignKey("Deal", null=True, blank=True)
    entity_member =  models.ForeignKey("Member", related_name='+', null=True, blank=True)
    external_inv = models.ForeignKey("PublisherExternalInventoryCode", null=True, blank=True)
    geo_country = models.ForeignKey("Country", null=True, blank=True)
    height = models.IntegerField(null=True, blank=True)
    imp_type_id = models.IntegerField(
        choices=IMPRESSION_TYPE_CHOICES,
        null=True, blank=True)
    insertion_order = models.ForeignKey("InsertionOrder", null=True, blank=True)
    insertion_order_code = models.IntegerField(null=True, blank=True)
    line_item = models.ForeignKey("LineItem", null=True, blank=True)
    line_item_code = models.IntegerField(null=True, blank=True)
    media_type = models.ForeignKey("MediaType", null=True, blank=True)
    media_subtype = models.ForeignKey("MediaSubType", null=True, blank=True)
    pixel = models.ForeignKey("ConversionPixel", null=True, blank=True)
    placement = models.ForeignKey("Placement", null=True, blank=True)
    publisher = models.ForeignKey("Publisher", null=True, blank=True)
    pub_rule = models.ForeignKey("AdQualityRule", null=True, blank=True)
    seller_member = models.ForeignKey("PlatformMember", related_name='+', null=True, blank=True)
    site = models.ForeignKey("Site", null=True, blank=True)
    size = models.TextField(null=True, blank=True)
    width = models.IntegerField(null=True, blank=True)
    payment_type = models.TextField(
        choices=DEAL_PAYMENT_TYPE_CHOICES,
        null=True, blank=True)
    revenue_type_id = models.IntegerField(
        choices=REVENUE_TYPE_CHOICES,
        null=True, blank=True)
    booked_revenue = models.DecimalField(null=True, blank=True, max_digits=35, decimal_places=10)
    booked_revenue_adv_curr = models.DecimalField(null=True, blank=True, max_digits=35, decimal_places=10)
    clicks = models.IntegerField(null=True, blank=True)
    commissions = models.DecimalField(null=True, blank=True, max_digits=35, decimal_places=10)
    imps = models.IntegerField(null=True, blank=True)
    media_cost = models.DecimalField(null=True, blank=True, max_digits=35, decimal_places=10)
    media_cost_pub_curr = models.DecimalField(null=True, blank=True, max_digits=35, decimal_places=10)
    network_advertiser_rpm = models.DecimalField(null=True, blank=True, max_digits=35, decimal_places=10)
    network_advertiser_rpm_adv_curr = models.DecimalField(null=True, blank=True, max_digits=35, decimal_places=10)
    network_resold_rpm = models.FloatField(null=True, blank=True)
    post_click_convs = models.IntegerField(null=True, blank=True)
    post_click_revenue = models.DecimalField(null=True, blank=True, max_digits=35, decimal_places=10)
    post_view_convs = models.IntegerField(null=True, blank=True)
    post_view_revenue = models.DecimalField(null=True, blank=True, max_digits=35, decimal_places=10)
    ppm = models.DecimalField(null=True, blank=True, max_digits=35, decimal_places=10)
    profit = models.DecimalField(null=True, blank=True, max_digits=35, decimal_places=10)
    publisher_rpm_publisher_currency = models.DecimalField(null=True, blank=True, max_digits=35, decimal_places=10)
    reseller_revenue = models.DecimalField(null=True, blank=True, max_digits=35, decimal_places=10)
    revenue = models.DecimalField(null=True, blank=True, max_digits=35, decimal_places=10)
    revenue_adv_curr = models.DecimalField(null=True, blank=True, max_digits=35, decimal_places=10)
    rpm_adv_curr = models.FloatField(null=True, blank=True)
    serving_fees = models.DecimalField(null=True, blank=True, max_digits=35, decimal_places=10)
    total_convs = models.IntegerField(null=True, blank=True)
    total_network_rpm = models.DecimalField(null=True, blank=True, max_digits=35, decimal_places=10)
    total_publisher_rpm = models.FloatField(null=True, blank=True)
    imps_viewed = models.IntegerField(null=True, blank=True)
    view_measured_imps = models.IntegerField(null=True, blank=True)
    view_rate = models.FloatField(null=True, blank=True)
    view_measurement_rate = models.FloatField(null=True, blank=True)

    class Meta:
        db_table = "network_analytics_feed"


class ClickTrackerPublisher(models.Model):
    click_tracker = models.ForeignKey("ClickTracker", null=True, blank=True)
    publisher = models.ForeignKey("Publisher", null=True, blank=True)

    class Meta:
        db_table = "click_tracker_publisher"


class ClickTrackerLineItem(models.Model):
    click_tracker = models.ForeignKey("ClickTracker", null=True, blank=True)
    line_item = models.ForeignKey("LineItem", null=True, blank=True)

    class Meta:
        db_table = "click_tracker_line_item"


class ClickTrackerPaymentRule(models.Model):
    click_tracker = models.ForeignKey("ClickTracker", null=True, blank=True)
    payment_rule= models.ForeignKey("PaymentRule", null=True, blank=True)

    class Meta:
        db_table = "click_tracker_payment_rule"


class ClickTrackerFeed(models.Model):
    # https://wiki.appnexus.com/display/api/Clicktrackers+Feed
    fetch_date = models.DateTimeField(null=True, blank=True, db_index=True)
    hour = models.DateTimeField(null=True, blank=True, db_index=True)
    day = models.DateTimeField(null=True, blank=True, db_index=True)
    month = models.DateTimeField(null=True, blank=True, db_index=True)
    datetime = models.DateTimeField(null=True, blank=True, db_index=True)
    advertiser = models.ForeignKey("Advertiser", null=True, blank=True)
    auction_id = models.BigIntegerField(null=True, blank=True)
    line_item = models.ForeignKey("LineItem", null=True, blank=True)
    insertion_order = models.ForeignKey("InsertionOrder", null=True, blank=True)
    member = models.ForeignKey("Member", null=True, blank=True)
    pricing_type = models.TextField(
        choices=PRICING_TYPE_CHOICES,
        null=True, blank=True)
    publisher = models.ForeignKey("Publisher", null=True, blank=True)
    site_domain = models.TextField(null=True, blank=True, db_index=True)
    tag = models.ForeignKey("Placement", null=True, blank=True)
    tracker = models.ForeignKey("ClickTracker", null=True, blank=True)
    user = models.ForeignKey("User", null=True, blank=True)
    commission_cpm = models.DecimalField(null=True, blank=True, max_digits=35, decimal_places=10)
    commission_revshare = models.DecimalField(null=True, blank=True, max_digits=35, decimal_places=10)
    media_buy_cost = models.DecimalField(null=True, blank=True, max_digits=35, decimal_places=10)
    media_buy_rev_share_pct = models.FloatField(null=True, blank=True)
    revenue_value = models.DecimalField(null=True, blank=True, max_digits=35, decimal_places=10)

    class Meta:
        db_table = "click_tracker_feed"

