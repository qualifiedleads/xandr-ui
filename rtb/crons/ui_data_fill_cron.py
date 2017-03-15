from datetime import timedelta, datetime
from django.db import connection, transaction
from django.utils import timezone
from rtb.models.placement_state import LastModified
#
# PLACEMENTS GRID REPORT
#

def cummulatePlacementsGridData(type, start_date, finish_date):
    with connection.cursor() as cursor:
        cursor.execute("""
insert into ui_usual_placements_grid_data_""" + str(type) + """ as ut (
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
    t."hour" > '""" + str(start_date) +"""' and t."hour" <= '"""+ str(finish_date) + """'
  group by
    t.campaign_id, t.placement_id
ON CONFLICT (campaign_id, placement_id)
  DO UPDATE SET
     imps = coalesce(ut.imps, 0) + coalesce(Excluded.imps, 0),
     clicks = coalesce(ut.clicks, 0) + coalesce(Excluded.clicks, 0),
     spent = coalesce(ut.spent, 0) + coalesce(Excluded.spent, 0),
     conversions = coalesce(ut.conversions, 0) + coalesce(Excluded.conversions, 0),
     imps_viewed = coalesce(ut.imps_viewed, 0) + coalesce(Excluded.imps_viewed, 0),
     view_measured_imps = coalesce(ut.view_measured_imps, 0) + coalesce(Excluded.view_measured_imps, 0),
     cpm = case (coalesce(ut.imps, 0) + coalesce(Excluded.imps, 0)) when 0 then 0 else (coalesce(ut.spent, 0) + coalesce(Excluded.spent, 0)) / (coalesce(ut.imps, 0) + coalesce(Excluded.imps, 0)) * 1000.0 end,
     cvr = case (coalesce(ut.imps, 0) + coalesce(Excluded.imps, 0)) when 0 then 0 else (coalesce(ut.conversions, 0) + coalesce(Excluded.conversions, 0))::float / (coalesce(ut.imps, 0) + coalesce(Excluded.imps, 0)) end,
     ctr = case (coalesce(ut.imps, 0) + coalesce(Excluded.imps, 0)) when 0 then 0 else (coalesce(ut.clicks, 0) + coalesce(Excluded.clicks, 0))::float / (coalesce(ut.imps, 0) + coalesce(Excluded.imps, 0)) end,
     cpc = case (coalesce(ut.clicks, 0) + coalesce(Excluded.clicks, 0)) when 0 then 0 else (coalesce(ut.spent, 0) + coalesce(Excluded.spent, 0)) / (coalesce(ut.clicks, 0) + coalesce(Excluded.clicks, 0)) end,
     cpa = case (coalesce(ut.conversions, 0) + coalesce(Excluded.conversions, 0)) when 0 then 0 else (coalesce(ut.spent, 0) + coalesce(Excluded.spent, 0)) / (coalesce(ut.conversions, 0) + coalesce(Excluded.conversions, 0)) end,
     view_measurement_rate = case (coalesce(ut.imps, 0) + coalesce(Excluded.imps, 0)) when 0 then 0 else (coalesce(ut.view_measured_imps, 0) + coalesce(Excluded.view_measured_imps, 0))::float / (coalesce(ut.imps, 0) + coalesce(Excluded.imps, 0)) end,
     view_rate = case (coalesce(ut.view_measured_imps, 0) + coalesce(Excluded.view_measured_imps, 0)) when 0 then 0 else (coalesce(ut.imps_viewed, 0) + coalesce(Excluded.imps_viewed, 0))::float / (coalesce(ut.view_measured_imps, 0) + coalesce(Excluded.view_measured_imps, 0)) end;
""")

def subPlacementsGridData(type, start_date, finish_date):
    with connection.cursor() as cursor:
        cursor.execute("""
update ui_usual_placements_grid_data_""" + str(type) + """ as ut
set
  imps = ut.imps - info.imp,
  clicks = ut.clicks - info.clicks,
  spent = ut.spent - info.spent,
  conversions = ut.conversions - info.conversions,
  imps_viewed = ut.imps_viewed - info.imps_viewed,
  view_measured_imps = ut.view_measured_imps - info.view_measured_imps,
  cpm = case (ut.imps - info.imp) when 0 then 0 else (ut.spent - info.spent) / (ut.imps - info.imp) * 1000.0 end,
  cvr = case (ut.imps - info.imp) when 0 then 0 else (ut.conversions - info.conversions) / (ut.imps - info.imp) end,
  ctr = case (ut.imps - info.imp) when 0 then 0 else (ut.clicks - info.clicks) / (ut.imps - info.imp) end,
  cpc = case (ut.clicks - info.clicks) when 0 then 0 else (ut.spent - info.spent) / (ut.clicks - info.clicks) end,
  cpa = case (ut.conversions - info.conversions) when 0 then 0 else (ut.spent - info.spent) / (ut.conversions - info.conversions) end,
  view_measurement_rate = case (imps - info.imp) when 0 then 0 else (ut.view_measured_imps - info.view_measured_imps) / (ut.imps - info.imp) end,
  view_rate = case (ut.view_measured_imps - info.view_measured_imps) when 0 then 0 else (ut.imps_viewed - info.imps_viewed) / (ut.view_measured_imps - info.view_measured_imps) end
FROM (
  select
    campaign_id,
    placement_id,
    sum(imps) imp,
    sum(clicks) clicks,
    sum("cost") spent,
    sum(total_convs) conversions,
    sum(imps_viewed) imps_viewed,
    sum(view_measured_imps) view_measured_imps
  from
    network_analytics_report_by_placement
  where
    "hour" >= '""" + str(start_date) +"""' and "hour" < '""" + str(finish_date) + """'
  group by
    campaign_id, placement_id
) info
where ut.campaign_id = info.campaign_id and ut.placement_id = info.placement_id;
""")

def refreshPlacementsLastMonthGridData(start_date, finish_date):
    with connection.cursor() as cursor:
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
        t."hour" >= '""" + str(start_date) + """' and t."hour" < '""" + str(finish_date) + """'
      group by
        t.campaign_id, t.placement_id
    ON CONFLICT (campaign_id, placement_id)
      DO UPDATE SET
         imps = coalesce(Excluded.imps, 0),
         clicks = coalesce(Excluded.clicks, 0),
         spent = coalesce(Excluded.spent, 0),
         conversions = coalesce(Excluded.conversions, 0),
         imps_viewed = coalesce(Excluded.imps_viewed, 0),
         view_measured_imps = coalesce(Excluded.view_measured_imps, 0),
         cpm = case coalesce(Excluded.imps, 0) when 0 then 0 else coalesce(Excluded.spent, 0) / coalesce(Excluded.imps, 0) * 1000.0 end,
         cvr = case coalesce(Excluded.imps, 0) when 0 then 0 else coalesce(Excluded.conversions, 0)::float / coalesce(Excluded.imps, 0) end,
         ctr = case coalesce(Excluded.imps, 0) when 0 then 0 else coalesce(Excluded.clicks, 0)::float / coalesce(Excluded.imps, 0) end,
         cpc = case coalesce(Excluded.clicks, 0) when 0 then 0 else coalesce(Excluded.spent, 0) / coalesce(Excluded.clicks, 0) end,
         cpa = case coalesce(Excluded.conversions, 0) when 0 then 0 else coalesce(Excluded.spent, 0) / (coalesce(ut.conversions, 0) + coalesce(Excluded.conversions, 0)) end,
         view_measurement_rate = case coalesce(Excluded.imps, 0) when 0 then 0 else coalesce(Excluded.view_measured_imps, 0)::float / coalesce(Excluded.imps, 0) end,
         view_rate = case coalesce(Excluded.view_measured_imps, 0) when 0 then 0 else coalesce(Excluded.imps_viewed, 0)::float / coalesce(Excluded.view_measured_imps, 0) end;
    """)

#
# CAMPAIGNS GRID REPORT
#

def cummulateCampaignsGridData(type, start_date, finish_date):
    with connection.cursor() as cursor:
        cursor.execute("""
insert into ui_usual_campaigns_grid_data_""" + str(type) + """ as ut (
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
           and site_r.hour > '""" + str(start_date) + """' and site_r.hour <= '""" + str(finish_date) + """'
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
        site_r1.hour > '""" + str(start_date) + """'
        and site_r1.hour <= '""" + str(finish_date) + """'
      WINDOW w as (partition by site_r1.campaign_id order by site_r1.day desc)
     ) page
