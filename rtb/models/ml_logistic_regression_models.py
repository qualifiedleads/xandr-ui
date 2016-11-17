from django.db import models
from django.contrib.postgres.fields import ArrayField

class MLLogisticRegressionCoeff(models.Model):
    id = models.AutoField(primary_key=True)
    day = models.IntegerField(db_index=True)
    coeff = ArrayField(
            models.DecimalField(max_digits=35, decimal_places=10),
        )
    test_number = models.IntegerField(null=True, db_index=True)
    good_direction = models.TextField(null=True)

    class Meta:
        db_table = "ml_logistic_regression_coeff"
        unique_together = (('day', 'test_number'),)

class MLLogisticRegressionResults(models.Model):
    id = models.AutoField(primary_key=True)
    placement = models.ForeignKey("Placement", db_constraint=False, on_delete = models.DO_NOTHING)
    day = models.IntegerField(db_index=True)
    probability = models.DecimalField(max_digits=35, decimal_places=10)
    test_number = models.IntegerField(null=True, db_index=True)
    expert_decision = models.NullBooleanField(null=True, db_index=True)

    class Meta:
        db_table = "ml_logistic_regression_results"
        unique_together = (('placement', 'day', 'test_number'),)