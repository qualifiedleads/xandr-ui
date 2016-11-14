from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('rtb', '0103_lasttoken'),
    ]

    operations = [
        migrations.RunSQL(
            """
    CREATE MATERIALIZED VIEW
      ml_view_full_placements_data
    AS
      SELECT
        placement_id,
        SUM(imps) imps,
        SUM(clicks) clicks,
        SUM(total_convs) total_convs,
        SUM(imps_viewed) imps_viewed,
        SUM(view_measured_imps) view_measured_imps,
        SUM(cost) sum_cost,
        case SUM(total_convs) when 0 then 0 else SUM(cost)::float/SUM(total_convs) end cpa,
        case SUM(imps) when 0 then 0 else SUM(clicks)::float/SUM(imps) end ctr,
        case SUM(imps) when 0 then 0 else SUM(total_convs)::float/SUM(imps) end cvr,
        case SUM(clicks) when 0 then 0 else SUM(cost)::float/SUM(clicks) end cpc,
        case SUM(imps) when 0 then 0 else SUM(cost)::float/SUM(imps) end cpm,
        case SUM(view_measured_imps) when 0 then 0 else SUM(imps_viewed)::float/SUM(view_measured_imps) end view_rate,
        case SUM(imps) when 0 then 0 else SUM(view_measured_imps)::float/SUM(imps) end view_measurement_rate
      FROM
        network_analytics_report_by_placement
      GROUP BY
        placement_id
      HAVING
        COUNT(DISTINCT extract ( dow from hour)) = 7 and SUM(imps) >=1000;
    """),
        migrations.RunSQL('CREATE INDEX ml_view_full_placements_data__placement_id ON ml_view_full_placements_data (placement_id);'),
        migrations.RunSQL('CREATE INDEX ml_view_full_placements_data__imps ON ml_view_full_placements_data (imps);'),
    ]