ON CONFLICT (campaign_id)
  DO UPDATE SET
     imps = coalesce(ut.imps, 0) + coalesce(Excluded.imps, 0),
     clicks = coalesce(ut.clicks, 0) + coalesce(Excluded.clicks, 0),
     spent = coalesce(ut.spent, 0) + coalesce(Excluded.spent, 0),
     conversions = coalesce(ut.conversions, 0) + coalesce(Excluded.conversions, 0),
     imps_viewed = coalesce(ut.imps_viewed, 0) + coalesce(Excluded.imps_viewed, 0),
     view_measured_imps = coalesce(ut.view_measured_imps, 0) + coalesce(Excluded.view_measured_imps, 0),
     cpm = case (coalesce(ut.imps, 0) + coalesce(Excluded.imps, 0)) when 0 then 0 else (coalesce(ut.spent, 0) + coalesce(Excluded.spent, 0)) / (coalesce(ut.imps, 0) + coalesce(Excluded.imps, 0)) * 1000.0 end,
     cvr = case (coalesce(ut.imps, 0) + coalesce(Excluded.imps, 0)) when 0 then 0 else (coalesce(ut.conversions, 0) + coalesce(Excluded.conversions, 0))::float / (coalesce(ut.imps, 0) + coalesce(Excluded.imps, 0)) end,
     ctr = case (coalesce(ut.imps, 0) + coalesce(Excluded.imps, 0)) when 0 then 0 else (coalesce(ut.clicks, 0) + coalesce(Excluded.clicks, 0))::float / (coalesce(ut.imps, 0) + coalesce(Excluded.imps, 0)) end,
     cpc = case (coalesce(ut.clicks, 0) + coalesce(Excluded.clicks, 0)) when 0 then 0 else (coalesce(ut.spent, 0) + coalesce(Excluded.spent, 0)) / (coalesce(ut.clicks, 0) + coalesce(Excluded.clicks, 0)) end,
     view_measurement_rate = case (coalesce(ut.imps, 0) + coalesce(Excluded.imps, 0)) when 0 then 0 else (coalesce(ut.view_measured_imps, 0) + coalesce(Excluded.view_measured_imps, 0))::float / (coalesce(ut.imps, 0) + coalesce(Excluded.imps, 0)) end,
     view_rate = case (coalesce(ut.view_measured_imps, 0) + coalesce(Excluded.view_measured_imps, 0)) when 0 then 0 else (coalesce(ut.imps_viewed, 0) + coalesce(Excluded.imps_viewed, 0))::float / (coalesce(ut.view_measured_imps, 0) + coalesce(Excluded.view_measured_imps, 0)) end,
     day_chart = case (ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'day')::text when (Excluded.day_chart::json->0->'day')::text
                  then jsonb_set(
                    ut.day_chart::jsonb,
                    concat('{', (jsonb_array_length(ut.day_chart)-1), '}')::text[],
                    json_build_object(
                        'day', ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'day',
                        'imp', coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'imp')::text::integer,0) + coalesce((Excluded.day_chart::json->0->'imp')::text::integer,0),
                        'spend', coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'spend')::text::float,0) + coalesce((Excluded.day_chart::json->0->'spend')::text::float,0),
                        'clicks', coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'clicks')::text::integer,0) + coalesce((Excluded.day_chart::json->0->'clicks')::text::integer,0),
                        'conversions', coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'conversions')::text::integer,0) + coalesce((Excluded.day_chart::json->0->'conversions')::text::integer,0),
                        'cvr', case (coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'imp')::text::integer,0) + coalesce((Excluded.day_chart::json->0->'imp')::text::integer,0))
                               when 0 then 0
                               else (coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'conversions')::text::float,0) + coalesce((Excluded.day_chart::json->0->'conversions')::text::float,0))/(coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'imp')::text::float,0) + coalesce((Excluded.day_chart::json->0->'imp')::text::float,0)) end,
                        'cpc', case (coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'clicks')::text::integer,0) + coalesce((Excluded.day_chart::json->0->'clicks')::text::integer,0))
                               when 0 then 0
                               else (coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'spend')::text::float,0) + coalesce((Excluded.day_chart::json->0->'spend')::text::float,0))/(coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'clicks')::text::float,0) + coalesce((Excluded.day_chart::json->0->'clicks')::text::float,0)) end,
                        'ctr', case coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'imp')::text::integer,0) + coalesce((Excluded.day_chart::json->0->'imp')::text::integer,0)
                               when 0 then 0
                               else (coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'clicks')::text::float,0) + coalesce((Excluded.day_chart::json->0->'clicks')::text::float,0))/(coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'imp')::text::float,0) + coalesce((Excluded.day_chart::json->0->'imp')::text::float,0)) end
                    )::jsonb,
                    true)
                  else ut.day_chart||Excluded.day_chart end;
""")

def subCampaignsGridData(type, start_date, finish_date):
    with connection.cursor() as cursor:
        cursor.execute("""
update ui_usual_campaigns_grid_data_""" + str(type) + """ as ut
set
  imps = ut.imps - info.imp,
  clicks = ut.clicks - info.clicks,
  spent = ut.spent - info.spent,
  conversions = ut.conversions - info.conversions,
  imps_viewed = ut.imps_viewed - info.imps_viewed,
  view_measured_imps = ut.view_measured_imps - info.view_measured_imps,
  cpm = case (ut.imps - info.imp) when 0 then 0 else (ut.spent - info.spent) / (ut.imps - info.imp) * 1000.0 end,
  cvr = case (ut.imps - info.imp) when 0 then 0 else (ut.conversions - info.conversions) / (ut.imps - info.imp) end,
  ctr = case (ut.imps - info.imp) when 0 then 0 else (ut.clicks - info.clicks) / (ut.imps - info.imp) end,
  cpc = case (ut.clicks - info.clicks) when 0 then 0 else (ut.spent - info.spent) / (ut.clicks - info.clicks) end,
  view_measurement_rate = case (imps - info.imp) when 0 then 0 else (ut.view_measured_imps - info.view_measured_imps) / (ut.imps - info.imp) end,
  view_rate = case (ut.view_measured_imps - info.view_measured_imps) when 0 then 0 else (ut.imps_viewed - info.imps_viewed) / (ut.view_measured_imps - info.view_measured_imps) end,
  day_chart = day_chart - 0
FROM (
  select
    campaign_id,
    sum(imps) imp,
    sum(clicks) clicks,
    sum(media_cost) spent,
    (sum(post_click_convs) + sum(post_view_convs)) conversions,
    sum(imps_viewed) imps_viewed,
    sum(view_measured_imps) view_measured_imps
  from
    site_domain_performance_report
  where
    "hour" >= '""" + str(start_date) + """' and "hour" < '""" + str(finish_date) + """'
  group by
    campaign_id
) info
where ut.campaign_id = info.campaign_id;
""")

def refreshCampaignsLastMonthGridData(start_date, finish_date):
    with connection.cursor() as cursor:
        cursor.execute("""
insert into ui_usual_campaigns_grid_data_""" + str(type) + """ as ut (
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
           and site_r.hour >= '""" + str(start_date) + """' and site_r.hour < '""" + str(finish_date) + """'
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
        site_r1.hour >= '""" + str(start_date) + """'
        and site_r1.hour < '""" + str(finish_date) + """'
      WINDOW w as (partition by site_r1.campaign_id order by site_r1.day desc)
     ) page
ON CONFLICT (campaign_id)
  DO UPDATE SET
     imps = coalesce(Excluded.imps, 0),
     clicks = coalesce(Excluded.clicks, 0),
     spent = coalesce(Excluded.spent, 0),
     conversions = coalesce(Excluded.conversions, 0),
     imps_viewed = coalesce(Excluded.imps_viewed, 0),
     view_measured_imps = coalesce(Excluded.view_measured_imps, 0),
     cpm = case coalesce(Excluded.imps, 0) when 0 then 0 else coalesce(Excluded.spent, 0) / coalesce(Excluded.imps, 0) * 1000.0 end,
     cvr = case coalesce(Excluded.imps, 0) when 0 then 0 else coalesce(Excluded.conversions, 0)::float / coalesce(Excluded.imps, 0) end,
     ctr = case coalesce(Excluded.imps, 0) when 0 then 0 else  coalesce(Excluded.clicks, 0)::float / coalesce(Excluded.imps, 0) end,
     cpc = case coalesce(Excluded.clicks, 0) when 0 then 0 else coalesce(Excluded.spent, 0) / coalesce(Excluded.clicks, 0) end,
     view_measurement_rate = case coalesce(Excluded.imps, 0) when 0 then 0 else coalesce(Excluded.view_measured_imps, 0)::float / coalesce(Excluded.imps, 0) end,
     view_rate = case coalesce(Excluded.view_measured_imps, 0) when 0 then 0 else coalesce(Excluded.imps_viewed, 0)::float / coalesce(Excluded.view_measured_imps, 0) end,
     day_chart = Excluded.day_chart;
    """)

#
# ADVERTISERS GRAPH REPORT
#

def cummulateAdvertisersGraphData(type, start_date, finish_date):
    with connection.cursor() as cursor:
        cursor.execute("""
insert into ui_usual_advertisers_graph as ut (
    advertiser_id,
    type,
    day_chart)
  select
  ads.advertiser_id,
  '""" + str(type) + """',
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
     "hour" > '""" + str(start_date) + """'
      and
      "hour" <= '""" + str(finish_date) + """'
    group by "day"
    order by "day"
  ))
from (
       select distinct advertiser_id from site_domain_performance_report
        where
         "hour" > '""" + str(start_date) + """'
          and
          "hour" <= '""" + str(finish_date) + """') ads
ON CONFLICT (advertiser_id, type)
  DO UPDATE SET
     day_chart = case (ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'day')::text when (Excluded.day_chart::json->0->'day')::text
                  then jsonb_set(
                    ut.day_chart::jsonb,
                    concat('{', (jsonb_array_length(ut.day_chart)-1), '}')::text[],
                    json_build_object(
                        'day', ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'day',
                        'imp', coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'imp')::text::integer,0) + coalesce((Excluded.day_chart::json->0->'imp')::text::integer,0),
                        'spend', coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'spend')::text::float,0) + coalesce((Excluded.day_chart::json->0->'spend')::text::float,0),
                        'clicks', coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'clicks')::text::integer,0) + coalesce((Excluded.day_chart::json->0->'clicks')::text::integer,0),
                        'conversions', coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'conversions')::text::integer,0) + coalesce((Excluded.day_chart::json->0->'conversions')::text::integer,0),
                        'cvr', case (coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'imp')::text::integer,0) + coalesce((Excluded.day_chart::json->0->'imp')::text::integer,0))
                               when 0 then 0
                               else (coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'conversions')::text::float,0) + coalesce((Excluded.day_chart::json->0->'conversions')::text::float,0))/(coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'imp')::text::float,0) + coalesce((Excluded.day_chart::json->0->'imp')::text::float,0)) end,
                        'cpc', case (coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'clicks')::text::integer,0) + coalesce((Excluded.day_chart::json->0->'clicks')::text::integer,0))
                               when 0 then 0
                               else (coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'spend')::text::float,0) + coalesce((Excluded.day_chart::json->0->'spend')::text::float,0))/(coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'clicks')::text::float,0) + coalesce((Excluded.day_chart::json->0->'clicks')::text::float,0)) end,
                        'ctr', case coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'imp')::text::integer,0) + coalesce((Excluded.day_chart::json->0->'imp')::text::integer,0)
                               when 0 then 0
                               else (coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'clicks')::text::float,0) + coalesce((Excluded.day_chart::json->0->'clicks')::text::float,0))/(coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'imp')::text::float,0) + coalesce((Excluded.day_chart::json->0->'imp')::text::float,0)) end
                    )::jsonb,
                    true)
                  else ut.day_chart||Excluded.day_chart end;
        """)

def subAdvertisersGraphData(type, start_date, finish_date):
    with connection.cursor() as cursor:
        cursor.execute("""
