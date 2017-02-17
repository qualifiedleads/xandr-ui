from django.db import models

class MLVideoImpsTracker(models.Model):
    id = models.AutoField(primary_key=True)
    # same fields
    CpId = models.IntegerField(null=True, blank=True, db_index=True)
    AdvId = models.IntegerField(null=True, blank=True, db_index=True)
    CreativeId = models.IntegerField(null=True, blank=True)
    AuctionId = models.BigIntegerField(null=True, blank=True)
    Date = models.DateTimeField(null=True, blank=True, db_index=True)
    # impressions fields
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
    RemUser = models.IntegerField(null=True, blank=True)
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
    # video fields
    cpvm = models.DecimalField(null=True, max_digits=35, decimal_places=10)
    # type
    is_imp = models.BooleanField(db_index=True)

    class Meta:
        db_table = "ml_video_imps_tracker"

class MLVideoAdCampaignsModelsInfo(models.Model):
    id = models.AutoField(primary_key=True)
    campaign = models.ForeignKey("Campaign", null=True, blank=True, db_constraint=False, on_delete=models.DO_NOTHING)
    start = models.DateTimeField(db_index=True)
    finish = models.DateTimeField(db_index=True)
    evaluation_date = models.DateTimeField(db_index=True)
    path = models.TextField()
    type = models.TextField()
    score = models.DecimalField(null=True, max_digits=35, decimal_places=10)

    class Meta:
        db_table = "ml_video_ad_campaigns_models_info"
        unique_together = (('campaign', 'type'),)


class MLVideoAdCampaignsModels(models.Model):
    id = models.AutoField(primary_key=True)
    advertiser = models.ForeignKey("Advertiser", null=True, blank=True, db_constraint=False, on_delete=models.DO_NOTHING)
    campaign = models.ForeignKey("Campaign", null=True, blank=True, db_constraint=False, on_delete=models.DO_NOTHING, unique=True)
    path = models.TextField()
    type = models.TextField()

    class Meta:
        db_table = "ml_video_ad_campaigns_models"

class MLVideoAdCampaignsResults(models.Model):
    id = models.AutoField(primary_key=True)
    advertiser = models.ForeignKey("Advertiser", null=True, blank=True, db_constraint=False,on_delete=models.DO_NOTHING)
    campaign = models.ForeignKey("Campaign", null=True, blank=True, db_constraint=False, on_delete=models.DO_NOTHING)
    res_date = models.DateTimeField(null=True)
    type = models.TextField()
    fill_rate = models.DecimalField(max_digits=35, decimal_places=10)
    cpm = models.DecimalField(max_digits=35, decimal_places=10)
    profit_loss = models.DecimalField(null=True, max_digits=35, decimal_places=10)

    class Meta:
        db_table = "ml_video_ad_campaigns_results"