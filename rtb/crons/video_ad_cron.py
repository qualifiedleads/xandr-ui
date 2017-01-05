from rtb.models.video_ad_models import VideoAdCampaigns
from rtb.models import Advertiser, SiteDomainPerformanceReport
from rtb.models.rtb_impression_tracker import RtbAdStartTracker, RtbImpressionTracker
from django.utils import timezone
from datetime import datetime, timedelta
from django.db.models import Sum, Min, Max, Avg, Value, When, Case, F, Q, Func, FloatField

def fillVideoAdDataCron():
    now = timezone.make_aware(datetime.now(),
                        timezone.get_default_timezone())
    before = now - timedelta(hours=1)
    queryRes = SiteDomainPerformanceReport.objects.filter(
        day__gte=before,
        day__lte=now,
    ).values(
        "advertiser_id", "campaign_id"
    ).annotate(
        spend=Sum("media_cost"),
        imp=Sum("imps"),
    ).annotate(
        cpm=Case(When(~Q(imp=0), then=1.0 * F('spend') / F('imp') * 1000), output_field=FloatField()),
    )
    bulkAll = []
    for row in queryRes:
        query = RtbAdStartTracker.objects.raw("""
                SELECT
                  "CpId" as id,
                  SUM(cpvm::float) AS allcpvm,
                  COUNT(id) AS ad_starts,
                  case COUNT(id) when 0 then 0 else SUM(cpvm::float)/COUNT(id) end cpvm
                FROM
                  rtb_adstart_tracker
                WHERE
                  "CpId" = '""" + str(row["campaign_id"]) + """'
                  AND
                  "Date" >='""" + str(before) + """'
                  AND
                  "Date" <='""" + str(now) + """'
                GROUP BY
                  "CpId"
                  """
                                              )
        ans = VideoAdCampaigns()
        temp = 0
        for r in query:
            temp = r
        if temp == 0:
            ans.ad_starts_hour = 0
            ans.cpvm_hour = 0
            ans.spent_cpvm_hour = 0
            ans.fill_rate_hour = 0
            ans.profit_loss_hour = row["cpm"] * row["imp"]
        else:
            ans.ad_starts_hour = temp.ad_starts
            ans.cpvm_hour = temp.cpvm
            ans.spent_cpvm_hour = temp.allcpvm
            ans.fill_rate_hour = float(temp.ad_starts) / float(row["imp"])
            ans.profit_loss_hour = row["cpm"] * row["imp"] - temp.cpvm * float(temp.ad_starts)

        query = RtbImpressionTracker.objects.raw("""
                            SELECT
                              "CpId" as id,
                              SUM("PricePaid"::float) AS price_paid,
                              SUM("BidPrice"::float) AS bid_price
                            FROM
                              rtb_impression_tracker
                            WHERE
                              "CpId" = '""" + str(row["campaign_id"]) + """'
                              AND
                              "Date" >='""" + str(before) + """'
                              AND
                              "Date" <='""" + str(now) + """'
                            GROUP BY
                              "CpId"
                              """
                                                 )
        temp = 0
        for r in query:
            temp = r
        if temp == 0:
            ans.bid_hour = 0
            ans.spent_cpm_hour = 0
        else:
            ans.bid_hour = temp.bid_price
            ans.spent_cpm_hour = temp.price_paid

        bulkAll.append(VideoAdCampaigns(
            advertiser_id=row["advertiser_id"],
            campaign_id=row["campaign_id"],
            date=now,
            imp_hour=row["imp"],
            ad_starts_hour=ans.ad_starts_hour,
            spent_hour=row["spend"],
            cpm_hour=row["cpm"],
            spent_cpm_hour=ans.spent_cpm_hour,
            bid_hour=ans.bid_hour,
            cpvm_hour=ans.cpvm_hour,
            spent_cpvm_hour=ans.spent_cpvm_hour,
            fill_rate_hour=ans.fill_rate_hour,
            profit_loss_hour=ans.profit_loss_hour
        ))
    if not bulkAll:
        return -1
    VideoAdCampaigns.objects.bulk_create(bulkAll)
    return 1