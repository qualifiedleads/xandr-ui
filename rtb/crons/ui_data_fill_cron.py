from rtb.models.ui_data_models import \
    UIUsualCampaignsGridDataAll, UIUsualCampaignsGridDataYesterday, UIUsualCampaignsGridDataLast3Days,\
    UIUsualCampaignsGridDataLast7Days, UIUsualCampaignsGridDataLast14Days, UIUsualCampaignsGridDataLast21Days,\
    UIUsualCampaignsGridDataCurMonth, UIUsualCampaignsGridDataLastMonth, UIUsualCampaignsGridDataLast90Days, \
    UIUsualCampaignsGraph
from rtb.models import SiteDomainPerformanceReport, Campaign, Advertiser
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


def getUsualAdvertiserGraphData(start_date, finish_date, advertiser_id):
    queryRes = SiteDomainPerformanceReport.objects.raw("""
select
  array(
    select json_build_object(
      'day', "day"::timestamp::date,
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
    try:
        queryRes[0].id[0]
        return queryRes[0]
    except:
        return None

def fillUIGridDataCron():
    LastModified.objects.filter(type='hourlyTask') \
        .update(date=timezone.make_aware(datetime.now(), timezone.get_default_timezone()))
    modelsDict = {}
    modelsDict["yesterday"] = 1
    modelsDict["last_3_days"] = 3
    modelsDict["last_7_days"] = 7
    modelsDict["last_14_days"] = 14
    modelsDict["last_21_days"] = 21
    modelsDict["last_90_days"] = 90
    allAdvertisers = Advertiser.objects.filter(
        ad_type="usualAds",
        grid_data_source="report"
    )
    
    allNewAdvertiserts = []
    for adv in allAdvertisers:
        LastModified.objects.filter(type='hourlyTask') \
            .update(date=timezone.make_aware(datetime.now(), timezone.get_default_timezone()))
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
                finish_date=datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
            )
            if queryRes is None:
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
                    day_chart=[]
                ))
            else:
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
                    day_chart=queryRes.id
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
            try:
                prevData[0].save()
            except Exception, e:
                print "Can not update " + str(prevData[0].advertiser_id) + " advertiser all time data. Error: " + str(e)
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
                    start_date=(datetime.now() - timedelta(days=info)).replace(hour=0, minute=0, second=0,
                                                                                  microsecond=0),
                    finish_date=datetime.now().replace(hour=0, minute=0, second=0, microsecond=0),
                )
                if queryRes is None:
                    allNewAdvertiserts.append(UIUsualCampaignsGraph(
                        advertiser_id=adv.id,
                        type=type,
                        evaluation_date=timezone.make_aware(
                            datetime.now().replace(hour=0, minute=0, second=0, microsecond=0),
                            timezone.get_default_timezone()
                        ),
                        window_start_date=timezone.make_aware(
                            (datetime.now() - timedelta(days=info)).replace(hour=0, minute=0, second=0, microsecond=0),
                            timezone.get_default_timezone()
                        ),
                        day_chart=[]
                    ))
                else:
                    allNewAdvertiserts.append(UIUsualCampaignsGraph(
                        advertiser_id=adv.id,
                        type=type,
                        evaluation_date=timezone.make_aware(
                            datetime.now().replace(hour=0, minute=0, second=0, microsecond=0),
                            timezone.get_default_timezone()
                        ),
                        window_start_date=timezone.make_aware(
                            (datetime.now() - timedelta(days=info)).replace(hour=0, minute=0, second=0, microsecond=0),
                            timezone.get_default_timezone()
                        ),
                        day_chart=queryRes.id
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
                        if len(queryRes.id) >= (info + 1):
                            prevData[0].day_chart = queryRes.id[-(info + 1):]
                        else:
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
                                if (len(prevData[0].day_chart) + len(queryRes.id) - info - 2) > 0:
                                    prevData[0].day_chart = prevData[0].day_chart[(len(prevData[0].day_chart) + len(queryRes.id) - info - 2):]
                                prevData[0].day_chart.extend(queryRes.id[1:])
                            else:
                                if (len(prevData[0].day_chart) + len(queryRes.id) - info - 1) > 0:
                                    prevData[0].day_chart = prevData[0].day_chart[(len(prevData[0].day_chart) + len(queryRes.id) - info - 1):]
                                prevData[0].day_chart.extend(queryRes.id)
                try:
                    prevData[0].save()
                except Exception, e:
                    print "Can not update " + str(prevData[0].advertiser_id) + " advertiser " + type + " data. Error: " + str(e)
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
                finish_date=datetime.now().replace(day=1, hour=0, minute=0, second=0, microsecond=0)
            )
            if queryRes is None:
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
                    day_chart=[]
                ))
            else:
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
                    day_chart=queryRes.id
                ))
        # updating
        else:
            if (datetime.now().month - prevData[0].window_start_date.month) >= 2:
                queryRes = getSiteDomainsReportInfo(
                    start_date=(datetime.now().replace(day=1) - timedelta(days=1)).replace(day=1, hour=0, minute=0,
                                                                                           second=0, microsecond=0),
                    finish_date=datetime.now().replace(day=1, hour=0, minute=0, second=0, microsecond=0),
                    camp_id=prevData[0].campaign_id
                )
                if queryRes is not None:
                    prevData[0].day_chart = queryRes.id
                    try:
                        prevData[0].save()
                    except Exception, e:
                        print "Can not update " + str(prevData[0].advertiser_id) + " advertiser last month data. Error: " + str(e)
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
            )
            if queryRes is None:
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
                    day_chart=[]
                ))
            else:
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
                    day_chart=queryRes.id
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
                    LastModified.objects.filter(type='hourlyTask') \
                        .update(date=timezone.make_aware(datetime.now(), timezone.get_default_timezone()))
                    queryRes = getSiteDomainsReportInfo(
                        start_date=datetime.now().replace(day=1, hour=0, minute=0, second=0, microsecond=0),
                        finish_date=datetime.now().replace(minute=0, second=0, microsecond=0),
                        camp_id=prevData[0].campaign_id
                    )
                    if queryRes is not None:
                        prevData[0].evaluation_date = datetime.now().replace(minute=0, second=0, microsecond=0)
                        prevData[0].window_start_date = datetime.now().replace(day=1, hour=0, minute=0, second=0, microsecond=0)
                        prevData[0].day_chart = queryRes.id
                try:
                    prevData[0].save()
                except Exception, e:
                    print "Can not update " + str(prevData[0].advertiser) + " advertiser current month data. Error: " + str(e)

    LastModified.objects.filter(type='hourlyTask') \
        .update(date=timezone.make_aware(datetime.now(), timezone.get_default_timezone()))
    if not allNewAdvertiserts:
        pass
    else:
        try:
            UIUsualCampaignsGraph.objects.bulk_create(allNewAdvertiserts)
        except Exception, e:
            print "Can not save campaigns all time data. Error: " + str(e)
    LastModified.objects.filter(type='hourlyTask') \
        .update(date=timezone.make_aware(datetime.now(), timezone.get_default_timezone()))

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
                        print "Can not update " + str(row.campaign_id) + "campaign " + str(type) + " data. Error: " + str(e)
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
                print "Can not update " + str(row.campaign_id) + "campaign " + str(type) + " data. Error: " + str(e)
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
            print "Can not update " + str(row.campaign_id) + "campaign last month data. Error: " + str(e)
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
                print "Can not update " + str(row.campaign_id) + "campaign current month data. Error: " + str(e)
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
                print "Can not update " + str(row.campaign_id) + "campaign current month data. Error: " + str(e)

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
