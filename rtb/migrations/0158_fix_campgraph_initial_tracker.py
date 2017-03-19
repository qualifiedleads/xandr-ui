from __future__ import unicode_literals

import django.contrib.postgres.fields.jsonb
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('rtb', '0157_ui_tracker_initial_fill_with_indexes'),
    ]

    operations = [
        ##
        # CAMPAIGNS GRAPH
        ##

        # all

        migrations.RunSQL("delete from ui_usual_campaigns_graph_tracker;"),

        migrations.RunSQL("""
    insert into ui_usual_campaigns_graph_tracker as ut (
        campaign_id,
        type,
        day_chart)
      select
      page."CpId",
      'all',
      array_to_json(array((select
             json_build_object(
             'day', site_r."Date"::timestamp::date,
             'impression', count(site_r."id"),
             'mediaspent', sum(site_r."PricePaid"),
             'clicks', 0,
             'conversions', 0,
             'cpa', 0,
             'cpc', 0,
             'ctr', 0)
           from
                rtb_impression_tracker site_r
           where site_r."CpId"= page."CpId"
             and site_r."Date" <= (select date from last_modified where type='lastPrecalculatedTrackerCron')
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
    insert into ui_usual_campaigns_graph_tracker as ut (
        campaign_id,
        type,
        day_chart)
      select
      page."CpId",
      'all',
      array_to_json(array((select
             json_build_object(
             'day', site_r."Date"::timestamp::date,
             'impression', 0,
             'mediaspent', 0,
             'clicks', count(site_r."id"),
             'conversions', 0,
             'cpa', 0,
             'cpc', 0,
             'ctr', 0)
           from
                rtb_click_tracker site_r
           where site_r."CpId"= page."CpId"
             and site_r."Date" <= (select date from last_modified where type='lastPrecalculatedTrackerCron')
           group by site_r."Date"::timestamp::date
           order by site_r."Date"::timestamp::date))) id
    from (
          select
            distinct rtb_click_tracker."CpId"
          from
            rtb_click_tracker
          where
            rtb_click_tracker."Date" <= (select date from last_modified where type='lastPrecalculatedTrackerCron')
         ) page
    ON CONFLICT (campaign_id, type)
      DO UPDATE SET
         day_chart = case (ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'day')::text when (Excluded.day_chart::json->0->'day')::text
                      then jsonb_set(
                        ut.day_chart::jsonb,
                        concat('{', (jsonb_array_length(ut.day_chart)-1), '}')::text[],
                        json_build_object(
                            'day', ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'day',
                            'impression', coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'impression')::text::integer,0),
                            'mediaspent', coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'mediaspent')::text::float,0),
                            'clicks', coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'clicks')::text::integer,0) + coalesce((Excluded.day_chart::json->0->'clicks')::text::integer,0),
                            'conversions', coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'conversions')::text::integer,0),
                            'cpa', case (coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'conversions')::text::integer,0) + coalesce((Excluded.day_chart::json->0->'conversions')::text::integer,0))
                                   when 0 then 0
                                   else (coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'mediaspent')::text::float,0) + coalesce((Excluded.day_chart::json->0->'mediaspent')::text::float,0))/(coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'conversions')::text::float,0) + coalesce((Excluded.day_chart::json->0->'conversions')::text::float,0)) end,
                            'cpc', case (coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'clicks')::text::integer,0) + coalesce((Excluded.day_chart::json->0->'clicks')::text::integer,0))
                                   when 0 then 0
                                   else (coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'mediaspent')::text::float,0) + coalesce((Excluded.day_chart::json->0->'mediaspent')::text::float,0))/(coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'clicks')::text::float,0) + coalesce((Excluded.day_chart::json->0->'clicks')::text::float,0)) end,
                            'ctr', case coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'impression')::text::integer,0) + coalesce((Excluded.day_chart::json->0->'impression')::text::integer,0)
                                   when 0 then 0
                                   else (coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'clicks')::text::float,0) + coalesce((Excluded.day_chart::json->0->'clicks')::text::float,0))/(coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'impression')::text::float,0) + coalesce((Excluded.day_chart::json->0->'impression')::text::float,0)) end
                        )::jsonb,
                        true)
                      else ut.day_chart||Excluded.day_chart end;
                """),

        migrations.RunSQL("""
    insert into ui_usual_campaigns_graph_tracker as ut (
        campaign_id,
        type,
        day_chart)
      select
      page."CpId",
      'all',
      array_to_json(array((select
             json_build_object(
             'day', site_r."Date"::timestamp::date,
             'impression', 0,
             'mediaspent', 0,
             'clicks', 0,
             'conversions', count(site_r."id"),
             'cpa', 0,
             'cpc', 0,
             'ctr', 0)
           from
                rtb_conversion_tracker site_r
           where site_r."CpId"= page."CpId"
             and site_r."Date" <= (select date from last_modified where type='lastPrecalculatedTrackerCron')
           group by site_r."Date"::timestamp::date
           order by site_r."Date"::timestamp::date))) id
    from (
          select
            distinct "CpId"
          from
            rtb_conversion_tracker
          where
            rtb_conversion_tracker."Date" <= (select date from last_modified where type='lastPrecalculatedTrackerCron')
         ) page
    ON CONFLICT (campaign_id, type)
      DO UPDATE SET
         day_chart = case (ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'day')::text when (Excluded.day_chart::json->0->'day')::text
                      then jsonb_set(
                        ut.day_chart::jsonb,
                        concat('{', (jsonb_array_length(ut.day_chart)-1), '}')::text[],
                        json_build_object(
                            'day', ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'day',
                            'impression', coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'impression')::text::integer,0),
                            'mediaspent', coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'mediaspent')::text::float,0),
                            'clicks', coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'clicks')::text::integer,0),
                            'conversions', coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'conversions')::text::integer,0) + coalesce((Excluded.day_chart::json->0->'conversions')::text::integer,0),
                            'cpa', case (coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'conversions')::text::integer,0) + coalesce((Excluded.day_chart::json->0->'conversions')::text::integer,0))
                                   when 0 then 0
                                   else (coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'mediaspent')::text::float,0) + coalesce((Excluded.day_chart::json->0->'mediaspent')::text::float,0))/(coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'conversions')::text::float,0) + coalesce((Excluded.day_chart::json->0->'conversions')::text::float,0)) end,
                            'cpc', case (coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'clicks')::text::integer,0) + coalesce((Excluded.day_chart::json->0->'clicks')::text::integer,0))
                                   when 0 then 0
                                   else (coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'mediaspent')::text::float,0) + coalesce((Excluded.day_chart::json->0->'mediaspent')::text::float,0))/(coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'clicks')::text::float,0) + coalesce((Excluded.day_chart::json->0->'clicks')::text::float,0)) end,
                            'ctr', case coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'impression')::text::integer,0) + coalesce((Excluded.day_chart::json->0->'impression')::text::integer,0)
                                   when 0 then 0
                                   else (coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'clicks')::text::float,0) + coalesce((Excluded.day_chart::json->0->'clicks')::text::float,0))/(coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'impression')::text::float,0) + coalesce((Excluded.day_chart::json->0->'impression')::text::float,0)) end
                        )::jsonb,
                        true)
                      else ut.day_chart||Excluded.day_chart end;
                """),

        # yesterday

        migrations.RunSQL("""
        insert into ui_usual_campaigns_graph_tracker as ut (
            campaign_id,
            type,
            day_chart)
          select
          page."CpId",
          'yesterday',
          array_to_json(array((select
                 json_build_object(
                 'day', site_r."Date"::timestamp::date,
                 'impression', count(site_r."id"),
                 'mediaspent', sum(site_r."PricePaid"),
                 'clicks', 0,
                 'conversions', 0,
                 'cpa', 0,
                 'cpc', 0,
                 'ctr', 0)
               from
                    rtb_impression_tracker site_r
               where site_r."CpId"= page."CpId"
                 and site_r."Date" >= date_trunc('day',(select date from last_modified where type='lastPrecalculatedTrackerCron') - interval '1 day')
                 and site_r."Date" <= (select date from last_modified where type='lastPrecalculatedTrackerCron')
               group by site_r."Date"::timestamp::date
               order by site_r."Date"::timestamp::date))) id
        from (
              select
                distinct "CpId"
              from
                rtb_impression_tracker
              where
                "Date" >= date_trunc('day',(select date from last_modified where type='lastPrecalculatedTrackerCron') - interval '1 day')
                and
                "Date" <= (select date from last_modified where type='lastPrecalculatedTrackerCron')
             ) page;
                """),

        migrations.RunSQL("""
        insert into ui_usual_campaigns_graph_tracker as ut (
            campaign_id,
            type,
            day_chart)
          select
          page."CpId",
          'yesterday',
          array_to_json(array((select
                 json_build_object(
                 'day', site_r."Date"::timestamp::date,
                 'impression', 0,
                 'mediaspent', 0,
                 'clicks', count(site_r."id"),
                 'conversions', 0,
                 'cpa', 0,
                 'cpc', 0,
                 'ctr', 0)
               from
                    rtb_click_tracker site_r
               where site_r."CpId"= page."CpId"
                 and site_r."Date" >= date_trunc('day',(select date from last_modified where type='lastPrecalculatedTrackerCron') - interval '1 day')
                 and site_r."Date" <= (select date from last_modified where type='lastPrecalculatedTrackerCron')
               group by site_r."Date"::timestamp::date
               order by site_r."Date"::timestamp::date))) id
        from (
              select
                distinct rtb_click_tracker."CpId"
              from
                rtb_click_tracker
              where
                rtb_click_tracker."Date" >= date_trunc('day',(select date from last_modified where type='lastPrecalculatedTrackerCron') - interval '1 day')
                and
                rtb_click_tracker."Date" <= (select date from last_modified where type='lastPrecalculatedTrackerCron')
             ) page
        ON CONFLICT (campaign_id, type)
          DO UPDATE SET
             day_chart = case (ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'day')::text when (Excluded.day_chart::json->0->'day')::text
                          then jsonb_set(
                            ut.day_chart::jsonb,
                            concat('{', (jsonb_array_length(ut.day_chart)-1), '}')::text[],
                            json_build_object(
                                'day', ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'day',
                                'impression', coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'impression')::text::integer,0),
                                'mediaspent', coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'mediaspent')::text::float,0),
                                'clicks', coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'clicks')::text::integer,0) + coalesce((Excluded.day_chart::json->0->'clicks')::text::integer,0),
                                'conversions', coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'conversions')::text::integer,0),
                                'cpa', case (coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'conversions')::text::integer,0) + coalesce((Excluded.day_chart::json->0->'conversions')::text::integer,0))
                                       when 0 then 0
                                       else (coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'mediaspent')::text::float,0) + coalesce((Excluded.day_chart::json->0->'mediaspent')::text::float,0))/(coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'conversions')::text::float,0) + coalesce((Excluded.day_chart::json->0->'conversions')::text::float,0)) end,
                                'cpc', case (coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'clicks')::text::integer,0) + coalesce((Excluded.day_chart::json->0->'clicks')::text::integer,0))
                                       when 0 then 0
                                       else (coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'mediaspent')::text::float,0) + coalesce((Excluded.day_chart::json->0->'mediaspent')::text::float,0))/(coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'clicks')::text::float,0) + coalesce((Excluded.day_chart::json->0->'clicks')::text::float,0)) end,
                                'ctr', case coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'impression')::text::integer,0) + coalesce((Excluded.day_chart::json->0->'impression')::text::integer,0)
                                       when 0 then 0
                                       else (coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'clicks')::text::float,0) + coalesce((Excluded.day_chart::json->0->'clicks')::text::float,0))/(coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'impression')::text::float,0) + coalesce((Excluded.day_chart::json->0->'impression')::text::float,0)) end
                            )::jsonb,
                            true)
                          else ut.day_chart||Excluded.day_chart end;
                    """),

        migrations.RunSQL("""
        insert into ui_usual_campaigns_graph_tracker as ut (
            campaign_id,
            type,
            day_chart)
          select
          page."CpId",
          'yesterday',
          array_to_json(array((select
                 json_build_object(
                 'day', site_r."Date"::timestamp::date,
                 'impression', 0,
                 'mediaspent', 0,
                 'clicks', 0,
                 'conversions', count(site_r."id"),
                 'cpa', 0,
                 'cpc', 0,
                 'ctr', 0)
               from
                    rtb_conversion_tracker site_r
               where site_r."CpId"= page."CpId"
                 and site_r."Date" >= date_trunc('day',(select date from last_modified where type='lastPrecalculatedTrackerCron') - interval '1 day')
                 and site_r."Date" <= (select date from last_modified where type='lastPrecalculatedTrackerCron')
               group by site_r."Date"::timestamp::date
               order by site_r."Date"::timestamp::date))) id
        from (
              select
                distinct "CpId"
              from
                rtb_conversion_tracker
              where
                rtb_conversion_tracker."Date" >= date_trunc('day',(select date from last_modified where type='lastPrecalculatedTrackerCron') - interval '1 day')
                and
                rtb_conversion_tracker."Date" <= (select date from last_modified where type='lastPrecalculatedTrackerCron')
             ) page
        ON CONFLICT (campaign_id, type)
          DO UPDATE SET
             day_chart = case (ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'day')::text when (Excluded.day_chart::json->0->'day')::text
                          then jsonb_set(
                            ut.day_chart::jsonb,
                            concat('{', (jsonb_array_length(ut.day_chart)-1), '}')::text[],
                            json_build_object(
                                'day', ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'day',
                                'impression', coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'impression')::text::integer,0),
                                'mediaspent', coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'mediaspent')::text::float,0),
                                'clicks', coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'clicks')::text::integer,0),
                                'conversions', coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'conversions')::text::integer,0) + coalesce((Excluded.day_chart::json->0->'conversions')::text::integer,0),
                                'cpa', case (coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'conversions')::text::integer,0) + coalesce((Excluded.day_chart::json->0->'conversions')::text::integer,0))
                                       when 0 then 0
                                       else (coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'mediaspent')::text::float,0) + coalesce((Excluded.day_chart::json->0->'mediaspent')::text::float,0))/(coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'conversions')::text::float,0) + coalesce((Excluded.day_chart::json->0->'conversions')::text::float,0)) end,
                                'cpc', case (coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'clicks')::text::integer,0) + coalesce((Excluded.day_chart::json->0->'clicks')::text::integer,0))
                                       when 0 then 0
                                       else (coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'mediaspent')::text::float,0) + coalesce((Excluded.day_chart::json->0->'mediaspent')::text::float,0))/(coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'clicks')::text::float,0) + coalesce((Excluded.day_chart::json->0->'clicks')::text::float,0)) end,
                                'ctr', case coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'impression')::text::integer,0) + coalesce((Excluded.day_chart::json->0->'impression')::text::integer,0)
                                       when 0 then 0
                                       else (coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'clicks')::text::float,0) + coalesce((Excluded.day_chart::json->0->'clicks')::text::float,0))/(coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'impression')::text::float,0) + coalesce((Excluded.day_chart::json->0->'impression')::text::float,0)) end
                            )::jsonb,
                            true)
                          else ut.day_chart||Excluded.day_chart end;
                    """),

        # last 3 days

        migrations.RunSQL("""
            insert into ui_usual_campaigns_graph_tracker as ut (
                campaign_id,
                type,
                day_chart)
              select
              page."CpId",
              'last_3_days',
              array_to_json(array((select
                     json_build_object(
                     'day', site_r."Date"::timestamp::date,
                     'impression', count(site_r."id"),
                     'mediaspent', sum(site_r."PricePaid"),
                     'clicks', 0,
                     'conversions', 0,
                     'cpa', 0,
                     'cpc', 0,
                     'ctr', 0)
                   from
                        rtb_impression_tracker site_r
                   where site_r."CpId"= page."CpId"
                     and site_r."Date" >= date_trunc('day',(select date from last_modified where type='lastPrecalculatedTrackerCron') - interval '3 day')
                     and site_r."Date" <= (select date from last_modified where type='lastPrecalculatedTrackerCron')
                   group by site_r."Date"::timestamp::date
                   order by site_r."Date"::timestamp::date))) id
            from (
                  select
                    distinct "CpId"
                  from
                    rtb_impression_tracker
                  where
                    "Date" >= date_trunc('day',(select date from last_modified where type='lastPrecalculatedTrackerCron') - interval '3 day')
                    and
                    "Date" <= (select date from last_modified where type='lastPrecalculatedTrackerCron')
                 ) page;
                    """),

        migrations.RunSQL("""
            insert into ui_usual_campaigns_graph_tracker as ut (
                campaign_id,
                type,
                day_chart)
              select
              page."CpId",
              'last_3_days',
              array_to_json(array((select
                     json_build_object(
                     'day', site_r."Date"::timestamp::date,
                     'impression', 0,
                     'mediaspent', 0,
                     'clicks', count(site_r."id"),
                     'conversions', 0,
                     'cpa', 0,
                     'cpc', 0,
                     'ctr', 0)
                   from
                        rtb_click_tracker site_r
                   where site_r."CpId"= page."CpId"
                     and site_r."Date" >= date_trunc('day',(select date from last_modified where type='lastPrecalculatedTrackerCron') - interval '3 day')
                     and site_r."Date" <= (select date from last_modified where type='lastPrecalculatedTrackerCron')
                   group by site_r."Date"::timestamp::date
                   order by site_r."Date"::timestamp::date))) id
            from (
                  select
                    distinct rtb_click_tracker."CpId"
                  from
                    rtb_click_tracker
                  where
                    rtb_click_tracker."Date" >= date_trunc('day',(select date from last_modified where type='lastPrecalculatedTrackerCron') - interval '3 day')
                    and
                    rtb_click_tracker."Date" <= (select date from last_modified where type='lastPrecalculatedTrackerCron')
                 ) page
            ON CONFLICT (campaign_id, type)
              DO UPDATE SET
                 day_chart = case (ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'day')::text when (Excluded.day_chart::json->0->'day')::text
                              then jsonb_set(
                                ut.day_chart::jsonb,
                                concat('{', (jsonb_array_length(ut.day_chart)-1), '}')::text[],
                                json_build_object(
                                    'day', ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'day',
                                    'impression', coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'impression')::text::integer,0),
                                    'mediaspent', coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'mediaspent')::text::float,0),
                                    'clicks', coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'clicks')::text::integer,0) + coalesce((Excluded.day_chart::json->0->'clicks')::text::integer,0),
                                    'conversions', coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'conversions')::text::integer,0),
                                    'cpa', case (coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'conversions')::text::integer,0) + coalesce((Excluded.day_chart::json->0->'conversions')::text::integer,0))
                                           when 0 then 0
                                           else (coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'mediaspent')::text::float,0) + coalesce((Excluded.day_chart::json->0->'mediaspent')::text::float,0))/(coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'conversions')::text::float,0) + coalesce((Excluded.day_chart::json->0->'conversions')::text::float,0)) end,
                                    'cpc', case (coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'clicks')::text::integer,0) + coalesce((Excluded.day_chart::json->0->'clicks')::text::integer,0))
                                           when 0 then 0
                                           else (coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'mediaspent')::text::float,0) + coalesce((Excluded.day_chart::json->0->'mediaspent')::text::float,0))/(coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'clicks')::text::float,0) + coalesce((Excluded.day_chart::json->0->'clicks')::text::float,0)) end,
                                    'ctr', case coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'impression')::text::integer,0) + coalesce((Excluded.day_chart::json->0->'impression')::text::integer,0)
                                           when 0 then 0
                                           else (coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'clicks')::text::float,0) + coalesce((Excluded.day_chart::json->0->'clicks')::text::float,0))/(coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'impression')::text::float,0) + coalesce((Excluded.day_chart::json->0->'impression')::text::float,0)) end
                                )::jsonb,
                                true)
                              else ut.day_chart||Excluded.day_chart end;
                        """),

        migrations.RunSQL("""
            insert into ui_usual_campaigns_graph_tracker as ut (
                campaign_id,
                type,
                day_chart)
              select
              page."CpId",
              'last_3_days',
              array_to_json(array((select
                     json_build_object(
                     'day', site_r."Date"::timestamp::date,
                     'impression', 0,
                     'mediaspent', 0,
                     'clicks', 0,
                     'conversions', count(site_r."id"),
                     'cpa', 0,
                     'cpc', 0,
                     'ctr', 0)
                   from
                        rtb_conversion_tracker site_r
                   where site_r."CpId"= page."CpId"
                     and site_r."Date" >= date_trunc('day',(select date from last_modified where type='lastPrecalculatedTrackerCron') - interval '3 day')
                     and site_r."Date" <= (select date from last_modified where type='lastPrecalculatedTrackerCron')
                   group by site_r."Date"::timestamp::date
                   order by site_r."Date"::timestamp::date))) id
            from (
                  select
                    distinct "CpId"
                  from
                    rtb_conversion_tracker
                  where
                    rtb_conversion_tracker."Date" >= date_trunc('day',(select date from last_modified where type='lastPrecalculatedTrackerCron') - interval '3 day')
                    and
                    rtb_conversion_tracker."Date" <= (select date from last_modified where type='lastPrecalculatedTrackerCron')
                 ) page
            ON CONFLICT (campaign_id, type)
              DO UPDATE SET
                 day_chart = case (ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'day')::text when (Excluded.day_chart::json->0->'day')::text
                              then jsonb_set(
                                ut.day_chart::jsonb,
                                concat('{', (jsonb_array_length(ut.day_chart)-1), '}')::text[],
                                json_build_object(
                                    'day', ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'day',
                                    'impression', coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'impression')::text::integer,0),
                                    'mediaspent', coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'mediaspent')::text::float,0),
                                    'clicks', coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'clicks')::text::integer,0),
                                    'conversions', coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'conversions')::text::integer,0) + coalesce((Excluded.day_chart::json->0->'conversions')::text::integer,0),
                                    'cpa', case (coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'conversions')::text::integer,0) + coalesce((Excluded.day_chart::json->0->'conversions')::text::integer,0))
                                           when 0 then 0
                                           else (coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'mediaspent')::text::float,0) + coalesce((Excluded.day_chart::json->0->'mediaspent')::text::float,0))/(coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'conversions')::text::float,0) + coalesce((Excluded.day_chart::json->0->'conversions')::text::float,0)) end,
                                    'cpc', case (coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'clicks')::text::integer,0) + coalesce((Excluded.day_chart::json->0->'clicks')::text::integer,0))
                                           when 0 then 0
                                           else (coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'mediaspent')::text::float,0) + coalesce((Excluded.day_chart::json->0->'mediaspent')::text::float,0))/(coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'clicks')::text::float,0) + coalesce((Excluded.day_chart::json->0->'clicks')::text::float,0)) end,
                                    'ctr', case coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'impression')::text::integer,0) + coalesce((Excluded.day_chart::json->0->'impression')::text::integer,0)
                                           when 0 then 0
                                           else (coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'clicks')::text::float,0) + coalesce((Excluded.day_chart::json->0->'clicks')::text::float,0))/(coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'impression')::text::float,0) + coalesce((Excluded.day_chart::json->0->'impression')::text::float,0)) end
                                )::jsonb,
                                true)
                              else ut.day_chart||Excluded.day_chart end;
                        """),

        # last 7 days

        migrations.RunSQL("""
                insert into ui_usual_campaigns_graph_tracker as ut (
                    campaign_id,
                    type,
                    day_chart)
                  select
                  page."CpId",
                  'last_7_days',
                  array_to_json(array((select
                         json_build_object(
                         'day', site_r."Date"::timestamp::date,
                         'impression', count(site_r."id"),
                         'mediaspent', sum(site_r."PricePaid"),
                         'clicks', 0,
                         'conversions', 0,
                         'cpa', 0,
                         'cpc', 0,
                         'ctr', 0)
                       from
                            rtb_impression_tracker site_r
                       where site_r."CpId"= page."CpId"
                         and site_r."Date" >= date_trunc('day',(select date from last_modified where type='lastPrecalculatedTrackerCron') - interval '7 day')
                         and site_r."Date" <= (select date from last_modified where type='lastPrecalculatedTrackerCron')
                       group by site_r."Date"::timestamp::date
                       order by site_r."Date"::timestamp::date))) id
                from (
                      select
                        distinct "CpId"
                      from
                        rtb_impression_tracker
                      where
                        "Date" >= date_trunc('day',(select date from last_modified where type='lastPrecalculatedTrackerCron') - interval '7 day')
                        and
                        "Date" <= (select date from last_modified where type='lastPrecalculatedTrackerCron')
                     ) page;
                        """),

        migrations.RunSQL("""
                insert into ui_usual_campaigns_graph_tracker as ut (
                    campaign_id,
                    type,
                    day_chart)
                  select
                  page."CpId",
                  'last_7_days',
                  array_to_json(array((select
                         json_build_object(
                         'day', site_r."Date"::timestamp::date,
                         'impression', 0,
                         'mediaspent', 0,
                         'clicks', count(site_r."id"),
                         'conversions', 0,
                         'cpa', 0,
                         'cpc', 0,
                         'ctr', 0)
                       from
                            rtb_click_tracker site_r
                       where site_r."CpId"= page."CpId"
                         and site_r."Date" >= date_trunc('day',(select date from last_modified where type='lastPrecalculatedTrackerCron') - interval '7 day')
                         and site_r."Date" <= (select date from last_modified where type='lastPrecalculatedTrackerCron')
                       group by site_r."Date"::timestamp::date
                       order by site_r."Date"::timestamp::date))) id
                from (
                      select
                        distinct rtb_click_tracker."CpId"
                      from
                        rtb_click_tracker
                      where
                        rtb_click_tracker."Date" >= date_trunc('day',(select date from last_modified where type='lastPrecalculatedTrackerCron') - interval '7 day')
                        and
                        rtb_click_tracker."Date" <= (select date from last_modified where type='lastPrecalculatedTrackerCron')
                     ) page
                ON CONFLICT (campaign_id, type)
                  DO UPDATE SET
                     day_chart = case (ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'day')::text when (Excluded.day_chart::json->0->'day')::text
                                  then jsonb_set(
                                    ut.day_chart::jsonb,
                                    concat('{', (jsonb_array_length(ut.day_chart)-1), '}')::text[],
                                    json_build_object(
                                        'day', ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'day',
                                        'impression', coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'impression')::text::integer,0),
                                        'mediaspent', coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'mediaspent')::text::float,0),
                                        'clicks', coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'clicks')::text::integer,0) + coalesce((Excluded.day_chart::json->0->'clicks')::text::integer,0),
                                        'conversions', coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'conversions')::text::integer,0),
                                        'cpa', case (coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'conversions')::text::integer,0) + coalesce((Excluded.day_chart::json->0->'conversions')::text::integer,0))
                                               when 0 then 0
                                               else (coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'mediaspent')::text::float,0) + coalesce((Excluded.day_chart::json->0->'mediaspent')::text::float,0))/(coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'conversions')::text::float,0) + coalesce((Excluded.day_chart::json->0->'conversions')::text::float,0)) end,
                                        'cpc', case (coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'clicks')::text::integer,0) + coalesce((Excluded.day_chart::json->0->'clicks')::text::integer,0))
                                               when 0 then 0
                                               else (coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'mediaspent')::text::float,0) + coalesce((Excluded.day_chart::json->0->'mediaspent')::text::float,0))/(coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'clicks')::text::float,0) + coalesce((Excluded.day_chart::json->0->'clicks')::text::float,0)) end,
                                        'ctr', case coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'impression')::text::integer,0) + coalesce((Excluded.day_chart::json->0->'impression')::text::integer,0)
                                               when 0 then 0
                                               else (coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'clicks')::text::float,0) + coalesce((Excluded.day_chart::json->0->'clicks')::text::float,0))/(coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'impression')::text::float,0) + coalesce((Excluded.day_chart::json->0->'impression')::text::float,0)) end
                                    )::jsonb,
                                    true)
                                  else ut.day_chart||Excluded.day_chart end;
                            """),

        migrations.RunSQL("""
                insert into ui_usual_campaigns_graph_tracker as ut (
                    campaign_id,
                    type,
                    day_chart)
                  select
                  page."CpId",
                  'last_7_days',
                  array_to_json(array((select
                         json_build_object(
                         'day', site_r."Date"::timestamp::date,
                         'impression', 0,
                         'mediaspent', 0,
                         'clicks', 0,
                         'conversions', count(site_r."id"),
                         'cpa', 0,
                         'cpc', 0,
                         'ctr', 0)
                       from
                            rtb_conversion_tracker site_r
                       where site_r."CpId"= page."CpId"
                         and site_r."Date" >= date_trunc('day',(select date from last_modified where type='lastPrecalculatedTrackerCron') - interval '7 day')
                         and site_r."Date" <= (select date from last_modified where type='lastPrecalculatedTrackerCron')
                       group by site_r."Date"::timestamp::date
                       order by site_r."Date"::timestamp::date))) id
                from (
                      select
                        distinct "CpId"
                      from
                        rtb_conversion_tracker
                      where
                        rtb_conversion_tracker."Date" >= date_trunc('day',(select date from last_modified where type='lastPrecalculatedTrackerCron') - interval '7 day')
                        and
                        rtb_conversion_tracker."Date" <= (select date from last_modified where type='lastPrecalculatedTrackerCron')
                     ) page
                ON CONFLICT (campaign_id, type)
                  DO UPDATE SET
                     day_chart = case (ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'day')::text when (Excluded.day_chart::json->0->'day')::text
                                  then jsonb_set(
                                    ut.day_chart::jsonb,
                                    concat('{', (jsonb_array_length(ut.day_chart)-1), '}')::text[],
                                    json_build_object(
                                        'day', ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'day',
                                        'impression', coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'impression')::text::integer,0),
                                        'mediaspent', coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'mediaspent')::text::float,0),
                                        'clicks', coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'clicks')::text::integer,0),
                                        'conversions', coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'conversions')::text::integer,0) + coalesce((Excluded.day_chart::json->0->'conversions')::text::integer,0),
                                        'cpa', case (coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'conversions')::text::integer,0) + coalesce((Excluded.day_chart::json->0->'conversions')::text::integer,0))
                                               when 0 then 0
                                               else (coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'mediaspent')::text::float,0) + coalesce((Excluded.day_chart::json->0->'mediaspent')::text::float,0))/(coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'conversions')::text::float,0) + coalesce((Excluded.day_chart::json->0->'conversions')::text::float,0)) end,
                                        'cpc', case (coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'clicks')::text::integer,0) + coalesce((Excluded.day_chart::json->0->'clicks')::text::integer,0))
                                               when 0 then 0
                                               else (coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'mediaspent')::text::float,0) + coalesce((Excluded.day_chart::json->0->'mediaspent')::text::float,0))/(coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'clicks')::text::float,0) + coalesce((Excluded.day_chart::json->0->'clicks')::text::float,0)) end,
                                        'ctr', case coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'impression')::text::integer,0) + coalesce((Excluded.day_chart::json->0->'impression')::text::integer,0)
                                               when 0 then 0
                                               else (coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'clicks')::text::float,0) + coalesce((Excluded.day_chart::json->0->'clicks')::text::float,0))/(coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'impression')::text::float,0) + coalesce((Excluded.day_chart::json->0->'impression')::text::float,0)) end
                                    )::jsonb,
                                    true)
                                  else ut.day_chart||Excluded.day_chart end;
                            """),

        # last 14 days

        migrations.RunSQL("""
                insert into ui_usual_campaigns_graph_tracker as ut (
                    campaign_id,
                    type,
                    day_chart)
                  select
                  page."CpId",
                  'last_14_days',
                  array_to_json(array((select
                         json_build_object(
                         'day', site_r."Date"::timestamp::date,
                         'impression', count(site_r."id"),
                         'mediaspent', sum(site_r."PricePaid"),
                         'clicks', 0,
                         'conversions', 0,
                         'cpa', 0,
                         'cpc', 0,
                         'ctr', 0)
                       from
                            rtb_impression_tracker site_r
                       where site_r."CpId"= page."CpId"
                         and site_r."Date" >= date_trunc('day',(select date from last_modified where type='lastPrecalculatedTrackerCron') - interval '14 day')
                         and site_r."Date" <= (select date from last_modified where type='lastPrecalculatedTrackerCron')
                       group by site_r."Date"::timestamp::date
                       order by site_r."Date"::timestamp::date))) id
                from (
                      select
                        distinct "CpId"
                      from
                        rtb_impression_tracker
                      where
                        "Date" >= date_trunc('day',(select date from last_modified where type='lastPrecalculatedTrackerCron') - interval '14 day')
                        and
                        "Date" <= (select date from last_modified where type='lastPrecalculatedTrackerCron')
                     ) page;
                        """),

        migrations.RunSQL("""
                insert into ui_usual_campaigns_graph_tracker as ut (
                    campaign_id,
                    type,
                    day_chart)
                  select
                  page."CpId",
                  'last_14_days',
                  array_to_json(array((select
                         json_build_object(
                         'day', site_r."Date"::timestamp::date,
                         'impression', 0,
                         'mediaspent', 0,
                         'clicks', count(site_r."id"),
                         'conversions', 0,
                         'cpa', 0,
                         'cpc', 0,
                         'ctr', 0)
                       from
                            rtb_click_tracker site_r
                       where site_r."CpId"= page."CpId"
                         and site_r."Date" >= date_trunc('day',(select date from last_modified where type='lastPrecalculatedTrackerCron') - interval '14 day')
                         and site_r."Date" <= (select date from last_modified where type='lastPrecalculatedTrackerCron')
                       group by site_r."Date"::timestamp::date
                       order by site_r."Date"::timestamp::date))) id
                from (
                      select
                        distinct rtb_click_tracker."CpId"
                      from
                        rtb_click_tracker
                      where
                        rtb_click_tracker."Date" >= date_trunc('day',(select date from last_modified where type='lastPrecalculatedTrackerCron') - interval '14 day')
                        and
                        rtb_click_tracker."Date" <= (select date from last_modified where type='lastPrecalculatedTrackerCron')
                     ) page
                ON CONFLICT (campaign_id, type)
                  DO UPDATE SET
                     day_chart = case (ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'day')::text when (Excluded.day_chart::json->0->'day')::text
                                  then jsonb_set(
                                    ut.day_chart::jsonb,
                                    concat('{', (jsonb_array_length(ut.day_chart)-1), '}')::text[],
                                    json_build_object(
                                        'day', ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'day',
                                        'impression', coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'impression')::text::integer,0),
                                        'mediaspent', coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'mediaspent')::text::float,0),
                                        'clicks', coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'clicks')::text::integer,0) + coalesce((Excluded.day_chart::json->0->'clicks')::text::integer,0),
                                        'conversions', coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'conversions')::text::integer,0),
                                        'cpa', case (coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'conversions')::text::integer,0) + coalesce((Excluded.day_chart::json->0->'conversions')::text::integer,0))
                                               when 0 then 0
                                               else (coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'mediaspent')::text::float,0) + coalesce((Excluded.day_chart::json->0->'mediaspent')::text::float,0))/(coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'conversions')::text::float,0) + coalesce((Excluded.day_chart::json->0->'conversions')::text::float,0)) end,
                                        'cpc', case (coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'clicks')::text::integer,0) + coalesce((Excluded.day_chart::json->0->'clicks')::text::integer,0))
                                               when 0 then 0
                                               else (coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'mediaspent')::text::float,0) + coalesce((Excluded.day_chart::json->0->'mediaspent')::text::float,0))/(coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'clicks')::text::float,0) + coalesce((Excluded.day_chart::json->0->'clicks')::text::float,0)) end,
                                        'ctr', case coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'impression')::text::integer,0) + coalesce((Excluded.day_chart::json->0->'impression')::text::integer,0)
                                               when 0 then 0
                                               else (coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'clicks')::text::float,0) + coalesce((Excluded.day_chart::json->0->'clicks')::text::float,0))/(coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'impression')::text::float,0) + coalesce((Excluded.day_chart::json->0->'impression')::text::float,0)) end
                                    )::jsonb,
                                    true)
                                  else ut.day_chart||Excluded.day_chart end;
                            """),

        migrations.RunSQL("""
                insert into ui_usual_campaigns_graph_tracker as ut (
                    campaign_id,
                    type,
                    day_chart)
                  select
                  page."CpId",
                  'last_14_days',
                  array_to_json(array((select
                         json_build_object(
                         'day', site_r."Date"::timestamp::date,
                         'impression', 0,
                         'mediaspent', 0,
                         'clicks', 0,
                         'conversions', count(site_r."id"),
                         'cpa', 0,
                         'cpc', 0,
                         'ctr', 0)
                       from
                            rtb_conversion_tracker site_r
                       where site_r."CpId"= page."CpId"
                         and site_r."Date" >= date_trunc('day',(select date from last_modified where type='lastPrecalculatedTrackerCron') - interval '14 day')
                         and site_r."Date" <= (select date from last_modified where type='lastPrecalculatedTrackerCron')
                       group by site_r."Date"::timestamp::date
                       order by site_r."Date"::timestamp::date))) id
                from (
                      select
                        distinct "CpId"
                      from
                        rtb_conversion_tracker
                      where
                        rtb_conversion_tracker."Date" >= date_trunc('day',(select date from last_modified where type='lastPrecalculatedTrackerCron') - interval '14 day')
                        and
                        rtb_conversion_tracker."Date" <= (select date from last_modified where type='lastPrecalculatedTrackerCron')
                     ) page
                ON CONFLICT (campaign_id, type)
                  DO UPDATE SET
                     day_chart = case (ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'day')::text when (Excluded.day_chart::json->0->'day')::text
                                  then jsonb_set(
                                    ut.day_chart::jsonb,
                                    concat('{', (jsonb_array_length(ut.day_chart)-1), '}')::text[],
                                    json_build_object(
                                        'day', ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'day',
                                        'impression', coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'impression')::text::integer,0),
                                        'mediaspent', coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'mediaspent')::text::float,0),
                                        'clicks', coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'clicks')::text::integer,0),
                                        'conversions', coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'conversions')::text::integer,0) + coalesce((Excluded.day_chart::json->0->'conversions')::text::integer,0),
                                        'cpa', case (coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'conversions')::text::integer,0) + coalesce((Excluded.day_chart::json->0->'conversions')::text::integer,0))
                                               when 0 then 0
                                               else (coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'mediaspent')::text::float,0) + coalesce((Excluded.day_chart::json->0->'mediaspent')::text::float,0))/(coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'conversions')::text::float,0) + coalesce((Excluded.day_chart::json->0->'conversions')::text::float,0)) end,
                                        'cpc', case (coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'clicks')::text::integer,0) + coalesce((Excluded.day_chart::json->0->'clicks')::text::integer,0))
                                               when 0 then 0
                                               else (coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'mediaspent')::text::float,0) + coalesce((Excluded.day_chart::json->0->'mediaspent')::text::float,0))/(coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'clicks')::text::float,0) + coalesce((Excluded.day_chart::json->0->'clicks')::text::float,0)) end,
                                        'ctr', case coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'impression')::text::integer,0) + coalesce((Excluded.day_chart::json->0->'impression')::text::integer,0)
                                               when 0 then 0
                                               else (coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'clicks')::text::float,0) + coalesce((Excluded.day_chart::json->0->'clicks')::text::float,0))/(coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'impression')::text::float,0) + coalesce((Excluded.day_chart::json->0->'impression')::text::float,0)) end
                                    )::jsonb,
                                    true)
                                  else ut.day_chart||Excluded.day_chart end;
                            """),

        # last 21 days

        migrations.RunSQL("""
                insert into ui_usual_campaigns_graph_tracker as ut (
                    campaign_id,
                    type,
                    day_chart)
                  select
                  page."CpId",
                  'last_21_days',
                  array_to_json(array((select
                         json_build_object(
                         'day', site_r."Date"::timestamp::date,
                         'impression', count(site_r."id"),
                         'mediaspent', sum(site_r."PricePaid"),
                         'clicks', 0,
                         'conversions', 0,
                         'cpa', 0,
                         'cpc', 0,
                         'ctr', 0)
                       from
                            rtb_impression_tracker site_r
                       where site_r."CpId"= page."CpId"
                         and site_r."Date" >= date_trunc('day',(select date from last_modified where type='lastPrecalculatedTrackerCron') - interval '21 day')
                         and site_r."Date" <= (select date from last_modified where type='lastPrecalculatedTrackerCron')
                       group by site_r."Date"::timestamp::date
                       order by site_r."Date"::timestamp::date))) id
                from (
                      select
                        distinct "CpId"
                      from
                        rtb_impression_tracker
                      where
                        "Date" >= date_trunc('day',(select date from last_modified where type='lastPrecalculatedTrackerCron') - interval '21 day')
                        and
                        "Date" <= (select date from last_modified where type='lastPrecalculatedTrackerCron')
                     ) page;
                        """),

        migrations.RunSQL("""
                insert into ui_usual_campaigns_graph_tracker as ut (
                    campaign_id,
                    type,
                    day_chart)
                  select
                  page."CpId",
                  'last_21_days',
                  array_to_json(array((select
                         json_build_object(
                         'day', site_r."Date"::timestamp::date,
                         'impression', 0,
                         'mediaspent', 0,
                         'clicks', count(site_r."id"),
                         'conversions', 0,
                         'cpa', 0,
                         'cpc', 0,
                         'ctr', 0)
                       from
                            rtb_click_tracker site_r
                       where site_r."CpId"= page."CpId"
                         and site_r."Date" >= date_trunc('day',(select date from last_modified where type='lastPrecalculatedTrackerCron') - interval '21 day')
                         and site_r."Date" <= (select date from last_modified where type='lastPrecalculatedTrackerCron')
                       group by site_r."Date"::timestamp::date
                       order by site_r."Date"::timestamp::date))) id
                from (
                      select
                        distinct rtb_click_tracker."CpId"
                      from
                        rtb_click_tracker
                      where
                        rtb_click_tracker."Date" >= date_trunc('day',(select date from last_modified where type='lastPrecalculatedTrackerCron') - interval '21 day')
                        and
                        rtb_click_tracker."Date" <= (select date from last_modified where type='lastPrecalculatedTrackerCron')
                     ) page
                ON CONFLICT (campaign_id, type)
                  DO UPDATE SET
                     day_chart = case (ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'day')::text when (Excluded.day_chart::json->0->'day')::text
                                  then jsonb_set(
                                    ut.day_chart::jsonb,
                                    concat('{', (jsonb_array_length(ut.day_chart)-1), '}')::text[],
                                    json_build_object(
                                        'day', ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'day',
                                        'impression', coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'impression')::text::integer,0),
                                        'mediaspent', coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'mediaspent')::text::float,0),
                                        'clicks', coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'clicks')::text::integer,0) + coalesce((Excluded.day_chart::json->0->'clicks')::text::integer,0),
                                        'conversions', coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'conversions')::text::integer,0),
                                        'cpa', case (coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'conversions')::text::integer,0) + coalesce((Excluded.day_chart::json->0->'conversions')::text::integer,0))
                                               when 0 then 0
                                               else (coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'mediaspent')::text::float,0) + coalesce((Excluded.day_chart::json->0->'mediaspent')::text::float,0))/(coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'conversions')::text::float,0) + coalesce((Excluded.day_chart::json->0->'conversions')::text::float,0)) end,
                                        'cpc', case (coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'clicks')::text::integer,0) + coalesce((Excluded.day_chart::json->0->'clicks')::text::integer,0))
                                               when 0 then 0
                                               else (coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'mediaspent')::text::float,0) + coalesce((Excluded.day_chart::json->0->'mediaspent')::text::float,0))/(coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'clicks')::text::float,0) + coalesce((Excluded.day_chart::json->0->'clicks')::text::float,0)) end,
                                        'ctr', case coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'impression')::text::integer,0) + coalesce((Excluded.day_chart::json->0->'impression')::text::integer,0)
                                               when 0 then 0
                                               else (coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'clicks')::text::float,0) + coalesce((Excluded.day_chart::json->0->'clicks')::text::float,0))/(coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'impression')::text::float,0) + coalesce((Excluded.day_chart::json->0->'impression')::text::float,0)) end
                                    )::jsonb,
                                    true)
                                  else ut.day_chart||Excluded.day_chart end;
                            """),

        migrations.RunSQL("""
                insert into ui_usual_campaigns_graph_tracker as ut (
                    campaign_id,
                    type,
                    day_chart)
                  select
                  page."CpId",
                  'last_21_days',
                  array_to_json(array((select
                         json_build_object(
                         'day', site_r."Date"::timestamp::date,
                         'impression', 0,
                         'mediaspent', 0,
                         'clicks', 0,
                         'conversions', count(site_r."id"),
                         'cpa', 0,
                         'cpc', 0,
                         'ctr', 0)
                       from
                            rtb_conversion_tracker site_r
                       where site_r."CpId"= page."CpId"
                         and site_r."Date" >= date_trunc('day',(select date from last_modified where type='lastPrecalculatedTrackerCron') - interval '21 day')
                         and site_r."Date" <= (select date from last_modified where type='lastPrecalculatedTrackerCron')
                       group by site_r."Date"::timestamp::date
                       order by site_r."Date"::timestamp::date))) id
                from (
                      select
                        distinct "CpId"
                      from
                        rtb_conversion_tracker
                      where
                        rtb_conversion_tracker."Date" >= date_trunc('day',(select date from last_modified where type='lastPrecalculatedTrackerCron') - interval '21 day')
                        and
                        rtb_conversion_tracker."Date" <= (select date from last_modified where type='lastPrecalculatedTrackerCron')
                     ) page
                ON CONFLICT (campaign_id, type)
                  DO UPDATE SET
                     day_chart = case (ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'day')::text when (Excluded.day_chart::json->0->'day')::text
                                  then jsonb_set(
                                    ut.day_chart::jsonb,
                                    concat('{', (jsonb_array_length(ut.day_chart)-1), '}')::text[],
                                    json_build_object(
                                        'day', ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'day',
                                        'impression', coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'impression')::text::integer,0),
                                        'mediaspent', coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'mediaspent')::text::float,0),
                                        'clicks', coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'clicks')::text::integer,0),
                                        'conversions', coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'conversions')::text::integer,0) + coalesce((Excluded.day_chart::json->0->'conversions')::text::integer,0),
                                        'cpa', case (coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'conversions')::text::integer,0) + coalesce((Excluded.day_chart::json->0->'conversions')::text::integer,0))
                                               when 0 then 0
                                               else (coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'mediaspent')::text::float,0) + coalesce((Excluded.day_chart::json->0->'mediaspent')::text::float,0))/(coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'conversions')::text::float,0) + coalesce((Excluded.day_chart::json->0->'conversions')::text::float,0)) end,
                                        'cpc', case (coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'clicks')::text::integer,0) + coalesce((Excluded.day_chart::json->0->'clicks')::text::integer,0))
                                               when 0 then 0
                                               else (coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'mediaspent')::text::float,0) + coalesce((Excluded.day_chart::json->0->'mediaspent')::text::float,0))/(coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'clicks')::text::float,0) + coalesce((Excluded.day_chart::json->0->'clicks')::text::float,0)) end,
                                        'ctr', case coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'impression')::text::integer,0) + coalesce((Excluded.day_chart::json->0->'impression')::text::integer,0)
                                               when 0 then 0
                                               else (coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'clicks')::text::float,0) + coalesce((Excluded.day_chart::json->0->'clicks')::text::float,0))/(coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'impression')::text::float,0) + coalesce((Excluded.day_chart::json->0->'impression')::text::float,0)) end
                                    )::jsonb,
                                    true)
                                  else ut.day_chart||Excluded.day_chart end;
                            """),

        # last 90 days

        migrations.RunSQL("""
                insert into ui_usual_campaigns_graph_tracker as ut (
                    campaign_id,
                    type,
                    day_chart)
                  select
                  page."CpId",
                  'last_90_days',
                  array_to_json(array((select
                         json_build_object(
                         'day', site_r."Date"::timestamp::date,
                         'impression', count(site_r."id"),
                         'mediaspent', sum(site_r."PricePaid"),
                         'clicks', 0,
                         'conversions', 0,
                         'cpa', 0,
                         'cpc', 0,
                         'ctr', 0)
                       from
                            rtb_impression_tracker site_r
                       where site_r."CpId"= page."CpId"
                         and site_r."Date" >= date_trunc('day',(select date from last_modified where type='lastPrecalculatedTrackerCron') - interval '90 day')
                         and site_r."Date" <= (select date from last_modified where type='lastPrecalculatedTrackerCron')
                       group by site_r."Date"::timestamp::date
                       order by site_r."Date"::timestamp::date))) id
                from (
                      select
                        distinct "CpId"
                      from
                        rtb_impression_tracker
                      where
                        "Date" >= date_trunc('day',(select date from last_modified where type='lastPrecalculatedTrackerCron') - interval '90 day')
                        and
                        "Date" <= (select date from last_modified where type='lastPrecalculatedTrackerCron')
                     ) page;
                        """),

        migrations.RunSQL("""
                insert into ui_usual_campaigns_graph_tracker as ut (
                    campaign_id,
                    type,
                    day_chart)
                  select
                  page."CpId",
                  'last_90_days',
                  array_to_json(array((select
                         json_build_object(
                         'day', site_r."Date"::timestamp::date,
                         'impression', 0,
                         'mediaspent', 0,
                         'clicks', count(site_r."id"),
                         'conversions', 0,
                         'cpa', 0,
                         'cpc', 0,
                         'ctr', 0)
                       from
                            rtb_click_tracker site_r
                       where site_r."CpId"= page."CpId"
                         and site_r."Date" >= date_trunc('day',(select date from last_modified where type='lastPrecalculatedTrackerCron') - interval '90 day')
                         and site_r."Date" <= (select date from last_modified where type='lastPrecalculatedTrackerCron')
                       group by site_r."Date"::timestamp::date
                       order by site_r."Date"::timestamp::date))) id
                from (
                      select
                        distinct rtb_click_tracker."CpId"
                      from
                        rtb_click_tracker
                      where
                        rtb_click_tracker."Date" >= date_trunc('day',(select date from last_modified where type='lastPrecalculatedTrackerCron') - interval '90 day')
                        and
                        rtb_click_tracker."Date" <= (select date from last_modified where type='lastPrecalculatedTrackerCron')
                     ) page
                ON CONFLICT (campaign_id, type)
                  DO UPDATE SET
                     day_chart = case (ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'day')::text when (Excluded.day_chart::json->0->'day')::text
                                  then jsonb_set(
                                    ut.day_chart::jsonb,
                                    concat('{', (jsonb_array_length(ut.day_chart)-1), '}')::text[],
                                    json_build_object(
                                        'day', ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'day',
                                        'impression', coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'impression')::text::integer,0),
                                        'mediaspent', coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'mediaspent')::text::float,0),
                                        'clicks', coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'clicks')::text::integer,0) + coalesce((Excluded.day_chart::json->0->'clicks')::text::integer,0),
                                        'conversions', coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'conversions')::text::integer,0),
                                        'cpa', case (coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'conversions')::text::integer,0) + coalesce((Excluded.day_chart::json->0->'conversions')::text::integer,0))
                                               when 0 then 0
                                               else (coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'mediaspent')::text::float,0) + coalesce((Excluded.day_chart::json->0->'mediaspent')::text::float,0))/(coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'conversions')::text::float,0) + coalesce((Excluded.day_chart::json->0->'conversions')::text::float,0)) end,
                                        'cpc', case (coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'clicks')::text::integer,0) + coalesce((Excluded.day_chart::json->0->'clicks')::text::integer,0))
                                               when 0 then 0
                                               else (coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'mediaspent')::text::float,0) + coalesce((Excluded.day_chart::json->0->'mediaspent')::text::float,0))/(coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'clicks')::text::float,0) + coalesce((Excluded.day_chart::json->0->'clicks')::text::float,0)) end,
                                        'ctr', case coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'impression')::text::integer,0) + coalesce((Excluded.day_chart::json->0->'impression')::text::integer,0)
                                               when 0 then 0
                                               else (coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'clicks')::text::float,0) + coalesce((Excluded.day_chart::json->0->'clicks')::text::float,0))/(coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'impression')::text::float,0) + coalesce((Excluded.day_chart::json->0->'impression')::text::float,0)) end
                                    )::jsonb,
                                    true)
                                  else ut.day_chart||Excluded.day_chart end;
                            """),

        migrations.RunSQL("""
                insert into ui_usual_campaigns_graph_tracker as ut (
                    campaign_id,
                    type,
                    day_chart)
                  select
                  page."CpId",
                  'last_90_days',
                  array_to_json(array((select
                         json_build_object(
                         'day', site_r."Date"::timestamp::date,
                         'impression', 0,
                         'mediaspent', 0,
                         'clicks', 0,
                         'conversions', count(site_r."id"),
                         'cpa', 0,
                         'cpc', 0,
                         'ctr', 0)
                       from
                            rtb_conversion_tracker site_r
                       where site_r."CpId"= page."CpId"
                         and site_r."Date" >= date_trunc('day',(select date from last_modified where type='lastPrecalculatedTrackerCron') - interval '90 day')
                         and site_r."Date" <= (select date from last_modified where type='lastPrecalculatedTrackerCron')
                       group by site_r."Date"::timestamp::date
                       order by site_r."Date"::timestamp::date))) id
                from (
                      select
                        distinct "CpId"
                      from
                        rtb_conversion_tracker
                      where
                        rtb_conversion_tracker."Date" >= date_trunc('day',(select date from last_modified where type='lastPrecalculatedTrackerCron') - interval '90 day')
                        and
                        rtb_conversion_tracker."Date" <= (select date from last_modified where type='lastPrecalculatedTrackerCron')
                     ) page
                ON CONFLICT (campaign_id, type)
                  DO UPDATE SET
                     day_chart = case (ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'day')::text when (Excluded.day_chart::json->0->'day')::text
                                  then jsonb_set(
                                    ut.day_chart::jsonb,
                                    concat('{', (jsonb_array_length(ut.day_chart)-1), '}')::text[],
                                    json_build_object(
                                        'day', ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'day',
                                        'impression', coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'impression')::text::integer,0),
                                        'mediaspent', coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'mediaspent')::text::float,0),
                                        'clicks', coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'clicks')::text::integer,0),
                                        'conversions', coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'conversions')::text::integer,0) + coalesce((Excluded.day_chart::json->0->'conversions')::text::integer,0),
                                        'cpa', case (coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'conversions')::text::integer,0) + coalesce((Excluded.day_chart::json->0->'conversions')::text::integer,0))
                                               when 0 then 0
                                               else (coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'mediaspent')::text::float,0) + coalesce((Excluded.day_chart::json->0->'mediaspent')::text::float,0))/(coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'conversions')::text::float,0) + coalesce((Excluded.day_chart::json->0->'conversions')::text::float,0)) end,
                                        'cpc', case (coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'clicks')::text::integer,0) + coalesce((Excluded.day_chart::json->0->'clicks')::text::integer,0))
                                               when 0 then 0
                                               else (coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'mediaspent')::text::float,0) + coalesce((Excluded.day_chart::json->0->'mediaspent')::text::float,0))/(coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'clicks')::text::float,0) + coalesce((Excluded.day_chart::json->0->'clicks')::text::float,0)) end,
                                        'ctr', case coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'impression')::text::integer,0) + coalesce((Excluded.day_chart::json->0->'impression')::text::integer,0)
                                               when 0 then 0
                                               else (coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'clicks')::text::float,0) + coalesce((Excluded.day_chart::json->0->'clicks')::text::float,0))/(coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'impression')::text::float,0) + coalesce((Excluded.day_chart::json->0->'impression')::text::float,0)) end
                                    )::jsonb,
                                    true)
                                  else ut.day_chart||Excluded.day_chart end;
                            """),

        # last month

        migrations.RunSQL("""
                    insert into ui_usual_campaigns_graph_tracker as ut (
                        campaign_id,
                        type,
                        day_chart)
                      select
                      page."CpId",
                      'last_month',
                      array_to_json(array((select
                             json_build_object(
                             'day', site_r."Date"::timestamp::date,
                             'impression', count(site_r."id"),
                             'mediaspent', sum(site_r."PricePaid"),
                             'clicks', 0,
                             'conversions', 0,
                             'cpa', 0,
                             'cpc', 0,
                             'ctr', 0)
                           from
                                rtb_impression_tracker site_r
                           where site_r."CpId"= page."CpId"
                             and site_r."Date" >= date_trunc('month',(select date from last_modified where type='lastPrecalculatedTrackerCron') - interval '1 month')
                             and site_r."Date" < date_trunc('month',(select date from last_modified where type='lastPrecalculatedTrackerCron'))
                           group by site_r."Date"::timestamp::date
                           order by site_r."Date"::timestamp::date))) id
                    from (
                          select
                            distinct "CpId"
                          from
                            rtb_impression_tracker
                          where
                            "Date" >= date_trunc('month',(select date from last_modified where type='lastPrecalculatedTrackerCron') - interval '1 month')
                            and
                            "Date" < date_trunc('month',(select date from last_modified where type='lastPrecalculatedTrackerCron'))
                         ) page;
                            """),

        migrations.RunSQL("""
                    insert into ui_usual_campaigns_graph_tracker as ut (
                        campaign_id,
                        type,
                        day_chart)
                      select
                      page."CpId",
                      'last_month',
                      array_to_json(array((select
                             json_build_object(
                             'day', site_r."Date"::timestamp::date,
                             'impression', 0,
                             'mediaspent', 0,
                             'clicks', count(site_r."id"),
                             'conversions', 0,
                             'cpa', 0,
                             'cpc', 0,
                             'ctr', 0)
                           from
                                rtb_click_tracker site_r
                           where site_r."CpId"= page."CpId"
                             and site_r."Date" >= date_trunc('month',(select date from last_modified where type='lastPrecalculatedTrackerCron') - interval '1 month')
                             and site_r."Date" < date_trunc('month',(select date from last_modified where type='lastPrecalculatedTrackerCron'))
                           group by site_r."Date"::timestamp::date
                           order by site_r."Date"::timestamp::date))) id
                    from (
                          select
                            distinct rtb_click_tracker."CpId"
                          from
                            rtb_click_tracker
                          where
                            rtb_click_tracker."Date" >= date_trunc('month',(select date from last_modified where type='lastPrecalculatedTrackerCron') - interval '1 month')
                            and
                            rtb_click_tracker."Date" < date_trunc('month',(select date from last_modified where type='lastPrecalculatedTrackerCron'))
                         ) page
                    ON CONFLICT (campaign_id, type)
                      DO UPDATE SET
                         day_chart = case (ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'day')::text when (Excluded.day_chart::json->0->'day')::text
                                      then jsonb_set(
                                        ut.day_chart::jsonb,
                                        concat('{', (jsonb_array_length(ut.day_chart)-1), '}')::text[],
                                        json_build_object(
                                            'day', ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'day',
                                            'impression', coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'impression')::text::integer,0),
                                            'mediaspent', coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'mediaspent')::text::float,0),
                                            'clicks', coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'clicks')::text::integer,0) + coalesce((Excluded.day_chart::json->0->'clicks')::text::integer,0),
                                            'conversions', coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'conversions')::text::integer,0),
                                            'cpa', case (coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'conversions')::text::integer,0) + coalesce((Excluded.day_chart::json->0->'conversions')::text::integer,0))
                                                   when 0 then 0
                                                   else (coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'mediaspent')::text::float,0) + coalesce((Excluded.day_chart::json->0->'mediaspent')::text::float,0))/(coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'conversions')::text::float,0) + coalesce((Excluded.day_chart::json->0->'conversions')::text::float,0)) end,
                                            'cpc', case (coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'clicks')::text::integer,0) + coalesce((Excluded.day_chart::json->0->'clicks')::text::integer,0))
                                                   when 0 then 0
                                                   else (coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'mediaspent')::text::float,0) + coalesce((Excluded.day_chart::json->0->'mediaspent')::text::float,0))/(coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'clicks')::text::float,0) + coalesce((Excluded.day_chart::json->0->'clicks')::text::float,0)) end,
                                            'ctr', case coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'impression')::text::integer,0) + coalesce((Excluded.day_chart::json->0->'impression')::text::integer,0)
                                                   when 0 then 0
                                                   else (coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'clicks')::text::float,0) + coalesce((Excluded.day_chart::json->0->'clicks')::text::float,0))/(coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'impression')::text::float,0) + coalesce((Excluded.day_chart::json->0->'impression')::text::float,0)) end
                                        )::jsonb,
                                        true)
                                      else ut.day_chart||Excluded.day_chart end;
                                """),

        migrations.RunSQL("""
                    insert into ui_usual_campaigns_graph_tracker as ut (
                        campaign_id,
                        type,
                        day_chart)
                      select
                      page."CpId",
                      'last_month',
                      array_to_json(array((select
                             json_build_object(
                             'day', site_r."Date"::timestamp::date,
                             'impression', 0,
                             'mediaspent', 0,
                             'clicks', 0,
                             'conversions', count(site_r."id"),
                             'cpa', 0,
                             'cpc', 0,
                             'ctr', 0)
                           from
                                rtb_conversion_tracker site_r
                           where site_r."CpId"= page."CpId"
                             and site_r."Date" >= date_trunc('month',(select date from last_modified where type='lastPrecalculatedTrackerCron') - interval '1 month')
                             and site_r."Date" < date_trunc('month',(select date from last_modified where type='lastPrecalculatedTrackerCron'))
                           group by site_r."Date"::timestamp::date
                           order by site_r."Date"::timestamp::date))) id
                    from (
                          select
                            distinct "CpId"
                          from
                            rtb_conversion_tracker
                          where
                            rtb_conversion_tracker."Date" >= date_trunc('month',(select date from last_modified where type='lastPrecalculatedTrackerCron') - interval '1 month')
                            and
                            rtb_conversion_tracker."Date" < date_trunc('month',(select date from last_modified where type='lastPrecalculatedTrackerCron'))
                         ) page
                    ON CONFLICT (campaign_id, type)
                      DO UPDATE SET
                         day_chart = case (ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'day')::text when (Excluded.day_chart::json->0->'day')::text
                                      then jsonb_set(
                                        ut.day_chart::jsonb,
                                        concat('{', (jsonb_array_length(ut.day_chart)-1), '}')::text[],
                                        json_build_object(
                                            'day', ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'day',
                                            'impression', coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'impression')::text::integer,0),
                                            'mediaspent', coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'mediaspent')::text::float,0),
                                            'clicks', coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'clicks')::text::integer,0),
                                            'conversions', coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'conversions')::text::integer,0) + coalesce((Excluded.day_chart::json->0->'conversions')::text::integer,0),
                                            'cpa', case (coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'conversions')::text::integer,0) + coalesce((Excluded.day_chart::json->0->'conversions')::text::integer,0))
                                                   when 0 then 0
                                                   else (coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'mediaspent')::text::float,0) + coalesce((Excluded.day_chart::json->0->'mediaspent')::text::float,0))/(coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'conversions')::text::float,0) + coalesce((Excluded.day_chart::json->0->'conversions')::text::float,0)) end,
                                            'cpc', case (coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'clicks')::text::integer,0) + coalesce((Excluded.day_chart::json->0->'clicks')::text::integer,0))
                                                   when 0 then 0
                                                   else (coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'mediaspent')::text::float,0) + coalesce((Excluded.day_chart::json->0->'mediaspent')::text::float,0))/(coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'clicks')::text::float,0) + coalesce((Excluded.day_chart::json->0->'clicks')::text::float,0)) end,
                                            'ctr', case coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'impression')::text::integer,0) + coalesce((Excluded.day_chart::json->0->'impression')::text::integer,0)
                                                   when 0 then 0
                                                   else (coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'clicks')::text::float,0) + coalesce((Excluded.day_chart::json->0->'clicks')::text::float,0))/(coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'impression')::text::float,0) + coalesce((Excluded.day_chart::json->0->'impression')::text::float,0)) end
                                        )::jsonb,
                                        true)
                                      else ut.day_chart||Excluded.day_chart end;
                                """),

        # cur month

        migrations.RunSQL("""
                    insert into ui_usual_campaigns_graph_tracker as ut (
                        campaign_id,
                        type,
                        day_chart)
                      select
                      page."CpId",
                      'cur_month',
                      array_to_json(array((select
                             json_build_object(
                             'day', site_r."Date"::timestamp::date,
                             'impression', count(site_r."id"),
                             'mediaspent', sum(site_r."PricePaid"),
                             'clicks', 0,
                             'conversions', 0,
                             'cpa', 0,
                             'cpc', 0,
                             'ctr', 0)
                           from
                                rtb_impression_tracker site_r
                           where site_r."CpId"= page."CpId"
                             and site_r."Date" >= date_trunc('month',(select date from last_modified where type='lastPrecalculatedTrackerCron'))
                             and site_r."Date" <= (select date from last_modified where type='lastPrecalculatedTrackerCron')
                           group by site_r."Date"::timestamp::date
                           order by site_r."Date"::timestamp::date))) id
                    from (
                          select
                            distinct "CpId"
                          from
                            rtb_impression_tracker
                          where
                            "Date" >= date_trunc('month',(select date from last_modified where type='lastPrecalculatedTrackerCron'))
                            and
                            "Date" <= (select date from last_modified where type='lastPrecalculatedTrackerCron')
                         ) page;
                            """),

        migrations.RunSQL("""
                    insert into ui_usual_campaigns_graph_tracker as ut (
                        campaign_id,
                        type,
                        day_chart)
                      select
                      page."CpId",
                      'cur_month',
                      array_to_json(array((select
                             json_build_object(
                             'day', site_r."Date"::timestamp::date,
                             'impression', 0,
                             'mediaspent', 0,
                             'clicks', count(site_r."id"),
                             'conversions', 0,
                             'cpa', 0,
                             'cpc', 0,
                             'ctr', 0)
                           from
                                rtb_click_tracker site_r
                           where site_r."CpId"= page."CpId"
                             and site_r."Date" >= date_trunc('month',(select date from last_modified where type='lastPrecalculatedTrackerCron'))
                             and site_r."Date" <= (select date from last_modified where type='lastPrecalculatedTrackerCron')
                           group by site_r."Date"::timestamp::date
                           order by site_r."Date"::timestamp::date))) id
                    from (
                          select
                            distinct rtb_click_tracker."CpId"
                          from
                            rtb_click_tracker
                          where
                            rtb_click_tracker."Date" >= date_trunc('month',(select date from last_modified where type='lastPrecalculatedTrackerCron'))
                            and
                            rtb_click_tracker."Date" <= (select date from last_modified where type='lastPrecalculatedTrackerCron')
                         ) page
                    ON CONFLICT (campaign_id, type)
                      DO UPDATE SET
                         day_chart = case (ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'day')::text when (Excluded.day_chart::json->0->'day')::text
                                      then jsonb_set(
                                        ut.day_chart::jsonb,
                                        concat('{', (jsonb_array_length(ut.day_chart)-1), '}')::text[],
                                        json_build_object(
                                            'day', ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'day',
                                            'impression', coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'impression')::text::integer,0),
                                            'mediaspent', coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'mediaspent')::text::float,0),
                                            'clicks', coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'clicks')::text::integer,0) + coalesce((Excluded.day_chart::json->0->'clicks')::text::integer,0),
                                            'conversions', coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'conversions')::text::integer,0),
                                            'cpa', case (coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'conversions')::text::integer,0) + coalesce((Excluded.day_chart::json->0->'conversions')::text::integer,0))
                                                   when 0 then 0
                                                   else (coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'mediaspent')::text::float,0) + coalesce((Excluded.day_chart::json->0->'mediaspent')::text::float,0))/(coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'conversions')::text::float,0) + coalesce((Excluded.day_chart::json->0->'conversions')::text::float,0)) end,
                                            'cpc', case (coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'clicks')::text::integer,0) + coalesce((Excluded.day_chart::json->0->'clicks')::text::integer,0))
                                                   when 0 then 0
                                                   else (coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'mediaspent')::text::float,0) + coalesce((Excluded.day_chart::json->0->'mediaspent')::text::float,0))/(coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'clicks')::text::float,0) + coalesce((Excluded.day_chart::json->0->'clicks')::text::float,0)) end,
                                            'ctr', case coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'impression')::text::integer,0) + coalesce((Excluded.day_chart::json->0->'impression')::text::integer,0)
                                                   when 0 then 0
                                                   else (coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'clicks')::text::float,0) + coalesce((Excluded.day_chart::json->0->'clicks')::text::float,0))/(coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'impression')::text::float,0) + coalesce((Excluded.day_chart::json->0->'impression')::text::float,0)) end
                                        )::jsonb,
                                        true)
                                      else ut.day_chart||Excluded.day_chart end;
                                """),

        migrations.RunSQL("""
                    insert into ui_usual_campaigns_graph_tracker as ut (
                        campaign_id,
                        type,
                        day_chart)
                      select
                      page."CpId",
                      'cur_month',
                      array_to_json(array((select
                             json_build_object(
                             'day', site_r."Date"::timestamp::date,
                             'impression', 0,
                             'mediaspent', 0,
                             'clicks', 0,
                             'conversions', count(site_r."id"),
                             'cpa', 0,
                             'cpc', 0,
                             'ctr', 0)
                           from
                                rtb_conversion_tracker site_r
                           where site_r."CpId"= page."CpId"
                             and site_r."Date" >= date_trunc('month',(select date from last_modified where type='lastPrecalculatedTrackerCron'))
                             and site_r."Date" <= (select date from last_modified where type='lastPrecalculatedTrackerCron')
                           group by site_r."Date"::timestamp::date
                           order by site_r."Date"::timestamp::date))) id
                    from (
                          select
                            distinct "CpId"
                          from
                            rtb_conversion_tracker
                          where
                            rtb_conversion_tracker."Date" >= date_trunc('month',(select date from last_modified where type='lastPrecalculatedTrackerCron'))
                            and
                            rtb_conversion_tracker."Date" <= (select date from last_modified where type='lastPrecalculatedTrackerCron')
                         ) page
                    ON CONFLICT (campaign_id, type)
                      DO UPDATE SET
                         day_chart = case (ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'day')::text when (Excluded.day_chart::json->0->'day')::text
                                      then jsonb_set(
                                        ut.day_chart::jsonb,
                                        concat('{', (jsonb_array_length(ut.day_chart)-1), '}')::text[],
                                        json_build_object(
                                            'day', ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'day',
                                            'impression', coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'impression')::text::integer,0),
                                            'mediaspent', coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'mediaspent')::text::float,0),
                                            'clicks', coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'clicks')::text::integer,0),
                                            'conversions', coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'conversions')::text::integer,0) + coalesce((Excluded.day_chart::json->0->'conversions')::text::integer,0),
                                            'cpa', case (coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'conversions')::text::integer,0) + coalesce((Excluded.day_chart::json->0->'conversions')::text::integer,0))
                                                   when 0 then 0
                                                   else (coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'mediaspent')::text::float,0) + coalesce((Excluded.day_chart::json->0->'mediaspent')::text::float,0))/(coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'conversions')::text::float,0) + coalesce((Excluded.day_chart::json->0->'conversions')::text::float,0)) end,
                                            'cpc', case (coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'clicks')::text::integer,0) + coalesce((Excluded.day_chart::json->0->'clicks')::text::integer,0))
                                                   when 0 then 0
                                                   else (coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'mediaspent')::text::float,0) + coalesce((Excluded.day_chart::json->0->'mediaspent')::text::float,0))/(coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'clicks')::text::float,0) + coalesce((Excluded.day_chart::json->0->'clicks')::text::float,0)) end,
                                            'ctr', case coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'impression')::text::integer,0) + coalesce((Excluded.day_chart::json->0->'impression')::text::integer,0)
                                                   when 0 then 0
                                                   else (coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'clicks')::text::float,0) + coalesce((Excluded.day_chart::json->0->'clicks')::text::float,0))/(coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'impression')::text::float,0) + coalesce((Excluded.day_chart::json->0->'impression')::text::float,0)) end
                                        )::jsonb,
                                        true)
                                      else ut.day_chart||Excluded.day_chart end;
                                """),

    ]