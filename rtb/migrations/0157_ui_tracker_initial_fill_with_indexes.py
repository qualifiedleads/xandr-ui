from __future__ import unicode_literals

import django.contrib.postgres.fields.jsonb
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('rtb', '0156_imptracker_index_cpid_placementid'),
    ]

    operations = [
        migrations.RunSQL(""" delete from last_modified where type='lastPrecalculatedTrackerCron';
insert into last_modified (type, date) values ('lastPrecalculatedTrackerCron', (select date_trunc('hour', max("Date")) from rtb_impression_tracker));"""),
        ##
        #PLACEMENTS GRID
        ##

        # all
        migrations.RunSQL("delete from ui_usual_placements_grid_data_all_tracker;"),

        migrations.RunSQL("""
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
  where "Date" <= (select date from last_modified where type='lastPrecalculatedTrackerCron')
  group by "CpId", "PlacementId";
        """),

        migrations.RunSQL("""
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
  where rtb_click_tracker."Date" <= (select date from last_modified where type='lastPrecalculatedTrackerCron')
  group by rtb_impression_tracker."CpId", rtb_impression_tracker."PlacementId"
ON CONFLICT (campaign_id, placement_id)
  DO UPDATE SET
    clicks = coalesce(ut.clicks, 0) + coalesce(Excluded.clicks, 0),
    ctr = case coalesce(ut.imps, 0) when 0 then 0 else (ut.clicks + Excluded.clicks)::float / ut.imps end,
    cpc = case (ut.clicks + Excluded.clicks) when 0 then 0 else ut.spent / (ut.clicks + Excluded.clicks) end;
            """),

        migrations.RunSQL("""
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
  from rtb_conversion_tracker
  left join rtb_impression_tracker
  on rtb_conversion_tracker."AuctionId" = rtb_impression_tracker."AuctionId"
  where rtb_conversion_tracker."Date" <= (select date from last_modified where type='lastPrecalculatedTrackerCron')
group by rtb_impression_tracker."CpId",rtb_impression_tracker."PlacementId"
ON CONFLICT (campaign_id, placement_id)
  DO UPDATE SET
    conversions = ut.conversions + Excluded.conversions,
    cvr = case coalesce(ut.imps, 0) when 0 then 0 else coalesce((ut.conversions + Excluded.conversions),0)::float / ut.imps end,
    cpa = case coalesce((ut.conversions + Excluded.conversions),0) when 0 then 0 else coalesce(ut.spent, 0) / (ut.conversions + Excluded.conversions) end;
            """),

        # yesterday

        migrations.RunSQL("delete from ui_usual_placements_grid_data_yesterday_tracker;"),

        migrations.RunSQL("""
                insert into ui_usual_placements_grid_data_yesterday_tracker as ut (
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
          where
          "Date" >= date_trunc('day',(select date from last_modified where type='lastPrecalculatedTrackerCron') - interval '1 day')
          and
          "Date" <= (select date from last_modified where type='lastPrecalculatedTrackerCron')
          group by "CpId", "PlacementId";
                """),

        migrations.RunSQL("""
        insert into ui_usual_placements_grid_data_yesterday_tracker as ut (
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
          where
          rtb_click_tracker."Date" >= date_trunc('day',(select date from last_modified where type='lastPrecalculatedTrackerCron') - interval '1 day')
          and
          rtb_click_tracker."Date" <= (select date from last_modified where type='lastPrecalculatedTrackerCron')
          group by rtb_impression_tracker."CpId", rtb_impression_tracker."PlacementId"
        ON CONFLICT (campaign_id, placement_id)
          DO UPDATE SET
            clicks = coalesce(ut.clicks, 0) + coalesce(Excluded.clicks, 0),
            ctr = case coalesce(ut.imps, 0) when 0 then 0 else (ut.clicks + Excluded.clicks)::float / ut.imps end,
            cpc = case (ut.clicks + Excluded.clicks) when 0 then 0 else ut.spent / (ut.clicks + Excluded.clicks) end;
                    """),

        migrations.RunSQL("""
        insert into ui_usual_placements_grid_data_yesterday_tracker as ut (
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
          from rtb_conversion_tracker
          left join rtb_impression_tracker
          on rtb_conversion_tracker."AuctionId" = rtb_impression_tracker."AuctionId"
          where
          rtb_conversion_tracker."Date" >= date_trunc('day',(select date from last_modified where type='lastPrecalculatedTrackerCron') - interval '1 day')
          and
          rtb_conversion_tracker."Date" <= (select date from last_modified where type='lastPrecalculatedTrackerCron')
        group by rtb_impression_tracker."CpId",rtb_impression_tracker."PlacementId"
        ON CONFLICT (campaign_id, placement_id)
          DO UPDATE SET
            conversions = ut.conversions + Excluded.conversions,
            cvr = case coalesce(ut.imps, 0) when 0 then 0 else coalesce((ut.conversions + Excluded.conversions),0)::float / ut.imps end,
            cpa = case coalesce((ut.conversions + Excluded.conversions),0) when 0 then 0 else coalesce(ut.spent, 0) / (ut.conversions + Excluded.conversions) end;
                    """),

        # last 3 days

        migrations.RunSQL("delete from ui_usual_placements_grid_data_last_3_days_tracker;"),

        migrations.RunSQL("""
                    insert into ui_usual_placements_grid_data_last_3_days_tracker as ut (
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
              where
              "Date" >= date_trunc('day',(select date from last_modified where type='lastPrecalculatedTrackerCron') - interval '3 day')
              and
              "Date" <= (select date from last_modified where type='lastPrecalculatedTrackerCron')
              group by "CpId", "PlacementId";
                    """),

        migrations.RunSQL("""
            insert into ui_usual_placements_grid_data_last_3_days_tracker as ut (
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
              where
              rtb_click_tracker."Date" >= date_trunc('day',(select date from last_modified where type='lastPrecalculatedTrackerCron') - interval '3 day')
              and
              rtb_click_tracker."Date" <= (select date from last_modified where type='lastPrecalculatedTrackerCron')
              group by rtb_impression_tracker."CpId", rtb_impression_tracker."PlacementId"
            ON CONFLICT (campaign_id, placement_id)
              DO UPDATE SET
                clicks = coalesce(ut.clicks, 0) + coalesce(Excluded.clicks, 0),
                ctr = case coalesce(ut.imps, 0) when 0 then 0 else (ut.clicks + Excluded.clicks)::float / ut.imps end,
                cpc = case (ut.clicks + Excluded.clicks) when 0 then 0 else ut.spent / (ut.clicks + Excluded.clicks) end;
                        """),

        migrations.RunSQL("""
            insert into ui_usual_placements_grid_data_last_3_days_tracker as ut (
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
              from rtb_conversion_tracker
              left join rtb_impression_tracker
              on rtb_conversion_tracker."AuctionId" = rtb_impression_tracker."AuctionId"
              where
              rtb_conversion_tracker."Date" >= date_trunc('day',(select date from last_modified where type='lastPrecalculatedTrackerCron') - interval '3 day')
              and
              rtb_conversion_tracker."Date" <= (select date from last_modified where type='lastPrecalculatedTrackerCron')
            group by rtb_impression_tracker."CpId",rtb_impression_tracker."PlacementId"
            ON CONFLICT (campaign_id, placement_id)
              DO UPDATE SET
                conversions = ut.conversions + Excluded.conversions,
                cvr = case coalesce(ut.imps, 0) when 0 then 0 else coalesce((ut.conversions + Excluded.conversions),0)::float / ut.imps end,
                cpa = case coalesce((ut.conversions + Excluded.conversions),0) when 0 then 0 else coalesce(ut.spent, 0) / (ut.conversions + Excluded.conversions) end;
                        """),

        # last 7 days

        migrations.RunSQL("delete from ui_usual_placements_grid_data_last_7_days_tracker;"),

        migrations.RunSQL("""
                        insert into ui_usual_placements_grid_data_last_7_days_tracker as ut (
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
                  where
                  "Date" >= date_trunc('day',(select date from last_modified where type='lastPrecalculatedTrackerCron') - interval '7 day')
                  and
                  "Date" <= (select date from last_modified where type='lastPrecalculatedTrackerCron')
                  group by "CpId", "PlacementId";
                        """),

        migrations.RunSQL("""
                insert into ui_usual_placements_grid_data_last_7_days_tracker as ut (
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
                  where
                  rtb_click_tracker."Date" >= date_trunc('day',(select date from last_modified where type='lastPrecalculatedTrackerCron') - interval '7 day')
                  and
                  rtb_click_tracker."Date" <= (select date from last_modified where type='lastPrecalculatedTrackerCron')
                  group by rtb_impression_tracker."CpId", rtb_impression_tracker."PlacementId"
                ON CONFLICT (campaign_id, placement_id)
                  DO UPDATE SET
                    clicks = coalesce(ut.clicks, 0) + coalesce(Excluded.clicks, 0),
                    ctr = case coalesce(ut.imps, 0) when 0 then 0 else (ut.clicks + Excluded.clicks)::float / ut.imps end,
                    cpc = case (ut.clicks + Excluded.clicks) when 0 then 0 else ut.spent / (ut.clicks + Excluded.clicks) end;
                            """),

        migrations.RunSQL("""
                insert into ui_usual_placements_grid_data_last_7_days_tracker as ut (
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
                  from rtb_conversion_tracker
                  left join rtb_impression_tracker
                  on rtb_conversion_tracker."AuctionId" = rtb_impression_tracker."AuctionId"
                  where
                  rtb_conversion_tracker."Date" >= date_trunc('day',(select date from last_modified where type='lastPrecalculatedTrackerCron') - interval '7 day')
                  and
                  rtb_conversion_tracker."Date" <= (select date from last_modified where type='lastPrecalculatedTrackerCron')
                group by rtb_impression_tracker."CpId",rtb_impression_tracker."PlacementId"
                ON CONFLICT (campaign_id, placement_id)
                  DO UPDATE SET
                    conversions = ut.conversions + Excluded.conversions,
                    cvr = case coalesce(ut.imps, 0) when 0 then 0 else coalesce((ut.conversions + Excluded.conversions),0)::float / ut.imps end,
                    cpa = case coalesce((ut.conversions + Excluded.conversions),0) when 0 then 0 else coalesce(ut.spent, 0) / (ut.conversions + Excluded.conversions) end;
                            """),

        # last 14 days

        migrations.RunSQL("delete from ui_usual_placements_grid_data_last_14_days_tracker;"),

        migrations.RunSQL("""
                        insert into ui_usual_placements_grid_data_last_14_days_tracker as ut (
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
                  where
                  "Date" >= date_trunc('day',(select date from last_modified where type='lastPrecalculatedTrackerCron') - interval '14 day')
                  and
                  "Date" <= (select date from last_modified where type='lastPrecalculatedTrackerCron')
                  group by "CpId", "PlacementId";
                        """),

        migrations.RunSQL("""
                insert into ui_usual_placements_grid_data_last_14_days_tracker as ut (
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
                  where
                  rtb_click_tracker."Date" >= date_trunc('day',(select date from last_modified where type='lastPrecalculatedTrackerCron') - interval '14 day')
                  and
                  rtb_click_tracker."Date" <= (select date from last_modified where type='lastPrecalculatedTrackerCron')
                  group by rtb_impression_tracker."CpId", rtb_impression_tracker."PlacementId"
                ON CONFLICT (campaign_id, placement_id)
                  DO UPDATE SET
                    clicks = coalesce(ut.clicks, 0) + coalesce(Excluded.clicks, 0),
                    ctr = case coalesce(ut.imps, 0) when 0 then 0 else (ut.clicks + Excluded.clicks)::float / ut.imps end,
                    cpc = case (ut.clicks + Excluded.clicks) when 0 then 0 else ut.spent / (ut.clicks + Excluded.clicks) end;
                            """),

        migrations.RunSQL("""
                insert into ui_usual_placements_grid_data_last_14_days_tracker as ut (
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
                  from rtb_conversion_tracker
                  left join rtb_impression_tracker
                  on rtb_conversion_tracker."AuctionId" = rtb_impression_tracker."AuctionId"
                  where
                  rtb_conversion_tracker."Date" >= date_trunc('day',(select date from last_modified where type='lastPrecalculatedTrackerCron') - interval '14 day')
                  and
                  rtb_conversion_tracker."Date" <= (select date from last_modified where type='lastPrecalculatedTrackerCron')
                group by rtb_impression_tracker."CpId",rtb_impression_tracker."PlacementId"
                ON CONFLICT (campaign_id, placement_id)
                  DO UPDATE SET
                    conversions = ut.conversions + Excluded.conversions,
                    cvr = case coalesce(ut.imps, 0) when 0 then 0 else coalesce((ut.conversions + Excluded.conversions),0)::float / ut.imps end,
                    cpa = case coalesce((ut.conversions + Excluded.conversions),0) when 0 then 0 else coalesce(ut.spent, 0) / (ut.conversions + Excluded.conversions) end;
                            """),

        # last 21 days

        migrations.RunSQL("delete from ui_usual_placements_grid_data_last_21_days_tracker;"),

        migrations.RunSQL("""
                        insert into ui_usual_placements_grid_data_last_21_days_tracker as ut (
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
                  where
                  "Date" >= date_trunc('day',(select date from last_modified where type='lastPrecalculatedTrackerCron') - interval '21 day')
                  and
                  "Date" <= (select date from last_modified where type='lastPrecalculatedTrackerCron')
                  group by "CpId", "PlacementId";
                        """),

        migrations.RunSQL("""
                insert into ui_usual_placements_grid_data_last_21_days_tracker as ut (
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
                  where
                  rtb_click_tracker."Date" >= date_trunc('day',(select date from last_modified where type='lastPrecalculatedTrackerCron') - interval '21 day')
                  and
                  rtb_click_tracker."Date" <= (select date from last_modified where type='lastPrecalculatedTrackerCron')
                  group by rtb_impression_tracker."CpId", rtb_impression_tracker."PlacementId"
                ON CONFLICT (campaign_id, placement_id)
                  DO UPDATE SET
                    clicks = coalesce(ut.clicks, 0) + coalesce(Excluded.clicks, 0),
                    ctr = case coalesce(ut.imps, 0) when 0 then 0 else (ut.clicks + Excluded.clicks)::float / ut.imps end,
                    cpc = case (ut.clicks + Excluded.clicks) when 0 then 0 else ut.spent / (ut.clicks + Excluded.clicks) end;
                            """),

        migrations.RunSQL("""
                insert into ui_usual_placements_grid_data_last_21_days_tracker as ut (
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
                  from rtb_conversion_tracker
                  left join rtb_impression_tracker
                  on rtb_conversion_tracker."AuctionId" = rtb_impression_tracker."AuctionId"
                  where
                  rtb_conversion_tracker."Date" >= date_trunc('day',(select date from last_modified where type='lastPrecalculatedTrackerCron') - interval '21 day')
                  and
                  rtb_conversion_tracker."Date" <= (select date from last_modified where type='lastPrecalculatedTrackerCron')
                group by rtb_impression_tracker."CpId",rtb_impression_tracker."PlacementId"
                ON CONFLICT (campaign_id, placement_id)
                  DO UPDATE SET
                    conversions = ut.conversions + Excluded.conversions,
                    cvr = case coalesce(ut.imps, 0) when 0 then 0 else coalesce((ut.conversions + Excluded.conversions),0)::float / ut.imps end,
                    cpa = case coalesce((ut.conversions + Excluded.conversions),0) when 0 then 0 else coalesce(ut.spent, 0) / (ut.conversions + Excluded.conversions) end;
                            """),

        # last 90 days

        migrations.RunSQL("delete from ui_usual_placements_grid_data_last_90_days_tracker;"),

        migrations.RunSQL("""
                        insert into ui_usual_placements_grid_data_last_90_days_tracker as ut (
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
                  where
                  "Date" >= date_trunc('day',(select date from last_modified where type='lastPrecalculatedTrackerCron') - interval '90 day')
                  and
                  "Date" <= (select date from last_modified where type='lastPrecalculatedTrackerCron')
                  group by "CpId", "PlacementId";
                        """),

        migrations.RunSQL("""
                insert into ui_usual_placements_grid_data_last_90_days_tracker as ut (
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
                  where
                  rtb_click_tracker."Date" >= date_trunc('day',(select date from last_modified where type='lastPrecalculatedTrackerCron') - interval '90 day')
                  and
                  rtb_click_tracker."Date" <= (select date from last_modified where type='lastPrecalculatedTrackerCron')
                  group by rtb_impression_tracker."CpId", rtb_impression_tracker."PlacementId"
                ON CONFLICT (campaign_id, placement_id)
                  DO UPDATE SET
                    clicks = coalesce(ut.clicks, 0) + coalesce(Excluded.clicks, 0),
                    ctr = case coalesce(ut.imps, 0) when 0 then 0 else (ut.clicks + Excluded.clicks)::float / ut.imps end,
                    cpc = case (ut.clicks + Excluded.clicks) when 0 then 0 else ut.spent / (ut.clicks + Excluded.clicks) end;
                            """),

        migrations.RunSQL("""
                insert into ui_usual_placements_grid_data_last_90_days_tracker as ut (
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
                  from rtb_conversion_tracker
                  left join rtb_impression_tracker
                  on rtb_conversion_tracker."AuctionId" = rtb_impression_tracker."AuctionId"
                  where
                  rtb_conversion_tracker."Date" >= date_trunc('day',(select date from last_modified where type='lastPrecalculatedTrackerCron') - interval '90 day')
                  and
                  rtb_conversion_tracker."Date" <= (select date from last_modified where type='lastPrecalculatedTrackerCron')
                group by rtb_impression_tracker."CpId",rtb_impression_tracker."PlacementId"
                ON CONFLICT (campaign_id, placement_id)
                  DO UPDATE SET
                    conversions = ut.conversions + Excluded.conversions,
                    cvr = case coalesce(ut.imps, 0) when 0 then 0 else coalesce((ut.conversions + Excluded.conversions),0)::float / ut.imps end,
                    cpa = case coalesce((ut.conversions + Excluded.conversions),0) when 0 then 0 else coalesce(ut.spent, 0) / (ut.conversions + Excluded.conversions) end;
                            """),

        # last month

        migrations.RunSQL("delete from ui_usual_placements_grid_data_last_month_tracker;"),

        migrations.RunSQL("""
                            insert into ui_usual_placements_grid_data_last_month_tracker as ut (
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
                      where
                      "Date" >= date_trunc('month',(select date from last_modified where type='lastPrecalculatedTrackerCron') - interval '1 month')
                      and
                      "Date" < date_trunc('month',(select date from last_modified where type='lastPrecalculatedTrackerCron'))
                      group by "CpId", "PlacementId";
                            """),

        migrations.RunSQL("""
                    insert into ui_usual_placements_grid_data_last_month_tracker as ut (
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
                      where
                      rtb_click_tracker."Date" >= date_trunc('month',(select date from last_modified where type='lastPrecalculatedTrackerCron') - interval '1 month')
                      and
                      rtb_click_tracker."Date" < date_trunc('month',(select date from last_modified where type='lastPrecalculatedTrackerCron'))
                      group by rtb_impression_tracker."CpId", rtb_impression_tracker."PlacementId"
                    ON CONFLICT (campaign_id, placement_id)
                      DO UPDATE SET
                        clicks = coalesce(ut.clicks, 0) + coalesce(Excluded.clicks, 0),
                        ctr = case coalesce(ut.imps, 0) when 0 then 0 else (ut.clicks + Excluded.clicks)::float / ut.imps end,
                        cpc = case (ut.clicks + Excluded.clicks) when 0 then 0 else ut.spent / (ut.clicks + Excluded.clicks) end;
                                """),

        migrations.RunSQL("""
                    insert into ui_usual_placements_grid_data_last_month_tracker as ut (
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
                      from rtb_conversion_tracker
                      left join rtb_impression_tracker
                      on rtb_conversion_tracker."AuctionId" = rtb_impression_tracker."AuctionId"
                      where
                      rtb_conversion_tracker."Date" >= date_trunc('month',(select date from last_modified where type='lastPrecalculatedTrackerCron') - interval '1 month')
                      and
                      rtb_conversion_tracker."Date" < date_trunc('month',(select date from last_modified where type='lastPrecalculatedTrackerCron'))
                    group by rtb_impression_tracker."CpId",rtb_impression_tracker."PlacementId"
                    ON CONFLICT (campaign_id, placement_id)
                      DO UPDATE SET
                        conversions = ut.conversions + Excluded.conversions,
                        cvr = case coalesce(ut.imps, 0) when 0 then 0 else coalesce((ut.conversions + Excluded.conversions),0)::float / ut.imps end,
                        cpa = case coalesce((ut.conversions + Excluded.conversions),0) when 0 then 0 else coalesce(ut.spent, 0) / (ut.conversions + Excluded.conversions) end;
                                """),

        # cur month

        migrations.RunSQL("delete from ui_usual_placements_grid_data_cur_month_tracker;"),

        migrations.RunSQL("""
                            insert into ui_usual_placements_grid_data_cur_month_tracker as ut (
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
                      where
                      "Date" >= date_trunc('month',(select date from last_modified where type='lastPrecalculatedTrackerCron'))
                      and
                      "Date" <= (select date from last_modified where type='lastPrecalculatedTrackerCron')
                      group by "CpId", "PlacementId";
                            """),

        migrations.RunSQL("""
                    insert into ui_usual_placements_grid_data_cur_month_tracker as ut (
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
                      where
                      rtb_click_tracker."Date" >= date_trunc('month',(select date from last_modified where type='lastPrecalculatedTrackerCron'))
                      and
                      rtb_click_tracker."Date" <= (select date from last_modified where type='lastPrecalculatedTrackerCron')
                      group by rtb_impression_tracker."CpId", rtb_impression_tracker."PlacementId"
                    ON CONFLICT (campaign_id, placement_id)
                      DO UPDATE SET
                        clicks = coalesce(ut.clicks, 0) + coalesce(Excluded.clicks, 0),
                        ctr = case coalesce(ut.imps, 0) when 0 then 0 else (ut.clicks + Excluded.clicks)::float / ut.imps end,
                        cpc = case (ut.clicks + Excluded.clicks) when 0 then 0 else ut.spent / (ut.clicks + Excluded.clicks) end;
                                """),

        migrations.RunSQL("""
                    insert into ui_usual_placements_grid_data_cur_month_tracker as ut (
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
                      from rtb_conversion_tracker
                      left join rtb_impression_tracker
                      on rtb_conversion_tracker."AuctionId" = rtb_impression_tracker."AuctionId"
                      where
                      rtb_conversion_tracker."Date" >= date_trunc('month',(select date from last_modified where type='lastPrecalculatedTrackerCron'))
                      and
                      rtb_conversion_tracker."Date" <= (select date from last_modified where type='lastPrecalculatedTrackerCron')
                    group by rtb_impression_tracker."CpId",rtb_impression_tracker."PlacementId"
                    ON CONFLICT (campaign_id, placement_id)
                      DO UPDATE SET
                        conversions = ut.conversions + Excluded.conversions,
                        cvr = case coalesce(ut.imps, 0) when 0 then 0 else coalesce((ut.conversions + Excluded.conversions),0)::float / ut.imps end,
                        cpa = case coalesce((ut.conversions + Excluded.conversions),0) when 0 then 0 else coalesce(ut.spent, 0) / (ut.conversions + Excluded.conversions) end;
                                """),

        ##
        # CAMPAIGNS GRID
        ##

        # all

        migrations.RunSQL("delete from ui_usual_campaigns_grid_data_all_tracker;"),

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
    0 as clicks,
    page.spent,
    0 as conversions,
    0,
    0,
    case coalesce(page.imps, 0) when 0 then 0 else coalesce(page.spent, 0) / coalesce(page.imps, 0) * 1000.0 end,
    0,
    0,
    0,
    0,
    0,
    array_to_json(array((select
         json_build_object(
         'day', site_r."Date"::timestamp::date,
         'imp', count(site_r."id"),
         'spend', sum(site_r."PricePaid"),
         'clicks', 0,
         'conversions', 0,
         'cvr', 0,
         'cpc', 0,
         'ctr', 0)
       from
            rtb_impression_tracker site_r
       where site_r."CpId"= page."CpId"
       and
       site_r."Date" <= (select date from last_modified where type='lastPrecalculatedTrackerCron')
       group by site_r."Date"::timestamp::date
       order by site_r."Date"::timestamp::date)))
from (
      select
        "CpId",
        count(id) as imps,
        sum("PricePaid") as spent
      from
        rtb_impression_tracker
      where "Date" <= (select date from last_modified where type='lastPrecalculatedTrackerCron')
      group by
        "CpId"
     ) page;
                    """),

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
    0,
    page.clicks,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    array_to_json(array((select
         json_build_object(
         'day', site_r."Date"::timestamp::date,
         'imp', 0,
         'mediaspent', 0,
         'clicks', count(site_r."id"),
         'conversions', 0,
         'cpa', 0,
         'cpc', 0,
         'ctr', 0)
       from
            rtb_click_tracker site_r
       where site_r."CpId"= page."CpId"
       and
       site_r."Date" <= (select date from last_modified where type='lastPrecalculatedTrackerCron')
       group by site_r."Date"::timestamp::date
       order by site_r."Date"::timestamp::date)))
from (
      select
        "CpId",
        count(id) as clicks
      from
        rtb_click_tracker
      where "Date" <= (select date from last_modified where type='lastPrecalculatedTrackerCron')
      group by
        "CpId"
     ) page
ON CONFLICT (campaign_id)
  DO UPDATE SET
     clicks = coalesce(ut.clicks, 0) + coalesce(Excluded.clicks, 0),
     ctr = case (coalesce(ut.imps, 0) + coalesce(Excluded.imps, 0)) when 0 then 0 else (coalesce(ut.clicks, 0) + coalesce(Excluded.clicks, 0))::float / (coalesce(ut.imps, 0) + coalesce(Excluded.imps, 0)) end,
     cpc = case (coalesce(ut.clicks, 0) + coalesce(Excluded.clicks, 0)) when 0 then 0 else (coalesce(ut.spent, 0) + coalesce(Excluded.spent, 0)) / (coalesce(ut.clicks, 0) + coalesce(Excluded.clicks, 0)) end,
     day_chart = case (ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'day')::text when (Excluded.day_chart::json->0->'day')::text
                  then jsonb_set(
                    ut.day_chart::jsonb,
                    concat('{', (jsonb_array_length(ut.day_chart)-1), '}')::text[],
                    json_build_object(
                        'day', ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'day',
                        'imp', coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'imp')::text::integer,0),
                        'spend', coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'spend')::text::float,0),
                        'clicks', coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'clicks')::text::integer,0) + coalesce((Excluded.day_chart::json->0->'clicks')::text::integer,0),
                        'conversions', coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'conversions')::text::integer,0),
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
                    """),

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
    0,
    0,
    page.conversions,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    array_to_json(array((select
         json_build_object(
         'day', site_r."Date"::timestamp::date,
         'imp', 0,
         'mediaspent', 0,
         'clicks', count(site_r."id"),
         'conversions', 0,
         'cpa', 0,
         'cpc', 0,
         'ctr', 0)
       from
            rtb_conversion_tracker site_r
       where site_r."CpId"= page."CpId"
       and
       site_r."Date" <= (select date from last_modified where type='lastPrecalculatedTrackerCron')
       group by site_r."Date"::timestamp::date
       order by site_r."Date"::timestamp::date)))
