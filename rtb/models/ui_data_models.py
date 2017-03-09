from django.db import models
from django.contrib.postgres.fields import JSONField

class UIUsualCampaignsGraph(models.Model):
    id = models.AutoField(primary_key=True)
    advertiser = models.ForeignKey("Advertiser", null=True, blank=True, db_constraint=False,
                                   on_delete=models.DO_NOTHING)
    type = models.TextField(db_index=True)
    # simple grid data
    day_chart = JSONField(default=list([]), null=True)

    class Meta:
        db_table = "ui_usual_advertisers_graph"
        unique_together = (('advertiser', 'type'),)

class UIUsualCampaignsGridDataYesterday(models.Model):
    id = models.AutoField(primary_key=True)
    campaign = models.ForeignKey("Campaign", null=True, blank=True, db_constraint=False, on_delete=models.DO_NOTHING, unique=True)
    # simple grid data
    spent = models.DecimalField(null=True, blank=True, max_digits=35, decimal_places=10)
    conversions = models.IntegerField()
    imps = models.IntegerField()
    clicks = models.IntegerField()
    cpc = models.DecimalField(null=True, blank=True, max_digits=35, decimal_places=10)
    cpm = models.DecimalField(null=True, blank=True, max_digits=35, decimal_places=10)
    cvr = models.DecimalField(null=True, blank=True, max_digits=35, decimal_places=10)
    ctr = models.FloatField(null=True, blank=True)
    imps_viewed = models.IntegerField(null=True, blank=True)
    view_measured_imps = models.IntegerField(null=True, blank=True)
    view_measurement_rate = models.FloatField(null=True, blank=True)
    view_rate = models.FloatField(null=True, blank=True)
    # charts
    day_chart = JSONField(default=list([]), null=True)

    class Meta:
        db_table = "ui_usual_campaigns_grid_data_yesterday"

class UIUsualCampaignsGridDataLast3Days(models.Model):
    id = models.AutoField(primary_key=True)
    campaign = models.ForeignKey("Campaign", null=True, blank=True, db_constraint=False, on_delete=models.DO_NOTHING, unique=True)
    # simple grid data
    spent = models.DecimalField(null=True, blank=True, max_digits=35, decimal_places=10)
    conversions = models.IntegerField()
    imps = models.IntegerField()
    clicks = models.IntegerField()
    cpc = models.DecimalField(null=True, blank=True, max_digits=35, decimal_places=10)
    cpm = models.DecimalField(null=True, blank=True, max_digits=35, decimal_places=10)
    cvr = models.DecimalField(null=True, blank=True, max_digits=35, decimal_places=10)
    ctr = models.FloatField(null=True, blank=True)
    imps_viewed = models.IntegerField(null=True, blank=True)
    view_measured_imps = models.IntegerField(null=True, blank=True)
    view_measurement_rate = models.FloatField(null=True, blank=True)
    view_rate = models.FloatField(null=True, blank=True)
    # charts
    day_chart = JSONField(default=list([]), null=True)

    class Meta:
        db_table = "ui_usual_campaigns_grid_data_last_3_days"

class UIUsualCampaignsGridDataLast7Days(models.Model):
    id = models.AutoField(primary_key=True)
    campaign = models.ForeignKey("Campaign", null=True, blank=True, db_constraint=False, on_delete=models.DO_NOTHING, unique=True)
    # simple grid data
    spent = models.DecimalField(null=True, blank=True, max_digits=35, decimal_places=10)
    conversions = models.IntegerField()
    imps = models.IntegerField()
    clicks = models.IntegerField()
    cpc = models.DecimalField(null=True, blank=True, max_digits=35, decimal_places=10)
    cpm = models.DecimalField(null=True, blank=True, max_digits=35, decimal_places=10)
    cvr = models.DecimalField(null=True, blank=True, max_digits=35, decimal_places=10)
    ctr = models.FloatField(null=True, blank=True)
    imps_viewed = models.IntegerField(null=True, blank=True)
    view_measured_imps = models.IntegerField(null=True, blank=True)
    view_measurement_rate = models.FloatField(null=True, blank=True)
    view_rate = models.FloatField(null=True, blank=True)
    # charts
    day_chart = JSONField(default=list([]), null=True)

    class Meta:
        db_table = "ui_usual_campaigns_grid_data_last_7_days"