update ui_usual_advertisers_graph as ut
set
    day_chart = day_chart - 0
FROM (
  select
    distinct advertiser_id
  from
    site_domain_performance_report
  where
    "hour" >= '""" + str(start_date) + """' and "hour" < '""" + str(finish_date) + """'
) info
where ut.advertiser_id = info.advertiser_id and type='""" + str(type) + """';
        """)

def refreshAdvertisersLastMonthGraphData(start_date, finish_date):
    with connection.cursor() as cursor:
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
     "hour" >= '""" + str(start_date) + """'
      and
      "hour" < '""" + str(finish_date) + """'
    group by "day"
    order by "day"
  ))
from (
       select distinct advertiser_id from site_domain_performance_report
        where
         "hour" >= '""" + str(start_date) + """'
          and
          "hour" < '""" + str(finish_date) + """') ads
ON CONFLICT (advertiser_id, type)
  DO UPDATE SET
     day_chart = Excluded.day_chart;
        """)

#
# CAMPAIGNS GRAPH REPORT
#

def cummulateCampaignsGraphData(type, start_date, finish_date):
    with connection.cursor() as cursor:
        cursor.execute("""
insert into ui_usual_placements_graph as ut (
    campaign_id,
    type,
    day_chart)
  select
  camps.campaign_id,
  '""" + str(type) + """',
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
      "hour" > '""" + str(start_date) + """'
    and
      "hour" <= '""" + str(finish_date) + """'
    group by "hour"::timestamp::date
    order by "hour"::timestamp::date
  ))
from (
       select distinct campaign_id from network_analytics_report_by_placement
       where
       "hour" > '""" + str(start_date) + """'
       and
       "hour" <= '""" + str(finish_date) + """') camps
ON CONFLICT (campaign_id, type)
  DO UPDATE SET
     day_chart = case (ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'day')::text when (Excluded.day_chart::json->0->'day')::text
                  then jsonb_set(
                    ut.day_chart::jsonb,
                    concat('{', (jsonb_array_length(ut.day_chart)-1), '}')::text[],
                    json_build_object(
                        'day', ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'day',
                        'impression', coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'impression')::text::integer,0) + coalesce((Excluded.day_chart::json->0->'impression')::text::integer,0),
                        'mediaspent', coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'mediaspent')::text::float,0) + coalesce((Excluded.day_chart::json->0->'mediaspent')::text::float,0),
                        'clicks', coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'clicks')::text::integer,0) + coalesce((Excluded.day_chart::json->0->'clicks')::text::integer,0),
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
        """)

def subCampaignsGraphData(type, start_date, finish_date):
    with connection.cursor() as cursor:
        cursor.execute("""
update ui_usual_placements_graph as ut
set
    day_chart = day_chart - 0
FROM (
  select
    distinct campaign_id
  from
    network_analytics_report_by_placement
  where
    "hour" >= '""" + str(start_date) + """' and "hour" < '""" + str(finish_date) + """'
) info
where ut.campaign_id = info.campaign_id and type='""" + str(type) + """';
        """)

def refreshCampaignsLastMonthGraphData(start_date, finish_date):
    with connection.cursor() as cursor:
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
      "hour" >= '""" + str(start_date) + """'
    and
      "hour" < '""" + str(finish_date) + """'
    group by "hour"::timestamp::date
    order by "hour"::timestamp::date
  ))
from (
       select distinct campaign_id from network_analytics_report_by_placement
       where
       "hour" >= '""" + str(start_date) + """'
       and
       "hour" < '""" + str(finish_date) + """') camps
ON CONFLICT (campaign_id, type)
  DO UPDATE SET
     day_chart = Excluded.day_chart;
        """)


#
# PLACEMENTS GRID TRACKER
#

def cummulatePlacementsGridDataTracker(type, start_date, finish_date):
    with connection.cursor() as cursor:
        cursor.execute("""
insert into ui_usual_placements_grid_data_all_tracker as ut (
    campaign_id,
    placement_id,
    imps,
    spent,
    clicks,
    conversions,
    cpm,
    ctr,
    cpc,
    cvr,
    cpa,
    imps_viewed,
    view_measured_imps,
    view_measurement_rate,
    view_rate)
  select
    "CpId",
    "PlacementId",
    count(id) as imps,
    sum("PricePaid") as spent,
    0,
    0,
    case coalesce(count(id), 0) when 0 then 0 else sum("PricePaid") / count(id) * 1000.0 end,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0
from rtb_impression_tracker
where "Date" > '2017-02-13 00:00:00' and "Date" <= '2017-03-13 04:00:00'
group by "CpId", "PlacementId"
ON CONFLICT (campaign_id, placement_id)
  DO UPDATE SET
    imps = coalesce(ut.imps, 0) + coalesce(Excluded.imps, 0),
    spent = coalesce(ut.spent, 0) + coalesce(Excluded.spent, 0),
    cpm = case (coalesce(ut.imps, 0) + coalesce(Excluded.imps, 0)) when 0 then 0 else (coalesce(ut.spent, 0) + coalesce(Excluded.spent, 0)) / (coalesce(ut.imps, 0) + coalesce(Excluded.imps, 0)) * 1000.0 end,
    ctr = case (coalesce(ut.imps, 0) + coalesce(Excluded.imps, 0)) when 0 then 0 else ut.clicks ::float / coalesce(ut.imps, 0) + coalesce(Excluded.imps, 0) end,
    cpc = case ut.clicks when 0 then 0 else (coalesce(ut.spent, 0) + coalesce(Excluded.spent, 0)) / ut.clicks end,
    cvr = case (coalesce(ut.imps, 0) + coalesce(Excluded.imps, 0)) when 0 then 0 else ut.conversions::float / (coalesce(ut.imps, 0) + coalesce(Excluded.imps, 0)) end,
    cpa = case ut.conversions + Excluded.conversions when 0 then 0 else (coalesce(ut.spent, 0) + coalesce(Excluded.spent, 0)) / ut.conversions end;
       """)

        cursor.execute("""
insert into ui_usual_placements_grid_data_""" + str(type) + """_tracker as ut (
    campaign_id,
    placement_id,
    imps,
    spent,
    clicks,
    conversions,
    cpm,
    ctr,
    cpc,
    cvr,
    cpa,
    imps_viewed,
    view_measured_imps,
    view_measurement_rate,
    view_rate)
  select
    rtb_impression_tracker."CpId",
    rtb_impression_tracker."PlacementId",
    0 as imps,
    0 as spent,
    count(rtb_click_tracker.id) as clicks,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0
from rtb_click_tracker
left join rtb_impression_tracker
  on rtb_impression_tracker."AuctionId" = rtb_click_tracker."AuctionId"
where rtb_click_tracker."Date" > '""" + str(start_date) + """' and rtb_click_tracker."Date" <= '""" + str(finish_date) + """'
group by rtb_impression_tracker."CpId", rtb_impression_tracker."PlacementId"
ON CONFLICT (campaign_id, placement_id)
  DO UPDATE SET
    clicks = coalesce(ut.clicks, 0) + coalesce(Excluded.clicks, 0),
    ctr = case coalesce(ut.imps, 0) when 0 then 0 else (ut.clicks + Excluded.clicks)::float / ut.imps end,
    cpc = case (ut.clicks + Excluded.clicks) when 0 then 0 else ut.spent / (ut.clicks + Excluded.clicks) end;
                """)

        cursor.execute("""
insert into ui_usual_placements_grid_data_""" + str(type) + """_tracker as ut (
    campaign_id,
    placement_id,
    imps,
    spent,
    clicks,
    conversions,
    cpm,
    ctr,
    cpc,
    cvr,
    cpa,
    imps_viewed,
    view_measured_imps,
    view_measurement_rate,
    view_rate)
  select
    rtb_impression_tracker."CpId",
    rtb_impression_tracker."PlacementId",
    0,
    0,
    0,
    count(rtb_conversion_tracker.id) as conversions,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0
from rtb_click_tracker
left join rtb_conversion_tracker
  on rtb_impression_tracker."AuctionId" = rtb_conversion_tracker."AuctionId"
where rtb_conversion_tracker."Date" > '""" + str(start_date) + """' and rtb_conversion_tracker."Date" <= '""" + str(finish_date) + """'
group by rtb_impression_tracker."CpId",rtb_impression_tracker."PlacementId"
ON CONFLICT (campaign_id, placement_id)
  DO UPDATE SET
    conversions = ut.conversions + Excluded.conversions,
    cvr = case coalesce(ut.imps, 0) when 0 then 0 else coalesce((ut.conversions + Excluded.conversions),0)::float / ut.imps end,
    cpa = case coalesce((ut.conversions + Excluded.conversions),0) when 0 then 0 else coalesce(ut.spent, 0) / (ut.conversions + Excluded.conversions) end;
                """)

def subPlacementsGridDataTracker(type, start_date, finish_date):
    with connection.cursor() as cursor:
        cursor.execute("""
