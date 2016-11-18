from rtb.models import NetworkAnalyticsReport_ByPlacement, MLPlacementsClustersKmeans
from rtb.models import MLLogisticRegressionCoeff
from rtb.ml_learn_kmeans import mlPredictKmeans, mlGetGoodClusters
from rtb.ml_logistic_regression import mlPredictLogisticRegression
from datetime import datetime, timedelta

def mlPredictNewPlacementsCron():
    impsBorder = 1000
    # find new placements for test_number 2
    started = datetime.now()
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
    timeout = False
    goodClusters = mlGetGoodClusters("ctr_cvr_cpc_cpm_cpa")
    if goodClusters == -1:
        print "K-means model is not taught"
    else:
        for row in newPlacementsList:
            mlPredictKmeans(row.id, "ctr_cvr_cpc_cpm_cpa")
            n += 1
            currentTime = datetime.now()
            if currentTime - started >= timedelta(minutes=57):
                timeout = True
            if timeout == True:
                print "Out of time"
                break
        else:
            print "Time for recognition: " +\
                  str(((currentTime - started).total_seconds() % 3600) // 60) + " minutes " +\
                  str((currentTime - started).total_seconds() % 60) + " seconds"

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
              placement_id NOT IN (SELECT DISTINCT placement_id FROM ml_logistic_regression_results WHERE test_number = 3)
            GROUP BY
              placement_id
            HAVING
              COUNT(DISTINCT extract ( dow from hour)) = 7 and SUM(imps) >=""" + str(impsBorder)
        )

        for row in newPlacementsList:
            mlPredictLogisticRegression(row.placement_id, "ctr_cvr_cpc_cpm_cpa")
            n += 1
            currentTime = datetime.now()
            if currentTime - started >= timedelta(minutes=57):
                timeout = True
            if timeout == True:
                print "Out of time"
                break
        print "Logistic regression placements recognized: " + str(n)
    print "New placements prediction completed"