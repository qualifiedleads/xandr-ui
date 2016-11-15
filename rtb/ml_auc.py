from ml_learn_kmeans import mlGetGoodClusters, mlGetCentroids, mlGetTestNumber, mlCalcCluster
from models.ml_kmeans_model import MLPlacementDailyFeatures, MLClustersCentroidsKmeans, MLPlacementsClustersKmeans, \
    MLNormalizationData, MLExpertsPlacementsMarks, MLTestDataSet
from models import NetworkAnalyticsReport_ByPlacement
from django.utils import timezone
import datetime

class mlPlacementsSet:
    placements = None
    test_type = None
    test_name = None

    def __init__(self, placementsIdSet, everyWeekDay, test_type, test_name):
        self.test_name = test_name
        self.test_type = test_type
        self.placements = []
        sqlSelectInPlacements = "(" + str(placementsIdSet[0])
        for i in xrange(1, len(placementsIdSet)):
            sqlSelectInPlacements += "," + str(placementsIdSet[i])
        sqlSelectInPlacements += ")"

        queryResultsPlacementInfo = NetworkAnalyticsReport_ByPlacement.objects.raw("""
                                SELECT
                                  placement_id AS id,
                                  extract (dow from hour) "dow",
                                  case SUM(total_convs) when 0 then 0 else SUM(cost)::float/SUM(total_convs) end CPA,
                                  case SUM(imps) when 0 then 0 else SUM(clicks)::float/SUM(imps) end CTR,
                                  case SUM(imps) when 0 then 0 else SUM(total_convs)::float/SUM(imps) end CVR,
                                  case SUM(clicks) when 0 then 0 else SUM(cost)::float/SUM(clicks) end CPC,
                                  case SUM(imps) when 0 then 0 else SUM(cost)::float/SUM(imps) end CPM
                                FROM
                                  network_analytics_report_by_placement
                                WHERE
                                  placement_id IN """ + sqlSelectInPlacements + """
                                group by
                                  placement_id, extract (dow from hour)
                                ORDER BY
                                  id, dow;
                                """
                                                                                   )
        goodClusters = mlGetGoodClusters(test_name)
        wholeWeekFeatures = []
        curId = 0
        curDays = 0
        for row in queryResultsPlacementInfo:
            if curId != row.id:
                wholeWeekFeatures = []
                curId = row.id
                curDays = 0
            tableFeatures = {}
            if test_name == "ctr_cvr_cpc_cpm_cpa":
                tableFeatures["ctr"] = row.ctr
                tableFeatures["cvr"] = row.cvr
                tableFeatures["cpc"] = row.cpc
                tableFeatures["cpm"] = row.cpm
                tableFeatures["cpa"] = row.cpa
                wholeWeekFeatures.append(tableFeatures)

            if everyWeekDay == True:#if we need to save features for every week day
                self.placements.append(
                    mlPlacementInfo(
                        incPlacementid=row.id,
                        incday=row.dow,
                        tableFeatures=tableFeatures,
                        goodCluster=goodClusters[row.dow],
                        test_type=test_type,
                        test_name=test_name))
            curDays += 1
            if curDays == 7:
                self.placements.append(
                    mlPlacementInfo(
                        incPlacementid=row.id,
                        incday=7,
                        tableFeatures=wholeWeekFeatures,
                        goodCluster=goodClusters[7],
                        test_type=test_type,
                        test_name=test_name))


