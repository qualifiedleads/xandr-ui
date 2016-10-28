from rtb.models import NetworkAnalyticsReport_ByPlacement, MLPlacementsClustersKmeans
from rtb.ml_learn_kmeans import mlPredictKmeans
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
    tt = 0
    for row in newPlacementsList:
        tt += 1
        if tt >=5:
            break
        mlPredictKmeans(row.id, "ctr_cvr_cpc_cpm_cpa")
        n += 1
        currentTime = datetime.now()
        if currentTime - started >= timedelta(minutes=57):
            timeout = True
            break
    if timeout == True:
        print "Out of time"
    else:
        print "Time for recognition: " +\
              str(((currentTime - started).total_seconds() % 3600) // 60) + " minutes " +\
              str((currentTime - started).total_seconds() % 60) + " seconds"

    print "Placements recognized: " + str(n)


    #TODO prediction for logreg
    # newPlacementsList = NetworkAnalyticsReport_ByPlacement.objects.raw(
    #     """SELECT
    #           placement_id
    #         FROM
    #           network_analytics_report_by_placement
    #         WHERE
    #           placement_id NOT IN (SELECT DISTINCT placement_id FROM ml_placements_clusters_kmeans WHERE test_number = 3)
    #         GROUP BY
    #           placement_id
    #         HAVING
    #           SUM(imps) >=""" + str(impsBorder)
    # )
    # for row in newPlacementsList:
    #     mlPredictLogisticRegression(row.placement_id, "ctr_cvr_cpc_cpm_cpa")
    print "New placements prediction completed"