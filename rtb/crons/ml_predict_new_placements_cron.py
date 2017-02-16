from rtb.models import NetworkAnalyticsReport_ByPlacement, MLPlacementsClustersKmeans
from rtb.models import MLLogisticRegressionCoeff
from rtb.ml_learn_kmeans import mlPredictKmeans, mlGetGoodClusters
from rtb.ml_logistic_regression import mlPredictLogisticRegression
from rtb.models.placement_state import LastModified
import datetime
from django.utils import timezone
from datetime import timedelta


def mlPredictNewPlacementsCron():
    try:
        change_state = LastModified.objects.filter(type='mlPredictNewPlacementsCron')
        if len(change_state) >= 1:
            if timezone.make_aware(datetime.datetime.now(), timezone.get_default_timezone()) - change_state[
                0].date >= timedelta(
                    minutes=15):
                LastModified.objects.filter(type='mlPredictNewPlacementsCron').delete()
            else:
                print "mlPredictNewPlacementsCron is busy, wait..."
                return None
        LastModified(type='mlPredictNewPlacementsCron',
                     date=timezone.make_aware(datetime.datetime.now(), timezone.get_default_timezone())).save()

        impsBorder = 1000
        goodClusters = mlGetGoodClusters("ctr_cvr_cpc_cpm_cpa")
        if goodClusters == -1:
            print "K-means model is not taught"
        else:
            # find new placements for test_number 2
            newPlacementsList = NetworkAnalyticsReport_ByPlacement.objects.raw(
                """SELECT
                      t1.placement_id as id
                    FROM
                      network_analytics_report_by_placement t1
                      left join ml_placements_clusters_kmeans t2 on t2.placement_id = t1.placement_id and test_number = 2
                    where t2.placement_id is null
                    GROUP BY
                      t1.placement_id
                    HAVING
                      COUNT(DISTINCT extract ( dow from t1.hour)) = 7 and SUM(t1.imps) >="""+ str(impsBorder)
            )
            # predict new placements for test_number 2
            n = 0
            LastModified.objects.filter(type='mlPredictNewPlacementsCron') \
                .update(date=timezone.make_aware(datetime.datetime.now(), timezone.get_default_timezone()))

            for row in newPlacementsList:
                LastModified.objects.filter(type='mlPredictNewPlacementsCron') \
                    .update(date=timezone.make_aware(datetime.datetime.now(), timezone.get_default_timezone()))
                mlPredictKmeans(row.id, "ctr_cvr_cpc_cpm_cpa")
                n += 1

            print "K-means placements recognized: " + str(n)

        #logreg
        n = 0
        tempQuery = MLLogisticRegressionCoeff.objects.filter(day=7, test_number=3)
        if not tempQuery:
            print "Logistic regression model is not taught"
        else:
            newPlacementsList = NetworkAnalyticsReport_ByPlacement.objects.raw(
                """
                SELECT
                  t1.placement_id as id
                FROM
                  network_analytics_report_by_placement t1
                  left join ml_logistic_regression_results t2 on t2.placement_id = t1.placement_id and test_number = 3 and probability != -1
                WHERE
                  t2.placement_id is null
                GROUP BY
                  t1.placement_id
                HAVING
                  COUNT(DISTINCT extract (dow from t1.hour)) = 7 and SUM(t1.imps) >=""" + str(impsBorder)
            )
            LastModified.objects.filter(type='mlPredictNewPlacementsCron') \
                .update(date=timezone.make_aware(datetime.datetime.now(), timezone.get_default_timezone()))
            for row in newPlacementsList:
                LastModified.objects.filter(type='mlPredictNewPlacementsCron') \
                    .update(date=timezone.make_aware(datetime.datetime.now(), timezone.get_default_timezone()))
                mlPredictLogisticRegression(row.placement_id, "ctr_cvr_cpc_cpm_cpa")
                n += 1
            print "Logistic regression placements recognized: " + str(n)
        print "New placements prediction completed"
        LastModified.objects.filter(type='mlPredictNewPlacementsCron').delete()
    except Exception, e:
        LastModified.objects.filter(type='mlPredictNewPlacementsCron').delete()
        print 'Cron job - suspend_state_middleware_cron Error: ' + str(e)