__author__ = 'USER'

import numpy as np
from sklearn.cluster import KMeans
from sklearn import preprocessing
#from matplotlib import pyplot as plt
from sklearn import metrics
from sklearn.ensemble import ExtraTreesClassifier
import psycopg2
from psycopg2 import extras
from datetime import datetime
from datetime import timedelta
from models.ml_kmeans_model import MLPlacementDailyFeatures, MLClustersCentroidsKmeans, MLPlacementsClustersKmeans
from models import NetworkAnalyticsReport_ByPlacement
from django.db.models import Sum, Min, Max, Avg, Value, When, Case, F, Q, Func, FloatField
import datetime
import math

#from .models import PlacementDailyFearures

class PlacementInfo:#objects with features for recognition
    placement_id = 0

    imps = 0
    clicks = 0
    cost = 0
    conversions = 0
    imps_viewed = 0
    view_measured_imps = 0

    cpa = 0
    view_rate = 0
    view_measurement_rate = 0

    features = np.empty(1)
    cluster = 0

def mlLearnKmeans (predict = False):#learn machine, save clusters, predict on training set
    kmeansSpaces = []
    colNumb = 0
    numbDays = 7
    numbFeaturesInDay = 2#change on len(featuresList) for dynamic
    numbClusters = 2
    #predict = False
    print predict
    for i in xrange(numbDays):
        print str(i) + " K-means space"
        kmeansSpaces.append(KMeans(n_clusters = numbClusters, init = 'k-means++'))
        numbFeaturesAll = (i + 1) * numbFeaturesInDay

        allFeatures = []
        allFeaturesPlacement = []

        onePlacementFeatures = np.zeros(numbFeaturesAll)

        queryResults = MLPlacementDailyFeatures.objects.raw("""
               SELECT
                 id,day,ctr,view_rate,placement_id
               FROM
                 ml_placement_daily_features
               WHERE
                 placement_id
               IN
                 (SELECT placement_id FROM ml_placement_daily_features WHERE day="""+ str(i) +""")
                 AND day<=""" + str(i) +
               "ORDER BY placement_id,day")

        for row in queryResults:
            onePlacementFeatures[colNumb] = row.ctr
            onePlacementFeatures[colNumb + 1] = row.view_rate
            colNumb += numbFeaturesInDay

            if colNumb >= numbFeaturesAll:
                allFeatures.append(onePlacementFeatures)
                allFeaturesPlacement.append(row.placement_id)
                onePlacementFeatures = np.zeros(numbFeaturesAll)
                colNumb = 0

        allFeatures = np.float32(allFeatures)
        allFeaturesForRecognition = np.vstack(allFeatures)
        if predict == True:
            labels = kmeansSpaces[i].fit_predict(allFeaturesForRecognition)
        else:
            kmeansSpaces[i].fit(allFeaturesForRecognition)
        # PREDICT
        #saving centroids in DB
        centroidsRecord = MLClustersCentroidsKmeans(day = i, cluster = 1, centroid = kmeansSpaces[i].cluster_centers_[0].tolist())
        try:
            centroidsRecord.save()
        except:
            centroidsRecord.save(force_update=True)
        centroidsRecord = MLClustersCentroidsKmeans(day = i, cluster = 2, centroid = kmeansSpaces[i].cluster_centers_[1].tolist())
        try:
            centroidsRecord.save()
        except:
            centroidsRecord.save(force_update=True)

        if predict == True:#prediction of training set
            for j in range(len(labels)):
                placementClusterRerocd = MLPlacementsClustersKmeans()
                placementClusterRerocd.day = i
                placementClusterRerocd.placement_id = allFeaturesPlacement[j]
                centroidsDistance = []

                for nCentr in xrange(numbClusters):
                    for iFeature in xrange(len(kmeansSpaces[i].cluster_centers_[nCentr])):
                        centroidsDistance[nCentr] += (kmeansSpaces[i].cluster_centers_[nCentr][iFeature] - allFeatures[j][iFeature])**2

                    centroidsDistance[nCentr] = math.sqrt(centroidsDistance[nCentr])

                if labels[j] == 0:
                    placementClusterRerocd.cluster = 1
                else:
                    placementClusterRerocd.cluster = 2

                MLPlacementsClustersKmeans.objects.save()

        print str(i) + " space done"



def mlPredictKmeans(placement_idRecogn):
    # RECOGNITION
    #placementNumb = listRecognPlacement_id
    # for placementNumb in listRecognPlacement_id:
    # start 1 tab+
    numbFeaturesInDay = 2
    numbClusters = 2

    queryResults = MLPlacementDailyFeatures.objects.filter(placement_id=placement_idRecogn).aggregate(mday=Max("day"))['mday']
    maxDay = queryResults['mday']
    print "Max day: " + str(maxDay)

    queryResultsPlacementInfo = MLPlacementDailyFeatures.objects.raw("""
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
            WHERE
              placement_id = """ + str(placement_idRecogn) + """
            group by
              placement_id, extract (dow from hour);
            ORDER BY
              dow;
            """
                                                                     )

    for i in xrange(maxDay + 1):
        numbFeaturesAll = (i+1) * numbFeaturesInDay
        onePlacementFeatures = np.zeros(numbFeaturesAll)
        colNumb = 0

        for row in queryResultsPlacementInfo:
            onePlacementFeatures[colNumb] = row.ctr
            onePlacementFeatures[colNumb + 1] = row.view_rate
            colNumb += numbFeaturesInDay

        onePlacementFeatures = np.float32(onePlacementFeatures)


        labels = kmeansSpaces[i].predict(onePlacementFeatures)
        placementClusterRerocd = MLPlacementsClustersKmeans()
        placementClusterRerocd.day = i
        placementClusterRerocd.placement_id = placement_idRecogn
        centroidsDistance = []

        for nCentr in xrange(numbClusters):
            for iFeature in xrange(len(kmeansSpaces[i].cluster_centers_[0])):
                centroidsDistance[nCentr] += (kmeansSpaces[i].cluster_centers_[0][iFeature] - onePlacementFeatures[
                    iFeature]) ** 2

            centroidsDistance[nCentr] = math.sqrt(centroidsDistance[nCentr])
        placementClusterRerocd.distanceToClusters = centroidsDistance

        if labels[0] == 0:
            placementClusterRerocd.cluster = 1
        else:
            placementClusterRerocd.cluster = 2

        MLPlacementsClustersKmeans.objects.save()

def fillingOnePlacementFeatures():
    pass