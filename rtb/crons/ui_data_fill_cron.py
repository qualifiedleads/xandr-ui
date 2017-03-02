from rtb.models.ui_data_models import \
    UIUsualCampaignsGridDataAll, UIUsualCampaignsGridDataYesterday, UIUsualCampaignsGridDataLast3Days,\
    UIUsualCampaignsGridDataLast7Days, UIUsualCampaignsGridDataLast14Days, UIUsualCampaignsGridDataLast21Days,\
    UIUsualCampaignsGridDataCurMonth, UIUsualCampaignsGridDataLastMonth, UIUsualCampaignsGridDataLast90Days, \
    UIUsualCampaignsGraph

from rtb.models.ui_data_models import \
    UIUsualPlacementsGridDataAll, UIUsualPlacementsGridDataYesterday, UIUsualPlacementsGridDataLast3Days,\
    UIUsualPlacementsGridDataLast7Days, UIUsualPlacementsGridDataLast14Days, UIUsualPlacementsGridDataLast21Days,\
    UIUsualPlacementsGridDataCurMonth, UIUsualPlacementsGridDataLastMonth, UIUsualPlacementsGridDataLast90Days, \
    UIUsualPlacementsGraph

from rtb.models import SiteDomainPerformanceReport, NetworkAnalyticsReport_ByPlacement, Advertiser, Campaign
from datetime import timedelta, datetime
from django.db.models import Sum, When, Case, F, Q, FloatField
from django.db import connection
from django.utils import timezone
from rtb.models.placement_state import LastModified

def getSiteDomainsReportInfo(start_date, finish_date, newCampaigns=None, camp_id=None):
    if newCampaigns is None:
        queryRes = SiteDomainPerformanceReport.objects.raw("""
            select page.*,
      array((select
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
               AND site_r.hour >= '""" + str(start_date) + """'
               AND site_r.hour < '""" + str(finish_date) + """'
             group by site_r.campaign_id, site_r.day
             order by site_r.day)) id
    from (
          select distinct on (site_r1.campaign_id)
            site_r1.campaign_id,
            SUM(site_r1.imps) over (partition by site_r1.campaign_id) imp,
            SUM(site_r1.media_cost) over (partition by site_r1.campaign_id) spend,
            SUM(site_r1.clicks) over (partition by site_r1.campaign_id) clicks,
            (SUM(site_r1.post_view_convs) over (partition by site_r1.campaign_id) + SUM(site_r1.post_click_convs) over (partition by site_r1.campaign_id)) conversions,
            SUM(site_r1.imps_viewed) over (partition by site_r1.campaign_id) imps_viewed,
            SUM(site_r1.view_measured_imps) over (partition by site_r1.campaign_id) view_measured_imps
          FROM
            site_domain_performance_report site_r1
          WHERE
            site_r1.campaign_id=""" + str(camp_id) + """
            AND site_r1.hour >= '""" + str(start_date) + """'
            AND site_r1.hour < '""" + str(finish_date) + """'
          WINDOW w as (partition by site_r1.campaign_id order by site_r1.day desc)
         ) page;
            """)
    else:
        queryRes = SiteDomainPerformanceReport.objects.raw("""
                select page.*,
                case page.imp when 0 then 0 else page.spend / page.imp * 1000.0 end cpm,
                case page.imp when 0 then 0 else page.conversions::float / page.imp end cvr,
                case page.imp when 0 then 0 else page.clicks::float / page.imp end ctr,
                case page.clicks when 0 then 0 else page.spend / page.clicks end cpc,
                case page.imp when 0 then 0 else page.view_measured_imps::float / page.imp end view_measurement_rate,
                case page.view_measured_imps when 0 then 0 else page.imps_viewed::float / page.view_measured_imps end view_rate,
                array((select
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
                   AND site_r.day >= '""" + str(start_date) + """'
                   AND site_r.day < '""" + str(finish_date) + """'
                 group by site_r.campaign_id, site_r.day
                 order by site_r.day)) id
        from (
              select distinct on (site_r1.campaign_id)
                site_r1.campaign_id,
                SUM(site_r1.imps) over (partition by site_r1.campaign_id) imp,
                SUM(site_r1.media_cost) over (partition by site_r1.campaign_id) spend,
                SUM(site_r1.clicks) over (partition by site_r1.campaign_id) clicks,
                (SUM(site_r1.post_view_convs) over (partition by site_r1.campaign_id) + SUM(site_r1.post_click_convs) over (partition by site_r1.campaign_id))  conversions,
                SUM(site_r1.imps_viewed) over (partition by site_r1.campaign_id) imps_viewed,
                SUM(site_r1.view_measured_imps) over (partition by site_r1.campaign_id) view_measured_imps
              FROM
                site_domain_performance_report site_r1
              WHERE
                site_r1.campaign_id in """ + newCampaigns + """
                AND site_r1.day >= '""" + str(start_date) + """'
                AND site_r1.day < '""" + str(finish_date) + """'
              WINDOW w as (partition by site_r1.campaign_id order by site_r1.day desc)
             ) page;
                """)
    return queryRes


def getUsualAdvertiserGraphData(start_date, finish_date, advertiser_id, new_one=False):
    if new_one:
        queryRes = SiteDomainPerformanceReport.objects.raw("""
    select
      array(
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
        from site_domain_performance_report
        where
          advertiser_id=""" + str(advertiser_id) + """
        and
          day >= '""" + str(start_date) + """'
        and
          day < '""" + str(finish_date) + """'
        group by "day"
        order by "day"
      ) id;""")
    else:
        queryRes = SiteDomainPerformanceReport.objects.raw("""
        select
          array(
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
            from site_domain_performance_report
            where
              advertiser_id=""" + str(advertiser_id) + """
            and
              hour >= '""" + str(start_date) + """'
            and
              hour < '""" + str(finish_date) + """'
            group by "day"
            order by "day"
          ) id;""")
    try:
        queryRes[0].id[0]
        return queryRes[0]
    except:
        return None

def getNetworkAnalyticsPlacementInfo(start_date, finish_date, campaign_id, place_id, new_one=False):
    if new_one:
        queryRes = NetworkAnalyticsReport_ByPlacement.objects.raw("""
        select
          placement_id as id,
          sum(imps) imp,
          sum(clicks) clicks,
          sum("cost") spend,
          sum(total_convs) conversions,
          sum(imps_viewed) imps_viewed,
          sum(view_measured_imps) view_measured_imps,
          case sum(imps) when 0 then 0 else sum("cost") / sum(imps) * 1000.0 end cpm,
          case sum(imps) when 0 then 0 else sum(total_convs)::float / sum(imps) end cvr,
          case sum(imps) when 0 then 0 else sum(clicks)::float / sum(imps) end ctr,
          case sum(clicks) when 0 then 0 else sum("cost") / sum(clicks) end cpc,
          case sum(total_convs) when 0 then 0 else sum("cost") / sum(total_convs) end cpa,
          case sum(imps) when 0 then 0 else sum(view_measured_imps)::float / sum(imps) end view_measurement_rate,
          case sum(view_measured_imps) when 0 then 0 else sum(imps_viewed)::float / sum(view_measured_imps) end view_rate
        from
          network_analytics_report_by_placement
        where
          placement_id = """ + str(place_id) + """
        and
          campaign_id = """ + str(campaign_id) + """
        and
          "hour" >= '""" + str(start_date) + """'
        and
          "hour" < '""" + str(finish_date) + """'
        group by placement_id;
                """)
    else:
        queryRes = NetworkAnalyticsReport_ByPlacement.objects.raw("""
    select
      placement_id as id,
      sum(imps) imp,
      sum(clicks) clicks,
      sum("cost") spend,
      sum(total_convs) conversions,
      sum(imps_viewed) imps_viewed,
      sum(view_measured_imps) view_measured_imps
    from
      network_analytics_report_by_placement
    where
      placement_id = """ + str(place_id) + """
    and
      campaign_id = """ + str(campaign_id) + """
    and
      "hour" >= '""" + str(start_date) + """'
    and
      "hour" < '""" + str(finish_date) + """'
    group by placement_id;
            """)
    try:
        return queryRes[0]
    except:
        return None

def getUsualCampaignGraphData(start_date, finish_date, campaign_id):
    queryRes = NetworkAnalyticsReport_ByPlacement.objects.raw("""
select
  array(
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
    from network_analytics_report_by_placement
    where
      campaign_id=""" + str(campaign_id) + """
    and
      "hour" >= '""" + str(start_date) + """'
    and
      "hour" < '""" + str(finish_date) + """'
    group by "hour"::timestamp::date
    order by "hour"::timestamp::date
  ) id;
""")
    try:
        queryRes[0].id[0]
        return queryRes[0]
    except:
        return None

