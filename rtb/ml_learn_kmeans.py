__author__ = 'USER'

import numpy as np
from sklearn.cluster import KMeans
from sklearn import preprocessing
#from matplotlib import pyplot as plt
from models.ml_kmeans_model import MLPlacementDailyFeatures, MLClustersCentroidsKmeans, MLPlacementsClustersKmeans
from models import NetworkAnalyticsReport_ByPlacement
from django.db.models import Sum, Min, Max, Avg, Value, When, Case, F, Q, Func, FloatField, Count
import math
import csv

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

def mlLearnKmeans ():#learn machine, save clusters, predict on training set
    kmeansSpaces = []
    colNumb = 0
    numbDays = 7
    numbFeaturesInDay = 2#change on len(featuresList) for dynamic
    numbClusters = 2
    random_state = 266
    for i in xrange(numbDays):#for every day K-means space
        print str(i) + " K-means space"
        kmeansSpaces.append(KMeans(n_clusters=numbClusters, random_state=random_state))

        allFeatures = []
        allFeaturesPlacement = []

        onePlacementFeatures = np.zeros(numbFeaturesInDay)

        queryResults = MLPlacementDailyFeatures.objects.raw("""
               SELECT
                 id,day,ctr,view_rate,placement_id
               FROM
                 ml_placement_daily_features
               WHERE
                 day=""" + str(i) +
               "ORDER BY placement_id")

        for row in queryResults:
            onePlacementFeatures[colNumb] = row.ctr
            onePlacementFeatures[colNumb + 1] = row.view_rate

            allFeatures.append(onePlacementFeatures)
            allFeaturesPlacement.append(row.placement_id)
            onePlacementFeatures = np.zeros(numbFeaturesInDay)

        allFeatures = np.float32(allFeatures)
        allFeaturesForRecognition = np.vstack(allFeatures)

        kmeansSpaces[i].fit(allFeaturesForRecognition)

        print str(i) + " space done"

    print str(numbDays) + " K-means space"#for last K-means space with all week
    kmeansSpaces.append(KMeans(n_clusters=numbClusters, random_state=random_state))

    queryResults = MLPlacementDailyFeatures.objects.raw("""
                   SELECT
                     id,day,ctr,view_rate,placement_id
                   FROM
                     ml_placement_daily_features
                   ORDER BY placement_id,day""")

    onePlacementFeatures = np.zeros(numbFeaturesInDay * numbDays)
    checkDay = 0
    allFeaturesPlacement = []
    allFeatures = []
    failedPlacement = 0
    for row in queryResults:
        if failedPlacement == row.placement_id:
            continue
        if row.day == checkDay:
            onePlacementFeatures[checkDay * numbFeaturesInDay] = row.ctr
            onePlacementFeatures[checkDay * numbFeaturesInDay + 1] = row.view_rate
            checkDay += 1
            if checkDay == numbDays - 1:
                allFeatures.append(onePlacementFeatures)
                allFeaturesPlacement.append(row.placement_id)
        else:
            failedPlacement = row.placement_id
            checkDay = 0
            onePlacementFeatures = np.zeros(numbFeaturesInDay * numbDays)

    allFeatures = np.float32(allFeatures)
    allFeaturesForRecognition = np.vstack(allFeatures)
    kmeansSpaces[numbDays].fit(allFeaturesForRecognition)

    for i in xrange(numbDays + 1):#saving clusters centroids
        centroidsRecord = MLClustersCentroidsKmeans(
            day=i,
            cluster=1,
            centroid=kmeansSpaces[i].cluster_centers_[0].tolist(),
            test_number=1)
        try:
            tempQuery = MLClustersCentroidsKmeans.objects.filter(
                cluster=centroidsRecord.cluster,
                day=centroidsRecord.day
            )
            if not tempQuery:
                centroidsRecord.save()
            tempQuery.update(
                centroid=centroidsRecord.centroid,
                test_number=1
            )
        except Exception, e:
            print "Can't save centroid to database. Error: " + str(e)


        centroidsRecord = MLClustersCentroidsKmeans(
            day=i,
            cluster=2,
            centroid=kmeansSpaces[i].cluster_centers_[1].tolist(),
            test_number=1)
        try:
            tempQuery = MLClustersCentroidsKmeans.objects.filter(
                cluster=centroidsRecord.cluster,
                day=centroidsRecord.day
            )

            if not tempQuery:
                centroidsRecord.save()

            tempQuery.update(
                centroid=centroidsRecord.centroid,
                test_number=1
            )
        except Exception, e:
            print "Can't save centroid to database. Error: " + str(e)

    print "Learning finished"