class UIUsualCampaignsGridDataLast14Days(models.Model):
    id = models.AutoField(primary_key=True)
    campaign = models.ForeignKey("Campaign", null=True, blank=True, db_constraint=False, on_delete=models.DO_NOTHING, unique=True)
    # simple grid data
    spent = models.DecimalField(null=True, blank=True, max_digits=35, decimal_places=10)
    conversions = models.IntegerField()
    imps = models.IntegerField()
    clicks = models.IntegerField()
    cpc = models.DecimalField(null=True, blank=True, max_digits=35, decimal_places=10)
    cpm = models.DecimalField(null=True, blank=True, max_digits=35, decimal_places=10)
    cvr = models.DecimalField(null=True, blank=True, max_digits=35, decimal_places=10)
    ctr = models.FloatField(null=True, blank=True)
    imps_viewed = models.IntegerField(null=True, blank=True)
    view_measured_imps = models.IntegerField(null=True, blank=True)
    view_measurement_rate = models.FloatField(null=True, blank=True)
    view_rate = models.FloatField(null=True, blank=True)
    # charts
    day_chart = JSONField(default=list([]), null=True)

    class Meta:
        db_table = "ui_usual_campaigns_grid_data_last_14_days"


class UIUsualCampaignsGridDataLast21Days(models.Model):
    id = models.AutoField(primary_key=True)
    campaign = models.ForeignKey("Campaign", null=True, blank=True, db_constraint=False, on_delete=models.DO_NOTHING,
                                 unique=True)
    # simple grid data
    spent = models.DecimalField(null=True, blank=True, max_digits=35, decimal_places=10)
    conversions = models.IntegerField()
    imps = models.IntegerField()
    clicks = models.IntegerField()
    cpc = models.DecimalField(null=True, blank=True, max_digits=35, decimal_places=10)
    cpm = models.DecimalField(null=True, blank=True, max_digits=35, decimal_places=10)
    cvr = models.DecimalField(null=True, blank=True, max_digits=35, decimal_places=10)
    ctr = models.FloatField(null=True, blank=True)
    imps_viewed = models.IntegerField(null=True, blank=True)
    view_measured_imps = models.IntegerField(null=True, blank=True)
    view_measurement_rate = models.FloatField(null=True, blank=True)
    view_rate = models.FloatField(null=True, blank=True)
    # charts
    day_chart = JSONField(default=list([]), null=True)

    class Meta:
        db_table = "ui_usual_campaigns_grid_data_last_21_days"


class UIUsualCampaignsGridDataCurMonth(models.Model):
    id = models.AutoField(primary_key=True)
    campaign = models.ForeignKey("Campaign", null=True, blank=True, db_constraint=False, on_delete=models.DO_NOTHING,
                                 unique=True)
    # simple grid data
    spent = models.DecimalField(null=True, blank=True, max_digits=35, decimal_places=10)
    conversions = models.IntegerField()
    imps = models.IntegerField()
    clicks = models.IntegerField()
    cpc = models.DecimalField(null=True, blank=True, max_digits=35, decimal_places=10)
    cpm = models.DecimalField(null=True, blank=True, max_digits=35, decimal_places=10)
    cvr = models.DecimalField(null=True, blank=True, max_digits=35, decimal_places=10)
    ctr = models.FloatField(null=True, blank=True)
    imps_viewed = models.IntegerField(null=True, blank=True)
    view_measured_imps = models.IntegerField(null=True, blank=True)
    view_measurement_rate = models.FloatField(null=True, blank=True)
    view_rate = models.FloatField(null=True, blank=True)
    # charts
    day_chart = JSONField(default=list([]), null=True)

    class Meta:
        db_table = "ui_usual_campaigns_grid_data_cur_month"


