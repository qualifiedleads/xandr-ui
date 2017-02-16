from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rtb', '0140_auto_20170207_1237'),
    ]

    operations = [
        migrations.RunSQL(
            'create index ml_placements_clusters_kmeans_placement_id_2_idx on  ml_placements_clusters_kmeans(placement_id) where test_number = 2;'),
        migrations.RunSQL(
            'create index ml_logistic_regression_results_placement_id_3_prob_idx on  ml_logistic_regression_results(placement_id) where test_number = 3 and probability != -1;'),
    ]
