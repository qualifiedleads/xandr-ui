import numpy as np
from sklearn.cluster import KMeans
from sklearn import preprocessing
#from matplotlib import pyplot as plt
from models.ml_kmeans_model import MLPlacementDailyFeatures, MLClustersCentroidsKmeans, MLPlacementsClustersKmeans, MLNormalizationData
from models import NetworkAnalyticsReport_ByPlacement
from django.db.models import Sum, Min, Max, Avg, Value, When, Case, F, Q, Func, FloatField, Count
import math
import csv

def mlLearnKmeans (test_name = "ctr_viewrate", advertiser_type="ecommerceAd"):#learn machine, save clusters, predict on training set
    kmeansSpaces = []
    colNumb = 0
    numbDays = 7
    numbFeaturesInDay = 0
    test_number_base = 0
    if test_name == "ctr_viewrate":#set number of features in dependence of test
        numbFeaturesInDay = 2
        test_number_base = 1
    if test_name == "ctr_cvr_cpc_cpm_cpa":
        numbFeaturesInDay = 5
        test_number_base = 2
    if test_number_base == 0:
        print "Wrong test name"
        return -1

    if advertiser_type != "ecommerceAd" and advertiser_type != "leadGenerationAd":
        print "Wrong test name"
        return -1

    numbClusters = 2
    random_state = 266
    for i in xrange(numbDays):#for every day K-means space
        print str(i) + " K-means space"
        kmeansSpaces.append(KMeans(n_clusters=numbClusters, random_state=random_state))

        allFeatures = []
        allFeaturesPlacement = []

        onePlacementFeatures = np.zeros(numbFeaturesInDay)

        queryResults = MLPlacementDailyFeatures.objects.filter(#get features for i-weekday
            day=i,
            adv_type=advertiser_type
        ).order_by(
            "placement_id")

        maxdata = MLPlacementDailyFeatures.objects.filter(
            day=i,
            adv_type=advertiser_type
        ).aggregate(
            Max("cpa"),
            Max("cvr"),
            Max("cpc"),
            Max("cpm")
        )

        try:
            MLNormalizationData.objects.update_or_create(
                test_number=test_number_base,
                day=i,
                adv_type=advertiser_type,
                defaults={
                    "maxcpa": maxdata["cpa__max"],
                    "maxcvr": maxdata["cvr__max"],
                    "maxcpc": maxdata["cpc__max"],
                    "maxcpm": maxdata["cpm__max"],
                }
            )
        except Exception, e:
            print "Can't save normalization data into the database. Error: " + str(e)

        for row in queryResults:#filling placements features for learning
            if test_name == "ctr_viewrate":
                onePlacementFeatures[0] = row.ctr
                onePlacementFeatures[1] = row.view_rate
            if test_name == "ctr_cvr_cpc_cpm_cpa":#normalization
                onePlacementFeatures[0] = row.ctr
                if row.cvr == 0:
                    onePlacementFeatures[1] = 0
                else:
                    onePlacementFeatures[1] = float(row.cvr) / float(maxdata["cvr__max"])

                if row.cpc == 0:
                    onePlacementFeatures[2] = 1
                else:
                    onePlacementFeatures[2] = float(row.cpc) / float(maxdata["cpc__max"])

                if row.cpm == 0:
                    onePlacementFeatures[3] = 1
                else:
                    onePlacementFeatures[3] = float(row.cpm) / float(maxdata["cpm__max"])

                if row.cpa == 0:
                    onePlacementFeatures[4] = 1
                else:
                    onePlacementFeatures[4] = float(row.cpa) / float(maxdata["cpa__max"])

            allFeatures.append(onePlacementFeatures)
            allFeaturesPlacement.append(row.placement_id)
            onePlacementFeatures = np.zeros(numbFeaturesInDay)

        allFeatures = np.float32(allFeatures)
        allFeaturesForRecognition = np.vstack(allFeatures)

        kmeansSpaces[i].fit(allFeaturesForRecognition)

        print str(i) + " space done"

    print str(numbDays) + " K-means space"#for last K-means space with all week
    kmeansSpaces.append(KMeans(n_clusters=numbClusters, random_state=random_state))

    onePlacementFeatures = np.zeros(numbFeaturesInDay * numbDays)
    checkDay = 0
    allFeaturesPlacement = []
    allFeatures = []
    failedPlacement = 0
    maxdata = MLPlacementDailyFeatures.objects.filter(
        adv_type=advertiser_type
    ).aggregate(
        Max("cpa"),
        Max("cvr"),
        Max("cpc"),
        Max("cpm")
    )

    try:
        MLNormalizationData.objects.update_or_create(
            test_number=test_number_base,
            day=numbDays,
            adv_type=advertiser_type,
            defaults={
                "maxcpa": maxdata["cpa__max"],
                "maxcvr": maxdata["cvr__max"],
                "maxcpc": maxdata["cpc__max"],
                "maxcpm": maxdata["cpm__max"],
            }
        )
    except Exception, e:
        print "Can't save normalization data into the database. Error: " + str(e)

    queryResults = MLPlacementDailyFeatures.objects.order_by(
        "placement_id",
        "day")
    for row in queryResults:
        if failedPlacement == row.placement_id:
            continue
        if row.day == checkDay:
            if test_name == "ctr_viewrate":
                onePlacementFeatures[checkDay * numbFeaturesInDay] = row.ctr
                onePlacementFeatures[checkDay * numbFeaturesInDay + 1] = row.view_rate
            if test_name == "ctr_cvr_cpc_cpm_cpa":
                onePlacementFeatures[checkDay * numbFeaturesInDay] = row.ctr
                if row.cvr == 0:
                    onePlacementFeatures[checkDay * numbFeaturesInDay + 1] = 0
                else:
                    onePlacementFeatures[checkDay * numbFeaturesInDay + 1] = float(row.cvr) / float(maxdata["cvr__max"])
                if row.cpc == 0:
                    onePlacementFeatures[checkDay * numbFeaturesInDay + 2] = 1
                else:
                    onePlacementFeatures[checkDay * numbFeaturesInDay + 2] = float(row.cpc) / float(maxdata["cpc__max"])
                if row.cpm == 0:
                    onePlacementFeatures[checkDay * numbFeaturesInDay + 3] = 1
                else:
                    onePlacementFeatures[checkDay * numbFeaturesInDay + 3] = float(row.cpm) / float(maxdata["cpm__max"])
                if row.cpa == 0:
                    onePlacementFeatures[checkDay * numbFeaturesInDay + 4] = 1
                else:
                    onePlacementFeatures[checkDay * numbFeaturesInDay + 4] = float(row.cpa) / float(maxdata["cpa__max"])
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
    print str(numbDays) + " K-means space done"
    print "Saving centroids into the database..."

    for i in xrange(numbDays + 1):#saving clusters centroids
        try:
            MLClustersCentroidsKmeans.objects.update_or_create(
                test_number=test_number_base,
                day=i,
                cluster=1,
                adv_type=advertiser_type,
                defaults={
                    "centroid": kmeansSpaces[i].cluster_centers_[0].tolist()
                }
            )
        except Exception, e:
            print "Can't save cluster centroids data into the database. Error: " + str(e)

        try:
            MLClustersCentroidsKmeans.objects.update_or_create(
                test_number=test_number_base,
                day=i,
                cluster=2,
                adv_type=advertiser_type,
                defaults={
                    "centroid": kmeansSpaces[i].cluster_centers_[1].tolist()
                }
            )
        except Exception, e:
            print "Can't save cluster centroids data into the database. Error: " + str(e)

    print "Learning finished"