class UIUsualCampaignsGridDataLastMonth(models.Model):
    id = models.AutoField(primary_key=True)
    campaign = models.ForeignKey("Campaign", null=True, blank=True, db_constraint=False, on_delete=models.DO_NOTHING,
                                 unique=True)
    # simple grid data
    spent = models.DecimalField(null=True, blank=True, max_digits=35, decimal_places=10)
    conversions = models.IntegerField()
    imps = models.IntegerField()
    clicks = models.IntegerField()
    cpc = models.DecimalField(null=True, blank=True, max_digits=35, decimal_places=10)
    cpm = models.DecimalField(null=True, blank=True, max_digits=35, decimal_places=10)
    cvr = models.DecimalField(null=True, blank=True, max_digits=35, decimal_places=10)
    ctr = models.FloatField(null=True, blank=True)
    imps_viewed = models.IntegerField(null=True, blank=True)
    view_measured_imps = models.IntegerField(null=True, blank=True)
    view_measurement_rate = models.FloatField(null=True, blank=True)
    view_rate = models.FloatField(null=True, blank=True)
    # charts
    day_chart = JSONField(default=list([]), null=True)

    class Meta:
        db_table = "ui_usual_campaigns_grid_data_last_month"


class UIUsualCampaignsGridDataLast90Days(models.Model):
    id = models.AutoField(primary_key=True)
    campaign = models.ForeignKey("Campaign", null=True, blank=True, db_constraint=False, on_delete=models.DO_NOTHING,
                                 unique=True)
    # simple grid data
    spent = models.DecimalField(null=True, blank=True, max_digits=35, decimal_places=10)
    conversions = models.IntegerField()
    imps = models.IntegerField()
    clicks = models.IntegerField()
    cpc = models.DecimalField(null=True, blank=True, max_digits=35, decimal_places=10)
    cpm = models.DecimalField(null=True, blank=True, max_digits=35, decimal_places=10)
    cvr = models.DecimalField(null=True, blank=True, max_digits=35, decimal_places=10)
    ctr = models.FloatField(null=True, blank=True)
    imps_viewed = models.IntegerField(null=True, blank=True)
    view_measured_imps = models.IntegerField(null=True, blank=True)
    view_measurement_rate = models.FloatField(null=True, blank=True)
    view_rate = models.FloatField(null=True, blank=True)
    # charts
    day_chart = JSONField(default=list([]), null=True)

    class Meta:
        db_table = "ui_usual_campaigns_grid_data_last_90_days"

class UIUsualCampaignsGridDataAll(models.Model):
    id = models.AutoField(primary_key=True)
    campaign = models.ForeignKey("Campaign", null=True, blank=True, db_constraint=False, on_delete=models.DO_NOTHING,
                                 unique=True)
    # simple grid data
    spent = models.DecimalField(null=True, blank=True, max_digits=35, decimal_places=10)
    conversions = models.IntegerField()
    imps = models.IntegerField()
    clicks = models.IntegerField()
    cpc = models.DecimalField(null=True, blank=True, max_digits=35, decimal_places=10)
    cpm = models.DecimalField(null=True, blank=True, max_digits=35, decimal_places=10)
    cvr = models.DecimalField(null=True, blank=True, max_digits=35, decimal_places=10)
    ctr = models.FloatField(null=True, blank=True)
    imps_viewed = models.IntegerField(null=True, blank=True)
    view_measured_imps = models.IntegerField(null=True, blank=True)
    view_measurement_rate = models.FloatField(null=True, blank=True)
    view_rate = models.FloatField(null=True, blank=True)
    # charts
    day_chart = JSONField(default=list([]), null=True)

    class Meta:
        db_table = "ui_usual_campaigns_grid_data_all"

###
# usual placements
###
class UIUsualPlacementsGraph(models.Model):
    id = models.AutoField(primary_key=True)
    campaign = models.ForeignKey("Campaign", null=True, blank=True, db_constraint=False, on_delete=models.DO_NOTHING)
    type = models.TextField(db_index=True)
    # simple grid data
    day_chart = JSONField(default=list([]), null=True)

    class Meta:
        db_table = "ui_usual_placements_graph"
        unique_together = (('campaign', 'type'),)

class UIUsualPlacementsGridDataYesterday(models.Model):
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
        db_table = "ui_usual_placements_grid_data_yesterday"
        unique_together = (('campaign', 'placement'),)

class UIUsualPlacementsGridDataLast3Days(models.Model):
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
        db_table = "ui_usual_placements_grid_data_last_3_days"
        unique_together = (('campaign', 'placement'),)

