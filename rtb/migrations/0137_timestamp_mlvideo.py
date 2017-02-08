from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('rtb', '0136_auto_20170204_2339'),
    ]

    operations = [
        migrations.RunSQL('ALTER TABLE video_ad_placements ALTER COLUMN date TYPE timestamp without time zone;'),
        migrations.RunSQL('ALTER TABLE video_ad_placements ALTER COLUMN hour TYPE timestamp without time zone;'),
        migrations.RunSQL('ALTER TABLE ml_video_imps_tracker ALTER COLUMN "Date" TYPE timestamp without time zone;'),
        migrations.RunSQL('ALTER TABLE ml_video_ad_campaigns_models_info ALTER COLUMN start TYPE timestamp without time zone;'),
        migrations.RunSQL('ALTER TABLE ml_video_ad_campaigns_models_info ALTER COLUMN finish TYPE timestamp without time zone;'),
    ]
