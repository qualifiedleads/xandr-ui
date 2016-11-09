from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('rtb', '0082_networkanalyticsreport_byplacement_test_geo_country_name'),
    ]

    operations = [
        migrations.RunSQL(
            'ALTER TABLE network_carrier_report_simple ALTER COLUMN day TYPE timestamp without time zone;'),
        migrations.RunSQL("""
            DROP INDEX IF EXISTS network_carrier_report_simple_campaign_days;
            CREATE INDEX network_carrier_report_simple_campaign_days ON network_carrier_report_simple USING btree (campaign_id, day, day DESC);
            """),
        migrations.RunSQL(
            'ALTER TABLE network_carrier_report_simple CLUSTER ON network_carrier_report_simple_campaign_days;'),

        migrations.RunSQL(
            'ALTER TABLE network_device_report_simple ALTER COLUMN day TYPE timestamp without time zone;'),
        migrations.RunSQL("""
            DROP INDEX IF EXISTS network_device_report_simple_campaign_days;
            CREATE INDEX network_device_report_simple_campaign_days ON network_device_report_simple USING btree (campaign_id, day, day DESC);
            """),
        migrations.RunSQL(
            'ALTER TABLE network_device_report_simple CLUSTER ON network_device_report_simple_campaign_days;'),

        migrations.RunSQL(
            'ALTER TABLE network_analytics_report ALTER COLUMN hour TYPE timestamp without time zone;'),
        migrations.RunSQL("""
        DROP INDEX IF EXISTS network_analytics_report_campaign_hours;
        CREATE INDEX network_analytics_report_campaign_hours ON network_analytics_report USING btree (campaign_id, hour, hour DESC);
        """),
        migrations.RunSQL(
            'ALTER TABLE network_analytics_report CLUSTER ON network_analytics_report_campaign_hours;'),

        migrations.RunSQL("""
        DROP INDEX IF EXISTS geo_analytics_report_campaign_days;
        CREATE INDEX geo_analytics_report_campaign_days ON geo_analytics_report USING btree (campaign_id, day, day DESC);
        """),
        migrations.RunSQL(
            'ALTER TABLE geo_analytics_report CLUSTER ON geo_analytics_report_campaign_days;'),
    ]