def mlPredictKmeans(placement_idRecogn = 1, test_name = "ctr_viewrate", advertiser_type="ecommerceAd"):#prediction

    numbFeaturesInDay = 0
    if test_name == "ctr_viewrate":
        numbFeaturesInDay = 2
    if test_name == "ctr_cvr_cpc_cpm_cpa":
        numbFeaturesInDay = 5
    if numbFeaturesInDay == 0:
        print "Wrong test name"
        return -1
    numbClusters = 2

    if placement_idRecogn == -1:#recongition of all placements in database
        queryResultsAllPlacements = NetworkAnalyticsReport_ByPlacement.objects.raw("""
               SELECT
                 DISTINCT placement_id AS id
               FROM
                 network_analytics_report_by_placement
               ORDER BY
                 placement_id DESC"""
               )

        for plId in queryResultsAllPlacements:#sending every placement id on recognirion
            mlPredictOnePlacement(placement_id=plId.id,
                                  numbClusters=numbClusters,
                                  test_name=test_name,
                                  advertiser_type=advertiser_type)
    else:#recognition of one placement in database
        mlPredictOnePlacement(placement_id=placement_idRecogn,
                              numbClusters=numbClusters,
                              test_name=test_name,
                              advertiser_type=advertiser_type)


def mlGetPlacementInfoKmeans(placement_id = 1, flagAllWeek = False, test_type = "kmeans", test_name = "ctr_viewrate", advertiser_type="ecommerceAd"):#getting info about placement cluster from database
    #placement_id - palcement for recognition
    # flagAllWeek: True - return data about all weekdays, False - return about only whole week analyze
    wholeWeekInd = 7#index of whole week recognition data in column "day"
    goodClusters = mlGetGoodClusters(test_name)  # getting info about good cluster in days
    if goodClusters == -1:#if K-means didn't learn
        return -1

    test_number = mlGetTestNumber(test_type, test_name)

    if test_number == 0:
        return -1

    queryClusterInfo = MLPlacementsClustersKmeans.objects.filter(placement_id=placement_id, test_number=test_number, adv_type=advertiser_type)

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
        if str(wholeWeekInd) not in mlAnswer:
            queryClusterInfo = MLPlacementsClustersKmeans.objects.filter(
                placement_id=placement_id,
                day=wholeWeekInd,
                test_number=test_number)
            if not queryClusterInfo:
                queryClusterInfo = MLPlacementsClustersKmeans.objects.filter(
                    placement_id=placement_id,
                    test_number=test_number)
                badDistance = 0
                goodDistance = 0
                n = 0
                mlAnswer[str(wholeWeekInd)] = {}
                for row in queryClusterInfo:
                    n += 1
                    goodDistance += row.distance_to_clusters[goodClusters[row.day] - 1]
                    badDistance += row.distance_to_clusters[goodClusters[row.day] % 2]
                    mlAnswer[str(wholeWeekInd)]["checked"] = row.expert_decision
                mlAnswer[str(wholeWeekInd)]["good"] = goodDistance / n
                mlAnswer[str(wholeWeekInd)]["bad"] = badDistance / n
    else:
        queryClusterInfo = MLPlacementsClustersKmeans.objects.filter(
            placement_id=placement_id,
            day=wholeWeekInd,
            test_number=test_number,
            adv_type=advertiser_type
        )
        if not queryClusterInfo:
            queryClusterInfo = MLPlacementsClustersKmeans.objects.filter(
                placement_id=placement_id,
                test_number=test_number,
                adv_type=advertiser_type
            )
            badDistance = 0
            goodDistance = 0
            n = 0
            mlAnswer[str(wholeWeekInd)] = {}
            for row in queryClusterInfo:
                n += 1
                goodDistance += row.distance_to_clusters[goodClusters[row.day] - 1]
                badDistance += row.distance_to_clusters[goodClusters[row.day] % 2]
                mlAnswer[str(wholeWeekInd)]["checked"] = row.expert_decision
            mlAnswer[str(wholeWeekInd)]["good"] = goodDistance / n
            mlAnswer[str(wholeWeekInd)]["bad"] = badDistance / n
            return mlAnswer

        mlAnswer[str(wholeWeekInd)] = {}#insert data for answer to contoller about all weekdays
        mlAnswer[str(queryClusterInfo[0].day)]['good'] = queryClusterInfo[0].distance_to_clusters[goodClusters[queryClusterInfo[0].day] - 1]
        mlAnswer[str(queryClusterInfo[0].day)]['bad'] = queryClusterInfo[0].distance_to_clusters[goodClusters[queryClusterInfo[0].day] % 2]
        mlAnswer[str(queryClusterInfo[0].day)]['checked'] = queryClusterInfo[0].expert_decision

    return mlAnswer


