__author__ = 'USER'
from django.db import models
from django.contrib.postgres.fields import ArrayField

class MLPlacementDailyFeatures(models.Model):
    id = models.AutoField(primary_key=True)
    placement = models.ForeignKey("Placement", db_constraint=False, on_delete = models.DO_NOTHING)
    day = models.IntegerField(db_index=True)
    imps = models.IntegerField()
    clicks = models.IntegerField()
    total_convs = models.IntegerField()
    imps_viewed = models.IntegerField()
    view_measured_imps = models.IntegerField()
    cost = models.DecimalField(max_digits=35, decimal_places=10)
    view_rate = models.FloatField(db_index=True)
    view_measurement_rate = models.FloatField(db_index=True)
    cpa = models.FloatField()
    ctr = models.FloatField(db_index=True)
    cvr = models.DecimalField(null=True, max_digits=35, decimal_places=10)
    cpc = models.DecimalField(null=True, max_digits=35, decimal_places=10)
    cpm = models.DecimalField(null=True, max_digits=35, decimal_places=10)

    class Meta:
        db_table = "ml_placement_daily_features"
        unique_together = (('placement', 'day'),)


class MLPlacementsClustersKmeans(models.Model):
    id = models.AutoField(primary_key=True)
    placement = models.ForeignKey("Placement", db_constraint=False, on_delete = models.DO_NOTHING)
    day = models.IntegerField(db_index=True)
    cluster = models.IntegerField(db_index=True)
    distance_to_clusters = ArrayField(
            models.DecimalField(max_digits=35, decimal_places=10), null = True,
        )
    test_number = models.IntegerField(null=True)
    expert_decision = models.NullBooleanField(null=True)

    class Meta:
        db_table = "ml_placements_clusters_kmeans"
        unique_together = (('placement', 'day', 'test_number'),)


class MLClustersCentroidsKmeans(models.Model):
    id = models.AutoField(primary_key=True)
    cluster = models.IntegerField()
    day = models.IntegerField(db_index=True)
    centroid = ArrayField(
            models.DecimalField(max_digits=35, decimal_places=10),
        )
    test_number = models.IntegerField(null=True)

    class Meta:
        db_table = "ml_clusters_centroids_kmeans"
        unique_together = (('cluster', 'day', 'test_number'),)
