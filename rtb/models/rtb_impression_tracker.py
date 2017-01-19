from django.db import models


class RtbImpressionTracker(models.Model):
    id = models.AutoField(primary_key=True, db_index=True)
    LocationsOrigins = models.TextField(null=True, blank=True)
    UserCountry = models.TextField(null=True, blank=True)
    SessionFreq = models.TextField(null=True, blank=True)
    PricePaid = models.DecimalField(null=True, max_digits=35, decimal_places=10)
    AdvFreq = models.TextField(null=True, blank=True)
    UserState = models.TextField(null=True, blank=True)
    CpgId = models.IntegerField(null=True, blank=True)
    CustomModelLastModified = models.TextField(null=True, blank=True)
    UserId = models.BigIntegerField(null=True, blank=True)
    XRealIp = models.TextField(null=True, blank=True)
    BidPrice = models.DecimalField(null=True, max_digits=35, decimal_places=10)
    SegIds = models.IntegerField(null=True, blank=True)
    UserAgent = models.TextField(null=True, blank=True)
    AuctionId = models.BigIntegerField(null=True, blank=True)
    RemUser = models.IntegerField(null=True, blank=True)
    CpId = models.IntegerField(null=True, blank=True)
    UserCity = models.TextField(null=True, blank=True)
    Age = models.IntegerField(null=True, blank=True)
    ReservePrice = models.DecimalField(null=True, max_digits=35, decimal_places=10)
    CacheBuster = models.IntegerField(null=True, blank=True)
    Ecp = models.DecimalField(null=True, max_digits=35, decimal_places=10)
    CustomModelId = models.IntegerField(null=True, blank=True)
    PlacementId = models.IntegerField(null=True, blank=True, db_index=True)
    SeqCodes = models.TextField(null=True, blank=True)
    CustomModelLeafName = models.TextField(null=True, blank=True)
    XForwardedFor = models.TextField(null=True, blank=True)
    CreativeId = models.IntegerField(null=True, blank=True)
    AdvId = models.IntegerField(null=True, blank=True)
    Date = models.DateTimeField(null=True, blank=True, db_index=True)

    class Meta:
        db_table = "rtb_impression_tracker"


class RtbImpressionTrackerPlacement(models.Model):

    id = models.AutoField(primary_key=True)
    placement = models.ForeignKey("Placement", db_constraint=False, on_delete = models.DO_NOTHING)
    domain = models.TextField(null=True, blank=True, db_index=True)

    class Meta:
        db_table = "rtb_impression_tracker_placement"
        unique_together = (('placement', 'domain'),)


class RtbImpressionTrackerPlacementDomain(models.Model):

    id = models.AutoField(primary_key=True)
    placement = models.ForeignKey("Placement", db_constraint=False, on_delete = models.DO_NOTHING, unique=True)
    domain = models.TextField(null=True, blank=True, db_index=True)

    class Meta:
        db_table = "rtb_impression_tracker_placement_domain"


class RtbDomainTracker(models.Model):
    id = models.AutoField(primary_key=True)
    placement = models.ForeignKey("Placement", db_constraint=False, on_delete=models.DO_NOTHING)
    domain = models.TextField(null=True, blank=True, db_index=True)
    auctionid = models.BigIntegerField(null=True, blank=True, db_index=True)
    userid = models.BigIntegerField(null=True, blank=True)
    advid = models.IntegerField(null=True, blank=True)
    Date = models.DateTimeField(null=True, blank=True, db_index=True)

    class Meta:
        db_table = "rtb_domain_tracker"


class RtbClickTracker(models.Model):
    id = models.AutoField(primary_key=True, db_index=True)
    CpId = models.IntegerField(null=True, blank=True, db_index=True)
    AdvId = models.IntegerField(null=True, blank=True, db_index=True)
    CreativeId = models.IntegerField(null=True, blank=True)
    AuctionId = models.BigIntegerField(null=True, blank=True)
    Date = models.DateTimeField(null=True, blank=True, db_index=True)

    class Meta:
        db_table = "rtb_click_tracker"


class RtbConversionTracker(models.Model):
    id = models.AutoField(primary_key=True, db_index=True)
    CpId = models.IntegerField(null=True, blank=True, db_index=True)
    AdvId = models.IntegerField(null=True, blank=True, db_index=True)
    CreativeId = models.IntegerField(null=True, blank=True)
    AuctionId = models.BigIntegerField(null=True, blank=True)
    Date = models.DateTimeField(null=True, blank=True, db_index=True)

    class Meta:
        db_table = "rtb_conversion_tracker"


class RtbAdStartTracker(models.Model):
    id = models.AutoField(primary_key=True, db_index=True)
    CpId = models.IntegerField(null=True, blank=True, db_index=True)
    AdvId = models.IntegerField(null=True, blank=True, db_index=True)
    CreativeId = models.IntegerField(null=True, blank=True)
    AuctionId = models.BigIntegerField(null=True, blank=True)
    cpvm = models.DecimalField(null=True, max_digits=35, decimal_places=10)
    Date = models.DateTimeField(null=True, blank=True, db_index=True)

    class Meta:
        db_table = "rtb_adstart_tracker"

