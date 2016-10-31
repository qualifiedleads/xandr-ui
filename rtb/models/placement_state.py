from django.db import models
from django.contrib.postgres.fields import JSONField

class PlacementState(models.Model):

    id = models.AutoField(primary_key=True)
    campaign = models.ForeignKey("Campaign", db_constraint=False, db_index=True, on_delete=models.DO_NOTHING)
    placement = models.ForeignKey("Placement", db_constraint=False, db_index=True, on_delete=models.DO_NOTHING)
    state = models.IntegerField(null=True, blank=True)  # 4 - white / 2 - black / 1 - suspend
    suspend = models.DateTimeField(null=True, blank=True)
    change = models.BooleanField(default=False)

    class Meta:
        db_table = "placement_state"

class CampaignRules(models.Model):
    id = models.AutoField(primary_key=True)
    campaign = models.ForeignKey("Campaign", db_constraint=False, db_index=True, on_delete=models.DO_NOTHING, unique=True)
    rules = JSONField()

    class Meta:
        db_table = "campaign_rules"

class LastModified(models.Model):
    id = models.AutoField(primary_key=True)
    type = models.TextField(null=True, blank=True)
    date = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = "last_modified"