def mlGetGoodClusters(test_name = "ctr_viewrate", advertiser_type="ecommerceAd"):#get array of "good" clusters for every k-means space
    numbFeaturesInDay = 0
    test_number = mlGetTestNumber("kmeans", test_name)
    if test_name == "ctr_viewrate":
        numbFeaturesInDay = 2
    if test_name == "ctr_cvr_cpc_cpm_cpa":
        numbFeaturesInDay = 5

    if numbFeaturesInDay == 0:
        print "Wrong test name"
        return -1

    numbClusters = 2
    numbDays = 8

    queryResults = MLClustersCentroidsKmeans.objects.filter(test_number=test_number, adv_type=advertiser_type)
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
        if test_name == "ctr_viewrate":
            maxClustDist = 0
        if test_name == "ctr_cvr_cpc_cpm_cpa":
            maxClustDist = -100000
        maxClust = 0
        for j in xrange(numbClusters):
            dist = 0
            if test_name == "ctr_viewrate":
                for iFeature in xrange(numbFeaturesInDay):
                    dist += centroidsCoord[i][j][iFeature] ** 2

                dist = math.sqrt(dist)
            if test_name == "ctr_cvr_cpc_cpm_cpa":
                dist = centroidsCoord[i][j][0]
                dist += centroidsCoord[i][j][1]
                dist -= centroidsCoord[i][j][2]
                dist -= centroidsCoord[i][j][3]
                dist -= centroidsCoord[i][j][4]

            if dist > maxClustDist:
                maxClustDist = dist
                maxClust = j + 1
        goodClusters.append(maxClust)
    #whole week
    if test_name == "ctr_viewrate":
        maxClustDist = 0
    if test_name == "ctr_cvr_cpc_cpm_cpa":
        maxClustDist = -100000
    for j in xrange(numbClusters):  # for all weekdays
        dist = 0
        if test_name == "ctr_viewrate":
            for iFeature in xrange(numbFeaturesInDay * (numbDays - 1)):
                dist += centroidsCoord[7][j][iFeature] ** 2
            dist = math.sqrt(dist)

        if test_name == "ctr_cvr_cpc_cpm_cpa":
            dist = centroidsCoord[7][j][0]
            dist += centroidsCoord[7][j][1]
            dist -= centroidsCoord[7][j][2]
            dist -= centroidsCoord[7][j][3]
            dist -= centroidsCoord[7][j][4]
        if dist > maxClustDist:
            maxClustDist = dist
            maxClust = j + 1
    goodClusters.append(maxClust)
    return goodClusters

