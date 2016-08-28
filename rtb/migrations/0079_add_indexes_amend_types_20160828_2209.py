from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('rtb', '0078_auto_20160826_0708'),
    ]

    operations = [
        migrations.RunSQL(
            'ALTER TABLE network_analytics_report_by_placement ALTER COLUMN hour TYPE timestamp without time zone;'),
        migrations.RunSQL(
            'CREATE INDEX IF NOT EXISTS network_analytics_report_by_placement_campaign_hours ON network_analytics_report_by_placement USING btree (campaign_id, hour, hour DESC);'),
        migrations.RunSQL(
            'ALTER TABLE network_analytics_report_by_placement CLUSTER ON network_analytics_report_by_placement_campaign_hours;'),
        migrations.RunSQL(
            'ALTER TABLE site_domain_performance_report ALTER COLUMN day TYPE timestamp without time zone;'),
        migrations.RunSQL(
            'CREATE INDEX IF NOT EXISTS site_domain_performance_report_campaign_id_days ON site_domain_performance_report USING btree (campaign_id, day, day DESC);'),
        migrations.RunSQL(
            'CREATE INDEX IF NOT EXISTS site_domain_performance_report_campaign_id_day ON site_domain_performance_report USING btree (campaign_id, day);'),
        migrations.RunSQL(
            'ALTER TABLE site_domain_performance_report CLUSTER ON site_domain_performance_report_campaign_id_days;'),
    ]
