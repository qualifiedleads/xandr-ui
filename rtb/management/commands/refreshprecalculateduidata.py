from django.core.management import BaseCommand
from django.db import connection

class Command(BaseCommand):
    help = """
        Call for truncate and refresh tables with UI table data
        """

    def handle(self, *args, **options):
        print "refreshPrecalculatedUIData started"
        with connection.cursor() as cursor:
            ###
            #REFRESH PLACEMENTS GRID DATA
            ###
            cursor.execute("delete from ui_usual_placements_grid_data_all")
            print "Placements grid data refreshing started"
            cursor.execute("""
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
  where
    t."hour" >= '1970-01-01 00:00:00' and t."hour" <= current_timestamp::timestamp without time zone
  group by
    t.campaign_id, t.placement_id;
                        """)

            cursor.execute("delete from ui_usual_placements_grid_data_yesterday;")

            cursor.execute("""
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
        t."hour" >= date_trunc('day',current_timestamp::timestamp without time zone - interval '1 day')
        and t."hour" <= current_timestamp::timestamp without time zone
      group by
        t.campaign_id, t.placement_id;
                                    """)

            cursor.execute("delete from ui_usual_placements_grid_data_last_3_days;")

            cursor.execute("""
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
            t."hour" >= date_trunc('day',current_timestamp::timestamp without time zone - interval '3 day')
            and t."hour" <= current_timestamp::timestamp without time zone
          group by
            t.campaign_id, t.placement_id;
                                    """)

            cursor.execute("delete from ui_usual_placements_grid_data_last_7_days;")

            cursor.execute("""
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
            t."hour" >= date_trunc('day',current_timestamp::timestamp without time zone - interval '7 day')
            and t."hour" <= current_timestamp::timestamp without time zone
          group by
            t.campaign_id, t.placement_id;
                                    """)

            cursor.execute("delete from ui_usual_placements_grid_data_last_14_days;")

            cursor.execute("""
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
            t."hour" >= date_trunc('day',current_timestamp::timestamp without time zone - interval '14 day')
            and t."hour" <= current_timestamp::timestamp without time zone
          group by
            t.campaign_id, t.placement_id;
                                    """)

            cursor.execute("delete from ui_usual_placements_grid_data_last_21_days;")

            cursor.execute("""
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
            t."hour" >= date_trunc('day',current_timestamp::timestamp without time zone - interval '21 day')
            and t."hour" <= current_timestamp::timestamp without time zone
          group by
            t.campaign_id, t.placement_id;
                                    """)

            cursor.execute("delete from ui_usual_placements_grid_data_last_90_days;")

            cursor.execute("""
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
            t."hour" >= date_trunc('day',current_timestamp::timestamp without time zone - interval '90 day')
            and t."hour" <= current_timestamp::timestamp without time zone
          group by
            t.campaign_id, t.placement_id;
                                    """)

            cursor.execute("delete from ui_usual_placements_grid_data_last_month;")

            cursor.execute("""
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
            t."hour" >= date_trunc('month',current_timestamp::timestamp without time zone - interval '1 month')
            and t."hour" < date_trunc('month',current_timestamp::timestamp without time zone)
          group by
            t.campaign_id, t.placement_id;
                                    """)

            cursor.execute("delete from ui_usual_placements_grid_data_cur_month;")

            cursor.execute("""
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
            t."hour" >= date_trunc('month',current_timestamp::timestamp without time zone)
            and t."hour" <= current_timestamp::timestamp without time zone
          group by
            t.campaign_id, t.placement_id;
                                    """)

            print "Placements grid data refreshing finished"

            ###
            #CAMPAIGNS GRID
            ###
            cursor.execute("delete from ui_usual_campaigns_grid_data_all;")
            print "Campaigns grid data refreshing started"
            cursor.execute("""
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
           and ((site_r.hour >= '1970-01-01 00:00:00' and site_r.hour < current_timestamp::timestamp without time zone)
           or (site_r.day >= '1970-01-01 00:00:00' and site_r.day < current_timestamp::timestamp without time zone))
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
        (site_r1.hour >= '1970-01-01 00:00:00'
        and site_r1.hour < current_timestamp::timestamp without time zone)
        or
        (site_r1.day >= '1970-01-01 00:00:00'
        and site_r1.day < current_timestamp::timestamp without time zone)
      WINDOW w as (partition by site_r1.campaign_id order by site_r1.day desc)
     ) page;
                                    """)

            cursor.execute("delete from ui_usual_campaigns_grid_data_yesterday;")

            cursor.execute("""
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
               and (
               (site_r.hour >= date_trunc('day',current_timestamp::timestamp without time zone - interval '1 day')
               and site_r.hour <= current_timestamp::timestamp without time zone)
               or (
               site_r.day >= date_trunc('day',current_timestamp::timestamp without time zone - interval '1 day')
               and site_r.day <= current_timestamp::timestamp without time zone))
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
            (site_r1.hour >= date_trunc('day',current_timestamp::timestamp without time zone - interval '1 day')
            and site_r1.hour <= current_timestamp::timestamp without time zone)
            or
            (site_r1.day >= date_trunc('day',current_timestamp::timestamp without time zone - interval '1 day')
            and site_r1.day <= current_timestamp::timestamp without time zone)
          WINDOW w as (partition by site_r1.campaign_id order by site_r1.day desc)
         ) page;
                                                """)

            cursor.execute("delete from ui_usual_campaigns_grid_data_last_3_days;")

            cursor.execute("""
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
               and (
               (site_r.hour >= date_trunc('day',current_timestamp::timestamp without time zone - interval '3 day')
               and site_r.hour <= current_timestamp::timestamp without time zone)
               or (
               site_r.day >= date_trunc('day',current_timestamp::timestamp without time zone - interval '3 day')
               and site_r.day <= current_timestamp::timestamp without time zone))
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
            (site_r1.hour >= date_trunc('day',current_timestamp::timestamp without time zone - interval '3 day')
            and site_r1.hour <= current_timestamp::timestamp without time zone)
            or
            (site_r1.day >= date_trunc('day',current_timestamp::timestamp without time zone - interval '3 day')
            and site_r1.day <= current_timestamp::timestamp without time zone)
          WINDOW w as (partition by site_r1.campaign_id order by site_r1.day desc)
         ) page;
                                                """)

            cursor.execute("delete from ui_usual_campaigns_grid_data_last_7_days;")

            cursor.execute("""
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
               and (
               (site_r.hour >= date_trunc('day',current_timestamp::timestamp without time zone - interval '7 day')
               and site_r.hour <= current_timestamp::timestamp without time zone)
               or (
               site_r.day >= date_trunc('day',current_timestamp::timestamp without time zone - interval '7 day')
               and site_r.day <= current_timestamp::timestamp without time zone))
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
            (site_r1.hour >= date_trunc('day',current_timestamp::timestamp without time zone - interval '7 day')
            and site_r1.hour <= current_timestamp::timestamp without time zone)
            or
            (site_r1.day >= date_trunc('day',current_timestamp::timestamp without time zone - interval '7 day')
            and site_r1.day <= current_timestamp::timestamp without time zone)
          WINDOW w as (partition by site_r1.campaign_id order by site_r1.day desc)
         ) page;
                                                """)

            cursor.execute("delete from ui_usual_campaigns_grid_data_last_14_days;")

            cursor.execute("""
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
               and (
               (site_r.hour >= date_trunc('day',current_timestamp::timestamp without time zone - interval '14 day')
               and site_r.hour <= current_timestamp::timestamp without time zone)
               or (
               site_r.day >= date_trunc('day',current_timestamp::timestamp without time zone - interval '14 day')
               and site_r.day <= current_timestamp::timestamp without time zone))
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
            (site_r1.hour >= date_trunc('day',current_timestamp::timestamp without time zone - interval '14 day')
            and site_r1.hour <= current_timestamp::timestamp without time zone)
            or
            (site_r1.day >= date_trunc('day',current_timestamp::timestamp without time zone - interval '14 day')
            and site_r1.day <= current_timestamp::timestamp without time zone)
          WINDOW w as (partition by site_r1.campaign_id order by site_r1.day desc)
         ) page;
                                                """)

            cursor.execute("delete from ui_usual_campaigns_grid_data_last_21_days;")

            cursor.execute("""
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
               and (
               (site_r.hour >= date_trunc('day',current_timestamp::timestamp without time zone - interval '21 day')
               and site_r.hour <= current_timestamp::timestamp without time zone)
               or (
               site_r.day >= date_trunc('day',current_timestamp::timestamp without time zone - interval '21 day')
               and site_r.day <= current_timestamp::timestamp without time zone))
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
            (site_r1.hour >= date_trunc('day',current_timestamp::timestamp without time zone - interval '21 day')
            and site_r1.hour <= current_timestamp::timestamp without time zone)
            or
            (site_r1.day >= date_trunc('day',current_timestamp::timestamp without time zone - interval '21 day')
            and site_r1.day <= current_timestamp::timestamp without time zone)
          WINDOW w as (partition by site_r1.campaign_id order by site_r1.day desc)
         ) page;
                                                """)

            cursor.execute("delete from ui_usual_campaigns_grid_data_last_90_days;")

            cursor.execute("""
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
               (site_r.hour >= date_trunc('day',current_timestamp::timestamp without time zone - interval '90 day')
               and site_r.hour <= current_timestamp::timestamp without time zone)
               or (
               site_r.day >= date_trunc('day',current_timestamp::timestamp without time zone - interval '90 day')
               and site_r.day <= current_timestamp::timestamp without time zone))
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
            (site_r1.hour >= date_trunc('day',current_timestamp::timestamp without time zone - interval '90 day')
            and site_r1.hour <= current_timestamp::timestamp without time zone)
            or
            (site_r1.day >= date_trunc('day',current_timestamp::timestamp without time zone - interval '90 day')
            and site_r1.day <= current_timestamp::timestamp without time zone)
          WINDOW w as (partition by site_r1.campaign_id order by site_r1.day desc)
         ) page;
                                                """)

            cursor.execute("delete from ui_usual_campaigns_grid_data_last_month;")

            cursor.execute("""
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
                   and (
                   (site_r.hour >= date_trunc('month',current_timestamp::timestamp without time zone - interval '1 month')
                   and site_r.hour < date_trunc('month',current_timestamp::timestamp without time zone))
                   or (
                   site_r.day >= date_trunc('month',current_timestamp::timestamp without time zone - interval '1 month')
                   and site_r.day < date_trunc('month',current_timestamp::timestamp without time zone)))
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
                (site_r1.hour >= date_trunc('month',current_timestamp::timestamp without time zone - interval '1 month')
                and site_r1.hour < date_trunc('month',current_timestamp::timestamp without time zone))
                or
                (site_r1.day >= date_trunc('month',current_timestamp::timestamp without time zone - interval '1 month')
                and site_r1.day < date_trunc('month',current_timestamp::timestamp without time zone))
              WINDOW w as (partition by site_r1.campaign_id order by site_r1.day desc)
             ) page;
                                                """)

            cursor.execute("delete from ui_usual_campaigns_grid_data_cur_month;")

            cursor.execute("""
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
                   and (
                   (site_r.hour >= date_trunc('month',current_timestamp::timestamp without time zone)
                   and site_r.hour <= current_timestamp::timestamp without time zone)
                   or (
                   site_r.day >= date_trunc('month',current_timestamp::timestamp without time zone)
                   and site_r.day <= current_timestamp::timestamp without time zone))
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
                (site_r1.hour >= date_trunc('month',current_timestamp::timestamp without time zone)
                and site_r1.hour <= current_timestamp::timestamp without time zone)
                or
                (site_r1.day >= date_trunc('month',current_timestamp::timestamp without time zone)
                and site_r1.day <= current_timestamp::timestamp without time zone)
              WINDOW w as (partition by site_r1.campaign_id order by site_r1.day desc)
             ) page;
                                                """)

            print "Campaigns grid data refreshing finished"

            ###
            # REFRESH ADVERTISERS GRAPH DATA
            ###

            cursor.execute("delete from ui_usual_advertisers_graph;")

            print "Advertisers graph data refreshing started"

            cursor.execute("""
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
    and
      (("day" >= '1970-01-01 00:00:00'
        and
        "day" <= current_timestamp::timestamp without time zone)
      or
       ("hour" >= '1970-01-01 00:00:00'
        and
        "hour" <= current_timestamp::timestamp without time zone))
    group by "day"
    order by "day"
  ))
from (
       select distinct advertiser_id from site_domain_performance_report
        where
        (("day" >= '1970-01-01 00:00:00'
                and
                "day" <= current_timestamp::timestamp without time zone)
              or
               ("hour" >= '1970-01-01 00:00:00'
                and
                "hour" <= current_timestamp::timestamp without time zone)))ads;
                                                """)

            cursor.execute("""
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
          (("day" >= date_trunc('day',current_timestamp::timestamp without time zone - interval '1 day')
            and
            "day" <= current_timestamp::timestamp without time zone)
          or
           ("hour" >= date_trunc('day',current_timestamp::timestamp without time zone - interval '1 day')
            and
            "hour" <= current_timestamp::timestamp without time zone))
        group by "day"
        order by "day"
      ))
    from (
           select distinct advertiser_id from site_domain_performance_report
            where
            (("day" >= date_trunc('day',current_timestamp::timestamp without time zone - interval '1 day')
                    and
                    "day" <= current_timestamp::timestamp without time zone)
                  or
                   ("hour" >= date_trunc('day',current_timestamp::timestamp without time zone - interval '1 day')
                    and
                    "hour" <= current_timestamp::timestamp without time zone)))ads;
                                                            """)

            cursor.execute("""
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
          (("day" >= date_trunc('day',current_timestamp::timestamp without time zone - interval '3 day')
            and
            "day" <= current_timestamp::timestamp without time zone)
          or
           ("hour" >= date_trunc('day',current_timestamp::timestamp without time zone - interval '3 day')
            and
            "hour" <= current_timestamp::timestamp without time zone))
        group by "day"
        order by "day"
      ))
    from (
           select distinct advertiser_id from site_domain_performance_report
            where
            (("day" >= date_trunc('day',current_timestamp::timestamp without time zone - interval '3 day')
                    and
                    "day" <= current_timestamp::timestamp without time zone)
                  or
                   ("hour" >= date_trunc('day',current_timestamp::timestamp without time zone - interval '3 day')
                    and
                    "hour" <= current_timestamp::timestamp without time zone)))ads;
                                                            """)

            cursor.execute("""
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
              (("day" >= date_trunc('day',current_timestamp::timestamp without time zone - interval '7 day')
                and
                "day" <= current_timestamp::timestamp without time zone)
              or
               ("hour" >= date_trunc('day',current_timestamp::timestamp without time zone - interval '7 day')
                and
                "hour" <= current_timestamp::timestamp without time zone))
            group by "day"
            order by "day"
          ))
        from (
               select distinct advertiser_id from site_domain_performance_report
                where
                (("day" >= date_trunc('day',current_timestamp::timestamp without time zone - interval '7 day')
                        and
                        "day" <= current_timestamp::timestamp without time zone)
                      or
                       ("hour" >= date_trunc('day',current_timestamp::timestamp without time zone - interval '7 day')
                        and
                        "hour" <= current_timestamp::timestamp without time zone)))ads;
                                                            """)

            cursor.execute("""
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
              (("day" >= date_trunc('day',current_timestamp::timestamp without time zone - interval '14 day')
                and
                "day" <= current_timestamp::timestamp without time zone)
              or
               ("hour" >= date_trunc('day',current_timestamp::timestamp without time zone - interval '14 day')
                and
                "hour" <= current_timestamp::timestamp without time zone))
            group by "day"
            order by "day"
          ))
        from (
               select distinct advertiser_id from site_domain_performance_report
                where
                (("day" >= date_trunc('day',current_timestamp::timestamp without time zone - interval '14 day')
                        and
                        "day" <= current_timestamp::timestamp without time zone)
                      or
                       ("hour" >= date_trunc('day',current_timestamp::timestamp without time zone - interval '14 day')
                        and
                        "hour" <= current_timestamp::timestamp without time zone)))ads;
                                                            """)

            cursor.execute("""
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
              (("day" >= date_trunc('day',current_timestamp::timestamp without time zone - interval '21 day')
                and
                "day" <= current_timestamp::timestamp without time zone)
              or
               ("hour" >= date_trunc('day',current_timestamp::timestamp without time zone - interval '21 day')
                and
                "hour" <= current_timestamp::timestamp without time zone))
            group by "day"
            order by "day"
          ))
        from (
               select distinct advertiser_id from site_domain_performance_report
                where
                (("day" >= date_trunc('day',current_timestamp::timestamp without time zone - interval '21 day')
                        and
                        "day" <= current_timestamp::timestamp without time zone)
                      or
                       ("hour" >= date_trunc('day',current_timestamp::timestamp without time zone - interval '21 day')
                        and
                        "hour" <= current_timestamp::timestamp without time zone)))ads;
                                                            """)

            cursor.execute("""
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
              (("day" >= date_trunc('day',current_timestamp::timestamp without time zone - interval '90 day')
                and
                "day" <= current_timestamp::timestamp without time zone)
              or
               ("hour" >= date_trunc('day',current_timestamp::timestamp without time zone - interval '90 day')
                and
                "hour" <= current_timestamp::timestamp without time zone))
            group by "day"
            order by "day"
          ))
        from (
               select distinct advertiser_id from site_domain_performance_report
                where
                (("day" >= date_trunc('day',current_timestamp::timestamp without time zone - interval '90 day')
                        and
                        "day" <= current_timestamp::timestamp without time zone)
                      or
                       ("hour" >= date_trunc('day',current_timestamp::timestamp without time zone - interval '90 day')
                        and
                        "hour" <= current_timestamp::timestamp without time zone)))ads;
                                                            """)

            cursor.execute("""
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
                  (("day" >= date_trunc('month',current_timestamp::timestamp without time zone - interval '1 month')
                    and
                    "day" < date_trunc('month',current_timestamp::timestamp without time zone))
                  or
                   ("hour" >= date_trunc('month',current_timestamp::timestamp without time zone - interval '1 month')
                    and
                    "hour" < date_trunc('month',current_timestamp::timestamp without time zone)))
                group by "day"
                order by "day"
              ))
            from (
                   select distinct advertiser_id from site_domain_performance_report
                    where
                    (("day" >= date_trunc('month',current_timestamp::timestamp without time zone - interval '1 month')
                            and
                            "day" < date_trunc('month',current_timestamp::timestamp without time zone))
                          or
                           ("hour" >= date_trunc('month',current_timestamp::timestamp without time zone - interval '1 month')
                            and
                            "hour" < date_trunc('month',current_timestamp::timestamp without time zone))))ads;
                                                            """)

            cursor.execute("""
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
                  (("day" >= date_trunc('month',current_timestamp::timestamp without time zone)
                    and
                    "day" <= current_timestamp::timestamp without time zone)
                  or
                   ("hour" >= date_trunc('month',current_timestamp::timestamp without time zone)
                    and
                    "hour" <= current_timestamp::timestamp without time zone))
                group by "day"
                order by "day"
              ))
            from (
                   select distinct advertiser_id from site_domain_performance_report
                    where
                    (("day" >= date_trunc('month',current_timestamp::timestamp without time zone)
                            and
                            "day" <= current_timestamp::timestamp without time zone)
                          or
                           ("hour" >= date_trunc('month',current_timestamp::timestamp without time zone)
                            and
                            "hour" <= current_timestamp::timestamp without time zone)))ads;
                                                            """)

            print "Advertisers graph data refreshing finished"
            ###
            # REFRESH CAMPAIGNS GRAPH DATA
            ###

            cursor.execute("delete from ui_usual_placements_graph;")

            print "Campaigns graph data refreshing started"

            cursor.execute("""
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
    camps.campaign_id=tt.campaign_id and
      "hour" >= '1970-01-01 00:00:00'
    and
      "hour" <= current_timestamp::timestamp without time zone
    group by "hour"::timestamp::date
    order by "hour"::timestamp::date
  ))
from (
       select distinct campaign_id from network_analytics_report_by_placement
       where
       "hour" >= '1970-01-01 00:00:00'
       and
       "hour" <= current_timestamp::timestamp without time zone) camps;
            """)

            cursor.execute("""
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
          "hour" >= date_trunc('day',current_timestamp::timestamp without time zone - interval '1 day')
        and
          "hour" <= current_timestamp::timestamp without time zone
        group by "hour"::timestamp::date
        order by "hour"::timestamp::date
      ))
    from (
           select distinct campaign_id from network_analytics_report_by_placement
           where
           "hour" >= date_trunc('day',current_timestamp::timestamp without time zone - interval '1 day')
           and
           "hour" <= current_timestamp::timestamp without time zone) camps;
                        """)

            cursor.execute("""
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
              "hour" >= date_trunc('day',current_timestamp::timestamp without time zone - interval '3 day')
            and
              "hour" <= current_timestamp::timestamp without time zone
            group by "hour"::timestamp::date
            order by "hour"::timestamp::date
          ))
        from (
               select distinct campaign_id from network_analytics_report_by_placement
               where
               "hour" >= date_trunc('day',current_timestamp::timestamp without time zone - interval '3 day')
               and
               "hour" <= current_timestamp::timestamp without time zone) camps;
                        """)

            cursor.execute("""
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
              "hour" >= date_trunc('day',current_timestamp::timestamp without time zone - interval '7 day')
            and
              "hour" <= current_timestamp::timestamp without time zone
            group by "hour"::timestamp::date
            order by "hour"::timestamp::date
          ))
        from (
               select distinct campaign_id from network_analytics_report_by_placement
               where
               "hour" >= date_trunc('day',current_timestamp::timestamp without time zone - interval '7 day')
               and
               "hour" <= current_timestamp::timestamp without time zone) camps;
                        """)

            cursor.execute("""
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
              "hour" >= date_trunc('day',current_timestamp::timestamp without time zone - interval '14 day')
            and
              "hour" <= current_timestamp::timestamp without time zone
            group by "hour"::timestamp::date
            order by "hour"::timestamp::date
          ))
        from (
               select distinct campaign_id from network_analytics_report_by_placement
               where
               "hour" >= date_trunc('day',current_timestamp::timestamp without time zone - interval '14 day')
               and
               "hour" <= current_timestamp::timestamp without time zone) camps;
                                    """)

            cursor.execute("""
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
              "hour" >= date_trunc('day',current_timestamp::timestamp without time zone - interval '21 day')
            and
              "hour" <= current_timestamp::timestamp without time zone
            group by "hour"::timestamp::date
            order by "hour"::timestamp::date
          ))
        from (
               select distinct campaign_id from network_analytics_report_by_placement
               where
               "hour" >= date_trunc('day',current_timestamp::timestamp without time zone - interval '21 day')
               and
               "hour" <= current_timestamp::timestamp without time zone) camps;
                                    """)

            cursor.execute("""
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
                  "hour" >= date_trunc('day',current_timestamp::timestamp without time zone - interval '90 day')
                and
                  "hour" <= current_timestamp::timestamp without time zone
                group by "hour"::timestamp::date
                order by "hour"::timestamp::date
              ))
            from (
                   select distinct campaign_id from network_analytics_report_by_placement
                   where
                   "hour" >= date_trunc('day',current_timestamp::timestamp without time zone - interval '90 day')
                   and
                   "hour" <= current_timestamp::timestamp without time zone) camps;
                        """)

            cursor.execute("""
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
                      "hour" >= date_trunc('month',current_timestamp::timestamp without time zone - interval '1 month')
                    and
                      "hour" < date_trunc('month',current_timestamp::timestamp without time zone)
                    group by "hour"::timestamp::date
                    order by "hour"::timestamp::date
                  ))
                from (
                       select distinct campaign_id from network_analytics_report_by_placement
                       where
                       "hour" >= date_trunc('month',current_timestamp::timestamp without time zone - interval '1 month')
                       and
                       "hour" < date_trunc('month',current_timestamp::timestamp without time zone)) camps;
                                    """)

            cursor.execute("""
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
                      "hour" >= date_trunc('month',current_timestamp::timestamp without time zone)
                    and
                      "hour" <= current_timestamp::timestamp without time zone
                    group by "hour"::timestamp::date
                    order by "hour"::timestamp::date
                  ))
                from (
                       select distinct campaign_id from network_analytics_report_by_placement
                       where
                       "hour" >= date_trunc('month',current_timestamp::timestamp without time zone)
                       and
                       "hour" <= current_timestamp::timestamp without time zone) camps;
                                    """)

            print "Campaigns graph data refreshing finished"

        print "refreshPrecalculatedUIData finished"