def fillUIGridDataCron():
    print "fillUIGridDataCron started: " + str(datetime.now())
    LastModified.objects.filter(type='hourlyTask') \
        .update(date=timezone.make_aware(datetime.now(), timezone.get_default_timezone()))
    modelsDict = {}
    modelsDict["yesterday"] = [UIUsualPlacementsGridDataYesterday, 1]
    modelsDict["last_3_days"] = [UIUsualPlacementsGridDataLast3Days, 3]
    modelsDict["last_7_days"] = [UIUsualPlacementsGridDataLast7Days, 7]
    modelsDict["last_14_days"] = [UIUsualPlacementsGridDataLast14Days, 14]
    modelsDict["last_21_days"] = [UIUsualPlacementsGridDataLast21Days, 21]
    modelsDict["last_90_days"] = [UIUsualPlacementsGridDataLast90Days, 90]

    newPlacements = {
        "all_time": [[], UIUsualPlacementsGridDataAll],
        "yesterday": [[], UIUsualPlacementsGridDataYesterday],
        "last_3_days": [[], UIUsualPlacementsGridDataLast3Days],
        "last_7_days": [[], UIUsualPlacementsGridDataLast7Days],
        "last_14_days": [[], UIUsualPlacementsGridDataLast14Days],
        "last_21_days": [[], UIUsualPlacementsGridDataLast21Days],
        "last_90_days": [[], UIUsualPlacementsGridDataLast90Days],
        "last_month": [[], UIUsualPlacementsGridDataLastMonth],
        "cur_month": [[], UIUsualPlacementsGridDataCurMonth]
    }

    allAdvertisers = Advertiser.objects.filter(
        ad_type="usualAds",
        grid_data_source="report"
    )

    allNewAdvertiserts = []
    allNewCampaigns = []
    for adv in allAdvertisers:
        LastModified.objects.filter(type='hourlyTask') \
            .update(date=timezone.make_aware(datetime.now(), timezone.get_default_timezone()))
        # USUAL ADV GRAPH
        #
        # ALL TIME DATA
        #
        prevData = UIUsualCampaignsGraph.objects.filter(
            advertiser_id=adv.id,
            type="all"
        )
        # creating
        if len(prevData) == 0:
            queryRes = getUsualAdvertiserGraphData(
                advertiser_id=adv.id,
                start_date=datetime.strptime("1970 01 01 00:00:00", "%Y %m %d %H:%M:%S"),
                finish_date=datetime.now().replace(hour=0, minute=0, second=0, microsecond=0),
                new_one=True
            )
            allNewAdvertiserts.append(UIUsualCampaignsGraph(
                advertiser_id=adv.id,
                type="all",
                evaluation_date=timezone.make_aware(
                    datetime.now().replace(hour=0, minute=0, second=0, microsecond=0),
                    timezone.get_default_timezone()
                ),
                window_start_date=timezone.make_aware(
                    datetime.strptime("1970 01 01 00:00:00", "%Y %m %d %H:%M:%S"),
                    timezone.get_default_timezone()
                ),
                day_chart=[] if queryRes is None else queryRes.id
            ))
        # updating
        else:
            if (datetime.now() - prevData[0].evaluation_date) >= timedelta(hours=1):
                queryRes = getUsualAdvertiserGraphData(
                    advertiser_id=adv.id,
                    start_date=prevData[0].evaluation_date,
                    finish_date=datetime.now().replace(minute=0, second=0, microsecond=0)
                )
                if queryRes is not None:
                    if prevData[0].day_chart:
                        if prevData[0].day_chart[len(prevData[0].day_chart) - 1]["day"] == queryRes.id[0]["day"]:
                            prevData[0].day_chart[len(prevData[0].day_chart) - 1]["imp"] += queryRes.id[0]["imp"]
                            prevData[0].day_chart[len(prevData[0].day_chart) - 1]["spend"] += queryRes.id[0]["spend"]
                            prevData[0].day_chart[len(prevData[0].day_chart) - 1]["clicks"] += queryRes.id[0]["clicks"]
                            prevData[0].day_chart[len(prevData[0].day_chart) - 1]["conversions"] += queryRes.id[0]["conversions"]

                            if prevData[0].day_chart[len(prevData[0].day_chart) - 1]["imp"] == 0:
                                prevData[0].day_chart[len(prevData[0].day_chart) - 1]["cvr"] = 0
                                prevData[0].day_chart[len(prevData[0].day_chart) - 1]["ctr"] = 0
                            else:
                                prevData[0].day_chart[len(prevData[0].day_chart) - 1]["cvr"] = float(
                                    prevData[0].day_chart[len(prevData[0].day_chart) - 1]["conversions"]) / prevData[0].day_chart[len(prevData[0].day_chart) - 1][
                                                                                   "imp"]
                                prevData[0].day_chart[len(prevData[0].day_chart) - 1]["ctr"] = float(
                                    prevData[0].day_chart[len(prevData[0].day_chart) - 1]["clicks"]) / prevData[0].day_chart[len(prevData[0].day_chart) - 1]["imp"]
                            prevData[0].day_chart[len(prevData[0].day_chart) - 1]["cpc"] = 0 if (
                            prevData[0].day_chart[len(prevData[0].day_chart) - 1]["clicks"] == 0) else (
                            prevData[0].day_chart[len(prevData[0].day_chart) - 1]["spend"] / prevData[0].day_chart[len(prevData[0].day_chart) - 1]["clicks"])
                            prevData[0].day_chart.extend(queryRes.id[1:])
                        else:
                            prevData[0].day_chart.extend(queryRes.id)
                    else:
                        prevData[0].day_chart.extend(queryRes.id)
                    prevData[0].evaluation_date = timezone.make_aware(
                        datetime.now().replace(minute=0, second=0, microsecond=0),
                        timezone.get_default_timezone()
                    )
                    try:
                        prevData[0].save()
                    except Exception, e:
                        print "Can not update " + str(prevData[0].advertiser_id) + " advertiser all time graph data. Error: " + str(e)
        LastModified.objects.filter(type='hourlyTask') \
            .update(date=timezone.make_aware(datetime.now(), timezone.get_default_timezone()))
        #
        # LAST N DAYS DATA
        #
        for type, info in modelsDict.iteritems():
            prevData = UIUsualCampaignsGraph.objects.filter(
                advertiser_id=adv.id,
                type=type
            )
            # creating
            if len(prevData) == 0:
                queryRes = getUsualAdvertiserGraphData(
                    advertiser_id=adv.id,
                    start_date=(datetime.now() - timedelta(days=info[1])).replace(hour=0, minute=0, second=0,
                                                                                  microsecond=0),
                    finish_date=datetime.now().replace(hour=0, minute=0, second=0, microsecond=0),
                    new_one=True
                )
                allNewAdvertiserts.append(UIUsualCampaignsGraph(
                    advertiser_id=adv.id,
                    type=type,
                    evaluation_date=timezone.make_aware(
                        datetime.now().replace(hour=0, minute=0, second=0, microsecond=0),
                        timezone.get_default_timezone()
                    ),
                    window_start_date=timezone.make_aware(
                        (datetime.now() - timedelta(days=info[1])).replace(hour=0, minute=0, second=0, microsecond=0),
                        timezone.get_default_timezone()
                    ),
                    day_chart=[] if queryRes is None else queryRes.id
                ))
            # updating
            else:
                if (datetime.now() - prevData[0].evaluation_date) >= timedelta(hours=1):
                    queryRes = getUsualAdvertiserGraphData(
                        advertiser_id=adv.id,
                        start_date=prevData[0].evaluation_date,
                        finish_date=datetime.now().replace(minute=0, second=0, microsecond=0)
                    )
                    if queryRes is not None:
                        # chart
                        # if new data is greater, then time period
                        if len(queryRes.id) >= (info[1] + 1):
                            prevData[0].day_chart = queryRes.id[-(info[1] + 1):]
                        else:
                            if prevData[0].day_chart:
                                # if old data don't fill time period
                                if queryRes.id[0]["day"] == prevData[0].day_chart[len(prevData[0].day_chart) - 1]["day"]:
                                    prevData[0].day_chart[len(prevData[0].day_chart) - 1]["imp"] += queryRes.id[0]["imp"]
                                    prevData[0].day_chart[len(prevData[0].day_chart) - 1]["spend"] += queryRes.id[0]["spend"]
                                    prevData[0].day_chart[len(prevData[0].day_chart) - 1]["clicks"] += queryRes.id[0]["clicks"]
                                    prevData[0].day_chart[len(prevData[0].day_chart) - 1]["conversions"] += queryRes.id[0]["conversions"]

                                    if prevData[0].day_chart[len(prevData[0].day_chart) - 1]["imp"] == 0:
                                        prevData[0].day_chart[len(prevData[0].day_chart) - 1]["cvr"] = 0
                                        prevData[0].day_chart[len(prevData[0].day_chart) - 1]["ctr"] = 0
                                    else:
                                        prevData[0].day_chart[len(prevData[0].day_chart) - 1]["cvr"] = float(
                                            prevData[0].day_chart[len(prevData[0].day_chart) - 1]["conversions"]) / \
                                                                                       prevData[0].day_chart[len(prevData[0].day_chart) - 1]["imp"]
                                        prevData[0].day_chart[len(prevData[0].day_chart) - 1]["ctr"] = float(
                                            prevData[0].day_chart[len(prevData[0].day_chart) - 1]["clicks"]) / \
                                                                                       prevData[0].day_chart[len(prevData[0].day_chart) - 1]["imp"]

                                    prevData[0].day_chart[len(prevData[0].day_chart) - 1]["cpc"] = 0 if (
                                    prevData[0].day_chart[len(prevData[0].day_chart) - 1]["clicks"] == 0) else (
                                        prevData[0].day_chart[len(prevData[0].day_chart) - 1]["spend"] / prevData[0].day_chart[len(prevData[0].day_chart) - 1][
                                            "clicks"])
                                    # cut and extend
                                    if (len(prevData[0].day_chart) + len(queryRes.id) - info[1] - 2) > 0:
                                        prevData[0].day_chart = prevData[0].day_chart[(len(prevData[0].day_chart) + len(queryRes.id) - info[1] - 2):]
                                    prevData[0].day_chart.extend(queryRes.id[1:])
                                else:
                                    if (len(prevData[0].day_chart) + len(queryRes.id) - info[1] - 1) > 0:
                                        prevData[0].day_chart = prevData[0].day_chart[(len(prevData[0].day_chart) + len(queryRes.id) - info[1] - 1):]
                                    prevData[0].day_chart.extend(queryRes.id)
                            else:
                                prevData[0].day_chart.extend(queryRes.id)

                        prevData[0].evaluation_date = timezone.make_aware(
                            datetime.now().replace(minute=0, second=0, microsecond=0),
                            timezone.get_default_timezone()
                        )

                        try:
                            prevData[0].save()
                        except Exception, e:
                            print "Can not update " + str(prevData[0].advertiser_id) + " advertiser " + type + " graph data. Error: " + str(e)
        LastModified.objects.filter(type='hourlyTask') \
            .update(date=timezone.make_aware(datetime.now(), timezone.get_default_timezone()))
        #
        # LAST MONTH
        #

        prevData = UIUsualCampaignsGraph.objects.filter(
            advertiser_id=adv.id,
            type="last_month"
        )
        # creating
        if len(prevData) == 0:
            queryRes = getUsualAdvertiserGraphData(
                advertiser_id=adv.id,
                start_date=(datetime.now().replace(day=1) - timedelta(days=1)).replace(day=1, hour=0, minute=0,
                                                                                       second=0, microsecond=0),
                finish_date=datetime.now().replace(day=1, hour=0, minute=0, second=0, microsecond=0),
                new_one=True
            )
            allNewAdvertiserts.append(UIUsualCampaignsGraph(
                advertiser_id=adv.id,
                type="last_month",
                evaluation_date=timezone.make_aware(
                    datetime.now().replace(day=1, hour=0, minute=0, second=0, microsecond=0)
                ),
                window_start_date=timezone.make_aware(
                    (datetime.now().replace(day=1) - timedelta(days=1)).replace(day=1, hour=0, minute=0,
                                                                                second=0, microsecond=0),
                    timezone.get_default_timezone()
                ),
                day_chart=[] if queryRes is None else queryRes.id
            ))
        # updating
        else:
            if (datetime.now().month - prevData[0].window_start_date.month) >= 2:
                queryRes = getUsualAdvertiserGraphData(
                    advertiser_id=adv.id,
                    start_date=(datetime.now().replace(day=1) - timedelta(days=1)).replace(day=1, hour=0, minute=0, second=0, microsecond=0),
                    finish_date=datetime.now().replace(day=1, hour=0, minute=0, second=0, microsecond=0)
                )
                if queryRes is not None:
                    prevData[0].day_chart = queryRes.id
                    prevData[0].window_start_date = timezone.make_aware(
                        (datetime.now().replace(day=1) - timedelta(days=1)).replace(day=1, hour=0, minute=0, second=0, microsecond=0),
                        timezone.get_default_timezone()
                    )
                    prevData[0].evaluation_date = timezone.make_aware(
                        datetime.now().replace(day=1, hour=0, minute=0, second=0, microsecond=0),
                        timezone.get_default_timezone()
                    )
                    try:
                        prevData[0].save()
                    except Exception, e:
                        print "Can not update " + str(prevData[0].advertiser_id) + " advertiser last month graph data. Error: " + str(e)
        LastModified.objects.filter(type='hourlyTask') \
            .update(date=timezone.make_aware(datetime.now(), timezone.get_default_timezone()))
        #
        # CUR MONTH
        #
        prevData = UIUsualCampaignsGraph.objects.filter(
            advertiser_id=adv.id,
            type="cur_month"
        )
        # creating
        if len(prevData) == 0:
            queryRes = getUsualAdvertiserGraphData(
                advertiser_id=adv.id,
                start_date=datetime.now().replace(day=1, hour=0, minute=0, second=0, microsecond=0),
                finish_date=datetime.now().replace(hour=0, minute=0, second=0, microsecond=0),
                new_one=True
            )
            allNewAdvertiserts.append(UIUsualCampaignsGraph(
                advertiser_id=adv.id,
                type="cur_month",
                evaluation_date=timezone.make_aware(
                    datetime.now().replace(hour=0, minute=0, second=0, microsecond=0),
                    timezone.get_default_timezone()
                ),
                window_start_date=timezone.make_aware(
                    datetime.now().replace(day=1, hour=0, minute=0, second=0, microsecond=0),
                    timezone.get_default_timezone()
                ),
                day_chart=[] if queryRes is None else queryRes.id
            ))
        # updating
        else:
            # if next month - change, if cur - cummulate
            if (datetime.now() - prevData[0].evaluation_date) >= timedelta(hours=1):
                if prevData[0].window_start_date.month == datetime.now().month:
                    queryRes = getUsualAdvertiserGraphData(
                        advertiser_id=adv.id,
                        start_date=prevData[0].evaluation_date,
                        finish_date=datetime.now().replace(minute=0, second=0, microsecond=0)
                    )
                    if queryRes is not None:
                        prevData[0].evaluation_date = datetime.now().replace(minute=0, second=0, microsecond=0)

                        # chart
                        # if old data don't fill time period
                        if prevData[0].day_chart:
                            if queryRes.id[0]["day"] == prevData[0].day_chart[len(prevData[0].day_chart) - 1]:
                                prevData[0].day_chart[len(prevData[0].day_chart) - 1]["imp"] += queryRes.id[0]["imp"]
                                prevData[0].day_chart[len(prevData[0].day_chart) - 1]["spend"] += queryRes.id[0]["spend"]
                                prevData[0].day_chart[len(prevData[0].day_chart) - 1]["clicks"] += queryRes.id[0]["clicks"]
                                prevData[0].day_chart[len(prevData[0].day_chart) - 1]["conversions"] += queryRes.id[0]["conversions"]

                                if prevData[0].day_chart[len(prevData[0].day_chart) - 1]["imp"] == 0:
                                    prevData[0].day_chart[len(prevData[0].day_chart) - 1]["cvr"] = 0
                                    prevData[0].day_chart[len(prevData[0].day_chart) - 1]["ctr"] = 0
                                else:
                                    prevData[0].day_chart[len(prevData[0].day_chart) - 1]["cvr"] = float(
                                        prevData[0].day_chart[len(prevData[0].day_chart) - 1]["conversions"]) / \
                                                                                   prevData[0].day_chart[len(prevData[0].day_chart) - 1]["imp"]
                                    prevData[0].day_chart[len(prevData[0].day_chart) - 1]["ctr"] = float(
                                        prevData[0].day_chart[len(prevData[0].day_chart) - 1]["clicks"]) / \
                                                                                   prevData[0].day_chart[len(prevData[0].day_chart) - 1]["imp"]

                                prevData[0].day_chart[len(prevData[0].day_chart) - 1]["cpc"] = 0 if (
                                    prevData[0].chart[len(prevData[0].day_chart) - 1]["clicks"] == 0) else (
                                    prevData[0].day_chart[len(prevData[0].day_chart) - 1]["spend"] / prevData[0].chart[len(prevData[0].day_chart) - 1]["clicks"])
                                # cut and extend
                                prevData[0].day_chart.extend(queryRes.id[1:])
                            else:
                                prevData[0].day_chart.extend(queryRes.id)
                        else:
                            prevData[0].day_chart.extend(queryRes.id)
                else:
                    LastModified.objects.filter(type='hourlyTask') \
                        .update(date=timezone.make_aware(datetime.now(), timezone.get_default_timezone()))
                    queryRes = getUsualAdvertiserGraphData(
                        advertiser_id=adv.id,
                        start_date=datetime.now().replace(day=1, hour=0, minute=0, second=0, microsecond=0),
                        finish_date=datetime.now().replace(minute=0, second=0, microsecond=0),
                    )
                    if queryRes is not None:
                        prevData[0].evaluation_date = timezone.make_aware(
                            datetime.now().replace(minute=0, second=0, microsecond=0),
                            timezone.get_default_timezone()
                        )

                        prevData[0].window_start_date = timezone.make_aware(
                            datetime.now().replace(day=1, hour=0, minute=0, second=0, microsecond=0),
                            timezone.get_default_timezone()
                        )

                        prevData[0].day_chart = queryRes.id
                try:
                    prevData[0].save()
                except Exception, e:
                    print "Can not update " + str(prevData[0].advertiser_id) + " advertiser current month data. Error: " + str(e)
        #
        # all usual placements
        #

        advertiserCampaigns = Campaign.objects.filter(advertiser_id=adv.id)
        for camp in advertiserCampaigns.iterator():
            allCampaignPlacements = NetworkAnalyticsReport_ByPlacement.objects.filter(
                campaign_id=camp.id
            ).values(
                'placement_id'
            ).distinct()
            for placement in allCampaignPlacements:
                LastModified.objects.filter(type='hourlyTask').update(date=timezone.make_aware(datetime.now(), timezone.get_default_timezone()))
                #
                # ALL TIME
                #
                prevData = UIUsualPlacementsGridDataAll.objects.filter(
                    campaign_id=camp.id,
                    placement_id=placement["placement_id"]
                )
                # creating
                if len(prevData) == 0:
                    queryRes = getNetworkAnalyticsPlacementInfo(
                        start_date="1970-01-01 00:00:00",
                        finish_date=datetime.now().replace(hour=0, minute=0, second=0, microsecond=0),
                        place_id=placement["placement_id"],
                        campaign_id=camp.id,
                        new_one=True
                    )
                    if queryRes is not None:
                        newPlacements["all_time"][0].append(UIUsualPlacementsGridDataAll(
                            campaign_id=camp.id,
                            placement_id=queryRes.id,
                            evaluation_date=timezone.make_aware(
                                datetime.now().replace(hour=0, minute=0, second=0, microsecond=0),
                                timezone.get_default_timezone()
                            ),
                            spent=queryRes.spend,
                            conversions=queryRes.conversions,
                            imps=queryRes.imp,
                            clicks=queryRes.clicks,
                            cpc=queryRes.cpc,
                            cpm=queryRes.cpm,
                            cvr=queryRes.cvr,
                            ctr=queryRes.ctr,
                            cpa=queryRes.cpa,
                            imps_viewed=queryRes.imps_viewed,
                            view_measured_imps=queryRes.view_measured_imps,
                            view_measurement_rate=queryRes.view_measurement_rate,
                            view_rate=queryRes.view_rate
                        ))
                # updating all days data
                else:
                    # check if less than an hour had pass
                    if (datetime.now() - prevData[0].evaluation_date) >= timedelta(hours=1):
                        queryRes = getNetworkAnalyticsPlacementInfo(
                            start_date=prevData[0].evaluation_date,
                            finish_date=datetime.now().replace(minute=0, second=0, microsecond=0),
                            place_id=prevData[0].placement_id,
                            campaign_id=camp.id
                        )
                        if queryRes is not None:
                            # cummulative data
                            prevData[0].imps += 0 if queryRes[0].imp is None else queryRes[0].imp
                            prevData[0].conversions += 0 if queryRes[0].conversions is None else queryRes[0].conversions
                            prevData[0].spent += 0 if queryRes[0].spend is None else queryRes[0].spend
                            prevData[0].clicks += 0 if queryRes[0].clicks is None else queryRes[0].clicks
                            prevData[0].imps_viewed += 0 if queryRes[0].imps_viewed is None else queryRes[0].imps_viewed
                            prevData[0].view_measured_imps += 0 if queryRes[0].view_measured_imps is None else queryRes[
                                0].view_measured_imps
                            # calculated rates
                            if prevData[0].imps == 0:
                                prevData[0].cpm = 0
                                prevData[0].cvr = 0
                                prevData[0].ctr = 0
                                prevData[0].view_measurement_rate = 0
                            else:
                                prevData[0].cpm = float(prevData[0].spent) / prevData[0].imps * 1000.0
                                prevData[0].cvr = float(prevData[0].conversions) / prevData[0].imps
                                prevData[0].ctr = float(prevData[0].clicks) / prevData[0].imps
                                prevData[0].view_measurement_rate = float(prevData[0].view_measured_imps) / prevData[0].imps
                            prevData[0].cpc = 0 if prevData[0].clicks == 0 else (float(prevData[0].spent) / prevData[0].clicks)
                            prevData[0].cpa = 0 if prevData[0].conversions == 0 else (float(prevData[0].spent) / prevData[0].conversions)
                            prevData[0].view_rate = 0 if prevData[0].view_measured_imps == 0 else (
                            float(prevData[0].imps_viewed) / prevData[0].view_measured_imps)

                            prevData[0].evaluation_date = datetime.now().replace(minute=0, second=0, microsecond=0)
                            try:
                                prevData[0].save()
                            except Exception, e:
                                print "Can not update " + str(prevData[0].placement_id) + " placement all time data. Error: " + str(e)
                #
                # LAST N DAYS
                #
                for type, info in modelsDict.iteritems():
                    LastModified.objects.filter(type='hourlyTask').update(date=timezone.make_aware(datetime.now(), timezone.get_default_timezone()))
                    prevData = info[0].objects.filter(
                        campaign_id=camp.id,
                        placement_id=placement["placement_id"]
                    )
                    # creating
                    if len(prevData) == 0:
                        queryRes = getNetworkAnalyticsPlacementInfo(
                            start_date=(datetime.now() - timedelta(days=info[1])).replace(hour=0, minute=0, second=0,
                                                                                          microsecond=0),
                            finish_date=datetime.now().replace(hour=0, minute=0, second=0, microsecond=0),
                            place_id=placement["placement_id"],
                            campaign_id=camp.id,
                            new_one=True
                        )

                        if queryRes is not None:
                            newPlacements[type][0].append(info[0](
                                campaign_id=camp.id,
                                placement_id=queryRes.id,
                                window_start_date=timezone.make_aware(
                                    (datetime.now() - timedelta(days=info[1])).replace(hour=0, minute=0, second=0, microsecond=0),
                                    timezone.get_default_timezone()
                                ),
                                evaluation_date=timezone.make_aware(
                                    datetime.now().replace(hour=0, minute=0, second=0, microsecond=0),
                                    timezone.get_default_timezone()
                                ),
                                spent=queryRes.spend,
                                conversions=queryRes.conversions,
                                imps=queryRes.imp,
                                clicks=queryRes.clicks,
                                cpc=queryRes.cpc,
                                cpm=queryRes.cpm,
                                cvr=queryRes.cvr,
                                ctr=queryRes.ctr,
                                cpa=queryRes.cpa,
                                imps_viewed=queryRes.imps_viewed,
                                view_measured_imps=queryRes.view_measured_imps,
                                view_measurement_rate=queryRes.view_measurement_rate,
                                view_rate=queryRes.view_rate
                            ))
                    # updating
                    else:
                        if (datetime.now() - prevData[0].evaluation_date) >= timedelta(hours=1):
                            queryRes = getNetworkAnalyticsPlacementInfo(
                                start_date=prevData[0].evaluation_date,
                                finish_date=datetime.now().replace(minute=0, second=0, microsecond=0),
                                place_id=prevData[0].placement_id,
                                campaign_id=camp.id
                            )
                            if queryRes is not None:
                                # cummulative data
                                prevData[0].imps += queryRes[0].imp
                                prevData[0].conversions += queryRes[0].conversions
                                prevData[0].spent += queryRes[0].spend
                                prevData[0].clicks += queryRes[0].clicks
                                prevData[0].imps_viewed += queryRes[0].imps_viewed
                                prevData[0].view_measured_imps += queryRes[0].view_measured_imps
                                # check if need to sub days
                                if (datetime.now() - prevData[0].window_start_date) >= timedelta(days=info[1] + 1):
                                    # data for sub
                                    queryRes = getNetworkAnalyticsPlacementInfo(
                                        start_date=prevData[0].window_start_date,
                                        finish_date=(datetime.now() - timedelta(days=info[1])).replace(hour=0, minute=0,
                                                                                                       second=0,
                                                                                                       microsecond=0),
                                        place_id=prevData[0].placement_id
                                    )
                                    LastModified.objects.filter(type='hourlyTask').update(date=timezone.make_aware(datetime.now(), timezone.get_default_timezone()))
                                    if queryRes is not None:
                                        # cummulative data
                                        prevData[0].imps -= queryRes.imp
                                        prevData[0].conversions -= queryRes.conversions
                                        prevData[0].spent -= queryRes.spend
                                        prevData[0].clicks -= queryRes.clicks
                                        prevData[0].imps_viewed -= queryRes.imps_viewed
                                        prevData[0].view_measured_imps -= queryRes.view_measured_imps
                                # calculated rates
                                if prevData[0].imps == 0:
                                    prevData[0].cpm = 0
                                    prevData[0].cvr = 0
                                    prevData[0].ctr = 0
                                    prevData[0].view_measurement_rate = 0
                                else:
                                    prevData[0].cpm = float(prevData[0].spent) / prevData[0].imps * 1000.0
                                    prevData[0].cvr = float(prevData[0].conversions) / prevData[0].imps
                                    prevData[0].ctr = float(prevData[0].clicks) / prevData[0].imps
                                    prevData[0].view_measurement_rate = float(prevData[0].view_measured_imps) / prevData[0].imps
                                prevData[0].cpa = 0 if prevData[0].conversions == 0 else (float(prevData[0].spent) / prevData[0].conversions)
                                prevData[0].cpc = 0 if prevData[0].clicks == 0 else (float(prevData[0].spent) / prevData[0].clicks)
                                prevData[0].view_rate = 0 if prevData[0].view_measured_imps == 0 else (
                                float(prevData[0].imps_viewed) / prevData[0].view_measured_imps)

                                prevData[0].evaluation_date = timezone.make_aware(
                                    datetime.now().replace(minute=0, second=0, microsecond=0),
                                    timezone.get_default_timezone()
                                )

                                prevData[0].window_start_date = timezone.make_aware(
                                    (datetime.now() - timedelta(days=info[1])).replace(hour=0, minute=0, second=0, microsecond=0),
                                    timezone.get_default_timezone()
                                )

                                try:
                                    prevData[0].save()
                                except Exception, e:
                                    print "Can not update " + str(prevData[0].placement_id) + " placement " + str(
                                        type) + " data. Error: " + str(e)
                #
                # LAST MONTH
                #
                LastModified.objects.filter(type='hourlyTask').update(date=timezone.make_aware(datetime.now(), timezone.get_default_timezone()))
                prevData = UIUsualPlacementsGridDataLastMonth.objects.filter(
                    campaign_id=camp.id,
                    placement_id=placement["placement_id"]
                )
                # creating
                if len(prevData) == 0:
                    queryRes = getNetworkAnalyticsPlacementInfo(
                        start_date=(datetime.now().replace(day=1) - timedelta(days=1)).replace(day=1, hour=0, minute=0,
                                                                                               second=0, microsecond=0),
                        finish_date=datetime.now().replace(day=1, hour=0, minute=0, second=0, microsecond=0),
                        campaign_id=camp.id,
                        place_id=placement["placement_id"],
                        new_one=True
                    )
                    if queryRes is not None:
                        newPlacements["last_month"][0].append(UIUsualPlacementsGridDataLastMonth(
                            campaign_id=camp.id,
                            placement_id=placement["placement_id"],
                            evaluation_date=timezone.make_aware(
                                datetime.now().replace(minute=0, second=0, microsecond=0),
                                timezone.get_default_timezone()
                            ),
                            window_start_date=timezone.make_aware(
                                (datetime.now().replace(day=1) - timedelta(days=1)).replace(day=1, hour=0, minute=0,
                                                                                            second=0,
                                                                                            microsecond=0),
                                timezone.get_default_timezone()
                            ),
                            spent=queryRes.spend,
                            conversions=queryRes.conversions,
                            imps=queryRes.imp,
                            clicks=queryRes.clicks,
                            cpc=queryRes.cpc,
                            cpm=queryRes.cpm,
                            cvr=queryRes.cvr,
                            ctr=queryRes.ctr,
                            cpa=queryRes.cpa,
                            imps_viewed=queryRes.imps_viewed,
                            view_measured_imps=queryRes.view_measured_imps,
                            view_measurement_rate=queryRes.view_measurement_rate,
                            view_rate=queryRes.view_rate
                        ))
                # updating
                else:
                    # check if less than a month had pass
                    if (datetime.now().month - prevData[0].window_start_date.month) >= 2:
                        queryRes = getNetworkAnalyticsPlacementInfo(
                            start_date=(datetime.now().replace(day=1) - timedelta(days=1)).replace(day=1, hour=0, minute=0,
                                                                                                   second=0, microsecond=0),
                            finish_date=datetime.now().replace(day=1, hour=0, minute=0, second=0, microsecond=0),
                            campaign_id=camp.id,
                            place_id=prevData[0].placement_id
                        )
                        if queryRes is not None:
                            # cummulative data
                            prevData[0].imps = queryRes[0].imp
                            prevData[0].conversions = queryRes[0].conversions
                            prevData[0].spent = queryRes[0].spend
                            prevData[0].clicks = queryRes[0].clicks
                            prevData[0].imps_viewed = queryRes[0].imps_viewed
                            prevData[0].view_measured_imps = queryRes[0].view_measured_imps
                            # calculated rates
                            if prevData[0].imps == 0:
                                prevData[0].cpm = 0
                                prevData[0].cvr = 0
                                prevData[0].ctr = 0
                                prevData[0].view_measurement_rate = 0
                            else:
                                prevData[0].cpm = float(prevData[0].spent) / prevData[0].imps * 1000.0
                                prevData[0].cvr = float(prevData[0].conversions) / prevData[0].imps
                                prevData[0].ctr = float(prevData[0].clicks) / prevData[0].imps
                                prevData[0].view_measurement_rate = float(prevData[0].view_measured_imps) / prevData[0].imps
                            prevData[0].cpa = 0 if prevData[0].conversions == 0 else (float(prevData[0].spent) / prevData[0].conversions)
                            prevData[0].cpc = 0 if prevData[0].clicks == 0 else (float(prevData[0].spent) / prevData[0].clicks)
                            prevData[0].view_rate = 0 if prevData[0].view_measured_imps == 0 else (
                            float(prevData[0].imps_viewed) / prevData[0].view_measured_imps)

                            prevData[0].evaluation_date = timezone.make_aware(
                                datetime.now().replace(minute=0, second=0, microsecond=0),
                                timezone.get_default_timezone()
                            )

                            prevData[0].window_start_date = timezone.make_aware(
                                (datetime.now().replace(day=1) - timedelta(days=1)).replace(day=1, hour=0, minute=0, second=0, microsecond=0),
                                timezone.get_default_timezone()
                            )

                            try:
                                prevData[0].save()
                            except Exception, e:
                                print "Can not update " + str(prevData[0].placement_id) + " placement last month data. Error: " + str(e)

                #
                # CUR MONTH
                #
                LastModified.objects.filter(type='hourlyTask').update(date=timezone.make_aware(datetime.now(), timezone.get_default_timezone()))
                prevData = UIUsualPlacementsGridDataCurMonth.objects.filter(
                    campaign_id=camp.id,
                    placement_id=placement["placement_id"]
                )
                # creating
                if len(prevData) == 0:
                    queryRes = getNetworkAnalyticsPlacementInfo(
                        start_date=datetime.now().replace(day=1, hour=0, minute=0, second=0, microsecond=0),
                        finish_date=datetime.now().replace(hour=0, minute=0, second=0, microsecond=0),
                        campaign_id=camp.id,
                        place_id=placement["placement_id"],
                        new_one=True
                    )
                    if queryRes is not None:
                        newPlacements["cur_month"][0].append(UIUsualPlacementsGridDataCurMonth(
                            campaign_id=camp.id,
                            placement_id=queryRes.id,
                            evaluation_date=timezone.make_aware(
                                datetime.now().replace(hour=0, minute=0, second=0, microsecond=0),
                                timezone.get_default_timezone()
                            ),
                            window_start_date=timezone.make_aware(
                                datetime.now().replace(day=1, hour=0, minute=0, second=0, microsecond=0),
                                timezone.get_default_timezone()
                            ),
                            spent=queryRes.spend,
                            conversions=queryRes.conversions,
                            imps=queryRes.imp,
                            clicks=queryRes.clicks,
                            cpc=queryRes.cpc,
                            cpm=queryRes.cpm,
                            cvr=queryRes.cvr,
                            ctr=queryRes.ctr,
                            cpa=queryRes.cpa,
                            imps_viewed=queryRes.imps_viewed,
                            view_measured_imps=queryRes.view_measured_imps,
                            view_measurement_rate=queryRes.view_measurement_rate,
                            view_rate=queryRes.view_rate
                        ))
                # updating
                else:
                    # check if less than an hour had pass
                    if (datetime.now() - prevData[0].evaluation_date) >= timedelta(hours=1):
                        # if next month - change, if cur - cummulate
                        if prevData[0].window_start_date.month == datetime.now().month:
                            queryRes = getNetworkAnalyticsPlacementInfo(
                                start_date=prevData[0].evaluation_date,
                                finish_date=datetime.now().replace(minute=0, second=0, microsecond=0),
                                campaign_id=camp.id,
                                place_id=prevData[0].placement_id
                            )
                            if queryRes is not None:
                                # cummulative data
                                prevData[0].imps += queryRes[0].imp
                                prevData[0].conversions += queryRes[0].conversions
                                prevData[0].spent += queryRes[0].spend
                                prevData[0].clicks += queryRes[0].clicks
                                prevData[0].imps_viewed += queryRes[0].imps_viewed
                                prevData[0].view_measured_imps += queryRes[0].view_measured_imps
                                # calculated rates
                                if prevData[0].imps == 0:
                                    prevData[0].cpm = 0
                                    prevData[0].cvr = 0
                                    prevData[0].ctr = 0
                                    prevData[0].view_measurement_rate = 0
                                else:
                                    prevData[0].cpm = float(prevData[0].spent) / prevData[0].imps * 1000.0
                                    prevData[0].cvr = float(prevData[0].conversions) / prevData[0].imps
                                    prevData[0].ctr = float(prevData[0].clicks) / prevData[0].imps
                                    prevData[0].view_measurement_rate = float(prevData[0].view_measured_imps) / prevData[0].imps
                                prevData[0].cpa = 0 if prevData[0].conversions == 0 else (float(prevData[0].spent) / prevData[0].conversions)
                                prevData[0].cpc = 0 if prevData[0].clicks == 0 else (float(prevData[0].spent) / prevData[0].clicks)
                                prevData[0].view_rate = 0 if prevData[0].view_measured_imps == 0 else (
                                float(prevData[0].imps_viewed) / prevData[0].view_measured_imps)

                                prevData[0].evaluation_date = timezone.make_aware(
                                    datetime.now().replace(minute=0, second=0, microsecond=0),
                                    timezone.get_default_timezone()
                                )

                                try:
                                    prevData[0].save()
                                except Exception, e:
                                    print "Can not update " + str(
                                        prevData[0].placement_id) + " placement current month data. Error: " + str(e)
                        else:
                            queryRes = getNetworkAnalyticsPlacementInfo(
                                start_date=datetime.now().replace(day=1, hour=0, minute=0, second=0, microsecond=0),
                                finish_date=datetime.now().replace(minute=0, second=0, microsecond=0),
                                campaign_id=camp.id,
                                place_id=prevData[0].placement_id
                            )
                            if queryRes is not None:
                                # cummulative data
                                prevData[0].imps = queryRes[0].imp
                                prevData[0].conversions = queryRes[0].conversions
                                prevData[0].spent = queryRes[0].spend
                                prevData[0].clicks = queryRes[0].clicks
                                prevData[0].imps_viewed = queryRes[0].imps_viewed
                                prevData[0].view_measured_imps = queryRes[0].view_measured_imps
                                # calculated rates
                                if prevData[0].imps == 0:
                                    prevData[0].cpm = 0
                                    prevData[0].cvr = 0
                                    prevData[0].ctr = 0
                                    prevData[0].view_measurement_rate = 0
                                else:
                                    prevData[0].cpm = float(prevData[0].spent) / prevData[0].imps * 1000.0
                                    prevData[0].cvr = float(prevData[0].conversions) / prevData[0].imps
                                    prevData[0].ctr = float(prevData[0].clicks) / prevData[0].imps
                                    prevData[0].view_measurement_rate = float(prevData[0].view_measured_imps) / prevData[0].imps
                                prevData[0].cpa = 0 if prevData[0].conversions == 0 else (float(prevData[0].spent) / prevData[0].conversions)
                                prevData[0].cpc = 0 if prevData[0].clicks == 0 else (float(prevData[0].spent) / prevData[0].clicks)
                                prevData[0].view_rate = 0 if prevData[0].view_measured_imps == 0 else (
                                float(prevData[0].imps_viewed) / prevData[0].view_measured_imps)

                                prevData[0].evaluation_date = timezone.make_aware(
                                    datetime.now().replace(minute=0, second=0, microsecond=0),
                                    timezone.get_default_timezone()
                                )

                                prevData[0].window_start_date = timezone.make_aware(
                                    datetime.now().replace(day=1, hour=0, minute=0, second=0, microsecond=0),
                                    timezone.get_default_timezone()
                                )

                                try:
                                    prevData[0].save()
                                except Exception, e:
                                    print "Can not update " + str(
                                        prevData[0].placement_id) + " placement current month data. Error: " + str(e)

            #
            # CAMPAIGN GRAPH
            #
            LastModified.objects.filter(type='hourlyTask') \
                .update(date=timezone.make_aware(datetime.now(), timezone.get_default_timezone()))
            #
            # ALL TIME DATA
            #
            prevData = UIUsualPlacementsGraph.objects.filter(
                campaign_id=camp.id,
                type="all"
            )

            # creating
            if len(prevData) == 0:
                queryRes = getUsualCampaignGraphData(
                    campaign_id=camp.id,
                    start_date=datetime.strptime("1970 01 01 00:00:00", "%Y %m %d %H:%M:%S"),
                    finish_date=datetime.now().replace(minute=0, second=0, microsecond=0)
                )
                allNewCampaigns.append(UIUsualPlacementsGraph(
                    campaign_id=camp.id,
                    type="all",
                    evaluation_date=timezone.make_aware(
                        datetime.now().replace(minute=0, second=0, microsecond=0),
                        timezone.get_default_timezone()
                    ),
                    window_start_date=timezone.make_aware(
                        datetime.strptime("1970 01 01 00:00:00", "%Y %m %d %H:%M:%S"),
                        timezone.get_default_timezone()
                    ),
                    day_chart=[] if queryRes is None else queryRes.id
                ))
            # updating
            else:
                if (datetime.now() - prevData[0].evaluation_date) >= timedelta(hours=1):
                    queryRes = UIUsualPlacementsGraph(
                        campaign_id=camp.id,
                        start_date=prevData[0].evaluation_date,
                        finish_date=datetime.now().replace(minute=0, second=0, microsecond=0)
                    )
                    if queryRes is not None:
                        if prevData[0].day_chart:
                            if prevData[0].day_chart[len(prevData[0].day_chart) - 1]["day"] == queryRes.id[0]["day"]:
                                prevData[0].day_chart[len(prevData[0].day_chart) - 1]["impression"] += queryRes.id[0]["impression"]
                                prevData[0].day_chart[len(prevData[0].day_chart) - 1]["mediaspent"] += queryRes.id[0]["mediaspent"]
                                prevData[0].day_chart[len(prevData[0].day_chart) - 1]["clicks"] += queryRes.id[0]["clicks"]
                                prevData[0].day_chart[len(prevData[0].day_chart) - 1]["conversions"] += queryRes.id[0]["conversions"]

                                prevData[0].day_chart[len(prevData[0].day_chart) - 1]["cpa"] = 0 if prevData[0].day_chart[len(prevData[0].day_chart) - 1]["conversions"] == 0 else(prevData[0].day_chart[len(prevData[0].day_chart) - 1]["mediaspent"] / prevData[0].day_chart[len(prevData[0].day_chart) - 1]["conversions"])
                                prevData[0].day_chart[len(prevData[0].day_chart) - 1]["cpc"] = 0 if prevData[0].day_chart[len(prevData[0].day_chart) - 1]["clicks"] == 0 else(prevData[0].day_chart[len(prevData[0].day_chart) - 1]["mediaspent"] / prevData[0].day_chart[len(prevData[0].day_chart) - 1]["clicks"])
                                prevData[0].day_chart[len(prevData[0].day_chart) - 1]["ctr"] = 0 if prevData[0].day_chart[len(prevData[0].day_chart) - 1]["imp"] == 0 else(prevData[0].day_chart[len(prevData[0].day_chart) - 1]["clicks"] / prevData[0].day_chart[len(prevData[0].day_chart) - 1]["impression"])

                                prevData[0].day_chart.extend(queryRes.id[1:])
                            else:
                                prevData[0].day_chart.extend(queryRes.id)
                        else:
                            prevData[0].day_chart.extend(queryRes.id)

                        prevData[0].evaluation_date = timezone.make_aware(
                            datetime.now().replace(minute=0, second=0, microsecond=0),
                            timezone.get_default_timezone()
                        )
                        try:
                            prevData[0].save()
                        except Exception, e:
                            print "Can not update " + str(prevData[0].campaign_id) + " campaign graph all time graph data. Error: " + str(e)
            LastModified.objects.filter(type='hourlyTask') \
                .update(date=timezone.make_aware(datetime.now(), timezone.get_default_timezone()))
            #
            # LAST N DAYS
            #
            for type, info in modelsDict.iteritems():
                prevData = UIUsualPlacementsGraph.objects.filter(
                    campaign_id=camp.id,
                    type=type
                )
                # creating
                if len(prevData) == 0:
                    queryRes = getUsualCampaignGraphData(
                        campaign_id=camp.id,
                        start_date=(datetime.now() - timedelta(days=info[1])).replace(hour=0, minute=0, second=0,
                                                                                      microsecond=0),
                        finish_date=datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
                    )
                    allNewCampaigns.append(UIUsualPlacementsGraph(
                        campaign_id=camp.id,
                        type=type,
                        evaluation_date=timezone.make_aware(
                            datetime.now().replace(hour=0, minute=0, second=0, microsecond=0),
                            timezone.get_default_timezone()
                        ),
                        window_start_date=timezone.make_aware(
                            (datetime.now() - timedelta(days=info[1])).replace(hour=0, minute=0, second=0,
                                                                               microsecond=0),
                            timezone.get_default_timezone()
                        ),
                        day_chart=[] if queryRes is None else queryRes.id
                    ))
                # updating
                else:
                    if (datetime.now() - prevData[0].evaluation_date) >= timedelta(hours=1):
                        queryRes = getUsualCampaignGraphData(
                            campaign_id=camp.id,
                            start_date=prevData[0].evaluation_date,
                            finish_date=datetime.now().replace(minute=0, second=0, microsecond=0)
                        )
                        if queryRes is not None:
                            # chart
                            # if new data is greater, then time period
                            if len(queryRes.id) >= (info[1] + 1):
                                prevData[0].day_chart = queryRes.id[-(info[1] + 1):]
                            else:
                                if prevData[0].day_chart:
                                    # if old data don't fill time period
                                    if queryRes.id[0]["day"] == prevData[0].day_chart[len(prevData[0].day_chart) - 1]["day"]:
                                        prevData[0].day_chart[len(prevData[0].day_chart) - 1]["impression"] += queryRes.id[0][
                                            "impression"]
                                        prevData[0].day_chart[len(prevData[0].day_chart) - 1]["mediaspent"] += queryRes.id[0][
                                            "mediaspent"]
                                        prevData[0].day_chart[len(prevData[0].day_chart) - 1]["clicks"] += queryRes.id[0][
                                            "clicks"]
                                        prevData[0].day_chart[len(prevData[0].day_chart) - 1]["conversions"] += queryRes.id[0]["conversions"]

                                        prevData[0].day_chart[len(prevData[0].day_chart) - 1]["cpa"] = 0 if prevData[0].day_chart[len(prevData[0].day_chart) - 1]["conversions"] == 0 else(prevData[0].day_chart[len(prevData[0].day_chart) - 1]["mediaspent"] / prevData[0].day_chart[len(prevData[0].day_chart) - 1]["conversions"])
                                        prevData[0].day_chart[len(prevData[0].day_chart) - 1]["cpc"] = 0 if prevData[0].day_chart[len(prevData[0].day_chart) - 1]["clicks"] == 0 else(prevData[0].day_chart[len(prevData[0].day_chart) - 1]["mediaspent"] / prevData[0].day_chart[len(prevData[0].day_chart) - 1]["clicks"])
                                        prevData[0].day_chart[len(prevData[0].day_chart) - 1]["ctr"] = 0 if prevData[0].day_chart[len(prevData[0].day_chart) - 1]["impression"] == 0 else(prevData[0].day_chart[len(prevData[0].day_chart) - 1]["clicks"] / prevData[0].day_chart[len(prevData[0].day_chart) - 1]["impression"])

                                        # cut and extend
                                        if (len(prevData[0].day_chart) + len(queryRes.id) - info[1] - 2) > 0:
                                            prevData[0].day_chart = prevData[0].day_chart[(len(prevData[0].day_chart) + len(queryRes.id) - info - 2):]
                                        prevData[0].day_chart.extend(queryRes.id[1:])
                                    else:
                                        if (len(prevData[0].day_chart) + len(queryRes.id) - info[1] - 1) > 0:
                                            prevData[0].day_chart = prevData[0].day_chart[(
                                            len(prevData[0].day_chart) + len(queryRes.id) - info[1] - 1):]
                                        prevData[0].day_chart.extend(queryRes.id)
                                else:
                                    prevData[0].day_chart.extend(queryRes.id)

                            prevData[0].evaluation_date = timezone.make_aware(
                                datetime.now().replace(minute=0, second=0, microsecond=0),
                                timezone.get_default_timezone()
                            )
                            try:
                                prevData[0].save()
                            except Exception, e:
                                print "Can not update " + str(prevData[0].campaign_id) + " campaign " + type + " graph data. Error: " + str(e)
            LastModified.objects.filter(type='hourlyTask').update(date=timezone.make_aware(datetime.now(), timezone.get_default_timezone()))
            #
            # LAST MONTH
            #
            prevData = UIUsualPlacementsGraph.objects.filter(
                campaign_id=camp.id,
                type="last_month"
            )
            # creating
            if len(prevData) == 0:
                queryRes = getUsualCampaignGraphData(
                    campaign_id=camp.id,
                    start_date=(datetime.now().replace(day=1) - timedelta(days=1)).replace(day=1, hour=0, minute=0,
                                                                                           second=0, microsecond=0),
                    finish_date=datetime.now().replace(day=1, hour=0, minute=0, second=0, microsecond=0)
                )
                allNewCampaigns.append(UIUsualPlacementsGraph(
                    campaign_id=camp.id,
                    type="last_month",
                    evaluation_date=timezone.make_aware(
                        datetime.now().replace(day=1, hour=0, minute=0, second=0, microsecond=0)
                    ),
                    window_start_date=timezone.make_aware(
                        (datetime.now().replace(day=1) - timedelta(days=1)).replace(day=1, hour=0, minute=0,
                                                                                    second=0, microsecond=0),
                        timezone.get_default_timezone()
                    ),
                    day_chart=[] if queryRes is None else queryRes.id
                ))
            # updating
            else:
                if (datetime.now().month - prevData[0].window_start_date.month) >= 2:
                    queryRes = getUsualCampaignGraphData(
                        start_date=(datetime.now().replace(day=1) - timedelta(days=1)).replace(day=1, hour=0, minute=0,
                                                                                               second=0, microsecond=0),
                        finish_date=datetime.now().replace(day=1, hour=0, minute=0, second=0, microsecond=0),
                        campaign_id=prevData[0].campaign_id
                    )
                    if queryRes is not None:
                        prevData[0].day_chart = queryRes.id
                        prevData[0].window_start_date = timezone.make_aware(
                            (datetime.now().replace(day=1) - timedelta(days=1)).replace(day=1, hour=0, minute=0, second=0, microsecond=0),
                            timezone.get_default_timezone()
                        )
                        prevData[0].evaluation_date = timezone.make_aware(
                            datetime.now().replace(minute=0, second=0, microsecond=0),
                            timezone.get_default_timezone()
                        )
                        try:
                            prevData[0].save()
                        except Exception, e:
                            print "Can not update " + str(
                                prevData[0].campaign_id) + " advertiser last month data. Error: " + str(e)
            LastModified.objects.filter(type='hourlyTask') \
                .update(date=timezone.make_aware(datetime.now(), timezone.get_default_timezone()))
            #
            # CUR MONTH
            #
            prevData = UIUsualPlacementsGraph.objects.filter(
                campaign_id=camp.id,
                type="cur_month"
            )
            # creating
            if len(prevData) == 0:
                queryRes = getUsualCampaignGraphData(
                    campaign_id=camp.id,
                    start_date=datetime.now().replace(day=1, hour=0, minute=0, second=0, microsecond=0),
                    finish_date=datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
                )
                if queryRes is None:
                    allNewCampaigns.append(UIUsualPlacementsGraph(
                        campaign_id=camp.id,
                        type="cur_month",
                        evaluation_date=timezone.make_aware(
                            datetime.now().replace(hour=0, minute=0, second=0, microsecond=0),
                            timezone.get_default_timezone()
                        ),
                        window_start_date=timezone.make_aware(
                            datetime.now().replace(day=1, hour=0, minute=0, second=0, microsecond=0),
                            timezone.get_default_timezone()
                        ),
                        day_chart=[] if queryRes is None else queryRes.id
                    ))
            # updating
            else:
                # if next month - change, if cur - cummulate
                if (datetime.now() - prevData[0].evaluation_date) >= timedelta(hours=1):
                    if prevData[0].window_start_date.month == datetime.now().month:
                        queryRes = getUsualCampaignGraphData(
                            campaign_id=camp.id,
                            start_date=prevData[0].evaluation_date,
                            finish_date=datetime.now().replace(minute=0, second=0, microsecond=0)
                        )
                        if queryRes is not None:
                            prevData[0].evaluation_date = datetime.now().replace(minute=0, second=0, microsecond=0)

                            # chart
                            if prevData[0].day_chart:
                                # if old data don't fill time period
                                if queryRes.id[0]["day"] == prevData[0].day_chart[len(prevData[0].day_chart) - 1]:
                                    prevData[0].day_chart[len(prevData[0].day_chart) - 1]["impression"] += queryRes.id[0]["impression"]
                                    prevData[0].day_chart[len(prevData[0].day_chart) - 1]["mediaspent"] += queryRes.id[0][
                                        "mediaspent"]
                                    prevData[0].day_chart[len(prevData[0].day_chart) - 1]["clicks"] += queryRes.id[0][
                                        "clicks"]
                                    prevData[0].day_chart[len(prevData[0].day_chart) - 1]["conversions"] += queryRes.id[0][
                                        "conversions"]

                                    prevData[0].day_chart[len(prevData[0].day_chart) - 1]["cpa"] = 0 if prevData[0].day_chart[len(prevData[0].day_chart) - 1]["conversions"] == 0 else (prevData[0].day_chart[len(prevData[0].day_chart) - 1]["mediaspent"] / prevData[0].day_chart[len(prevData[0].day_chart) - 1]["conversions"])
                                    prevData[0].day_chart[len(prevData[0].day_chart) - 1]["cpc"] = 0 if prevData[0].day_chart[len(prevData[0].day_chart) - 1]["clicks"] == 0 else (prevData[0].day_chart[len(prevData[0].day_chart) - 1]["mediaspent"] / prevData[0].day_chart[len(prevData[0].day_chart) - 1]["clicks"])
                                    prevData[0].day_chart[len(prevData[0].day_chart) - 1]["ctr"] = 0 if prevData[0].day_chart[len(prevData[0].day_chart) - 1]["impression"] == 0 else (prevData[0].day_chart[len(prevData[0].day_chart) - 1]["clicks"] / prevData[0].day_chart[len(prevData[0].day_chart) - 1]["impression"])

                                    # cut and extend
                                    prevData[0].day_chart.extend(queryRes.id[1:])
                                else:
                                    prevData[0].day_chart.extend(queryRes.id)
                            else:
                                prevData[0].day_chart.extend(queryRes.id)
                    else:
                        LastModified.objects.filter(type='hourlyTask').update(date=timezone.make_aware(datetime.now(), timezone.get_default_timezone()))
                        queryRes = getUsualCampaignGraphData(
                            campaign_id=prevData[0].campaign_id,
                            start_date=datetime.now().replace(day=1, hour=0, minute=0, second=0, microsecond=0),
                            finish_date=datetime.now().replace(minute=0, second=0, microsecond=0)
                        )
                        if queryRes is not None:
                            prevData[0].evaluation_date = timezone.make_aware(
                                datetime.now().replace(minute=0, second=0, microsecond=0),
                                timezone.get_default_timezone()
                            )

                            prevData[0].window_start_date = timezone.make_aware(
                                datetime.now().replace(day=1, hour=0, minute=0, second=0, microsecond=0),
                                timezone.get_default_timezone()
                            )

                            prevData[0].day_chart = queryRes.id
                    try:
                        prevData[0].save()
                    except Exception, e:
                        print "Can not update " + str(
                            prevData[0].advertiser) + " advertiser current month data. Error: " + str(e)


    # creating all new placements
    for type, info in newPlacements.iteritems():
        LastModified.objects.filter(type='hourlyTask').update(date=timezone.make_aware(datetime.now(), timezone.get_default_timezone()))
        if info[0]:
            info[1].objects.bulk_create(info[0])
    print "New placements created"
    LastModified.objects.filter(type='hourlyTask').update(date=timezone.make_aware(datetime.now(), timezone.get_default_timezone()))
    if allNewAdvertiserts:
        try:
            UIUsualCampaignsGraph.objects.bulk_create(allNewAdvertiserts)
        except Exception, e:
            print "Can not save new advertiser's graph. Error: " + str(e)
    LastModified.objects.filter(type='hourlyTask').update(date=timezone.make_aware(datetime.now(), timezone.get_default_timezone()))
    print "New advertisers graphs saved"
    if allNewCampaigns:
        try:
            UIUsualPlacementsGraph.objects.bulk_create(allNewCampaigns)
        except Exception, e:
            print "Can not save new campaign's graph. Error: " + str(e)
    LastModified.objects.filter(type='hourlyTask').update(date=timezone.make_aware(datetime.now(), timezone.get_default_timezone()))
    print "New campaigns graphs saved"
    #
    # all usual
    #
    # updating existing campaigns
    allCampaignsInfo = UIUsualCampaignsGridDataAll.objects.all()
    for row in allCampaignsInfo.iterator():
        LastModified.objects.filter(type='hourlyTask') \
            .update(date=timezone.make_aware(datetime.now(), timezone.get_default_timezone()))
        # check if less than an hour had pass
        if (datetime.now() - row.evaluation_date) < timedelta(hours=1):
            continue
        queryRes = getSiteDomainsReportInfo(
            start_date=row.evaluation_date,
            finish_date=datetime.now().replace(minute=0, second=0, microsecond=0),
            camp_id=row.campaign_id
        )
        try:
            queryRes[0]
        except:
            continue
        # cummulative data
        row.imps += 0 if queryRes[0].imp is None else queryRes[0].imp
        row.conversions += 0 if queryRes[0].conversions is None else queryRes[0].conversions
        row.spent += 0 if queryRes[0].spend is None else queryRes[0].spend
        row.clicks += 0 if queryRes[0].clicks is None else queryRes[0].clicks
        row.imps_viewed += 0 if queryRes[0].imps_viewed is None else queryRes[0].imps_viewed
        row.view_measured_imps += 0 if queryRes[0].view_measured_imps is None else queryRes[0].view_measured_imps
        # calculated rates
        if row.imps == 0:
            row.cpm = 0
            row.cvr = 0
            row.ctr = 0
            row.view_measurement_rate = 0
        else:
            row.cpm = float(row.spent) / row.imps * 1000.0
            row.cvr = float(row.conversions) / row.imps
            row.ctr = float(row.clicks) / row.imps
            row.view_measurement_rate = float(row.view_measured_imps) / row.imps
        row.cpc = 0 if row.clicks == 0 else (float(row.spent) / row.clicks)
        row.view_rate = 0 if row.view_measured_imps == 0 else (float(row.imps_viewed) / row.view_measured_imps)

        if row.day_chart[len(row.day_chart)-1]["day"] == queryRes[0].id[0]["day"]:
            row.day_chart[len(row.day_chart) - 1]["imp"] += queryRes[0].id[0]["imp"]
            row.day_chart[len(row.day_chart) - 1]["spend"] += queryRes[0].id[0]["spend"]
            row.day_chart[len(row.day_chart) - 1]["clicks"] += queryRes[0].id[0]["clicks"]
            row.day_chart[len(row.day_chart) - 1]["conversions"] += queryRes[0].id[0]["conversions"]

            if row.day_chart[len(row.day_chart) - 1]["imp"] == 0:
                row.day_chart[len(row.day_chart) - 1]["cvr"] = 0
                row.day_chart[len(row.day_chart) - 1]["ctr"] = 0
            else:
                row.day_chart[len(row.day_chart) - 1]["cvr"] = float(row.day_chart[len(row.day_chart) - 1]["conversions"]) /  row.day_chart[len(row.day_chart) - 1]["imp"]
                row.day_chart[len(row.day_chart) - 1]["ctr"] = float(row.day_chart[len(row.day_chart) - 1]["clicks"]) / row.day_chart[len(row.day_chart) - 1]["imp"]
            row.day_chart[len(row.day_chart) - 1]["cpc"] = 0 if (row.day_chart[len(row.day_chart) - 1]["clicks"] == 0) else (row.day_chart[len(row.day_chart) - 1]["spend"] / row.day_chart[len(row.day_chart) - 1]["clicks"])
            row.day_chart.extend(queryRes[0].id[1:])
        else:
            row.day_chart.extend(queryRes[0].id)

        row.evaluation_date = datetime.now().replace(minute=0, second=0, microsecond=0)
        try:
            row.save()
        except Exception, e:
            print "Can not update " + str(row.campaign_id) + "campaign all time data. Error: " + str(e)
    # finding and filling every new campaign
    allNewCampaigns = []
    with connection.cursor() as cursor:
        cursor.execute(
            "select array_to_string(array(select id from campaign where id not in (select distinct campaign_id from ui_usual_campaigns_grid_data_all)),',');")
        newCampaigns = cursor.fetchone()[0]
    newCampaigns = '(' + newCampaigns + ')'
    queryRes = getSiteDomainsReportInfo(
        start_date="1970-01-01 00:00:00",
        finish_date=datetime.now().replace(hour=0, minute=0, second=0, microsecond=0),
        newCampaigns=newCampaigns
    )

    for row in queryRes:
        LastModified.objects.filter(type='hourlyTask') \
            .update(date=timezone.make_aware(datetime.now(), timezone.get_default_timezone()))
        allNewCampaigns.append(UIUsualCampaignsGridDataAll(
            campaign_id=row.campaign_id,
            evaluation_date=timezone.make_aware(
                datetime.now().replace(hour=0, minute=0, second=0, microsecond=0),
                timezone.get_default_timezone()
            ),
            spent=row.spend,
            conversions=row.conversions,
            imps=row.imp,
            clicks=row.clicks,
            cpc=row.cpc,
            cpm=row.cpm,
            cvr=row.cvr,
            ctr=row.ctr,
            imps_viewed=row.imps_viewed,
            view_measured_imps=row.view_measured_imps,
            view_measurement_rate=row.view_measurement_rate,
            view_rate=row.view_rate,
            day_chart=row.id
            )
        )
    if not allNewCampaigns:
        pass
    else:
        try:
            UIUsualCampaignsGridDataAll.objects.bulk_create(allNewCampaigns)
        except Exception, e:
            print "Can not save campaigns all time data. Error: " + str(e)

    #
    # last N days usual
    #
    # updating existing campaigns
    modelsDict = {}
    modelsDict["yesterday"] = [UIUsualCampaignsGridDataYesterday, 1]
    modelsDict["last_3_days"] = [UIUsualCampaignsGridDataLast3Days, 3]
    modelsDict["last_7_days"] = [UIUsualCampaignsGridDataLast7Days, 7]
    modelsDict["last_14_days"] = [UIUsualCampaignsGridDataLast14Days, 14]
    modelsDict["last_21_days"] = [UIUsualCampaignsGridDataLast21Days, 21]
    modelsDict["last_90_days"] = [UIUsualCampaignsGridDataLast90Days, 90]

    for type, info in modelsDict.iteritems():
        allCampaignsInfo = info[0].objects.all()
        for row in allCampaignsInfo.iterator():
            LastModified.objects.filter(type='hourlyTask') \
                .update(date=timezone.make_aware(datetime.now(), timezone.get_default_timezone()))
            # check if less than an hour had pass
            if (datetime.now() - row.evaluation_date) < timedelta(hours=1):
                continue
            queryRes = getSiteDomainsReportInfo(
                start_date=row.evaluation_date,
                finish_date=datetime.now().replace(minute=0, second=0, microsecond=0),
                camp_id=row.campaign_id
            )
            try:
                queryRes[0]
            except:
                continue
            # cummulative data
            row.imps += queryRes[0].imp
            row.conversions += queryRes[0].conversions
            row.spent += queryRes[0].spend
            row.clicks += queryRes[0].clicks
            row.imps_viewed += queryRes[0].imps_viewed
            row.view_measured_imps += queryRes[0].view_measured_imps

            # chart
            # if new data is greater, then time period
            if len(queryRes[0].id) >= (info[1]+1):
                row.day_chart = queryRes[0].id[-(info[1]+1):]
            else:
                # if old data don't fill time period
                if queryRes[0].id[0]["day"] == row.day_chart[len(row.day_chart)-1]["day"]:
                    row.day_chart[len(row.day_chart) - 1]["imp"] += queryRes[0].id[0]["imp"]
                    row.day_chart[len(row.day_chart) - 1]["spend"] += queryRes[0].id[0]["spend"]
                    row.day_chart[len(row.day_chart) - 1]["clicks"] += queryRes[0].id[0]["clicks"]
                    row.day_chart[len(row.day_chart) - 1]["conversions"] += queryRes[0].id[0]["conversions"]

                    if row.day_chart[len(row.day_chart) - 1]["imp"] == 0:
                        row.day_chart[len(row.day_chart) - 1]["cvr"] = 0
                        row.day_chart[len(row.day_chart) - 1]["ctr"] = 0
                    else:
                        row.day_chart[len(row.day_chart) - 1]["cvr"] = float(row.day_chart[len(row.day_chart) - 1]["conversions"]) / \
                                                               row.day_chart[len(row.day_chart) - 1]["imp"]
                        row.day_chart[len(row.day_chart) - 1]["ctr"] = float(row.day_chart[len(row.day_chart) - 1]["clicks"]) / \
                                                               row.day_chart[len(row.day_chart) - 1]["imp"]

                    row.day_chart[len(row.day_chart) - 1]["cpc"] = 0 if (row.day_chart[len(row.day_chart) - 1]["clicks"] == 0) else (
                        row.day_chart[len(row.day_chart) - 1]["spend"] / row.day_chart[len(row.day_chart) - 1]["clicks"])
                    # cut and extend
                    if (len(row.day_chart) + len(queryRes[0].id) - info[1] - 2) > 0:
                        row.day_chart = row.day_chart[(len(row.day_chart) + len(queryRes[0].id) - info[1] - 2):]
                    row.day_chart.extend(queryRes[0].id[1:])
                else:
                    if (len(row.day_chart) + len(queryRes[0].id) - info[1] - 1) > 0:
                        row.day_chart = row.day_chart[(len(row.day_chart)+len(queryRes[0].id)-info[1]-1):]
                    row.day_chart.extend(queryRes[0].id)

            # check if need to sub days
            if (datetime.now() - row.window_start_date) >= timedelta(days=info[1]+1):
                # data for sub
                queryRes = getSiteDomainsReportInfo(
                    start_date=row.window_start_date,
                    finish_date=(datetime.now() - timedelta(days=info[1])).replace(hour=0, minute=0, second=0, microsecond=0),
                    camp_id=row.campaign_id
                )
                LastModified.objects.filter(type='hourlyTask') \
                    .update(date=timezone.make_aware(datetime.now(), timezone.get_default_timezone()))
                try:
                    queryRes[0]
                except:
                    # calculated rates
                    if row.imps == 0:
                        row.cpm = 0
                        row.cvr = 0
                        row.ctr = 0
                        row.view_measurement_rate = 0
                    else:
                        row.cpm = float(row.spent) / row.imps * 1000.0
                        row.cvr = float(row.conversions) / row.imps
                        row.ctr = float(row.clicks) / row.imps
                        row.view_measurement_rate = float(row.view_measured_imps) / row.imps
                    row.cpc = 0 if row.clicks == 0 else (float(row.spent) / row.clicks)
                    row.view_rate = 0 if row.view_measured_imps == 0 else (
                    float(row.imps_viewed) / row.view_measured_imps)
                    row.evaluation_date = datetime.now().replace(minute=0, second=0, microsecond=0)
                    row.window_start_date = (datetime.now() - timedelta(days=info[1])).replace(hour=0, minute=0, second=0, microsecond=0)
                    try:
                        row.save()
                    except Exception, e:
                        print "Can not update " + str(row.campaign_id) + " campaign " + str(type) + " data. Error: " + str(e)
                    continue
                # cummulative data
                row.imps -= queryRes[0].imp
                row.conversions -= queryRes[0].conversions
                row.spent -= queryRes[0].spend
                row.clicks -= queryRes[0].clicks
                row.imps_viewed -= queryRes[0].imps_viewed
                row.view_measured_imps -= queryRes[0].view_measured_imps
                LastModified.objects.filter(type='hourlyTask') \
                    .update(date=timezone.make_aware(datetime.now(), timezone.get_default_timezone()))

            # calculated rates
            if row.imps == 0:
                row.cpm = 0
                row.cvr = 0
                row.ctr = 0
                row.view_measurement_rate = 0
            else:
                row.cpm = float(row.spent) / row.imps * 1000.0
                row.cvr = float(row.conversions) / row.imps
                row.ctr = float(row.clicks) / row.imps
                row.view_measurement_rate = float(row.view_measured_imps) / row.imps
            row.cpc = 0 if row.clicks == 0 else (float(row.spent) / row.clicks)
            row.view_rate = 0 if row.view_measured_imps == 0 else (float(row.imps_viewed) / row.view_measured_imps)
            row.evaluation_date = datetime.now().replace(minute=0, second=0, microsecond=0)
            row.window_start_date = (datetime.now() - timedelta(days=info[1])).replace(hour=0, minute=0, second=0,
                                                                                       microsecond=0)
            try:
                row.save()
            except Exception, e:
                print "Can not update " + str(row.campaign_id) + " campaign " + str(type) + " data. Error: " + str(e)
            row.save()

        # finding and filling every new campaign
        allNewCampaigns = []
        with connection.cursor() as cursor:
            cursor.execute("""
select array_to_string(
 array(
   select id
   from campaign
   where id not in (select distinct campaign_id from ui_usual_campaigns_grid_data_"""+str(type)+""")),',');""")
            newCampaigns = cursor.fetchone()[0]
        newCampaigns = '(' + newCampaigns + ')'
        queryRes = getSiteDomainsReportInfo(
            start_date=(datetime.now() - timedelta(days=info[1])).replace(hour=0, minute=0, second=0, microsecond=0),
            finish_date=datetime.now().replace(hour=0, minute=0, second=0, microsecond=0),
            newCampaigns=newCampaigns
        )
        for row in queryRes:
            LastModified.objects.filter(type='hourlyTask') \
                .update(date=timezone.make_aware(datetime.now(), timezone.get_default_timezone()))
            allNewCampaigns.append(info[0](
                campaign_id=row.campaign_id,
                evaluation_date=timezone.make_aware(
                    datetime.now().replace(hour=0, minute=0, second=0, microsecond=0),
                    timezone.get_default_timezone()
                ),
                window_start_date=timezone.make_aware(
                    (datetime.now() - timedelta(days=info[1])).replace(hour=0, minute=0, second=0, microsecond=0),
                    timezone.get_default_timezone()
                ),
                spent=row.spend,
                conversions=row.conversions,
                imps=row.imp,
                clicks=row.clicks,
                cpc=row.cpc,
                cpm=row.cpm,
                cvr=row.cvr,
                ctr=row.ctr,
                imps_viewed=row.imps_viewed,
                view_measured_imps=row.view_measured_imps,
                view_measurement_rate=row.view_measurement_rate,
                view_rate=row.view_rate,
                day_chart=row.id
            )
            )
        if not allNewCampaigns:
            pass
        else:
            try:
                info[0].objects.bulk_create(allNewCampaigns)
            except Exception, e:
                print "Can not save campaign " + str(type) + " data. Error: " + str(e)

    #LAST MONTH
    # updating existing campaigns
    allCampaignsInfo = UIUsualCampaignsGridDataLastMonth.objects.all()

    for row in allCampaignsInfo.iterator():
        LastModified.objects.filter(type='hourlyTask') \
            .update(date=timezone.make_aware(datetime.now(), timezone.get_default_timezone()))
        # check if less than a month had pass
        if (datetime.now().month - row.window_start_date.month) < 2:
            continue
        queryRes = getSiteDomainsReportInfo(
            start_date=(datetime.now().replace(day=1) - timedelta(days=1)).replace(day=1, hour=0, minute=0, second=0, microsecond=0),
            finish_date=datetime.now().replace(day=1, hour=0, minute=0, second=0, microsecond=0),
            camp_id=row.campaign_id
        )
        try:
            queryRes[0]
        except:
            continue

        # cummulative data
        row.imps = queryRes[0].imp
        row.conversions = queryRes[0].conversions
        row.spent = queryRes[0].spend
        row.clicks = queryRes[0].clicks
        row.imps_viewed = queryRes[0].imps_viewed
        row.view_measured_imps = queryRes[0].view_measured_imps
        # calculated rates
        if row.imps == 0:
            row.cpm = 0
            row.cvr = 0
            row.ctr = 0
            row.view_measurement_rate = 0
        else:
            row.cpm = float(row.spent) / row.imps * 1000.0
            row.cvr = float(row.conversions) / row.imps
            row.ctr = float(row.clicks) / row.imps
            row.view_measurement_rate = float(row.view_measured_imps) / row.imps
        row.cpc = 0 if row.clicks == 0 else (float(row.spent) / row.clicks)
        row.view_rate = 0 if row.view_measured_imps == 0 else (float(row.imps_viewed) / row.view_measured_imps)
        row.evaluation_date = datetime.now().replace(minute=0, second=0, microsecond=0)
        row.window_start_date =(datetime.now().replace(day=1) - timedelta(days=1)).replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        row.day_chart = queryRes[0].id
        try:
            row.save()
        except Exception, e:
            print "Can not update " + str(row.campaign_id) + " campaign last month data. Error: " + str(e)
    # finding and filling every new campaign
    allNewCampaigns = []
    with connection.cursor() as cursor:
        cursor.execute(
            "select array_to_string(array(select id from campaign where id not in (select distinct campaign_id from ui_usual_campaigns_grid_data_last_month)),',');")
        newCampaigns = cursor.fetchone()[0]
    newCampaigns = '(' + newCampaigns + ')'
    queryRes = getSiteDomainsReportInfo(
        start_date=(datetime.now().replace(day=1) - timedelta(days=1)).replace(day=1, hour=0, minute=0, second=0, microsecond=0),
        finish_date=datetime.now().replace(day=1, hour=0, minute=0, second=0, microsecond=0),
        newCampaigns=newCampaigns
    )

    for row in queryRes:
        LastModified.objects.filter(type='hourlyTask') \
            .update(date=timezone.make_aware(datetime.now(), timezone.get_default_timezone()))
        allNewCampaigns.append(UIUsualCampaignsGridDataLastMonth(
            campaign_id=row.campaign_id,
            evaluation_date=timezone.make_aware(
                datetime.now().replace(minute=0, second=0, microsecond=0),
                timezone.get_default_timezone()
            ),
            window_start_date=timezone.make_aware(
                (datetime.now().replace(day=1) - timedelta(days=1)).replace(day=1, hour=0, minute=0, second=0,
                                                                            microsecond=0),
                timezone.get_default_timezone()
            ),
            spent=row.spend,
            conversions=row.conversions,
            imps=row.imp,
            clicks=row.clicks,
            cpc=row.cpc,
            cpm=row.cpm,
            cvr=row.cvr,
            ctr=row.ctr,
            imps_viewed=row.imps_viewed,
            view_measured_imps=row.view_measured_imps,
            view_measurement_rate=row.view_measurement_rate,
            view_rate=row.view_rate,
            day_chart=row.id
        )
        )
    if not allNewCampaigns:
        pass
    else:
        try:
            UIUsualCampaignsGridDataLastMonth.objects.bulk_create(allNewCampaigns)
        except Exception, e:
            print "Can not save campaigns last month data. Error: " + str(e)

    # CUR MONTH
    # updating existing campaigns
    allCampaignsInfo = UIUsualCampaignsGridDataCurMonth.objects.all()
    for row in allCampaignsInfo.iterator():
        LastModified.objects.filter(type='hourlyTask') \
            .update(date=timezone.make_aware(datetime.now(), timezone.get_default_timezone()))
        # check if less than an hour had pass
        if (datetime.now() - row.evaluation_date) < timedelta(hours=1):
            continue
        # if next month - change, if cur - cummulate
        if row.window_start_date.month == datetime.now().month:
            queryRes = getSiteDomainsReportInfo(
                start_date=row.evaluation_date,
                finish_date=datetime.now().replace(minute=0, second=0, microsecond=0),
                camp_id=row.campaign_id
            )
            try:
                queryRes[0]
            except:
                continue
            # cummulative data
            row.imps += queryRes[0].imp
            row.conversions += queryRes[0].conversions
            row.spent += queryRes[0].spend
            row.clicks += queryRes[0].clicks
            row.imps_viewed += queryRes[0].imps_viewed
            row.view_measured_imps += queryRes[0].view_measured_imps
            # calculated rates
            if row.imps == 0:
                row.cpm = 0
                row.cvr = 0
                row.ctr = 0
                row.view_measurement_rate = 0
            else:
                row.cpm = float(row.spent) / row.imps * 1000.0
                row.cvr = float(row.conversions) / row.imps
                row.ctr = float(row.clicks) / row.imps
                row.view_measurement_rate = float(row.view_measured_imps) / row.imps
            row.cpc = 0 if row.clicks == 0 else (float(row.spent) / row.clicks)
            row.view_rate = 0 if row.view_measured_imps == 0 else (float(row.imps_viewed) / row.view_measured_imps)
            row.evaluation_date = datetime.now().replace(minute=0, second=0, microsecond=0)

            # chart
            # if old data don't fill time period
            if queryRes[0].id[0]["day"] == row.day_chart[len(row.day_chart) - 1]:
                row.day_chart[len(row.day_chart) - 1]["imp"] += queryRes[0].id[0]["imp"]
                row.day_chart[len(row.day_chart) - 1]["spend"] += queryRes[0].id[0]["spend"]
                row.day_chart[len(row.day_chart) - 1]["clicks"] += queryRes[0].id[0]["clicks"]
                row.day_chart[len(row.day_chart) - 1]["conversions"] += queryRes[0].id[0]["conversions"]

                if row.day_chart[len(row.day_chart) - 1]["imp"] == 0:
                    row.day_chart[len(row.day_chart) - 1]["cvr"] = 0
                    row.day_chart[len(row.day_chart) - 1]["ctr"] = 0
                else:
                    row.day_chart[len(row.day_chart) - 1]["cvr"] = float(
                        row.day_chart[len(row.day_chart) - 1]["conversions"]) / \
                                                                   row.day_chart[len(row.day_chart) - 1]["imp"]
                    row.day_chart[len(row.day_chart) - 1]["ctr"] = float(
                        row.day_chart[len(row.day_chart) - 1]["clicks"]) / \
                                                                   row.day_chart[len(row.day_chart) - 1]["imp"]

                row.day_chart[len(row.day_chart) - 1]["cpc"] = 0 if (
                row.chart[len(row.day_chart) - 1]["clicks"] == 0) else (
                    row.day_chart[len(row.day_chart) - 1]["spend"] / row.chart[len(row.day_chart) - 1]["clicks"])
                # cut and extend
                row.day_chart.extend(queryRes[0].id[1:])
            else:
                row.day_chart.extend(queryRes[0].id)

            try:
                row.save()
            except Exception, e:
                print "Can not update " + str(row.campaign_id) + " campaign current month data. Error: " + str(e)
        else:
            LastModified.objects.filter(type='hourlyTask') \
                .update(date=timezone.make_aware(datetime.now(), timezone.get_default_timezone()))
            queryRes = getSiteDomainsReportInfo(
                start_date=datetime.now().replace(day=1, hour=0, minute=0, second=0, microsecond=0),
                finish_date=datetime.now().replace(minute=0, second=0, microsecond=0),
                camp_id=row.campaign_id
            )
            try:
                queryRes[0]
            except:
                continue
            # cummulative data
            row.imps = queryRes[0].imp
            row.conversions = queryRes[0].conversions
            row.spent = queryRes[0].spend
            row.clicks = queryRes[0].clicks
            row.imps_viewed = queryRes[0].imps_viewed
            row.view_measured_imps = queryRes[0].view_measured_imps
            # calculated rates
            if row.imps == 0:
                row.cpm = 0
                row.cvr = 0
                row.ctr = 0
                row.view_measurement_rate = 0
            else:
                row.cpm = float(row.spent) / row.imps * 1000.0
                row.cvr = float(row.conversions) / row.imps
                row.ctr = float(row.clicks) / row.imps
                row.view_measurement_rate = float(row.view_measured_imps) / row.imps
            row.cpc = 0 if row.clicks == 0 else (float(row.spent) / row.clicks)
            row.view_rate = 0 if row.view_measured_imps == 0 else (float(row.imps_viewed) / row.view_measured_imps)
            row.evaluation_date = datetime.now().replace(minute=0, second=0, microsecond=0)
            row.window_start_date = datetime.now().replace(day=1, hour=0, minute=0, second=0, microsecond=0)
            row.day_chart = queryRes[0].id
            try:
                row.save()
            except Exception, e:
                print "Can not update " + str(row.campaign_id) + " campaign current month data. Error: " + str(e)

    # finding and filling every new campaign
    allNewCampaigns = []
    with connection.cursor() as cursor:
        cursor.execute(
            "select array_to_string(array(select id from campaign where id not in (select distinct campaign_id from ui_video_campaigns_grid_data_cur_month)),',');")
        newCampaigns = cursor.fetchone()[0]
    newCampaigns = '(' + newCampaigns + ')'
    queryRes = getSiteDomainsReportInfo(
        start_date=datetime.now().replace(day=1, hour=0, minute=0, second=0, microsecond=0),
        finish_date=datetime.now().replace(hour=0, minute=0, second=0, microsecond=0),
        newCampaigns=newCampaigns
    )
    for row in queryRes:
        LastModified.objects.filter(type='hourlyTask') \
            .update(date=timezone.make_aware(datetime.now(), timezone.get_default_timezone()))
        allNewCampaigns.append(UIUsualCampaignsGridDataCurMonth(
            campaign_id=row.campaign_id,
            evaluation_date=timezone.make_aware(
                datetime.now().replace(hour=0, minute=0, second=0, microsecond=0),
                timezone.get_default_timezone()
            ),
            window_start_date=timezone.make_aware(
                datetime.now().replace(day=1, hour=0, minute=0, second=0, microsecond=0),
                timezone.get_default_timezone()
            ),
            spent=row.spend,
            conversions=row.conversions,
            imps=row.imp,
            clicks=row.clicks,
            cpc=row.cpc,
            cpm=row.cpm,
            cvr=row.cvr,
            ctr=row.ctr,
            imps_viewed=row.imps_viewed,
            view_measured_imps=row.view_measured_imps,
            view_measurement_rate=row.view_measurement_rate,
            view_rate=row.view_rate,
            day_chart=row.id
        )
        )
    if not allNewCampaigns:
        pass
    else:
        try:
            UIUsualCampaignsGridDataCurMonth.objects.bulk_create(allNewCampaigns)
        except Exception, e:
            print "Can not save campaigns current month data. Error: " + str(e)
    print "fillUIGridDataCron finished: " + str(datetime.now())