class mlPlacementInfo:
    placement_id = None
    day = None
    features = None
    expert_cluster = None

    def __init__(self, incPlacementid, incday, tableFeatures, goodCluster, test_type = None, test_name = None):
        test_number = mlGetTestNumber(test_type, test_name)
        if test_number == 0:
            self.placement_id = -1
            return
        self.placement_id = incPlacementid
        self.day = incday

        expertMark = MLExpertsPlacementsMarks.objects.filter(placement_id=incPlacementid, day=7)
        if expertMark[0].expert_decision == "good":
            self.expert_cluster = goodCluster
        if expertMark[0].expert_decision == "bad":
            self.expert_cluster = goodCluster % 2 + 1

        self.features = []

        if incday != 7:
            maxData = MLNormalizationData.objects.filter(day=incday, test_number=test_number)
            self.features.append(tableFeatures["ctr"])
            if tableFeatures["cvr"] == 0:
                self.features.append(0)
            else:
                self.features.append(float(tableFeatures["cvr"]) / float(maxData[0].maxcvr))

            if tableFeatures["cpc"] == 0:
                self.features.append(1)
            else:
                self.features.append(float(tableFeatures["cpc"]) / float(maxData[0].maxcpc))

            if tableFeatures["cpm"] == 0:
                self.features.append(1)
            else:
                self.features.append(float(tableFeatures["cpm"]) / float(maxData[0].maxcpm))

            if tableFeatures["cpa"] == 0:
                self.features.append(1)
            else:
                self.features.append(float(tableFeatures["cpa"]) / float(maxData[0].maxcpa))
        else:
            numbDays = 7
            for iDay in xrange(numbDays):
                maxData = MLNormalizationData.objects.filter(day=iDay, test_number=test_number)
                self.features.append(tableFeatures[iDay]["ctr"])
                if tableFeatures[iDay]["cvr"] == 0:
                    self.features.append(0)
                else:
                    self.features.append(float(tableFeatures[iDay]["cvr"]) / float(maxData[0].maxcvr))

                if tableFeatures[iDay]["cpc"] == 0:
                    self.features.append(1)
                else:
                    self.features.append(float(tableFeatures[iDay]["cpc"]) / float(maxData[0].maxcpc))

                if tableFeatures[iDay]["cpm"] == 0:
                    self.features.append(1)
                else:
                    self.features.append(float(tableFeatures[iDay]["cpm"]) / float(maxData[0].maxcpm))

                if tableFeatures[iDay]["cpa"] == 0:
                    self.features.append(1)
                else:
                    self.features.append(float(tableFeatures[iDay]["cpa"]) / float(maxData[0].maxcpa))


