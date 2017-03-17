from __future__ import unicode_literals

import django.contrib.postgres.fields.jsonb
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('rtb', '0153_auto_20170309_1140'),
    ]

    operations = [
        ##
        #PLACEMENTS GRID
        ##

        migrations.RunSQL("delete from ui_usual_placements_grid_data_all"),

        migrations.RunSQL("""
            insert into ui_usual_placements_grid_data_all as ut (
        campaign_id,
        placement_id,
        imps,
        clicks,
        spent,
        conversions,
        imps_viewed,
        view_measured_imps,
        cpm,
        cvr,
        ctr,
        cpc,
        cpa,
        view_measurement_rate,
        view_rate)
      select
        t.campaign_id,
        t.placement_id as id,
        sum(t.imps) imps,
        sum(t.clicks) clicks,
        sum(t."cost") spend,
        sum(t.total_convs) conversions,
        sum(t.imps_viewed) imps_viewed,
        sum(t.view_measured_imps) view_measured_imps,
        case sum(t.imps) when 0 then 0 else sum(t."cost") / sum(t.imps) * 1000.0 end cpm,
        case sum(t.imps) when 0 then 0 else sum(t.total_convs)::float / sum(t.imps) end cvr,
        case sum(t.imps) when 0 then 0 else sum(t.clicks)::float / sum(t.imps) end ctr,
        case sum(t.clicks) when 0 then 0 else sum(t."cost") / sum(t.clicks) end cpc,
        case sum(t.total_convs) when 0 then 0 else sum(t."cost") / sum(t.total_convs) end cpa,
        case sum(t.imps) when 0 then 0 else sum(t.view_measured_imps)::float / sum(t.imps) end view_measurement_rate,
        case sum(t.view_measured_imps) when 0 then 0 else sum(t.imps_viewed)::float / sum(t.view_measured_imps) end view_rate
      from
        network_analytics_report_by_placement t
      group by
        t.campaign_id, t.placement_id
                """),

        migrations.RunSQL("delete from ui_usual_placements_grid_data_yesterday"),

        migrations.RunSQL("""
                insert into ui_usual_placements_grid_data_yesterday as ut (
            campaign_id,
            placement_id,
            imps,
            clicks,
            spent,
            conversions,
            imps_viewed,
            view_measured_imps,
            cpm,
            cvr,
            ctr,
            cpc,
            cpa,
            view_measurement_rate,
            view_rate)
          select
            t.campaign_id,
            t.placement_id as id,
            sum(t.imps) imps,
            sum(t.clicks) clicks,
            sum(t."cost") spend,
            sum(t.total_convs) conversions,
            sum(t.imps_viewed) imps_viewed,
            sum(t.view_measured_imps) view_measured_imps,
            case sum(t.imps) when 0 then 0 else sum(t."cost") / sum(t.imps) * 1000.0 end cpm,
            case sum(t.imps) when 0 then 0 else sum(t.total_convs)::float / sum(t.imps) end cvr,
            case sum(t.imps) when 0 then 0 else sum(t.clicks)::float / sum(t.imps) end ctr,
            case sum(t.clicks) when 0 then 0 else sum(t."cost") / sum(t.clicks) end cpc,
            case sum(t.total_convs) when 0 then 0 else sum(t."cost") / sum(t.total_convs) end cpa,
            case sum(t.imps) when 0 then 0 else sum(t.view_measured_imps)::float / sum(t.imps) end view_measurement_rate,
            case sum(t.view_measured_imps) when 0 then 0 else sum(t.imps_viewed)::float / sum(t.view_measured_imps) end view_rate
          from
            network_analytics_report_by_placement t
          where
            t."hour" >= date_trunc('day',(select max(hour) from network_analytics_report_by_placement) - interval '1 day')
          group by
            t.campaign_id, t.placement_id
                    """),

        migrations.RunSQL("delete from ui_usual_placements_grid_data_last_3_days"),

        migrations.RunSQL("""
                    insert into ui_usual_placements_grid_data_last_3_days as ut (
                campaign_id,
                placement_id,
                imps,
                clicks,
                spent,
                conversions,
                imps_viewed,
                view_measured_imps,
                cpm,
                cvr,
                ctr,
                cpc,
                cpa,
                view_measurement_rate,
                view_rate)
              select
                t.campaign_id,
                t.placement_id as id,
                sum(t.imps) imps,
                sum(t.clicks) clicks,
                sum(t."cost") spend,
                sum(t.total_convs) conversions,
                sum(t.imps_viewed) imps_viewed,
                sum(t.view_measured_imps) view_measured_imps,
                case sum(t.imps) when 0 then 0 else sum(t."cost") / sum(t.imps) * 1000.0 end cpm,
                case sum(t.imps) when 0 then 0 else sum(t.total_convs)::float / sum(t.imps) end cvr,
                case sum(t.imps) when 0 then 0 else sum(t.clicks)::float / sum(t.imps) end ctr,
                case sum(t.clicks) when 0 then 0 else sum(t."cost") / sum(t.clicks) end cpc,
                case sum(t.total_convs) when 0 then 0 else sum(t."cost") / sum(t.total_convs) end cpa,
                case sum(t.imps) when 0 then 0 else sum(t.view_measured_imps)::float / sum(t.imps) end view_measurement_rate,
                case sum(t.view_measured_imps) when 0 then 0 else sum(t.imps_viewed)::float / sum(t.view_measured_imps) end view_rate
              from
                network_analytics_report_by_placement t
              where
                t."hour" >= date_trunc('day',(select max(hour) from network_analytics_report_by_placement) - interval '3 day')
              group by
                t.campaign_id, t.placement_id
                        """),

        migrations.RunSQL("delete from ui_usual_placements_grid_data_last_7_days"),

        migrations.RunSQL("""
                    insert into ui_usual_placements_grid_data_last_7_days as ut (
                campaign_id,
                placement_id,
                imps,
                clicks,
                spent,
                conversions,
                imps_viewed,
                view_measured_imps,
                cpm,
                cvr,
                ctr,
                cpc,
                cpa,
                view_measurement_rate,
                view_rate)
              select
                t.campaign_id,
                t.placement_id as id,
                sum(t.imps) imps,
                sum(t.clicks) clicks,
                sum(t."cost") spend,
                sum(t.total_convs) conversions,
                sum(t.imps_viewed) imps_viewed,
                sum(t.view_measured_imps) view_measured_imps,
                case sum(t.imps) when 0 then 0 else sum(t."cost") / sum(t.imps) * 1000.0 end cpm,
                case sum(t.imps) when 0 then 0 else sum(t.total_convs)::float / sum(t.imps) end cvr,
                case sum(t.imps) when 0 then 0 else sum(t.clicks)::float / sum(t.imps) end ctr,
                case sum(t.clicks) when 0 then 0 else sum(t."cost") / sum(t.clicks) end cpc,
                case sum(t.total_convs) when 0 then 0 else sum(t."cost") / sum(t.total_convs) end cpa,
                case sum(t.imps) when 0 then 0 else sum(t.view_measured_imps)::float / sum(t.imps) end view_measurement_rate,
                case sum(t.view_measured_imps) when 0 then 0 else sum(t.imps_viewed)::float / sum(t.view_measured_imps) end view_rate
              from
                network_analytics_report_by_placement t
              where
                t."hour" >= date_trunc('day',(select max(hour) from network_analytics_report_by_placement) - interval '7 day')
              group by
                t.campaign_id, t.placement_id
                        """),

        migrations.RunSQL("delete from ui_usual_placements_grid_data_last_14_days"),

        migrations.RunSQL("""
                    insert into ui_usual_placements_grid_data_last_14_days as ut (
                campaign_id,
                placement_id,
                imps,
                clicks,
                spent,
                conversions,
                imps_viewed,
                view_measured_imps,
                cpm,
                cvr,
                ctr,
                cpc,
                cpa,
                view_measurement_rate,
                view_rate)
              select
                t.campaign_id,
                t.placement_id as id,
                sum(t.imps) imps,
                sum(t.clicks) clicks,
                sum(t."cost") spend,
                sum(t.total_convs) conversions,
                sum(t.imps_viewed) imps_viewed,
                sum(t.view_measured_imps) view_measured_imps,
                case sum(t.imps) when 0 then 0 else sum(t."cost") / sum(t.imps) * 1000.0 end cpm,
                case sum(t.imps) when 0 then 0 else sum(t.total_convs)::float / sum(t.imps) end cvr,
                case sum(t.imps) when 0 then 0 else sum(t.clicks)::float / sum(t.imps) end ctr,
                case sum(t.clicks) when 0 then 0 else sum(t."cost") / sum(t.clicks) end cpc,
                case sum(t.total_convs) when 0 then 0 else sum(t."cost") / sum(t.total_convs) end cpa,
                case sum(t.imps) when 0 then 0 else sum(t.view_measured_imps)::float / sum(t.imps) end view_measurement_rate,
                case sum(t.view_measured_imps) when 0 then 0 else sum(t.imps_viewed)::float / sum(t.view_measured_imps) end view_rate
              from
                network_analytics_report_by_placement t
              where
                t."hour" >= date_trunc('day',(select max(hour) from network_analytics_report_by_placement) - interval '14 day')
              group by
                t.campaign_id, t.placement_id
                        """),

        migrations.RunSQL("delete from ui_usual_placements_grid_data_last_21_days"),

        migrations.RunSQL("""
                    insert into ui_usual_placements_grid_data_last_21_days as ut (
                campaign_id,
                placement_id,
                imps,
                clicks,
                spent,
                conversions,
                imps_viewed,
                view_measured_imps,
                cpm,
                cvr,
                ctr,
                cpc,
                cpa,
                view_measurement_rate,
                view_rate)
              select
                t.campaign_id,
                t.placement_id as id,
                sum(t.imps) imps,
                sum(t.clicks) clicks,
                sum(t."cost") spend,
                sum(t.total_convs) conversions,
                sum(t.imps_viewed) imps_viewed,
                sum(t.view_measured_imps) view_measured_imps,
                case sum(t.imps) when 0 then 0 else sum(t."cost") / sum(t.imps) * 1000.0 end cpm,
                case sum(t.imps) when 0 then 0 else sum(t.total_convs)::float / sum(t.imps) end cvr,
                case sum(t.imps) when 0 then 0 else sum(t.clicks)::float / sum(t.imps) end ctr,
                case sum(t.clicks) when 0 then 0 else sum(t."cost") / sum(t.clicks) end cpc,
                case sum(t.total_convs) when 0 then 0 else sum(t."cost") / sum(t.total_convs) end cpa,
                case sum(t.imps) when 0 then 0 else sum(t.view_measured_imps)::float / sum(t.imps) end view_measurement_rate,
                case sum(t.view_measured_imps) when 0 then 0 else sum(t.imps_viewed)::float / sum(t.view_measured_imps) end view_rate
              from
                network_analytics_report_by_placement t
              where
                t."hour" >= date_trunc('day',(select max(hour) from network_analytics_report_by_placement) - interval '21 day')
              group by
                t.campaign_id, t.placement_id
                        """),

        migrations.RunSQL("delete from ui_usual_placements_grid_data_last_90_days"),

        migrations.RunSQL("""
                    insert into ui_usual_placements_grid_data_last_90_days as ut (
                campaign_id,
                placement_id,
                imps,
                clicks,
                spent,
                conversions,
                imps_viewed,
                view_measured_imps,
                cpm,
                cvr,
                ctr,
                cpc,
                cpa,
                view_measurement_rate,
                view_rate)
              select
                t.campaign_id,
                t.placement_id as id,
                sum(t.imps) imps,
                sum(t.clicks) clicks,
                sum(t."cost") spend,
                sum(t.total_convs) conversions,
                sum(t.imps_viewed) imps_viewed,
                sum(t.view_measured_imps) view_measured_imps,
                case sum(t.imps) when 0 then 0 else sum(t."cost") / sum(t.imps) * 1000.0 end cpm,
                case sum(t.imps) when 0 then 0 else sum(t.total_convs)::float / sum(t.imps) end cvr,
                case sum(t.imps) when 0 then 0 else sum(t.clicks)::float / sum(t.imps) end ctr,
                case sum(t.clicks) when 0 then 0 else sum(t."cost") / sum(t.clicks) end cpc,
                case sum(t.total_convs) when 0 then 0 else sum(t."cost") / sum(t.total_convs) end cpa,
                case sum(t.imps) when 0 then 0 else sum(t.view_measured_imps)::float / sum(t.imps) end view_measurement_rate,
                case sum(t.view_measured_imps) when 0 then 0 else sum(t.imps_viewed)::float / sum(t.view_measured_imps) end view_rate
              from
                network_analytics_report_by_placement t
              where
                t."hour" >= date_trunc('day',(select max(hour) from network_analytics_report_by_placement) - interval '90 day')
              group by
                t.campaign_id, t.placement_id
                        """),

        migrations.RunSQL("delete from ui_usual_placements_grid_data_last_month"),

        migrations.RunSQL("""
                    insert into ui_usual_placements_grid_data_last_month as ut (
                campaign_id,
                placement_id,
                imps,
                clicks,
                spent,
                conversions,
                imps_viewed,
                view_measured_imps,
                cpm,
                cvr,
                ctr,
                cpc,
                cpa,
                view_measurement_rate,
                view_rate)
              select
                t.campaign_id,
                t.placement_id as id,
                sum(t.imps) imps,
                sum(t.clicks) clicks,
                sum(t."cost") spend,
                sum(t.total_convs) conversions,
                sum(t.imps_viewed) imps_viewed,
                sum(t.view_measured_imps) view_measured_imps,
                case sum(t.imps) when 0 then 0 else sum(t."cost") / sum(t.imps) * 1000.0 end cpm,
                case sum(t.imps) when 0 then 0 else sum(t.total_convs)::float / sum(t.imps) end cvr,
                case sum(t.imps) when 0 then 0 else sum(t.clicks)::float / sum(t.imps) end ctr,
                case sum(t.clicks) when 0 then 0 else sum(t."cost") / sum(t.clicks) end cpc,
                case sum(t.total_convs) when 0 then 0 else sum(t."cost") / sum(t.total_convs) end cpa,
                case sum(t.imps) when 0 then 0 else sum(t.view_measured_imps)::float / sum(t.imps) end view_measurement_rate,
                case sum(t.view_measured_imps) when 0 then 0 else sum(t.imps_viewed)::float / sum(t.view_measured_imps) end view_rate
              from
                network_analytics_report_by_placement t
              where
                t."hour" >= date_trunc('month',(select max(hour) from network_analytics_report_by_placement) - interval '1 month')
                and t."hour" < date_trunc('month',(select max(hour) from network_analytics_report_by_placement))
              group by
                t.campaign_id, t.placement_id
                        """),

        migrations.RunSQL("delete from ui_usual_placements_grid_data_cur_month"),

        migrations.RunSQL("""
                    insert into ui_usual_placements_grid_data_cur_month as ut (
                campaign_id,
                placement_id,
                imps,
                clicks,
                spent,
                conversions,
                imps_viewed,
                view_measured_imps,
                cpm,
                cvr,
                ctr,
                cpc,
                cpa,
                view_measurement_rate,
                view_rate)
              select
                t.campaign_id,
                t.placement_id as id,
                sum(t.imps) imps,
                sum(t.clicks) clicks,
                sum(t."cost") spend,
                sum(t.total_convs) conversions,
                sum(t.imps_viewed) imps_viewed,
                sum(t.view_measured_imps) view_measured_imps,
                case sum(t.imps) when 0 then 0 else sum(t."cost") / sum(t.imps) * 1000.0 end cpm,
                case sum(t.imps) when 0 then 0 else sum(t.total_convs)::float / sum(t.imps) end cvr,
                case sum(t.imps) when 0 then 0 else sum(t.clicks)::float / sum(t.imps) end ctr,
                case sum(t.clicks) when 0 then 0 else sum(t."cost") / sum(t.clicks) end cpc,
                case sum(t.total_convs) when 0 then 0 else sum(t."cost") / sum(t.total_convs) end cpa,
                case sum(t.imps) when 0 then 0 else sum(t.view_measured_imps)::float / sum(t.imps) end view_measurement_rate,
                case sum(t.view_measured_imps) when 0 then 0 else sum(t.imps_viewed)::float / sum(t.view_measured_imps) end view_rate
              from
                network_analytics_report_by_placement t
              where
                t."hour" >= date_trunc('month',(select max(hour) from network_analytics_report_by_placement))
              group by
                t.campaign_id, t.placement_id
                        """),

        ##
        #CAMPAIGNS GRID
        ##

        migrations.RunSQL("delete from ui_usual_campaigns_grid_data_all"),

        migrations.RunSQL("""
    insert into ui_usual_campaigns_grid_data_all as ut (
        campaign_id,
        imps,
        clicks,
        spent,
        conversions,
        imps_viewed,
        view_measured_imps,
        cpm,
        cvr,
        ctr,
        cpc,
        view_measurement_rate,
        view_rate,
        day_chart)
      select
        page.campaign_id,
        page.imps,
        page.clicks,
        page.spent,
        page.conversions,
        page.imps_viewed,
        page.view_measured_imps,
        case coalesce(page.imps, 0) when 0 then 0 else coalesce(page.spent, 0) / coalesce(page.imps, 0) * 1000.0 end,
        case coalesce(page.imps, 0) when 0 then 0 else coalesce(page.conversions, 0)::float / coalesce(page.imps, 0) end,
        case coalesce(page.imps, 0) when 0 then 0 else coalesce(page.clicks, 0)::float / coalesce(page.imps, 0) end,
        case coalesce(page.clicks, 0) when 0 then 0 else coalesce(page.spent, 0) / coalesce(page.clicks, 0) end,
        case coalesce(page.imps, 0) when 0 then 0 else coalesce(page.view_measured_imps, 0)::float / coalesce(page.imps, 0) end,
        case coalesce(page.view_measured_imps, 0) when 0 then 0 else coalesce(page.imps_viewed, 0)::float / coalesce(page.view_measured_imps, 0) end,
        array_to_json(array((select
               json_build_object(
               'day', site_r.day,
               'imp', SUM(site_r.imps),
               'spend', SUM(site_r.media_cost),
               'clicks', SUM(site_r.clicks),
               'conversions', SUM(site_r.post_click_convs) + SUM(site_r.post_view_convs),
               'cvr', case SUM(site_r.imps) when 0 then 0 else (SUM(site_r.post_click_convs) + SUM(site_r.post_view_convs))::float/SUM(site_r.imps) end,
               'cpc', case SUM(site_r.clicks) when 0 then 0 else SUM(site_r.media_cost)::float/SUM(site_r.clicks) end,
               'ctr', case SUM(site_r.imps) when 0 then 0 else SUM(site_r.clicks)::float/SUM(site_r.imps) end)
             from site_domain_performance_report site_r
             where site_r.campaign_id=page.campaign_id
             group by site_r.campaign_id, site_r.day
             order by site_r.day))) id
    from (
          select distinct on (site_r1.campaign_id)
            site_r1.campaign_id,
            SUM(site_r1.imps) over (partition by site_r1.campaign_id) imps,
            SUM(site_r1.media_cost) over (partition by site_r1.campaign_id) spent,
            SUM(site_r1.clicks) over (partition by site_r1.campaign_id) clicks,
            (SUM(site_r1.post_view_convs) over (partition by site_r1.campaign_id) + SUM(site_r1.post_click_convs) over (partition by site_r1.campaign_id)) conversions,
            SUM(site_r1.imps_viewed) over (partition by site_r1.campaign_id) imps_viewed,
            SUM(site_r1.view_measured_imps) over (partition by site_r1.campaign_id) view_measured_imps
          from
            site_domain_performance_report site_r1
          WINDOW w as (partition by site_r1.campaign_id order by site_r1.day desc)
         ) page;
            """),

        migrations.RunSQL("delete from ui_usual_campaigns_grid_data_yesterday"),

        migrations.RunSQL("""
        insert into ui_usual_campaigns_grid_data_yesterday as ut (
            campaign_id,
            imps,
            clicks,
            spent,
            conversions,
            imps_viewed,
            view_measured_imps,
            cpm,
            cvr,
            ctr,
            cpc,
            view_measurement_rate,
            view_rate,
            day_chart)
          select
            page.campaign_id,
            page.imps,
            page.clicks,
            page.spent,
            page.conversions,
            page.imps_viewed,
            page.view_measured_imps,
            case coalesce(page.imps, 0) when 0 then 0 else coalesce(page.spent, 0) / coalesce(page.imps, 0) * 1000.0 end,
            case coalesce(page.imps, 0) when 0 then 0 else coalesce(page.conversions, 0)::float / coalesce(page.imps, 0) end,
            case coalesce(page.imps, 0) when 0 then 0 else coalesce(page.clicks, 0)::float / coalesce(page.imps, 0) end,
            case coalesce(page.clicks, 0) when 0 then 0 else coalesce(page.spent, 0) / coalesce(page.clicks, 0) end,
            case coalesce(page.imps, 0) when 0 then 0 else coalesce(page.view_measured_imps, 0)::float / coalesce(page.imps, 0) end,
            case coalesce(page.view_measured_imps, 0) when 0 then 0 else coalesce(page.imps_viewed, 0)::float / coalesce(page.view_measured_imps, 0) end,
            array_to_json(array((select
                   json_build_object(
                   'day', site_r.day,
                   'imp', SUM(site_r.imps),
                   'spend', SUM(site_r.media_cost),
                   'clicks', SUM(site_r.clicks),
                   'conversions', SUM(site_r.post_click_convs) + SUM(site_r.post_view_convs),
                   'cvr', case SUM(site_r.imps) when 0 then 0 else (SUM(site_r.post_click_convs) + SUM(site_r.post_view_convs))::float/SUM(site_r.imps) end,
                   'cpc', case SUM(site_r.clicks) when 0 then 0 else SUM(site_r.media_cost)::float/SUM(site_r.clicks) end,
                   'ctr', case SUM(site_r.imps) when 0 then 0 else SUM(site_r.clicks)::float/SUM(site_r.imps) end)
                 from site_domain_performance_report site_r
                 where site_r.campaign_id=page.campaign_id
                   and
                   site_r.hour >= date_trunc('day',(select max(hour) from site_domain_performance_report) - interval '1 day')
                 group by site_r.campaign_id, site_r.day
                 order by site_r.day))) id
        from (
              select distinct on (site_r1.campaign_id)
                site_r1.campaign_id,
                SUM(site_r1.imps) over (partition by site_r1.campaign_id) imps,
                SUM(site_r1.media_cost) over (partition by site_r1.campaign_id) spent,
                SUM(site_r1.clicks) over (partition by site_r1.campaign_id) clicks,
                (SUM(site_r1.post_view_convs) over (partition by site_r1.campaign_id) + SUM(site_r1.post_click_convs) over (partition by site_r1.campaign_id)) conversions,
                SUM(site_r1.imps_viewed) over (partition by site_r1.campaign_id) imps_viewed,
                SUM(site_r1.view_measured_imps) over (partition by site_r1.campaign_id) view_measured_imps
              from
                site_domain_performance_report site_r1
              where
                site_r1.hour >= date_trunc('day',(select max(hour) from site_domain_performance_report) - interval '1 day')
              WINDOW w as (partition by site_r1.campaign_id order by site_r1.day desc)
             ) page;
                """),

        migrations.RunSQL("delete from ui_usual_campaigns_grid_data_last_3_days"),

        migrations.RunSQL("""
        insert into ui_usual_campaigns_grid_data_last_3_days as ut (
            campaign_id,
            imps,
            clicks,
            spent,
            conversions,
            imps_viewed,
            view_measured_imps,
            cpm,
            cvr,
            ctr,
            cpc,
            view_measurement_rate,
            view_rate,
            day_chart)
          select
            page.campaign_id,
            page.imps,
            page.clicks,
            page.spent,
            page.conversions,
            page.imps_viewed,
            page.view_measured_imps,
            case coalesce(page.imps, 0) when 0 then 0 else coalesce(page.spent, 0) / coalesce(page.imps, 0) * 1000.0 end,
            case coalesce(page.imps, 0) when 0 then 0 else coalesce(page.conversions, 0)::float / coalesce(page.imps, 0) end,
            case coalesce(page.imps, 0) when 0 then 0 else coalesce(page.clicks, 0)::float / coalesce(page.imps, 0) end,
            case coalesce(page.clicks, 0) when 0 then 0 else coalesce(page.spent, 0) / coalesce(page.clicks, 0) end,
            case coalesce(page.imps, 0) when 0 then 0 else coalesce(page.view_measured_imps, 0)::float / coalesce(page.imps, 0) end,
            case coalesce(page.view_measured_imps, 0) when 0 then 0 else coalesce(page.imps_viewed, 0)::float / coalesce(page.view_measured_imps, 0) end,
            array_to_json(array((select
                   json_build_object(
                   'day', site_r.day,
                   'imp', SUM(site_r.imps),
                   'spend', SUM(site_r.media_cost),
                   'clicks', SUM(site_r.clicks),
                   'conversions', SUM(site_r.post_click_convs) + SUM(site_r.post_view_convs),
                   'cvr', case SUM(site_r.imps) when 0 then 0 else (SUM(site_r.post_click_convs) + SUM(site_r.post_view_convs))::float/SUM(site_r.imps) end,
                   'cpc', case SUM(site_r.clicks) when 0 then 0 else SUM(site_r.media_cost)::float/SUM(site_r.clicks) end,
                   'ctr', case SUM(site_r.imps) when 0 then 0 else SUM(site_r.clicks)::float/SUM(site_r.imps) end)
                 from site_domain_performance_report site_r
                 where site_r.campaign_id=page.campaign_id
                   and
                   site_r.hour >= date_trunc('day',(select max(hour) from site_domain_performance_report) - interval '3 day')
                 group by site_r.campaign_id, site_r.day
                 order by site_r.day))) id
        from (
              select distinct on (site_r1.campaign_id)
                site_r1.campaign_id,
                SUM(site_r1.imps) over (partition by site_r1.campaign_id) imps,
                SUM(site_r1.media_cost) over (partition by site_r1.campaign_id) spent,
                SUM(site_r1.clicks) over (partition by site_r1.campaign_id) clicks,
                (SUM(site_r1.post_view_convs) over (partition by site_r1.campaign_id) + SUM(site_r1.post_click_convs) over (partition by site_r1.campaign_id)) conversions,
                SUM(site_r1.imps_viewed) over (partition by site_r1.campaign_id) imps_viewed,
                SUM(site_r1.view_measured_imps) over (partition by site_r1.campaign_id) view_measured_imps
              from
                site_domain_performance_report site_r1
              where
                site_r1.hour >= date_trunc('day',(select max(hour) from site_domain_performance_report) - interval '3 day')
              WINDOW w as (partition by site_r1.campaign_id order by site_r1.day desc)
             ) page;
                """),

        migrations.RunSQL("delete from ui_usual_campaigns_grid_data_last_7_days"),

        migrations.RunSQL("""
        insert into ui_usual_campaigns_grid_data_last_7_days as ut (
            campaign_id,
            imps,
            clicks,
            spent,
            conversions,
            imps_viewed,
            view_measured_imps,
            cpm,
            cvr,
            ctr,
            cpc,
            view_measurement_rate,
            view_rate,
            day_chart)
          select
            page.campaign_id,
            page.imps,
            page.clicks,
            page.spent,
            page.conversions,
            page.imps_viewed,
            page.view_measured_imps,
            case coalesce(page.imps, 0) when 0 then 0 else coalesce(page.spent, 0) / coalesce(page.imps, 0) * 1000.0 end,
            case coalesce(page.imps, 0) when 0 then 0 else coalesce(page.conversions, 0)::float / coalesce(page.imps, 0) end,
            case coalesce(page.imps, 0) when 0 then 0 else coalesce(page.clicks, 0)::float / coalesce(page.imps, 0) end,
            case coalesce(page.clicks, 0) when 0 then 0 else coalesce(page.spent, 0) / coalesce(page.clicks, 0) end,
            case coalesce(page.imps, 0) when 0 then 0 else coalesce(page.view_measured_imps, 0)::float / coalesce(page.imps, 0) end,
            case coalesce(page.view_measured_imps, 0) when 0 then 0 else coalesce(page.imps_viewed, 0)::float / coalesce(page.view_measured_imps, 0) end,
            array_to_json(array((select
                   json_build_object(
                   'day', site_r.day,
                   'imp', SUM(site_r.imps),
                   'spend', SUM(site_r.media_cost),
                   'clicks', SUM(site_r.clicks),
                   'conversions', SUM(site_r.post_click_convs) + SUM(site_r.post_view_convs),
                   'cvr', case SUM(site_r.imps) when 0 then 0 else (SUM(site_r.post_click_convs) + SUM(site_r.post_view_convs))::float/SUM(site_r.imps) end,
                   'cpc', case SUM(site_r.clicks) when 0 then 0 else SUM(site_r.media_cost)::float/SUM(site_r.clicks) end,
                   'ctr', case SUM(site_r.imps) when 0 then 0 else SUM(site_r.clicks)::float/SUM(site_r.imps) end)
                 from site_domain_performance_report site_r
                 where site_r.campaign_id=page.campaign_id
                   and
                   site_r.hour >= date_trunc('day',(select max(hour) from site_domain_performance_report) - interval '7 day')
                 group by site_r.campaign_id, site_r.day
                 order by site_r.day))) id
        from (
              select distinct on (site_r1.campaign_id)
                site_r1.campaign_id,
                SUM(site_r1.imps) over (partition by site_r1.campaign_id) imps,
                SUM(site_r1.media_cost) over (partition by site_r1.campaign_id) spent,
                SUM(site_r1.clicks) over (partition by site_r1.campaign_id) clicks,
                (SUM(site_r1.post_view_convs) over (partition by site_r1.campaign_id) + SUM(site_r1.post_click_convs) over (partition by site_r1.campaign_id)) conversions,
                SUM(site_r1.imps_viewed) over (partition by site_r1.campaign_id) imps_viewed,
                SUM(site_r1.view_measured_imps) over (partition by site_r1.campaign_id) view_measured_imps
              from
                site_domain_performance_report site_r1
              where
                site_r1.hour >= date_trunc('day',(select max(hour) from site_domain_performance_report) - interval '7 day')
              WINDOW w as (partition by site_r1.campaign_id order by site_r1.day desc)
             ) page;
                """),

        migrations.RunSQL("delete from ui_usual_campaigns_grid_data_last_14_days"),

        migrations.RunSQL("""
        insert into ui_usual_campaigns_grid_data_last_14_days as ut (
            campaign_id,
            imps,
            clicks,
            spent,
            conversions,
            imps_viewed,
            view_measured_imps,
            cpm,
            cvr,
            ctr,
            cpc,
            view_measurement_rate,
            view_rate,
            day_chart)
          select
            page.campaign_id,
            page.imps,
            page.clicks,
            page.spent,
            page.conversions,
            page.imps_viewed,
            page.view_measured_imps,
            case coalesce(page.imps, 0) when 0 then 0 else coalesce(page.spent, 0) / coalesce(page.imps, 0) * 1000.0 end,
            case coalesce(page.imps, 0) when 0 then 0 else coalesce(page.conversions, 0)::float / coalesce(page.imps, 0) end,
            case coalesce(page.imps, 0) when 0 then 0 else coalesce(page.clicks, 0)::float / coalesce(page.imps, 0) end,
            case coalesce(page.clicks, 0) when 0 then 0 else coalesce(page.spent, 0) / coalesce(page.clicks, 0) end,
            case coalesce(page.imps, 0) when 0 then 0 else coalesce(page.view_measured_imps, 0)::float / coalesce(page.imps, 0) end,
            case coalesce(page.view_measured_imps, 0) when 0 then 0 else coalesce(page.imps_viewed, 0)::float / coalesce(page.view_measured_imps, 0) end,
            array_to_json(array((select
                   json_build_object(
                   'day', site_r.day,
                   'imp', SUM(site_r.imps),
                   'spend', SUM(site_r.media_cost),
                   'clicks', SUM(site_r.clicks),
                   'conversions', SUM(site_r.post_click_convs) + SUM(site_r.post_view_convs),
                   'cvr', case SUM(site_r.imps) when 0 then 0 else (SUM(site_r.post_click_convs) + SUM(site_r.post_view_convs))::float/SUM(site_r.imps) end,
                   'cpc', case SUM(site_r.clicks) when 0 then 0 else SUM(site_r.media_cost)::float/SUM(site_r.clicks) end,
                   'ctr', case SUM(site_r.imps) when 0 then 0 else SUM(site_r.clicks)::float/SUM(site_r.imps) end)
                 from site_domain_performance_report site_r
                 where site_r.campaign_id=page.campaign_id
                   and
                   site_r.hour >= date_trunc('day',(select max(hour) from site_domain_performance_report) - interval '14 day')
                 group by site_r.campaign_id, site_r.day
                 order by site_r.day))) id
        from (
              select distinct on (site_r1.campaign_id)
                site_r1.campaign_id,
                SUM(site_r1.imps) over (partition by site_r1.campaign_id) imps,
                SUM(site_r1.media_cost) over (partition by site_r1.campaign_id) spent,
                SUM(site_r1.clicks) over (partition by site_r1.campaign_id) clicks,
                (SUM(site_r1.post_view_convs) over (partition by site_r1.campaign_id) + SUM(site_r1.post_click_convs) over (partition by site_r1.campaign_id)) conversions,
                SUM(site_r1.imps_viewed) over (partition by site_r1.campaign_id) imps_viewed,
                SUM(site_r1.view_measured_imps) over (partition by site_r1.campaign_id) view_measured_imps
              from
                site_domain_performance_report site_r1
              where
                site_r1.hour >= date_trunc('day',(select max(hour) from site_domain_performance_report) - interval '14 day')
              WINDOW w as (partition by site_r1.campaign_id order by site_r1.day desc)
             ) page;
                """),

        migrations.RunSQL("delete from ui_usual_campaigns_grid_data_last_21_days"),

        migrations.RunSQL("""
        insert into ui_usual_campaigns_grid_data_last_21_days as ut (
            campaign_id,
            imps,
            clicks,
            spent,
            conversions,
            imps_viewed,
            view_measured_imps,
            cpm,
            cvr,
            ctr,
            cpc,
            view_measurement_rate,
            view_rate,
            day_chart)
          select
            page.campaign_id,
            page.imps,
            page.clicks,
            page.spent,
            page.conversions,
            page.imps_viewed,
            page.view_measured_imps,
            case coalesce(page.imps, 0) when 0 then 0 else coalesce(page.spent, 0) / coalesce(page.imps, 0) * 1000.0 end,
            case coalesce(page.imps, 0) when 0 then 0 else coalesce(page.conversions, 0)::float / coalesce(page.imps, 0) end,
            case coalesce(page.imps, 0) when 0 then 0 else coalesce(page.clicks, 0)::float / coalesce(page.imps, 0) end,
            case coalesce(page.clicks, 0) when 0 then 0 else coalesce(page.spent, 0) / coalesce(page.clicks, 0) end,
            case coalesce(page.imps, 0) when 0 then 0 else coalesce(page.view_measured_imps, 0)::float / coalesce(page.imps, 0) end,
            case coalesce(page.view_measured_imps, 0) when 0 then 0 else coalesce(page.imps_viewed, 0)::float / coalesce(page.view_measured_imps, 0) end,
            array_to_json(array((select
                   json_build_object(
                   'day', site_r.day,
                   'imp', SUM(site_r.imps),
                   'spend', SUM(site_r.media_cost),
                   'clicks', SUM(site_r.clicks),
                   'conversions', SUM(site_r.post_click_convs) + SUM(site_r.post_view_convs),
                   'cvr', case SUM(site_r.imps) when 0 then 0 else (SUM(site_r.post_click_convs) + SUM(site_r.post_view_convs))::float/SUM(site_r.imps) end,
                   'cpc', case SUM(site_r.clicks) when 0 then 0 else SUM(site_r.media_cost)::float/SUM(site_r.clicks) end,
                   'ctr', case SUM(site_r.imps) when 0 then 0 else SUM(site_r.clicks)::float/SUM(site_r.imps) end)
                 from site_domain_performance_report site_r
                 where site_r.campaign_id=page.campaign_id
                   and
                   site_r.hour >= date_trunc('day',(select max(hour) from site_domain_performance_report) - interval '21 day')
                 group by site_r.campaign_id, site_r.day
                 order by site_r.day))) id
        from (
              select distinct on (site_r1.campaign_id)
                site_r1.campaign_id,
                SUM(site_r1.imps) over (partition by site_r1.campaign_id) imps,
                SUM(site_r1.media_cost) over (partition by site_r1.campaign_id) spent,
                SUM(site_r1.clicks) over (partition by site_r1.campaign_id) clicks,
                (SUM(site_r1.post_view_convs) over (partition by site_r1.campaign_id) + SUM(site_r1.post_click_convs) over (partition by site_r1.campaign_id)) conversions,
                SUM(site_r1.imps_viewed) over (partition by site_r1.campaign_id) imps_viewed,
                SUM(site_r1.view_measured_imps) over (partition by site_r1.campaign_id) view_measured_imps
              from
                site_domain_performance_report site_r1
              where
                site_r1.hour >= date_trunc('day',(select max(hour) from site_domain_performance_report) - interval '21 day')
              WINDOW w as (partition by site_r1.campaign_id order by site_r1.day desc)
             ) page;
                """),

        migrations.RunSQL("delete from ui_usual_campaigns_grid_data_last_90_days"),

        migrations.RunSQL("""
        insert into ui_usual_campaigns_grid_data_last_90_days as ut (
            campaign_id,
            imps,
            clicks,
            spent,
            conversions,
            imps_viewed,
            view_measured_imps,
            cpm,
            cvr,
            ctr,
            cpc,
            view_measurement_rate,
            view_rate,
            day_chart)
          select
            page.campaign_id,
            page.imps,
            page.clicks,
            page.spent,
            page.conversions,
            page.imps_viewed,
            page.view_measured_imps,
            case coalesce(page.imps, 0) when 0 then 0 else coalesce(page.spent, 0) / coalesce(page.imps, 0) * 1000.0 end,
            case coalesce(page.imps, 0) when 0 then 0 else coalesce(page.conversions, 0)::float / coalesce(page.imps, 0) end,
            case coalesce(page.imps, 0) when 0 then 0 else coalesce(page.clicks, 0)::float / coalesce(page.imps, 0) end,
            case coalesce(page.clicks, 0) when 0 then 0 else coalesce(page.spent, 0) / coalesce(page.clicks, 0) end,
            case coalesce(page.imps, 0) when 0 then 0 else coalesce(page.view_measured_imps, 0)::float / coalesce(page.imps, 0) end,
            case coalesce(page.view_measured_imps, 0) when 0 then 0 else coalesce(page.imps_viewed, 0)::float / coalesce(page.view_measured_imps, 0) end,
            array_to_json(array((select
                   json_build_object(
                   'day', site_r.day,
                   'imp', SUM(site_r.imps),
                   'spend', SUM(site_r.media_cost),
                   'clicks', SUM(site_r.clicks),
                   'conversions', SUM(site_r.post_click_convs) + SUM(site_r.post_view_convs),
                   'cvr', case SUM(site_r.imps) when 0 then 0 else (SUM(site_r.post_click_convs) + SUM(site_r.post_view_convs))::float/SUM(site_r.imps) end,
                   'cpc', case SUM(site_r.clicks) when 0 then 0 else SUM(site_r.media_cost)::float/SUM(site_r.clicks) end,
                   'ctr', case SUM(site_r.imps) when 0 then 0 else SUM(site_r.clicks)::float/SUM(site_r.imps) end)
                 from site_domain_performance_report site_r
                 where site_r.campaign_id=page.campaign_id
                   and (
                   site_r.hour >= date_trunc('day',(select max(hour) from site_domain_performance_report) - interval '90 day')
                   or
                   site_r.day >= date_trunc('day',(select max(hour) from site_domain_performance_report) - interval '90 day'))
                 group by site_r.campaign_id, site_r.day
                 order by site_r.day))) id
        from (
              select distinct on (site_r1.campaign_id)
                site_r1.campaign_id,
                SUM(site_r1.imps) over (partition by site_r1.campaign_id) imps,
                SUM(site_r1.media_cost) over (partition by site_r1.campaign_id) spent,
                SUM(site_r1.clicks) over (partition by site_r1.campaign_id) clicks,
                (SUM(site_r1.post_view_convs) over (partition by site_r1.campaign_id) + SUM(site_r1.post_click_convs) over (partition by site_r1.campaign_id)) conversions,
                SUM(site_r1.imps_viewed) over (partition by site_r1.campaign_id) imps_viewed,
                SUM(site_r1.view_measured_imps) over (partition by site_r1.campaign_id) view_measured_imps
              from
                site_domain_performance_report site_r1
              where
                site_r1.hour >= date_trunc('day',(select max(hour) from site_domain_performance_report) - interval '90 day')
                or
                site_r1.day >= date_trunc('day',(select max(hour) from site_domain_performance_report) - interval '90 day')
              WINDOW w as (partition by site_r1.campaign_id order by site_r1.day desc)
             ) page;
                """),

        migrations.RunSQL("delete from ui_usual_campaigns_grid_data_last_month"),

        migrations.RunSQL("""
            insert into ui_usual_campaigns_grid_data_last_month as ut (
                campaign_id,
                imps,
                clicks,
                spent,
                conversions,
                imps_viewed,
                view_measured_imps,
                cpm,
                cvr,
                ctr,
                cpc,
                view_measurement_rate,
                view_rate,
                day_chart)
              select
                page.campaign_id,
                page.imps,
                page.clicks,
                page.spent,
                page.conversions,
                page.imps_viewed,
                page.view_measured_imps,
                case coalesce(page.imps, 0) when 0 then 0 else coalesce(page.spent, 0) / coalesce(page.imps, 0) * 1000.0 end,
                case coalesce(page.imps, 0) when 0 then 0 else coalesce(page.conversions, 0)::float / coalesce(page.imps, 0) end,
                case coalesce(page.imps, 0) when 0 then 0 else coalesce(page.clicks, 0)::float / coalesce(page.imps, 0) end,
                case coalesce(page.clicks, 0) when 0 then 0 else coalesce(page.spent, 0) / coalesce(page.clicks, 0) end,
                case coalesce(page.imps, 0) when 0 then 0 else coalesce(page.view_measured_imps, 0)::float / coalesce(page.imps, 0) end,
                case coalesce(page.view_measured_imps, 0) when 0 then 0 else coalesce(page.imps_viewed, 0)::float / coalesce(page.view_measured_imps, 0) end,
                array_to_json(array((select
                       json_build_object(
                       'day', site_r.day,
                       'imp', SUM(site_r.imps),
                       'spend', SUM(site_r.media_cost),
                       'clicks', SUM(site_r.clicks),
                       'conversions', SUM(site_r.post_click_convs) + SUM(site_r.post_view_convs),
                       'cvr', case SUM(site_r.imps) when 0 then 0 else (SUM(site_r.post_click_convs) + SUM(site_r.post_view_convs))::float/SUM(site_r.imps) end,
                       'cpc', case SUM(site_r.clicks) when 0 then 0 else SUM(site_r.media_cost)::float/SUM(site_r.clicks) end,
                       'ctr', case SUM(site_r.imps) when 0 then 0 else SUM(site_r.clicks)::float/SUM(site_r.imps) end)
                     from site_domain_performance_report site_r
                     where site_r.campaign_id=page.campaign_id
                       and
                       site_r.hour >= date_trunc('month',(select max(hour) from site_domain_performance_report) - interval '1 month')
                       and site_r.hour < date_trunc('month',(select max(hour) from site_domain_performance_report))
                     group by site_r.campaign_id, site_r.day
                     order by site_r.day))) id
            from (
                  select distinct on (site_r1.campaign_id)
                    site_r1.campaign_id,
                    SUM(site_r1.imps) over (partition by site_r1.campaign_id) imps,
                    SUM(site_r1.media_cost) over (partition by site_r1.campaign_id) spent,
                    SUM(site_r1.clicks) over (partition by site_r1.campaign_id) clicks,
                    (SUM(site_r1.post_view_convs) over (partition by site_r1.campaign_id) + SUM(site_r1.post_click_convs) over (partition by site_r1.campaign_id)) conversions,
                    SUM(site_r1.imps_viewed) over (partition by site_r1.campaign_id) imps_viewed,
                    SUM(site_r1.view_measured_imps) over (partition by site_r1.campaign_id) view_measured_imps
                  from
                    site_domain_performance_report site_r1
                  where
                    site_r1.hour >= date_trunc('month',(select max(hour) from site_domain_performance_report) - interval '1 month')
                    and site_r1.hour < date_trunc('month',(select max(hour) from site_domain_performance_report))
                  WINDOW w as (partition by site_r1.campaign_id order by site_r1.day desc)
                 ) page;
                    """),

        migrations.RunSQL("delete from ui_usual_campaigns_grid_data_cur_month"),

        migrations.RunSQL("""
            insert into ui_usual_campaigns_grid_data_cur_month as ut (
                campaign_id,
                imps,
                clicks,
                spent,
                conversions,
                imps_viewed,
                view_measured_imps,
                cpm,
                cvr,
                ctr,
                cpc,
                view_measurement_rate,
                view_rate,
                day_chart)
              select
                page.campaign_id,
                page.imps,
                page.clicks,
                page.spent,
                page.conversions,
                page.imps_viewed,
                page.view_measured_imps,
                case coalesce(page.imps, 0) when 0 then 0 else coalesce(page.spent, 0) / coalesce(page.imps, 0) * 1000.0 end,
                case coalesce(page.imps, 0) when 0 then 0 else coalesce(page.conversions, 0)::float / coalesce(page.imps, 0) end,
                case coalesce(page.imps, 0) when 0 then 0 else coalesce(page.clicks, 0)::float / coalesce(page.imps, 0) end,
                case coalesce(page.clicks, 0) when 0 then 0 else coalesce(page.spent, 0) / coalesce(page.clicks, 0) end,
                case coalesce(page.imps, 0) when 0 then 0 else coalesce(page.view_measured_imps, 0)::float / coalesce(page.imps, 0) end,
                case coalesce(page.view_measured_imps, 0) when 0 then 0 else coalesce(page.imps_viewed, 0)::float / coalesce(page.view_measured_imps, 0) end,
                array_to_json(array((select
                       json_build_object(
                       'day', site_r.day,
                       'imp', SUM(site_r.imps),
                       'spend', SUM(site_r.media_cost),
                       'clicks', SUM(site_r.clicks),
                       'conversions', SUM(site_r.post_click_convs) + SUM(site_r.post_view_convs),
                       'cvr', case SUM(site_r.imps) when 0 then 0 else (SUM(site_r.post_click_convs) + SUM(site_r.post_view_convs))::float/SUM(site_r.imps) end,
                       'cpc', case SUM(site_r.clicks) when 0 then 0 else SUM(site_r.media_cost)::float/SUM(site_r.clicks) end,
                       'ctr', case SUM(site_r.imps) when 0 then 0 else SUM(site_r.clicks)::float/SUM(site_r.imps) end)
                     from site_domain_performance_report site_r
                     where site_r.campaign_id=page.campaign_id
                       and
                       site_r.hour >= date_trunc('month',(select max(hour) from site_domain_performance_report))
                     group by site_r.campaign_id, site_r.day
                     order by site_r.day))) id
            from (
                  select distinct on (site_r1.campaign_id)
                    site_r1.campaign_id,
                    SUM(site_r1.imps) over (partition by site_r1.campaign_id) imps,
                    SUM(site_r1.media_cost) over (partition by site_r1.campaign_id) spent,
                    SUM(site_r1.clicks) over (partition by site_r1.campaign_id) clicks,
                    (SUM(site_r1.post_view_convs) over (partition by site_r1.campaign_id) + SUM(site_r1.post_click_convs) over (partition by site_r1.campaign_id)) conversions,
                    SUM(site_r1.imps_viewed) over (partition by site_r1.campaign_id) imps_viewed,
                    SUM(site_r1.view_measured_imps) over (partition by site_r1.campaign_id) view_measured_imps
                  from
                    site_domain_performance_report site_r1
                  where
                    site_r1.hour >= date_trunc('month',(select max(hour) from site_domain_performance_report))
                  WINDOW w as (partition by site_r1.campaign_id order by site_r1.day desc)
                 ) page;
                    """),

        ##
        #ADVERTISERS GRAPH
        ##

        migrations.RunSQL("delete from ui_usual_advertisers_graph"),

        migrations.RunSQL("""
      insert into ui_usual_advertisers_graph as ut (
        advertiser_id,
        type,
        day_chart)
      select
      ads.advertiser_id,
      'all',
      array_to_json(array(
        select json_build_object(
          'day', "day",
          'imp', sum(imps),
          'spend', sum(media_cost),
          'clicks', sum(clicks),
          'conversions', sum(post_click_convs) + sum(post_view_convs),
          'cvr', case sum(imps) when 0 then 0 else (sum(post_click_convs) + sum(post_view_convs)) / sum(imps)::float end,
          'cpc', case sum(clicks) when 0 then 0 else sum(media_cost) / sum(clicks) end,
          'ctr', case sum(imps) when 0 then 0 else sum(clicks)::float / sum(imps) end
        )
        from site_domain_performance_report tt
        where
          ads.advertiser_id=tt.advertiser_id
        group by "day"
        order by "day"
      ))
    from (select distinct advertiser_id from site_domain_performance_report)ads;
                            """),

        migrations.RunSQL("""
          insert into ui_usual_advertisers_graph as ut (
            advertiser_id,
            type,
            day_chart)
          select
          ads.advertiser_id,
          'yesterday',
          array_to_json(array(
            select json_build_object(
              'day', "day",
              'imp', sum(imps),
              'spend', sum(media_cost),
              'clicks', sum(clicks),
              'conversions', sum(post_click_convs) + sum(post_view_convs),
              'cvr', case sum(imps) when 0 then 0 else (sum(post_click_convs) + sum(post_view_convs)) / sum(imps)::float end,
              'cpc', case sum(clicks) when 0 then 0 else sum(media_cost) / sum(clicks) end,
              'ctr', case sum(imps) when 0 then 0 else sum(clicks)::float / sum(imps) end
            )
            from site_domain_performance_report tt
            where
              ads.advertiser_id=tt.advertiser_id
            and
              "hour" >= date_trunc('day',(select max(hour) from site_domain_performance_report) - interval '1 day')
            group by "day"
            order by "day"
          ))
        from (
               select distinct advertiser_id from site_domain_performance_report
                where
                "hour" >= date_trunc('day',(select max(hour) from site_domain_performance_report) - interval '1 day'))ads;
                                """),

        migrations.RunSQL("""
          insert into ui_usual_advertisers_graph as ut (
            advertiser_id,
            type,
            day_chart)
          select
          ads.advertiser_id,
          'last_3_days',
          array_to_json(array(
            select json_build_object(
              'day', "day",
              'imp', sum(imps),
              'spend', sum(media_cost),
              'clicks', sum(clicks),
              'conversions', sum(post_click_convs) + sum(post_view_convs),
              'cvr', case sum(imps) when 0 then 0 else (sum(post_click_convs) + sum(post_view_convs)) / sum(imps)::float end,
              'cpc', case sum(clicks) when 0 then 0 else sum(media_cost) / sum(clicks) end,
              'ctr', case sum(imps) when 0 then 0 else sum(clicks)::float / sum(imps) end
            )
            from site_domain_performance_report tt
            where
              ads.advertiser_id=tt.advertiser_id
            and
              "hour" >= date_trunc('day',(select max(hour) from site_domain_performance_report) - interval '3 day')
            group by "day"
            order by "day"
          ))
        from (
               select distinct advertiser_id from site_domain_performance_report
                where
                "hour" >= date_trunc('day',(select max(hour) from site_domain_performance_report) - interval '3 day'))ads;
                                """),

        migrations.RunSQL("""
              insert into ui_usual_advertisers_graph as ut (
                advertiser_id,
                type,
                day_chart)
              select
              ads.advertiser_id,
              'last_7_days',
              array_to_json(array(
                select json_build_object(
                  'day', "day",
                  'imp', sum(imps),
                  'spend', sum(media_cost),
                  'clicks', sum(clicks),
                  'conversions', sum(post_click_convs) + sum(post_view_convs),
                  'cvr', case sum(imps) when 0 then 0 else (sum(post_click_convs) + sum(post_view_convs)) / sum(imps)::float end,
                  'cpc', case sum(clicks) when 0 then 0 else sum(media_cost) / sum(clicks) end,
                  'ctr', case sum(imps) when 0 then 0 else sum(clicks)::float / sum(imps) end
                )
                from site_domain_performance_report tt
                where
                  ads.advertiser_id=tt.advertiser_id
                and
                  "hour" >= date_trunc('day',(select max(hour) from site_domain_performance_report) - interval '7 day')
                group by "day"
                order by "day"
              ))
            from (
                   select distinct advertiser_id from site_domain_performance_report
                    where
                    "hour" >= date_trunc('day',(select max(hour) from site_domain_performance_report) - interval '7 day'))ads;
                                    """),

        migrations.RunSQL("""
              insert into ui_usual_advertisers_graph as ut (
                advertiser_id,
                type,
                day_chart)
              select
              ads.advertiser_id,
              'last_14_days',
              array_to_json(array(
                select json_build_object(
                  'day', "day",
                  'imp', sum(imps),
                  'spend', sum(media_cost),
                  'clicks', sum(clicks),
                  'conversions', sum(post_click_convs) + sum(post_view_convs),
                  'cvr', case sum(imps) when 0 then 0 else (sum(post_click_convs) + sum(post_view_convs)) / sum(imps)::float end,
                  'cpc', case sum(clicks) when 0 then 0 else sum(media_cost) / sum(clicks) end,
                  'ctr', case sum(imps) when 0 then 0 else sum(clicks)::float / sum(imps) end
                )
                from site_domain_performance_report tt
                where
                  ads.advertiser_id=tt.advertiser_id
                and
                  "hour" >= date_trunc('day',(select max(hour) from site_domain_performance_report) - interval '14 day')
                group by "day"
                order by "day"
              ))
            from (
                   select distinct advertiser_id from site_domain_performance_report
                    where
                    "hour" >= date_trunc('day',(select max(hour) from site_domain_performance_report) - interval '14 day'))ads;
                                    """),

        migrations.RunSQL("""
              insert into ui_usual_advertisers_graph as ut (
                advertiser_id,
                type,
                day_chart)
              select
              ads.advertiser_id,
              'last_21_days',
              array_to_json(array(
                select json_build_object(
                  'day', "day",
                  'imp', sum(imps),
                  'spend', sum(media_cost),
                  'clicks', sum(clicks),
                  'conversions', sum(post_click_convs) + sum(post_view_convs),
                  'cvr', case sum(imps) when 0 then 0 else (sum(post_click_convs) + sum(post_view_convs)) / sum(imps)::float end,
                  'cpc', case sum(clicks) when 0 then 0 else sum(media_cost) / sum(clicks) end,
                  'ctr', case sum(imps) when 0 then 0 else sum(clicks)::float / sum(imps) end
                )
                from site_domain_performance_report tt
                where
                  ads.advertiser_id=tt.advertiser_id
                and
                  "hour" >= date_trunc('day',(select max(hour) from site_domain_performance_report) - interval '21 day')
                group by "day"
                order by "day"
              ))
            from (
                   select distinct advertiser_id from site_domain_performance_report
                    where
                    "hour" >= date_trunc('day',(select max(hour) from site_domain_performance_report) - interval '21 day'))ads;
                                    """),

        migrations.RunSQL("""
              insert into ui_usual_advertisers_graph as ut (
        advertiser_id,
        type,
        day_chart)
      select
      ads.advertiser_id,
      'last_90_days',
      array_to_json(array(
        select json_build_object(
          'day', "day",
          'imp', sum(imps),
          'spend', sum(media_cost),
          'clicks', sum(clicks),
          'conversions', sum(post_click_convs) + sum(post_view_convs),
          'cvr', case sum(imps) when 0 then 0 else (sum(post_click_convs) + sum(post_view_convs)) / sum(imps)::float end,
          'cpc', case sum(clicks) when 0 then 0 else sum(media_cost) / sum(clicks) end,
          'ctr', case sum(imps) when 0 then 0 else sum(clicks)::float / sum(imps) end
        )
        from site_domain_performance_report tt
        where
          ads.advertiser_id=tt.advertiser_id
        and
          ("day" >= (select max(hour) from site_domain_performance_report) - interval '90 day'
          or
           "hour" >= (select max(hour) from site_domain_performance_report) - interval '90 day')
        group by "day"
        order by "day"
      ))
    from (
           select distinct advertiser_id from site_domain_performance_report
            where
            ("day" >= (select max(hour) from site_domain_performance_report) - interval '90 day'
                  or
                   "hour" >= (select max(hour) from site_domain_performance_report) - interval '90 day'))ads;
                                    """),

        migrations.RunSQL("""
                  insert into ui_usual_advertisers_graph as ut (
                    advertiser_id,
                    type,
                    day_chart)
                  select
                  ads.advertiser_id,
                  'last_month',
                  array_to_json(array(
                    select json_build_object(
                      'day', "day",
                      'imp', sum(imps),
                      'spend', sum(media_cost),
                      'clicks', sum(clicks),
                      'conversions', sum(post_click_convs) + sum(post_view_convs),
                      'cvr', case sum(imps) when 0 then 0 else (sum(post_click_convs) + sum(post_view_convs)) / sum(imps)::float end,
                      'cpc', case sum(clicks) when 0 then 0 else sum(media_cost) / sum(clicks) end,
                      'ctr', case sum(imps) when 0 then 0 else sum(clicks)::float / sum(imps) end
                    )
                    from site_domain_performance_report tt
                    where
                      ads.advertiser_id=tt.advertiser_id
                    and
                    "hour" >= date_trunc('month',(select max(hour) from site_domain_performance_report) - interval '1 month')
                    and
                    "hour" < date_trunc('month',(select max(hour) from site_domain_performance_report))
                    group by "day"
                    order by "day"
                  ))
                from (
                       select distinct advertiser_id from site_domain_performance_report
                        where
                        "hour" >= date_trunc('month',(select max(hour) from site_domain_performance_report) - interval '1 month')
                        and
                        "hour" < date_trunc('month',(select max(hour) from site_domain_performance_report)))ads;
                                        """),

        migrations.RunSQL("""
                  insert into ui_usual_advertisers_graph as ut (
                    advertiser_id,
                    type,
                    day_chart)
                  select
                  ads.advertiser_id,
                  'cur_month',
                  array_to_json(array(
                    select json_build_object(
                      'day', "day",
                      'imp', sum(imps),
                      'spend', sum(media_cost),
                      'clicks', sum(clicks),
                      'conversions', sum(post_click_convs) + sum(post_view_convs),
                      'cvr', case sum(imps) when 0 then 0 else (sum(post_click_convs) + sum(post_view_convs)) / sum(imps)::float end,
                      'cpc', case sum(clicks) when 0 then 0 else sum(media_cost) / sum(clicks) end,
                      'ctr', case sum(imps) when 0 then 0 else sum(clicks)::float / sum(imps) end
                    )
                    from site_domain_performance_report tt
                    where
                      ads.advertiser_id=tt.advertiser_id
                    and
                      "hour" >= date_trunc('month',(select max(hour) from site_domain_performance_report))
                    group by "day"
                    order by "day"
                  ))
                from (
                       select distinct advertiser_id from site_domain_performance_report
                        where
                        "hour" >= date_trunc('month',(select max(hour) from site_domain_performance_report)))ads;
                                        """),

        ##
        #CAMPAIGNS GRAPH
        ##

        migrations.RunSQL("delete from ui_usual_placements_graph"),

        migrations.RunSQL("""
    insert into ui_usual_placements_graph as ut (
        campaign_id,
        type,
        day_chart)
      select
      camps.campaign_id,
      'all',
      array_to_json(array(
        select json_build_object(
          'day', "hour"::timestamp::date,
          'impression', sum(imps),
          'mediaspent', sum("cost"),
          'clicks', sum(clicks),
          'conversions', sum(total_convs),
          'cpa', case sum(total_convs) when 0 then 0 else sum("cost") / sum(total_convs) end,
          'cpc', case sum(clicks) when 0 then 0 else sum("cost") / sum(clicks) end,
          'ctr', case sum(imps) when 0 then 0 else sum(clicks)::float / sum(imps) end
        )
        from network_analytics_report_by_placement tt
        where
        camps.campaign_id=tt.campaign_id
        group by "hour"::timestamp::date
        order by "hour"::timestamp::date
      ))
    from (select distinct campaign_id from network_analytics_report_by_placement) camps;
                        """),

        migrations.RunSQL("""
        insert into ui_usual_placements_graph as ut (
            campaign_id,
            type,
            day_chart)
          select
          camps.campaign_id,
          'yesterday',
          array_to_json(array(
            select json_build_object(
              'day', "hour"::timestamp::date,
              'impression', sum(imps),
              'mediaspent', sum("cost"),
              'clicks', sum(clicks),
              'conversions', sum(total_convs),
              'cpa', case sum(total_convs) when 0 then 0 else sum("cost") / sum(total_convs) end,
              'cpc', case sum(clicks) when 0 then 0 else sum("cost") / sum(clicks) end,
              'ctr', case sum(imps) when 0 then 0 else sum(clicks)::float / sum(imps) end
            )
            from network_analytics_report_by_placement tt
            where
            camps.campaign_id=tt.campaign_id and
              "hour" >= date_trunc('day',(select max(hour) from network_analytics_report_by_placement) - interval '1 day')
            group by "hour"::timestamp::date
            order by "hour"::timestamp::date
          ))
        from (
               select distinct campaign_id from network_analytics_report_by_placement
               where
               "hour" >= date_trunc('day',(select max(hour) from network_analytics_report_by_placement) - interval '1 day')) camps;
                            """),

        migrations.RunSQL("""
            insert into ui_usual_placements_graph as ut (
                campaign_id,
                type,
                day_chart)
              select
              camps.campaign_id,
              'last_3_days',
              array_to_json(array(
                select json_build_object(
                  'day', "hour"::timestamp::date,
                  'impression', sum(imps),
                  'mediaspent', sum("cost"),
                  'clicks', sum(clicks),
                  'conversions', sum(total_convs),
                  'cpa', case sum(total_convs) when 0 then 0 else sum("cost") / sum(total_convs) end,
                  'cpc', case sum(clicks) when 0 then 0 else sum("cost") / sum(clicks) end,
                  'ctr', case sum(imps) when 0 then 0 else sum(clicks)::float / sum(imps) end
                )
                from network_analytics_report_by_placement tt
                where
                camps.campaign_id=tt.campaign_id and
                  "hour" >= date_trunc('day',(select max(hour) from network_analytics_report_by_placement) - interval '3 day')
                group by "hour"::timestamp::date
                order by "hour"::timestamp::date
              ))
            from (
                   select distinct campaign_id from network_analytics_report_by_placement
                   where
                   "hour" >= date_trunc('day',(select max(hour) from network_analytics_report_by_placement) - interval '3 day')) camps;
                                """),

        migrations.RunSQL("""
            insert into ui_usual_placements_graph as ut (
                campaign_id,
                type,
                day_chart)
              select
              camps.campaign_id,
              'last_7_days',
              array_to_json(array(
                select json_build_object(
                  'day', "hour"::timestamp::date,
                  'impression', sum(imps),
                  'mediaspent', sum("cost"),
                  'clicks', sum(clicks),
                  'conversions', sum(total_convs),
                  'cpa', case sum(total_convs) when 0 then 0 else sum("cost") / sum(total_convs) end,
                  'cpc', case sum(clicks) when 0 then 0 else sum("cost") / sum(clicks) end,
                  'ctr', case sum(imps) when 0 then 0 else sum(clicks)::float / sum(imps) end
                )
                from network_analytics_report_by_placement tt
                where
                camps.campaign_id=tt.campaign_id and
                  "hour" >= date_trunc('day',(select max(hour) from network_analytics_report_by_placement) - interval '7 day')
                group by "hour"::timestamp::date
                order by "hour"::timestamp::date
              ))
            from (
                   select distinct campaign_id from network_analytics_report_by_placement
                   where
                   "hour" >= date_trunc('day',(select max(hour) from network_analytics_report_by_placement) - interval '7 day')) camps;
                                """),

        migrations.RunSQL("""
            insert into ui_usual_placements_graph as ut (
                campaign_id,
                type,
                day_chart)
              select
              camps.campaign_id,
              'last_14_days',
              array_to_json(array(
                select json_build_object(
                  'day', "hour"::timestamp::date,
                  'impression', sum(imps),
                  'mediaspent', sum("cost"),
                  'clicks', sum(clicks),
                  'conversions', sum(total_convs),
                  'cpa', case sum(total_convs) when 0 then 0 else sum("cost") / sum(total_convs) end,
                  'cpc', case sum(clicks) when 0 then 0 else sum("cost") / sum(clicks) end,
                  'ctr', case sum(imps) when 0 then 0 else sum(clicks)::float / sum(imps) end
                )
                from network_analytics_report_by_placement tt
                where
                camps.campaign_id=tt.campaign_id and
                  "hour" >= date_trunc('day',(select max(hour) from network_analytics_report_by_placement) - interval '14 day')
                group by "hour"::timestamp::date
                order by "hour"::timestamp::date
              ))
            from (
                   select distinct campaign_id from network_analytics_report_by_placement
                   where
                   "hour" >= date_trunc('day',(select max(hour) from network_analytics_report_by_placement) - interval '14 day')) camps;
                                """),

        migrations.RunSQL("""
            insert into ui_usual_placements_graph as ut (
                campaign_id,
                type,
                day_chart)
              select
              camps.campaign_id,
              'last_21_days',
              array_to_json(array(
                select json_build_object(
                  'day', "hour"::timestamp::date,
                  'impression', sum(imps),
                  'mediaspent', sum("cost"),
                  'clicks', sum(clicks),
                  'conversions', sum(total_convs),
                  'cpa', case sum(total_convs) when 0 then 0 else sum("cost") / sum(total_convs) end,
                  'cpc', case sum(clicks) when 0 then 0 else sum("cost") / sum(clicks) end,
                  'ctr', case sum(imps) when 0 then 0 else sum(clicks)::float / sum(imps) end
                )
                from network_analytics_report_by_placement tt
                where
                camps.campaign_id=tt.campaign_id and
                  "hour" >= date_trunc('day',(select max(hour) from network_analytics_report_by_placement) - interval '21 day')
                group by "hour"::timestamp::date
                order by "hour"::timestamp::date
              ))
            from (
                   select distinct campaign_id from network_analytics_report_by_placement
                   where
                   "hour" >= date_trunc('day',(select max(hour) from network_analytics_report_by_placement) - interval '21 day')) camps;
                                """),

        migrations.RunSQL("""
                insert into ui_usual_placements_graph as ut (
                    campaign_id,
                    type,
                    day_chart)
                  select
                  camps.campaign_id,
                  'last_90_days',
                  array_to_json(array(
                    select json_build_object(
                      'day', "hour"::timestamp::date,
                      'impression', sum(imps),
                      'mediaspent', sum("cost"),
                      'clicks', sum(clicks),
                      'conversions', sum(total_convs),
                      'cpa', case sum(total_convs) when 0 then 0 else sum("cost") / sum(total_convs) end,
                      'cpc', case sum(clicks) when 0 then 0 else sum("cost") / sum(clicks) end,
                      'ctr', case sum(imps) when 0 then 0 else sum(clicks)::float / sum(imps) end
                    )
                    from network_analytics_report_by_placement tt
                    where
                    camps.campaign_id=tt.campaign_id and
                      "hour" >= date_trunc('day',(select max(hour) from network_analytics_report_by_placement) - interval '90 day')
                    group by "hour"::timestamp::date
                    order by "hour"::timestamp::date
                  ))
                from (
                       select distinct campaign_id from network_analytics_report_by_placement
                       where
                       "hour" >= date_trunc('day',(select max(hour) from network_analytics_report_by_placement) - interval '90 day')) camps;
                                    """),

        migrations.RunSQL("""
                    insert into ui_usual_placements_graph as ut (
                        campaign_id,
                        type,
                        day_chart)
                      select
                      camps.campaign_id,
                      'last_month',
                      array_to_json(array(
                        select json_build_object(
                          'day', "hour"::timestamp::date,
                          'impression', sum(imps),
                          'mediaspent', sum("cost"),
                          'clicks', sum(clicks),
                          'conversions', sum(total_convs),
                          'cpa', case sum(total_convs) when 0 then 0 else sum("cost") / sum(total_convs) end,
                          'cpc', case sum(clicks) when 0 then 0 else sum("cost") / sum(clicks) end,
                          'ctr', case sum(imps) when 0 then 0 else sum(clicks)::float / sum(imps) end
                        )
                        from network_analytics_report_by_placement tt
                        where
                        camps.campaign_id=tt.campaign_id and
                          "hour" >= date_trunc('month',(select max(hour) from network_analytics_report_by_placement) - interval '1 month')
                        and
                          "hour" < date_trunc('month',(select max(hour) from network_analytics_report_by_placement))
                        group by "hour"::timestamp::date
                        order by "hour"::timestamp::date
                      ))
                    from (
                           select distinct campaign_id from network_analytics_report_by_placement
                           where
                           "hour" >= date_trunc('month',(select max(hour) from network_analytics_report_by_placement) - interval '1 month')
                           and
                           "hour" < date_trunc('month',(select max(hour) from network_analytics_report_by_placement))) camps;
                                        """),

        migrations.RunSQL("""
                    insert into ui_usual_placements_graph as ut (
                        campaign_id,
                        type,
                        day_chart)
                      select
                      camps.campaign_id,
                      'cur_month',
                      array_to_json(array(
                        select json_build_object(
                          'day', "hour"::timestamp::date,
                          'impression', sum(imps),
                          'mediaspent', sum("cost"),
                          'clicks', sum(clicks),
                          'conversions', sum(total_convs),
                          'cpa', case sum(total_convs) when 0 then 0 else sum("cost") / sum(total_convs) end,
                          'cpc', case sum(clicks) when 0 then 0 else sum("cost") / sum(clicks) end,
                          'ctr', case sum(imps) when 0 then 0 else sum(clicks)::float / sum(imps) end
                        )
                        from network_analytics_report_by_placement tt
                        where
                        camps.campaign_id=tt.campaign_id and
                          "hour" >= date_trunc('month',(select max(hour) from network_analytics_report_by_placement))
                        group by "hour"::timestamp::date
                        order by "hour"::timestamp::date
                      ))
                    from (
                           select distinct campaign_id from network_analytics_report_by_placement
                           where
                           "hour" >= date_trunc('month',(select max(hour) from network_analytics_report_by_placement))) camps;
                                        """),
    ]