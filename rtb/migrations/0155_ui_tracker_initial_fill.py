from __future__ import unicode_literals

import django.contrib.postgres.fields.jsonb
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('rtb', '0154_ui_report_initial_fill'),
    ]

    operations = [

        migrations.RunSQL("""insert into last_modified (type, date)
    values ('lastPrecalculatedTrackerCron', (select date_trunc('hour', max("Date")) from rtb_impression_tracker));"""),

        migrations.RunSQL("delete from ui_usual_campaigns_graph_tracker"),

        migrations.RunSQL("""
insert into ui_usual_campaigns_graph_tracker(
  campaign_id,
  type,
  day_chart
)
select
  page."CpId",
  'all',
  array_to_json(array((select
         json_build_object(
         'day', site_r."Date"::timestamp::date,
         'impression', count(site_r."id"),
         'mediaspent', sum(site_r."PricePaid"),
         'clicks', count(clicktable.id),
         'conversions', count(conversiontable.id),
         'cpa', case count(conversiontable.id) when 0 then 0 else sum(site_r."PricePaid")/count(conversiontable.id) end,
         'cpc', case count(clicktable.id) when 0 then 0 else sum(site_r."PricePaid")::float/count(clicktable.id) end,
         'ctr', case count(site_r."id") when 0 then 0 else count(clicktable.id)::float/count(site_r."id") end)
       from
            rtb_impression_tracker site_r
            LEFT JOIN rtb_click_tracker clicktable ON clicktable."AuctionId" = site_r."AuctionId"
            LEFT JOIN rtb_conversion_tracker conversiontable ON conversiontable."AuctionId" = site_r."AuctionId"
       where site_r."CpId"= page."CpId" and site_r."Date" <= (select date from last_modified where type='lastPrecalculatedTrackerCron')
       group by site_r."Date"::timestamp::date
       order by site_r."Date"::timestamp::date))) id
from (
      select
        distinct "CpId"
      from
        rtb_impression_tracker
      where
      "Date" <= (select date from last_modified where type='lastPrecalculatedTrackerCron')
     ) page;
            """),

        migrations.RunSQL("""
    insert into ui_usual_campaigns_graph_tracker(
      campaign_id,
      type,
      day_chart
    )
    select
      page."CpId",
      'yesterday',
      array_to_json(array((select
             json_build_object(
             'day', site_r."Date"::timestamp::date,
             'impression', count(site_r."id"),
             'mediaspent', sum(site_r."PricePaid"),
             'clicks', count(clicktable.id),
             'conversions', count(conversiontable.id),
             'cpa', case count(conversiontable.id) when 0 then 0 else sum(site_r."PricePaid")/count(conversiontable.id) end,
             'cpc', case count(clicktable.id) when 0 then 0 else sum(site_r."PricePaid")::float/count(clicktable.id) end,
             'ctr', case count(site_r."id") when 0 then 0 else count(clicktable.id)::float/count(site_r."id") end)
           from
                rtb_impression_tracker site_r
                LEFT JOIN rtb_click_tracker clicktable ON clicktable."AuctionId" = site_r."AuctionId"
                LEFT JOIN rtb_conversion_tracker conversiontable ON conversiontable."AuctionId" = site_r."AuctionId"
           where site_r."CpId"= page."CpId"
             and (
             site_r."Date" >= date_trunc('day',(select date from last_modified where type='lastPrecalculatedTrackerCron') - interval '1 day')
             and site_r."Date" <= (select date from last_modified where type='lastPrecalculatedTrackerCron'))
           group by site_r."Date"::timestamp::date
           order by site_r."Date"::timestamp::date))) id
    from (
          select
            distinct "CpId"
          from
            rtb_impression_tracker
          where
            "Date" >= date_trunc('day',(select date from last_modified where type='lastPrecalculatedTrackerCron') - interval '1 day')
            and "Date" <= (select date from last_modified where type='lastPrecalculatedTrackerCron')
         ) page;
                """),

        migrations.RunSQL("""
        insert into ui_usual_campaigns_graph_tracker(
          campaign_id,
          type,
          day_chart
        )
        select
          page."CpId",
          'last_3_days',
          array_to_json(array((select
                 json_build_object(
                 'day', site_r."Date"::timestamp::date,
                 'impression', count(site_r."id"),
                 'mediaspent', sum(site_r."PricePaid"),
                 'clicks', count(clicktable.id),
                 'conversions', count(conversiontable.id),
                 'cpa', case count(conversiontable.id) when 0 then 0 else sum(site_r."PricePaid")/count(conversiontable.id) end,
                 'cpc', case count(clicktable.id) when 0 then 0 else sum(site_r."PricePaid")::float/count(clicktable.id) end,
                 'ctr', case count(site_r."id") when 0 then 0 else count(clicktable.id)::float/count(site_r."id") end)
               from
                    rtb_impression_tracker site_r
                    LEFT JOIN rtb_click_tracker clicktable ON clicktable."AuctionId" = site_r."AuctionId"
                    LEFT JOIN rtb_conversion_tracker conversiontable ON conversiontable."AuctionId" = site_r."AuctionId"
               where site_r."CpId"= page."CpId"
                 and (
                 site_r."Date" >= date_trunc('day',(select date from last_modified where type='lastPrecalculatedTrackerCron') - interval '3 day')
                 and site_r."Date" <= (select date from last_modified where type='lastPrecalculatedTrackerCron'))
               group by site_r."Date"::timestamp::date
               order by site_r."Date"::timestamp::date))) id
        from (
              select
                distinct "CpId"
              from
                rtb_impression_tracker
              where
                "Date" >= date_trunc('day',(select date from last_modified where type='lastPrecalculatedTrackerCron') - interval '3 day')
                and "Date" <= (select date from last_modified where type='lastPrecalculatedTrackerCron')
             ) page;
                    """),

        migrations.RunSQL("""
        insert into ui_usual_campaigns_graph_tracker(
          campaign_id,
          type,
          day_chart
        )
        select
          page."CpId",
          'last_7_days',
          array_to_json(array((select
                 json_build_object(
                 'day', site_r."Date"::timestamp::date,
                 'impression', count(site_r."id"),
                 'mediaspent', sum(site_r."PricePaid"),
                 'clicks', count(clicktable.id),
                 'conversions', count(conversiontable.id),
                 'cpa', case count(conversiontable.id) when 0 then 0 else sum(site_r."PricePaid")/count(conversiontable.id) end,
                 'cpc', case count(clicktable.id) when 0 then 0 else sum(site_r."PricePaid")::float/count(clicktable.id) end,
                 'ctr', case count(site_r."id") when 0 then 0 else count(clicktable.id)::float/count(site_r."id") end)
               from
                    rtb_impression_tracker site_r
                    LEFT JOIN rtb_click_tracker clicktable ON clicktable."AuctionId" = site_r."AuctionId"
                    LEFT JOIN rtb_conversion_tracker conversiontable ON conversiontable."AuctionId" = site_r."AuctionId"
               where site_r."CpId"= page."CpId"
                 and (
                 site_r."Date" >= date_trunc('day',(select date from last_modified where type='lastPrecalculatedTrackerCron') - interval '7 day')
                 and site_r."Date" <= (select date from last_modified where type='lastPrecalculatedTrackerCron'))
               group by site_r."Date"::timestamp::date
               order by site_r."Date"::timestamp::date))) id
        from (
              select
                distinct "CpId"
              from
                rtb_impression_tracker
              where
                "Date" >= date_trunc('day',(select date from last_modified where type='lastPrecalculatedTrackerCron') - interval '7 day')
                and "Date" <= (select date from last_modified where type='lastPrecalculatedTrackerCron')
             ) page;
                    """),

        migrations.RunSQL("""
        insert into ui_usual_campaigns_graph_tracker(
          campaign_id,
          type,
          day_chart
        )
        select
          page."CpId",
          'last_14_days',
          array_to_json(array((select
                 json_build_object(
                 'day', site_r."Date"::timestamp::date,
                 'impression', count(site_r."id"),
                 'mediaspent', sum(site_r."PricePaid"),
                 'clicks', count(clicktable.id),
                 'conversions', count(conversiontable.id),
                 'cpa', case count(conversiontable.id) when 0 then 0 else sum(site_r."PricePaid")/count(conversiontable.id) end,
                 'cpc', case count(clicktable.id) when 0 then 0 else sum(site_r."PricePaid")::float/count(clicktable.id) end,
                 'ctr', case count(site_r."id") when 0 then 0 else count(clicktable.id)::float/count(site_r."id") end)
               from
                    rtb_impression_tracker site_r
                    LEFT JOIN rtb_click_tracker clicktable ON clicktable."AuctionId" = site_r."AuctionId"
                    LEFT JOIN rtb_conversion_tracker conversiontable ON conversiontable."AuctionId" = site_r."AuctionId"
               where site_r."CpId"= page."CpId"
                 and (
                 site_r."Date" >= date_trunc('day',(select date from last_modified where type='lastPrecalculatedTrackerCron') - interval '14 day')
                 and site_r."Date" <= (select date from last_modified where type='lastPrecalculatedTrackerCron'))
               group by site_r."Date"::timestamp::date
               order by site_r."Date"::timestamp::date))) id
        from (
              select
                distinct "CpId"
              from
                rtb_impression_tracker
              where
                "Date" >= date_trunc('day',(select date from last_modified where type='lastPrecalculatedTrackerCron') - interval '14 day')
                and "Date" <= (select date from last_modified where type='lastPrecalculatedTrackerCron')
             ) page;
                    """),

        migrations.RunSQL("""
        insert into ui_usual_campaigns_graph_tracker(
          campaign_id,
          type,
          day_chart
        )
        select
          page."CpId",
          'last_21_days',
          array_to_json(array((select
                 json_build_object(
                 'day', site_r."Date"::timestamp::date,
                 'impression', count(site_r."id"),
                 'mediaspent', sum(site_r."PricePaid"),
                 'clicks', count(clicktable.id),
                 'conversions', count(conversiontable.id),
                 'cpa', case count(conversiontable.id) when 0 then 0 else sum(site_r."PricePaid")/count(conversiontable.id) end,
                 'cpc', case count(clicktable.id) when 0 then 0 else sum(site_r."PricePaid")::float/count(clicktable.id) end,
                 'ctr', case count(site_r."id") when 0 then 0 else count(clicktable.id)::float/count(site_r."id") end)
               from
                    rtb_impression_tracker site_r
                    LEFT JOIN rtb_click_tracker clicktable ON clicktable."AuctionId" = site_r."AuctionId"
                    LEFT JOIN rtb_conversion_tracker conversiontable ON conversiontable."AuctionId" = site_r."AuctionId"
               where site_r."CpId"= page."CpId"
                 and (
                 site_r."Date" >= date_trunc('day',(select date from last_modified where type='lastPrecalculatedTrackerCron') - interval '21 day')
                 and site_r."Date" <= (select date from last_modified where type='lastPrecalculatedTrackerCron'))
               group by site_r."Date"::timestamp::date
               order by site_r."Date"::timestamp::date))) id
        from (
              select
                distinct "CpId"
              from
                rtb_impression_tracker
              where
                "Date" >= date_trunc('day',(select date from last_modified where type='lastPrecalculatedTrackerCron') - interval '21 day')
                and "Date" <= (select date from last_modified where type='lastPrecalculatedTrackerCron')
             ) page;
                    """),

        migrations.RunSQL("""
        insert into ui_usual_campaigns_graph_tracker(
          campaign_id,
          type,
          day_chart
        )
        select
          page."CpId",
          'last_90_days',
          array_to_json(array((select
                 json_build_object(
                 'day', site_r."Date"::timestamp::date,
                 'impression', count(site_r."id"),
                 'mediaspent', sum(site_r."PricePaid"),
                 'clicks', count(clicktable.id),
                 'conversions', count(conversiontable.id),
                 'cpa', case count(conversiontable.id) when 0 then 0 else sum(site_r."PricePaid")/count(conversiontable.id) end,
                 'cpc', case count(clicktable.id) when 0 then 0 else sum(site_r."PricePaid")::float/count(clicktable.id) end,
                 'ctr', case count(site_r."id") when 0 then 0 else count(clicktable.id)::float/count(site_r."id") end)
               from
                    rtb_impression_tracker site_r
                    LEFT JOIN rtb_click_tracker clicktable ON clicktable."AuctionId" = site_r."AuctionId"
                    LEFT JOIN rtb_conversion_tracker conversiontable ON conversiontable."AuctionId" = site_r."AuctionId"
               where site_r."CpId"= page."CpId"
                 and (
                 site_r."Date" >= date_trunc('day',(select date from last_modified where type='lastPrecalculatedTrackerCron') - interval '90 day')
                 and site_r."Date" <= (select date from last_modified where type='lastPrecalculatedTrackerCron'))
               group by site_r."Date"::timestamp::date
               order by site_r."Date"::timestamp::date))) id
        from (
              select
                distinct "CpId"
              from
                rtb_impression_tracker
              where
                "Date" >= date_trunc('day',(select date from last_modified where type='lastPrecalculatedTrackerCron') - interval '90 day')
                and "Date" <= (select date from last_modified where type='lastPrecalculatedTrackerCron')
             ) page;
                    """),

        migrations.RunSQL("""
            insert into ui_usual_campaigns_graph_tracker(
              campaign_id,
              type,
              day_chart
            )
            select
              page."CpId",
              'last_month',
              array_to_json(array((select
                     json_build_object(
                     'day', site_r."Date"::timestamp::date,
                     'impression', count(site_r."id"),
                     'mediaspent', sum(site_r."PricePaid"),
                     'clicks', count(clicktable.id),
                     'conversions', count(conversiontable.id),
                     'cpa', case count(conversiontable.id) when 0 then 0 else sum(site_r."PricePaid")/count(conversiontable.id) end,
                     'cpc', case count(clicktable.id) when 0 then 0 else sum(site_r."PricePaid")::float/count(clicktable.id) end,
                     'ctr', case count(site_r."id") when 0 then 0 else count(clicktable.id)::float/count(site_r."id") end)
                   from
                        rtb_impression_tracker site_r
                        LEFT JOIN rtb_click_tracker clicktable ON clicktable."AuctionId" = site_r."AuctionId"
                        LEFT JOIN rtb_conversion_tracker conversiontable ON conversiontable."AuctionId" = site_r."AuctionId"
                   where site_r."CpId"= page."CpId"
                     and (
                     site_r."Date" >= date_trunc('month',(select date from last_modified where type='lastPrecalculatedTrackerCron') - interval '1 month')
                     and site_r."Date" < (select date from last_modified where type='lastPrecalculatedTrackerCron'))
                   group by site_r."Date"::timestamp::date
                   order by site_r."Date"::timestamp::date))) id
            from (
                  select
                    distinct "CpId"
                  from
                    rtb_impression_tracker
                  where
                    "Date" >= date_trunc('month',(select date from last_modified where type='lastPrecalculatedTrackerCron') - interval '1 month')
                    and "Date" < date_trunc('month',(select date from last_modified where type='lastPrecalculatedTrackerCron'))
                 ) page;
                        """),

        migrations.RunSQL("""
            insert into ui_usual_campaigns_graph_tracker(
              campaign_id,
              type,
              day_chart
            )
            select
              page."CpId",
              'cur_month',
              array_to_json(array((select
                     json_build_object(
                     'day', site_r."Date"::timestamp::date,
                     'impression', count(site_r."id"),
                     'mediaspent', sum(site_r."PricePaid"),
                     'clicks', count(clicktable.id),
                     'conversions', count(conversiontable.id),
                     'cpa', case count(conversiontable.id) when 0 then 0 else sum(site_r."PricePaid")/count(conversiontable.id) end,
                     'cpc', case count(clicktable.id) when 0 then 0 else sum(site_r."PricePaid")::float/count(clicktable.id) end,
                     'ctr', case count(site_r."id") when 0 then 0 else count(clicktable.id)::float/count(site_r."id") end)
                   from
                        rtb_impression_tracker site_r
                        LEFT JOIN rtb_click_tracker clicktable ON clicktable."AuctionId" = site_r."AuctionId"
                        LEFT JOIN rtb_conversion_tracker conversiontable ON conversiontable."AuctionId" = site_r."AuctionId"
                   where site_r."CpId"= page."CpId"
                     and (
                     site_r."Date" >= date_trunc('month',(select date from last_modified where type='lastPrecalculatedTrackerCron'))
                     and site_r."Date" <= (select date from last_modified where type='lastPrecalculatedTrackerCron'))
                   group by site_r."Date"::timestamp::date
                   order by site_r."Date"::timestamp::date))) id
            from (
                  select
                    distinct "CpId"
                  from
                    rtb_impression_tracker
                  where
                    "Date" >= date_trunc('month',(select date from last_modified where type='lastPrecalculatedTrackerCron'))
                    and "Date" <= (select date from last_modified where type='lastPrecalculatedTrackerCron')
                 ) page;
                        """),

        migrations.RunSQL("delete from ui_usual_placements_grid_data_all_tracker"),

        migrations.RunSQL("""
insert into ui_usual_placements_grid_data_all_tracker as ut (
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
  t."CpId",
  t."PlacementId",
  count(t."id") as imps,
  count(clicktable.id) as clicks,
  sum(t."PricePaid") as spend,
  count(conversiontable.id) as conversions,
  0 as imps_viewed,
  0 as view_measured_imps,
  case count(t."id") when 0 then 0 else sum(t."PricePaid") / count(t."id") * 1000.0 end cpm,
  case count(t."id") when 0 then 0 else count(conversiontable.id)::float / count(t."id") end cvr,
  case count(t."id") when 0 then 0 else count(clicktable.id)::float / count(t."id") end ctr,
  case count(clicktable.id) when 0 then 0 else sum(t."PricePaid") / count(clicktable.id) end cpc,
  case count(conversiontable.id) when 0 then 0 else sum(t."PricePaid") / count(conversiontable.id) end cpa,
  0 as view_measurement_rate,
  0 as view_rate
from
  rtb_impression_tracker t
  LEFT JOIN rtb_click_tracker clicktable ON clicktable."AuctionId" = t."AuctionId"
  LEFT JOIN rtb_conversion_tracker conversiontable ON conversiontable."AuctionId" = t."AuctionId"
where
  t."Date" <= (select date from last_modified where type='lastPrecalculatedTrackerCron')
group by
  t."CpId", t."PlacementId"
        """),

        migrations.RunSQL("delete from ui_usual_placements_grid_data_yesterday_tracker"),

        migrations.RunSQL("""
insert into ui_usual_placements_grid_data_yesterday_tracker as ut (
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
  t."CpId",
  t."PlacementId" as id,
  count(t."id") as imps,
  count(clicktable.id) as clicks,
  sum(t."PricePaid") as spend,
  count(conversiontable.id) as conversions,
  0 as imps_viewed,
  0 as view_measured_imps,
  case count(t."id") when 0 then 0 else sum(t."PricePaid") / count(t."id") * 1000.0 end cpm,
  case count(t."id") when 0 then 0 else count(conversiontable.id)::float / count(t."id") end cvr,
  case count(t."id") when 0 then 0 else count(clicktable.id)::float / count(t."id") end ctr,
  case count(clicktable.id) when 0 then 0 else sum(t."PricePaid") / count(clicktable.id) end cpc,
  case count(conversiontable.id) when 0 then 0 else sum(t."PricePaid") / count(conversiontable.id) end cpa,
  0 as view_measurement_rate,
  0 as view_rate
from
  rtb_impression_tracker t
  LEFT JOIN rtb_click_tracker clicktable ON clicktable."AuctionId" = t."AuctionId"
  LEFT JOIN rtb_conversion_tracker conversiontable ON conversiontable."AuctionId" = t."AuctionId"
where
  t."Date" >= date_trunc('day',(select date from last_modified where type='lastPrecalculatedTrackerCron') - interval '1 day')
  and t."Date" <= (select date from last_modified where type='lastPrecalculatedTrackerCron')
group by
  t."CpId", t."PlacementId"
            """),

        migrations.RunSQL("delete from ui_usual_placements_grid_data_last_3_days_tracker"),

        migrations.RunSQL("""
    insert into ui_usual_placements_grid_data_last_3_days_tracker as ut (
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
      t."CpId",
      t."PlacementId" as id,
      count(t."id") as imps,
      count(clicktable.id) as clicks,
      sum(t."PricePaid") as spend,
      count(conversiontable.id) as conversions,
      0 as imps_viewed,
      0 as view_measured_imps,
      case count(t."id") when 0 then 0 else sum(t."PricePaid") / count(t."id") * 1000.0 end cpm,
      case count(t."id") when 0 then 0 else count(conversiontable.id)::float / count(t."id") end cvr,
      case count(t."id") when 0 then 0 else count(clicktable.id)::float / count(t."id") end ctr,
      case count(clicktable.id) when 0 then 0 else sum(t."PricePaid") / count(clicktable.id) end cpc,
      case count(conversiontable.id) when 0 then 0 else sum(t."PricePaid") / count(conversiontable.id) end cpa,
      0 as view_measurement_rate,
      0 as view_rate
    from
      rtb_impression_tracker t
      LEFT JOIN rtb_click_tracker clicktable ON clicktable."AuctionId" = t."AuctionId"
      LEFT JOIN rtb_conversion_tracker conversiontable ON conversiontable."AuctionId" = t."AuctionId"
    where
      t."Date" >= date_trunc('day',(select date from last_modified where type='lastPrecalculatedTrackerCron') - interval '3 day')
      and t."Date" <= (select date from last_modified where type='lastPrecalculatedTrackerCron')
    group by
      t."CpId", t."PlacementId"
                """),

        migrations.RunSQL("delete from ui_usual_placements_grid_data_last_7_days_tracker"),

        migrations.RunSQL("""
    insert into ui_usual_placements_grid_data_last_7_days_tracker as ut (
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
      t."CpId",
      t."PlacementId" as id,
      count(t."id") as imps,
      count(clicktable.id) as clicks,
      sum(t."PricePaid") as spend,
      count(conversiontable.id) as conversions,
      0 as imps_viewed,
      0 as view_measured_imps,
      case count(t."id") when 0 then 0 else sum(t."PricePaid") / count(t."id") * 1000.0 end cpm,
      case count(t."id") when 0 then 0 else count(conversiontable.id)::float / count(t."id") end cvr,
      case count(t."id") when 0 then 0 else count(clicktable.id)::float / count(t."id") end ctr,
      case count(clicktable.id) when 0 then 0 else sum(t."PricePaid") / count(clicktable.id) end cpc,
      case count(conversiontable.id) when 0 then 0 else sum(t."PricePaid") / count(conversiontable.id) end cpa,
      0 as view_measurement_rate,
      0 as view_rate
    from
      rtb_impression_tracker t
      LEFT JOIN rtb_click_tracker clicktable ON clicktable."AuctionId" = t."AuctionId"
      LEFT JOIN rtb_conversion_tracker conversiontable ON conversiontable."AuctionId" = t."AuctionId"
    where
      t."Date" >= date_trunc('day',(select date from last_modified where type='lastPrecalculatedTrackerCron') - interval '7 day')
      and t."Date" <= (select date from last_modified where type='lastPrecalculatedTrackerCron')
    group by
      t."CpId", t."PlacementId"
                """),

        migrations.RunSQL("delete from ui_usual_placements_grid_data_last_14_days_tracker"),

        migrations.RunSQL("""
    insert into ui_usual_placements_grid_data_last_14_days_tracker as ut (
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
      t."CpId",
      t."PlacementId" as id,
      count(t."id") as imps,
      count(clicktable.id) as clicks,
      sum(t."PricePaid") as spend,
      count(conversiontable.id) as conversions,
      0 as imps_viewed,
      0 as view_measured_imps,
      case count(t."id") when 0 then 0 else sum(t."PricePaid") / count(t."id") * 1000.0 end cpm,
      case count(t."id") when 0 then 0 else count(conversiontable.id)::float / count(t."id") end cvr,
      case count(t."id") when 0 then 0 else count(clicktable.id)::float / count(t."id") end ctr,
      case count(clicktable.id) when 0 then 0 else sum(t."PricePaid") / count(clicktable.id) end cpc,
      case count(conversiontable.id) when 0 then 0 else sum(t."PricePaid") / count(conversiontable.id) end cpa,
      0 as view_measurement_rate,
      0 as view_rate
    from
      rtb_impression_tracker t
      LEFT JOIN rtb_click_tracker clicktable ON clicktable."AuctionId" = t."AuctionId"
      LEFT JOIN rtb_conversion_tracker conversiontable ON conversiontable."AuctionId" = t."AuctionId"
    where
      t."Date" >= date_trunc('day',(select date from last_modified where type='lastPrecalculatedTrackerCron') - interval '14 day')
      and t."Date" <= (select date from last_modified where type='lastPrecalculatedTrackerCron')
    group by
      t."CpId", t."PlacementId"
                """),

        migrations.RunSQL("delete from ui_usual_placements_grid_data_last_21_days_tracker"),

        migrations.RunSQL("""
    insert into ui_usual_placements_grid_data_last_21_days_tracker as ut (
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
      t."CpId",
      t."PlacementId" as id,
      count(t."id") as imps,
      count(clicktable.id) as clicks,
      sum(t."PricePaid") as spend,
      count(conversiontable.id) as conversions,
      0 as imps_viewed,
      0 as view_measured_imps,
      case count(t."id") when 0 then 0 else sum(t."PricePaid") / count(t."id") * 1000.0 end cpm,
      case count(t."id") when 0 then 0 else count(conversiontable.id)::float / count(t."id") end cvr,
      case count(t."id") when 0 then 0 else count(clicktable.id)::float / count(t."id") end ctr,
      case count(clicktable.id) when 0 then 0 else sum(t."PricePaid") / count(clicktable.id) end cpc,
      case count(conversiontable.id) when 0 then 0 else sum(t."PricePaid") / count(conversiontable.id) end cpa,
      0 as view_measurement_rate,
      0 as view_rate
    from
      rtb_impression_tracker t
      LEFT JOIN rtb_click_tracker clicktable ON clicktable."AuctionId" = t."AuctionId"
      LEFT JOIN rtb_conversion_tracker conversiontable ON conversiontable."AuctionId" = t."AuctionId"
    where
      t."Date" >= date_trunc('day',(select date from last_modified where type='lastPrecalculatedTrackerCron') - interval '21 day')
      and t."Date" <= (select date from last_modified where type='lastPrecalculatedTrackerCron')
    group by
      t."CpId", t."PlacementId"
                """),

        migrations.RunSQL("delete from ui_usual_placements_grid_data_last_90_days_tracker"),

        migrations.RunSQL("""
    insert into ui_usual_placements_grid_data_last_90_days_tracker as ut (
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
      t."CpId",
      t."PlacementId" as id,
      count(t."id") as imps,
      count(clicktable.id) as clicks,
      sum(t."PricePaid") as spend,
      count(conversiontable.id) as conversions,
      0 as imps_viewed,
      0 as view_measured_imps,
      case count(t."id") when 0 then 0 else sum(t."PricePaid") / count(t."id") * 1000.0 end cpm,
      case count(t."id") when 0 then 0 else count(conversiontable.id)::float / count(t."id") end cvr,
      case count(t."id") when 0 then 0 else count(clicktable.id)::float / count(t."id") end ctr,
      case count(clicktable.id) when 0 then 0 else sum(t."PricePaid") / count(clicktable.id) end cpc,
      case count(conversiontable.id) when 0 then 0 else sum(t."PricePaid") / count(conversiontable.id) end cpa,
      0 as view_measurement_rate,
      0 as view_rate
    from
      rtb_impression_tracker t
      LEFT JOIN rtb_click_tracker clicktable ON clicktable."AuctionId" = t."AuctionId"
      LEFT JOIN rtb_conversion_tracker conversiontable ON conversiontable."AuctionId" = t."AuctionId"
    where
      t."Date" >= date_trunc('day',(select date from last_modified where type='lastPrecalculatedTrackerCron') - interval '90 day')
      and t."Date" <= (select date from last_modified where type='lastPrecalculatedTrackerCron')
    group by
      t."CpId", t."PlacementId"
                """),

        migrations.RunSQL("delete from ui_usual_placements_grid_data_last_month_tracker"),

        migrations.RunSQL("""
        insert into ui_usual_placements_grid_data_last_month_tracker as ut (
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
          t."CpId",
          t."PlacementId" as id,
          count(t."id") as imps,
          count(clicktable.id) as clicks,
          sum(t."PricePaid") as spend,
          count(conversiontable.id) as conversions,
          0 as imps_viewed,
          0 as view_measured_imps,
          case count(t."id") when 0 then 0 else sum(t."PricePaid") / count(t."id") * 1000.0 end cpm,
          case count(t."id") when 0 then 0 else count(conversiontable.id)::float / count(t."id") end cvr,
          case count(t."id") when 0 then 0 else count(clicktable.id)::float / count(t."id") end ctr,
          case count(clicktable.id) when 0 then 0 else sum(t."PricePaid") / count(clicktable.id) end cpc,
          case count(conversiontable.id) when 0 then 0 else sum(t."PricePaid") / count(conversiontable.id) end cpa,
          0 as view_measurement_rate,
          0 as view_rate
        from
          rtb_impression_tracker t
          LEFT JOIN rtb_click_tracker clicktable ON clicktable."AuctionId" = t."AuctionId"
          LEFT JOIN rtb_conversion_tracker conversiontable ON conversiontable."AuctionId" = t."AuctionId"
        where
          t."Date" >= date_trunc('month',(select date from last_modified where type='lastPrecalculatedTrackerCron') - interval '1 month')
          and t."Date" < date_trunc('month',(select date from last_modified where type='lastPrecalculatedTrackerCron'))
        group by
          t."CpId", t."PlacementId"
                    """),

        migrations.RunSQL("delete from ui_usual_placements_grid_data_cur_month_tracker"),

        migrations.RunSQL("""
        insert into ui_usual_placements_grid_data_cur_month_tracker as ut (
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
          t."CpId",
          t."PlacementId" as id,
          count(t."id") as imps,
          count(clicktable.id) as clicks,
          sum(t."PricePaid") as spend,
          count(conversiontable.id) as conversions,
          0 as imps_viewed,
          0 as view_measured_imps,
          case count(t."id") when 0 then 0 else sum(t."PricePaid") / count(t."id") * 1000.0 end cpm,
          case count(t."id") when 0 then 0 else count(conversiontable.id)::float / count(t."id") end cvr,
          case count(t."id") when 0 then 0 else count(clicktable.id)::float / count(t."id") end ctr,
          case count(clicktable.id) when 0 then 0 else sum(t."PricePaid") / count(clicktable.id) end cpc,
          case count(conversiontable.id) when 0 then 0 else sum(t."PricePaid") / count(conversiontable.id) end cpa,
          0 as view_measurement_rate,
          0 as view_rate
        from
          rtb_impression_tracker t
          LEFT JOIN rtb_click_tracker clicktable ON clicktable."AuctionId" = t."AuctionId"
          LEFT JOIN rtb_conversion_tracker conversiontable ON conversiontable."AuctionId" = t."AuctionId"
        where
          t."Date" >= date_trunc('month',(select date from last_modified where type='lastPrecalculatedTrackerCron'))
          and t."Date" <= (select date from last_modified where type='lastPrecalculatedTrackerCron')
        group by
          t."CpId", t."PlacementId"
                    """),

        migrations.RunSQL("delete from ui_usual_advertisers_graph_tracker"),

        migrations.RunSQL("""
    insert into ui_usual_advertisers_graph_tracker (
      advertiser_id,
      type,
      day_chart
    )
    select
      page."AdvId",
      'all',
      array_to_json(array((select
             json_build_object(
             'day', site_r."Date"::timestamp::date,
             'imp', count(site_r."id"),
             'spend', sum(site_r."PricePaid"),
             'clicks', count(clicktable.id),
             'conversions', count(conversiontable.id),
             'cvr', case count(site_r."id") when 0 then 0 else (count(conversiontable.id))::float/count(site_r."id") end,
             'cpc', case count(clicktable.id) when 0 then 0 else sum(site_r."PricePaid")::float/count(clicktable.id) end,
             'ctr', case count(site_r."id") when 0 then 0 else count(clicktable.id)::float/count(site_r."id") end)
           from
                rtb_impression_tracker site_r
                LEFT JOIN rtb_click_tracker clicktable ON clicktable."AuctionId" = site_r."AuctionId"
                LEFT JOIN rtb_conversion_tracker conversiontable ON conversiontable."AuctionId" = site_r."AuctionId"
           where site_r."AdvId"= page."AdvId"
             and site_r."Date" <= (select date from last_modified where type='lastPrecalculatedTrackerCron')
           group by site_r."Date"::timestamp::date
           order by site_r."Date"::timestamp::date))) id
    from (
          select
            distinct "AdvId"
          from
            rtb_impression_tracker
          where
            "Date" <= (select date from last_modified where type='lastPrecalculatedTrackerCron')
         ) page;
                """),

        migrations.RunSQL("""
        insert into ui_usual_advertisers_graph_tracker (
          advertiser_id,
          type,
          day_chart
        )
        select
          page."AdvId",
          'yesterday',
          array_to_json(array((select
                 json_build_object(
                 'day', site_r."Date"::timestamp::date,
                 'imp', count(site_r."id"),
                 'spend', sum(site_r."PricePaid"),
                 'clicks', count(clicktable.id),
                 'conversions', count(conversiontable.id),
                 'cvr', case count(site_r."id") when 0 then 0 else (count(conversiontable.id))::float/count(site_r."id") end,
                 'cpc', case count(clicktable.id) when 0 then 0 else sum(site_r."PricePaid")::float/count(clicktable.id) end,
                 'ctr', case count(site_r."id") when 0 then 0 else count(clicktable.id)::float/count(site_r."id") end)
               from
                    rtb_impression_tracker site_r
                    LEFT JOIN rtb_click_tracker clicktable ON clicktable."AuctionId" = site_r."AuctionId"
                    LEFT JOIN rtb_conversion_tracker conversiontable ON conversiontable."AuctionId" = site_r."AuctionId"
               where site_r."AdvId"= page."AdvId"
                 and (
                 site_r."Date" >= date_trunc('day',(select date from last_modified where type='lastPrecalculatedTrackerCron') - interval '1 day')
                 and site_r."Date" <= (select date from last_modified where type='lastPrecalculatedTrackerCron'))
               group by site_r."Date"::timestamp::date
               order by site_r."Date"::timestamp::date))) id
        from (
              select
                distinct "AdvId"
              from
                rtb_impression_tracker
              where
                "Date" >= date_trunc('day',(select date from last_modified where type='lastPrecalculatedTrackerCron') - interval '1 day')
                and "Date" <= (select date from last_modified where type='lastPrecalculatedTrackerCron')
             ) page;
                    """),

        migrations.RunSQL("""
            insert into ui_usual_advertisers_graph_tracker (
              advertiser_id,
              type,
              day_chart
            )
            select
              page."AdvId",
              'last_3_days',
              array_to_json(array((select
                     json_build_object(
                     'day', site_r."Date"::timestamp::date,
                     'imp', count(site_r."id"),
                     'spend', sum(site_r."PricePaid"),
                     'clicks', count(clicktable.id),
                     'conversions', count(conversiontable.id),
                     'cvr', case count(site_r."id") when 0 then 0 else (count(conversiontable.id))::float/count(site_r."id") end,
                     'cpc', case count(clicktable.id) when 0 then 0 else sum(site_r."PricePaid")::float/count(clicktable.id) end,
                     'ctr', case count(site_r."id") when 0 then 0 else count(clicktable.id)::float/count(site_r."id") end)
                   from
                        rtb_impression_tracker site_r
                        LEFT JOIN rtb_click_tracker clicktable ON clicktable."AuctionId" = site_r."AuctionId"
                        LEFT JOIN rtb_conversion_tracker conversiontable ON conversiontable."AuctionId" = site_r."AuctionId"
                   where site_r."AdvId"= page."AdvId"
                     and (
                     site_r."Date" >= date_trunc('day',(select date from last_modified where type='lastPrecalculatedTrackerCron') - interval '3 day')
                     and site_r."Date" <= (select date from last_modified where type='lastPrecalculatedTrackerCron'))
                   group by site_r."Date"::timestamp::date
                   order by site_r."Date"::timestamp::date))) id
            from (
                  select
                    distinct "AdvId"
                  from
                    rtb_impression_tracker
                  where
                    "Date" >= date_trunc('day',(select date from last_modified where type='lastPrecalculatedTrackerCron') - interval '3 day')
                    and "Date" <= (select date from last_modified where type='lastPrecalculatedTrackerCron')
                 ) page;
                        """),

        migrations.RunSQL("""
            insert into ui_usual_advertisers_graph_tracker (
              advertiser_id,
              type,
              day_chart
            )
            select
              page."AdvId",
              'last_7_days',
              array_to_json(array((select
                     json_build_object(
                     'day', site_r."Date"::timestamp::date,
                     'imp', count(site_r."id"),
                     'spend', sum(site_r."PricePaid"),
                     'clicks', count(clicktable.id),
                     'conversions', count(conversiontable.id),
                     'cvr', case count(site_r."id") when 0 then 0 else (count(conversiontable.id))::float/count(site_r."id") end,
                     'cpc', case count(clicktable.id) when 0 then 0 else sum(site_r."PricePaid")::float/count(clicktable.id) end,
                     'ctr', case count(site_r."id") when 0 then 0 else count(clicktable.id)::float/count(site_r."id") end)
                   from
                        rtb_impression_tracker site_r
                        LEFT JOIN rtb_click_tracker clicktable ON clicktable."AuctionId" = site_r."AuctionId"
                        LEFT JOIN rtb_conversion_tracker conversiontable ON conversiontable."AuctionId" = site_r."AuctionId"
                   where site_r."AdvId"= page."AdvId"
                     and (
                     site_r."Date" >= date_trunc('day',(select date from last_modified where type='lastPrecalculatedTrackerCron') - interval '7 day')
                     and site_r."Date" <= (select date from last_modified where type='lastPrecalculatedTrackerCron'))
                   group by site_r."Date"::timestamp::date
                   order by site_r."Date"::timestamp::date))) id
            from (
                  select
                    distinct "AdvId"
                  from
                    rtb_impression_tracker
                  where
                    "Date" >= date_trunc('day',(select date from last_modified where type='lastPrecalculatedTrackerCron') - interval '7 day')
                    and "Date" <= (select date from last_modified where type='lastPrecalculatedTrackerCron')
                 ) page;
                        """),

        migrations.RunSQL("""
            insert into ui_usual_advertisers_graph_tracker (
              advertiser_id,
              type,
              day_chart
            )
            select
              page."AdvId",
              'last_14_days',
              array_to_json(array((select
                     json_build_object(
                     'day', site_r."Date"::timestamp::date,
                     'imp', count(site_r."id"),
                     'spend', sum(site_r."PricePaid"),
                     'clicks', count(clicktable.id),
                     'conversions', count(conversiontable.id),
                     'cvr', case count(site_r."id") when 0 then 0 else (count(conversiontable.id))::float/count(site_r."id") end,
                     'cpc', case count(clicktable.id) when 0 then 0 else sum(site_r."PricePaid")::float/count(clicktable.id) end,
                     'ctr', case count(site_r."id") when 0 then 0 else count(clicktable.id)::float/count(site_r."id") end)
                   from
                        rtb_impression_tracker site_r
                        LEFT JOIN rtb_click_tracker clicktable ON clicktable."AuctionId" = site_r."AuctionId"
                        LEFT JOIN rtb_conversion_tracker conversiontable ON conversiontable."AuctionId" = site_r."AuctionId"
                   where site_r."AdvId"= page."AdvId"
                     and (
                     site_r."Date" >= date_trunc('day',(select date from last_modified where type='lastPrecalculatedTrackerCron') - interval '14 day')
                     and site_r."Date" <= (select date from last_modified where type='lastPrecalculatedTrackerCron'))
                   group by site_r."Date"::timestamp::date
                   order by site_r."Date"::timestamp::date))) id
            from (
                  select
                    distinct "AdvId"
                  from
                    rtb_impression_tracker
                  where
                    "Date" >= date_trunc('day',(select date from last_modified where type='lastPrecalculatedTrackerCron') - interval '14 day')
                    and "Date" <= (select date from last_modified where type='lastPrecalculatedTrackerCron')
                 ) page;
                        """),

        migrations.RunSQL("""
            insert into ui_usual_advertisers_graph_tracker (
              advertiser_id,
              type,
              day_chart
            )
            select
              page."AdvId",
              'last_21_days',
              array_to_json(array((select
                     json_build_object(
                     'day', site_r."Date"::timestamp::date,
                     'imp', count(site_r."id"),
                     'spend', sum(site_r."PricePaid"),
                     'clicks', count(clicktable.id),
                     'conversions', count(conversiontable.id),
                     'cvr', case count(site_r."id") when 0 then 0 else (count(conversiontable.id))::float/count(site_r."id") end,
                     'cpc', case count(clicktable.id) when 0 then 0 else sum(site_r."PricePaid")::float/count(clicktable.id) end,
                     'ctr', case count(site_r."id") when 0 then 0 else count(clicktable.id)::float/count(site_r."id") end)
                   from
                        rtb_impression_tracker site_r
                        LEFT JOIN rtb_click_tracker clicktable ON clicktable."AuctionId" = site_r."AuctionId"
                        LEFT JOIN rtb_conversion_tracker conversiontable ON conversiontable."AuctionId" = site_r."AuctionId"
                   where site_r."AdvId"= page."AdvId"
                     and (
                     site_r."Date" >= date_trunc('day',(select date from last_modified where type='lastPrecalculatedTrackerCron') - interval '21 day')
                     and site_r."Date" <= (select date from last_modified where type='lastPrecalculatedTrackerCron'))
                   group by site_r."Date"::timestamp::date
                   order by site_r."Date"::timestamp::date))) id
            from (
                  select
                    distinct "AdvId"
                  from
                    rtb_impression_tracker
                  where
                    "Date" >= date_trunc('day',(select date from last_modified where type='lastPrecalculatedTrackerCron') - interval '21 day')
                    and "Date" <= (select date from last_modified where type='lastPrecalculatedTrackerCron')
                 ) page;
                        """),

        migrations.RunSQL("""
            insert into ui_usual_advertisers_graph_tracker (
              advertiser_id,
              type,
              day_chart
            )
            select
              page."AdvId",
              'last_90_days',
              array_to_json(array((select
                     json_build_object(
                     'day', site_r."Date"::timestamp::date,
                     'imp', count(site_r."id"),
                     'spend', sum(site_r."PricePaid"),
                     'clicks', count(clicktable.id),
                     'conversions', count(conversiontable.id),
                     'cvr', case count(site_r."id") when 0 then 0 else (count(conversiontable.id))::float/count(site_r."id") end,
                     'cpc', case count(clicktable.id) when 0 then 0 else sum(site_r."PricePaid")::float/count(clicktable.id) end,
                     'ctr', case count(site_r."id") when 0 then 0 else count(clicktable.id)::float/count(site_r."id") end)
                   from
                        rtb_impression_tracker site_r
                        LEFT JOIN rtb_click_tracker clicktable ON clicktable."AuctionId" = site_r."AuctionId"
                        LEFT JOIN rtb_conversion_tracker conversiontable ON conversiontable."AuctionId" = site_r."AuctionId"
                   where site_r."AdvId"= page."AdvId"
                     and (
                     site_r."Date" >= date_trunc('day',(select date from last_modified where type='lastPrecalculatedTrackerCron') - interval '90 day')
                     and site_r."Date" <= (select date from last_modified where type='lastPrecalculatedTrackerCron'))
                   group by site_r."Date"::timestamp::date
                   order by site_r."Date"::timestamp::date))) id
            from (
                  select
                    distinct "AdvId"
                  from
                    rtb_impression_tracker
                  where
                    "Date" >= date_trunc('day',(select date from last_modified where type='lastPrecalculatedTrackerCron') - interval '90 day')
                    and "Date" <= (select date from last_modified where type='lastPrecalculatedTrackerCron')
                 ) page;
                        """),

        migrations.RunSQL("""
                insert into ui_usual_advertisers_graph_tracker (
                  advertiser_id,
                  type,
                  day_chart
                )
                select
                  page."AdvId",
                  'last_month',
                  array_to_json(array((select
                         json_build_object(
                         'day', site_r."Date"::timestamp::date,
                         'imp', count(site_r."id"),
                         'spend', sum(site_r."PricePaid"),
                         'clicks', count(clicktable.id),
                         'conversions', count(conversiontable.id),
                         'cvr', case count(site_r."id") when 0 then 0 else (count(conversiontable.id))::float/count(site_r."id") end,
                         'cpc', case count(clicktable.id) when 0 then 0 else sum(site_r."PricePaid")::float/count(clicktable.id) end,
                         'ctr', case count(site_r."id") when 0 then 0 else count(clicktable.id)::float/count(site_r."id") end)
                       from
                            rtb_impression_tracker site_r
                            LEFT JOIN rtb_click_tracker clicktable ON clicktable."AuctionId" = site_r."AuctionId"
                            LEFT JOIN rtb_conversion_tracker conversiontable ON conversiontable."AuctionId" = site_r."AuctionId"
                       where site_r."AdvId"= page."AdvId"
                         and (
                         site_r."Date" >= date_trunc('month',(select date from last_modified where type='lastPrecalculatedTrackerCron') - interval '1 month')
                         and site_r."Date" < date_trunc('month',(select date from last_modified where type='lastPrecalculatedTrackerCron')))
                       group by site_r."Date"::timestamp::date
                       order by site_r."Date"::timestamp::date))) id
                from (
                      select
                        distinct "AdvId"
                      from
                        rtb_impression_tracker
                      where
                        "Date" >= date_trunc('month',(select date from last_modified where type='lastPrecalculatedTrackerCron') - interval '1 month')
                        and "Date" < date_trunc('month',(select date from last_modified where type='lastPrecalculatedTrackerCron'))
                     ) page;
                            """),

        migrations.RunSQL("""
                insert into ui_usual_advertisers_graph_tracker (
                  advertiser_id,
                  type,
                  day_chart
                )
                select
                  page."AdvId",
                  'cur_month',
                  array_to_json(array((select
                         json_build_object(
                         'day', site_r."Date"::timestamp::date,
                         'imp', count(site_r."id"),
                         'spend', sum(site_r."PricePaid"),
                         'clicks', count(clicktable.id),
                         'conversions', count(conversiontable.id),
                         'cvr', case count(site_r."id") when 0 then 0 else (count(conversiontable.id))::float/count(site_r."id") end,
                         'cpc', case count(clicktable.id) when 0 then 0 else sum(site_r."PricePaid")::float/count(clicktable.id) end,
                         'ctr', case count(site_r."id") when 0 then 0 else count(clicktable.id)::float/count(site_r."id") end)
                       from
                            rtb_impression_tracker site_r
                            LEFT JOIN rtb_click_tracker clicktable ON clicktable."AuctionId" = site_r."AuctionId"
                            LEFT JOIN rtb_conversion_tracker conversiontable ON conversiontable."AuctionId" = site_r."AuctionId"
                       where site_r."AdvId"= page."AdvId"
                         and (
                         site_r."Date" >= date_trunc('month',(select date from last_modified where type='lastPrecalculatedTrackerCron'))
                         and site_r."Date" <= (select date from last_modified where type='lastPrecalculatedTrackerCron'))
                       group by site_r."Date"::timestamp::date
                       order by site_r."Date"::timestamp::date))) id
                from (
                      select
                        distinct "AdvId"
                      from
                        rtb_impression_tracker
                      where
                        "Date" >= date_trunc('month',(select date from last_modified where type='lastPrecalculatedTrackerCron'))
                        and "Date" <= (select date from last_modified where type='lastPrecalculatedTrackerCron')
                     ) page;
                            """),

        migrations.RunSQL("delete from ui_usual_campaigns_grid_data_all_tracker"),

        migrations.RunSQL("""
    insert into ui_usual_campaigns_grid_data_all_tracker as ut (
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
      page."CpId",
      page.imps,
      page.clicks,
      page.spend,
      page.conversions,
      page.imps_viewed,
      page.view_measured_imps,
      page.cpm,
      page.cvr,
      page.ctr,
      page.cpc,
      page.view_measurement_rate,
      page.view_rate,
      array_to_json(array((select
             json_build_object(
             'day', site_r."Date"::timestamp::date,
             'imp', count(site_r."id"),
             'spend', sum(site_r."PricePaid"),
             'clicks', count(clicktable.id),
             'conversions', count(conversiontable.id),
             'cvr', case count(site_r."id") when 0 then 0 else (count(conversiontable.id))::float/count(site_r."id") end,
             'cpc', case count(clicktable.id) when 0 then 0 else sum(site_r."PricePaid")::float/count(clicktable.id) end,
             'ctr', case count(site_r."id") when 0 then 0 else count(clicktable.id)::float/count(site_r."id") end)
           from
                rtb_impression_tracker site_r
                LEFT JOIN rtb_click_tracker clicktable ON clicktable."AuctionId" = site_r."AuctionId"
                LEFT JOIN rtb_conversion_tracker conversiontable ON conversiontable."AuctionId" = site_r."AuctionId"
           where site_r."CpId"= page."CpId"
           and
             site_r."Date" <= (select date from last_modified where type='lastPrecalculatedTrackerCron')
           group by site_r."Date"::timestamp::date
           order by site_r."Date"::timestamp::date))) id
    from (
          select
            t."CpId",
            count(clicktable.id) as clicks,
            count(conversiontable.id) as conversions,
            count(t."id") as imps,
            sum(t."PricePaid") as spend,
            0 as imps_viewed,
            0 as view_measured_imps,
            case count(t."id") when 0 then 0 else sum(t."PricePaid") / count(t."id") * 1000.0 end cpm,
            case count(t."id") when 0 then 0 else count(conversiontable.id)::float / count(t."id") end cvr,
            case count(t."id") when 0 then 0 else count(clicktable.id)::float / count(t."id") end ctr,
            case count(clicktable.id) when 0 then 0 else sum(t."PricePaid") / count(clicktable.id) end cpc,
            0 as view_measurement_rate,
            0 as view_rate
          from
            rtb_impression_tracker t
            LEFT JOIN rtb_click_tracker clicktable ON clicktable."AuctionId" = t."AuctionId"
            LEFT JOIN rtb_conversion_tracker conversiontable ON conversiontable."AuctionId" = t."AuctionId"
          where
            t."Date" <= (select date from last_modified where type='lastPrecalculatedTrackerCron')
          group by t."CpId"
         ) page;
            """),

        migrations.RunSQL("delete from ui_usual_campaigns_grid_data_yesterday_tracker;"),

        migrations.RunSQL("""
    insert into ui_usual_campaigns_grid_data_yesterday_tracker as ut (
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
      page."CpId",
      page.imps,
      page.clicks,
      page.spend,
      page.conversions,
      page.imps_viewed,
      page.view_measured_imps,
      page.cpm,
      page.cvr,
      page.ctr,
      page.cpc,
      page.view_measurement_rate,
      page.view_rate,
      array_to_json(array((select
             json_build_object(
             'day', site_r."Date"::timestamp::date,
             'imp', count(site_r."id"),
             'spend', sum(site_r."PricePaid"),
             'clicks', count(clicktable.id),
             'conversions', count(conversiontable.id),
             'cvr', case count(site_r."id") when 0 then 0 else (count(conversiontable.id))::float/count(site_r."id") end,
             'cpc', case count(clicktable.id) when 0 then 0 else sum(site_r."PricePaid")::float/count(clicktable.id) end,
             'ctr', case count(site_r."id") when 0 then 0 else count(clicktable.id)::float/count(site_r."id") end)
           from
                rtb_impression_tracker site_r
                LEFT JOIN rtb_click_tracker clicktable ON clicktable."AuctionId" = site_r."AuctionId"
                LEFT JOIN rtb_conversion_tracker conversiontable ON conversiontable."AuctionId" = site_r."AuctionId"
           where site_r."CpId"= page."CpId"
             and (
             site_r."Date" >= date_trunc('day',(select date from last_modified where type='lastPrecalculatedTrackerCron') - interval '1 day')
             and site_r."Date" <= (select date from last_modified where type='lastPrecalculatedTrackerCron'))
           group by site_r."Date"::timestamp::date
           order by site_r."Date"::timestamp::date))) id
    from (
          select
            t."CpId",
            count(clicktable.id) as clicks,
            count(conversiontable.id) as conversions,
            count(t."id") as imps,
            sum(t."PricePaid") as spend,
            0 as imps_viewed,
            0 as view_measured_imps,
            case count(t."id") when 0 then 0 else sum(t."PricePaid") / count(t."id") * 1000.0 end cpm,
            case count(t."id") when 0 then 0 else count(conversiontable.id)::float / count(t."id") end cvr,
            case count(t."id") when 0 then 0 else count(clicktable.id)::float / count(t."id") end ctr,
            case count(clicktable.id) when 0 then 0 else sum(t."PricePaid") / count(clicktable.id) end cpc,
            0 as view_measurement_rate,
            0 as view_rate
          from
            rtb_impression_tracker t
            LEFT JOIN rtb_click_tracker clicktable ON clicktable."AuctionId" = t."AuctionId"
            LEFT JOIN rtb_conversion_tracker conversiontable ON conversiontable."AuctionId" = t."AuctionId"
          where
            t."Date" >= date_trunc('day',(select date from last_modified where type='lastPrecalculatedTrackerCron') - interval '1 day')
            and t."Date" <= (select date from last_modified where type='lastPrecalculatedTrackerCron')
          group by t."CpId"
         ) page;
                """),

        migrations.RunSQL("delete from ui_usual_campaigns_grid_data_last_3_days_tracker"),

        migrations.RunSQL("""
    insert into ui_usual_campaigns_grid_data_last_3_days_tracker as ut (
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
      page."CpId",
      page.imps,
      page.clicks,
      page.spend,
      page.conversions,
      page.imps_viewed,
      page.view_measured_imps,
      page.cpm,
      page.cvr,
      page.ctr,
      page.cpc,
      page.view_measurement_rate,
      page.view_rate,
      array_to_json(array((select
             json_build_object(
             'day', site_r."Date"::timestamp::date,
             'imp', count(site_r."id"),
             'spend', sum(site_r."PricePaid"),
             'clicks', count(clicktable.id),
             'conversions', count(conversiontable.id),
             'cvr', case count(site_r."id") when 0 then 0 else (count(conversiontable.id))::float/count(site_r."id") end,
             'cpc', case count(clicktable.id) when 0 then 0 else sum(site_r."PricePaid")::float/count(clicktable.id) end,
             'ctr', case count(site_r."id") when 0 then 0 else count(clicktable.id)::float/count(site_r."id") end)
           from
                rtb_impression_tracker site_r
                LEFT JOIN rtb_click_tracker clicktable ON clicktable."AuctionId" = site_r."AuctionId"
                LEFT JOIN rtb_conversion_tracker conversiontable ON conversiontable."AuctionId" = site_r."AuctionId"
           where site_r."CpId"= page."CpId"
             and (
             site_r."Date" >= date_trunc('day',(select date from last_modified where type='lastPrecalculatedTrackerCron') - interval '3 day')
             and site_r."Date" <= (select date from last_modified where type='lastPrecalculatedTrackerCron'))
           group by site_r."Date"::timestamp::date
           order by site_r."Date"::timestamp::date))) id
    from (
          select
            t."CpId",
            count(clicktable.id) as clicks,
            count(conversiontable.id) as conversions,
            count(t."id") as imps,
            sum(t."PricePaid") as spend,
            0 as imps_viewed,
            0 as view_measured_imps,
            case count(t."id") when 0 then 0 else sum(t."PricePaid") / count(t."id") * 1000.0 end cpm,
            case count(t."id") when 0 then 0 else count(conversiontable.id)::float / count(t."id") end cvr,
            case count(t."id") when 0 then 0 else count(clicktable.id)::float / count(t."id") end ctr,
            case count(clicktable.id) when 0 then 0 else sum(t."PricePaid") / count(clicktable.id) end cpc,
            0 as view_measurement_rate,
            0 as view_rate
          from
            rtb_impression_tracker t
            LEFT JOIN rtb_click_tracker clicktable ON clicktable."AuctionId" = t."AuctionId"
            LEFT JOIN rtb_conversion_tracker conversiontable ON conversiontable."AuctionId" = t."AuctionId"
          where
            t."Date" >= date_trunc('day',(select date from last_modified where type='lastPrecalculatedTrackerCron') - interval '3 day')
            and t."Date" <= (select date from last_modified where type='lastPrecalculatedTrackerCron')
          group by t."CpId"
         ) page;
                """),

        migrations.RunSQL("delete from ui_usual_campaigns_grid_data_last_7_days_tracker"),

        migrations.RunSQL("""
    insert into ui_usual_campaigns_grid_data_last_7_days_tracker as ut (
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
      page."CpId",
      page.imps,
      page.clicks,
      page.spend,
      page.conversions,
      page.imps_viewed,
      page.view_measured_imps,
      page.cpm,
      page.cvr,
      page.ctr,
      page.cpc,
      page.view_measurement_rate,
      page.view_rate,
      array_to_json(array((select
             json_build_object(
             'day', site_r."Date"::timestamp::date,
             'imp', count(site_r."id"),
             'spend', sum(site_r."PricePaid"),
             'clicks', count(clicktable.id),
             'conversions', count(conversiontable.id),
             'cvr', case count(site_r."id") when 0 then 0 else (count(conversiontable.id))::float/count(site_r."id") end,
             'cpc', case count(clicktable.id) when 0 then 0 else sum(site_r."PricePaid")::float/count(clicktable.id) end,
             'ctr', case count(site_r."id") when 0 then 0 else count(clicktable.id)::float/count(site_r."id") end)
           from
                rtb_impression_tracker site_r
                LEFT JOIN rtb_click_tracker clicktable ON clicktable."AuctionId" = site_r."AuctionId"
                LEFT JOIN rtb_conversion_tracker conversiontable ON conversiontable."AuctionId" = site_r."AuctionId"
           where site_r."CpId"= page."CpId"
             and (
             site_r."Date" >= date_trunc('day',(select date from last_modified where type='lastPrecalculatedTrackerCron') - interval '7 day')
             and site_r."Date" <= (select date from last_modified where type='lastPrecalculatedTrackerCron'))
           group by site_r."Date"::timestamp::date
           order by site_r."Date"::timestamp::date))) id
    from (
          select
            t."CpId",
            count(clicktable.id) as clicks,
            count(conversiontable.id) as conversions,
            count(t."id") as imps,
            sum(t."PricePaid") as spend,
            0 as imps_viewed,
            0 as view_measured_imps,
            case count(t."id") when 0 then 0 else sum(t."PricePaid") / count(t."id") * 1000.0 end cpm,
            case count(t."id") when 0 then 0 else count(conversiontable.id)::float / count(t."id") end cvr,
            case count(t."id") when 0 then 0 else count(clicktable.id)::float / count(t."id") end ctr,
            case count(clicktable.id) when 0 then 0 else sum(t."PricePaid") / count(clicktable.id) end cpc,
            0 as view_measurement_rate,
            0 as view_rate
          from
            rtb_impression_tracker t
            LEFT JOIN rtb_click_tracker clicktable ON clicktable."AuctionId" = t."AuctionId"
            LEFT JOIN rtb_conversion_tracker conversiontable ON conversiontable."AuctionId" = t."AuctionId"
          where
            t."Date" >= date_trunc('day',(select date from last_modified where type='lastPrecalculatedTrackerCron') - interval '7 day')
            and t."Date" <= (select date from last_modified where type='lastPrecalculatedTrackerCron')
          group by t."CpId"
         ) page;
                """),

        migrations.RunSQL("delete from ui_usual_campaigns_grid_data_last_14_days_tracker"),

        migrations.RunSQL("""
    insert into ui_usual_campaigns_grid_data_last_14_days_tracker as ut (
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
      page."CpId",
      page.imps,
      page.clicks,
      page.spend,
      page.conversions,
      page.imps_viewed,
      page.view_measured_imps,
      page.cpm,
      page.cvr,
      page.ctr,
      page.cpc,
      page.view_measurement_rate,
      page.view_rate,
      array_to_json(array((select
             json_build_object(
             'day', site_r."Date"::timestamp::date,
             'imp', count(site_r."id"),
             'spend', sum(site_r."PricePaid"),
             'clicks', count(clicktable.id),
             'conversions', count(conversiontable.id),
             'cvr', case count(site_r."id") when 0 then 0 else (count(conversiontable.id))::float/count(site_r."id") end,
             'cpc', case count(clicktable.id) when 0 then 0 else sum(site_r."PricePaid")::float/count(clicktable.id) end,
             'ctr', case count(site_r."id") when 0 then 0 else count(clicktable.id)::float/count(site_r."id") end)
           from
                rtb_impression_tracker site_r
                LEFT JOIN rtb_click_tracker clicktable ON clicktable."AuctionId" = site_r."AuctionId"
                LEFT JOIN rtb_conversion_tracker conversiontable ON conversiontable."AuctionId" = site_r."AuctionId"
           where site_r."CpId"= page."CpId"
             and (
             site_r."Date" >= date_trunc('day',(select date from last_modified where type='lastPrecalculatedTrackerCron') - interval '14 day')
             and site_r."Date" <= (select date from last_modified where type='lastPrecalculatedTrackerCron'))
           group by site_r."Date"::timestamp::date
           order by site_r."Date"::timestamp::date))) id
    from (
          select
            t."CpId",
            count(clicktable.id) as clicks,
            count(conversiontable.id) as conversions,
            count(t."id") as imps,
            sum(t."PricePaid") as spend,
            0 as imps_viewed,
            0 as view_measured_imps,
            case count(t."id") when 0 then 0 else sum(t."PricePaid") / count(t."id") * 1000.0 end cpm,
            case count(t."id") when 0 then 0 else count(conversiontable.id)::float / count(t."id") end cvr,
            case count(t."id") when 0 then 0 else count(clicktable.id)::float / count(t."id") end ctr,
            case count(clicktable.id) when 0 then 0 else sum(t."PricePaid") / count(clicktable.id) end cpc,
            0 as view_measurement_rate,
            0 as view_rate
          from
            rtb_impression_tracker t
            LEFT JOIN rtb_click_tracker clicktable ON clicktable."AuctionId" = t."AuctionId"
            LEFT JOIN rtb_conversion_tracker conversiontable ON conversiontable."AuctionId" = t."AuctionId"
          where
            t."Date" >= date_trunc('day',(select date from last_modified where type='lastPrecalculatedTrackerCron') - interval '14 day')
            and t."Date" <= (select date from last_modified where type='lastPrecalculatedTrackerCron')
          group by t."CpId"
         ) page;
                """),

        migrations.RunSQL("delete from ui_usual_campaigns_grid_data_last_21_days_tracker"),

        migrations.RunSQL("""
    insert into ui_usual_campaigns_grid_data_last_21_days_tracker as ut (
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
      page."CpId",
      page.imps,
      page.clicks,
      page.spend,
      page.conversions,
      page.imps_viewed,
      page.view_measured_imps,
      page.cpm,
      page.cvr,
      page.ctr,
      page.cpc,
      page.view_measurement_rate,
      page.view_rate,
      array_to_json(array((select
             json_build_object(
             'day', site_r."Date"::timestamp::date,
             'imp', count(site_r."id"),
             'spend', sum(site_r."PricePaid"),
             'clicks', count(clicktable.id),
             'conversions', count(conversiontable.id),
             'cvr', case count(site_r."id") when 0 then 0 else (count(conversiontable.id))::float/count(site_r."id") end,
             'cpc', case count(clicktable.id) when 0 then 0 else sum(site_r."PricePaid")::float/count(clicktable.id) end,
             'ctr', case count(site_r."id") when 0 then 0 else count(clicktable.id)::float/count(site_r."id") end)
           from
                rtb_impression_tracker site_r
                LEFT JOIN rtb_click_tracker clicktable ON clicktable."AuctionId" = site_r."AuctionId"
                LEFT JOIN rtb_conversion_tracker conversiontable ON conversiontable."AuctionId" = site_r."AuctionId"
           where site_r."CpId"= page."CpId"
             and (
             site_r."Date" >= date_trunc('day',(select date from last_modified where type='lastPrecalculatedTrackerCron') - interval '21 day')
             and site_r."Date" <= (select date from last_modified where type='lastPrecalculatedTrackerCron'))
           group by site_r."Date"::timestamp::date
           order by site_r."Date"::timestamp::date))) id
    from (
          select
            t."CpId",
            count(clicktable.id) as clicks,
            count(conversiontable.id) as conversions,
            count(t."id") as imps,
            sum(t."PricePaid") as spend,
            0 as imps_viewed,
            0 as view_measured_imps,
            case count(t."id") when 0 then 0 else sum(t."PricePaid") / count(t."id") * 1000.0 end cpm,
            case count(t."id") when 0 then 0 else count(conversiontable.id)::float / count(t."id") end cvr,
            case count(t."id") when 0 then 0 else count(clicktable.id)::float / count(t."id") end ctr,
            case count(clicktable.id) when 0 then 0 else sum(t."PricePaid") / count(clicktable.id) end cpc,
            0 as view_measurement_rate,
            0 as view_rate
          from
            rtb_impression_tracker t
            LEFT JOIN rtb_click_tracker clicktable ON clicktable."AuctionId" = t."AuctionId"
            LEFT JOIN rtb_conversion_tracker conversiontable ON conversiontable."AuctionId" = t."AuctionId"
          where
            t."Date" >= date_trunc('day',(select date from last_modified where type='lastPrecalculatedTrackerCron') - interval '21 day')
            and t."Date" <= (select date from last_modified where type='lastPrecalculatedTrackerCron')
          group by t."CpId"
         ) page;
                """),

        migrations.RunSQL("delete from ui_usual_campaigns_grid_data_last_90_days_tracker"),

        migrations.RunSQL("""
    insert into ui_usual_campaigns_grid_data_last_90_days_tracker as ut (
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
      page."CpId",
      page.imps,
      page.clicks,
      page.spend,
      page.conversions,
      page.imps_viewed,
      page.view_measured_imps,
      page.cpm,
      page.cvr,
      page.ctr,
      page.cpc,
      page.view_measurement_rate,
      page.view_rate,
      array_to_json(array((select
             json_build_object(
             'day', site_r."Date"::timestamp::date,
             'imp', count(site_r."id"),
             'spend', sum(site_r."PricePaid"),
             'clicks', count(clicktable.id),
             'conversions', count(conversiontable.id),
             'cvr', case count(site_r."id") when 0 then 0 else (count(conversiontable.id))::float/count(site_r."id") end,
             'cpc', case count(clicktable.id) when 0 then 0 else sum(site_r."PricePaid")::float/count(clicktable.id) end,
             'ctr', case count(site_r."id") when 0 then 0 else count(clicktable.id)::float/count(site_r."id") end)
           from
                rtb_impression_tracker site_r
                LEFT JOIN rtb_click_tracker clicktable ON clicktable."AuctionId" = site_r."AuctionId"
                LEFT JOIN rtb_conversion_tracker conversiontable ON conversiontable."AuctionId" = site_r."AuctionId"
           where site_r."CpId"= page."CpId"
             and (
             site_r."Date" >= date_trunc('day',(select date from last_modified where type='lastPrecalculatedTrackerCron') - interval '90 day')
             and site_r."Date" <= (select date from last_modified where type='lastPrecalculatedTrackerCron'))
           group by site_r."Date"::timestamp::date
           order by site_r."Date"::timestamp::date))) id
    from (
          select
            t."CpId",
            count(clicktable.id) as clicks,
            count(conversiontable.id) as conversions,
            count(t."id") as imps,
            sum(t."PricePaid") as spend,
            0 as imps_viewed,
            0 as view_measured_imps,
            case count(t."id") when 0 then 0 else sum(t."PricePaid") / count(t."id") * 1000.0 end cpm,
            case count(t."id") when 0 then 0 else count(conversiontable.id)::float / count(t."id") end cvr,
            case count(t."id") when 0 then 0 else count(clicktable.id)::float / count(t."id") end ctr,
            case count(clicktable.id) when 0 then 0 else sum(t."PricePaid") / count(clicktable.id) end cpc,
            0 as view_measurement_rate,
            0 as view_rate
          from
            rtb_impression_tracker t
            LEFT JOIN rtb_click_tracker clicktable ON clicktable."AuctionId" = t."AuctionId"
            LEFT JOIN rtb_conversion_tracker conversiontable ON conversiontable."AuctionId" = t."AuctionId"
          where
            t."Date" >= date_trunc('day',(select date from last_modified where type='lastPrecalculatedTrackerCron') - interval '90 day')
            and t."Date" <= (select date from last_modified where type='lastPrecalculatedTrackerCron')
          group by t."CpId"
         ) page;
                """),

        migrations.RunSQL("delete from ui_usual_campaigns_grid_data_last_month_tracker"),

        migrations.RunSQL("""
    insert into ui_usual_campaigns_grid_data_last_month_tracker as ut (
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
      page."CpId",
      page.imps,
      page.clicks,
      page.spend,
      page.conversions,
      page.imps_viewed,
      page.view_measured_imps,
      page.cpm,
      page.cvr,
      page.ctr,
      page.cpc,
      page.view_measurement_rate,
      page.view_rate,
      array_to_json(array((select
             json_build_object(
             'day', site_r."Date"::timestamp::date,
             'imp', count(site_r."id"),
             'spend', sum(site_r."PricePaid"),
             'clicks', count(clicktable.id),
             'conversions', count(conversiontable.id),
             'cvr', case count(site_r."id") when 0 then 0 else (count(conversiontable.id))::float/count(site_r."id") end,
             'cpc', case count(clicktable.id) when 0 then 0 else sum(site_r."PricePaid")::float/count(clicktable.id) end,
             'ctr', case count(site_r."id") when 0 then 0 else count(clicktable.id)::float/count(site_r."id") end)
           from
                rtb_impression_tracker site_r
                LEFT JOIN rtb_click_tracker clicktable ON clicktable."AuctionId" = site_r."AuctionId"
                LEFT JOIN rtb_conversion_tracker conversiontable ON conversiontable."AuctionId" = site_r."AuctionId"
           where site_r."CpId"= page."CpId"
             and (
             site_r."Date" >= date_trunc('month',(select date from last_modified where type='lastPrecalculatedTrackerCron') - interval '1 month')
             and site_r."Date" < date_trunc('month',(select date from last_modified where type='lastPrecalculatedTrackerCron')))
           group by site_r."Date"::timestamp::date
           order by site_r."Date"::timestamp::date))) id
    from (
          select
            t."CpId",
            count(clicktable.id) as clicks,
            count(conversiontable.id) as conversions,
            count(t."id") as imps,
            sum(t."PricePaid") as spend,
            0 as imps_viewed,
            0 as view_measured_imps,
            case count(t."id") when 0 then 0 else sum(t."PricePaid") / count(t."id") * 1000.0 end cpm,
            case count(t."id") when 0 then 0 else count(conversiontable.id)::float / count(t."id") end cvr,
            case count(t."id") when 0 then 0 else count(clicktable.id)::float / count(t."id") end ctr,
            case count(clicktable.id) when 0 then 0 else sum(t."PricePaid") / count(clicktable.id) end cpc,
            0 as view_measurement_rate,
            0 as view_rate
          from
            rtb_impression_tracker t
            LEFT JOIN rtb_click_tracker clicktable ON clicktable."AuctionId" = t."AuctionId"
            LEFT JOIN rtb_conversion_tracker conversiontable ON conversiontable."AuctionId" = t."AuctionId"
          where
            t."Date" >= date_trunc('month',(select date from last_modified where type='lastPrecalculatedTrackerCron') - interval '1 month')
            and t."Date" < date_trunc('month',(select date from last_modified where type='lastPrecalculatedTrackerCron'))
          group by t."CpId"
         ) page;
                """),

        migrations.RunSQL("delete from ui_usual_campaigns_grid_data_cur_month_tracker"),

        migrations.RunSQL("""
    insert into ui_usual_campaigns_grid_data_cur_month_tracker as ut (
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
      page."CpId",
      page.imps,
      page.clicks,
      page.spend,
      page.conversions,
      page.imps_viewed,
      page.view_measured_imps,
      page.cpm,
      page.cvr,
      page.ctr,
      page.cpc,
      page.view_measurement_rate,
      page.view_rate,
      array_to_json(array((select
             json_build_object(
             'day', site_r."Date"::timestamp::date,
             'imp', count(site_r."id"),
             'spend', sum(site_r."PricePaid"),
             'clicks', count(clicktable.id),
             'conversions', count(conversiontable.id),
             'cvr', case count(site_r."id") when 0 then 0 else (count(conversiontable.id))::float/count(site_r."id") end,
             'cpc', case count(clicktable.id) when 0 then 0 else sum(site_r."PricePaid")::float/count(clicktable.id) end,
             'ctr', case count(site_r."id") when 0 then 0 else count(clicktable.id)::float/count(site_r."id") end)
           from
                rtb_impression_tracker site_r
                LEFT JOIN rtb_click_tracker clicktable ON clicktable."AuctionId" = site_r."AuctionId"
                LEFT JOIN rtb_conversion_tracker conversiontable ON conversiontable."AuctionId" = site_r."AuctionId"
           where site_r."CpId"= page."CpId"
             and (
             site_r."Date" >= date_trunc('month',(select date from last_modified where type='lastPrecalculatedTrackerCron'))
             and site_r."Date" <= (select date from last_modified where type='lastPrecalculatedTrackerCron'))
           group by site_r."Date"::timestamp::date
           order by site_r."Date"::timestamp::date))) id
    from (
          select
            t."CpId",
            count(clicktable.id) as clicks,
            count(conversiontable.id) as conversions,
            count(t."id") as imps,
            sum(t."PricePaid") as spend,
            0 as imps_viewed,
            0 as view_measured_imps,
            case count(t."id") when 0 then 0 else sum(t."PricePaid") / count(t."id") * 1000.0 end cpm,
            case count(t."id") when 0 then 0 else count(conversiontable.id)::float / count(t."id") end cvr,
            case count(t."id") when 0 then 0 else count(clicktable.id)::float / count(t."id") end ctr,
            case count(clicktable.id) when 0 then 0 else sum(t."PricePaid") / count(clicktable.id) end cpc,
            0 as view_measurement_rate,
            0 as view_rate
          from
            rtb_impression_tracker t
            LEFT JOIN rtb_click_tracker clicktable ON clicktable."AuctionId" = t."AuctionId"
            LEFT JOIN rtb_conversion_tracker conversiontable ON conversiontable."AuctionId" = t."AuctionId"
          where
            t."Date" >= date_trunc('month',(select date from last_modified where type='lastPrecalculatedTrackerCron'))
            and t."Date" <= (select date from last_modified where type='lastPrecalculatedTrackerCron')
          group by t."CpId"
         ) page;
                """),
    ]