def mlBuildROC(test_type = "kmeans", test_name = "ctr_cvr_cpc_cpm_cpa", date = -1):
    numbDays = 8
    samplesNumb = 127
    if test_type == "kmeans":
        goodClusters = mlGetGoodClusters(test_name)
        if goodClusters == -1:
            print "System isn't taught"
            return -1, -1

        testPlacementsIds = []
        if date == -1:#getting latest test dataset and adding it placements to our list
            max_date = MLTestDataSet.objects.latest("created")
            res = MLTestDataSet.objects.filter(created=max_date.created).values("data")
            for record in res[0]["data"]:
                testPlacementsIds.append(record["placement_id"])
        else:
            pass#TODO getting data from exactly date test dataset

        testSamples = MLExpertsPlacementsMarks.objects.filter(
            placement_id__in=testPlacementsIds,
            expert_decision__isnull=False
        )


        if len(testSamples) != samplesNumb:
            print "Not all placements are marked by experts"
            return -1, -1

        goodPlacements = []
        badPlacements = []
        for placement in testSamples:  # CHANGE TO ADDING EXPERTS TRUE TEST SAMPLES
            if placement.expert_decision == "good":
                goodPlacements.append(placement.placement_id)
            if placement.expert_decision == "bad":
                badPlacements.append(placement.placement_id)
        goodClusterSamples = mlPlacementsSet(goodPlacements, False, test_type, test_name)
        badClusterSamples = mlPlacementsSet(badPlacements, False, test_type, test_name)

        centroidsCoord = mlGetCentroids(test_name)#get centroids coord
        #centroidsCoord[x][y][z] - x=day, y=cluster, z=coord numb
        numbFeatures = len(centroidsCoord[0][0])
        directions = [0] * numbDays
        for i in xrange(numbDays):
            if i == (numbDays - 1):
                directions[i] = [0] * (numbFeatures * (numbDays - 1))
            else:
                directions[i] = [0] * numbFeatures#in which side cluster is going for every day
        #directions[day][feature] = direction
        for iDay in xrange(numbDays):#set directions
            for iFeature in xrange(len(centroidsCoord[iDay][0])):
                if centroidsCoord[iDay][0][iFeature] > centroidsCoord[iDay][1][iFeature]:
                    directions[iDay][iFeature] = 1
                else:
                    directions[iDay][iFeature] = -1
        delta = 0.00001
        rocSensetivities = []
        rocFalsePositivesRates = []
        # set up variables for getting new ROC coord
        testResults = {}
        testResults["true_positives"] = 0.0
        testResults["false_negatives"] = 0.0
        testResults["true_negatives"] = 0.0
        testResults["false_positives"] = 0.0
        for placement in goodClusterSamples.placements:
            curCluster = mlCalcCluster(placement.features, centroidsCoord, 7)
            if curCluster == placement.expert_cluster:
                testResults["true_negatives"] += 1
            else:
                testResults["false_positives"] += 1
        for placement in badClusterSamples.placements:
            curCluster = mlCalcCluster(placement.features, centroidsCoord, 7)
            if curCluster == placement.expert_cluster:
                testResults["true_positives"] += 1
            else:
                testResults["false_negatives"] += 1

        falsePositiveRate = float(testResults["false_positives"]) / float(
            (testResults["false_positives"] + testResults["true_negatives"])) * 100
        sensetivity = float(testResults["true_positives"]) / (testResults["true_positives"] + testResults["false_negatives"]) * 100
        rocSensetivities.append(sensetivity)
        rocFalsePositivesRates.append(falsePositiveRate)
        # first cluster is going out of second
        while True:#checkpoint
            #set up variables for getting new ROC coord
            testResults["true_positives"] = 0.0
            testResults["false_negatives"] = 0.0
            testResults["true_negatives"] = 0.0
            testResults["false_positives"] = 0.0

            for iDay in xrange(numbDays):  # changing of centroid coords
                for iFeature in xrange(numbFeatures):
                    centroidsCoord[iDay][0][iFeature] = centroidsCoord[iDay][0][iFeature] + (delta * directions[iDay][iFeature])

            for placement in goodClusterSamples.placements:#getting data for rates calculating
                curCluster = mlCalcCluster(placement.features, centroidsCoord, 7)
                if curCluster == placement.expert_cluster:
                    testResults["true_negatives"] += 1
                else:
                    testResults["false_positives"] += 1
            for placement in badClusterSamples.placements:
                curCluster = mlCalcCluster(placement.features, centroidsCoord, 7)
                if curCluster == placement.expert_cluster:
                    testResults["true_positives"] += 1
                else:
                    testResults["false_negatives"] += 1

            falsePositiveRate = float(testResults["false_positives"]) / float((
                testResults["false_positives"] + testResults["true_negatives"])) * 100
            sensetivity = float(testResults["true_positives"]) / (testResults["true_positives"] + testResults["false_negatives"]) * 100

            newPoint = True #check if that is new point on the chart
            for i in xrange(len(rocSensetivities)):
                if sensetivity == rocSensetivities[i]:
                    if falsePositiveRate == rocFalsePositivesRates[i]:
                        newPoint = False
                        break
            if newPoint == True:
                rocSensetivities.append(sensetivity)
                rocFalsePositivesRates.append(falsePositiveRate)
                delta = delta / 2
            else:
                delta = delta * 2

            if (sensetivity == 100 and falsePositiveRate == 100) or (sensetivity == 0 and falsePositiveRate == 0):
                break
        #second cluster is going out of first
        for iDay in xrange(numbDays):  # change direction
            for iFeature in xrange(len(centroidsCoord[iDay][0])):
                directions[iDay][iFeature] = directions[iDay][iFeature] * (-1)

        centroidsCoord = mlGetCentroids(test_name)
        delta = 0.00001
        while True:
            # set up variables for getting new ROC coord
            testResults["true_positives"] = 0.0
            testResults["false_negatives"] = 0.0
            testResults["true_negatives"] = 0.0
            testResults["false_positives"] = 0.0

            for iDay in xrange(numbDays):  # change centroid coords
                for iFeature in xrange(numbFeatures):
                    centroidsCoord[iDay][1][iFeature] += (delta * directions[iDay][iFeature])

            for placement in goodClusterSamples.placements:  # calculating
                curCluster = mlCalcCluster(placement.features, centroidsCoord, 7)
                if curCluster == placement.expert_cluster:
                    testResults["true_negatives"] += 1
                else:
                    testResults["false_positives"] += 1
            for placement in badClusterSamples.placements:
                curCluster = mlCalcCluster(placement.features, centroidsCoord, 7)
                if curCluster == placement.expert_cluster:
                    testResults["true_positives"] += 1
                else:
                    testResults["false_negatives"] += 1

            falsePositiveRate = float(testResults["false_positives"]) / float((
                testResults["false_positives"] + testResults["true_negatives"])) * 100
            sensetivity = float(testResults["true_positives"]) / (
                testResults["true_positives"] + testResults["false_negatives"]) * 100
            newPoint = True  # check if that is new point on the chart
            for i in xrange(len(rocSensetivities)):
                if sensetivity == rocSensetivities[i]:
                    if falsePositiveRate == rocFalsePositivesRates[i]:
                        newPoint = False
                        break
            if newPoint == True:
                rocSensetivities.append(sensetivity)
                rocFalsePositivesRates.append(falsePositiveRate)
                delta = delta / 2
            else:
                delta = delta * 2

            if (sensetivity == 100 and falsePositiveRate == 100) or (sensetivity == 0 and falsePositiveRate == 0):
                break
        return rocSensetivities, rocFalsePositivesRates

    if test_type == "log":
        return

    print "Wrong test type"
    return -1

