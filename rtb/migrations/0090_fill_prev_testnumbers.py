from __future__ import unicode_literals

from django.db import migrations, models

class Migration(migrations.Migration):

    dependencies = [
        ('rtb', '0089_auto_20161005_0732'),
    ]

    operations = [
        migrations.RunSQL(
            'UPDATE ml_clusters_centroids_kmeans SET test_number=1 WHERE test_number is NULL ;'),
        migrations.RunSQL(
            'UPDATE ml_placements_clusters_kmeans SET test_number=1 WHERE test_number is NULL ;'),
    ]