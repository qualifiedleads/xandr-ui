from django.db import models

class MLDecisionTreeClassifierResults(models.Model):
    id = models.AutoField(primary_key=True)
    placement = models.ForeignKey("Placement", db_constraint=False, on_delete=models.DO_NOTHING)
    day = models.IntegerField(db_index=True)
    test_number = models.IntegerField(null=True, db_index=True)
    expert_decision = models.NullBooleanField(null=True, db_index=True)
    good = models.NullBooleanField(null=True)

    class Meta:
        db_table = "ml_decision_tree_classifier_results"
        unique_together = (('placement', 'day', 'test_number'),)