class UIUsualPlacementsGridDataLast7Days(models.Model):
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
        db_table = "ui_usual_placements_grid_data_last_7_days"
        unique_together = (('campaign', 'placement'),)

class UIUsualPlacementsGridDataLast14Days(models.Model):
    id = models.AutoField(primary_key=True)
    campaign = models.ForeignKey("Campaign", null=True, blank=True, db_constraint=False, on_delete=models.DO_NOTHING)
    placement = models.ForeignKey("Placement", null=True, blank=True, db_constraint=False, on_delete=models.DO_NOTHING,)
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
        db_table = "ui_usual_placements_grid_data_last_14_days"
        unique_together = (('campaign', 'placement'),)


class UIUsualPlacementsGridDataLast21Days(models.Model):
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
        db_table = "ui_usual_placements_grid_data_last_21_days"
        unique_together = (('campaign', 'placement'),)


class UIUsualPlacementsGridDataCurMonth(models.Model):
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
        db_table = "ui_usual_placements_grid_data_cur_month"
        unique_together = (('campaign', 'placement'),)


class UIUsualPlacementsGridDataLastMonth(models.Model):
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
        db_table = "ui_usual_placements_grid_data_last_month"
        unique_together = (('campaign', 'placement'),)


class UIUsualPlacementsGridDataLast90Days(models.Model):
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
        db_table = "ui_usual_placements_grid_data_last_90_days"
        unique_together = (('campaign', 'placement'),)

class UIUsualPlacementsGridDataAll(models.Model):
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
        db_table = "ui_usual_placements_grid_data_all"
        unique_together = (('campaign', 'placement'),)

class PlacementsAdditionalNames(models.Model):
    id = models.AutoField(primary_key=True)
    placement = models.ForeignKey("Placement", null=True, blank=True, db_constraint=False, on_delete=models.DO_NOTHING, unique=True)
    publisher_name = models.TextField(null=True, blank=True)
    seller_member_name = models.TextField(null=True, blank=True)

    class Meta:
        db_table = "placements_additional_names"
###
# video campaigns
###
class UIVideoCampaignsGridDataYesterday(models.Model):
    id = models.AutoField(primary_key=True)
    campaign = models.ForeignKey("Campaign", null=True, blank=True, db_constraint=False, on_delete=models.DO_NOTHING, unique=True)
    evaluation_date = models.DateTimeField(db_index=True)
    window_start_date = models.DateTimeField(db_index=True)
    # simple grid data
    spent = models.DecimalField(null=True, max_digits=35, decimal_places=10)
    imps = models.IntegerField(null=True)
    ad_starts = models.IntegerField(null=True)
    cpm = models.DecimalField(null=True, max_digits=35, decimal_places=10)
    fill_rate = models.DecimalField(null=True, max_digits=35, decimal_places=10)
    profit_loss = models.DecimalField(null=True, max_digits=35, decimal_places=10)
    delta_fill_rate = models.DecimalField(null=True, max_digits=35, decimal_places=10)
    delta_profit_loss = models.DecimalField(null=True, max_digits=35, decimal_places=10)
    # charts
    day_chart = JSONField(default=list([]), null=True)

    class Meta:
        db_table = "ui_video_campaigns_grid_data_yesterday"

class UIVideoCampaignsGridDataLast3Days(models.Model):
    id = models.AutoField(primary_key=True)
    campaign = models.ForeignKey("Campaign", null=True, blank=True, db_constraint=False, on_delete=models.DO_NOTHING, unique=True)
    evaluation_date = models.DateTimeField(db_index=True)
    window_start_date = models.DateTimeField(db_index=True)
    # simple grid data
    spent = models.DecimalField(null=True, max_digits=35, decimal_places=10)
    imps = models.IntegerField(null=True)
    ad_starts = models.IntegerField(null=True)
    cpm = models.DecimalField(null=True, max_digits=35, decimal_places=10)
    fill_rate = models.DecimalField(null=True, max_digits=35, decimal_places=10)
    profit_loss = models.DecimalField(null=True, max_digits=35, decimal_places=10)
    delta_fill_rate = models.DecimalField(null=True, max_digits=35, decimal_places=10)
    delta_profit_loss = models.DecimalField(null=True, max_digits=35, decimal_places=10)
    # charts
    day_chart = JSONField(default=list([]), null=True)

    class Meta:
        db_table = "ui_video_campaigns_grid_data_last_3_days"

