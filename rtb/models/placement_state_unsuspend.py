from django.db import models
from django.contrib.postgres.fields import JSONField

class PlacementStateUnsuspend(models.Model):
    id = models.AutoField(primary_key=True)
    campaign = models.ForeignKey("Campaign", null=True, blank=True, db_constraint=False, on_delete=models.DO_NOTHING)
    placement = models.ForeignKey("Placement", null=True, blank=True, db_constraint=False, on_delete=models.DO_NOTHING)
    # simple grid data
    spent = models.DecimalField(null=True, blank=True, max_digits=35, decimal_places=10)
    conversions = models.IntegerField(null=True)
    imps = models.IntegerField(null=True)
    clicks = models.IntegerField(null=True)
    cpa = models.DecimalField(null=True, blank=True, max_digits=35, decimal_places=10)
    cpc = models.DecimalField(null=True, blank=True, max_digits=35, decimal_places=10)
    cpm = models.DecimalField(null=True, blank=True, max_digits=35, decimal_places=10)
    cvr = models.DecimalField(null=True, blank=True, max_digits=35, decimal_places=10)
    ctr = models.FloatField(null=True, blank=True)
    imps_viewed = models.IntegerField(null=True, blank=True)
    view_measured_imps = models.IntegerField(null=True, blank=True)
    view_measurement_rate = models.FloatField(null=True, blank=True)
    view_rate = models.FloatField(null=True, blank=True)

    class Meta:
        db_table = "placement_state_unsuspend"
        unique_together = (('campaign', 'placement'),)

