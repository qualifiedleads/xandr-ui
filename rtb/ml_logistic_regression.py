import numpy as np
from sklearn import linear_model
import math
from django.db.models import Sum, Min, Max, Avg, Value, When, Case, F, Q, Func, FloatField, Count
from models.ml_logistic_regression_models import MLLogisticRegressionResults, MLLogisticRegressionCoeff
from models.ml_kmeans_model import MLPlacementDailyFeatures, MLExpertsPlacementsMarks
from models import NetworkAnalyticsReport_ByPlacement
from rtb.ml_learn_kmeans import mlGetTestNumber

#learn logistic regression model
def mlLearnLogisticRegression(test_name = "ctr_cvr_cpc_cpm_cpa"):
    numbDays = 7
    numbFeaturesInDay = 0
    test_number_base = 0
    if test_name == "ctr_cvr_cpc_cpm_cpa":
        numbFeaturesInDay = 5
        test_number_base = 3
    if test_number_base == 0:
        print "Wrong test name"
        return -1

    allMarkedPlacements = []#TODO remove into the loop if we will get experts mark for every weekday
    queryResults = MLExpertsPlacementsMarks.objects.filter(expert_decision__isnull=False)
    if not queryResults:
        print "Data base hasn't any of expert marks"
        return -1
    placementsMarks = {}
    sqlMarkedPlacementsIn = "("
    for row in queryResults.iterator():
        allMarkedPlacements.append(row.placement_id)
        placementsMarks[str(row.placement_id)] = row.expert_decision
        sqlMarkedPlacementsIn += (str(row.placement_id) + ',')

    sqlMarkedPlacementsIn = sqlMarkedPlacementsIn[:-1]
    sqlMarkedPlacementsIn += ')'
    queryResults = MLPlacementDailyFeatures.objects.raw("""
    SELECT
      *
    FROM
      ml_placement_daily_features
    WHERE
      placement_id IN(
      SELECT placement_id
      FROM ml_placement_daily_features
      GROUP BY placement_id
      HAVING COUNT(day) = 7
      ) AND
      placement_id IN""" + sqlMarkedPlacementsIn +
    """ORDER BY
      placement_id, day
    """)

    allFeatures = []
    allFeaturesPlacement = []

    onePlacementFeatures = np.zeros(numbFeaturesInDay * numbDays)
    recognitionMarks = []
    numbPlacement = 0
    curFeature = 0
    allFeaturesNumb = numbFeaturesInDay * numbDays

    for row in queryResults:#filling placements features for learning
        if test_name == "ctr_cvr_cpc_cpm_cpa":
            onePlacementFeatures[curFeature] = row.ctr
            onePlacementFeatures[curFeature + 1] = row.cvr
            onePlacementFeatures[curFeature + 2] = row.cpc
            onePlacementFeatures[curFeature + 3] = row.cpm
            onePlacementFeatures[curFeature + 4] = row.cpa

        curFeature += 5
        if curFeature == (allFeaturesNumb):
            if placementsMarks[str(row.placement_id)] == "good":
                recognitionMarks.append(1)
            if placementsMarks[str(row.placement_id)] == "bad":
                recognitionMarks.append(0)
            allFeatures.append(onePlacementFeatures)
            allFeaturesPlacement.append(row.placement_id)
            onePlacementFeatures = np.zeros(numbFeaturesInDay * numbDays)
            numbPlacement += 1
            curFeature = 0

    allFeatures = np.float32(allFeatures)
    allFeaturesForRecognition = np.vstack(allFeatures)
    recognitionMarks = np.float32(recognitionMarks)
    logitModel = linear_model.LogisticRegression(C=1e5)
    logitModel.fit(allFeaturesForRecognition, recognitionMarks)

    testDirectionFeatures = allFeaturesForRecognition[0]#get good direction of probability
    testDirectionMark = recognitionMarks[0]
    testDirectionFeatures = testDirectionFeatures.reshape(1, -1)
    testDirectionFunc = logitModel.decision_function(testDirectionFeatures)[0]
    testDirectionProbability = 1.0 / (1.0 + math.exp(testDirectionFunc))
    goodDirection = ""
    if testDirectionMark == logitModel.predict(testDirectionFeatures)[0]:
        if testDirectionMark == 1:
            if testDirectionProbability > 0.5:
                goodDirection = "higher"
            else:
                goodDirection = "lower"
        if testDirectionMark == 0:
            if testDirectionProbability > 0.5:
                goodDirection = "lower"
            else:
                goodDirection = "higher"

    if goodDirection == "":
        MLLogisticRegressionCoeff.objects.update_or_create(
            day=7,
            test_number=3,
            defaults={
                "coeff":logitModel.coef_[0].tolist()
            }
        )
    else:
        MLLogisticRegressionCoeff.objects.update_or_create(
            day=7,
            test_number=3,
            defaults={
                "coeff": logitModel.coef_[0].tolist(),
                "good_direction": goodDirection
            }
        )
    print "Model is done"