def mlPredictKmeans(placement_idRecogn):#prediction
    numbFeaturesInDay = 2
    numbClusters = 2

    if placement_idRecogn == -1:#recongition of all placements in database
        queryResultsAllPlacements = NetworkAnalyticsReport_ByPlacement.objects.raw("""
               SELECT
                 DISTINCT placement_id AS id
               FROM
                 network_analytics_report_by_placement
               WHERE
                 placement_id <= 9024766
               ORDER BY
                 placement_id DESC"""
               )

        for plId in queryResultsAllPlacements:#sending every placement id on recognirion
            mlPredictOnePlacement(placement_id=plId.placement_id,
                                  numbClusters=numbClusters,
                                  numbFeaturesInDay=numbFeaturesInDay)
    else:#recognition of one placement in database
        mlPredictOnePlacement(placement_id=placement_idRecogn, numbClusters=numbClusters, numbFeaturesInDay=numbFeaturesInDay)


def mlGetPlacementInfoKmeans(placement_id = 1, flagAllWeek = False):#getting info about placement cluster from database
    #placement_id - palcement for recognition
    # flagAllWeek: True - return data about all weekdays, False - return about only whole week analyze
    wholeWeekInd = 7#index of whole week recognition data in column "day"
    goodClusters = mlGetGoodClusters()  # getting info about good cluster in days
    if goodClusters == -1:#if K-means didn't learn
        return -1

    queryClusterInfo = MLPlacementsClustersKmeans.objects.filter(placement_id=placement_id)

    if not queryClusterInfo:#if that placement is not recognized
        return -2

    mlAnswer = {}  # answer from backend to controllerr; format: mlAnswer[day][good/bad]
    if flagAllWeek == True:
        for row in queryClusterInfo.iterator():#insert data for answer to contoller about all weekdays
            if str(row.day) not in mlAnswer:
                mlAnswer[str(row.day)] = {}
            mlAnswer[str(row.day)]['good'] = row.distance_to_clusters[goodClusters[row.day]-1]
            mlAnswer[str(row.day)]['bad'] = row.distance_to_clusters[goodClusters[row.day] % 2]
            mlAnswer[str(row.day)]['checked'] = row.expert_decision
    else:
        queryClusterInfo = MLPlacementsClustersKmeans.objects.filter(placement_id=placement_id, day=wholeWeekInd)
        if not queryClusterInfo:
            return mlAnswer
        mlAnswer[str(wholeWeekInd)] = {}#insert data for answer to contoller about all weekdays
        mlAnswer[str(queryClusterInfo[0].day)]['good'] = queryClusterInfo[0].distance_to_clusters[goodClusters[queryClusterInfo[0].day] - 1]
        mlAnswer[str(queryClusterInfo[0].day)]['bad'] = queryClusterInfo[0].distance_to_clusters[goodClusters[queryClusterInfo[0].day] % 2]
        mlAnswer[str(queryClusterInfo[0].day)]['checked'] = queryClusterInfo[0].expert_decision

    return mlAnswer


def mlGetGoodClusters():#get array of "good" clusters for every k-means space
    numbFeaturesInDay = 2
    numbClusters = 2
    numbDays = 8

    queryResults = MLClustersCentroidsKmeans.objects.all()#get info from database about clusters centroids

    if not queryResults:
        return -1

    centroidsCoord = [0] * numbDays
    goodClusters = []  # goodClusters[x] - x day good cluster
    for i in xrange(numbDays):
        centroidsCoord[i] = [0] * numbClusters

    for row in queryResults.iterator():  # getting data about cluster centroids
        centroidsCoord[row.day][row.cluster - 1] = row.centroid

        # centroidsCoord[x][y][x] - x=day, y=cluster, z=coord numb

    #separatly weekdays
    for i in xrange(numbDays - 1):  # clusters centres distance to 0 calculating
        maxClustDist = 0
        maxClust = 0
        for j in xrange(numbClusters):
            dist = 0
            for iFeature in xrange(numbFeaturesInDay):
                dist += centroidsCoord[i][j][iFeature] ** 2

            dist = math.sqrt(dist)
            if dist > maxClustDist:
                maxClustDist = dist
                maxClust = j + 1
        goodClusters.append(maxClust)
    #whole week
    for j in xrange(numbClusters):  # for all weekdays
        dist = 0
        for iFeature in xrange(numbFeaturesInDay * (numbDays - 1)):
            dist += centroidsCoord[7][j][iFeature] ** 2
        dist = math.sqrt(dist)
        if dist > maxClustDist:
            maxClustDist = dist
            maxClust = j + 1
    goodClusters.append(maxClust)
    return goodClusters

