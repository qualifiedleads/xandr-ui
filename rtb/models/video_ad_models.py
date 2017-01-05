from django.db import models

class VideoAdCampaigns(models.Model):
    id = models.AutoField(primary_key=True)
    advertiser_id = models.IntegerField(db_index=True)
    campaign_id = models.IntegerField(db_index=True)
    date = models.DateTimeField(db_index=True)
    imp_hour = models.IntegerField()
    ad_starts_hour = models.IntegerField()
    spent_hour = models.DecimalField(max_digits=35, decimal_places=10)
    cpm_hour = models.DecimalField(max_digits=35, decimal_places=10)
    spent_cpm_hour = models.DecimalField(null=True, max_digits=35, decimal_places=10)
    bid_hour = models.DecimalField(null=True, max_digits=35, decimal_places=10)
    cpvm_hour = models.DecimalField(null=True, max_digits=35, decimal_places=10)
    spent_cpvm_hour = models.DecimalField(null=True, max_digits=35, decimal_places=10)
    fill_rate_hour = models.DecimalField(max_digits=35, decimal_places=10)
    profit_loss_hour = models.DecimalField(max_digits=35, decimal_places=10)

    class Meta:
        db_table = "video_ad_campaigns"