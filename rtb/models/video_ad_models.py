from django.db import models

class VideoAdCampaigns(models.Model):
    id = models.AutoField(primary_key=True)
    advertiser = models.ForeignKey("Advertiser", null=True, blank=True, db_constraint=False, on_delete = models.DO_NOTHING)
    campaign = models.ForeignKey("Campaign", null=True, blank=True, db_constraint=False, on_delete = models.DO_NOTHING)
    campaign_name = models.TextField(null=True, blank=True)
    date = models.DateTimeField(db_index=True)
    hour = models.DateTimeField(db_index=True, null=True)
    imp_hour = models.IntegerField(null=True)
    ad_starts_hour = models.IntegerField(null=True)
    spent_hour = models.DecimalField(null=True, max_digits=35, decimal_places=10)
    cpm_hour = models.DecimalField(null=True, max_digits=35, decimal_places=10)
    spent_cpm_hour = models.DecimalField(null=True, max_digits=35, decimal_places=10)
    bid_hour = models.DecimalField(null=True, max_digits=35, decimal_places=10)
    cpvm_hour = models.DecimalField(null=True, max_digits=35, decimal_places=10)
    spent_cpvm_hour = models.DecimalField(null=True, max_digits=35, decimal_places=10)
    fill_rate_hour = models.DecimalField(null=True, max_digits=35, decimal_places=10)
    profit_loss_hour = models.DecimalField(null=True, max_digits=35, decimal_places=10)

    class Meta:
        db_table = "video_ad_campaigns"