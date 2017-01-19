from rtb.ml_general import mlGetPlacementsInfo, mlGetOnePlacementFeatures
from sklearn.externals import joblib
from sklearn import tree
from models import NetworkAnalyticsReport_ByPlacement
import graphviz
from rtb.models.ml_decision_tree_model import MLDecisionTreeClassifierResults

def mlCreateDecisionClassifierTree(test_name, goodPlacementsIds, badPlacementsIds):
    allFeaturesForRecognition, recognitionMarks = mlGetPlacementsInfo(test_name=test_name,
                                                                      teacher=True,
                                                                      goodPlacementsIds=goodPlacementsIds,
                                                                      badPlacementsIds=badPlacementsIds)
    print "creating tree"
    treeClassifier = tree.DecisionTreeClassifier().fit(allFeaturesForRecognition, recognitionMarks)
    joblib.dump(treeClassifier, "decision_classifier_tree_weekly.pkl", compress=1)
    feature_names = ["Sunday ctr", "Sunday cvr", "Sunday cpc", "Sunday cpm", "Sunday cpa",
                     "Monday ctr", "Monday cvr", "Monday cpc", "Monday cpm", "Monday cpa",
                     "Tuesday ctr", "Tuesday cvr", "Tuesday cpc", "Tuesday cpm", "Tuesday cpa",
                     "Wednesday ctr", "Wednesday cvr", "Wednesday cpc", "Wednesday cpm", "Wednesday cpa",
                     "Thursday ctr", "Thursday cvr", "Thursday cpc", "Thursday cpm", "Thursday cpa",
                     "Friday ctr", "Friday cvr", "Friday cpc", "Friday cpm", "Friday cpa",
                     "Saturday ctr", "Saturday cvr", "Saturday cpc", "Saturday cpm", "Saturday cpa"]
    class_names = ["bad", "good"]
    print "save png"
    dot_data = tree.export_graphviz(treeClassifier, out_file="decision_classifier_tree_weekly.dot",
                                    feature_names=feature_names,
                                    class_names=class_names,
                                    filled=True, rounded=True,
                                    special_characters=True)
    graphviz.render("dot", "png", "decision_classifier_tree_weekly.dot")


def mlPredictDecisionClassifierTree(placement_id, test_name):
    if test_name == "ctr_cvr_cpc_cpm_cpa":
        try:
            treeClassifier = joblib.load("decision_classifier_tree_weekly.pkl")
        except Exception, e:
            print "Decision tree is not exist. Train model first"
            return -1
        if placement_id == -1:#recognize all placements
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

            for plId in queryResultsAllPlacements:
                features = mlGetOnePlacementFeatures(test_name=test_name, placement_id=plId.id)
                treeClassifier.predict(features)

        else:#recognize single placement
            features = mlGetOnePlacementFeatures(test_name=test_name, placement_id=placement_id)
            if treeClassifier.predict(features)[0] == 0:
                MLDecisionTreeClassifierResults.objects.update_or_create(
                    placement_id=placement_id,
                    day=7,
                    test_number=4,
                    defaults={
                        "good": False
                    }
                )
                return False
            else:
                MLDecisionTreeClassifierResults.objects.update_or_create(
                    placement_id=placement_id,
                    day=7,
                    test_number=4,
                    defaults={
                        "good" : True
                }
                )
                return True

