from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('rtb', '0108_auto_20161116_1350'),
    ]

    operations = [
        migrations.RunSQL(
            """
                CREATE MATERIALIZED VIEW
                  view_rules_campaign_placements
                AS
                  SELECT
                    campaign_id,
                    placement_id,
                    SUM(imps) imressions,
                    SUM(clicks) clicks,
                    SUM(cost) spent,
                    case SUM(total_convs) when 0 then 0 else SUM(cost)::float/SUM(total_convs) end cpa,
                    case SUM(imps) when 0 then 0 else SUM(clicks)::float/SUM(imps) end ctr,
                    case SUM(imps) when 0 then 0 else SUM(total_convs)::float/SUM(imps) end cvr,
                    case SUM(clicks) when 0 then 0 else SUM(cost)::float/SUM(clicks) end cpc
                  FROM
                    network_analytics_report_by_placement
                  group by campaign_id,placement_id;
            """
        ),
        migrations.RunSQL('CREATE INDEX view_rules_campaign_placements_placement_and_campaign_idx ON view_rules_campaign_placements (campaign_id, placement_id);'),
        migrations.RunSQL('CREATE INDEX view_rules_campaign_placements_imressions_idx ON view_rules_campaign_placements (imressions);'),
        migrations.RunSQL('CREATE INDEX view_rules_campaign_placements_clicks_idx ON view_rules_campaign_placements (clicks);'),
        migrations.RunSQL('CREATE INDEX view_rules_campaign_placements_spent_idx ON view_rules_campaign_placements (spent);'),
        migrations.RunSQL('CREATE INDEX view_rules_campaign_placements_cpa_idx ON view_rules_campaign_placements (cpa);'),
        migrations.RunSQL('CREATE INDEX view_rules_campaign_placements_ctr_idx ON view_rules_campaign_placements (ctr);'),
        migrations.RunSQL('CREATE INDEX view_rules_campaign_placements_cvr_idx ON view_rules_campaign_placements (cvr);'),
        migrations.RunSQL('CREATE INDEX view_rules_campaign_placements_cpc_idx ON view_rules_campaign_placements (cpc);'),
    ]