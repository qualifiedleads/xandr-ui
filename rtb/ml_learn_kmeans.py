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

def mlLearnKmeans (listRecognPlacement_id=None,featuresList=None):
    kmeansSpaces = []

    colNumb = 0
    numbDays = 7
    numbFeaturesInDay = 3#change on len(featuresList) for dynamic
    numbClusters = 2
    #LEARN/PREDICT
    queryResults = MLPlacementDailyFeatures.objects.aggregate(mcpa=Max("cpa"), mctr=Max("ctr"))['cpa']['ctr']

    maxCPA = queryResults['cpa']
    maxCTR = queryResults['ctr']

    for i in xrange(numbDays):
        print "Learning and predicting" + str(i) + " K-means space"
        kmeansSpaces.append(KMeans(n_clusters = numbClusters, init = 'k-means++'))
        numbFeaturesAll = (i + 1) * numbFeaturesInDay

        allFeatures = []
        allFeaturesPlacement = []

        onePlacementFeatures = np.zeros(numbFeaturesAll)

        queryResults = MLPlacementDailyFeatures.objects.raw("""
               SELECT
                 day,cpa,ctr,view_rate,placement_id
               FROM
                 placement_daily_features
               WHERE
                 placement_id
               IN
                 (SELECT placement_id FROM placement_daily_features WHERE day=%s)
                 AND day<=""" + str(i) +
               "ORDER BY placement_id,day")

        for row in queryResults.iterator():
            if row.cpa == 0:
                onePlacementFeatures[colNumb] = 1
            else:
                onePlacementFeatures[colNumb] = float(row.cpa) / float(maxCPA)

            onePlacementFeatures[colNumb + 1] = float(row.ctr) / float(maxCTR)
            onePlacementFeatures[colNumb + 2] = row.view_rate
            colNumb += 3

            if colNumb >= numbFeaturesAll:
                allFeatures.append(onePlacementFeatures)
                allFeaturesPlacement.append(row.placement_id)
                onePlacementFeatures = np.zeros(numbFeaturesAll)
                colNumb = 0

        allFeatures = np.float32(allFeatures)
        allFeaturesForRecognition = np.vstack(allFeatures)
        labels = kmeansSpaces[i].fit_predict(allFeaturesForRecognition)
        # PREDICT
        #saving centroids in DB
        MLClustersCentroidsKmeans.objects.save(day = i, cluster = 1, centroid = kmeansSpaces[i].cluster_centers_[0])
        MLClustersCentroidsKmeans.objects.save(day = i, cluster = 2, centroid = kmeansSpaces[i].cluster_centers_[1])
        for j in range(len(labels)):
            placementClusterRerocd = MLPlacementsClustersKmeans()
            placementClusterRerocd.day = i
            placementClusterRerocd.placement_id = allFeaturesPlacement[j]
            centroidsDistance = []

            for nCentr in xrange(numbClusters):
                for iFeature in xrange(len(kmeansSpaces[i].cluster_centers_[0])):
                    centroidsDistance[nCentr] += (kmeansSpaces[i].cluster_centers_[0][iFeature] - allFeatures[j][iFeature])**2

                centroidsDistance[nCentr] = math.sqrt(centroidsDistance[nCentr])

            if labels[j] == 0:
                placementClusterRerocd.cluster = 1
            else:
                placementClusterRerocd.cluster = 2

            MLPlacementsClustersKmeans.objects.save()

        print str(i) + " space done"

    #RECOGNITION
    placementNumb = listRecognPlacement_id
    #for placementNumb in listRecognPlacement_id:
    #start 1 tab+
    queryResults = MLPlacementDailyFeatures.objects.filter(placement_id = placementNumb).aggregate(mday=Max("day"))['mday']
    maxDay = queryResults['mday']

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
          placement_id = """ + str(placementNumb) + """
        group by
          placement_id, extract (dow from hour);
        ORDER BY
          dow;
        """
    )

    for i in xrange(maxDay+1):
        onePlacementFeatures = np.zeros(numbFeaturesAll)
        colNumb = 0

        for row in queryResultsPlacementInfo:
            if row.cpa == 0:
                onePlacementFeatures[colNumb] = 1
            else:
                onePlacementFeatures[colNumb] = float(row.cpa) / float(maxCPA)

            if row.ctr == 0:
                onePlacementFeatures[colNumb + 1] = 0
            else:
                onePlacementFeatures[colNumb + 1] = float(row.ctr) / float(maxCTR)
            onePlacementFeatures[colNumb + 2] = row.view_rate
            colNumb += 3

        onePlacementFeatures = np.float32(onePlacementFeatures)
        labels = kmeansSpaces[i].predict(onePlacementFeatures)
        placementClusterRerocd = MLPlacementsClustersKmeans()
        placementClusterRerocd.day = i
        placementClusterRerocd.placement_id = placementNumb
        centroidsDistance = []

        for nCentr in xrange(numbClusters):
            for iFeature in xrange(len(kmeansSpaces[i].cluster_centers_[0])):
                centroidsDistance[nCentr] += (kmeansSpaces[i].cluster_centers_[0][iFeature] - onePlacementFeatures[iFeature])**2

            centroidsDistance[nCentr] = math.sqrt(centroidsDistance[nCentr])
        placementClusterRerocd.distanceToClusters = centroidsDistance

        if labels[0] == 0:
            placementClusterRerocd.cluster = 1
        else:
            placementClusterRerocd.cluster = 2

        MLPlacementsClustersKmeans.objects.save()

        #fin 1 tab+