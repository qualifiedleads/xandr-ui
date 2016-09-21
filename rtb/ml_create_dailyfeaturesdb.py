from models.ml_kmeans_model import MLPlacementDailyFeatures
from models.network_analitics_models import NetworkAnalyticsReport_ByPlacement
from django.db.models import Sum, Min, Max, Avg, Value, When, Case, F, Q, Func, FloatField

def mlCreatePlacementDailyFeaturesDB():
    try:
        trainingSet = MLPlacementDailyFeatures.objects.raw("""
        INSERT INTO ml_placement_daily_features(
          placement_id,
          day,
          imps,
          clicks,
          total_convs,
          imps_viewed,
          view_measured_imps,
          cost,
          cpa,
          ctr,
          view_rate,
          view_measurement_rate)

        SELECT
          placement_id,
          extract (dow from hour) "dow",
          SUM(imps), SUM(clicks), SUM(total_convs), SUM(imps_viewed), SUM(view_measured_imps), SUM(cost),
          case SUM(total_convs) when 0 then 0 else SUM(cost)::float/SUM(total_convs) end CPA,
          case SUM(imps) when 0 then 0 else SUM(clicks)::float/SUM(imps) end CTR,
          case SUM(view_measured_imps) when 0 then 0 else SUM(imps_viewed)::float/SUM(view_measured_imps) end view_rate,
          case SUM(imps) when 0 then 0 else SUM(view_measured_imps)::float/SUM(imps) end view_measurement_rate
        FROM
          network_analytics_report_by_placement
        group by
          placement_id, extract (dow from hour);
        """)

        print trainingSet[0]


    except Exception, e:
        print "Failed to save training set " + str(e)

    print "Database ml_placement_daily_features filled"