class UIVideoCampaignsGridDataLast7Days(models.Model):
    id = models.AutoField(primary_key=True)
    campaign = models.ForeignKey("Campaign", null=True, blank=True, db_constraint=False, on_delete=models.DO_NOTHING, unique=True)
    evaluation_date = models.DateTimeField(db_index=True)
    window_start_date = models.DateTimeField(db_index=True)
    # simple grid data
    spent = models.DecimalField(null=True, max_digits=35, decimal_places=10)
    imps = models.IntegerField(null=True)
    ad_starts = models.IntegerField(null=True)
    cpm = models.DecimalField(null=True, max_digits=35, decimal_places=10)
    fill_rate = models.DecimalField(null=True, max_digits=35, decimal_places=10)
    profit_loss = models.DecimalField(null=True, max_digits=35, decimal_places=10)
    delta_fill_rate = models.DecimalField(null=True, max_digits=35, decimal_places=10)
    delta_profit_loss = models.DecimalField(null=True, max_digits=35, decimal_places=10)
    # charts
    day_chart = JSONField(default=list([]), null=True)

    class Meta:
        db_table = "ui_video_campaigns_grid_data_last_7_days"

class UIVideoCampaignsGridDataLast14Days(models.Model):
    id = models.AutoField(primary_key=True)
    campaign = models.ForeignKey("Campaign", null=True, blank=True, db_constraint=False, on_delete=models.DO_NOTHING,
                                 unique=True)
    evaluation_date = models.DateTimeField(db_index=True)
    window_start_date = models.DateTimeField(db_index=True)
    # simple grid data
    spent = models.DecimalField(null=True, max_digits=35, decimal_places=10)
    imps = models.IntegerField(null=True)
    ad_starts = models.IntegerField(null=True)
    cpm = models.DecimalField(null=True, max_digits=35, decimal_places=10)
    fill_rate = models.DecimalField(null=True, max_digits=35, decimal_places=10)
    profit_loss = models.DecimalField(null=True, max_digits=35, decimal_places=10)
    delta_fill_rate = models.DecimalField(null=True, max_digits=35, decimal_places=10)
    delta_profit_loss = models.DecimalField(null=True, max_digits=35, decimal_places=10)
    # charts
    day_chart = JSONField(default=list([]), null=True)

    class Meta:
        db_table = "ui_video_campaigns_grid_data_last_14_days"

class UIVideoCampaignsGridDataLast21Days(models.Model):
    id = models.AutoField(primary_key=True)
    campaign = models.ForeignKey("Campaign", null=True, blank=True, db_constraint=False, on_delete=models.DO_NOTHING,
                                 unique=True)
    evaluation_date = models.DateTimeField(db_index=True)
    window_start_date = models.DateTimeField(db_index=True)
    # simple grid data
    spent = models.DecimalField(null=True, max_digits=35, decimal_places=10)
    imps = models.IntegerField(null=True)
    ad_starts = models.IntegerField(null=True)
    cpm = models.DecimalField(null=True, max_digits=35, decimal_places=10)
    fill_rate = models.DecimalField(null=True, max_digits=35, decimal_places=10)
    profit_loss = models.DecimalField(null=True, max_digits=35, decimal_places=10)
    delta_fill_rate = models.DecimalField(null=True, max_digits=35, decimal_places=10)
    delta_profit_loss = models.DecimalField(null=True, max_digits=35, decimal_places=10)
    # charts
    day_chart = JSONField(default=list([]), null=True)

    class Meta:
        db_table = "ui_video_campaigns_grid_data_last_21_days"

