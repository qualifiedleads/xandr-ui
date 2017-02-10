from rest_framework.decorators import api_view, parser_classes
from rest_framework.response import Response
from rtb.models.ml_video_ad_model import MLVideoAdCampaignsModelsInfo, MLVideoAdCampaignsModels, MLVideoAdCampaignsResults, MLVideoImpsTracker
from rest_framework import status
from sklearn.externals import joblib
from os.path import isfile
from rtb.crons.ml_video_ad_camp_algo_cron import getMLCpmData, getDataWindow
from datetime import datetime, timedelta

@api_view(["GET"])
# @check_user_advertiser_permissions(campaign_id_num=0)
def apiSendMLGraphInfo(request, id):
    algoVocabl = []
    algoVocabl.append("gradient")
    algoVocabl.append("random_forest")
    algoVocabl.append("abtree")
    algoList = {}
    frontCaptions = []
    frontCaptions.append({
        "name": "Switch off automatic CPM",
        "back_name": "none"
    })
    frontCaptions.append({
        "name": "Gradient boosting",
        "back_name": "gradient"
    })
    frontCaptions.append({
        "name": "Random forest",
        "back_name": "random_forest"
    })
    frontCaptions.append({
        "name": "Decision tree",
        "back_name": "abtree"
    })
    cpmGraph = []
    fillrateGraph = []
    profitGraph = []
    # predict models loading
    for i in xrange(len(algoVocabl)):
        if isfile("rtb/res/prediction_models_cpm/" + str(id) + "_" + str(algoVocabl[i]) + ".pkl"):
            algoList[algoVocabl[i]] = joblib.load("rtb/res/prediction_models_cpm/" + str(id) + "_" + str(algoVocabl[i]) + ".pkl")

    data = getMLCpmData(
        campaignId=id,
        fromDate=datetime.now() - timedelta(days=7),
        toDate=datetime.now()
    )
    # data:
    # 0 - current hour from the day start
    # 1 - imps
    # 2 - ad starts
    # 3 - fill rate
    # 4 - cpm
    # 5 - profit/loss
    # 6 - date
    # 7 - rpm
    allFillRate = {}
    allCpm = {}
    allProfit = {}
    allDate = []
    allFillRate["true"] = []
    allCpm["true"] = []
    allProfit["true"] = []

    for i in xrange(len(data)):
        allDate.append(datetime.strftime(data[i][6], "%Y-%m-%d %H:%M:%S"))
        allFillRate["true"].append(data[i][3])
        allCpm["true"].append(data[i][4])
        allProfit["true"].append(data[i][5])

    for algoName, algo in algoList.iteritems():
        allFillRate[algoName] = []
        allCpm[algoName] = []
        allProfit[algoName] = []
        windowData, allFeatures, allResults = getDataWindow(
            type=algoVocabl.index(algoName),
            data=data,
            windowSize=12
        )
        ans = algoList[algoName].predict(allFeatures)
        for k in xrange(len(ans)):
            allFillRate[algoName].append(ans[k])
            allCpm[algoName].append(ans[k] * float(windowData[k][7]))
            if ans[k] < 0:
                ans[k] = 0
            ans[k] = ans[k] / 100.0
            allProfit[algoName].append(float(windowData[k + 1][2]) * float(windowData[k + 1][7]) / 1000.0 - float(windowData[k + 1][1]) * (
            ans[k] * float(windowData[k + 1][7])) / 1000.0)

    windowSize = 12
    for i in xrange(len(allDate)):
        cpmGraph.append({
            "date": allDate[i],
            "true_cpm": round(allCpm["true"][i],2),
            "gradient_cpm": round(allCpm[algoVocabl[0]][i-windowSize],2) if (algoVocabl[0] in allCpm and i >= windowSize) else None,
            "random_forest_cpm": round(allCpm[algoVocabl[1]][i-windowSize],2) if (algoVocabl[1] in allCpm and i >= windowSize) else None,
            "abtree_cpm": round(allCpm[algoVocabl[2]][i-windowSize],2) if (algoVocabl[2] in allCpm and i >= windowSize) else None
        })
        fillrateGraph.append({
            "date": allDate[i],
            "true_fillrate": round(allFillRate["true"][i],2),
            "gradient_fillrate": round(allFillRate[algoVocabl[0]][i-windowSize],2) if (algoVocabl[0] in allFillRate and i >=windowSize) else None,
            "random_forest_fillrate": round(allFillRate[algoVocabl[1]][i-windowSize],2) if (algoVocabl[1] in allFillRate and i >=windowSize) else None,
            "abtree_fillrate": round(allFillRate[algoVocabl[2]][i-windowSize],2) if (algoVocabl[2] in allFillRate and i >=windowSize) else None
        })
        profitGraph.append({
            "date": allDate[i],
            "true_profit": round(allProfit["true"][i],2),
            "gradient_profit": round(allProfit[algoVocabl[0]][i-windowSize],2) if (algoVocabl[0] in allProfit and i >=windowSize) else None,
            "random_forest_profit": round(allProfit[algoVocabl[1]][i-windowSize],2) if (algoVocabl[1] in allProfit and i >=windowSize) else None,
            "abtree_profit": round(allProfit[algoVocabl[2]][i-windowSize],2) if (algoVocabl[2] in allProfit and i >=windowSize) else None
            })

    queryAns = {}
    queryAns["choice_list"] = frontCaptions
    curAlgo = MLVideoAdCampaignsModels.objects.filter(campaign_id=id)
    if not curAlgo:
        queryAns["current_algo"] = "None"
    else:
        queryAns["current_algo"] = frontCaptions[algoVocabl.index(curAlgo[0].type)+1]["name"]
    queryAns["cpm_graph"] = cpmGraph
    queryAns["fillrate_graph"] = fillrateGraph
    queryAns["profit_graph"] = profitGraph


    return Response(queryAns)


@api_view(["PUT"])
# @check_user_advertiser_permissions(campaign_id_num=0)
def apiSetCampaignAlgo(request, id):
    try:
        if request.data.get("back_name") == "none":
            MLVideoAdCampaignsModels.objects.filter(
                advertiser_id=request.data.get("advertiserId"),
                campaign_id=id,
            ).delete()
            return Response({"current_algo": "None"})
        queryRes = MLVideoAdCampaignsModelsInfo.objects.filter(
            campaign_id=id,
            type=request.data.get("back_name")
        )
        MLVideoAdCampaignsModels.objects.update_or_create(
            advertiser_id=request.data.get("advertiserId"),
            campaign_id=id,
            defaults={
                "path": queryRes[0].path,
                "type": queryRes[0].type
            }
        )
        frontCaptions = {}
        frontCaptions["gradient"] = "Gradient boosting"
        frontCaptions["random_forest"] = "Random forest"
        frontCaptions["abtree"] = "Decision tree"
        return Response({"current_algo": frontCaptions[request.data.get("back_name")]})
    except Exception, e:
        print "Can't save model fot the campaign. Error: " + str(e)
        return Response(status=status.HTTP_400_BAD_REQUEST)