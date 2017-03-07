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
from django.db import connection
from django.utils import timezone
from rtb.models.placement_state import LastModified

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
                    datetime.now().replace(day=1, hour=0, minute=0, second=0, microsecond=0),
                    timezone.get_default_timezone()
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
                        prevData[0].evaluation_date = timezone.make_aware(
                            datetime.now().replace(minute=0, second=0, microsecond=0),
                            timezone.get_default_timezone()
                        )
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

        advertiserCampaigns = Campaign.objects.filter(advertiser_id=adv.id)
        for camp in advertiserCampaigns.iterator():
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
                    queryRes = getUsualCampaignGraphData(
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
                                prevData[0].day_chart[len(prevData[0].day_chart) - 1]["ctr"] = 0 if prevData[0].day_chart[len(prevData[0].day_chart) - 1]["impression"] == 0 else(prevData[0].day_chart[len(prevData[0].day_chart) - 1]["clicks"] / prevData[0].day_chart[len(prevData[0].day_chart) - 1]["impression"])

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
                        datetime.now().replace(day=1, hour=0, minute=0, second=0, microsecond=0),
                        timezone.get_default_timezone()
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
                            print "Can not update " + str(prevData[0].campaign_id) + " advertiser last month data. Error: " + str(e)
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
                            prevData[0].evaluation_date = timezone.make_aware(
                                datetime.now().replace(minute=0, second=0, microsecond=0),
                                timezone.get_default_timezone()
                            )
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
                        print "Can not update " + str(prevData[0].advertiser) + " advertiser current month data. Error: " + str(e)

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
    print "fillUIGridDataCron finished: " + str(datetime.now())


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
#### NEW
def refreshGridPlacementsData(start_date, finish_date):
    print "Refreshing grid data from " + str(start_date) + " to " + str(finish_date) + " started: " + str(datetime.now())
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
    # refreshing campaigns
    cummulateCampaignsGridData(type="all", start_date=start_date, finish_date=finish_date)
    LastModified.objects.filter(type='hourlyTask').update(
        date=timezone.make_aware(datetime.now(), timezone.get_default_timezone()))
    print "Refreshing all time campaigns grid data finished: " + str(datetime.now())
    cummulateCampaignsGridData(type="cur_month", start_date=start_date, finish_date=finish_date)
    LastModified.objects.filter(type='hourlyTask').update(
        date=timezone.make_aware(datetime.now(), timezone.get_default_timezone()))
    print "Refreshing current month campaigns grid data finished: " + str(datetime.now())
    # refreshing placements
    cummulatePlacementsGridData(type="all", start_date=start_date, finish_date=finish_date)
    LastModified.objects.filter(type='hourlyTask').update(
        date=timezone.make_aware(datetime.now(), timezone.get_default_timezone()))
    print "Refreshing all time placements grid data finished: " + str(datetime.now())
    cummulatePlacementsGridData(type="cur_month", start_date=start_date, finish_date=finish_date)
    LastModified.objects.filter(type='hourlyTask').update(
        date=timezone.make_aware(datetime.now(), timezone.get_default_timezone()))
    print "Refreshing current month placements grid data finished: " + str(datetime.now())
    for type in tableTypes:
        # refreshing campaigns
        LastModified.objects.filter(type='hourlyTask').update(
            date=timezone.make_aware(datetime.now(), timezone.get_default_timezone()))
        # adding data
        cummulateCampaignsGridData(type=type[0], start_date=start_date, finish_date=finish_date)
        LastModified.objects.filter(type='hourlyTask').update(
            date=timezone.make_aware(datetime.now(), timezone.get_default_timezone()))
        # sub data
        if finish_date == finish_date.replace(hour=0, minute=0, second=0, microsecond=0):
            subCampaignsGridData(type=type[0],
                                  start_date=finish_date - timedelta(days=type[1] + 1),
                                  finish_date=finish_date - timedelta(days=type[1])
                                  )
            LastModified.objects.filter(type='hourlyTask').update(
                date=timezone.make_aware(datetime.now(), timezone.get_default_timezone()))
        print "Refreshing " + str(type[0]) + " campaigns grid data finished: " + str(datetime.now())

        # refreshing placements
        LastModified.objects.filter(type='hourlyTask').update(
            date=timezone.make_aware(datetime.now(), timezone.get_default_timezone()))
        # adding data
        cummulatePlacementsGridData(type=type[0], start_date=start_date, finish_date=finish_date)
        LastModified.objects.filter(type='hourlyTask').update(
            date=timezone.make_aware(datetime.now(), timezone.get_default_timezone()))
        # sub data
        if finish_date == finish_date.replace(hour=0, minute=0, second=0, microsecond=0):
            subPlacementsGridData(type=type[0],
                                  start_date=finish_date - timedelta(days=type[1]+1),
                                  finish_date=finish_date - timedelta(days=type[1])
                                  )
            LastModified.objects.filter(type='hourlyTask').update(
                date=timezone.make_aware(datetime.now(), timezone.get_default_timezone()))
        print "Refreshing " + str(type[0]) + " placements grid data finished: " + str(datetime.now())
    # refresh last month
    if finish_date == finish_date.replace(day=1, hour=0, minute=0, second=0, microsecond=0):
        # campaigns refreshing
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
        # placements refreshing
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
    LastModified.objects.filter(type='hourlyTask').update(date=timezone.make_aware(datetime.now(), timezone.get_default_timezone()))
    print "Refreshing grid data from " + str(start_date) + " to " + str(finish_date) + " finished: " + str(datetime.now())