update ui_usual_placements_grid_data_""" + str(type) + """_tracker as ut
set
  imps = ut.imps - info.imp,
  clicks = ut.clicks - info.clicks,
  spent = ut.spent - info.spent,
  conversions = ut.conversions - info.conversions,
  imps_viewed = ut.imps_viewed - info.imps_viewed,
  view_measured_imps = ut.view_measured_imps - info.view_measured_imps,
  cpm = case (ut.imps - info.imp) when 0 then 0 else (ut.spent - info.spent) / (ut.imps - info.imp) * 1000.0 end,
  cvr = case (ut.imps - info.imp) when 0 then 0 else (ut.conversions - info.conversions) / (ut.imps - info.imp) end,
  ctr = case (ut.imps - info.imp) when 0 then 0 else (ut.clicks - info.clicks) / (ut.imps - info.imp) end,
  cpc = case (ut.clicks - info.clicks) when 0 then 0 else (ut.spent - info.spent) / (ut.clicks - info.clicks) end,
  cpa = case (ut.conversions - info.conversions) when 0 then 0 else (ut.spent - info.spent) / (ut.conversions - info.conversions) end,
  view_measurement_rate = case (imps - info.imp) when 0 then 0 else (ut.view_measured_imps - info.view_measured_imps) / (ut.imps - info.imp) end,
  view_rate = case (ut.view_measured_imps - info.view_measured_imps) when 0 then 0 else (ut.imps_viewed - info.imps_viewed) / (ut.view_measured_imps - info.view_measured_imps) end
FROM (
  select
  t."CpId",
  t."PlacementId",
  count(t."id") as imp,
  count(clicktable.id) as clicks,
  sum(t."PricePaid") as spent,
  count(conversiontable.id) as conversions,
  0 as imps_viewed,
  0 as view_measured_imps
from
  rtb_impression_tracker t
  LEFT JOIN rtb_click_tracker clicktable ON clicktable."AuctionId" = t."AuctionId"
  LEFT JOIN rtb_conversion_tracker conversiontable ON conversiontable."AuctionId" = t."AuctionId"
where
  t."Date" >= '""" + str(start_date) + """'
  and t."Date" < '""" + str(finish_date) + """'
group by
  t."CpId", t."PlacementId"
) info
where ut.campaign_id = info."CpId" and ut.placement_id = info."PlacementId";
        """)

def refreshPlacementsLastMonthGridDataTracker(start_date, finish_date):
    with connection.cursor() as cursor:
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
  t."Date" >= '""" + str(start_date) + """'
  and t."Date" < '""" + str(finish_date) + """'
group by
  t."CpId", t."PlacementId"
    ON CONFLICT (campaign_id, placement_id)
      DO UPDATE SET
         imps = coalesce(Excluded.imps, 0),
         clicks = coalesce(Excluded.clicks, 0),
         spent = coalesce(Excluded.spent, 0),
         conversions = coalesce(Excluded.conversions, 0),
         imps_viewed = coalesce(Excluded.imps_viewed, 0),
         view_measured_imps = coalesce(Excluded.view_measured_imps, 0),
         cpm = coalesce(Excluded.cpm, 0),
         cvr = coalesce(Excluded.cvr, 0),
         ctr = coalesce(Excluded.ctr, 0),
         cpc = coalesce(Excluded.cpc, 0),
         cpa = coalesce(Excluded.cpa, 0),
         view_measurement_rate = coalesce(Excluded.view_measurement_rate, 0),
         view_rate = coalesce(Excluded.view_rate, 0);
        """)


#
# CAMPAIGNS GRID TRACKER
#

def cummulateCampaignsGridDataTracker(type, start_date, finish_date):
    with connection.cursor() as cursor:
        cursor.execute("""
insert into ui_usual_campaigns_grid_data_""" + str(type) + """_tracker as ut (
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
         site_r."Date" > '""" + str(start_date) + """'
         and site_r."Date" <= '""" + str(finish_date) + """')
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
        t."Date" > '""" + str(start_date) + """'
        and t."Date" <= '""" + str(finish_date) + """'
      group by t."CpId"
     ) page
ON CONFLICT (campaign_id)
  DO UPDATE SET
     imps = coalesce(ut.imps, 0) + coalesce(Excluded.imps, 0),
     clicks = coalesce(ut.clicks, 0) + coalesce(Excluded.clicks, 0),
     spent = coalesce(ut.spent, 0) + coalesce(Excluded.spent, 0),
     conversions = coalesce(ut.conversions, 0) + coalesce(Excluded.conversions, 0),
     imps_viewed = coalesce(ut.imps_viewed, 0) + coalesce(Excluded.imps_viewed, 0),
     view_measured_imps = coalesce(ut.view_measured_imps, 0) + coalesce(Excluded.view_measured_imps, 0),
     cpm = case (coalesce(ut.imps, 0) + coalesce(Excluded.imps, 0)) when 0 then 0 else (coalesce(ut.spent, 0) + coalesce(Excluded.spent, 0)) / (coalesce(ut.imps, 0) + coalesce(Excluded.imps, 0)) * 1000.0 end,
     cvr = case (coalesce(ut.imps, 0) + coalesce(Excluded.imps, 0)) when 0 then 0 else (coalesce(ut.conversions, 0) + coalesce(Excluded.conversions, 0))::float / (coalesce(ut.imps, 0) + coalesce(Excluded.imps, 0)) end,
     ctr = case (coalesce(ut.imps, 0) + coalesce(Excluded.imps, 0)) when 0 then 0 else (coalesce(ut.clicks, 0) + coalesce(Excluded.clicks, 0))::float / (coalesce(ut.imps, 0) + coalesce(Excluded.imps, 0)) end,
     cpc = case (coalesce(ut.clicks, 0) + coalesce(Excluded.clicks, 0)) when 0 then 0 else (coalesce(ut.spent, 0) + coalesce(Excluded.spent, 0)) / (coalesce(ut.clicks, 0) + coalesce(Excluded.clicks, 0)) end,
     view_measurement_rate = case (coalesce(ut.imps, 0) + coalesce(Excluded.imps, 0)) when 0 then 0 else (coalesce(ut.view_measured_imps, 0) + coalesce(Excluded.view_measured_imps, 0))::float / (coalesce(ut.imps, 0) + coalesce(Excluded.imps, 0)) end,
     view_rate = case (coalesce(ut.view_measured_imps, 0) + coalesce(Excluded.view_measured_imps, 0)) when 0 then 0 else (coalesce(ut.imps_viewed, 0) + coalesce(Excluded.imps_viewed, 0))::float / (coalesce(ut.view_measured_imps, 0) + coalesce(Excluded.view_measured_imps, 0)) end,
     day_chart = case (ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'day')::text when (Excluded.day_chart::json->0->'day')::text
                  then jsonb_set(
                    ut.day_chart::jsonb,
                    concat('{', (jsonb_array_length(ut.day_chart)-1), '}')::text[],
                    json_build_object(
                        'day', ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'day',
                        'imp', coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'imp')::text::integer,0) + coalesce((Excluded.day_chart::json->0->'imp')::text::integer,0),
                        'spend', coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'spend')::text::float,0) + coalesce((Excluded.day_chart::json->0->'spend')::text::float,0),
                        'clicks', coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'clicks')::text::integer,0) + coalesce((Excluded.day_chart::json->0->'clicks')::text::integer,0),
                        'conversions', coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'conversions')::text::integer,0) + coalesce((Excluded.day_chart::json->0->'conversions')::text::integer,0),
                        'cvr', case (coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'imp')::text::integer,0) + coalesce((Excluded.day_chart::json->0->'imp')::text::integer,0))
                               when 0 then 0
                               else (coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'conversions')::text::float,0) + coalesce((Excluded.day_chart::json->0->'conversions')::text::float,0))/(coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'imp')::text::float,0) + coalesce((Excluded.day_chart::json->0->'imp')::text::float,0)) end,
                        'cpc', case (coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'clicks')::text::integer,0) + coalesce((Excluded.day_chart::json->0->'clicks')::text::integer,0))
                               when 0 then 0
                               else (coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'spend')::text::float,0) + coalesce((Excluded.day_chart::json->0->'spend')::text::float,0))/(coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'clicks')::text::float,0) + coalesce((Excluded.day_chart::json->0->'clicks')::text::float,0)) end,
                        'ctr', case coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'imp')::text::integer,0) + coalesce((Excluded.day_chart::json->0->'imp')::text::integer,0)
                               when 0 then 0
                               else (coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'clicks')::text::float,0) + coalesce((Excluded.day_chart::json->0->'clicks')::text::float,0))/(coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'imp')::text::float,0) + coalesce((Excluded.day_chart::json->0->'imp')::text::float,0)) end
                    )::jsonb,
                    true)
                  else ut.day_chart||Excluded.day_chart end;
        """)


def subCampaignsGridDataTracker(type, start_date, finish_date):
    with connection.cursor() as cursor:
        cursor.execute("""
update ui_usual_campaigns_grid_data_""" + str(type) + """_tracker as ut
set
  imps = ut.imps - info.imp,
  clicks = ut.clicks - info.clicks,
  spent = ut.spent - info.spent,
  conversions = ut.conversions - info.conversions,
  imps_viewed = ut.imps_viewed - info.imps_viewed,
  view_measured_imps = ut.view_measured_imps - info.view_measured_imps,
  cpm = case (ut.imps - info.imp) when 0 then 0 else (ut.spent - info.spent) / (ut.imps - info.imp) * 1000.0 end,
  cvr = case (ut.imps - info.imp) when 0 then 0 else (ut.conversions - info.conversions) / (ut.imps - info.imp) end,
  ctr = case (ut.imps - info.imp) when 0 then 0 else (ut.clicks - info.clicks) / (ut.imps - info.imp) end,
  cpc = case (ut.clicks - info.clicks) when 0 then 0 else (ut.spent - info.spent) / (ut.clicks - info.clicks) end,
  view_measurement_rate = case (imps - info.imp) when 0 then 0 else (ut.view_measured_imps - info.view_measured_imps) / (ut.imps - info.imp) end,
  view_rate = case (ut.view_measured_imps - info.view_measured_imps) when 0 then 0 else (ut.imps_viewed - info.imps_viewed) / (ut.view_measured_imps - info.view_measured_imps) end,
  day_chart = day_chart - 0
FROM (
  select
    t."CpId",
    count(clicktable.id) as clicks,
    count(conversiontable.id) as conversions,
    count(t."id") as imp,
    sum(t."PricePaid") as spent,
    0 as imps_viewed,
    0 as view_measured_imps,
  from
    rtb_impression_tracker t
    LEFT JOIN rtb_click_tracker clicktable ON clicktable."AuctionId" = t."AuctionId"
    LEFT JOIN rtb_conversion_tracker conversiontable ON conversiontable."AuctionId" = t."AuctionId"
  where
    t."Date" >= '""" + str(start_date) + """'
    and t."Date" < '""" + str(finish_date) + """'
  group by t."CpId"
) info
where ut.campaign_id = info."CpId";
        """)