from (
      select
        "CpId",
        count(id) as conversions
      from
        rtb_conversion_tracker
      where "Date" <= (select date from last_modified where type='lastPrecalculatedTrackerCron')
      group by
        "CpId"
     ) page
ON CONFLICT (campaign_id)
  DO UPDATE SET
     conversions = coalesce(ut.conversions, 0) + coalesce(Excluded.conversions, 0),
     cvr = case (coalesce(ut.imps, 0) + coalesce(Excluded.imps, 0)) when 0 then 0 else (coalesce(ut.conversions, 0) + coalesce(Excluded.conversions, 0))::float / (coalesce(ut.imps, 0) + coalesce(Excluded.imps, 0)) end,
     day_chart = case (ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'day')::text when (Excluded.day_chart::json->0->'day')::text
                  then jsonb_set(
                    ut.day_chart::jsonb,
                    concat('{', (jsonb_array_length(ut.day_chart)-1), '}')::text[],
                    json_build_object(
                        'day', ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'day',
                        'imp', coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'imp')::text::integer,0),
                        'spend', coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'spend')::text::float,0),
                        'clicks', coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'clicks')::text::integer,0),
                        'conversions', coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'conversions')::text::integer,0)  + coalesce((Excluded.day_chart::json->0->'conversions')::text::integer,0),
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
                        """),

        # yesterday

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
            0 as clicks,
            page.spent,
            0 as conversions,
            0,
            0,
            case coalesce(page.imps, 0) when 0 then 0 else coalesce(page.spent, 0) / coalesce(page.imps, 0) * 1000.0 end,
            0,
            0,
            0,
            0,
            0,
            array_to_json(array((select
                 json_build_object(
                 'day', site_r."Date"::timestamp::date,
                 'imp', count(site_r."id"),
                 'spend', sum(site_r."PricePaid"),
                 'clicks', 0,
                 'conversions', 0,
                 'cvr', 0,
                 'cpc', 0,
                 'ctr', 0)
               from
                    rtb_impression_tracker site_r
               where site_r."CpId"= page."CpId"
               and
               site_r."Date" >= date_trunc('day',(select date from last_modified where type='lastPrecalculatedTrackerCron') - interval '1 day')
               and
               site_r."Date" <= (select date from last_modified where type='lastPrecalculatedTrackerCron')
               group by site_r."Date"::timestamp::date
               order by site_r."Date"::timestamp::date)))
        from (
              select
                "CpId",
                count(id) as imps,
                sum("PricePaid") as spent
              from
                rtb_impression_tracker
              where
              "Date" >= date_trunc('day',(select date from last_modified where type='lastPrecalculatedTrackerCron') - interval '1 day')
              and
              "Date" <= (select date from last_modified where type='lastPrecalculatedTrackerCron')
              group by
                "CpId"
             ) page;
                            """),

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
            0,
            page.clicks,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            array_to_json(array((select
                 json_build_object(
                 'day', site_r."Date"::timestamp::date,
                 'imp', 0,
                 'mediaspent', 0,
                 'clicks', count(site_r."id"),
                 'conversions', 0,
                 'cpa', 0,
                 'cpc', 0,
                 'ctr', 0)
               from
                    rtb_click_tracker site_r
               where site_r."CpId"= page."CpId"
               and
               site_r."Date" >= date_trunc('day',(select date from last_modified where type='lastPrecalculatedTrackerCron') - interval '1 day')
               and
               site_r."Date" <= (select date from last_modified where type='lastPrecalculatedTrackerCron')
               group by site_r."Date"::timestamp::date
               order by site_r."Date"::timestamp::date)))
        from (
              select
                "CpId",
                count(id) as clicks
              from
                rtb_click_tracker
              where
              "Date" >= date_trunc('day',(select date from last_modified where type='lastPrecalculatedTrackerCron') - interval '1 day')
              and
              "Date" <= (select date from last_modified where type='lastPrecalculatedTrackerCron')
              group by
                "CpId"
             ) page
        ON CONFLICT (campaign_id)
          DO UPDATE SET
             clicks = coalesce(ut.clicks, 0) + coalesce(Excluded.clicks, 0),
             ctr = case (coalesce(ut.imps, 0) + coalesce(Excluded.imps, 0)) when 0 then 0 else (coalesce(ut.clicks, 0) + coalesce(Excluded.clicks, 0))::float / (coalesce(ut.imps, 0) + coalesce(Excluded.imps, 0)) end,
             cpc = case (coalesce(ut.clicks, 0) + coalesce(Excluded.clicks, 0)) when 0 then 0 else (coalesce(ut.spent, 0) + coalesce(Excluded.spent, 0)) / (coalesce(ut.clicks, 0) + coalesce(Excluded.clicks, 0)) end,
             day_chart = case (ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'day')::text when (Excluded.day_chart::json->0->'day')::text
                          then jsonb_set(
                            ut.day_chart::jsonb,
                            concat('{', (jsonb_array_length(ut.day_chart)-1), '}')::text[],
                            json_build_object(
                                'day', ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'day',
                                'imp', coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'imp')::text::integer,0),
                                'spend', coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'spend')::text::float,0),
                                'clicks', coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'clicks')::text::integer,0) + coalesce((Excluded.day_chart::json->0->'clicks')::text::integer,0),
                                'conversions', coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'conversions')::text::integer,0),
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
                            """),

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
            0,
            0,
            page.conversions,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            array_to_json(array((select
                 json_build_object(
                 'day', site_r."Date"::timestamp::date,
                 'imp', 0,
                 'mediaspent', 0,
                 'clicks', count(site_r."id"),
                 'conversions', 0,
                 'cpa', 0,
                 'cpc', 0,
                 'ctr', 0)
               from
                    rtb_conversion_tracker site_r
               where site_r."CpId"= page."CpId"
               and
               site_r."Date" >= date_trunc('day',(select date from last_modified where type='lastPrecalculatedTrackerCron') - interval '1 day')
               and
               site_r."Date" <= (select date from last_modified where type='lastPrecalculatedTrackerCron')
               group by site_r."Date"::timestamp::date
               order by site_r."Date"::timestamp::date)))
        from (
              select
                "CpId",
                count(id) as conversions
              from
                rtb_conversion_tracker
              where
              "Date" >= date_trunc('day',(select date from last_modified where type='lastPrecalculatedTrackerCron') - interval '1 day')
              and
              "Date" <= (select date from last_modified where type='lastPrecalculatedTrackerCron')
              group by
                "CpId"
             ) page
        ON CONFLICT (campaign_id)
          DO UPDATE SET
             conversions = coalesce(ut.conversions, 0) + coalesce(Excluded.conversions, 0),
             cvr = case (coalesce(ut.imps, 0) + coalesce(Excluded.imps, 0)) when 0 then 0 else (coalesce(ut.conversions, 0) + coalesce(Excluded.conversions, 0))::float / (coalesce(ut.imps, 0) + coalesce(Excluded.imps, 0)) end,
             day_chart = case (ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'day')::text when (Excluded.day_chart::json->0->'day')::text
                          then jsonb_set(
                            ut.day_chart::jsonb,
                            concat('{', (jsonb_array_length(ut.day_chart)-1), '}')::text[],
                            json_build_object(
                                'day', ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'day',
                                'imp', coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'imp')::text::integer,0),
                                'spend', coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'spend')::text::float,0),
                                'clicks', coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'clicks')::text::integer,0),
                                'conversions', coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'conversions')::text::integer,0)  + coalesce((Excluded.day_chart::json->0->'conversions')::text::integer,0),
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
                                """),

        # last 3 days

        migrations.RunSQL("delete from ui_usual_campaigns_grid_data_last_3_days_tracker;"),

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
                0 as clicks,
                page.spent,
                0 as conversions,
                0,
                0,
                case coalesce(page.imps, 0) when 0 then 0 else coalesce(page.spent, 0) / coalesce(page.imps, 0) * 1000.0 end,
                0,
                0,
                0,
                0,
                0,
                array_to_json(array((select
                     json_build_object(
                     'day', site_r."Date"::timestamp::date,
                     'imp', count(site_r."id"),
                     'spend', sum(site_r."PricePaid"),
                     'clicks', 0,
                     'conversions', 0,
                     'cvr', 0,
                     'cpc', 0,
                     'ctr', 0)
                   from
                        rtb_impression_tracker site_r
                   where site_r."CpId"= page."CpId"
                   and
                   site_r."Date" >= date_trunc('day',(select date from last_modified where type='lastPrecalculatedTrackerCron') - interval '3 day')
                   and
                   site_r."Date" <= (select date from last_modified where type='lastPrecalculatedTrackerCron')
                   group by site_r."Date"::timestamp::date
                   order by site_r."Date"::timestamp::date)))
            from (
                  select
                    "CpId",
                    count(id) as imps,
                    sum("PricePaid") as spent
                  from
                    rtb_impression_tracker
                  where
                  "Date" >= date_trunc('day',(select date from last_modified where type='lastPrecalculatedTrackerCron') - interval '3 day')
                  and
                  "Date" <= (select date from last_modified where type='lastPrecalculatedTrackerCron')
                  group by
                    "CpId"
                 ) page;
                                """),

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
                0,
                page.clicks,
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                array_to_json(array((select
                     json_build_object(
                     'day', site_r."Date"::timestamp::date,
                     'imp', 0,
                     'mediaspent', 0,
                     'clicks', count(site_r."id"),
                     'conversions', 0,
                     'cpa', 0,
                     'cpc', 0,
                     'ctr', 0)
                   from
                        rtb_click_tracker site_r
                   where site_r."CpId"= page."CpId"
                   and
                   site_r."Date" >= date_trunc('day',(select date from last_modified where type='lastPrecalculatedTrackerCron') - interval '3 day')
                   and
                   site_r."Date" <= (select date from last_modified where type='lastPrecalculatedTrackerCron')
                   group by site_r."Date"::timestamp::date
                   order by site_r."Date"::timestamp::date)))
            from (
                  select
                    "CpId",
                    count(id) as clicks
                  from
                    rtb_click_tracker
                  where
                  "Date" >= date_trunc('day',(select date from last_modified where type='lastPrecalculatedTrackerCron') - interval '3 day')
                  and
                  "Date" <= (select date from last_modified where type='lastPrecalculatedTrackerCron')
                  group by
                    "CpId"
                 ) page
            ON CONFLICT (campaign_id)
              DO UPDATE SET
                 clicks = coalesce(ut.clicks, 0) + coalesce(Excluded.clicks, 0),
                 ctr = case (coalesce(ut.imps, 0) + coalesce(Excluded.imps, 0)) when 0 then 0 else (coalesce(ut.clicks, 0) + coalesce(Excluded.clicks, 0))::float / (coalesce(ut.imps, 0) + coalesce(Excluded.imps, 0)) end,
                 cpc = case (coalesce(ut.clicks, 0) + coalesce(Excluded.clicks, 0)) when 0 then 0 else (coalesce(ut.spent, 0) + coalesce(Excluded.spent, 0)) / (coalesce(ut.clicks, 0) + coalesce(Excluded.clicks, 0)) end,
                 day_chart = case (ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'day')::text when (Excluded.day_chart::json->0->'day')::text
                              then jsonb_set(
                                ut.day_chart::jsonb,
                                concat('{', (jsonb_array_length(ut.day_chart)-1), '}')::text[],
                                json_build_object(
                                    'day', ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'day',
                                    'imp', coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'imp')::text::integer,0),
                                    'spend', coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'spend')::text::float,0),
                                    'clicks', coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'clicks')::text::integer,0) + coalesce((Excluded.day_chart::json->0->'clicks')::text::integer,0),
                                    'conversions', coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'conversions')::text::integer,0),
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
                                """),

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
                0,
                0,
                page.conversions,
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                array_to_json(array((select
                     json_build_object(
                     'day', site_r."Date"::timestamp::date,
                     'imp', 0,
                     'mediaspent', 0,
                     'clicks', count(site_r."id"),
                     'conversions', 0,
                     'cpa', 0,
                     'cpc', 0,
                     'ctr', 0)
                   from
                        rtb_conversion_tracker site_r
                   where site_r."CpId"= page."CpId"
                   and
                   site_r."Date" >= date_trunc('day',(select date from last_modified where type='lastPrecalculatedTrackerCron') - interval '3 day')
                   and
                   site_r."Date" <= (select date from last_modified where type='lastPrecalculatedTrackerCron')
                   group by site_r."Date"::timestamp::date
                   order by site_r."Date"::timestamp::date)))
            from (
                  select
                    "CpId",
                    count(id) as conversions
                  from
                    rtb_conversion_tracker
                  where
                  "Date" >= date_trunc('day',(select date from last_modified where type='lastPrecalculatedTrackerCron') - interval '3 day')
                  and
                  "Date" <= (select date from last_modified where type='lastPrecalculatedTrackerCron')
                  group by
                    "CpId"
                 ) page
            ON CONFLICT (campaign_id)
              DO UPDATE SET
                 conversions = coalesce(ut.conversions, 0) + coalesce(Excluded.conversions, 0),
                 cvr = case (coalesce(ut.imps, 0) + coalesce(Excluded.imps, 0)) when 0 then 0 else (coalesce(ut.conversions, 0) + coalesce(Excluded.conversions, 0))::float / (coalesce(ut.imps, 0) + coalesce(Excluded.imps, 0)) end,
                 day_chart = case (ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'day')::text when (Excluded.day_chart::json->0->'day')::text
                              then jsonb_set(
                                ut.day_chart::jsonb,
                                concat('{', (jsonb_array_length(ut.day_chart)-1), '}')::text[],
                                json_build_object(
                                    'day', ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'day',
                                    'imp', coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'imp')::text::integer,0),
                                    'spend', coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'spend')::text::float,0),
                                    'clicks', coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'clicks')::text::integer,0),
                                    'conversions', coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'conversions')::text::integer,0)  + coalesce((Excluded.day_chart::json->0->'conversions')::text::integer,0),
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
                                    """),

        # last 7 days

        migrations.RunSQL("delete from ui_usual_campaigns_grid_data_last_7_days_tracker;"),

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
                    0 as clicks,
                    page.spent,
                    0 as conversions,
                    0,
                    0,
                    case coalesce(page.imps, 0) when 0 then 0 else coalesce(page.spent, 0) / coalesce(page.imps, 0) * 1000.0 end,
                    0,
                    0,
                    0,
                    0,
                    0,
                    array_to_json(array((select
                         json_build_object(
                         'day', site_r."Date"::timestamp::date,
                         'imp', count(site_r."id"),
                         'spend', sum(site_r."PricePaid"),
                         'clicks', 0,
                         'conversions', 0,
                         'cvr', 0,
                         'cpc', 0,
                         'ctr', 0)
                       from
                            rtb_impression_tracker site_r
                       where site_r."CpId"= page."CpId"
                       and
                       site_r."Date" >= date_trunc('day',(select date from last_modified where type='lastPrecalculatedTrackerCron') - interval '7 day')
                       and
                       site_r."Date" <= (select date from last_modified where type='lastPrecalculatedTrackerCron')
                       group by site_r."Date"::timestamp::date
                       order by site_r."Date"::timestamp::date)))
                from (
                      select
                        "CpId",
                        count(id) as imps,
                        sum("PricePaid") as spent
                      from
                        rtb_impression_tracker
                      where
                      "Date" >= date_trunc('day',(select date from last_modified where type='lastPrecalculatedTrackerCron') - interval '7 day')
                      and
                      "Date" <= (select date from last_modified where type='lastPrecalculatedTrackerCron')
                      group by
                        "CpId"
                     ) page;
                                    """),

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
                    0,
                    page.clicks,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    array_to_json(array((select
                         json_build_object(
                         'day', site_r."Date"::timestamp::date,
                         'imp', 0,
                         'mediaspent', 0,
                         'clicks', count(site_r."id"),
                         'conversions', 0,
                         'cpa', 0,
                         'cpc', 0,
                         'ctr', 0)
                       from
                            rtb_click_tracker site_r
                       where site_r."CpId"= page."CpId"
                       and
                       site_r."Date" >= date_trunc('day',(select date from last_modified where type='lastPrecalculatedTrackerCron') - interval '7 day')
                       and
                       site_r."Date" <= (select date from last_modified where type='lastPrecalculatedTrackerCron')
                       group by site_r."Date"::timestamp::date
                       order by site_r."Date"::timestamp::date)))
                from (
                      select
                        "CpId",
                        count(id) as clicks
                      from
                        rtb_click_tracker
                      where
                      "Date" >= date_trunc('day',(select date from last_modified where type='lastPrecalculatedTrackerCron') - interval '7 day')
                      and
                      "Date" <= (select date from last_modified where type='lastPrecalculatedTrackerCron')
                      group by
                        "CpId"
                     ) page
                ON CONFLICT (campaign_id)
                  DO UPDATE SET
                     clicks = coalesce(ut.clicks, 0) + coalesce(Excluded.clicks, 0),
                     ctr = case (coalesce(ut.imps, 0) + coalesce(Excluded.imps, 0)) when 0 then 0 else (coalesce(ut.clicks, 0) + coalesce(Excluded.clicks, 0))::float / (coalesce(ut.imps, 0) + coalesce(Excluded.imps, 0)) end,
                     cpc = case (coalesce(ut.clicks, 0) + coalesce(Excluded.clicks, 0)) when 0 then 0 else (coalesce(ut.spent, 0) + coalesce(Excluded.spent, 0)) / (coalesce(ut.clicks, 0) + coalesce(Excluded.clicks, 0)) end,
                     day_chart = case (ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'day')::text when (Excluded.day_chart::json->0->'day')::text
                                  then jsonb_set(
                                    ut.day_chart::jsonb,
                                    concat('{', (jsonb_array_length(ut.day_chart)-1), '}')::text[],
                                    json_build_object(
                                        'day', ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'day',
                                        'imp', coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'imp')::text::integer,0),
                                        'spend', coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'spend')::text::float,0),
                                        'clicks', coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'clicks')::text::integer,0) + coalesce((Excluded.day_chart::json->0->'clicks')::text::integer,0),
                                        'conversions', coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'conversions')::text::integer,0),
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
                                    """),

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
                    0,
                    0,
                    page.conversions,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    array_to_json(array((select
                         json_build_object(
                         'day', site_r."Date"::timestamp::date,
                         'imp', 0,
                         'mediaspent', 0,
                         'clicks', count(site_r."id"),
                         'conversions', 0,
                         'cpa', 0,
                         'cpc', 0,
                         'ctr', 0)
                       from
                            rtb_conversion_tracker site_r
                       where site_r."CpId"= page."CpId"
                       and
                       site_r."Date" >= date_trunc('day',(select date from last_modified where type='lastPrecalculatedTrackerCron') - interval '7 day')
                       and
                       site_r."Date" <= (select date from last_modified where type='lastPrecalculatedTrackerCron')
                       group by site_r."Date"::timestamp::date
                       order by site_r."Date"::timestamp::date)))
                from (
                      select
                        "CpId",
                        count(id) as conversions
                      from
                        rtb_conversion_tracker
                      where
                      "Date" >= date_trunc('day',(select date from last_modified where type='lastPrecalculatedTrackerCron') - interval '7 day')
                      and
                      "Date" <= (select date from last_modified where type='lastPrecalculatedTrackerCron')
                      group by
                        "CpId"
                     ) page
                ON CONFLICT (campaign_id)
                  DO UPDATE SET
                     conversions = coalesce(ut.conversions, 0) + coalesce(Excluded.conversions, 0),
                     cvr = case (coalesce(ut.imps, 0) + coalesce(Excluded.imps, 0)) when 0 then 0 else (coalesce(ut.conversions, 0) + coalesce(Excluded.conversions, 0))::float / (coalesce(ut.imps, 0) + coalesce(Excluded.imps, 0)) end,
                     day_chart = case (ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'day')::text when (Excluded.day_chart::json->0->'day')::text
                                  then jsonb_set(
                                    ut.day_chart::jsonb,
                                    concat('{', (jsonb_array_length(ut.day_chart)-1), '}')::text[],
                                    json_build_object(
                                        'day', ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'day',
                                        'imp', coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'imp')::text::integer,0),
                                        'spend', coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'spend')::text::float,0),
                                        'clicks', coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'clicks')::text::integer,0),
                                        'conversions', coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'conversions')::text::integer,0)  + coalesce((Excluded.day_chart::json->0->'conversions')::text::integer,0),
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
                                        """),

        # last 14 days

        migrations.RunSQL("delete from ui_usual_campaigns_grid_data_last_14_days_tracker;"),

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
                    0 as clicks,
                    page.spent,
                    0 as conversions,
                    0,
                    0,
                    case coalesce(page.imps, 0) when 0 then 0 else coalesce(page.spent, 0) / coalesce(page.imps, 0) * 1000.0 end,
                    0,
                    0,
                    0,
                    0,
                    0,
                    array_to_json(array((select
                         json_build_object(
                         'day', site_r."Date"::timestamp::date,
                         'imp', count(site_r."id"),
                         'spend', sum(site_r."PricePaid"),
                         'clicks', 0,
                         'conversions', 0,
                         'cvr', 0,
                         'cpc', 0,
                         'ctr', 0)
                       from
                            rtb_impression_tracker site_r
                       where site_r."CpId"= page."CpId"
                       and
                       site_r."Date" >= date_trunc('day',(select date from last_modified where type='lastPrecalculatedTrackerCron') - interval '14 day')
                       and
                       site_r."Date" <= (select date from last_modified where type='lastPrecalculatedTrackerCron')
                       group by site_r."Date"::timestamp::date
                       order by site_r."Date"::timestamp::date)))
                from (
                      select
                        "CpId",
                        count(id) as imps,
                        sum("PricePaid") as spent
                      from
                        rtb_impression_tracker
                      where
                      "Date" >= date_trunc('day',(select date from last_modified where type='lastPrecalculatedTrackerCron') - interval '14 day')
                      and
                      "Date" <= (select date from last_modified where type='lastPrecalculatedTrackerCron')
                      group by
                        "CpId"
                     ) page;
                                    """),

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
                    0,
                    page.clicks,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    array_to_json(array((select
                         json_build_object(
                         'day', site_r."Date"::timestamp::date,
                         'imp', 0,
                         'mediaspent', 0,
                         'clicks', count(site_r."id"),
                         'conversions', 0,
                         'cpa', 0,
                         'cpc', 0,
                         'ctr', 0)
                       from
                            rtb_click_tracker site_r
                       where site_r."CpId"= page."CpId"
                       and
                       site_r."Date" >= date_trunc('day',(select date from last_modified where type='lastPrecalculatedTrackerCron') - interval '14 day')
                       and
                       site_r."Date" <= (select date from last_modified where type='lastPrecalculatedTrackerCron')
                       group by site_r."Date"::timestamp::date
                       order by site_r."Date"::timestamp::date)))
                from (
                      select
                        "CpId",
                        count(id) as clicks
                      from
                        rtb_click_tracker
                      where
                      "Date" >= date_trunc('day',(select date from last_modified where type='lastPrecalculatedTrackerCron') - interval '14 day')
                      and
                      "Date" <= (select date from last_modified where type='lastPrecalculatedTrackerCron')
                      group by
                        "CpId"
                     ) page
                ON CONFLICT (campaign_id)
                  DO UPDATE SET
                     clicks = coalesce(ut.clicks, 0) + coalesce(Excluded.clicks, 0),
                     ctr = case (coalesce(ut.imps, 0) + coalesce(Excluded.imps, 0)) when 0 then 0 else (coalesce(ut.clicks, 0) + coalesce(Excluded.clicks, 0))::float / (coalesce(ut.imps, 0) + coalesce(Excluded.imps, 0)) end,
                     cpc = case (coalesce(ut.clicks, 0) + coalesce(Excluded.clicks, 0)) when 0 then 0 else (coalesce(ut.spent, 0) + coalesce(Excluded.spent, 0)) / (coalesce(ut.clicks, 0) + coalesce(Excluded.clicks, 0)) end,
                     day_chart = case (ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'day')::text when (Excluded.day_chart::json->0->'day')::text
                                  then jsonb_set(
                                    ut.day_chart::jsonb,
                                    concat('{', (jsonb_array_length(ut.day_chart)-1), '}')::text[],
                                    json_build_object(
                                        'day', ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'day',
                                        'imp', coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'imp')::text::integer,0),
                                        'spend', coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'spend')::text::float,0),
                                        'clicks', coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'clicks')::text::integer,0) + coalesce((Excluded.day_chart::json->0->'clicks')::text::integer,0),
                                        'conversions', coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'conversions')::text::integer,0),
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
                                    """),

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
                    0,
                    0,
                    page.conversions,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    array_to_json(array((select
                         json_build_object(
                         'day', site_r."Date"::timestamp::date,
                         'imp', 0,
                         'mediaspent', 0,
                         'clicks', count(site_r."id"),
                         'conversions', 0,
                         'cpa', 0,
                         'cpc', 0,
                         'ctr', 0)
                       from
                            rtb_conversion_tracker site_r
                       where site_r."CpId"= page."CpId"
                       and
                       site_r."Date" >= date_trunc('day',(select date from last_modified where type='lastPrecalculatedTrackerCron') - interval '14 day')
                       and
                       site_r."Date" <= (select date from last_modified where type='lastPrecalculatedTrackerCron')
                       group by site_r."Date"::timestamp::date
                       order by site_r."Date"::timestamp::date)))
                from (
                      select
                        "CpId",
                        count(id) as conversions
                      from
                        rtb_conversion_tracker
                      where
                      "Date" >= date_trunc('day',(select date from last_modified where type='lastPrecalculatedTrackerCron') - interval '14 day')
                      and
                      "Date" <= (select date from last_modified where type='lastPrecalculatedTrackerCron')
                      group by
                        "CpId"
                     ) page
                ON CONFLICT (campaign_id)
                  DO UPDATE SET
                     conversions = coalesce(ut.conversions, 0) + coalesce(Excluded.conversions, 0),
                     cvr = case (coalesce(ut.imps, 0) + coalesce(Excluded.imps, 0)) when 0 then 0 else (coalesce(ut.conversions, 0) + coalesce(Excluded.conversions, 0))::float / (coalesce(ut.imps, 0) + coalesce(Excluded.imps, 0)) end,
                     day_chart = case (ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'day')::text when (Excluded.day_chart::json->0->'day')::text
                                  then jsonb_set(
                                    ut.day_chart::jsonb,
                                    concat('{', (jsonb_array_length(ut.day_chart)-1), '}')::text[],
                                    json_build_object(
                                        'day', ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'day',
                                        'imp', coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'imp')::text::integer,0),
                                        'spend', coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'spend')::text::float,0),
                                        'clicks', coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'clicks')::text::integer,0),
                                        'conversions', coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'conversions')::text::integer,0)  + coalesce((Excluded.day_chart::json->0->'conversions')::text::integer,0),
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
                                        """),

        # last 21 days

        migrations.RunSQL("delete from ui_usual_campaigns_grid_data_last_21_days_tracker;"),

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
                    0 as clicks,
                    page.spent,
                    0 as conversions,
                    0,
                    0,
                    case coalesce(page.imps, 0) when 0 then 0 else coalesce(page.spent, 0) / coalesce(page.imps, 0) * 1000.0 end,
                    0,
                    0,
                    0,
                    0,
                    0,
                    array_to_json(array((select
                         json_build_object(
                         'day', site_r."Date"::timestamp::date,
                         'imp', count(site_r."id"),
                         'spend', sum(site_r."PricePaid"),
                         'clicks', 0,
                         'conversions', 0,
                         'cvr', 0,
                         'cpc', 0,
                         'ctr', 0)
                       from
                            rtb_impression_tracker site_r
                       where site_r."CpId"= page."CpId"
                       and
                       site_r."Date" >= date_trunc('day',(select date from last_modified where type='lastPrecalculatedTrackerCron') - interval '21 day')
                       and
                       site_r."Date" <= (select date from last_modified where type='lastPrecalculatedTrackerCron')
                       group by site_r."Date"::timestamp::date
                       order by site_r."Date"::timestamp::date)))
                from (
                      select
                        "CpId",
                        count(id) as imps,
                        sum("PricePaid") as spent
                      from
                        rtb_impression_tracker
                      where
                      "Date" >= date_trunc('day',(select date from last_modified where type='lastPrecalculatedTrackerCron') - interval '21 day')
                      and
                      "Date" <= (select date from last_modified where type='lastPrecalculatedTrackerCron')
                      group by
                        "CpId"
                     ) page;
                                    """),

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
                    0,
                    page.clicks,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    array_to_json(array((select
                         json_build_object(
                         'day', site_r."Date"::timestamp::date,
                         'imp', 0,
                         'mediaspent', 0,
                         'clicks', count(site_r."id"),
                         'conversions', 0,
                         'cpa', 0,
                         'cpc', 0,
                         'ctr', 0)
                       from
                            rtb_click_tracker site_r
                       where site_r."CpId"= page."CpId"
                       and
                       site_r."Date" >= date_trunc('day',(select date from last_modified where type='lastPrecalculatedTrackerCron') - interval '21 day')
                       and
                       site_r."Date" <= (select date from last_modified where type='lastPrecalculatedTrackerCron')
                       group by site_r."Date"::timestamp::date
                       order by site_r."Date"::timestamp::date)))
                from (
                      select
                        "CpId",
                        count(id) as clicks
                      from
                        rtb_click_tracker
                      where
                      "Date" >= date_trunc('day',(select date from last_modified where type='lastPrecalculatedTrackerCron') - interval '21 day')
                      and
                      "Date" <= (select date from last_modified where type='lastPrecalculatedTrackerCron')
                      group by
                        "CpId"
                     ) page
                ON CONFLICT (campaign_id)
                  DO UPDATE SET
                     clicks = coalesce(ut.clicks, 0) + coalesce(Excluded.clicks, 0),
                     ctr = case (coalesce(ut.imps, 0) + coalesce(Excluded.imps, 0)) when 0 then 0 else (coalesce(ut.clicks, 0) + coalesce(Excluded.clicks, 0))::float / (coalesce(ut.imps, 0) + coalesce(Excluded.imps, 0)) end,
                     cpc = case (coalesce(ut.clicks, 0) + coalesce(Excluded.clicks, 0)) when 0 then 0 else (coalesce(ut.spent, 0) + coalesce(Excluded.spent, 0)) / (coalesce(ut.clicks, 0) + coalesce(Excluded.clicks, 0)) end,
                     day_chart = case (ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'day')::text when (Excluded.day_chart::json->0->'day')::text
                                  then jsonb_set(
                                    ut.day_chart::jsonb,
                                    concat('{', (jsonb_array_length(ut.day_chart)-1), '}')::text[],
                                    json_build_object(
                                        'day', ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'day',
                                        'imp', coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'imp')::text::integer,0),
                                        'spend', coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'spend')::text::float,0),
                                        'clicks', coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'clicks')::text::integer,0) + coalesce((Excluded.day_chart::json->0->'clicks')::text::integer,0),
                                        'conversions', coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'conversions')::text::integer,0),
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
                                    """),

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
                    0,
                    0,
                    page.conversions,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    array_to_json(array((select
                         json_build_object(
                         'day', site_r."Date"::timestamp::date,
                         'imp', 0,
                         'mediaspent', 0,
                         'clicks', count(site_r."id"),
                         'conversions', 0,
                         'cpa', 0,
                         'cpc', 0,
                         'ctr', 0)
                       from
                            rtb_conversion_tracker site_r
                       where site_r."CpId"= page."CpId"
                       and
                       site_r."Date" >= date_trunc('day',(select date from last_modified where type='lastPrecalculatedTrackerCron') - interval '21 day')
                       and
                       site_r."Date" <= (select date from last_modified where type='lastPrecalculatedTrackerCron')
                       group by site_r."Date"::timestamp::date
                       order by site_r."Date"::timestamp::date)))
                from (
                      select
                        "CpId",
                        count(id) as conversions
                      from
                        rtb_conversion_tracker
                      where
                      "Date" >= date_trunc('day',(select date from last_modified where type='lastPrecalculatedTrackerCron') - interval '21 day')
                      and
                      "Date" <= (select date from last_modified where type='lastPrecalculatedTrackerCron')
                      group by
                        "CpId"
                     ) page
                ON CONFLICT (campaign_id)
                  DO UPDATE SET
                     conversions = coalesce(ut.conversions, 0) + coalesce(Excluded.conversions, 0),
                     cvr = case (coalesce(ut.imps, 0) + coalesce(Excluded.imps, 0)) when 0 then 0 else (coalesce(ut.conversions, 0) + coalesce(Excluded.conversions, 0))::float / (coalesce(ut.imps, 0) + coalesce(Excluded.imps, 0)) end,
                     day_chart = case (ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'day')::text when (Excluded.day_chart::json->0->'day')::text
                                  then jsonb_set(
                                    ut.day_chart::jsonb,
                                    concat('{', (jsonb_array_length(ut.day_chart)-1), '}')::text[],
                                    json_build_object(
                                        'day', ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'day',
                                        'imp', coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'imp')::text::integer,0),
                                        'spend', coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'spend')::text::float,0),
                                        'clicks', coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'clicks')::text::integer,0),
                                        'conversions', coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'conversions')::text::integer,0)  + coalesce((Excluded.day_chart::json->0->'conversions')::text::integer,0),
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
                                        """),

        # last 90 days

        migrations.RunSQL("delete from ui_usual_campaigns_grid_data_last_90_days_tracker;"),

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
                    0 as clicks,
                    page.spent,
                    0 as conversions,
                    0,
                    0,
                    case coalesce(page.imps, 0) when 0 then 0 else coalesce(page.spent, 0) / coalesce(page.imps, 0) * 1000.0 end,
                    0,
                    0,
                    0,
                    0,
                    0,
                    array_to_json(array((select
                         json_build_object(
                         'day', site_r."Date"::timestamp::date,
                         'imp', count(site_r."id"),
                         'spend', sum(site_r."PricePaid"),
                         'clicks', 0,
                         'conversions', 0,
                         'cvr', 0,
                         'cpc', 0,
                         'ctr', 0)
                       from
                            rtb_impression_tracker site_r
                       where site_r."CpId"= page."CpId"
                       and
                       site_r."Date" >= date_trunc('day',(select date from last_modified where type='lastPrecalculatedTrackerCron') - interval '90 day')
                       and
                       site_r."Date" <= (select date from last_modified where type='lastPrecalculatedTrackerCron')
                       group by site_r."Date"::timestamp::date
                       order by site_r."Date"::timestamp::date)))
                from (
                      select
                        "CpId",
                        count(id) as imps,
                        sum("PricePaid") as spent
                      from
                        rtb_impression_tracker
                      where
                      "Date" >= date_trunc('day',(select date from last_modified where type='lastPrecalculatedTrackerCron') - interval '90 day')
                      and
                      "Date" <= (select date from last_modified where type='lastPrecalculatedTrackerCron')
                      group by
                        "CpId"
                     ) page;
                                    """),

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
                    0,
                    page.clicks,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    array_to_json(array((select
                         json_build_object(
                         'day', site_r."Date"::timestamp::date,
                         'imp', 0,
                         'mediaspent', 0,
                         'clicks', count(site_r."id"),
                         'conversions', 0,
                         'cpa', 0,
                         'cpc', 0,
                         'ctr', 0)
                       from
                            rtb_click_tracker site_r
                       where site_r."CpId"= page."CpId"
                       and
                       site_r."Date" >= date_trunc('day',(select date from last_modified where type='lastPrecalculatedTrackerCron') - interval '90 day')
                       and
                       site_r."Date" <= (select date from last_modified where type='lastPrecalculatedTrackerCron')
                       group by site_r."Date"::timestamp::date
                       order by site_r."Date"::timestamp::date)))
                from (
                      select
                        "CpId",
                        count(id) as clicks
                      from
                        rtb_click_tracker
                      where
                      "Date" >= date_trunc('day',(select date from last_modified where type='lastPrecalculatedTrackerCron') - interval '90 day')
                      and
                      "Date" <= (select date from last_modified where type='lastPrecalculatedTrackerCron')
                      group by
                        "CpId"
                     ) page
                ON CONFLICT (campaign_id)
                  DO UPDATE SET
                     clicks = coalesce(ut.clicks, 0) + coalesce(Excluded.clicks, 0),
                     ctr = case (coalesce(ut.imps, 0) + coalesce(Excluded.imps, 0)) when 0 then 0 else (coalesce(ut.clicks, 0) + coalesce(Excluded.clicks, 0))::float / (coalesce(ut.imps, 0) + coalesce(Excluded.imps, 0)) end,
                     cpc = case (coalesce(ut.clicks, 0) + coalesce(Excluded.clicks, 0)) when 0 then 0 else (coalesce(ut.spent, 0) + coalesce(Excluded.spent, 0)) / (coalesce(ut.clicks, 0) + coalesce(Excluded.clicks, 0)) end,
                     day_chart = case (ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'day')::text when (Excluded.day_chart::json->0->'day')::text
                                  then jsonb_set(
                                    ut.day_chart::jsonb,
                                    concat('{', (jsonb_array_length(ut.day_chart)-1), '}')::text[],
                                    json_build_object(
                                        'day', ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'day',
                                        'imp', coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'imp')::text::integer,0),
                                        'spend', coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'spend')::text::float,0),
                                        'clicks', coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'clicks')::text::integer,0) + coalesce((Excluded.day_chart::json->0->'clicks')::text::integer,0),
                                        'conversions', coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'conversions')::text::integer,0),
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
                                    """),

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
                    0,
                    0,
                    page.conversions,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    array_to_json(array((select
                         json_build_object(
                         'day', site_r."Date"::timestamp::date,
                         'imp', 0,
                         'mediaspent', 0,
                         'clicks', count(site_r."id"),
                         'conversions', 0,
                         'cpa', 0,
                         'cpc', 0,
                         'ctr', 0)
                       from
                            rtb_conversion_tracker site_r
                       where site_r."CpId"= page."CpId"
                       and
                       site_r."Date" >= date_trunc('day',(select date from last_modified where type='lastPrecalculatedTrackerCron') - interval '90 day')
                       and
                       site_r."Date" <= (select date from last_modified where type='lastPrecalculatedTrackerCron')
                       group by site_r."Date"::timestamp::date
                       order by site_r."Date"::timestamp::date)))
                from (
                      select
                        "CpId",
                        count(id) as conversions
                      from
                        rtb_conversion_tracker
                      where
                      "Date" >= date_trunc('day',(select date from last_modified where type='lastPrecalculatedTrackerCron') - interval '90 day')
                      and
                      "Date" <= (select date from last_modified where type='lastPrecalculatedTrackerCron')
                      group by
                        "CpId"
                     ) page
                ON CONFLICT (campaign_id)
                  DO UPDATE SET
                     conversions = coalesce(ut.conversions, 0) + coalesce(Excluded.conversions, 0),
                     cvr = case (coalesce(ut.imps, 0) + coalesce(Excluded.imps, 0)) when 0 then 0 else (coalesce(ut.conversions, 0) + coalesce(Excluded.conversions, 0))::float / (coalesce(ut.imps, 0) + coalesce(Excluded.imps, 0)) end,
                     day_chart = case (ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'day')::text when (Excluded.day_chart::json->0->'day')::text
                                  then jsonb_set(
                                    ut.day_chart::jsonb,
                                    concat('{', (jsonb_array_length(ut.day_chart)-1), '}')::text[],
                                    json_build_object(
                                        'day', ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'day',
                                        'imp', coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'imp')::text::integer,0),
                                        'spend', coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'spend')::text::float,0),
                                        'clicks', coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'clicks')::text::integer,0),
                                        'conversions', coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'conversions')::text::integer,0)  + coalesce((Excluded.day_chart::json->0->'conversions')::text::integer,0),
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
                                        """),

        # last month

        migrations.RunSQL("delete from ui_usual_campaigns_grid_data_last_month_tracker;"),

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
                        0 as clicks,
                        page.spent,
                        0 as conversions,
                        0,
                        0,
                        case coalesce(page.imps, 0) when 0 then 0 else coalesce(page.spent, 0) / coalesce(page.imps, 0) * 1000.0 end,
                        0,
                        0,
                        0,
                        0,
                        0,
                        array_to_json(array((select
                             json_build_object(
                             'day', site_r."Date"::timestamp::date,
                             'imp', count(site_r."id"),
                             'spend', sum(site_r."PricePaid"),
                             'clicks', 0,
                             'conversions', 0,
                             'cvr', 0,
                             'cpc', 0,
                             'ctr', 0)
                           from
                                rtb_impression_tracker site_r
                           where site_r."CpId"= page."CpId"
                           and
                           site_r."Date" >= date_trunc('month',(select date from last_modified where type='lastPrecalculatedTrackerCron') - interval '1 month')
                           and
                           site_r."Date" < date_trunc('month',(select date from last_modified where type='lastPrecalculatedTrackerCron'))
                           group by site_r."Date"::timestamp::date
                           order by site_r."Date"::timestamp::date)))
                    from (
                          select
                            "CpId",
                            count(id) as imps,
                            sum("PricePaid") as spent
                          from
                            rtb_impression_tracker
                          where
                          "Date" >= date_trunc('month',(select date from last_modified where type='lastPrecalculatedTrackerCron') - interval '1 month')
                          and
                          "Date" < date_trunc('month',(select date from last_modified where type='lastPrecalculatedTrackerCron'))
                          group by
                            "CpId"
                         ) page;
                                        """),

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
                        0,
                        page.clicks,
                        0,
                        0,
                        0,
                        0,
                        0,
                        0,
                        0,
                        0,
                        0,
                        0,
                        array_to_json(array((select
                             json_build_object(
                             'day', site_r."Date"::timestamp::date,
                             'imp', 0,
                             'mediaspent', 0,
                             'clicks', count(site_r."id"),
                             'conversions', 0,
                             'cpa', 0,
                             'cpc', 0,
                             'ctr', 0)
                           from
                                rtb_click_tracker site_r
                           where site_r."CpId"= page."CpId"
                           and
                           site_r."Date" >= date_trunc('month',(select date from last_modified where type='lastPrecalculatedTrackerCron') - interval '1 month')
                           and
                           site_r."Date" < date_trunc('month',(select date from last_modified where type='lastPrecalculatedTrackerCron'))
                           group by site_r."Date"::timestamp::date
                           order by site_r."Date"::timestamp::date)))
                    from (
                          select
                            "CpId",
                            count(id) as clicks
                          from
                            rtb_click_tracker
                          where
                          "Date" >= date_trunc('month',(select date from last_modified where type='lastPrecalculatedTrackerCron') - interval '1 month')
                          and
                          "Date" < date_trunc('month',(select date from last_modified where type='lastPrecalculatedTrackerCron'))
                          group by
                            "CpId"
                         ) page
                    ON CONFLICT (campaign_id)
                      DO UPDATE SET
                         clicks = coalesce(ut.clicks, 0) + coalesce(Excluded.clicks, 0),
                         ctr = case (coalesce(ut.imps, 0) + coalesce(Excluded.imps, 0)) when 0 then 0 else (coalesce(ut.clicks, 0) + coalesce(Excluded.clicks, 0))::float / (coalesce(ut.imps, 0) + coalesce(Excluded.imps, 0)) end,
                         cpc = case (coalesce(ut.clicks, 0) + coalesce(Excluded.clicks, 0)) when 0 then 0 else (coalesce(ut.spent, 0) + coalesce(Excluded.spent, 0)) / (coalesce(ut.clicks, 0) + coalesce(Excluded.clicks, 0)) end,
                         day_chart = case (ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'day')::text when (Excluded.day_chart::json->0->'day')::text
                                      then jsonb_set(
                                        ut.day_chart::jsonb,
                                        concat('{', (jsonb_array_length(ut.day_chart)-1), '}')::text[],
                                        json_build_object(
                                            'day', ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'day',
                                            'imp', coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'imp')::text::integer,0),
                                            'spend', coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'spend')::text::float,0),
                                            'clicks', coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'clicks')::text::integer,0) + coalesce((Excluded.day_chart::json->0->'clicks')::text::integer,0),
                                            'conversions', coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'conversions')::text::integer,0),
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
                                        """),

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
                        0,
                        0,
                        page.conversions,
                        0,
                        0,
                        0,
                        0,
                        0,
                        0,
                        0,
                        0,
                        0,
                        array_to_json(array((select
                             json_build_object(
                             'day', site_r."Date"::timestamp::date,
                             'imp', 0,
                             'mediaspent', 0,
                             'clicks', count(site_r."id"),
                             'conversions', 0,
                             'cpa', 0,
                             'cpc', 0,
                             'ctr', 0)
                           from
                                rtb_conversion_tracker site_r
                           where site_r."CpId"= page."CpId"
                           and
                           site_r."Date" >= date_trunc('month',(select date from last_modified where type='lastPrecalculatedTrackerCron') - interval '1 month')
                           and
                           site_r."Date" < date_trunc('month',(select date from last_modified where type='lastPrecalculatedTrackerCron'))
                           group by site_r."Date"::timestamp::date
                           order by site_r."Date"::timestamp::date)))
                    from (
                          select
                            "CpId",
                            count(id) as conversions
                          from
                            rtb_conversion_tracker
                          where
                          "Date" >= date_trunc('month',(select date from last_modified where type='lastPrecalculatedTrackerCron') - interval '1 month')
                          and
                          "Date" < date_trunc('month',(select date from last_modified where type='lastPrecalculatedTrackerCron'))
                          group by
                            "CpId"
                         ) page
                    ON CONFLICT (campaign_id)
                      DO UPDATE SET
                         conversions = coalesce(ut.conversions, 0) + coalesce(Excluded.conversions, 0),
                         cvr = case (coalesce(ut.imps, 0) + coalesce(Excluded.imps, 0)) when 0 then 0 else (coalesce(ut.conversions, 0) + coalesce(Excluded.conversions, 0))::float / (coalesce(ut.imps, 0) + coalesce(Excluded.imps, 0)) end,
                         day_chart = case (ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'day')::text when (Excluded.day_chart::json->0->'day')::text
                                      then jsonb_set(
                                        ut.day_chart::jsonb,
                                        concat('{', (jsonb_array_length(ut.day_chart)-1), '}')::text[],
                                        json_build_object(
                                            'day', ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'day',
                                            'imp', coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'imp')::text::integer,0),
                                            'spend', coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'spend')::text::float,0),
                                            'clicks', coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'clicks')::text::integer,0),
                                            'conversions', coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'conversions')::text::integer,0)  + coalesce((Excluded.day_chart::json->0->'conversions')::text::integer,0),
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
                                            """),

        # cur month

        migrations.RunSQL("delete from ui_usual_campaigns_grid_data_cur_month_tracker;"),

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
                        0 as clicks,
                        page.spent,
                        0 as conversions,
                        0,
                        0,
                        case coalesce(page.imps, 0) when 0 then 0 else coalesce(page.spent, 0) / coalesce(page.imps, 0) * 1000.0 end,
                        0,
                        0,
                        0,
                        0,
                        0,
                        array_to_json(array((select
                             json_build_object(
                             'day', site_r."Date"::timestamp::date,
                             'imp', count(site_r."id"),
                             'spend', sum(site_r."PricePaid"),
                             'clicks', 0,
                             'conversions', 0,
                             'cvr', 0,
                             'cpc', 0,
                             'ctr', 0)
                           from
                                rtb_impression_tracker site_r
                           where site_r."CpId"= page."CpId"
                           and
                           site_r."Date" >= date_trunc('month',(select date from last_modified where type='lastPrecalculatedTrackerCron'))
                           and
                           site_r."Date" <= (select date from last_modified where type='lastPrecalculatedTrackerCron')
                           group by site_r."Date"::timestamp::date
                           order by site_r."Date"::timestamp::date)))
                    from (
                          select
                            "CpId",
                            count(id) as imps,
                            sum("PricePaid") as spent
                          from
                            rtb_impression_tracker
                          where
                          "Date" >= date_trunc('month',(select date from last_modified where type='lastPrecalculatedTrackerCron'))
                          and
                          "Date" <= (select date from last_modified where type='lastPrecalculatedTrackerCron')
                          group by
                            "CpId"
                         ) page;
                                        """),

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
                        0,
                        page.clicks,
                        0,
                        0,
                        0,
                        0,
                        0,
                        0,
                        0,
                        0,
                        0,
                        0,
                        array_to_json(array((select
                             json_build_object(
                             'day', site_r."Date"::timestamp::date,
                             'imp', 0,
                             'mediaspent', 0,
                             'clicks', count(site_r."id"),
                             'conversions', 0,
                             'cpa', 0,
                             'cpc', 0,
                             'ctr', 0)
                           from
                                rtb_click_tracker site_r
                           where site_r."CpId"= page."CpId"
                           and
                           site_r."Date" >= date_trunc('month',(select date from last_modified where type='lastPrecalculatedTrackerCron'))
                           and
                           site_r."Date" <= (select date from last_modified where type='lastPrecalculatedTrackerCron')
                           group by site_r."Date"::timestamp::date
                           order by site_r."Date"::timestamp::date)))
                    from (
                          select
                            "CpId",
                            count(id) as clicks
                          from
                            rtb_click_tracker
                          where
                          "Date" >= date_trunc('month',(select date from last_modified where type='lastPrecalculatedTrackerCron'))
                          and
                          "Date" <= (select date from last_modified where type='lastPrecalculatedTrackerCron')
                          group by
                            "CpId"
                         ) page
                    ON CONFLICT (campaign_id)
                      DO UPDATE SET
                         clicks = coalesce(ut.clicks, 0) + coalesce(Excluded.clicks, 0),
                         ctr = case (coalesce(ut.imps, 0) + coalesce(Excluded.imps, 0)) when 0 then 0 else (coalesce(ut.clicks, 0) + coalesce(Excluded.clicks, 0))::float / (coalesce(ut.imps, 0) + coalesce(Excluded.imps, 0)) end,
                         cpc = case (coalesce(ut.clicks, 0) + coalesce(Excluded.clicks, 0)) when 0 then 0 else (coalesce(ut.spent, 0) + coalesce(Excluded.spent, 0)) / (coalesce(ut.clicks, 0) + coalesce(Excluded.clicks, 0)) end,
                         day_chart = case (ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'day')::text when (Excluded.day_chart::json->0->'day')::text
                                      then jsonb_set(
                                        ut.day_chart::jsonb,
                                        concat('{', (jsonb_array_length(ut.day_chart)-1), '}')::text[],
                                        json_build_object(
                                            'day', ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'day',
                                            'imp', coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'imp')::text::integer,0),
                                            'spend', coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'spend')::text::float,0),
                                            'clicks', coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'clicks')::text::integer,0) + coalesce((Excluded.day_chart::json->0->'clicks')::text::integer,0),
                                            'conversions', coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'conversions')::text::integer,0),
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
                                        """),

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
                        0,
                        0,
                        page.conversions,
                        0,
                        0,
                        0,
                        0,
                        0,
                        0,
                        0,
                        0,
                        0,
                        array_to_json(array((select
                             json_build_object(
                             'day', site_r."Date"::timestamp::date,
                             'imp', 0,
                             'mediaspent', 0,
                             'clicks', count(site_r."id"),
                             'conversions', 0,
                             'cpa', 0,
                             'cpc', 0,
                             'ctr', 0)
                           from
                                rtb_conversion_tracker site_r
                           where site_r."CpId"= page."CpId"
                           and
                           site_r."Date" >= date_trunc('month',(select date from last_modified where type='lastPrecalculatedTrackerCron'))
                           and
                           site_r."Date" <= (select date from last_modified where type='lastPrecalculatedTrackerCron')
                           group by site_r."Date"::timestamp::date
                           order by site_r."Date"::timestamp::date)))
                    from (
                          select
                            "CpId",
                            count(id) as conversions
                          from
                            rtb_conversion_tracker
                          where
                          "Date" >= date_trunc('month',(select date from last_modified where type='lastPrecalculatedTrackerCron'))
                          and
                          "Date" <= (select date from last_modified where type='lastPrecalculatedTrackerCron')
                          group by
                            "CpId"
                         ) page
                    ON CONFLICT (campaign_id)
                      DO UPDATE SET
                         conversions = coalesce(ut.conversions, 0) + coalesce(Excluded.conversions, 0),
                         cvr = case (coalesce(ut.imps, 0) + coalesce(Excluded.imps, 0)) when 0 then 0 else (coalesce(ut.conversions, 0) + coalesce(Excluded.conversions, 0))::float / (coalesce(ut.imps, 0) + coalesce(Excluded.imps, 0)) end,
                         day_chart = case (ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'day')::text when (Excluded.day_chart::json->0->'day')::text
                                      then jsonb_set(
                                        ut.day_chart::jsonb,
                                        concat('{', (jsonb_array_length(ut.day_chart)-1), '}')::text[],
                                        json_build_object(
                                            'day', ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'day',
                                            'imp', coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'imp')::text::integer,0),
                                            'spend', coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'spend')::text::float,0),
                                            'clicks', coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'clicks')::text::integer,0),
                                            'conversions', coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'conversions')::text::integer,0)  + coalesce((Excluded.day_chart::json->0->'conversions')::text::integer,0),
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
                                            """),

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
         'imp', count(site_r."id"),
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
         'imp', 0,
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
                        'imp', coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'imp')::text::integer,0),
                        'mediaspent', coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'mediaspent')::text::float,0),
                        'clicks', coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'clicks')::text::integer,0) + coalesce((Excluded.day_chart::json->0->'clicks')::text::integer,0),
                        'conversions', coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'conversions')::text::integer,0),
                        'cpa', case (coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'conversions')::text::integer,0) + coalesce((Excluded.day_chart::json->0->'conversions')::text::integer,0))
                               when 0 then 0
                               else (coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'mediaspent')::text::float,0) + coalesce((Excluded.day_chart::json->0->'mediaspent')::text::float,0))/(coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'conversions')::text::float,0) + coalesce((Excluded.day_chart::json->0->'conversions')::text::float,0)) end,
                        'cpc', case (coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'clicks')::text::integer,0) + coalesce((Excluded.day_chart::json->0->'clicks')::text::integer,0))
                               when 0 then 0
                               else (coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'mediaspent')::text::float,0) + coalesce((Excluded.day_chart::json->0->'mediaspent')::text::float,0))/(coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'clicks')::text::float,0) + coalesce((Excluded.day_chart::json->0->'clicks')::text::float,0)) end,
                        'ctr', case coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'imp')::text::integer,0) + coalesce((Excluded.day_chart::json->0->'imp')::text::integer,0)
                               when 0 then 0
                               else (coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'clicks')::text::float,0) + coalesce((Excluded.day_chart::json->0->'clicks')::text::float,0))/(coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'imp')::text::float,0) + coalesce((Excluded.day_chart::json->0->'imp')::text::float,0)) end
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
         'imp', 0,
         'spend', 0,
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
                        'imp', coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'imp')::text::integer,0),
                        'mediaspent', coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'mediaspent')::text::float,0),
                        'clicks', coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'clicks')::text::integer,0),
                        'conversions', coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'conversions')::text::integer,0) + coalesce((Excluded.day_chart::json->0->'conversions')::text::integer,0),
                        'cpa', case (coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'conversions')::text::integer,0) + coalesce((Excluded.day_chart::json->0->'conversions')::text::integer,0))
                               when 0 then 0
                               else (coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'mediaspent')::text::float,0) + coalesce((Excluded.day_chart::json->0->'mediaspent')::text::float,0))/(coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'conversions')::text::float,0) + coalesce((Excluded.day_chart::json->0->'conversions')::text::float,0)) end,
                        'cpc', case (coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'clicks')::text::integer,0) + coalesce((Excluded.day_chart::json->0->'clicks')::text::integer,0))
                               when 0 then 0
                               else (coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'mediaspent')::text::float,0) + coalesce((Excluded.day_chart::json->0->'mediaspent')::text::float,0))/(coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'clicks')::text::float,0) + coalesce((Excluded.day_chart::json->0->'clicks')::text::float,0)) end,
                        'ctr', case coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'imp')::text::integer,0) + coalesce((Excluded.day_chart::json->0->'imp')::text::integer,0)
                               when 0 then 0
                               else (coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'clicks')::text::float,0) + coalesce((Excluded.day_chart::json->0->'clicks')::text::float,0))/(coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'imp')::text::float,0) + coalesce((Excluded.day_chart::json->0->'imp')::text::float,0)) end
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
             'imp', count(site_r."id"),
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
             'imp', 0,
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
                            'imp', coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'imp')::text::integer,0),
                            'mediaspent', coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'mediaspent')::text::float,0),
                            'clicks', coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'clicks')::text::integer,0) + coalesce((Excluded.day_chart::json->0->'clicks')::text::integer,0),
                            'conversions', coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'conversions')::text::integer,0),
                            'cpa', case (coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'conversions')::text::integer,0) + coalesce((Excluded.day_chart::json->0->'conversions')::text::integer,0))
                                   when 0 then 0
                                   else (coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'mediaspent')::text::float,0) + coalesce((Excluded.day_chart::json->0->'mediaspent')::text::float,0))/(coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'conversions')::text::float,0) + coalesce((Excluded.day_chart::json->0->'conversions')::text::float,0)) end,
                            'cpc', case (coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'clicks')::text::integer,0) + coalesce((Excluded.day_chart::json->0->'clicks')::text::integer,0))
                                   when 0 then 0
                                   else (coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'mediaspent')::text::float,0) + coalesce((Excluded.day_chart::json->0->'mediaspent')::text::float,0))/(coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'clicks')::text::float,0) + coalesce((Excluded.day_chart::json->0->'clicks')::text::float,0)) end,
                            'ctr', case coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'imp')::text::integer,0) + coalesce((Excluded.day_chart::json->0->'imp')::text::integer,0)
                                   when 0 then 0
                                   else (coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'clicks')::text::float,0) + coalesce((Excluded.day_chart::json->0->'clicks')::text::float,0))/(coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'imp')::text::float,0) + coalesce((Excluded.day_chart::json->0->'imp')::text::float,0)) end
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
             'imp', 0,
             'spend', 0,
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
                            'imp', coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'imp')::text::integer,0),
                            'mediaspent', coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'mediaspent')::text::float,0),
                            'clicks', coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'clicks')::text::integer,0),
                            'conversions', coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'conversions')::text::integer,0) + coalesce((Excluded.day_chart::json->0->'conversions')::text::integer,0),
                            'cpa', case (coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'conversions')::text::integer,0) + coalesce((Excluded.day_chart::json->0->'conversions')::text::integer,0))
                                   when 0 then 0
                                   else (coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'mediaspent')::text::float,0) + coalesce((Excluded.day_chart::json->0->'mediaspent')::text::float,0))/(coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'conversions')::text::float,0) + coalesce((Excluded.day_chart::json->0->'conversions')::text::float,0)) end,
                            'cpc', case (coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'clicks')::text::integer,0) + coalesce((Excluded.day_chart::json->0->'clicks')::text::integer,0))
                                   when 0 then 0
                                   else (coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'mediaspent')::text::float,0) + coalesce((Excluded.day_chart::json->0->'mediaspent')::text::float,0))/(coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'clicks')::text::float,0) + coalesce((Excluded.day_chart::json->0->'clicks')::text::float,0)) end,
                            'ctr', case coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'imp')::text::integer,0) + coalesce((Excluded.day_chart::json->0->'imp')::text::integer,0)
                                   when 0 then 0
                                   else (coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'clicks')::text::float,0) + coalesce((Excluded.day_chart::json->0->'clicks')::text::float,0))/(coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'imp')::text::float,0) + coalesce((Excluded.day_chart::json->0->'imp')::text::float,0)) end
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
                 'imp', count(site_r."id"),
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
                 'imp', 0,
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
                                'imp', coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'imp')::text::integer,0),
                                'mediaspent', coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'mediaspent')::text::float,0),
                                'clicks', coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'clicks')::text::integer,0) + coalesce((Excluded.day_chart::json->0->'clicks')::text::integer,0),
                                'conversions', coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'conversions')::text::integer,0),
                                'cpa', case (coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'conversions')::text::integer,0) + coalesce((Excluded.day_chart::json->0->'conversions')::text::integer,0))
                                       when 0 then 0
                                       else (coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'mediaspent')::text::float,0) + coalesce((Excluded.day_chart::json->0->'mediaspent')::text::float,0))/(coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'conversions')::text::float,0) + coalesce((Excluded.day_chart::json->0->'conversions')::text::float,0)) end,
                                'cpc', case (coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'clicks')::text::integer,0) + coalesce((Excluded.day_chart::json->0->'clicks')::text::integer,0))
                                       when 0 then 0
                                       else (coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'mediaspent')::text::float,0) + coalesce((Excluded.day_chart::json->0->'mediaspent')::text::float,0))/(coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'clicks')::text::float,0) + coalesce((Excluded.day_chart::json->0->'clicks')::text::float,0)) end,
                                'ctr', case coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'imp')::text::integer,0) + coalesce((Excluded.day_chart::json->0->'imp')::text::integer,0)
                                       when 0 then 0
                                       else (coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'clicks')::text::float,0) + coalesce((Excluded.day_chart::json->0->'clicks')::text::float,0))/(coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'imp')::text::float,0) + coalesce((Excluded.day_chart::json->0->'imp')::text::float,0)) end
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
                 'imp', 0,
                 'spend', 0,
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
                                'imp', coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'imp')::text::integer,0),
                                'mediaspent', coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'mediaspent')::text::float,0),
                                'clicks', coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'clicks')::text::integer,0),
                                'conversions', coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'conversions')::text::integer,0) + coalesce((Excluded.day_chart::json->0->'conversions')::text::integer,0),
                                'cpa', case (coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'conversions')::text::integer,0) + coalesce((Excluded.day_chart::json->0->'conversions')::text::integer,0))
                                       when 0 then 0
                                       else (coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'mediaspent')::text::float,0) + coalesce((Excluded.day_chart::json->0->'mediaspent')::text::float,0))/(coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'conversions')::text::float,0) + coalesce((Excluded.day_chart::json->0->'conversions')::text::float,0)) end,
                                'cpc', case (coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'clicks')::text::integer,0) + coalesce((Excluded.day_chart::json->0->'clicks')::text::integer,0))
                                       when 0 then 0
                                       else (coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'mediaspent')::text::float,0) + coalesce((Excluded.day_chart::json->0->'mediaspent')::text::float,0))/(coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'clicks')::text::float,0) + coalesce((Excluded.day_chart::json->0->'clicks')::text::float,0)) end,
                                'ctr', case coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'imp')::text::integer,0) + coalesce((Excluded.day_chart::json->0->'imp')::text::integer,0)
                                       when 0 then 0
                                       else (coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'clicks')::text::float,0) + coalesce((Excluded.day_chart::json->0->'clicks')::text::float,0))/(coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'imp')::text::float,0) + coalesce((Excluded.day_chart::json->0->'imp')::text::float,0)) end
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
                     'imp', count(site_r."id"),
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
                     'imp', 0,
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
                                    'imp', coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'imp')::text::integer,0),
                                    'mediaspent', coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'mediaspent')::text::float,0),
                                    'clicks', coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'clicks')::text::integer,0) + coalesce((Excluded.day_chart::json->0->'clicks')::text::integer,0),
                                    'conversions', coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'conversions')::text::integer,0),
                                    'cpa', case (coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'conversions')::text::integer,0) + coalesce((Excluded.day_chart::json->0->'conversions')::text::integer,0))
                                           when 0 then 0
                                           else (coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'mediaspent')::text::float,0) + coalesce((Excluded.day_chart::json->0->'mediaspent')::text::float,0))/(coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'conversions')::text::float,0) + coalesce((Excluded.day_chart::json->0->'conversions')::text::float,0)) end,
                                    'cpc', case (coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'clicks')::text::integer,0) + coalesce((Excluded.day_chart::json->0->'clicks')::text::integer,0))
                                           when 0 then 0
                                           else (coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'mediaspent')::text::float,0) + coalesce((Excluded.day_chart::json->0->'mediaspent')::text::float,0))/(coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'clicks')::text::float,0) + coalesce((Excluded.day_chart::json->0->'clicks')::text::float,0)) end,
                                    'ctr', case coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'imp')::text::integer,0) + coalesce((Excluded.day_chart::json->0->'imp')::text::integer,0)
                                           when 0 then 0
                                           else (coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'clicks')::text::float,0) + coalesce((Excluded.day_chart::json->0->'clicks')::text::float,0))/(coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'imp')::text::float,0) + coalesce((Excluded.day_chart::json->0->'imp')::text::float,0)) end
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
                     'imp', 0,
                     'spend', 0,
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
                                    'imp', coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'imp')::text::integer,0),
                                    'mediaspent', coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'mediaspent')::text::float,0),
                                    'clicks', coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'clicks')::text::integer,0),
                                    'conversions', coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'conversions')::text::integer,0) + coalesce((Excluded.day_chart::json->0->'conversions')::text::integer,0),
                                    'cpa', case (coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'conversions')::text::integer,0) + coalesce((Excluded.day_chart::json->0->'conversions')::text::integer,0))
                                           when 0 then 0
                                           else (coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'mediaspent')::text::float,0) + coalesce((Excluded.day_chart::json->0->'mediaspent')::text::float,0))/(coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'conversions')::text::float,0) + coalesce((Excluded.day_chart::json->0->'conversions')::text::float,0)) end,
                                    'cpc', case (coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'clicks')::text::integer,0) + coalesce((Excluded.day_chart::json->0->'clicks')::text::integer,0))
                                           when 0 then 0
                                           else (coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'mediaspent')::text::float,0) + coalesce((Excluded.day_chart::json->0->'mediaspent')::text::float,0))/(coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'clicks')::text::float,0) + coalesce((Excluded.day_chart::json->0->'clicks')::text::float,0)) end,
                                    'ctr', case coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'imp')::text::integer,0) + coalesce((Excluded.day_chart::json->0->'imp')::text::integer,0)
                                           when 0 then 0
                                           else (coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'clicks')::text::float,0) + coalesce((Excluded.day_chart::json->0->'clicks')::text::float,0))/(coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'imp')::text::float,0) + coalesce((Excluded.day_chart::json->0->'imp')::text::float,0)) end
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
                     'imp', count(site_r."id"),
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
                     'imp', 0,
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
                                    'imp', coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'imp')::text::integer,0),
                                    'mediaspent', coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'mediaspent')::text::float,0),
                                    'clicks', coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'clicks')::text::integer,0) + coalesce((Excluded.day_chart::json->0->'clicks')::text::integer,0),
                                    'conversions', coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'conversions')::text::integer,0),
                                    'cpa', case (coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'conversions')::text::integer,0) + coalesce((Excluded.day_chart::json->0->'conversions')::text::integer,0))
                                           when 0 then 0
                                           else (coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'mediaspent')::text::float,0) + coalesce((Excluded.day_chart::json->0->'mediaspent')::text::float,0))/(coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'conversions')::text::float,0) + coalesce((Excluded.day_chart::json->0->'conversions')::text::float,0)) end,
                                    'cpc', case (coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'clicks')::text::integer,0) + coalesce((Excluded.day_chart::json->0->'clicks')::text::integer,0))
                                           when 0 then 0
                                           else (coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'mediaspent')::text::float,0) + coalesce((Excluded.day_chart::json->0->'mediaspent')::text::float,0))/(coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'clicks')::text::float,0) + coalesce((Excluded.day_chart::json->0->'clicks')::text::float,0)) end,
                                    'ctr', case coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'imp')::text::integer,0) + coalesce((Excluded.day_chart::json->0->'imp')::text::integer,0)
                                           when 0 then 0
                                           else (coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'clicks')::text::float,0) + coalesce((Excluded.day_chart::json->0->'clicks')::text::float,0))/(coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'imp')::text::float,0) + coalesce((Excluded.day_chart::json->0->'imp')::text::float,0)) end
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
                     'imp', 0,
                     'spend', 0,
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
                                    'imp', coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'imp')::text::integer,0),
                                    'mediaspent', coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'mediaspent')::text::float,0),
                                    'clicks', coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'clicks')::text::integer,0),
                                    'conversions', coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'conversions')::text::integer,0) + coalesce((Excluded.day_chart::json->0->'conversions')::text::integer,0),
                                    'cpa', case (coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'conversions')::text::integer,0) + coalesce((Excluded.day_chart::json->0->'conversions')::text::integer,0))
                                           when 0 then 0
                                           else (coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'mediaspent')::text::float,0) + coalesce((Excluded.day_chart::json->0->'mediaspent')::text::float,0))/(coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'conversions')::text::float,0) + coalesce((Excluded.day_chart::json->0->'conversions')::text::float,0)) end,
                                    'cpc', case (coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'clicks')::text::integer,0) + coalesce((Excluded.day_chart::json->0->'clicks')::text::integer,0))
                                           when 0 then 0
                                           else (coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'mediaspent')::text::float,0) + coalesce((Excluded.day_chart::json->0->'mediaspent')::text::float,0))/(coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'clicks')::text::float,0) + coalesce((Excluded.day_chart::json->0->'clicks')::text::float,0)) end,
                                    'ctr', case coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'imp')::text::integer,0) + coalesce((Excluded.day_chart::json->0->'imp')::text::integer,0)
                                           when 0 then 0
                                           else (coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'clicks')::text::float,0) + coalesce((Excluded.day_chart::json->0->'clicks')::text::float,0))/(coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'imp')::text::float,0) + coalesce((Excluded.day_chart::json->0->'imp')::text::float,0)) end
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
                     'imp', count(site_r."id"),
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
                     'imp', 0,
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
                                    'imp', coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'imp')::text::integer,0),
                                    'mediaspent', coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'mediaspent')::text::float,0),
                                    'clicks', coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'clicks')::text::integer,0) + coalesce((Excluded.day_chart::json->0->'clicks')::text::integer,0),
                                    'conversions', coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'conversions')::text::integer,0),
                                    'cpa', case (coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'conversions')::text::integer,0) + coalesce((Excluded.day_chart::json->0->'conversions')::text::integer,0))
                                           when 0 then 0
                                           else (coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'mediaspent')::text::float,0) + coalesce((Excluded.day_chart::json->0->'mediaspent')::text::float,0))/(coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'conversions')::text::float,0) + coalesce((Excluded.day_chart::json->0->'conversions')::text::float,0)) end,
                                    'cpc', case (coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'clicks')::text::integer,0) + coalesce((Excluded.day_chart::json->0->'clicks')::text::integer,0))
                                           when 0 then 0
                                           else (coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'mediaspent')::text::float,0) + coalesce((Excluded.day_chart::json->0->'mediaspent')::text::float,0))/(coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'clicks')::text::float,0) + coalesce((Excluded.day_chart::json->0->'clicks')::text::float,0)) end,
                                    'ctr', case coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'imp')::text::integer,0) + coalesce((Excluded.day_chart::json->0->'imp')::text::integer,0)
                                           when 0 then 0
                                           else (coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'clicks')::text::float,0) + coalesce((Excluded.day_chart::json->0->'clicks')::text::float,0))/(coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'imp')::text::float,0) + coalesce((Excluded.day_chart::json->0->'imp')::text::float,0)) end
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
                     'imp', 0,
                     'spend', 0,
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
                                    'imp', coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'imp')::text::integer,0),
                                    'mediaspent', coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'mediaspent')::text::float,0),
                                    'clicks', coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'clicks')::text::integer,0),
                                    'conversions', coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'conversions')::text::integer,0) + coalesce((Excluded.day_chart::json->0->'conversions')::text::integer,0),
                                    'cpa', case (coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'conversions')::text::integer,0) + coalesce((Excluded.day_chart::json->0->'conversions')::text::integer,0))
                                           when 0 then 0
                                           else (coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'mediaspent')::text::float,0) + coalesce((Excluded.day_chart::json->0->'mediaspent')::text::float,0))/(coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'conversions')::text::float,0) + coalesce((Excluded.day_chart::json->0->'conversions')::text::float,0)) end,
                                    'cpc', case (coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'clicks')::text::integer,0) + coalesce((Excluded.day_chart::json->0->'clicks')::text::integer,0))
                                           when 0 then 0
                                           else (coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'mediaspent')::text::float,0) + coalesce((Excluded.day_chart::json->0->'mediaspent')::text::float,0))/(coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'clicks')::text::float,0) + coalesce((Excluded.day_chart::json->0->'clicks')::text::float,0)) end,
                                    'ctr', case coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'imp')::text::integer,0) + coalesce((Excluded.day_chart::json->0->'imp')::text::integer,0)
                                           when 0 then 0
                                           else (coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'clicks')::text::float,0) + coalesce((Excluded.day_chart::json->0->'clicks')::text::float,0))/(coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'imp')::text::float,0) + coalesce((Excluded.day_chart::json->0->'imp')::text::float,0)) end
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
                     'imp', count(site_r."id"),
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
                     'imp', 0,
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
                                    'imp', coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'imp')::text::integer,0),
                                    'mediaspent', coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'mediaspent')::text::float,0),
                                    'clicks', coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'clicks')::text::integer,0) + coalesce((Excluded.day_chart::json->0->'clicks')::text::integer,0),
                                    'conversions', coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'conversions')::text::integer,0),
                                    'cpa', case (coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'conversions')::text::integer,0) + coalesce((Excluded.day_chart::json->0->'conversions')::text::integer,0))
                                           when 0 then 0
                                           else (coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'mediaspent')::text::float,0) + coalesce((Excluded.day_chart::json->0->'mediaspent')::text::float,0))/(coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'conversions')::text::float,0) + coalesce((Excluded.day_chart::json->0->'conversions')::text::float,0)) end,
                                    'cpc', case (coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'clicks')::text::integer,0) + coalesce((Excluded.day_chart::json->0->'clicks')::text::integer,0))
                                           when 0 then 0
                                           else (coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'mediaspent')::text::float,0) + coalesce((Excluded.day_chart::json->0->'mediaspent')::text::float,0))/(coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'clicks')::text::float,0) + coalesce((Excluded.day_chart::json->0->'clicks')::text::float,0)) end,
                                    'ctr', case coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'imp')::text::integer,0) + coalesce((Excluded.day_chart::json->0->'imp')::text::integer,0)
                                           when 0 then 0
                                           else (coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'clicks')::text::float,0) + coalesce((Excluded.day_chart::json->0->'clicks')::text::float,0))/(coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'imp')::text::float,0) + coalesce((Excluded.day_chart::json->0->'imp')::text::float,0)) end
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
                     'imp', 0,
                     'spend', 0,
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
                                    'imp', coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'imp')::text::integer,0),
                                    'mediaspent', coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'mediaspent')::text::float,0),
                                    'clicks', coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'clicks')::text::integer,0),
                                    'conversions', coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'conversions')::text::integer,0) + coalesce((Excluded.day_chart::json->0->'conversions')::text::integer,0),
                                    'cpa', case (coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'conversions')::text::integer,0) + coalesce((Excluded.day_chart::json->0->'conversions')::text::integer,0))
                                           when 0 then 0
                                           else (coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'mediaspent')::text::float,0) + coalesce((Excluded.day_chart::json->0->'mediaspent')::text::float,0))/(coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'conversions')::text::float,0) + coalesce((Excluded.day_chart::json->0->'conversions')::text::float,0)) end,
                                    'cpc', case (coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'clicks')::text::integer,0) + coalesce((Excluded.day_chart::json->0->'clicks')::text::integer,0))
                                           when 0 then 0
                                           else (coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'mediaspent')::text::float,0) + coalesce((Excluded.day_chart::json->0->'mediaspent')::text::float,0))/(coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'clicks')::text::float,0) + coalesce((Excluded.day_chart::json->0->'clicks')::text::float,0)) end,
                                    'ctr', case coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'imp')::text::integer,0) + coalesce((Excluded.day_chart::json->0->'imp')::text::integer,0)
                                           when 0 then 0
                                           else (coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'clicks')::text::float,0) + coalesce((Excluded.day_chart::json->0->'clicks')::text::float,0))/(coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'imp')::text::float,0) + coalesce((Excluded.day_chart::json->0->'imp')::text::float,0)) end
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
                         'imp', count(site_r."id"),
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
                         'imp', 0,
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
                                        'imp', coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'imp')::text::integer,0),
                                        'mediaspent', coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'mediaspent')::text::float,0),
                                        'clicks', coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'clicks')::text::integer,0) + coalesce((Excluded.day_chart::json->0->'clicks')::text::integer,0),
                                        'conversions', coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'conversions')::text::integer,0),
                                        'cpa', case (coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'conversions')::text::integer,0) + coalesce((Excluded.day_chart::json->0->'conversions')::text::integer,0))
                                               when 0 then 0
                                               else (coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'mediaspent')::text::float,0) + coalesce((Excluded.day_chart::json->0->'mediaspent')::text::float,0))/(coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'conversions')::text::float,0) + coalesce((Excluded.day_chart::json->0->'conversions')::text::float,0)) end,
                                        'cpc', case (coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'clicks')::text::integer,0) + coalesce((Excluded.day_chart::json->0->'clicks')::text::integer,0))
                                               when 0 then 0
                                               else (coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'mediaspent')::text::float,0) + coalesce((Excluded.day_chart::json->0->'mediaspent')::text::float,0))/(coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'clicks')::text::float,0) + coalesce((Excluded.day_chart::json->0->'clicks')::text::float,0)) end,
                                        'ctr', case coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'imp')::text::integer,0) + coalesce((Excluded.day_chart::json->0->'imp')::text::integer,0)
                                               when 0 then 0
                                               else (coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'clicks')::text::float,0) + coalesce((Excluded.day_chart::json->0->'clicks')::text::float,0))/(coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'imp')::text::float,0) + coalesce((Excluded.day_chart::json->0->'imp')::text::float,0)) end
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
                         'imp', 0,
                         'spend', 0,
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
                                        'imp', coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'imp')::text::integer,0),
                                        'mediaspent', coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'mediaspent')::text::float,0),
                                        'clicks', coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'clicks')::text::integer,0),
                                        'conversions', coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'conversions')::text::integer,0) + coalesce((Excluded.day_chart::json->0->'conversions')::text::integer,0),
                                        'cpa', case (coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'conversions')::text::integer,0) + coalesce((Excluded.day_chart::json->0->'conversions')::text::integer,0))
                                               when 0 then 0
                                               else (coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'mediaspent')::text::float,0) + coalesce((Excluded.day_chart::json->0->'mediaspent')::text::float,0))/(coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'conversions')::text::float,0) + coalesce((Excluded.day_chart::json->0->'conversions')::text::float,0)) end,
                                        'cpc', case (coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'clicks')::text::integer,0) + coalesce((Excluded.day_chart::json->0->'clicks')::text::integer,0))
                                               when 0 then 0
                                               else (coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'mediaspent')::text::float,0) + coalesce((Excluded.day_chart::json->0->'mediaspent')::text::float,0))/(coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'clicks')::text::float,0) + coalesce((Excluded.day_chart::json->0->'clicks')::text::float,0)) end,
                                        'ctr', case coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'imp')::text::integer,0) + coalesce((Excluded.day_chart::json->0->'imp')::text::integer,0)
                                               when 0 then 0
                                               else (coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'clicks')::text::float,0) + coalesce((Excluded.day_chart::json->0->'clicks')::text::float,0))/(coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'imp')::text::float,0) + coalesce((Excluded.day_chart::json->0->'imp')::text::float,0)) end
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
                         'imp', count(site_r."id"),
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
                         'imp', 0,
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
                                        'imp', coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'imp')::text::integer,0),
                                        'mediaspent', coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'mediaspent')::text::float,0),
                                        'clicks', coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'clicks')::text::integer,0) + coalesce((Excluded.day_chart::json->0->'clicks')::text::integer,0),
                                        'conversions', coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'conversions')::text::integer,0),
                                        'cpa', case (coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'conversions')::text::integer,0) + coalesce((Excluded.day_chart::json->0->'conversions')::text::integer,0))
                                               when 0 then 0
                                               else (coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'mediaspent')::text::float,0) + coalesce((Excluded.day_chart::json->0->'mediaspent')::text::float,0))/(coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'conversions')::text::float,0) + coalesce((Excluded.day_chart::json->0->'conversions')::text::float,0)) end,
                                        'cpc', case (coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'clicks')::text::integer,0) + coalesce((Excluded.day_chart::json->0->'clicks')::text::integer,0))
                                               when 0 then 0
                                               else (coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'mediaspent')::text::float,0) + coalesce((Excluded.day_chart::json->0->'mediaspent')::text::float,0))/(coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'clicks')::text::float,0) + coalesce((Excluded.day_chart::json->0->'clicks')::text::float,0)) end,
                                        'ctr', case coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'imp')::text::integer,0) + coalesce((Excluded.day_chart::json->0->'imp')::text::integer,0)
                                               when 0 then 0
                                               else (coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'clicks')::text::float,0) + coalesce((Excluded.day_chart::json->0->'clicks')::text::float,0))/(coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'imp')::text::float,0) + coalesce((Excluded.day_chart::json->0->'imp')::text::float,0)) end
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
                         'imp', 0,
                         'spend', 0,
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
                                        'imp', coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'imp')::text::integer,0),
                                        'mediaspent', coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'mediaspent')::text::float,0),
                                        'clicks', coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'clicks')::text::integer,0),
                                        'conversions', coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'conversions')::text::integer,0) + coalesce((Excluded.day_chart::json->0->'conversions')::text::integer,0),
                                        'cpa', case (coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'conversions')::text::integer,0) + coalesce((Excluded.day_chart::json->0->'conversions')::text::integer,0))
                                               when 0 then 0
                                               else (coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'mediaspent')::text::float,0) + coalesce((Excluded.day_chart::json->0->'mediaspent')::text::float,0))/(coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'conversions')::text::float,0) + coalesce((Excluded.day_chart::json->0->'conversions')::text::float,0)) end,
                                        'cpc', case (coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'clicks')::text::integer,0) + coalesce((Excluded.day_chart::json->0->'clicks')::text::integer,0))
                                               when 0 then 0
                                               else (coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'mediaspent')::text::float,0) + coalesce((Excluded.day_chart::json->0->'mediaspent')::text::float,0))/(coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'clicks')::text::float,0) + coalesce((Excluded.day_chart::json->0->'clicks')::text::float,0)) end,
                                        'ctr', case coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'imp')::text::integer,0) + coalesce((Excluded.day_chart::json->0->'imp')::text::integer,0)
                                               when 0 then 0
                                               else (coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'clicks')::text::float,0) + coalesce((Excluded.day_chart::json->0->'clicks')::text::float,0))/(coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'imp')::text::float,0) + coalesce((Excluded.day_chart::json->0->'imp')::text::float,0)) end
                                    )::jsonb,
                                    true)
                                  else ut.day_chart||Excluded.day_chart end;
                            """),

        ##
        # ADVERTISERS GRAPH
        ##

        # all

        migrations.RunSQL("delete from ui_usual_advertisers_graph_tracker;"),

        migrations.RunSQL("""
insert into ui_usual_advertisers_graph_tracker as ut (
    advertiser_id,
    type,
    day_chart)
  select
  page."AdvId",
  'all',
  array_to_json(array((select
         json_build_object(
         'day', site_r."Date"::timestamp::date,
         'imp', count(site_r."id"),
         'spend', sum(site_r."PricePaid"),
         'clicks', 0,
         'conversions', 0,
         'cvr', 0,
         'cpc', 0,
         'ctr', 0)
       from
            rtb_impression_tracker site_r
       where site_r."AdvId"= page."AdvId"
       and
       site_r."Date" <= (select date from last_modified where type='lastPrecalculatedTrackerCron')
       group by site_r."Date"::timestamp::date
       order by site_r."Date"::timestamp::date))) id
from (
      select
        distinct "AdvId"
      from
        rtb_impression_tracker
      where "Date" <= (select date from last_modified where type='lastPrecalculatedTrackerCron')
     ) page;
                            """),

        migrations.RunSQL("""
insert into ui_usual_advertisers_graph_tracker as ut (
    advertiser_id,
    type,
    day_chart)
  select
  page."AdvId",
  'all',
  array_to_json(array((select
         json_build_object(
         'day', site_r."Date"::timestamp::date,
         'imp', 0,
         'spend', 0,
         'clicks', count(site_r."id"),
         'conversions', 0,
         'cvr', 0,
         'cpc', 0,
         'ctr', 0)
       from
            rtb_click_tracker site_r
       where site_r."AdvId"= page."AdvId"
       and
       site_r."Date" <= (select date from last_modified where type='lastPrecalculatedTrackerCron')
       group by site_r."Date"::timestamp::date
       order by site_r."Date"::timestamp::date))) id
from (
      select
        distinct rtb_click_tracker."AdvId"
      from
        rtb_click_tracker
      where "Date" <= (select date from last_modified where type='lastPrecalculatedTrackerCron')
     ) page
ON CONFLICT (advertiser_id, type)
  DO UPDATE SET
     day_chart = case (ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'day')::text when (Excluded.day_chart::json->0->'day')::text
                  then jsonb_set(
                    ut.day_chart::jsonb,
                    concat('{', (jsonb_array_length(ut.day_chart)-1), '}')::text[],
                    json_build_object(
                        'day', ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'day',
                        'imp', coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'imp')::text::integer,0),
                        'spend', coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'spend')::text::float,0),
                        'clicks', coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'clicks')::text::integer,0) + coalesce((Excluded.day_chart::json->0->'clicks')::text::integer,0),
                        'conversions', coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'conversions')::text::integer,0),
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
                            """),

        migrations.RunSQL("""
insert into ui_usual_advertisers_graph_tracker as ut (
    advertiser_id,
    type,
    day_chart)
  select
  page."AdvId",
  'all',
  array_to_json(array((select
         json_build_object(
         'day', site_r."Date"::timestamp::date,
         'imp', 0,
         'spend', 0,
         'clicks', 0,
         'conversions', count(site_r."id"),
         'cvr', 0,
         'cpc', 0,
         'ctr', 0)
       from
            rtb_conversion_tracker site_r
       where site_r."AdvId"= page."AdvId"
       and
       site_r."Date" <= (select date from last_modified where type='lastPrecalculatedTrackerCron')
       group by site_r."Date"::timestamp::date
       order by site_r."Date"::timestamp::date))) id
from (
      select
        distinct "AdvId"
      from
        rtb_conversion_tracker
      where "Date" <= (select date from last_modified where type='lastPrecalculatedTrackerCron')
     ) page
ON CONFLICT (advertiser_id, type)
  DO UPDATE SET
     day_chart = case (ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'day')::text when (Excluded.day_chart::json->0->'day')::text
                  then jsonb_set(
                    ut.day_chart::jsonb,
                    concat('{', (jsonb_array_length(ut.day_chart)-1), '}')::text[],
                    json_build_object(
                        'day', ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'day',
                        'imp', coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'imp')::text::integer,0),
                        'spend', coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'spend')::text::float,0),
                        'clicks', coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'clicks')::text::integer,0),
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
                                """),

        # yesterday

        migrations.RunSQL("""
insert into ui_usual_advertisers_graph_tracker as ut (
    advertiser_id,
    type,
    day_chart)
  select
  page."AdvId",
  'yesterday',
  array_to_json(array((select
         json_build_object(
         'day', site_r."Date"::timestamp::date,
         'imp', count(site_r."id"),
         'spend', sum(site_r."PricePaid"),
         'clicks', 0,
         'conversions', 0,
         'cvr', 0,
         'cpc', 0,
         'ctr', 0)
       from
            rtb_impression_tracker site_r
       where site_r."AdvId"= page."AdvId"
         and
         site_r."Date" >= date_trunc('day',(select date from last_modified where type='lastPrecalculatedTrackerCron') - interval '1 day')
         and
         site_r."Date" <= (select date from last_modified where type='lastPrecalculatedTrackerCron')
       group by site_r."Date"::timestamp::date
       order by site_r."Date"::timestamp::date))) id
from (
      select
        distinct "AdvId"
      from
        rtb_impression_tracker
      where
        "Date" >= date_trunc('day',(select date from last_modified where type='lastPrecalculatedTrackerCron') - interval '1 day')
        and
        "Date" <= (select date from last_modified where type='lastPrecalculatedTrackerCron')
     ) page;
                        """),

        migrations.RunSQL("""
insert into ui_usual_advertisers_graph_tracker as ut (
    advertiser_id,
    type,
    day_chart)
  select
  page."AdvId",
  'yesterday',
  array_to_json(array((select
         json_build_object(
         'day', site_r."Date"::timestamp::date,
         'imp', 0,
         'spend', 0,
         'clicks', count(site_r."id"),
         'conversions', 0,
         'cvr', 0,
         'cpc', 0,
         'ctr', 0)
       from
            rtb_click_tracker site_r
       where site_r."AdvId"= page."AdvId"
         and
         site_r."Date" >= date_trunc('day',(select date from last_modified where type='lastPrecalculatedTrackerCron') - interval '1 day')
         and
         site_r."Date" <= (select date from last_modified where type='lastPrecalculatedTrackerCron')
       group by site_r."Date"::timestamp::date
       order by site_r."Date"::timestamp::date))) id
from (
      select
        distinct rtb_click_tracker."AdvId"
      from
        rtb_click_tracker
      where
        rtb_click_tracker."Date" >= date_trunc('day',(select date from last_modified where type='lastPrecalculatedTrackerCron') - interval '1 day')
        and
        rtb_click_tracker."Date" <= (select date from last_modified where type='lastPrecalculatedTrackerCron')
     ) page
ON CONFLICT (advertiser_id, type)
  DO UPDATE SET
     day_chart = case (ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'day')::text when (Excluded.day_chart::json->0->'day')::text
                  then jsonb_set(
                    ut.day_chart::jsonb,
                    concat('{', (jsonb_array_length(ut.day_chart)-1), '}')::text[],
                    json_build_object(
                        'day', ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'day',
                        'imp', coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'imp')::text::integer,0),
                        'spend', coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'spend')::text::float,0),
                        'clicks', coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'clicks')::text::integer,0) + coalesce((Excluded.day_chart::json->0->'clicks')::text::integer,0),
                        'conversions', coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'conversions')::text::integer,0),
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
                        """),

        migrations.RunSQL("""
insert into ui_usual_advertisers_graph_tracker as ut (
    advertiser_id,
    type,
    day_chart)
  select
  page."AdvId",
  'yesterday',
  array_to_json(array((select
         json_build_object(
         'day', site_r."Date"::timestamp::date,
         'imp', 0,
         'spend', 0,
         'clicks', 0,
         'conversions', count(site_r."id"),
         'cvr', 0,
         'cpc', 0,
         'ctr', 0)
       from
            rtb_conversion_tracker site_r
       where site_r."AdvId"= page."AdvId"
         and
         site_r."Date" >= date_trunc('day',(select date from last_modified where type='lastPrecalculatedTrackerCron') - interval '1 day')
         and
         site_r."Date" <= (select date from last_modified where type='lastPrecalculatedTrackerCron')
       group by site_r."Date"::timestamp::date
       order by site_r."Date"::timestamp::date))) id
from (
      select
        distinct "AdvId"
      from
        rtb_conversion_tracker
      where
        rtb_conversion_tracker."Date" >= date_trunc('day',(select date from last_modified where type='lastPrecalculatedTrackerCron') - interval '1 day')
        and
        rtb_conversion_tracker."Date" <= (select date from last_modified where type='lastPrecalculatedTrackerCron')
     ) page
ON CONFLICT (advertiser_id, type)
  DO UPDATE SET
     day_chart = case (ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'day')::text when (Excluded.day_chart::json->0->'day')::text
                  then jsonb_set(
                    ut.day_chart::jsonb,
                    concat('{', (jsonb_array_length(ut.day_chart)-1), '}')::text[],
                    json_build_object(
                        'day', ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'day',
                        'imp', coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'imp')::text::integer,0),
                        'spend', coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'spend')::text::float,0),
                        'clicks', coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'clicks')::text::integer,0),
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
                            """),

        # last_3_days

        migrations.RunSQL("""
        insert into ui_usual_advertisers_graph_tracker as ut (
            advertiser_id,
            type,
            day_chart)
          select
          page."AdvId",
          'last_3_days',
          array_to_json(array((select
                 json_build_object(
                 'day', site_r."Date"::timestamp::date,
                 'imp', count(site_r."id"),
                 'spend', sum(site_r."PricePaid"),
                 'clicks', 0,
                 'conversions', 0,
                 'cvr', 0,
                 'cpc', 0,
                 'ctr', 0)
               from
                    rtb_impression_tracker site_r
               where site_r."AdvId"= page."AdvId"
                 and
                 site_r."Date" >= date_trunc('day',(select date from last_modified where type='lastPrecalculatedTrackerCron') - interval '3 day')
                 and
                 site_r."Date" <= (select date from last_modified where type='lastPrecalculatedTrackerCron')
               group by site_r."Date"::timestamp::date
               order by site_r."Date"::timestamp::date))) id
        from (
              select
                distinct "AdvId"
              from
                rtb_impression_tracker
              where
                "Date" >= date_trunc('day',(select date from last_modified where type='lastPrecalculatedTrackerCron') - interval '3 day')
                and
                "Date" <= (select date from last_modified where type='lastPrecalculatedTrackerCron')
             ) page;
                                """),

        migrations.RunSQL("""
        insert into ui_usual_advertisers_graph_tracker as ut (
            advertiser_id,
            type,
            day_chart)
          select
          page."AdvId",
          'last_3_days',
          array_to_json(array((select
                 json_build_object(
                 'day', site_r."Date"::timestamp::date,
                 'imp', 0,
                 'spend', 0,
                 'clicks', count(site_r."id"),
                 'conversions', 0,
                 'cvr', 0,
                 'cpc', 0,
                 'ctr', 0)
               from
                    rtb_click_tracker site_r
               where site_r."AdvId"= page."AdvId"
                 and
                 site_r."Date" >= date_trunc('day',(select date from last_modified where type='lastPrecalculatedTrackerCron') - interval '3 day')
                 and
                 site_r."Date" <= (select date from last_modified where type='lastPrecalculatedTrackerCron')
               group by site_r."Date"::timestamp::date
               order by site_r."Date"::timestamp::date))) id
        from (
              select
                distinct rtb_click_tracker."AdvId"
              from
                rtb_click_tracker
              where
                rtb_click_tracker."Date" >= date_trunc('day',(select date from last_modified where type='lastPrecalculatedTrackerCron') - interval '3 day')
                and
                rtb_click_tracker."Date" <= (select date from last_modified where type='lastPrecalculatedTrackerCron')
             ) page
        ON CONFLICT (advertiser_id, type)
          DO UPDATE SET
             day_chart = case (ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'day')::text when (Excluded.day_chart::json->0->'day')::text
                          then jsonb_set(
                            ut.day_chart::jsonb,
                            concat('{', (jsonb_array_length(ut.day_chart)-1), '}')::text[],
                            json_build_object(
                                'day', ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'day',
                                'imp', coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'imp')::text::integer,0),
                                'spend', coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'spend')::text::float,0),
                                'clicks', coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'clicks')::text::integer,0) + coalesce((Excluded.day_chart::json->0->'clicks')::text::integer,0),
                                'conversions', coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'conversions')::text::integer,0),
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
                                """),

        migrations.RunSQL("""
        insert into ui_usual_advertisers_graph_tracker as ut (
            advertiser_id,
            type,
            day_chart)
          select
          page."AdvId",
          'last_3_days',
          array_to_json(array((select
                 json_build_object(
                 'day', site_r."Date"::timestamp::date,
                 'imp', 0,
                 'spend', 0,
                 'clicks', 0,
                 'conversions', count(site_r."id"),
                 'cvr', 0,
                 'cpc', 0,
                 'ctr', 0)
               from
                    rtb_conversion_tracker site_r
               where site_r."AdvId"= page."AdvId"
                 and
                 site_r."Date" >= date_trunc('day',(select date from last_modified where type='lastPrecalculatedTrackerCron') - interval '3 day')
                 and
                 site_r."Date" <= (select date from last_modified where type='lastPrecalculatedTrackerCron')
               group by site_r."Date"::timestamp::date
               order by site_r."Date"::timestamp::date))) id
        from (
              select
                distinct "AdvId"
              from
                rtb_conversion_tracker
              where
                rtb_conversion_tracker."Date" >= date_trunc('day',(select date from last_modified where type='lastPrecalculatedTrackerCron') - interval '3 day')
                and
                rtb_conversion_tracker."Date" <= (select date from last_modified where type='lastPrecalculatedTrackerCron')
             ) page
        ON CONFLICT (advertiser_id, type)
          DO UPDATE SET
             day_chart = case (ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'day')::text when (Excluded.day_chart::json->0->'day')::text
                          then jsonb_set(
                            ut.day_chart::jsonb,
                            concat('{', (jsonb_array_length(ut.day_chart)-1), '}')::text[],
                            json_build_object(
                                'day', ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'day',
                                'imp', coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'imp')::text::integer,0),
                                'spend', coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'spend')::text::float,0),
                                'clicks', coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'clicks')::text::integer,0),
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
                                    """),

        # last_7_days

        migrations.RunSQL("""
            insert into ui_usual_advertisers_graph_tracker as ut (
                advertiser_id,
                type,
                day_chart)
              select
              page."AdvId",
              'last_7_days',
              array_to_json(array((select
                     json_build_object(
                     'day', site_r."Date"::timestamp::date,
                     'imp', count(site_r."id"),
                     'spend', sum(site_r."PricePaid"),
                     'clicks', 0,
                     'conversions', 0,
                     'cvr', 0,
                     'cpc', 0,
                     'ctr', 0)
                   from
                        rtb_impression_tracker site_r
                   where site_r."AdvId"= page."AdvId"
                     and
                     site_r."Date" >= date_trunc('day',(select date from last_modified where type='lastPrecalculatedTrackerCron') - interval '7 day')
                     and
                     site_r."Date" <= (select date from last_modified where type='lastPrecalculatedTrackerCron')
                   group by site_r."Date"::timestamp::date
                   order by site_r."Date"::timestamp::date))) id
            from (
                  select
                    distinct "AdvId"
                  from
                    rtb_impression_tracker
                  where
                    "Date" >= date_trunc('day',(select date from last_modified where type='lastPrecalculatedTrackerCron') - interval '7 day')
                    and
                    "Date" <= (select date from last_modified where type='lastPrecalculatedTrackerCron')
                 ) page;
                                    """),

        migrations.RunSQL("""
            insert into ui_usual_advertisers_graph_tracker as ut (
                advertiser_id,
                type,
                day_chart)
              select
              page."AdvId",
              'last_7_days',
              array_to_json(array((select
                     json_build_object(
                     'day', site_r."Date"::timestamp::date,
                     'imp', 0,
                     'spend', 0,
                     'clicks', count(site_r."id"),
                     'conversions', 0,
                     'cvr', 0,
                     'cpc', 0,
                     'ctr', 0)
                   from
                        rtb_click_tracker site_r
                   where site_r."AdvId"= page."AdvId"
                     and
                     site_r."Date" >= date_trunc('day',(select date from last_modified where type='lastPrecalculatedTrackerCron') - interval '7 day')
                     and
                     site_r."Date" <= (select date from last_modified where type='lastPrecalculatedTrackerCron')
                   group by site_r."Date"::timestamp::date
                   order by site_r."Date"::timestamp::date))) id
            from (
                  select
                    distinct rtb_click_tracker."AdvId"
                  from
                    rtb_click_tracker
                  where
                    rtb_click_tracker."Date" >= date_trunc('day',(select date from last_modified where type='lastPrecalculatedTrackerCron') - interval '7 day')
                    and
                    rtb_click_tracker."Date" <= (select date from last_modified where type='lastPrecalculatedTrackerCron')
                 ) page
            ON CONFLICT (advertiser_id, type)
              DO UPDATE SET
                 day_chart = case (ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'day')::text when (Excluded.day_chart::json->0->'day')::text
                              then jsonb_set(
                                ut.day_chart::jsonb,
                                concat('{', (jsonb_array_length(ut.day_chart)-1), '}')::text[],
                                json_build_object(
                                    'day', ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'day',
                                    'imp', coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'imp')::text::integer,0),
                                    'spend', coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'spend')::text::float,0),
                                    'clicks', coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'clicks')::text::integer,0) + coalesce((Excluded.day_chart::json->0->'clicks')::text::integer,0),
                                    'conversions', coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'conversions')::text::integer,0),
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
                                    """),

        migrations.RunSQL("""
            insert into ui_usual_advertisers_graph_tracker as ut (
                advertiser_id,
                type,
                day_chart)
              select
              page."AdvId",
              'last_7_days',
              array_to_json(array((select
                     json_build_object(
                     'day', site_r."Date"::timestamp::date,
                     'imp', 0,
                     'spend', 0,
                     'clicks', 0,
                     'conversions', count(site_r."id"),
                     'cvr', 0,
                     'cpc', 0,
                     'ctr', 0)
                   from
                        rtb_conversion_tracker site_r
                   where site_r."AdvId"= page."AdvId"
                     and
                     site_r."Date" >= date_trunc('day',(select date from last_modified where type='lastPrecalculatedTrackerCron') - interval '7 day')
                     and
                     site_r."Date" <= (select date from last_modified where type='lastPrecalculatedTrackerCron')
                   group by site_r."Date"::timestamp::date
                   order by site_r."Date"::timestamp::date))) id
            from (
                  select
                    distinct "AdvId"
                  from
                    rtb_conversion_tracker
                  where
                    rtb_conversion_tracker."Date" >= date_trunc('day',(select date from last_modified where type='lastPrecalculatedTrackerCron') - interval '7 day')
                    and
                    rtb_conversion_tracker."Date" <= (select date from last_modified where type='lastPrecalculatedTrackerCron')
                 ) page
            ON CONFLICT (advertiser_id, type)
              DO UPDATE SET
                 day_chart = case (ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'day')::text when (Excluded.day_chart::json->0->'day')::text
                              then jsonb_set(
                                ut.day_chart::jsonb,
                                concat('{', (jsonb_array_length(ut.day_chart)-1), '}')::text[],
                                json_build_object(
                                    'day', ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'day',
                                    'imp', coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'imp')::text::integer,0),
                                    'spend', coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'spend')::text::float,0),
                                    'clicks', coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'clicks')::text::integer,0),
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
                                        """),

        # last_14_days

        migrations.RunSQL("""
            insert into ui_usual_advertisers_graph_tracker as ut (
                advertiser_id,
                type,
                day_chart)
              select
              page."AdvId",
              'last_14_days',
              array_to_json(array((select
                     json_build_object(
                     'day', site_r."Date"::timestamp::date,
                     'imp', count(site_r."id"),
                     'spend', sum(site_r."PricePaid"),
                     'clicks', 0,
                     'conversions', 0,
                     'cvr', 0,
                     'cpc', 0,
                     'ctr', 0)
                   from
                        rtb_impression_tracker site_r
                   where site_r."AdvId"= page."AdvId"
                     and
                     site_r."Date" >= date_trunc('day',(select date from last_modified where type='lastPrecalculatedTrackerCron') - interval '14 day')
                     and
                     site_r."Date" <= (select date from last_modified where type='lastPrecalculatedTrackerCron')
                   group by site_r."Date"::timestamp::date
                   order by site_r."Date"::timestamp::date))) id
            from (
                  select
                    distinct "AdvId"
                  from
                    rtb_impression_tracker
                  where
                    "Date" >= date_trunc('day',(select date from last_modified where type='lastPrecalculatedTrackerCron') - interval '14 day')
                    and
                    "Date" <= (select date from last_modified where type='lastPrecalculatedTrackerCron')
                 ) page;
                                    """),

        migrations.RunSQL("""
            insert into ui_usual_advertisers_graph_tracker as ut (
                advertiser_id,
                type,
                day_chart)
              select
              page."AdvId",
              'last_14_days',
              array_to_json(array((select
                     json_build_object(
                     'day', site_r."Date"::timestamp::date,
                     'imp', 0,
                     'spend', 0,
                     'clicks', count(site_r."id"),
                     'conversions', 0,
                     'cvr', 0,
                     'cpc', 0,
                     'ctr', 0)
                   from
                        rtb_click_tracker site_r
                   where site_r."AdvId"= page."AdvId"
                     and
                     site_r."Date" >= date_trunc('day',(select date from last_modified where type='lastPrecalculatedTrackerCron') - interval '14 day')
                     and
                     site_r."Date" <= (select date from last_modified where type='lastPrecalculatedTrackerCron')
                   group by site_r."Date"::timestamp::date
                   order by site_r."Date"::timestamp::date))) id
            from (
                  select
                    distinct rtb_click_tracker."AdvId"
                  from
                    rtb_click_tracker
                  where
                    rtb_click_tracker."Date" >= date_trunc('day',(select date from last_modified where type='lastPrecalculatedTrackerCron') - interval '14 day')
                    and
                    rtb_click_tracker."Date" <= (select date from last_modified where type='lastPrecalculatedTrackerCron')
                 ) page
            ON CONFLICT (advertiser_id, type)
              DO UPDATE SET
                 day_chart = case (ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'day')::text when (Excluded.day_chart::json->0->'day')::text
                              then jsonb_set(
                                ut.day_chart::jsonb,
                                concat('{', (jsonb_array_length(ut.day_chart)-1), '}')::text[],
                                json_build_object(
                                    'day', ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'day',
                                    'imp', coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'imp')::text::integer,0),
                                    'spend', coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'spend')::text::float,0),
                                    'clicks', coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'clicks')::text::integer,0) + coalesce((Excluded.day_chart::json->0->'clicks')::text::integer,0),
                                    'conversions', coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'conversions')::text::integer,0),
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
                                    """),

        migrations.RunSQL("""
            insert into ui_usual_advertisers_graph_tracker as ut (
                advertiser_id,
                type,
                day_chart)
              select
              page."AdvId",
              'last_14_days',
              array_to_json(array((select
                     json_build_object(
                     'day', site_r."Date"::timestamp::date,
                     'imp', 0,
                     'spend', 0,
                     'clicks', 0,
                     'conversions', count(site_r."id"),
                     'cvr', 0,
                     'cpc', 0,
                     'ctr', 0)
                   from
                        rtb_conversion_tracker site_r
                   where site_r."AdvId"= page."AdvId"
                     and
                     site_r."Date" >= date_trunc('day',(select date from last_modified where type='lastPrecalculatedTrackerCron') - interval '14 day')
                     and
                     site_r."Date" <= (select date from last_modified where type='lastPrecalculatedTrackerCron')
                   group by site_r."Date"::timestamp::date
                   order by site_r."Date"::timestamp::date))) id
            from (
                  select
                    distinct "AdvId"
                  from
                    rtb_conversion_tracker
                  where
                    rtb_conversion_tracker."Date" >= date_trunc('day',(select date from last_modified where type='lastPrecalculatedTrackerCron') - interval '14 day')
                    and
                    rtb_conversion_tracker."Date" <= (select date from last_modified where type='lastPrecalculatedTrackerCron')
                 ) page
            ON CONFLICT (advertiser_id, type)
              DO UPDATE SET
                 day_chart = case (ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'day')::text when (Excluded.day_chart::json->0->'day')::text
                              then jsonb_set(
                                ut.day_chart::jsonb,
                                concat('{', (jsonb_array_length(ut.day_chart)-1), '}')::text[],
                                json_build_object(
                                    'day', ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'day',
                                    'imp', coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'imp')::text::integer,0),
                                    'spend', coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'spend')::text::float,0),
                                    'clicks', coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'clicks')::text::integer,0),
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
                                        """),

        # last_21_days

        migrations.RunSQL("""
            insert into ui_usual_advertisers_graph_tracker as ut (
                advertiser_id,
                type,
                day_chart)
              select
              page."AdvId",
              'last_21_days',
              array_to_json(array((select
                     json_build_object(
                     'day', site_r."Date"::timestamp::date,
                     'imp', count(site_r."id"),
                     'spend', sum(site_r."PricePaid"),
                     'clicks', 0,
                     'conversions', 0,
                     'cvr', 0,
                     'cpc', 0,
                     'ctr', 0)
                   from
                        rtb_impression_tracker site_r
                   where site_r."AdvId"= page."AdvId"
                     and
                     site_r."Date" >= date_trunc('day',(select date from last_modified where type='lastPrecalculatedTrackerCron') - interval '21 day')
                     and
                     site_r."Date" <= (select date from last_modified where type='lastPrecalculatedTrackerCron')
                   group by site_r."Date"::timestamp::date
                   order by site_r."Date"::timestamp::date))) id
            from (
                  select
                    distinct "AdvId"
                  from
                    rtb_impression_tracker
                  where
                    "Date" >= date_trunc('day',(select date from last_modified where type='lastPrecalculatedTrackerCron') - interval '21 day')
                    and
                    "Date" <= (select date from last_modified where type='lastPrecalculatedTrackerCron')
                 ) page;
                                    """),

        migrations.RunSQL("""
            insert into ui_usual_advertisers_graph_tracker as ut (
                advertiser_id,
                type,
                day_chart)
              select
              page."AdvId",
              'last_21_days',
              array_to_json(array((select
                     json_build_object(
                     'day', site_r."Date"::timestamp::date,
                     'imp', 0,
                     'spend', 0,
                     'clicks', count(site_r."id"),
                     'conversions', 0,
                     'cvr', 0,
                     'cpc', 0,
                     'ctr', 0)
                   from
                        rtb_click_tracker site_r
                   where site_r."AdvId"= page."AdvId"
                     and
                     site_r."Date" >= date_trunc('day',(select date from last_modified where type='lastPrecalculatedTrackerCron') - interval '21 day')
                     and
                     site_r."Date" <= (select date from last_modified where type='lastPrecalculatedTrackerCron')
                   group by site_r."Date"::timestamp::date
                   order by site_r."Date"::timestamp::date))) id
            from (
                  select
                    distinct rtb_click_tracker."AdvId"
                  from
                    rtb_click_tracker
                  where
                    rtb_click_tracker."Date" >= date_trunc('day',(select date from last_modified where type='lastPrecalculatedTrackerCron') - interval '21 day')
                    and
                    rtb_click_tracker."Date" <= (select date from last_modified where type='lastPrecalculatedTrackerCron')
                 ) page
            ON CONFLICT (advertiser_id, type)
              DO UPDATE SET
                 day_chart = case (ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'day')::text when (Excluded.day_chart::json->0->'day')::text
                              then jsonb_set(
                                ut.day_chart::jsonb,
                                concat('{', (jsonb_array_length(ut.day_chart)-1), '}')::text[],
                                json_build_object(
                                    'day', ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'day',
                                    'imp', coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'imp')::text::integer,0),
                                    'spend', coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'spend')::text::float,0),
                                    'clicks', coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'clicks')::text::integer,0) + coalesce((Excluded.day_chart::json->0->'clicks')::text::integer,0),
                                    'conversions', coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'conversions')::text::integer,0),
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
                                    """),

        migrations.RunSQL("""
            insert into ui_usual_advertisers_graph_tracker as ut (
                advertiser_id,
                type,
                day_chart)
              select
              page."AdvId",
              'last_21_days',
              array_to_json(array((select
                     json_build_object(
                     'day', site_r."Date"::timestamp::date,
                     'imp', 0,
                     'spend', 0,
                     'clicks', 0,
                     'conversions', count(site_r."id"),
                     'cvr', 0,
                     'cpc', 0,
                     'ctr', 0)
                   from
                        rtb_conversion_tracker site_r
                   where site_r."AdvId"= page."AdvId"
                     and
                     site_r."Date" >= date_trunc('day',(select date from last_modified where type='lastPrecalculatedTrackerCron') - interval '21 day')
                     and
                     site_r."Date" <= (select date from last_modified where type='lastPrecalculatedTrackerCron')
                   group by site_r."Date"::timestamp::date
                   order by site_r."Date"::timestamp::date))) id
            from (
                  select
                    distinct "AdvId"
                  from
                    rtb_conversion_tracker
                  where
                    rtb_conversion_tracker."Date" >= date_trunc('day',(select date from last_modified where type='lastPrecalculatedTrackerCron') - interval '21 day')
                    and
                    rtb_conversion_tracker."Date" <= (select date from last_modified where type='lastPrecalculatedTrackerCron')
                 ) page
            ON CONFLICT (advertiser_id, type)
              DO UPDATE SET
                 day_chart = case (ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'day')::text when (Excluded.day_chart::json->0->'day')::text
                              then jsonb_set(
                                ut.day_chart::jsonb,
                                concat('{', (jsonb_array_length(ut.day_chart)-1), '}')::text[],
                                json_build_object(
                                    'day', ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'day',
                                    'imp', coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'imp')::text::integer,0),
                                    'spend', coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'spend')::text::float,0),
                                    'clicks', coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'clicks')::text::integer,0),
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
                                        """),

        # last_90_days

        migrations.RunSQL("""
            insert into ui_usual_advertisers_graph_tracker as ut (
                advertiser_id,
                type,
                day_chart)
              select
              page."AdvId",
              'last_90_days',
              array_to_json(array((select
                     json_build_object(
                     'day', site_r."Date"::timestamp::date,
                     'imp', count(site_r."id"),
                     'spend', sum(site_r."PricePaid"),
                     'clicks', 0,
                     'conversions', 0,
                     'cvr', 0,
                     'cpc', 0,
                     'ctr', 0)
                   from
                        rtb_impression_tracker site_r
                   where site_r."AdvId"= page."AdvId"
                     and
                     site_r."Date" >= date_trunc('day',(select date from last_modified where type='lastPrecalculatedTrackerCron') - interval '90 day')
                     and
                     site_r."Date" <= (select date from last_modified where type='lastPrecalculatedTrackerCron')
                   group by site_r."Date"::timestamp::date
                   order by site_r."Date"::timestamp::date))) id
            from (
                  select
                    distinct "AdvId"
                  from
                    rtb_impression_tracker
                  where
                    "Date" >= date_trunc('day',(select date from last_modified where type='lastPrecalculatedTrackerCron') - interval '90 day')
                    and
                    "Date" <= (select date from last_modified where type='lastPrecalculatedTrackerCron')
                 ) page;
                                    """),

        migrations.RunSQL("""
            insert into ui_usual_advertisers_graph_tracker as ut (
                advertiser_id,
                type,
                day_chart)
              select
              page."AdvId",
              'last_90_days',
              array_to_json(array((select
                     json_build_object(
                     'day', site_r."Date"::timestamp::date,
                     'imp', 0,
                     'spend', 0,
                     'clicks', count(site_r."id"),
                     'conversions', 0,
                     'cvr', 0,
                     'cpc', 0,
                     'ctr', 0)
                   from
                        rtb_click_tracker site_r
                   where site_r."AdvId"= page."AdvId"
                     and
                     site_r."Date" >= date_trunc('day',(select date from last_modified where type='lastPrecalculatedTrackerCron') - interval '90 day')
                     and
                     site_r."Date" <= (select date from last_modified where type='lastPrecalculatedTrackerCron')
                   group by site_r."Date"::timestamp::date
                   order by site_r."Date"::timestamp::date))) id
            from (
                  select
                    distinct rtb_click_tracker."AdvId"
                  from
                    rtb_click_tracker
                  where
                    "Date" >= date_trunc('day',(select date from last_modified where type='lastPrecalculatedTrackerCron') - interval '90 day')
                    and
                    "Date" <= (select date from last_modified where type='lastPrecalculatedTrackerCron')
                 ) page
            ON CONFLICT (advertiser_id, type)
              DO UPDATE SET
                 day_chart = case (ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'day')::text when (Excluded.day_chart::json->0->'day')::text
                              then jsonb_set(
                                ut.day_chart::jsonb,
                                concat('{', (jsonb_array_length(ut.day_chart)-1), '}')::text[],
                                json_build_object(
                                    'day', ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'day',
                                    'imp', coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'imp')::text::integer,0),
                                    'spend', coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'spend')::text::float,0),
                                    'clicks', coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'clicks')::text::integer,0) + coalesce((Excluded.day_chart::json->0->'clicks')::text::integer,0),
                                    'conversions', coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'conversions')::text::integer,0),
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
                                    """),

        migrations.RunSQL("""
            insert into ui_usual_advertisers_graph_tracker as ut (
                advertiser_id,
                type,
                day_chart)
              select
              page."AdvId",
              'last_90_days',
              array_to_json(array((select
                     json_build_object(
                     'day', site_r."Date"::timestamp::date,
                     'imp', 0,
                     'spend', 0,
                     'clicks', 0,
                     'conversions', count(site_r."id"),
                     'cvr', 0,
                     'cpc', 0,
                     'ctr', 0)
                   from
                        rtb_conversion_tracker site_r
                   where site_r."AdvId"= page."AdvId"
                     and
                     site_r."Date" >= date_trunc('day',(select date from last_modified where type='lastPrecalculatedTrackerCron') - interval '90 day')
                   group by site_r."Date"::timestamp::date
                   order by site_r."Date"::timestamp::date))) id
            from (
                  select
                    distinct "AdvId"
                  from
                    rtb_conversion_tracker
                  where
                    rtb_conversion_tracker."Date" >= date_trunc('day',(select date from last_modified where type='lastPrecalculatedTrackerCron') - interval '90 day')
                    and
                    rtb_conversion_tracker."Date" <= (select date from last_modified where type='lastPrecalculatedTrackerCron')
                 ) page
            ON CONFLICT (advertiser_id, type)
              DO UPDATE SET
                 day_chart = case (ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'day')::text when (Excluded.day_chart::json->0->'day')::text
                              then jsonb_set(
                                ut.day_chart::jsonb,
                                concat('{', (jsonb_array_length(ut.day_chart)-1), '}')::text[],
                                json_build_object(
                                    'day', ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'day',
                                    'imp', coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'imp')::text::integer,0),
                                    'spend', coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'spend')::text::float,0),
                                    'clicks', coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'clicks')::text::integer,0),
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
                                        """),

        # last_month

        migrations.RunSQL("""
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
                         'clicks', 0,
                         'conversions', 0,
                         'cvr', 0,
                         'cpc', 0,
                         'ctr', 0)
                       from
                            rtb_impression_tracker site_r
                       where site_r."AdvId"= page."AdvId"
                         and
                         site_r."Date" >= date_trunc('month',(select date from last_modified where type='lastPrecalculatedTrackerCron') - interval '1 month')
                         and
                         site_r."Date" < date_trunc('month',(select date from last_modified where type='lastPrecalculatedTrackerCron'))
                       group by site_r."Date"::timestamp::date
                       order by site_r."Date"::timestamp::date))) id
                from (
                      select
                        distinct "AdvId"
                      from
                        rtb_impression_tracker
                      where
                        "Date" >= date_trunc('month',(select date from last_modified where type='lastPrecalculatedTrackerCron') - interval '1 month')
                        and
                        "Date" < date_trunc('month',(select date from last_modified where type='lastPrecalculatedTrackerCron'))
                     ) page;
                                        """),

        migrations.RunSQL("""
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
                         'imp', 0,
                         'spend', 0,
                         'clicks', count(site_r."id"),
                         'conversions', 0,
                         'cvr', 0,
                         'cpc', 0,
                         'ctr', 0)
                       from
                            rtb_click_tracker site_r
                       where site_r."AdvId"= page."AdvId"
                         and
                         site_r."Date" >= date_trunc('month',(select date from last_modified where type='lastPrecalculatedTrackerCron') - interval '1 month')
                         and
                         site_r."Date" < date_trunc('month',(select date from last_modified where type='lastPrecalculatedTrackerCron'))
                       group by site_r."Date"::timestamp::date
                       order by site_r."Date"::timestamp::date))) id
                from (
                      select
                        distinct rtb_click_tracker."AdvId"
                      from
                        rtb_click_tracker
                      where
                        rtb_click_tracker."Date" >= date_trunc('month',(select date from last_modified where type='lastPrecalculatedTrackerCron') - interval '1 month')
                        and
                        rtb_click_tracker."Date" < date_trunc('month',(select date from last_modified where type='lastPrecalculatedTrackerCron'))
                     ) page
                ON CONFLICT (advertiser_id, type)
                  DO UPDATE SET
                     day_chart = case (ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'day')::text when (Excluded.day_chart::json->0->'day')::text
                                  then jsonb_set(
                                    ut.day_chart::jsonb,
                                    concat('{', (jsonb_array_length(ut.day_chart)-1), '}')::text[],
                                    json_build_object(
                                        'day', ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'day',
                                        'imp', coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'imp')::text::integer,0),
                                        'spend', coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'spend')::text::float,0),
                                        'clicks', coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'clicks')::text::integer,0) + coalesce((Excluded.day_chart::json->0->'clicks')::text::integer,0),
                                        'conversions', coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'conversions')::text::integer,0),
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
                                        """),

        migrations.RunSQL("""
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
                         'imp', 0,
                         'spend', 0,
                         'clicks', 0,
                         'conversions', count(site_r."id"),
                         'cvr', 0,
                         'cpc', 0,
                         'ctr', 0)
                       from
                            rtb_conversion_tracker site_r
                       where site_r."AdvId"= page."AdvId"
                         and
                         site_r."Date" >= date_trunc('month',(select date from last_modified where type='lastPrecalculatedTrackerCron') - interval '1 month')
                         and
                         site_r."Date" < date_trunc('month',(select date from last_modified where type='lastPrecalculatedTrackerCron'))
                       group by site_r."Date"::timestamp::date
                       order by site_r."Date"::timestamp::date))) id
                from (
                      select
                        distinct "AdvId"
                      from
                        rtb_conversion_tracker
                      where
                        rtb_conversion_tracker."Date" >= date_trunc('month',(select date from last_modified where type='lastPrecalculatedTrackerCron') - interval '1 month')
                        and
                        rtb_conversion_tracker."Date" < date_trunc('month',(select date from last_modified where type='lastPrecalculatedTrackerCron'))
                     ) page
                ON CONFLICT (advertiser_id, type)
                  DO UPDATE SET
                     day_chart = case (ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'day')::text when (Excluded.day_chart::json->0->'day')::text
                                  then jsonb_set(
                                    ut.day_chart::jsonb,
                                    concat('{', (jsonb_array_length(ut.day_chart)-1), '}')::text[],
                                    json_build_object(
                                        'day', ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'day',
                                        'imp', coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'imp')::text::integer,0),
                                        'spend', coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'spend')::text::float,0),
                                        'clicks', coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'clicks')::text::integer,0),
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
                                            """),

        # cur_month

        migrations.RunSQL("""
                insert into ui_usual_advertisers_graph_tracker as ut (
                    advertiser_id,
                    type,
                    day_chart)
                  select
                  page."AdvId",
                  'cur_month',
                  array_to_json(array((select
                         json_build_object(
                         'day', site_r."Date"::timestamp::date,
                         'imp', count(site_r."id"),
                         'spend', sum(site_r."PricePaid"),
                         'clicks', 0,
                         'conversions', 0,
                         'cvr', 0,
                         'cpc', 0,
                         'ctr', 0)
                       from
                            rtb_impression_tracker site_r
                       where site_r."AdvId"= page."AdvId"
                         and
                         site_r."Date" >= date_trunc('month',(select date from last_modified where type='lastPrecalculatedTrackerCron'))
                         and
                         site_r."Date" <= (select date from last_modified where type='lastPrecalculatedTrackerCron')
                       group by site_r."Date"::timestamp::date
                       order by site_r."Date"::timestamp::date))) id
                from (
                      select
                        distinct "AdvId"
                      from
                        rtb_impression_tracker
                      where
                        "Date" >= date_trunc('month',(select date from last_modified where type='lastPrecalculatedTrackerCron'))
                        and
                        "Date" <= (select date from last_modified where type='lastPrecalculatedTrackerCron')
                     ) page;
                                        """),

        migrations.RunSQL("""
                insert into ui_usual_advertisers_graph_tracker as ut (
                    advertiser_id,
                    type,
                    day_chart)
                  select
                  page."AdvId",
                  'cur_month',
                  array_to_json(array((select
                         json_build_object(
                         'day', site_r."Date"::timestamp::date,
                         'imp', 0,
                         'spend', 0,
                         'clicks', count(site_r."id"),
                         'conversions', 0,
                         'cvr', 0,
                         'cpc', 0,
                         'ctr', 0)
                       from
                            rtb_click_tracker site_r
                       where site_r."AdvId"= page."AdvId"
                         and
                         site_r."Date" >= date_trunc('month',(select date from last_modified where type='lastPrecalculatedTrackerCron'))
                         and
                         site_r."Date" <= (select date from last_modified where type='lastPrecalculatedTrackerCron')
                       group by site_r."Date"::timestamp::date
                       order by site_r."Date"::timestamp::date))) id
                from (
                      select
                        distinct rtb_click_tracker."AdvId"
                      from
                        rtb_click_tracker
                      where
                        rtb_click_tracker."Date" >= date_trunc('month',(select date from last_modified where type='lastPrecalculatedTrackerCron') - interval '90 day')
                        and
                        rtb_click_tracker."Date" <= (select date from last_modified where type='lastPrecalculatedTrackerCron')
                     ) page
                ON CONFLICT (advertiser_id, type)
                  DO UPDATE SET
                     day_chart = case (ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'day')::text when (Excluded.day_chart::json->0->'day')::text
                                  then jsonb_set(
                                    ut.day_chart::jsonb,
                                    concat('{', (jsonb_array_length(ut.day_chart)-1), '}')::text[],
                                    json_build_object(
                                        'day', ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'day',
                                        'imp', coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'imp')::text::integer,0),
                                        'spend', coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'spend')::text::float,0),
                                        'clicks', coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'clicks')::text::integer,0) + coalesce((Excluded.day_chart::json->0->'clicks')::text::integer,0),
                                        'conversions', coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'conversions')::text::integer,0),
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
                                        """),

        migrations.RunSQL("""
                insert into ui_usual_advertisers_graph_tracker as ut (
                    advertiser_id,
                    type,
                    day_chart)
                  select
                  page."AdvId",
                  'cur_month',
                  array_to_json(array((select
                         json_build_object(
                         'day', site_r."Date"::timestamp::date,
                         'imp', 0,
                         'spend', 0,
                         'clicks', 0,
                         'conversions', count(site_r."id"),
                         'cvr', 0,
                         'cpc', 0,
                         'ctr', 0)
                       from
                            rtb_conversion_tracker site_r
                       where site_r."AdvId"= page."AdvId"
                         and
                         site_r."Date" >= date_trunc('month',(select date from last_modified where type='lastPrecalculatedTrackerCron'))
                         and
                         site_r."Date" <= (select date from last_modified where type='lastPrecalculatedTrackerCron')
                       group by site_r."Date"::timestamp::date
                       order by site_r."Date"::timestamp::date))) id
                from (
                      select
                        distinct "AdvId"
                      from
                        rtb_conversion_tracker
                      where
                        rtb_conversion_tracker."Date" >= date_trunc('month',(select date from last_modified where type='lastPrecalculatedTrackerCron'))
                        and
                        rtb_conversion_tracker."Date" <= (select date from last_modified where type='lastPrecalculatedTrackerCron')
                     ) page
                ON CONFLICT (advertiser_id, type)
                  DO UPDATE SET
                     day_chart = case (ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'day')::text when (Excluded.day_chart::json->0->'day')::text
                                  then jsonb_set(
                                    ut.day_chart::jsonb,
                                    concat('{', (jsonb_array_length(ut.day_chart)-1), '}')::text[],
                                    json_build_object(
                                        'day', ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'day',
                                        'imp', coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'imp')::text::integer,0),
                                        'spend', coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'spend')::text::float,0),
                                        'clicks', coalesce((ut.day_chart::json->(jsonb_array_length(ut.day_chart)-1)->'clicks')::text::integer,0),
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
                                            """),
    ]