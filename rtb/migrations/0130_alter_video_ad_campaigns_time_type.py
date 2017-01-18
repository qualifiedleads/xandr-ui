from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('rtb', '0129_auto_20170117_1319'),
    ]

    operations = [
        migrations.RunSQL('ALTER TABLE video_ad_campaigns ALTER COLUMN date TYPE timestamp without time zone;'),
        migrations.RunSQL('ALTER TABLE video_ad_campaigns ALTER COLUMN hour TYPE timestamp without time zone;'),
        ]