def quickSort(FPR, sens):
   quickSortHelper(FPR,0,len(FPR)-1, sens)

def quickSortHelper(FPR,first,last, sens):
   if first<last:

       splitpoint = partition(FPR,first,last, sens)

       quickSortHelper(FPR,first,splitpoint-1, sens)
       quickSortHelper(FPR,splitpoint+1,last, sens)


def partition(FPR,first,last, sens):
   pivotvalue = FPR[first]
   leftmark = first+1
   rightmark = last
   done = False
   while not done:
       while leftmark <= rightmark and \
               FPR[leftmark] <= pivotvalue:
           leftmark = leftmark + 1

       while FPR[rightmark] >= pivotvalue and \
               rightmark >= leftmark:
           rightmark = rightmark -1

       if rightmark < leftmark:
           done = True
       else:
           temp = FPR[leftmark]
           FPR[leftmark] = FPR[rightmark]
           FPR[rightmark] = temp
           temp = sens[leftmark]
           sens[leftmark] = sens[rightmark]
           sens[rightmark] = temp
   temp = FPR[first]
   FPR[first] = FPR[rightmark]
   FPR[rightmark] = temp
   temp = sens[first]
   sens[first] = sens[rightmark]
   sens[rightmark] = temp
   return rightmark

def mlCalcAuc(test_type = "kmeans", test_name = "ctr_cvr_cpc_cpm_cpa", date = -1):
    rocSensetivities, rocFalsePositivesRates = mlBuildROC(test_type, test_name)
    if rocSensetivities == -1:
        return -1
    quickSort(rocFalsePositivesRates, rocSensetivities)#create sorting of rocSensetivities,rocFalsePositivesRates asc

    i = 1#sorting of the points with same FPR
    while i < len(rocFalsePositivesRates):
        if rocFalsePositivesRates[i - 1] == rocFalsePositivesRates[i]:
            for j in xrange(i + 1, len(rocFalsePositivesRates)):
                if rocFalsePositivesRates[j] != rocFalsePositivesRates[i]:
                    for indIns in xrange(i - 1, j):
                        indMin = indIns
                        valMin = rocSensetivities[indIns]
                        for indIn in xrange(indIns, j):
                            if rocSensetivities[indIn] < valMin:
                                indMin = indIn
                                valMin = rocSensetivities[indIn]
                        temp = rocSensetivities[indIns]
                        rocSensetivities[indIns] = rocSensetivities[indMin]
                        rocSensetivities[indMin] = temp
                    i = j - 1
                    break
        i += 1

    auc = 0
    for i in xrange(1, len(rocFalsePositivesRates)):
        auc += ((((rocSensetivities[i-1] + rocSensetivities[i])/100.0) * ((rocFalsePositivesRates[i] - rocFalsePositivesRates[i-1])/100.0)) / 2.0)
    res = {}
    res["auc"] = auc
    res["chartCoord"] = []
    for i in xrange(len(rocSensetivities)):
        temp = {}
        temp["rocFalsePositiveRate"] = rocFalsePositivesRates[i]
        temp["rocSensetivities"] = rocSensetivities[i]
        res["chartCoord"].append(temp)
    return res
