__author__ = 'USER'
from django.db import models




class PlacementDailyFeatures(models.Model):
    id = models.AutoField(primary_key=True)
    placement_id = models.IntegerField()
    day = models.IntegerField()
    #weekday_start = models.IntegerField()#0 - Monday???  don't need to storage in every row
    imps = models.IntegerField()
    clicks = models.IntegerField()
    total_convs = models.IntegerField()
    imps_viewed = models.IntegerField()
    view_measured_imps = models.IntegerField()

    cost = models.DecimalField(max_digits=35, decimal_places=10)

    view_rate = models.FloatField()
    view_measurement_rate = models.FloatField()
    cpa = models.FloatField()
    ctr = models.FloatField()

    class Meta:
        db_table = "placement_daily_features"
        unique_together = (('placement_id', 'day'),)


class PlacementsClustersKmeans(models.Model):
    id = models.AutoField(primary_key=True)
    placement_id = models.IntegerField()
    cluster = models.IntegerField()
    day = models.IntegerField()

    class Meta:
        db_table = "placements_clusters_kmeans"


class ClustersCentroids(models.Model):
    id = models.AutoField(primary_key=True)
    cluster = models.IntegerField()
    centroid = models.DecimalField(max_digits=35, decimal_places=10)

    class Meta:
        db_table = "clusters_centroids"