def refreshCampaignsLastMonthGridDataTracker(start_date, finish_date):
    with connection.cursor() as cursor:
        cursor.execute("""
insert into ui_usual_campaigns_grid_data_""" + str(type) + """ as ut (
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
         site_r."Date" >= '""" + str(start_date) + """'
         and site_r."Date" < '""" + str(finish_date) + """')
       group by site_r."Date"::timestamp::date
       order by site_r."Date"::timestamp::date))) day_chart
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
        t."Date" >= '""" + str(start_date) + """'
        and t."Date" < '""" + str(finish_date) + """'
      group by t."CpId"
     ) page
ON CONFLICT (campaign_id)
  DO UPDATE SET
     imps = coalesce(Excluded.imps, 0),
     clicks = coalesce(Excluded.clicks, 0),
     spent = coalesce(Excluded.spent, 0),
     conversions = coalesce(Excluded.conversions, 0),
     imps_viewed = coalesce(Excluded.imps_viewed, 0),
     view_measured_imps = coalesce(Excluded.view_measured_imps, 0),
     cpm = coalesce(Excluded.cpm, 0),
     cvr = coalesce(Excluded.cvr, 0),
     ctr = coalesce(Excluded.ctr, 0),
     cpc = coalesce(Excluded.cpc, 0),
     view_measurement_rate = coalesce(Excluded.view_measurement_rate, 0),
     view_rate = coalesce(Excluded.view_rate, 0),
     day_chart = Excluded.day_chart;
        """)


#
# ADVERTISERS GRAPH TRACKER
#

def cummulateAdvertisersGraphDataTracker(type, start_date, finish_date):
    with connection.cursor() as cursor:
        cursor.execute("""
insert into ui_usual_advertisers_graph_tracker as ut (
    advertiser_id,
    type,
    day_chart)
  select
  page."AdvId",
  '""" + str(type) + """',
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
         site_r."Date" > '""" + str(start_date) + """'
         and site_r."Date" <= '""" + str(finish_date) + """')
       group by site_r."Date"::timestamp::date
       order by site_r."Date"::timestamp::date))) id
from (
      select
        distinct "AdvId"
      from
        rtb_impression_tracker
      where
        "Date" > '""" + str(start_date) + """'
        and "Date" <= '""" + str(finish_date) + """'
     ) page
ON CONFLICT (advertiser_id, type)
  DO UPDATE SET
     day_chart = case (ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'day')::text when (Excluded.day_chart::json->0->'day')::text
                  then jsonb_set(
                    ut.day_chart::jsonb,
                    concat('{', (jsonb_array_length(ut.day_chart)-1), '}')::text[],
                    json_build_object(
                        'day', ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'day',
                        'imp', coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'imp')::text::integer,0) + coalesce((Excluded.day_chart::json->0->'imp')::text::integer,0),
                        'spend', coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'spend')::text::float,0) + coalesce((Excluded.day_chart::json->0->'spend')::text::float,0),
                        'clicks', coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'clicks')::text::integer,0) + coalesce((Excluded.day_chart::json->0->'clicks')::text::integer,0),
                        'conversions', coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'conversions')::text::integer,0) + coalesce((Excluded.day_chart::json->0->'conversions')::text::integer,0),
                        'cvr', case (coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'imp')::text::integer,0) + coalesce((Excluded.day_chart::json->0->'imp')::text::integer,0))
                               when 0 then 0
                               else (coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'conversions')::text::float,0) + coalesce((Excluded.day_chart::json->0->'conversions')::text::float,0))/(coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'imp')::text::float,0) + coalesce((Excluded.day_chart::json->0->'imp')::text::float,0)) end,
                        'cpc', case (coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'clicks')::text::integer,0) + coalesce((Excluded.day_chart::json->0->'clicks')::text::integer,0))
                               when 0 then 0
                               else (coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'spend')::text::float,0) + coalesce((Excluded.day_chart::json->0->'spend')::text::float,0))/(coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'clicks')::text::float,0) + coalesce((Excluded.day_chart::json->0->'clicks')::text::float,0)) end,
                        'ctr', case coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'imp')::text::integer,0) + coalesce((Excluded.day_chart::json->0->'imp')::text::integer,0)
                               when 0 then 0
                               else (coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'clicks')::text::float,0) + coalesce((Excluded.day_chart::json->0->'clicks')::text::float,0))/(coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'imp')::text::float,0) + coalesce((Excluded.day_chart::json->0->'imp')::text::float,0)) end
                    )::jsonb,
                    true)
                  else ut.day_chart||Excluded.day_chart end;
        """)


def subAdvertisersGraphDataTracker(type, start_date, finish_date):
    with connection.cursor() as cursor:
        cursor.execute("""
update ui_usual_advertisers_graph_tracker as ut
set
    day_chart = day_chart - 0
FROM (
 select
        distinct "AdvId"
      from
        rtb_impression_tracker
      where
        "Date" >= '""" + str(start_date) + """'
        and "Date" < '""" + str(finish_date) + """'
) info
where ut.advertiser_id = info."AdvId" and type='""" + str(type) + """';
        """)


def refreshAdvertisersLastMonthGraphDataTracker(start_date, finish_date):
    with connection.cursor() as cursor:
        cursor.execute("""
insert into ui_usual_advertisers_graph_tracker as ut (
    advertiser_id,
    type,
    day_chart)
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
         site_r."Date" >= """ + str(start_date) + """
         and site_r."Date" < """ + str(finish_date) + """)
       group by site_r."Date"::timestamp::date
       order by site_r."Date"::timestamp::date))) id
from (
      select
        distinct "AdvId"
      from
        rtb_impression_tracker
      where
        "Date" >= """ + str(start_date) + """
        and "Date" < """ + str(finish_date) + """
     ) page
ON CONFLICT (advertiser_id, type)
  DO UPDATE SET
     day_chart = Excluded.day_chart;
        """)


#
# CAMPAIGNS GRAPH TRACKER
#

def cummulateCampaignsGraphDataTracker(type, start_date, finish_date):
    with connection.cursor() as cursor:
        cursor.execute("""
insert into ui_usual_campaigns_graph_tracker as ut (
    campaign_id,
    type,
    day_chart)
  select
      page."CpId",
      '""" + str(type) + """',
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
             site_r."Date" > '""" + str(start_date) + """'
             and site_r."Date" <= '""" + str(finish_date) + """')
           group by site_r."Date"::timestamp::date
           order by site_r."Date"::timestamp::date))) id
    from (
          select
            distinct "CpId"
          from
            rtb_impression_tracker
          where
            "Date" > '""" + str(start_date) + """'
            and "Date" <= '""" + str(finish_date) + """'
         ) page
ON CONFLICT (campaign_id, type)
  DO UPDATE SET
     day_chart = case (ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'day')::text when (Excluded.day_chart::json->0->'day')::text
                  then jsonb_set(
                    ut.day_chart::jsonb,
                    concat('{', (jsonb_array_length(ut.day_chart)-1), '}')::text[],
                    json_build_object(
                        'day', ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'day',
                        'impression', coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'impression')::text::integer,0) + coalesce((Excluded.day_chart::json->0->'impression')::text::integer,0),
                        'mediaspent', coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'mediaspent')::text::float,0) + coalesce((Excluded.day_chart::json->0->'mediaspent')::text::float,0),
                        'clicks', coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'clicks')::text::integer,0) + coalesce((Excluded.day_chart::json->0->'clicks')::text::integer,0),
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
        """)


def subCampaignsGraphDataTracker(type, start_date, finish_date):
    with connection.cursor() as cursor:
        cursor.execute("""
update ui_usual_campaigns_graph_tracker as ut
set
    day_chart = day_chart - 0
FROM (
  select
        distinct "CpId"
      from
        rtb_impression_tracker
      where
        "Date" >= '""" + str(start_date) + """'
        and "Date" <= '""" + str(finish_date) + """'
) info
where ut.campaign_id = info."CpId" and type='""" + str(type) + """';
        """)


def refreshCampaignsLastMonthGraphDataTracker(start_date, finish_date):
    with connection.cursor() as cursor:
        cursor.execute("""
insert into ui_usual_placements_graph as ut (
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
             site_r."Date" >= '""" + str(start_date) + """'
             and site_r."Date" < '""" + str(finish_date) + """')
           group by site_r."Date"::timestamp::date
           order by site_r."Date"::timestamp::date)))
    from (
          select
            distinct "CpId"
          from
            rtb_impression_tracker
          where
            "Date" >= '""" + str(start_date) + """'
            and "Date" < '""" + str(finish_date) + """'
         ) page
ON CONFLICT (campaign_id, type)
  DO UPDATE SET
     day_chart = Excluded.day_chart;
        """)