#predict log regression
def mlPredictLogisticRegression(placement_id, test_name = "ctr_cvr_cpc_cpm_cpa"):
    print "Logistic regression"
    if placement_id == -1:#predict all
        queryResultsAllPlacements = NetworkAnalyticsReport_ByPlacement.objects.raw("""
                       SELECT
                          placement_id AS id
                        FROM
                          network_analytics_report_by_placement
                        GROUP BY
                          placement_id
                        HAVING
                          COUNT(DISTINCT extract ( dow from hour)) = 7 and SUM(imps) >=1000
                        ORDER BY
                          placement_id DESC;"""
                                                                                   )

        for plId in queryResultsAllPlacements:  # sending every placement id on recognirion
            mlPredictOnePlacementLogisticRegression(placement_id=plId.id,test_name=test_name,check_days=False)
    else:#predict one placement
        mlPredictOnePlacementLogisticRegression(placement_id=placement_id, test_name=test_name,check_days=True)

def mlPredictOnePlacementLogisticRegression(placement_id, test_name = "ctr_cvr_cpc_cpm_cpa",check_days=True):
    test_number = mlGetTestNumber(test_type="log", test_name=test_name)#checking validation of the test
    if test_number == 0:
        print "Wrong test name"
        return -1
    #get regression coefficients
    coefficients = MLLogisticRegressionCoeff.objects.filter(
        test_number=test_number,
        day=7
    )[0].coeff
    for i in xrange(len(coefficients)):
        coefficients[i] = float(coefficients[i])
    if check_days:#checking: is placement has data for every weekday
        res = NetworkAnalyticsReport_ByPlacement.objects.raw("""
        SELECT placement_id AS id, COUNT(DISTINCT extract ( dow from hour)) AS days
        FROM network_analytics_report_by_placement
        WHERE placement_id=""" + str(placement_id) +  """
        GROUP BY placement_id
        """)
        if res[0].days != 7:
            print "Not enough weekdays data in " + str(placement_id) + " placement"
            return -1
    queryResultsPlacementInfo = NetworkAnalyticsReport_ByPlacement.objects.raw("""
                                    SELECT
                                      placement_id AS id,
                                      extract (dow from hour) "dow",
                                      case SUM(total_convs) when 0 then 0 else SUM(cost)::float/SUM(total_convs) end cpa,
                                      case SUM(imps) when 0 then 0 else SUM(clicks)::float/SUM(imps) end ctr,
                                      case SUM(imps) when 0 then 0 else SUM(total_convs)::float/SUM(imps) end cvr,
                                      case SUM(clicks) when 0 then 0 else SUM(cost)::float/SUM(clicks) end cpc,
                                      case SUM(imps) when 0 then 0 else SUM(cost)::float/SUM(imps) end cpm
                                    FROM
                                      network_analytics_report_by_placement
                                    WHERE
                                      placement_id = """ + str(placement_id) + """
                                    group by
                                      placement_id, extract (dow from hour)
                                    ORDER BY
                                      id, dow;
                                    """
    )
    placementFeatures = []#getting placement features
    for row in queryResultsPlacementInfo:
        placementFeatures.append(float(row.ctr))
        placementFeatures.append(float(row.cvr))
        placementFeatures.append(float(row.cpc))
        placementFeatures.append(float(row.cpm))
        placementFeatures.append(float(row.cpa))

    functionValue = 0#calc value of decision function
    for i in xrange(len(placementFeatures)):
        functionValue += (placementFeatures[i] * coefficients[i])
    if functionValue > 700:
        prob = 0
    else:
        prob = 1.0 / (1.0 + math.exp(functionValue))#calc probability of class
    MLLogisticRegressionResults.objects.update_or_create(
        placement_id=placement_id,
        day=7,
        test_number=3,
        defaults={
            "probability": prob
        }
    )
    print "Placement " + str(placement_id) + " predicted"