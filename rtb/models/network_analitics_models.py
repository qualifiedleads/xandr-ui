from django.db import models

class NetworkAnalyticsReport_ByPlacement(models.Model):
    hour = models.DateTimeField(null=True, blank=True, db_index=True)
    placement = models.ForeignKey("Placement", null=True, blank=True, db_constraint=False, on_delete = models.DO_NOTHING)
    campaign = models.ForeignKey("Campaign", null=True, blank=True, db_constraint=False, on_delete = models.DO_NOTHING)
    imps = models.IntegerField(null=True, blank=True)
    clicks = models.IntegerField(null=True, blank=True)
    cost = models.DecimalField(null=True, blank=True, max_digits=35, decimal_places=10)
    total_convs = models.IntegerField(null=True, blank=True)

    api_report_name = "network_analytics"

    class Meta:
        app_label = 'rtb'
        db_table = "network_analytics_report_by_placement"
        index_together = ["campaign", "hour"]
