from django.db import models


class PlacementState(models.Model):

    id = models.AutoField(primary_key=True)
    campaign = models.ForeignKey("Campaign", db_constraint=False, on_delete=models.DO_NOTHING)
    placement = models.ForeignKey("Placement", db_constraint=False, on_delete=models.DO_NOTHING)
    state = models.TextField(null=True, blank=True)
    suspend = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = "placement_state"
