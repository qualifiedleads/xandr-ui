from django.db import models


class RtbImpressionTracker(models.Model):
    id = models.AutoField(primary_key=True, db_index=True)
    LocationsOrigins = models.TextField(null=True, blank=True)
    UserCountry = models.TextField(null=True, blank=True)
    SessionFreq = models.TextField(null=True, blank=True)
    PricePaid = models.TextField(null=True, blank=True)
    AdvFreq = models.TextField(null=True, blank=True)
    UserState = models.TextField(null=True, blank=True)
    CpgId = models.TextField(null=True, blank=True)
    CustomModelLastModified = models.TextField(null=True, blank=True)
    UserId = models.TextField(null=True, blank=True)
    XRealIp = models.TextField(null=True, blank=True)
    BidPrice = models.TextField(null=True, blank=True)
    SegIds = models.TextField(null=True, blank=True)
    UserAgent = models.TextField(null=True, blank=True)
    AuctionId = models.TextField(null=True, blank=True)
    RemUser = models.TextField(null=True, blank=True)
    CpId = models.TextField(null=True, blank=True)
    UserCity = models.TextField(null=True, blank=True)
    Age = models.TextField(null=True, blank=True)
    ReservePrice = models.TextField(null=True, blank=True)
    CacheBuster = models.TextField(null=True, blank=True)
    Ecp = models.TextField(null=True, blank=True)
    CustomModelId = models.TextField(null=True, blank=True)
    PlacementId = models.TextField(null=True, blank=True, db_index=True)
    SeqCodes = models.TextField(null=True, blank=True)
    CustomModelLeafName = models.TextField(null=True, blank=True)
    XForwardedFor = models.TextField(null=True, blank=True)
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