class UIVideoCampaignsGridDataCurMonth(models.Model):
    id = models.AutoField(primary_key=True)
    campaign = models.ForeignKey("Campaign", null=True, blank=True, db_constraint=False, on_delete=models.DO_NOTHING,
                                 unique=True)
    evaluation_date = models.DateTimeField(db_index=True)
    window_start_date = models.DateTimeField(db_index=True)
    # simple grid data
    spent = models.DecimalField(null=True, max_digits=35, decimal_places=10)
    imps = models.IntegerField(null=True)
    ad_starts = models.IntegerField(null=True)
    cpm = models.DecimalField(null=True, max_digits=35, decimal_places=10)
    fill_rate = models.DecimalField(null=True, max_digits=35, decimal_places=10)
    profit_loss = models.DecimalField(null=True, max_digits=35, decimal_places=10)
    delta_fill_rate = models.DecimalField(null=True, max_digits=35, decimal_places=10)
    delta_profit_loss = models.DecimalField(null=True, max_digits=35, decimal_places=10)
    # charts
    day_chart = JSONField(default=list([]), null=True)

    class Meta:
        db_table = "ui_video_campaigns_grid_data_cur_month"

class UIVideoCampaignsGridDataLastMonth(models.Model):
    id = models.AutoField(primary_key=True)
    campaign = models.ForeignKey("Campaign", null=True, blank=True, db_constraint=False, on_delete=models.DO_NOTHING,
                                 unique=True)
    evaluation_date = models.DateTimeField(db_index=True)
    window_start_date = models.DateTimeField(db_index=True)
    # simple grid data
    spent = models.DecimalField(null=True, max_digits=35, decimal_places=10)
    imps = models.IntegerField(null=True)
    ad_starts = models.IntegerField(null=True)
    cpm = models.DecimalField(null=True, max_digits=35, decimal_places=10)
    fill_rate = models.DecimalField(null=True, max_digits=35, decimal_places=10)
    profit_loss = models.DecimalField(null=True, max_digits=35, decimal_places=10)
    delta_fill_rate = models.DecimalField(null=True, max_digits=35, decimal_places=10)
    delta_profit_loss = models.DecimalField(null=True, max_digits=35, decimal_places=10)
    # charts
    day_chart = JSONField(default=list([]), null=True)

    class Meta:
        db_table = "ui_video_campaigns_grid_data_last_month"

class UIVideoCampaignsGridDataLast90Days(models.Model):
    id = models.AutoField(primary_key=True)
    campaign = models.ForeignKey("Campaign", null=True, blank=True, db_constraint=False, on_delete=models.DO_NOTHING,
                                 unique=True)
    evaluation_date = models.DateTimeField(db_index=True)
    window_start_date = models.DateTimeField(db_index=True)
    # simple grid data
    spent = models.DecimalField(null=True, max_digits=35, decimal_places=10)
    imps = models.IntegerField(null=True)
    ad_starts = models.IntegerField(null=True)
    cpm = models.DecimalField(null=True, max_digits=35, decimal_places=10)
    fill_rate = models.DecimalField(null=True, max_digits=35, decimal_places=10)
    profit_loss = models.DecimalField(null=True, max_digits=35, decimal_places=10)
    delta_fill_rate = models.DecimalField(null=True, max_digits=35, decimal_places=10)
    delta_profit_loss = models.DecimalField(null=True, max_digits=35, decimal_places=10)
    # charts
    day_chart = JSONField(default=list([]), null=True)

    class Meta:
        db_table = "ui_video_campaigns_grid_data_last_90_days"

class UIVideoCampaignsGridDataAll(models.Model):
    id = models.AutoField(primary_key=True)
    campaign = models.ForeignKey("Campaign", null=True, blank=True, db_constraint=False, on_delete=models.DO_NOTHING, unique=True)
    evaluation_date = models.DateTimeField(db_index=True)
    # simple grid data
    spent = models.DecimalField(null=True, max_digits=35, decimal_places=10)
    imps = models.IntegerField(null=True)
    ad_starts = models.IntegerField(null=True)
    cpm = models.DecimalField(null=True, max_digits=35, decimal_places=10)
    fill_rate = models.DecimalField(null=True, max_digits=35, decimal_places=10)
    profit_loss = models.DecimalField(null=True, max_digits=35, decimal_places=10)
    delta_fill_rate = models.DecimalField(null=True, max_digits=35, decimal_places=10)
    delta_profit_loss = models.DecimalField(null=True, max_digits=35, decimal_places=10)
    # charts
    day_chart = JSONField(default=list([]), null=True)

    class Meta:
        db_table = "ui_video_campaigns_grid_data_all"