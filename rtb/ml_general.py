import numpy as np
from rtb.models.ml_kmeans_model import MLPlacementDailyFeatures
from models import NetworkAnalyticsReport_ByPlacement
import graphviz
from subprocess import check_call
import pydot

def mlGetPlacementsInfo(test_name = None, placementsIds = None, teacher = False, goodPlacementsIds = None, badPlacementsIds = None):
    if teacher:#create set for a learning with teacher
        if test_name == "ctr_cvr_cpc_cpm_cpa":
            if goodPlacementsIds is None or badPlacementsIds is None:
                print "No data in IDs info"
                return -1
            numbDays = 7
            numbFeaturesInDay = 0
            test_number_base = 0
            if test_name == "ctr_cvr_cpc_cpm_cpa":
                numbFeaturesInDay = 5
                test_number_base = 3
            if test_number_base == 0:
                print "Wrong test name"
                return -1

            placementsMarks = {}
            sqlMarkedPlacementsIn = "("

            for placement in goodPlacementsIds:
                placementsMarks[str(placement)] = "good"
                sqlMarkedPlacementsIn += (str(placement) + ',')
            for placement in badPlacementsIds:
                placementsMarks[str(placement)] = "bad"
                sqlMarkedPlacementsIn += (str(placement) + ',')

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

            for row in queryResults:  # filling placements features for learning
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
            return allFeaturesForRecognition, recognitionMarks
    else:#create set for a learning without teacher
        pass

def mlGetOnePlacementFeatures(test_name, placement_id):
    if test_name == "ctr_cvr_cpc_cpm_cpa":
        placementInfo = NetworkAnalyticsReport_ByPlacement.objects.raw("""
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
        placementFeatures = np.zeros(35)# getting placement features
        cur = 0
        for row in placementInfo:
            placementFeatures[cur] = (float(row.ctr))
            placementFeatures[cur + 1] = (float(row.cvr))
            placementFeatures[cur + 2] = (float(row.cpc))
            placementFeatures[cur + 3] = (float(row.cpm))
            placementFeatures[cur + 4] = (float(row.cpa))
            cur += 5

        placementFeatures = placementFeatures.reshape(1, -1)
        return placementFeatures