def mlPredictOnePlacement(placement_id, numbClusters, numbFeaturesInDay):
    numbDays = 8
    queryResults = MLClustersCentroidsKmeans.objects.all()
    centroidsCoord = [0] * numbDays
    for i in xrange(numbDays):
        centroidsCoord[i] = [0] * numbClusters

    for row in queryResults.iterator():  # getting data about cluster centroids
        centroidsCoord[row.day][row.cluster - 1] = row.centroid

    # centroidsCoord[x][y][x] - x=day, y=cluster, z=coord numb
    #Add dow as column in DB, set trigger on it to recalculate, create index for it
    queryResultsPlacementInfo = NetworkAnalyticsReport_ByPlacement.objects.raw("""
                SELECT
                  placement_id AS id,
                  extract (dow from hour) "dow",
                  SUM(imps), SUM(clicks), SUM(total_convs), SUM(imps_viewed), SUM(view_measured_imps), SUM(cost),
                  case SUM(imps) when 0 then 0 else SUM(clicks)::float/SUM(imps) end CTR,
                  case SUM(view_measured_imps) when 0 then 0 else SUM(imps_viewed)::float/SUM(view_measured_imps) end view_rate,
                  case SUM(imps) when 0 then 0 else SUM(view_measured_imps)::float/SUM(imps) end view_measurement_rate,
                  case SUM(imps) when 0 then 0 else SUM(id) end wtf
                FROM
                  network_analytics_report_by_placement
                WHERE
                  placement_id = """ + str(placement_id) + """
                group by
                  placement_id, extract (dow from hour)
                ORDER BY
                  dow;
                """
                )
    allDaysPlacementFeatures = []
    for row in queryResultsPlacementInfo:
        placementClusterRecord = MLPlacementsClustersKmeans()
        placementClusterRecord.day = row.dow
        placementClusterRecord.placement_id = placement_id
        clustersDistance = []
        oneDayPlacementFeatures = [row.ctr, row.view_rate]
        allDaysPlacementFeatures.append(row.ctr)
        allDaysPlacementFeatures.append(row.view_rate)
        for iCentr in xrange(numbClusters):
            distance = 0
            for iFeature in xrange(len(centroidsCoord[int(row.dow)][iCentr])):
                distance += (
                (float(centroidsCoord[int(row.dow)][iCentr][iFeature]) - float(oneDayPlacementFeatures[iFeature])) ** 2)
            distance = math.sqrt(distance)
            clustersDistance.append(distance)
        placementClusterRecord.distance_to_clusters = clustersDistance
        minDistance = clustersDistance[0]
        placementClusterRecord.cluster = 1
        placementClusterRecord.test_number = 1
        for i in xrange(1, numbClusters):
            if clustersDistance[i] < minDistance:
                minDistance = clustersDistance[i]
                placementClusterRecord.cluster = i + 1
        try:
            tempQuery = MLPlacementsClustersKmeans.objects.filter(
                placement_id=placement_id,
                day=placementClusterRecord.day
            )
            if not tempQuery:
                placementClusterRecord.save()
            tempQuery.update(
                distance_to_clusters=placementClusterRecord.distance_to_clusters,
                test_number=1
            )
        except Exception, e:
            print "Can't save recognition info. Error: " + str(e)

    if len(allDaysPlacementFeatures) < (numbDays - 1) * numbFeaturesInDay:
        print "Prediction completed (not enough data for weekly space) " + str(placement_id)
    else:
        placementClusterRecord = MLPlacementsClustersKmeans()
        placementClusterRecord.day = 7
        placementClusterRecord.placement_id = placement_id
        clustersDistance = []
        for iCentr in xrange(numbClusters):
            distance = 0
            for iFeature in xrange(len(centroidsCoord[7][iCentr])):
                distance += (
                (float(centroidsCoord[7][iCentr][iFeature]) - float(allDaysPlacementFeatures[iFeature])) ** 2)
            distance = math.sqrt(distance)
            clustersDistance.append(distance)
        placementClusterRecord.distance_to_clusters = clustersDistance
        minDistance = clustersDistance[0]
        placementClusterRecord.cluster = 1
        placementClusterRecord.test_number = 1
        for i in xrange(1, numbClusters):
            if clustersDistance[i] < minDistance:
                minDistance = clustersDistance[i]
                placementClusterRecord.cluster = i + 1

        try:
            tempQuery = MLPlacementsClustersKmeans.objects.filter(
                placement_id=placement_id,
                day=placementClusterRecord.day
            )
            if not tempQuery:
                placementClusterRecord.save()
            tempQuery.update(
                distance_to_clusters=placementClusterRecord.distance_to_clusters,
                test_number = 1
            )
        except Exception, e:
            print "Can't save recognition info. Error: " + str(e)
        print "Prediction completed " + str(placement_id)

def makeCsv():#making csv file from recognized database
    goodClusters = mlGetGoodClusters()#getting array of good clusters for every k-means space
    queryResults = MLPlacementsClustersKmeans.objects.all().order_by('placement_id', 'day')

    with open('ml_placements_prediction_ctr_viewrate.csv', 'w') as csvfile:
        fieldnames = ['placement_id', 'day', 'predict', 'distance to good', 'distance to bad', 'distance difference']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for row in queryResults.iterator():
            if goodClusters[row.day] == row.cluster:
                prediction = 'good'
            else:
                prediction = 'bad'

            distGood = row.distance_to_clusters[goodClusters[row.day] - 1]
            if goodClusters[row.day] == 1:
                distBad = row.distance_to_clusters[1]
            else:
                distBad = row.distance_to_clusters[0]
            dist = math.fabs(distGood - distBad)

            writer.writerow({'placement_id': row.placement_id,
                             'day': row.day,
                             'predict': prediction,
                             'distance to good': distGood,
                             'distance to bad': distBad,
                             'distance difference': dist})
