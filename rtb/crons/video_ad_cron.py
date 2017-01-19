from rtb.models.video_ad_models import VideoAdCampaigns
from rtb.models import Advertiser
from django.utils import timezone
from datetime import datetime, timedelta
from django.db.models import Max

def fillVideoAdDataCron():
    print "Begin of collecting hourly data for video ad"
    now = timezone.make_aware(datetime.now(), timezone.get_default_timezone())

    last_date = VideoAdCampaigns.objects.aggregate(Max("date"))
    if not last_date:
        last_date = now - timedelta(hours=1)
    else:
        last_date = last_date["date__max"]

    after = last_date + timedelta(hours=1) - timedelta(microseconds=1)

    while after < now:
        bulkAll = []
        queryRes = Advertiser.objects.raw("""
                    SELECT
                      advertiser.id,
                      camp.id AS campaign_id,
                      camp.name,
                      report.sum_cost,
                      report.sum_imps,
                      report.cpm,
                      video.allcpvm,
                      video.ad_starts,
                      video.cpvm,
                      imp_tracker.price_paid,
                      imp_tracker.bid_price,
                      CASE report.sum_imps WHEN 0 THEN 0 ELSE video.ad_starts::float/report.sum_imps*100 end fill_rate,
                      --report.cpm/1000 ???
                      coalesce(video.cpvm * video.ad_starts - report.cpm * report.sum_imps,-report.cpm * report.sum_imps,video.cpvm * video.ad_starts,0) AS profit_loss,
                      --coalesce(video.allcpvm-report.sum_cost,-report.sum_cost,video.allcpvm,0) AS profit_loss
                    FROM
                      advertiser
                      LEFT JOIN (
                      SELECT
                        id,
                        advertiser_id,
                        name
                      FROM
                        campaign
                      ) AS camp
                      ON camp.advertiser_id=advertiser.id
                      LEFT JOIN(
                        SELECT
                          campaign_id,
                          SUM(media_cost) AS sum_cost,
                          SUM(imps) AS sum_imps,
                          case SUM(imps) when 0 then 0 else SUM(media_cost)/SUM(imps)*1000 end cpm
                        FROM
                          site_domain_performance_report
                        WHERE
                          day >= '""" + str(last_date) + """'
                          AND
                          day <= '""" + str(after) + """'
                        GROUP BY
                          campaign_id
                      ) AS report
                      ON camp.id=report.campaign_id
                      LEFT JOIN(
                        SELECT
                          "CpId",
                          SUM(cpvm) AS allcpvm,
                          case COUNT("CpId") when 0 then 0 else COUNT("CpId") end ad_starts,
                          case COUNT(id) when 0 then 0 else SUM(cpvm)/COUNT("CpId") end cpvm--???
                        FROM
                          rtb_adstart_tracker
                        WHERE
                          "Date" >='""" + str(last_date) + """'
                          AND
                          "Date" <='""" + str(after) + """'
                        GROUP BY
                          "CpId"
                      ) AS video
                      ON camp.id=video."CpId"
                      LEFT JOIN (
                        SELECT
                          "CpId",
                          SUM("PricePaid") AS price_paid,
                          SUM("BidPrice") AS bid_price
                        FROM
                          rtb_impression_tracker
                        WHERE
                          "Date" >='""" + str(last_date) + """'
                        AND
                          "Date" <='""" + str(after) + """'
                        GROUP BY
                          "CpId"
                      ) AS imp_tracker
                      ON camp.id=imp_tracker."CpId"
                    WHERE advertiser.ad_type='videoAds';
                    """)
        for row in queryRes:
            bulkAll.append(VideoAdCampaigns(
                advertiser_id=row.id,
                campaign_id=row.campaign_id,
                campaign_name=row.name,
                date=after.replace(hour=0, minute=0, second=0, microsecond=0),
                hour=after,
                imp_hour=row.sum_imps,
                ad_starts_hour=row.ad_starts,
                spent_hour=row.sum_cost,
                cpm_hour=row.cpm,
                spent_cpm_hour=row.price_paid,
                bid_hour=row.bid_price,
                cpvm_hour=row.cpvm,
                spent_cpvm_hour=row.allcpvm,
                fill_rate_hour=row.fill_rate,
                profit_loss_hour=row.profit_loss
            ))
        if not bulkAll:
            print "There is nothing to add to table from " + str(last_date) + " to " + str(after)
        else:
            VideoAdCampaigns.objects.bulk_create(bulkAll)
            print "Video ad data from " + str(last_date) + " to " + str(after) + " has been added"
        last_date = last_date + timedelta(hours=1)
        after = last_date + timedelta(hours=1) - timedelta(microseconds=1)
    print "Refreshing of the video ad hourly data is finished"