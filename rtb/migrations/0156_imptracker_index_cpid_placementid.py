from __future__ import unicode_literals

import django.contrib.postgres.fields.jsonb
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('rtb', '0155_ui_tracker_initial_fill'),
    ]

    operations = [

        #
        # impression tracker
        #

        migrations.RunSQL("""
                            DROP INDEX IF EXISTS rtb_impression_tracker_cpid_placementid;
                            CREATE INDEX rtb_impression_tracker_cpid_placementid ON rtb_impression_tracker USING btree ("CpId", "PlacementId");
                            """),

    ]