def mlPredictOnePlacement(placement_id, numbClusters, test_name = "ctr_viewrate", advertiser_type="ecommerceAd"):
    numbDays = 8
    numbFeaturesInDay = 0
    test_number = 0
    if test_name == "ctr_viewrate":
        numbFeaturesInDay = 2
        test_number = 1
    if test_name == "ctr_cvr_cpc_cpm_cpa":
        numbFeaturesInDay = 5
        test_number = 2

    if test_number == 0:
        print "Wrong test name"
        return -1

    queryResults = MLClustersCentroidsKmeans.objects.filter(test_number=test_number, adv_type=advertiser_type)
    centroidsCoord = [0] * numbDays
    for i in xrange(numbDays):
        centroidsCoord[i] = [0] * numbClusters

    for row in queryResults.iterator():  # getting data about cluster centroids
        centroidsCoord[row.day][row.cluster - 1] = row.centroid

    # centroidsCoord[x][y][x] - x=day, y=cluster, z=coord numb
    #Add dow as column in DB, set trigger on it to recalculate, create index for it
    #get data about placement for recognition
    queryResultsPlacementInfo = NetworkAnalyticsReport_ByPlacement.objects.raw("""
                SELECT
                  placement_id AS id,
                  extract (dow from hour) "dow",
                  SUM(imps), SUM(clicks), SUM(total_convs), SUM(imps_viewed), SUM(view_measured_imps), SUM(cost),
                  case SUM(total_convs) when 0 then 0 else SUM(cost)::float/SUM(total_convs) end CPA,
                  case SUM(imps) when 0 then 0 else SUM(clicks)::float/SUM(imps) end CTR,
                  case SUM(imps) when 0 then 0 else SUM(total_convs)::float/SUM(imps) end CVR,
                  case SUM(clicks) when 0 then 0 else SUM(cost)::float/SUM(clicks) end CPC,
                  case SUM(imps) when 0 then 0 else SUM(cost)::float/SUM(imps) end CPM,
                  case SUM(view_measured_imps) when 0 then 0 else SUM(imps_viewed)::float/SUM(view_measured_imps) end view_rate,
                  case SUM(imps) when 0 then 0 else SUM(view_measured_imps)::float/SUM(imps) end view_measurement_rate
                FROM
                  network_analytics_report_by_placement
                  join campaign
                      on network_analytics_report_by_placement.campaign_id = campaign.id
                      join advertiser
                        on advertiser.id=campaign.advertiser_id
                WHERE
                  placement_id = """ + str(placement_id) + """ and advertiser.ad_type='""" + str(advertiser_type) + """'
                group by
                  placement_id, extract (dow from hour)
                ORDER BY
                  dow;
                """
                )
    if not queryResultsPlacementInfo:
        return -2
    allDaysPlacementFeatures = []
    for row in queryResultsPlacementInfo:#recognition of every weekday
        maxdata = MLNormalizationData.objects.filter(
            day=row.dow,
            test_number=test_number,
            adv_type=advertiser_type
        )
        maxdata = maxdata[0]
        placementClusterRecord = MLPlacementsClustersKmeans()
        placementClusterRecord.adv_type = advertiser_type
        placementClusterRecord.day = row.dow
        placementClusterRecord.placement_id = placement_id
        clustersDistance = []
        if test_name == "ctr_viewrate":
            oneDayPlacementFeatures = [row.ctr, row.view_rate]
            allDaysPlacementFeatures.append(row.ctr)
            allDaysPlacementFeatures.append(row.view_rate)
        if test_name == "ctr_cvr_cpc_cpm_cpa":
            oneDayPlacementFeatures = [row.ctr]
            allDaysPlacementFeatures.append(row.ctr)
            if row.cvr == 0:
                oneDayPlacementFeatures.append(0)
                allDaysPlacementFeatures.append(0)
            else:
                if row.cvr > maxdata.maxcvr:
                    oneDayPlacementFeatures.append(1)
                    allDaysPlacementFeatures.append(1)
                else:
                    oneDayPlacementFeatures.append(float(row.cvr) / float(maxdata.maxcvr))
                    allDaysPlacementFeatures.append(float(row.cvr) / float(maxdata.maxcvr))

            if row.cpc == 0 or row.cpc > maxdata.maxcpc:
                oneDayPlacementFeatures.append(1)
                allDaysPlacementFeatures.append(1)
            else:
                oneDayPlacementFeatures.append(float(row.cpc) / float(maxdata.maxcpc))
                allDaysPlacementFeatures.append(float(row.cpc) / float(maxdata.maxcpc))
            if row.cpm == 0 or row.cpm > maxdata.maxcpm:
                oneDayPlacementFeatures.append(1)
                allDaysPlacementFeatures.append(1)
            else:
                oneDayPlacementFeatures.append(float(row.cpm) / float(maxdata.maxcpm))
                allDaysPlacementFeatures.append(float(row.cpm) / float(maxdata.maxcpm))
            if row.cpa == 0 or row.cpa > maxdata.maxcpa:
                oneDayPlacementFeatures.append(1)
                allDaysPlacementFeatures.append(1)
            else:
                oneDayPlacementFeatures.append(float(row.cpa) / float(maxdata.maxcpa))
                allDaysPlacementFeatures.append(float(row.cpa) / float(maxdata.maxcpa))

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
        placementClusterRecord.test_number = test_number
        for i in xrange(1, numbClusters):
            if clustersDistance[i] < minDistance:
                minDistance = clustersDistance[i]
                placementClusterRecord.cluster = i + 1
        try:
            tempQuery = MLPlacementsClustersKmeans.objects.filter(
                placement_id=placement_id,
                day=placementClusterRecord.day,
                test_number=test_number,
                adv_type=advertiser_type
            )
            if not tempQuery:
                placementClusterRecord.save()
            tempQuery.update(
                distance_to_clusters=placementClusterRecord.distance_to_clusters,
                cluster=placementClusterRecord.cluster
            )
        except Exception, e:
            print "Can't save recognition info. Error: " + str(e)

    # checking of all weekdays in the week
    if len(allDaysPlacementFeatures) < (numbDays - 1) * numbFeaturesInDay:
        print "Prediction completed (not enough data for weekly space) " + str(placement_id)
        return 1
    else:
        placementClusterRecord = MLPlacementsClustersKmeans()
        placementClusterRecord.adv_type = advertiser_type
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
        placementClusterRecord.test_number = test_number
        for i in xrange(1, numbClusters):
            if clustersDistance[i] < minDistance:
                minDistance = clustersDistance[i]
                placementClusterRecord.cluster = i + 1
        goodClusters = mlGetGoodClusters("ctr_cvr_cpc_cpm_cpa", advertiser_type=advertiser_type)
        if placementClusterRecord.cluster == goodClusters[7]:
            placementClusterRecord.good = True
        else:
            placementClusterRecord.good = False

        try:
            MLPlacementsClustersKmeans.objects.update_or_create(
                placement_id=placement_id,
                day=placementClusterRecord.day,
                test_number=test_number,
                adv_type=advertiser_type,
                defaults={
                    "distance_to_clusters": placementClusterRecord.distance_to_clusters,
                    "cluster": placementClusterRecord.cluster,
                    "good": placementClusterRecord.good
                }
            )
        except Exception, e:
            print "Can't save recognition info. Error: " + str(e)
        print "Prediction completed " + str(placement_id)
        return 1