def refreshPrecalculatedDataPlacements(start_date, finish_date):
    print "Refreshing placements names"
    with connection.cursor() as cursor:
        cursor.execute("""
insert into placements_additional_names as ut (
    placement_id,
    publisher_name,
    seller_member_name)
  select
    distinct on (t.placement_id)
    t.placement_id,
    t.publisher_name,
    t.seller_member_name
  from
    network_analytics_report_by_placement t
  where
    t."hour" > '""" + str(start_date) + """' and t."hour" <= '""" + str(finish_date) + """'
ON CONFLICT (placement_id)
  DO UPDATE SET
    publisher_name=Excluded.publisher_name,
    seller_member_name=Excluded.seller_member_name;
        """)
    print "Refreshing placements precalculated data from " + str(start_date) + " to " + str(finish_date) + " started: " + str(datetime.now())
    finish_date = datetime(hour=finish_date.hour, day=finish_date.day, month=finish_date.month, year=finish_date.year)
    start_date = datetime(hour=start_date.hour, day=start_date.day, month=start_date.month, year=start_date.year)
    tableTypes = [
        ["yesterday", 1],
        ["last_3_days", 3],
        ["last_7_days", 7],
        ["last_14_days", 14],
        ["last_21_days", 21],
        ["last_90_days", 90]
    ]
    LastModified.objects.filter(type='hourlyTask').update(
        date=timezone.make_aware(datetime.now(), timezone.get_default_timezone()))

    # refreshing placements grid
    cummulatePlacementsGridData(type="all", start_date=start_date, finish_date=finish_date)
    LastModified.objects.filter(type='hourlyTask').update(
        date=timezone.make_aware(datetime.now(), timezone.get_default_timezone()))
    print "Refreshing all time placements grid data finished: " + str(datetime.now())
    cummulatePlacementsGridData(type="cur_month", start_date=start_date, finish_date=finish_date)
    LastModified.objects.filter(type='hourlyTask').update(
        date=timezone.make_aware(datetime.now(), timezone.get_default_timezone()))
    print "Refreshing current month placements grid data finished: " + str(datetime.now())

    # refreshing campaigns graph
    cummulateCampaignsGraphData(type="all", start_date=start_date, finish_date=finish_date)
    LastModified.objects.filter(type='hourlyTask').update(
        date=timezone.make_aware(datetime.now(), timezone.get_default_timezone()))
    print "Refreshing all time campaigns graph data finished: " + str(datetime.now())
    cummulateCampaignsGraphData(type="cur_month", start_date=start_date, finish_date=finish_date)
    LastModified.objects.filter(type='hourlyTask').update(
        date=timezone.make_aware(datetime.now(), timezone.get_default_timezone()))
    print "Refreshing current month campaigns graph data finished: " + str(datetime.now())

    for type in tableTypes:
        # refreshing placements grid
        LastModified.objects.filter(type='hourlyTask').update(
            date=timezone.make_aware(datetime.now(), timezone.get_default_timezone()))
        # adding data
        cummulatePlacementsGridData(type=type[0], start_date=start_date, finish_date=finish_date)
        LastModified.objects.filter(type='hourlyTask').update(
            date=timezone.make_aware(datetime.now(), timezone.get_default_timezone()))
        # sub data
        if finish_date == finish_date.replace(hour=0, minute=0, second=0, microsecond=0):
            subPlacementsGridData(type=type[0],
                                  start_date=finish_date - timedelta(days=type[1] + 2),
                                  finish_date=finish_date - timedelta(days=type[1] + 1)
                                  )
            LastModified.objects.filter(type='hourlyTask').update(
                date=timezone.make_aware(datetime.now(), timezone.get_default_timezone()))
        print "Refreshing " + str(type[0]) + " placements grid data finished: " + str(datetime.now())

        # refreshing campaigns graph
        LastModified.objects.filter(type='hourlyTask').update(
            date=timezone.make_aware(datetime.now(), timezone.get_default_timezone()))
        # adding data
        cummulateCampaignsGraphData(type=type[0], start_date=start_date, finish_date=finish_date)
        LastModified.objects.filter(type='hourlyTask').update(
            date=timezone.make_aware(datetime.now(), timezone.get_default_timezone()))
        # sub data
        if finish_date == finish_date.replace(hour=0, minute=0, second=0, microsecond=0):
            subCampaignsGraphData(type=type[0],
                                 start_date=finish_date - timedelta(days=type[1] + 2),
                                 finish_date=finish_date - timedelta(days=type[1] + 1)
                                 )
            LastModified.objects.filter(type='hourlyTask').update(
                date=timezone.make_aware(datetime.now(), timezone.get_default_timezone()))
        print "Refreshing " + str(type[0]) + " campaigns graph data finished: " + str(datetime.now())
    # refresh last month
    if finish_date == finish_date.replace(day=1, hour=0, minute=0, second=0, microsecond=0):
        # placements grid refreshing
        LastModified.objects.filter(type='hourlyTask').update(
            date=timezone.make_aware(datetime.now(), timezone.get_default_timezone()))
        with connection.cursor() as cursor:
            cursor.execute("""
            update ui_usual_placements_grid_data_cur_month set
            imps = 0,
            clicks = 0,
            spent = 0,
            conversions = 0,
            imps_viewed = 0,
            view_measured_imps = 0,
            cpm = 0,
            cvr = 0,
            ctr = 0,
            cpc = 0,
            cpa = 0,
            view_measurement_rate = 0,
            view_rate = 0;""")
            cursor.execute("""
            update ui_usual_placements_grid_data_last_month set
            imps = 0,
            clicks = 0,
            spent = 0,
            conversions = 0,
            imps_viewed = 0,
            view_measured_imps = 0,
            cpm = 0,
            cvr = 0,
            ctr = 0,
            cpc = 0,
            cpa = 0,
            view_measurement_rate = 0,
            view_rate = 0;""")
        refreshPlacementsLastMonthGridData(
            start_date=(finish_date.replace(day=1, hour=0, minute=0, second=0, microsecond=0) - timedelta(hours=1)
                        ).replace(day=1, hour=0, minute=0, second=0, microsecond=0),
            finish_date=finish_date.replace(day=1, hour=0, minute=0, second=0, microsecond=0))
        print "Refreshing last month placements grid data finished: " + str(datetime.now())

        # campaigns graph refreshing
        LastModified.objects.filter(type='hourlyTask').update(
            date=timezone.make_aware(datetime.now(), timezone.get_default_timezone()))
        with connection.cursor() as cursor:
            cursor.execute("""
                            update ui_usual_placements_graph set
                            day_chart=jsonb_build_array()
                            where type='cur_month';""")
            cursor.execute("""
                            update ui_usual_placements_graph set
                            day_chart=jsonb_build_array()
                            where type='last_month';""")
        refreshCampaignsLastMonthGraphData(
            start_date=(finish_date.replace(day=1, hour=0, minute=0, second=0, microsecond=0) - timedelta(hours=1)
                        ).replace(day=1, hour=0, minute=0, second=0, microsecond=0),
            finish_date=finish_date.replace(day=1, hour=0, minute=0, second=0, microsecond=0))
        print "Refreshing last month campaigns graph data finished: " + str(datetime.now())
    LastModified.objects.filter(type='hourlyTask').update(date=timezone.make_aware(datetime.now(), timezone.get_default_timezone()))
    print "Refreshing placements precalculated data from " + str(start_date) + " to " + str(finish_date) + " finished: " + str(datetime.now())

