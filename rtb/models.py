import datetime

from django.db import models


class UserType(models.Model):
    description = models.CharField(max_length=80)

    class Meta:
        db_table = "user_type"


class User(models.Model):
    is_active = models.BooleanField()
    username = models.CharField(max_length=80)
    email = models.CharField(max_length=80)
    first_name = models.CharField(max_length=80)
    last_name = models.CharField(max_length=80)
    password = models.CharField(max_length=200)
    date_added = models.DateTimeField(default=datetime.datetime.now)

    user_type = models.ForeignKey('UserType', null=True, blank=True)

    class Meta:
        db_table = "user"


class Category(models.Model):
    name = models.CharField(max_length=80)
    is_sensitive = models.BooleanField()
    requires_whitelist = models.BooleanField()
    requires_whitelist_on_external = models.BooleanField()
    last_modified = models.DateTimeField()
    is_brand_eligible = models.BooleanField()

    class Meta:
        db_table = "category"


class Brand(models.Model):
    name = models.CharField(max_length=80)
    urls = models.CharField(max_length=80)
    is_premium = models.BooleanField()
    category = models.ForeignKey("Category")
    company_id = models.IntegerField()
    num_creatives = models.IntegerField()
    last_modified = models.DateTimeField()


class Country(models.Model):
    name = models.CharField(max_length=80)
    code = models.CharField(max_length=80)


class BrandInCountry(models.Model):
    brand = models.ForeignKey("Brand")
    category = models.ForeignKey("Category")


STATE_CHOICES = (
    ('ACTIVE', 'Active'),
    ('INACTIVE', 'Inactive'),
)

TIME_FORMAT_CHOICES = (
    ('12', '12-Hour'),
    ('24', '24-Hour'),
)


class Advertiser(models.Model):
    code = models.CharField(max_length=80)
    name = models.CharField(max_length=80)
    state = models.CharField(
        max_length=80,
        choices=STATE_CHOICES,
        default="ACTIVE")
    default_brand_id = models.IntegerField()
    remarketing_segment_id = models.IntegerField()
    lifetime_budget = models.FloatField()
    lifetime_budget_imps = models.IntegerField()
    daily_budget = models.FloatField()
    daily_budget_imps = models.IntegerField()
    enable_pacing = models.BooleanField()
    allow_safety_pacing = models.BooleanField()
    profile_id = models.IntegerField()
    control_pct = models.FloatField()
    timezone = models.CharField(max_length=80)
    last_modified = models.DateTimeField()
    billing_name = models.CharField(max_length=200)
    billing_phone = models.CharField(max_length=200)
    billing_address1 = models.CharField(max_length=200)
    billing_address2 = models.CharField(max_length=200)
    billing_city = models.CharField(max_length=200)
    billing_state = models.CharField(max_length=200)
    billing_country = models.CharField(max_length=200)
    billing_zip = models.CharField(max_length=200)
    default_currency = models.CharField(max_length=200)
    default_category = models.CharField(max_length=200)
    use_insertion_orders = models.BooleanField()

    time_format = models.CharField(
        max_length=80,
        choices=TIME_FORMAT_CHOICES,
        default="12")

    is_mediated = models.BooleanField
    is_malicious = models.BooleanField


class AdvertiserBrand(models.Model):
    advertiser = models.ForeignKey("Advertiser")
    brand = models.ForeignKey("Brand")


class AdvertiserCategory(models.Model):
    advertiser = models.ForeignKey("Advertiser")
    category = models.ForeignKey("Category")


class AdvertiserLabel(models.Model):
    advertiser = models.ForeignKey("Advertiser")
    name = models.CharField(max_length=200)
    value = models.CharField(max_length=200)


class AdvertiserThirdpartyPixel(models.Model):
    advertiser = models.ForeignKey("Advertiser")


class ThirdPartyPixel(models.Model):
    is_active = models.BooleanField()
    name = models.CharField(max_length=200)


class NetworkAnalyticsRaw(models.Model):
    json = models.TextField(null=True, blank=True)
    csv = models.TextField(null=True, blank=True)
    report_type = models.CharField(max_length=50, null=True, blank=True)
    report_id = models.CharField(max_length=100, null=True, blank=True)
    last_updated = models.DateTimeField(default=datetime.datetime.now)

    class Meta:
        db_table = "network_analytics_raw"

    def __unicode__(self):
        return self.id


class NetworkAnalyticsReport(models.Model):
    hour = models.DateTimeField()
    entity_member_id = models.IntegerField()
    buyer_member_id = models.IntegerField()
    seller_member_id = models.IntegerField()
    advertiser_id = models.IntegerField()
    adjustment_id = models.IntegerField()
    publisher_id = models.IntegerField()
    pub_rule_id = models.IntegerField()
    site_id = models.IntegerField()
    pixel_id = models.IntegerField()
    placement_id = models.IntegerField()
    insertion_order_id = models.IntegerField()
    line_item_id = models.IntegerField()
    campaign_id = models.IntegerField()
    creative_id = models.IntegerField()
    size = models.CharField(max_length=200)
    brand_id = models.IntegerField()
    billing_period_start_date = models.DateTimeField()
    billing_period_end_date = models.DateTimeField()
    geo_country = models.CharField(max_length=200)
    inventory_class = models.CharField(max_length=200)
    bid_type = models.CharField(max_length=200)
    imp_type_id = models.IntegerField()
    buyer_type = models.CharField(max_length=200)
    seller_type = models.CharField(max_length=200)
    revenue_type_id = models.IntegerField()

    supply_type = models.CharField(max_length=200)
    payment_type = models.CharField(max_length=200)
    deal_id = models.IntegerField()
    media_type_id = models.IntegerField()