def mlmakeCsv(test_name = "ctr_viewrate"):#making csv file from recognized database
    test_number = mlGetTestNumber("kmeans", test_name)

    if test_number == 0:
        return -1

    goodClusters = mlGetGoodClusters(test_name)#getting array of good clusters for every k-means space
    queryResults = MLPlacementsClustersKmeans.objects.filter(test_number=test_number).order_by('placement_id', 'day')

    fileName = ""
    if test_number == 1:
        fileName = "ml_placements_prediction_ctr_viewrate.csv"
    if test_number == 2:
        fileName = "ml_placements_prediction_ctr_cvr_cpc_cpm_cpa.csv"

    first = True
    prevDay = 0
    with open(fileName, 'w') as csvfile:
        fieldnames = ['placement_id', 'day', 'predict', 'distance to good', 'distance to bad', 'distance difference']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for row in queryResults.iterator():
            if first:
                curPlacement = row.placement_id
                prevDay = row.day
                first = False

            if curPlacement != row.placement_id and prevDay != 7:#Ariphmetic mean
                queryClusterInfo = MLPlacementsClustersKmeans.objects.filter(
                    placement_id=curPlacement,
                    test_number=test_number)
                badDistance = 0
                goodDistance = 0
                n = 0
                for rowInf in queryClusterInfo:
                    n += 1
                    goodDistance += rowInf.distance_to_clusters[goodClusters[rowInf.day] - 1]
                    badDistance += rowInf.distance_to_clusters[goodClusters[rowInf.day] % 2]
                distGood = goodDistance / n
                distBad = badDistance / n
                if distGood < distBad:
                    prediction = "good"
                else:
                    prediction = "bad"
                dist = math.fabs(distGood - distBad)
                writer.writerow({'placement_id': curPlacement,
                                 'day': 7,
                                 'predict': prediction,
                                 'distance to good': distGood,
                                 'distance to bad': distBad,
                                 'distance difference': dist})

                curPlacement = row.placement_id


            if curPlacement != row.placement_id:
                curPlacement = row.placement_id

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
            prevDay = row.day
            writer.writerow({'placement_id': row.placement_id,
                             'day': row.day,
                             'predict': prediction,
                             'distance to good': distGood,
                             'distance to bad': distBad,
                             'distance difference': dist})

