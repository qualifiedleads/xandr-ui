from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('rtb', '0134_timestamp_imp_tracker'),
    ]

    operations = [
        migrations.RunSQL('CREATE INDEX video_ad_campaigns_hour_desc ON video_ad_campaigns USING btree (hour DESC);')
    ]