def refreshPrecalculatedDataCampaings(start_date, finish_date):
    print "Refreshing campaigns precalculated data from " + str(start_date) + " to " + str(finish_date) + " started: " + str(
        datetime.now())
    finish_date = datetime(hour=finish_date.hour, day=finish_date.day, month=finish_date.month, year=finish_date.year)
    start_date = datetime(hour=start_date.hour, day=start_date.day, month=start_date.month, year=start_date.year)
    tableTypes = [
        ["yesterday", 1],
        ["last_3_days", 3],
        ["last_7_days", 7],
        ["last_14_days", 14],
        ["last_21_days", 21],
        ["last_90_days", 90]
    ]
    LastModified.objects.filter(type='hourlyTask').update(
        date=timezone.make_aware(datetime.now(), timezone.get_default_timezone()))
    # refreshing campaigns grid
    cummulateCampaignsGridData(type="all", start_date=start_date, finish_date=finish_date)
    LastModified.objects.filter(type='hourlyTask').update(
        date=timezone.make_aware(datetime.now(), timezone.get_default_timezone()))
    print "Refreshing all time campaigns grid data finished: " + str(datetime.now())
    cummulateCampaignsGridData(type="cur_month", start_date=start_date, finish_date=finish_date)
    LastModified.objects.filter(type='hourlyTask').update(
        date=timezone.make_aware(datetime.now(), timezone.get_default_timezone()))
    print "Refreshing current month campaigns grid data finished: " + str(datetime.now())

    # refreshing advertisers graph
    cummulateAdvertisersGraphData(type="all", start_date=start_date, finish_date=finish_date)
    LastModified.objects.filter(type='hourlyTask').update(
        date=timezone.make_aware(datetime.now(), timezone.get_default_timezone()))
    print "Refreshing all time advertisers graph data finished: " + str(datetime.now())
    cummulateAdvertisersGraphData(type="cur_month", start_date=start_date, finish_date=finish_date)
    LastModified.objects.filter(type='hourlyTask').update(
        date=timezone.make_aware(datetime.now(), timezone.get_default_timezone()))
    print "Refreshing current month advertisers graph data finished: " + str(datetime.now())

    for type in tableTypes:
        # refreshing campaigns grid
        LastModified.objects.filter(type='hourlyTask').update(
            date=timezone.make_aware(datetime.now(), timezone.get_default_timezone()))
        # adding data
        cummulateCampaignsGridData(type=type[0], start_date=start_date, finish_date=finish_date)
        LastModified.objects.filter(type='hourlyTask').update(
            date=timezone.make_aware(datetime.now(), timezone.get_default_timezone()))
        # sub data
        if finish_date == finish_date.replace(hour=0, minute=0, second=0, microsecond=0):
            subCampaignsGridData(type=type[0],
                                  start_date=finish_date - timedelta(days=type[1] + 2),
                                  finish_date=finish_date - timedelta(days=type[1] + 1)
                                  )
            LastModified.objects.filter(type='hourlyTask').update(
                date=timezone.make_aware(datetime.now(), timezone.get_default_timezone()))
        print "Refreshing " + str(type[0]) + " campaigns grid data finished: " + str(datetime.now())

        # refreshing advertisers graph
        LastModified.objects.filter(type='hourlyTask').update(
            date=timezone.make_aware(datetime.now(), timezone.get_default_timezone()))
        # adding data
        cummulateAdvertisersGraphData(type=type[0], start_date=start_date, finish_date=finish_date)
        LastModified.objects.filter(type='hourlyTask').update(
            date=timezone.make_aware(datetime.now(), timezone.get_default_timezone()))
        # sub data
        if finish_date == finish_date.replace(hour=0, minute=0, second=0, microsecond=0):
            subAdvertisersGraphData(type=type[0],
                                    start_date=finish_date - timedelta(days=type[1] + 2),
                                    finish_date=finish_date - timedelta(days=type[1] + 1)
                                    )
            LastModified.objects.filter(type='hourlyTask').update(
                date=timezone.make_aware(datetime.now(), timezone.get_default_timezone()))
        print "Refreshing " + str(type[0]) + " advertisers graph data finished: " + str(datetime.now())

    # refresh last month
    if finish_date == finish_date.replace(day=1, hour=0, minute=0, second=0, microsecond=0):
        # campaigns grid refreshing
        LastModified.objects.filter(type='hourlyTask').update(
            date=timezone.make_aware(datetime.now(), timezone.get_default_timezone()))
        with connection.cursor() as cursor:
            cursor.execute("""
                    update ui_usual_campaigns_grid_data_cur_month set
                    imps = 0,
                    clicks = 0,
                    spent = 0,
                    conversions = 0,
                    imps_viewed = 0,
                    view_measured_imps = 0,
                    cpm = 0,
                    cvr = 0,
                    ctr = 0,
                    cpc = 0,
                    view_measurement_rate = 0,
                    view_rate = 0,
                    day_chart=jsonb_build_array();""")
            cursor.execute("""
                    update ui_usual_campaigns_grid_data_last_month set
                    imps = 0,
                    clicks = 0,
                    spent = 0,
                    conversions = 0,
                    imps_viewed = 0,
                    view_measured_imps = 0,
                    cpm = 0,
                    cvr = 0,
                    ctr = 0,
                    cpc = 0,
                    view_measurement_rate = 0,
                    view_rate = 0,
                    day_chart=jsonb_build_array();""")
        refreshCampaignsLastMonthGridData(
            start_date=(finish_date.replace(day=1, hour=0, minute=0, second=0, microsecond=0) - timedelta(hours=1)
                        ).replace(day=1, hour=0, minute=0, second=0, microsecond=0),
            finish_date=finish_date.replace(day=1, hour=0, minute=0, second=0, microsecond=0))
        print "Refreshing last month campaigns grid data finished: " + str(datetime.now())

        # advertisers graph refreshing
        LastModified.objects.filter(type='hourlyTask').update(
            date=timezone.make_aware(datetime.now(), timezone.get_default_timezone()))
        with connection.cursor() as cursor:
            cursor.execute("""
                                    update ui_usual_advertisers_graph set
                                    day_chart=jsonb_build_array()
                                    where type='cur_month';""")
            cursor.execute("""
                                    update ui_usual_advertisers_graph set
                                    day_chart=jsonb_build_array()
                                    where type='last_month';""")
        refreshAdvertisersLastMonthGraphData(
            start_date=(finish_date.replace(day=1, hour=0, minute=0, second=0, microsecond=0) - timedelta(hours=1)
                        ).replace(day=1, hour=0, minute=0, second=0, microsecond=0),
            finish_date=finish_date.replace(day=1, hour=0, minute=0, second=0, microsecond=0))
        print "Refreshing last month advertisers graph data finished: " + str(datetime.now())
    LastModified.objects.filter(type='hourlyTask').update(
        date=timezone.make_aware(datetime.now(), timezone.get_default_timezone()))
    print "Refreshing campaigns precalculated data from " + str(start_date) + " to " + str(finish_date) + " finished: " + str(
        datetime.now())

def refreshPrecalculatedDataTrackerCron():
    change_state = LastModified.objects.filter(type='refreshPrecalculatedDataTrackerCron')
    if len(change_state) >= 1:
        if timezone.make_aware(datetime.now(), timezone.get_default_timezone()) - change_state[0].date >= timedelta(
                minutes=15):
            LastModified.objects.filter(type='refreshPrecalculatedDataTrackerCron').delete()
        else:
            print "refreshPrecalculatedDataTrackerCron is busy, wait..."
            return None
    print "refreshPrecalculatedDataTrackerCron started: " + str(datetime.now())
    LastModified(type='refreshPrecalculatedDataTrackerCron',
                 date=timezone.make_aware(datetime.now(), timezone.get_default_timezone())).save()

    lastRefreshDate = LastModified.objects.filter(type='lastPrecalculatedTrackerCron')[0].date
    now = datetime.now()

    while (lastRefreshDate + timedelta(minutes=5)) <= now:
        with transaction.atomic():
            LastModified.objects.filter(type='refreshPrecalculatedDataTrackerCron').update(
                date=timezone.make_aware(datetime.now(), timezone.get_default_timezone()))
            refreshPrecalculatedDataTracker(start_date=lastRefreshDate, finish_date=lastRefreshDate + timedelta(minutes=5))
            LastModified.objects.filter(
                type='lastPrecalculatedTrackerCron'
            ).update(
                date=timezone.make_aware((lastRefreshDate + timedelta(minutes=5)), timezone.get_default_timezone())
            )
            lastRefreshDate = lastRefreshDate + timedelta(minutes=5)

    LastModified.objects.filter(type='refreshPrecalculatedDataTrackerCron').delete()
    print "refreshPrecalculatedDataTrackerCron finished: " + str(datetime.now())