#check placement good or bad
def mlGetPlacementQuallity(placement_id = 0, test_type = "kmeans", test_name = "ctr_viewrate"):
    print "Placement: " + str(placement_id)
    if test_type == "kmeans":
        error = mlPredictOnePlacement(placement_id, 2, test_name)
        if error == 1:
            test_number = mlGetTestNumber(test_type, test_name)
            if test_number == 0:
                return -1
            answer = {}
            placementsInfo = MLPlacementsClustersKmeans.objects.filter(placement_id=placement_id, test_number=test_number)
            goodClusters = mlGetGoodClusters("ctr_cvr_cpc_cpm_cpa")
            for row in placementsInfo:
                if row.cluster == goodClusters[row.day]:
                    answer[str(row.day)] = "good"
                    print "Day " + str(row.day) + " is good"
                else:
                    answer[str(row.day)] = "bad"
                    print "Day " + str(row.day) + " is bad"
            if '7' not in answer:#arihhmetic mean
                answer['7'] = mlCalcArihmeticMean(placement_id, test_type, test_name)
                print "Day 7 is " + answer['7']
            return answer
        else:
            print "Wrong input data"
            return -1

def mlCalcArihmeticMean(placement_id, test_type, test_name):#get whole week prediction with not enough data
    test_number = mlGetTestNumber(test_type, test_name)
    if test_number == 0:
        return -1
    queryClusterInfo = MLPlacementsClustersKmeans.objects.filter(
        placement_id=placement_id,
        test_number=test_number)
    goodClusters = mlGetGoodClusters(test_name)
    badDistance = 0
    goodDistance = 0
    n = 0
    for rowInf in queryClusterInfo:
        n += 1
        goodDistance += rowInf.distance_to_clusters[goodClusters[rowInf.day] - 1]
        badDistance += rowInf.distance_to_clusters[goodClusters[rowInf.day] % 2]
    distGood = goodDistance / n
    distBad = badDistance / n
    if distGood < distBad:
        return "good"
    else:
        return "bad"

