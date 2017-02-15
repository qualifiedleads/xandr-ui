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
        # find new placements for test_number 2

        newPlacementsList = NetworkAnalyticsReport_ByPlacement.objects.raw(
            """SELECT
              placement_id as id
            FROM
              network_analytics_report_by_placement
            WHERE
              placement_id NOT IN (SELECT DISTINCT placement_id FROM ml_placements_clusters_kmeans WHERE test_number = 2)
            GROUP BY
              placement_id
            HAVING
              COUNT(DISTINCT extract ( dow from hour)) = 7 and SUM(imps) >="""+ str(impsBorder)
        )
        # predict new placements for test_number 2
        n = 0

        goodClusters = mlGetGoodClusters("ctr_cvr_cpc_cpm_cpa")
        if goodClusters == -1:
            print "K-means model is not taught"
        else:
            for row in newPlacementsList:
                mlPredictKmeans(row.id, "ctr_cvr_cpc_cpm_cpa")
                LastModified.objects.filter(type='mlPredictNewPlacementsCron') \
                    .update(date=timezone.make_aware(datetime.datetime.now(), timezone.get_default_timezone()))
                n += 1

            print "K-means placements recognized: " + str(n)

        #logreg
        n = 0
        tempQuery = MLLogisticRegressionCoeff.objects.filter(day=7, test_number=3)
        if not tempQuery:
            print "Logistic regression model is not taught"
        else:
            newPlacementsList = NetworkAnalyticsReport_ByPlacement.objects.raw(
                """SELECT
                  placement_id as id
                FROM
                  network_analytics_report_by_placement
                WHERE
                  placement_id NOT IN (SELECT DISTINCT placement_id FROM ml_logistic_regression_results WHERE test_number = 3 AND probability != -1)
                GROUP BY
                  placement_id
                HAVING
                  COUNT(DISTINCT extract ( dow from hour)) = 7 and SUM(imps) >=""" + str(impsBorder)
            )

            for row in newPlacementsList:
                mlPredictLogisticRegression(row.placement_id, "ctr_cvr_cpc_cpm_cpa")
                LastModified.objects.filter(type='mlPredictNewPlacementsCron') \
                    .update(date=timezone.make_aware(datetime.datetime.now(), timezone.get_default_timezone()))
                n += 1
            print "Logistic regression placements recognized: " + str(n)
        print "New placements prediction completed"
        LastModified.objects.filter(type='mlPredictNewPlacementsCron').delete()
    except Exception, e:
        LastModified.objects.filter(type='mlPredictNewPlacementsCron').delete()
        print 'Cron job - suspend_state_middleware_cron Error: ' + str(e)