def refreshPrecalculatedDataTracker(start_date, finish_date):
    print "Refreshing tracker precalculated data from " + str(start_date) + " to " + str(finish_date) + " started: " + str(datetime.now())
    finish_date = datetime(hour=finish_date.hour, day=finish_date.day, month=finish_date.month, year=finish_date.year)
    start_date = datetime(hour=start_date.hour, day=start_date.day, month=start_date.month, year=start_date.year)
    tableTypes = [
        ["yesterday", 1],
        ["last_3_days", 3],
        ["last_7_days", 7],
        ["last_14_days", 14],
        ["last_21_days", 21],
        ["last_90_days", 90]
    ]
    LastModified.objects.filter(type='refreshPrecalculatedDataTrackerCron').update(
        date=timezone.make_aware(datetime.now(), timezone.get_default_timezone()))

    # refreshing campaigns grid
    cummulateCampaignsGridDataTracker(type="all", start_date=start_date, finish_date=finish_date)
    LastModified.objects.filter(type='refreshPrecalculatedDataTrackerCron').update(
        date=timezone.make_aware(datetime.now(), timezone.get_default_timezone()))
    print "Refreshing all time campaigns grid data finished: " + str(datetime.now())
    cummulateCampaignsGridDataTracker(type="cur_month", start_date=start_date, finish_date=finish_date)
    LastModified.objects.filter(type='refreshPrecalculatedDataTrackerCron').update(
        date=timezone.make_aware(datetime.now(), timezone.get_default_timezone()))
    print "Refreshing current month campaigns grid data finished: " + str(datetime.now())

    # refreshing placements grid
    cummulatePlacementsGridDataTracker(type="all", start_date=start_date, finish_date=finish_date)
    LastModified.objects.filter(type='refreshPrecalculatedDataTrackerCron').update(
        date=timezone.make_aware(datetime.now(), timezone.get_default_timezone()))
    print "Refreshing all time placements grid data finished: " + str(datetime.now())
    cummulatePlacementsGridDataTracker(type="cur_month", start_date=start_date, finish_date=finish_date)
    LastModified.objects.filter(type='refreshPrecalculatedDataTrackerCron').update(
        date=timezone.make_aware(datetime.now(), timezone.get_default_timezone()))
    print "Refreshing current month placements grid data finished: " + str(datetime.now())

    # refreshing advertisers graph
    cummulateAdvertisersGraphDataTracker(type="all", start_date=start_date, finish_date=finish_date)
    LastModified.objects.filter(type='refreshPrecalculatedDataTrackerCron').update(
        date=timezone.make_aware(datetime.now(), timezone.get_default_timezone()))
    print "Refreshing all time advertisers graph data finished: " + str(datetime.now())
    cummulateAdvertisersGraphDataTracker(type="cur_month", start_date=start_date, finish_date=finish_date)
    LastModified.objects.filter(type='refreshPrecalculatedDataTrackerCron').update(
        date=timezone.make_aware(datetime.now(), timezone.get_default_timezone()))
    print "Refreshing current month advertisers graph data finished: " + str(datetime.now())

    # refreshing campaigns graph
    cummulateCampaignsGraphDataTracker(type="all", start_date=start_date, finish_date=finish_date)
    LastModified.objects.filter(type='refreshPrecalculatedDataTrackerCron').update(
        date=timezone.make_aware(datetime.now(), timezone.get_default_timezone()))
    print "Refreshing all time campaigns graph data finished: " + str(datetime.now())
    cummulateCampaignsGraphDataTracker(type="cur_month", start_date=start_date, finish_date=finish_date)
    LastModified.objects.filter(type='refreshPrecalculatedDataTrackerCron').update(
        date=timezone.make_aware(datetime.now(), timezone.get_default_timezone()))
    print "Refreshing current month campaigns graph data finished: " + str(datetime.now())

    for type in tableTypes:
        # refreshing campaigns grid
        LastModified.objects.filter(type='refreshPrecalculatedDataTrackerCron').update(
            date=timezone.make_aware(datetime.now(), timezone.get_default_timezone()))
        # adding data
        cummulateCampaignsGridDataTracker(type=type[0], start_date=start_date, finish_date=finish_date)
        LastModified.objects.filter(type='refreshPrecalculatedDataTrackerCron').update(
            date=timezone.make_aware(datetime.now(), timezone.get_default_timezone()))
        # sub data
        if finish_date == finish_date.replace(hour=0, minute=0, second=0, microsecond=0):
            subCampaignsGridDataTracker(type=type[0],
                                  start_date=finish_date - timedelta(days=type[1] + 1),
                                  finish_date=finish_date - timedelta(days=type[1])
                                  )
            LastModified.objects.filter(type='refreshPrecalculatedDataTrackerCron').update(
                date=timezone.make_aware(datetime.now(), timezone.get_default_timezone()))
        print "Refreshing " + str(type[0]) + " campaigns grid data finished: " + str(datetime.now())

        # refreshing placements grid
        LastModified.objects.filter(type='refreshPrecalculatedDataTrackerCron').update(
            date=timezone.make_aware(datetime.now(), timezone.get_default_timezone()))
        # adding data
        cummulatePlacementsGridDataTracker(type=type[0], start_date=start_date, finish_date=finish_date)
        LastModified.objects.filter(type='refreshPrecalculatedDataTrackerCron').update(
            date=timezone.make_aware(datetime.now(), timezone.get_default_timezone()))
        # sub data
        if finish_date == finish_date.replace(hour=0, minute=0, second=0, microsecond=0):
            subPlacementsGridDataTracker(type=type[0],
                                  start_date=finish_date - timedelta(days=type[1]+1),
                                  finish_date=finish_date - timedelta(days=type[1])
                                  )
            LastModified.objects.filter(type='refreshPrecalculatedDataTrackerCron').update(
                date=timezone.make_aware(datetime.now(), timezone.get_default_timezone()))
        print "Refreshing " + str(type[0]) + " placements grid data finished: " + str(datetime.now())

        # refreshing advertisers grid
        LastModified.objects.filter(type='refreshPrecalculatedDataTrackerCron').update(
            date=timezone.make_aware(datetime.now(), timezone.get_default_timezone()))
        # adding data
        cummulateAdvertisersGraphDataTracker(type=type[0], start_date=start_date, finish_date=finish_date)
        LastModified.objects.filter(type='refreshPrecalculatedDataTrackerCron').update(
            date=timezone.make_aware(datetime.now(), timezone.get_default_timezone()))
        # sub data
        if finish_date == finish_date.replace(hour=0, minute=0, second=0, microsecond=0):
            subAdvertisersGraphDataTracker(type=type[0],
                                 start_date=finish_date - timedelta(days=type[1] + 1),
                                 finish_date=finish_date - timedelta(days=type[1])
                                 )
            LastModified.objects.filter(type='refreshPrecalculatedDataTrackerCron').update(
                date=timezone.make_aware(datetime.now(), timezone.get_default_timezone()))
        print "Refreshing " + str(type[0]) + " advertisers graph data finished: " + str(datetime.now())

        # refreshing campaigns grid
        LastModified.objects.filter(type='refreshPrecalculatedDataTrackerCron').update(
            date=timezone.make_aware(datetime.now(), timezone.get_default_timezone()))
        # adding data
        cummulateCampaignsGraphDataTracker(type=type[0], start_date=start_date, finish_date=finish_date)
        LastModified.objects.filter(type='refreshPrecalculatedDataTrackerCron').update(
            date=timezone.make_aware(datetime.now(), timezone.get_default_timezone()))
        # sub data
        if finish_date == finish_date.replace(hour=0, minute=0, second=0, microsecond=0):
            subCampaignsGraphDataTracker(type=type[0],
                                 start_date=finish_date - timedelta(days=type[1] + 1),
                                 finish_date=finish_date - timedelta(days=type[1])
                                 )
            LastModified.objects.filter(type='refreshPrecalculatedDataTrackerCron').update(
                date=timezone.make_aware(datetime.now(), timezone.get_default_timezone()))
        print "Refreshing " + str(type[0]) + " campaigns graph data finished: " + str(datetime.now())
    # refresh last month
    if finish_date == finish_date.replace(day=1, hour=0, minute=0, second=0, microsecond=0):
        # campaigns grid refreshing
        LastModified.objects.filter(type='refreshPrecalculatedDataTrackerCron').update(
            date=timezone.make_aware(datetime.now(), timezone.get_default_timezone()))
        with connection.cursor() as cursor:
            cursor.execute("""
                    update ui_usual_campaigns_grid_data_cur_month_tracker set
                    imps = 0,
                    clicks = 0,
                    spent = 0,
                    conversions = 0,
                    imps_viewed = 0,
                    view_measured_imps = 0,
                    cpm = 0,
                    cvr = 0,
                    ctr = 0,
                    cpc = 0,
                    view_measurement_rate = 0,
                    view_rate = 0,
                    day_chart=jsonb_build_array();""")
            cursor.execute("""
                    update ui_usual_campaigns_grid_data_last_month_tracker set
                    imps = 0,
                    clicks = 0,
                    spent = 0,
                    conversions = 0,
                    imps_viewed = 0,
                    view_measured_imps = 0,
                    cpm = 0,
                    cvr = 0,
                    ctr = 0,
                    cpc = 0,
                    view_measurement_rate = 0,
                    view_rate = 0,
                    day_chart=jsonb_build_array();""")
        refreshCampaignsLastMonthGridDataTracker(
            start_date=(finish_date.replace(day=1, hour=0, minute=0, second=0, microsecond=0) - timedelta(hours=1)
                        ).replace(day=1, hour=0, minute=0, second=0, microsecond=0),
            finish_date=finish_date.replace(day=1, hour=0, minute=0, second=0, microsecond=0))
        print "Refreshing last month campaigns grid data finished: " + str(datetime.now())

        # placements grid refreshing
        LastModified.objects.filter(type='refreshPrecalculatedDataTrackerCron').update(
            date=timezone.make_aware(datetime.now(), timezone.get_default_timezone()))
        with connection.cursor() as cursor:
            cursor.execute("""
            update ui_usual_placements_grid_data_cur_month_tracker set
            imps = 0,
            clicks = 0,
            spent = 0,
            conversions = 0,
            imps_viewed = 0,
            view_measured_imps = 0,
            cpm = 0,
            cvr = 0,
            ctr = 0,
            cpc = 0,
            cpa = 0,
            view_measurement_rate = 0,
            view_rate = 0;""")
            cursor.execute("""
            update ui_usual_placements_grid_data_last_month_tracker set
            imps = 0,
            clicks = 0,
            spent = 0,
            conversions = 0,
            imps_viewed = 0,
            view_measured_imps = 0,
            cpm = 0,
            cvr = 0,
            ctr = 0,
            cpc = 0,
            cpa = 0,
            view_measurement_rate = 0,
            view_rate = 0;""")
        refreshPlacementsLastMonthGridDataTracker(
            start_date=(finish_date.replace(day=1, hour=0, minute=0, second=0, microsecond=0) - timedelta(hours=1)
                        ).replace(day=1, hour=0, minute=0, second=0, microsecond=0),
            finish_date=finish_date.replace(day=1, hour=0, minute=0, second=0, microsecond=0))
        print "Refreshing last month placements grid data finished: " + str(datetime.now())

        # advertisers graph refreshing
        LastModified.objects.filter(type='refreshPrecalculatedDataTrackerCron').update(
            date=timezone.make_aware(datetime.now(), timezone.get_default_timezone()))
        with connection.cursor() as cursor:
            cursor.execute("""
                            update ui_usual_advertisers_graph_tracker set
                            day_chart=jsonb_build_array()
                            where type='cur_month';""")
            cursor.execute("""
                            update ui_usual_advertisers_graph_tracker set
                            day_chart=jsonb_build_array()
                            where type='last_month';""")
        refreshAdvertisersLastMonthGraphDataTracker(
            start_date=(finish_date.replace(day=1, hour=0, minute=0, second=0, microsecond=0) - timedelta(hours=1)
                        ).replace(day=1, hour=0, minute=0, second=0, microsecond=0),
            finish_date=finish_date.replace(day=1, hour=0, minute=0, second=0, microsecond=0))
        print "Refreshing last month advertisers graph data finished: " + str(datetime.now())

        # campaigns graph refreshing
        LastModified.objects.filter(type='refreshPrecalculatedDataTrackerCron').update(
            date=timezone.make_aware(datetime.now(), timezone.get_default_timezone()))
        with connection.cursor() as cursor:
            cursor.execute("""
                            update ui_usual_campaigns_graph_tracker set
                            day_chart=jsonb_build_array()
                            where type='cur_month';""")
            cursor.execute("""
                            update ui_usual_campaigns_graph_tracker set
                            day_chart=jsonb_build_array()
                            where type='last_month';""")
        refreshCampaignsLastMonthGraphDataTracker(
            start_date=(finish_date.replace(day=1, hour=0, minute=0, second=0, microsecond=0) - timedelta(hours=1)
                        ).replace(day=1, hour=0, minute=0, second=0, microsecond=0),
            finish_date=finish_date.replace(day=1, hour=0, minute=0, second=0, microsecond=0))
        print "Refreshing last month campaigns graph data finished: " + str(datetime.now())
    LastModified.objects.filter(type='refreshPrecalculatedDataTrackerCron').update(date=timezone.make_aware(datetime.now(), timezone.get_default_timezone()))
    print "Refreshing tracker precalculated from " + str(start_date) + " to " + str(finish_date) + " finished: " + str(datetime.now())