def mlGetCentroids(test_name):
    test_number = mlGetTestNumber("kmeans", test_name)
    if test_number == 0:
        return -1
    numbDays = 8
    numbClusters = 2
    queryResults = MLClustersCentroidsKmeans.objects.filter(test_number=test_number)
    # centroidsCoord[x][y][z] - x=day, y=cluster, z=coord numb
    centroidsCoord = [0] * numbDays
    for i in xrange(numbDays):
        centroidsCoord[i] = [0] * numbClusters

    for row in queryResults.iterator():  # getting data about cluster centroids
        centroidsCoord[row.day][row.cluster - 1] = row.centroid
        for iFeature in xrange(len(centroidsCoord[row.day][row.cluster - 1])):
            centroidsCoord[row.day][row.cluster - 1][iFeature] = float(centroidsCoord[row.day][row.cluster - 1][iFeature])
    return centroidsCoord

def mlGetTestNumber(test_type, test_name):
    test_number = 0
    if test_type == "kmeans":
        if test_name == "ctr_viewrate":
            test_number = 1
        if test_name == "ctr_cvr_cpc_cpm_cpa":
            test_number = 2
    if test_type == "log":
        if test_name == "ctr_cvr_cpc_cpm_cpa":
            test_number = 3
    if test_number == 0:
        print "Wrong test"
    return test_number

def mlCalcCluster(sampleFeatures, centroidsCoord, day):
    minDistance = 0
    minCluster = 0

    for iFeature in xrange(len(centroidsCoord[day][0])):
        minDistance += (
            (float(centroidsCoord[day][0][iFeature]) - float(sampleFeatures[iFeature])) ** 2)

    # centroidsCoord[x][y][z] - x=day, y=cluster, z=coord numb
    for iCluster in xrange(1, len(centroidsCoord[day])):
        curDistance = 0
        for iFeature in xrange(len(centroidsCoord[day][iCluster])):
            curDistance += (
                (float(centroidsCoord[day][iCluster][iFeature]) - float(sampleFeatures[iFeature])) ** 2)
        if curDistance < minDistance:
            minDistance = curDistance
            minCluster = iCluster
    return (minCluster + 1)