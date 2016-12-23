from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('rtb', '0113_mllogisticregressionresults_good'),
    ]

    operations = [
        migrations.RunSQL(""" DROP MATERIALIZED VIEW view_rules_campaign_placements; """),
        migrations.RunSQL(
            """
                CREATE MATERIALIZED VIEW
                  view_rules_campaign_placements
                AS
                  SELECT
                      na.campaign_id,
                      na.placement_id,
                      na.impressions,
                      na.clicks,
                      na.spent,
                      na.cpa,
                      na.ctr,
                      na.cvr,
                      na.cpc,
                      kmeans.good AS prediction1,
                      logreg.good AS prediction2
                    FROM ml_logistic_regression_results AS logreg
                      RIGHT JOIN
                      (SELECT
                        campaign_id,
                        placement_id,
                        SUM(imps) impressions,
                        SUM(clicks) clicks,
                        SUM(cost) spent,
                        case SUM(total_convs) when 0 then 0 else SUM(cost)::float/SUM(total_convs) end cpa,
                        case SUM(imps) when 0 then 0 else SUM(clicks)::float/SUM(imps) end ctr,
                        case SUM(imps) when 0 then 0 else SUM(total_convs)::float/SUM(imps) end cvr,
                        case SUM(clicks) when 0 then 0 else SUM(cost)::float/SUM(clicks) end cpc
                      FROM
                        network_analytics_report_by_placement
                      GROUP BY
                      campaign_id, placement_id) AS na
                      ON logreg.placement_id =  na.placement_id
                      LEFT JOIN
                        (SELECT placement_id, good FROM ml_placements_clusters_kmeans WHERE day=7 AND test_number = 2) AS kmeans
                        ON na.placement_id = kmeans.placement_id;
            """
        ),
        migrations.RunSQL('CREATE INDEX view_rules_campaign_placements_placement_and_campaign_idx ON view_rules_campaign_placements (campaign_id, placement_id);'),
        migrations.RunSQL('CREATE INDEX view_rules_campaign_placements_impressions_idx ON view_rules_campaign_placements (impressions);'),
        migrations.RunSQL('CREATE INDEX view_rules_campaign_placements_clicks_idx ON view_rules_campaign_placements (clicks);'),
        migrations.RunSQL('CREATE INDEX view_rules_campaign_placements_spent_idx ON view_rules_campaign_placements (spent);'),
        migrations.RunSQL('CREATE INDEX view_rules_campaign_placements_cpa_idx ON view_rules_campaign_placements (cpa);'),
        migrations.RunSQL('CREATE INDEX view_rules_campaign_placements_ctr_idx ON view_rules_campaign_placements (ctr);'),
        migrations.RunSQL('CREATE INDEX view_rules_campaign_placements_cvr_idx ON view_rules_campaign_placements (cvr);'),
        migrations.RunSQL('CREATE INDEX view_rules_campaign_placements_cpc_idx ON view_rules_campaign_placements (cpc);'),
        migrations.RunSQL('CREATE INDEX view_rules_campaign_placements_prediction1_idx ON view_rules_campaign_placements (prediction1);'),
        migrations.RunSQL('CREATE INDEX view_rules_campaign_placements_prediction2_idx ON view_rules_campaign_placements (prediction2);'),
    ]